#!/usr/bin/env python3
"""Live-credential VERIFICATION for DPG secret findings (read-only triage).

Detection tools (gitleaks/trufflehog) report *patterns*; they frequently cannot
tell you whether a leaked credential is actually LIVE. Notably, TruffleHog does
NOT verify AWS SES SMTP credentials (the key-id is an SMTP username paired with a
*derived* SMTP password, not the raw secret access key), so it reports them as
"unverified" even when active. This script closes that gap by attempting safe,
read-only liveness probes for the credential classes a DPG repo most often leaks.

SAFETY — this tool makes authenticated calls to the credential's own provider:
  * Only run it on a repository you OWN or are explicitly authorized to test.
  * Probes are READ-ONLY: SMTP AUTH then QUIT (no mail), AWS STS GetCallerIdentity
    (no mutation), JWT base64 decode (no network), HTTP GET of already-public URLs.
  * It NEVER sends email, writes to storage, or mutates any resource.
  * Secret values are masked in all output.
You must pass --authorize to run (a deliberate, auditable opt-in).

Usage:
    python verify_secrets.py <repo_path> --authorize [--gitleaks-report report.json]
    # If no report is given and gitleaks is installed, it is run over git history.

Findings source: a gitleaks JSON report (preferred) or a fresh gitleaks run.
For each high-signal finding the script reads the file blob at the finding's commit
to pair related values (e.g. SMTP server+username+password) before probing.
"""
import argparse
import base64
import json
import os
import re
import shutil
import smtplib
import ssl
import subprocess
import sys
import urllib.request
from pathlib import Path


def _mask(s, keep=4):
    if not s:
        return "<empty>"
    return (s[:keep] + "…" + s[-2:]) if len(s) > keep + 2 else "***"


def _run(cmd, cwd=None, timeout=300):
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except Exception as e:  # noqa: BLE001
        return 1, "", str(e)


def _blob_at(repo, commit, path):
    """Return file contents at a commit (or working tree if commit falsy)."""
    if commit:
        rc, out, _ = _run(["git", "show", f"{commit}:{path}"], cwd=str(repo))
        if rc == 0:
            return out
    p = repo / path
    return p.read_text(encoding="utf-8", errors="ignore") if p.is_file() else ""


def _get_findings(repo, report):
    if report and Path(report).is_file():
        try:
            return json.loads(Path(report).read_text())
        except Exception:  # noqa: BLE001
            pass
    if shutil.which("gitleaks"):
        rc, out, _ = _run(["gitleaks", "detect", "--no-banner", "--report-format", "json",
                           "--report-path", "/dev/stdout", "--source", str(repo)])
        try:
            return json.loads(out) if out.strip() else []
        except Exception:  # noqa: BLE001
            return []
    return []


# --------------------------------------------------------------------------- #
# Verifiers (all read-only)
# --------------------------------------------------------------------------- #
def verify_ses_smtp(repo, findings):
    """AWS SES SMTP: find Server(email-smtp.*.amazonaws.com)+Username(AKIA…)+Password
    sets in the files flagged by gitleaks, and attempt an SMTP AUTH handshake.
    The single most important check — TruffleHog cannot do this.

    Pairing must keep server/username/password from the SAME config block, so JSON
    is parsed structurally (a flat global regex would mis-pair the password with an
    unrelated 'password' field elsewhere in the file → false 'not live')."""
    results = []
    files = {(f.get("File"), f.get("Commit")) for f in findings if f.get("File")}
    for path, commit in sorted(files):
        txt = _blob_at(repo, commit, path)
        if "email-smtp" not in txt.lower():
            continue
        for srv, user, pw in _extract_smtp_sets(txt):
            verdict = _probe_smtp(srv, user, pw)
            results.append({"type": "aws-ses-smtp", "file": path, "commit": (commit or "")[:12],
                            "server": srv, "username": _mask(user), "verdict": verdict})
    return results


def _extract_smtp_sets(txt):
    """Yield (server, username, password) triples kept within one config block.
    JSON-aware (walks objects); falls back to proximity windows for .env/ini."""
    sets = []
    # 1) JSON: walk every object, pick ones whose values include an SES server.
    try:
        data = json.loads(txt)

        def walk(obj):
            if isinstance(obj, dict):
                ci = {k.lower(): v for k, v in obj.items() if isinstance(v, str)}
                srv = next((v for v in ci.values() if re.search(r'email-smtp\.[\w.-]+amazonaws\.com', v)), None)
                if srv:
                    user = next((ci[k] for k in ("username", "user", "smtpusername") if k in ci), None)
                    pw = next((ci[k] for k in ("password", "pass", "smtppassword") if k in ci), None)
                    if user and pw:
                        sets.append((re.search(r'email-smtp\.[\w.-]+amazonaws\.com', srv).group(0), user, pw))
                for v in obj.values():
                    walk(v)
            elif isinstance(obj, list):
                for v in obj:
                    walk(v)

        walk(data)
        if sets:
            return sets
    except Exception:  # noqa: BLE001 - not JSON, fall through
        pass
    # 2) Proximity fallback (.env / ini / unparsable JSON): pair within a window
    #    after each email-smtp occurrence.
    for m in re.finditer(r'(email-smtp\.[\w.-]+amazonaws\.com)', txt):
        window = txt[m.start(): m.start() + 600]
        user = _search(window, r'(AKIA[0-9A-Z]{16})')
        pw = _search(window, r'["\']?[Pp]ass(?:word)?["\']?\s*[:=]\s*["\']?([^"\'\s,}]{8,})')
        if user and pw:
            sets.append((m.group(1), user, pw))
    return sets


def _probe_smtp(server, user, pw):
    for port in (587, 2587):
        try:
            s = smtplib.SMTP(server, port, timeout=25)
            s.ehlo(); s.starttls(context=ssl.create_default_context()); s.ehlo()
            try:
                s.login(user, pw)
                return "LIVE — auth succeeded (credential ACTIVE; no mail sent)"
            except smtplib.SMTPAuthenticationError as e:
                return f"not live — auth rejected ({e.smtp_code})"
            finally:
                try: s.quit()
                except Exception: pass
        except Exception:  # noqa: BLE001 - try next port
            continue
    return "inconclusive — could not connect (port 587/2587 blocked?)"


def verify_aws_keys(repo, findings):
    """Raw AWS access key + secret: AKIA… + a 40-char secret in the same file →
    STS GetCallerIdentity (read-only). Uses boto3 if available."""
    results = []
    files = {(f.get("File"), f.get("Commit")) for f in findings
             if f.get("RuleID", "").startswith("aws") and f.get("File")}
    try:
        import boto3  # noqa: F401
        have_boto = True
    except Exception:  # noqa: BLE001
        have_boto = False
    for path, commit in sorted(files):
        txt = _blob_at(repo, commit, path)
        if "email-smtp" in txt.lower():
            continue  # handled by SES verifier
        key = _search(txt, r'(AKIA[0-9A-Z]{16})')
        secret = _search(txt, r'(?<![A-Za-z0-9/+=])([A-Za-z0-9/+=]{40})(?![A-Za-z0-9/+=])')
        if not (key and secret):
            if key:
                results.append({"type": "aws-key", "file": path, "commit": (commit or "")[:12],
                                "key": _mask(key), "verdict": "unverifiable — no paired secret access key found in file"})
            continue
        verdict = _probe_aws(key, secret) if have_boto else "skipped — boto3 not installed"
        results.append({"type": "aws-key", "file": path, "commit": (commit or "")[:12],
                        "key": _mask(key), "verdict": verdict})
    return results


def _probe_aws(key, secret):
    try:
        import boto3
        from botocore.config import Config
        sts = boto3.client("sts", aws_access_key_id=key, aws_secret_access_key=secret,
                           config=Config(connect_timeout=15, read_timeout=15, retries={"max_attempts": 1}))
        ident = sts.get_caller_identity()
        acct = ident.get("Account", "")
        return f"LIVE — STS accepted (account {acct[:4]}…)"
    except Exception as e:  # noqa: BLE001
        name = type(e).__name__
        if "ClientError" in name or "Invalid" in str(e) or "SignatureDoesNotMatch" in str(e):
            return "not live — STS rejected the credentials"
        return f"inconclusive — {name}: {str(e)[:80]}"


def verify_tokens_and_links(repo, findings):
    """JWTs / public embed links: decode (no network) for expiry & type; GET
    already-public URLs to confirm they resolve."""
    results = []
    files = {(f.get("File"), f.get("Commit")) for f in findings if f.get("File")}
    seen = set()
    for path, commit in sorted(files):
        txt = _blob_at(repo, commit, path)
        # public embed URLs (PowerBI publish-to-web etc.)
        for url in re.findall(r'https://app\.powerbi\.com/view\?r=[A-Za-z0-9._-]+', txt):
            if url in seen:
                continue
            seen.add(url)
            tok = url.split("r=", 1)[1]
            kind = _classify_jwt(tok)
            status = _http_status(url)
            results.append({"type": "powerbi-publish-to-web", "file": path,
                            "detail": kind, "verdict": f"PUBLIC link, HTTP {status} (public by design — review data exposure, not a key to rotate)"})
        # standalone JWTs
        for tok in set(re.findall(r'eyJ[A-Za-z0-9_-]{6,}\.[A-Za-z0-9_-]{6,}\.[A-Za-z0-9_-]+', txt)):
            if tok in seen:
                continue
            seen.add(tok)
            results.append({"type": "jwt", "file": path, "detail": _classify_jwt(tok),
                            "verdict": _jwt_expiry(tok)})
    return results


def _classify_jwt(tok):
    obj = _b64json(tok)
    if isinstance(obj, dict):
        if {"k", "t"} <= set(obj):
            return "PowerBI publish-to-web token ({k,t,c} shape)"
        return "JSON token keys: " + ",".join(list(obj)[:6])
    parts = tok.split(".")
    if len(parts) == 3:
        payload = _b64json(parts[1])
        if isinstance(payload, dict):
            return "JWT iss=%s aud=%s" % (str(payload.get("iss"))[:24], str(payload.get("aud"))[:24])
    return "opaque token"


def _jwt_expiry(tok):
    parts = tok.split(".")
    if len(parts) != 3:
        return "not a JWT — cannot decode expiry"
    payload = _b64json(parts[1])
    if not isinstance(payload, dict) or "exp" not in payload:
        return "decoded, but no exp claim (cannot determine expiry without network/secret)"
    # NOTE: time-based; pass current epoch in if you need a hard verdict.
    return f"JWT exp claim = {payload['exp']} (compare to now; past = expired/dead)"


def _b64json(s):
    try:
        s = s.split(".")[1] if s.count(".") == 2 else s  # JWT payload if full JWT
    except Exception:  # noqa: BLE001
        pass
    try:
        return json.loads(base64.urlsafe_b64decode(s + "=" * (-len(s) % 4)))
    except Exception:  # noqa: BLE001
        return None


def _http_status(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as r:  # noqa: S310 - public URL, GET only
            return r.status
    except Exception as e:  # noqa: BLE001
        code = getattr(e, "code", None)
        return code if code else f"error({type(e).__name__})"


def _search(txt, pat):
    m = re.search(pat, txt)
    return m.group(1) if m else None


def main():
    ap = argparse.ArgumentParser(description="Verify whether leaked credentials are LIVE (read-only).")
    ap.add_argument("repo")
    ap.add_argument("--authorize", action="store_true",
                    help="confirm you own / are authorized to test this repo's credentials")
    ap.add_argument("--gitleaks-report", default=None)
    ap.add_argument("--json", action="store_true", help="emit JSON")
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    if not repo.is_dir():
        print(f"error: {repo} is not a directory", file=sys.stderr); return 2
    if not args.authorize:
        print("REFUSING: live verification makes authenticated calls to credential providers.\n"
              "Re-run with --authorize only on a repo you own or are authorized to test.", file=sys.stderr)
        return 3

    findings = _get_findings(repo, args.gitleaks_report)
    out = {
        "repo": str(repo),
        "findings_examined": len(findings),
        "ses_smtp": verify_ses_smtp(repo, findings),
        "aws_keys": verify_aws_keys(repo, findings),
        "tokens_and_links": verify_tokens_and_links(repo, findings),
    }
    if args.json:
        print(json.dumps(out, indent=2)); return 0

    print(f"# Live-credential verification — {repo}")
    print(f"(examined {len(findings)} gitleaks finding(s); probes are read-only — no mail, no mutation)\n")
    any_live = False
    for section, label in (("ses_smtp", "AWS SES SMTP"), ("aws_keys", "AWS access keys"),
                           ("tokens_and_links", "Tokens & public links")):
        rows = out[section]
        print(f"## {label}: {len(rows) or 'none'}")
        for r in rows:
            v = r.get("verdict", "")
            if v.startswith("LIVE"):
                any_live = True
            loc = r.get("file", "") + (f"@{r['commit']}" if r.get("commit") else "")
            print(f"  - [{r['type']}] {loc} {r.get('username') or r.get('key') or r.get('detail') or ''}")
            print(f"      → {v}")
        print()
    if any_live:
        print("⚠️  At least one credential is LIVE. Rotate/deactivate it at the provider, then purge from git history.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
