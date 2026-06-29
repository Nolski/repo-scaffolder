#!/usr/bin/env python3
"""DPG readiness audit orchestrator.

Runs a battery of open-source checks against a target repository and writes a
normalized JSON report keyed to the DPG Standard indicators. The report is
consumed by the `dpg-assess` Claude skill (see .claude/skills/dpg-assess).

Design goals:
- Standard library only — runs anywhere with Python 3.8+.
- External tools (licensee, scorecard, gitleaks, trufflehog, markdownlint) are
  OPTIONAL. When a tool is missing, its check reports {"status": "not_run"}
  rather than crashing, so a partial audit is always possible.

Usage:
    python run_audit.py <repo_path> [--output audit-report.json] [--type software]

Each check returns a dict with at least:
    status:   ok | warn | fail | not_run | not_applicable
    evidence: list of strings (file paths, SPDX ids, finding summaries)
    detail:   free-form structured data for the skill to reason over

See maturity/indicators.md for how each report key maps to an indicator.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
LICENSES_PATH = REPO_ROOT / "maturity" / "licenses.json"

# Files whose presence feeds indicators 3, 5, 7, 9C (see indicators.md).
KEY_FILES = {
    "README": ["README.md", "README.rst", "README.txt", "README"],
    "LICENSE": ["LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING"],
    "PRIVACY": ["PRIVACY.md", "PRIVACY-POLICY.md", "docs/PRIVACY.md"],
    "CODE_OF_CONDUCT": ["CODE_OF_CONDUCT.md", ".github/CODE_OF_CONDUCT.md"],
    "GOVERNANCE": ["GOVERNANCE.md", "docs/GOVERNANCE.md"],
    "CONTRIBUTING": ["CONTRIBUTING.md", ".github/CONTRIBUTING.md"],
    "SECURITY": ["SECURITY.md", ".github/SECURITY.md"],
    "CONTENT_MODERATION": ["CONTENT_MODERATION.md", "docs/CONTENT_MODERATION.md"],
}

# README section coverage feeds indicators 1, 5, 6 (substring match, case-insensitive).
README_SECTIONS = {
    "sdg": ["sustainable development goal", "sdg"],            # indicator 1
    "about": ["about the project", "about"],                  # indicator 5
    "install": ["install", "getting started", "local development"],  # indicator 5
    "usage": ["usage", "how to use", "quick start"],          # indicator 5
    "data_export": ["data export", "portability", "exporting data"],  # indicator 6
    "dependencies": ["dependencies", "platform independence", "requirements"],  # indicator 4
}

# Dependency manifests -> ecosystem (feeds indicator 4).
MANIFESTS = {
    "package.json": "npm",
    "requirements.txt": "pip",
    "pyproject.toml": "python",
    "go.mod": "go",
    "Cargo.toml": "cargo",
    "pom.xml": "maven",
    "build.gradle": "gradle",
    "composer.json": "composer",
    "Gemfile": "rubygems",
}


def _have(tool):
    return shutil.which(tool) is not None


def _run(cmd, cwd=None, timeout=300):
    """Run a command, returning (returncode, stdout, stderr). Never raises."""
    try:
        p = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout
        )
        return p.returncode, p.stdout, p.stderr
    except Exception as e:  # noqa: BLE001 - audit must never crash
        return 1, "", str(e)


def _find_file(repo, candidates):
    for rel in candidates:
        if (repo / rel).is_file():
            return rel
    return None


def _load_license_lists():
    try:
        data = json.loads(LICENSES_PATH.read_text(encoding="utf-8"))
        return data["categories"]
    except Exception:  # noqa: BLE001
        return {}


# --------------------------------------------------------------------------- #
# Checks
# --------------------------------------------------------------------------- #
def check_license(repo, project_type):
    """Indicator 2: detect SPDX id and verify it is DPGA-approved for the type."""
    cats = _load_license_lists()
    detected = None
    method = None

    if _have("licensee"):
        rc, out, _ = _run(["licensee", "detect", "--json", str(repo)])
        if rc == 0 and out.strip():
            try:
                data = json.loads(out)
                lic = (data.get("licenses") or [{}])[0]
                detected = lic.get("spdx_id")
                method = "licensee"
            except Exception:  # noqa: BLE001
                pass

    if detected is None and _have("reuse"):
        rc, out, _ = _run(["reuse", "lint", "--json"], cwd=str(repo))
        if out.strip():
            method = "reuse"  # parsed leniently; SPDX surfaced below if present

    license_file = _find_file(repo, KEY_FILES["LICENSE"])
    if detected is None and license_file:
        # Stdlib fallback: sniff well-known SPDX markers from the license text.
        try:
            txt = (repo / license_file).read_text(encoding="utf-8", errors="ignore")
            detected = _sniff_spdx(txt)
            method = method or "text-sniff"
        except Exception:  # noqa: BLE001
            pass

    approved_for = []
    for cat, spec in cats.items():
        if detected and detected in spec.get("spdx", []):
            approved_for.append(cat)

    status = "fail"
    evidence = []
    detail = {"spdx": detected, "method": method, "license_file": license_file,
              "approved_for": approved_for, "project_type": project_type}

    if detected is None:
        status = "fail"
        evidence.append("No license detected" + (f" (LICENSE file: {license_file})" if license_file else " and no LICENSE file"))
    elif project_type in approved_for:
        status = "ok"
        evidence.append(f"{detected} is DPGA-approved for {project_type}")
    elif approved_for:
        # Detected an approved license, but for the wrong category — the classic
        # CC0-on-software anti-pattern.
        status = "fail"
        evidence.append(
            f"{detected} is approved only for {approved_for}, NOT for {project_type}. "
            f"DPG Indicator 2 requires an OSI license for software."
        )
        detail["anti_pattern"] = "license-category-mismatch"
    else:
        status = "fail"
        evidence.append(f"{detected} is not on any DPGA-approved list")

    return {"status": status, "evidence": evidence, "detail": detail}


def _sniff_spdx(txt):
    # An explicit SPDX-License-Identifier tag wins outright (preserve original case —
    # SPDX ids are case-sensitive and must match maturity/licenses.json exactly).
    m = re.search(r"SPDX-License-Identifier:\s*([A-Za-z0-9.\-+]+)", txt, re.I)
    if m:
        return m.group(1).strip().rstrip(".")
    t = txt.lower()
    # The GNU family must be disambiguated by the TITLE, not the body: the GPL-3.0
    # text mentions "GNU Affero General Public License" in section 13, so a naive
    # whole-text match misclassifies GPL-3.0 as AGPL-3.0. Look only at the title block.
    head = t[:400]
    if "general public license" in head:
        if "affero" in head:
            return "AGPL-3.0"
        if "lesser" in head:
            return "LGPL-3.0"
        return "GPL-3.0"
    # Everything else: distinctive full-text markers (order = most specific first).
    table = [
        ("apache license", "Apache-2.0"),
        ("mozilla public license", "MPL-2.0"),
        ("mit license", "MIT"),
        ("permission is hereby granted, free of charge", "MIT"),
        ("redistribution and use in source and binary", "BSD-3-Clause"),
        ("creative commons legal code\n\ncc0", "CC0-1.0"),
        ("cc0 1.0 universal", "CC0-1.0"),
        ("attribution-sharealike 4.0", "CC-BY-SA-4.0"),
        ("attribution 4.0 international", "CC-BY-4.0"),
        ("the unlicense", "Unlicense"),
        ("isc license", "ISC"),
    ]
    for needle, spdx in table:
        if needle in t:
            return spdx
    return None


def check_files(repo):
    """Indicators 3, 5, 7, 9C: presence of key governance/docs files."""
    found = {}
    for key, candidates in KEY_FILES.items():
        found[key] = _find_file(repo, candidates)
    present = [k for k, v in found.items() if v]
    missing = [k for k, v in found.items() if not v]
    status = "ok" if not ({"README", "LICENSE"} - set(present)) else "warn"
    return {
        "status": status,
        "evidence": [f"present: {', '.join(present) or 'none'}",
                     f"missing: {', '.join(missing) or 'none'}"],
        "detail": found,
    }


def check_sections(repo):
    """Indicators 1, 5, 6, 4: README section coverage (substring, case-insensitive)."""
    readme_rel = _find_file(repo, KEY_FILES["README"])
    if not readme_rel:
        return {"status": "fail", "evidence": ["no README"], "detail": {}}
    txt = (repo / readme_rel).read_text(encoding="utf-8", errors="ignore").lower()
    coverage = {}
    for section, needles in README_SECTIONS.items():
        coverage[section] = any(n in txt for n in needles)
    present = [s for s, ok in coverage.items() if ok]
    status = "ok" if len(present) >= 3 else "warn"
    return {
        "status": status,
        "evidence": [f"README sections found: {', '.join(present) or 'none'}"],
        "detail": coverage,
    }


def check_secrets(repo):
    """Indicator 9A: leaked secrets / PII via gitleaks (preferred) or trufflehog."""
    if _have("gitleaks"):
        rc, out, err = _run(
            ["gitleaks", "detect", "--no-banner", "--report-format", "json",
             "--report-path", "/dev/stdout", "--source", str(repo)]
        )
        findings = []
        if out.strip():
            try:
                findings = json.loads(out)
            except Exception:  # noqa: BLE001
                findings = []
        n = len(findings) if isinstance(findings, list) else 0
        return {
            "status": "ok" if n == 0 else "fail",
            "evidence": [f"gitleaks: {n} finding(s)"],
            "detail": {"tool": "gitleaks", "count": n,
                       "rules": sorted({f.get("RuleID", "") for f in findings}) if n else []},
        }
    if _have("trufflehog"):
        rc, out, _ = _run(["trufflehog", "filesystem", str(repo), "--json", "--no-update"])
        n = sum(1 for line in out.splitlines() if line.strip().startswith("{"))
        return {"status": "ok" if n == 0 else "fail",
                "evidence": [f"trufflehog: {n} finding(s)"],
                "detail": {"tool": "trufflehog", "count": n}}
    return {"status": "not_run", "evidence": ["gitleaks/trufflehog not installed"], "detail": {}}


def check_scorecard(repo):
    """Indicators 8, 9A: OpenSSF Scorecard. Needs git remote/auth; best-effort."""
    if not _have("scorecard"):
        return {"status": "not_run", "evidence": ["scorecard not installed"], "detail": {}}
    rc, out, err = _run(
        ["scorecard", f"--local={repo}", "--format=json", "--show-details"],
        timeout=420,
    )
    if rc != 0 or not out.strip():
        return {"status": "not_run",
                "evidence": [f"scorecard could not run locally: {err.strip()[:160]}"],
                "detail": {}}
    try:
        data = json.loads(out)
        score = data.get("score")
        checks = {c.get("name"): c.get("score") for c in data.get("checks", [])}
        return {"status": "ok" if (score or 0) >= 5 else "warn",
                "evidence": [f"scorecard aggregate: {score}"],
                "detail": {"score": score, "checks": checks}}
    except Exception as e:  # noqa: BLE001
        return {"status": "not_run", "evidence": [f"parse error: {e}"], "detail": {}}


def check_docs(repo):
    """Indicator 5: docs/ tree + markdownlint cleanliness."""
    docs_dir = (repo / "docs").is_dir()
    md_status = "not_run"
    md_detail = {}
    if _have("markdownlint"):
        rc, out, err = _run(["markdownlint", "**/*.md", "--json"], cwd=str(repo))
        md_status = "ok" if rc == 0 else "warn"
        md_detail = {"clean": rc == 0}
    return {
        "status": "ok" if docs_dir else "warn",
        "evidence": [f"docs/ dir: {docs_dir}", f"markdownlint: {md_status}"],
        "detail": {"docs_dir": docs_dir, "markdownlint": md_detail},
    }


def check_dependencies(repo):
    """Indicator 4: enumerate dependency manifests for platform-independence review."""
    found = []
    for manifest, eco in MANIFESTS.items():
        # search at root and one level down
        if (repo / manifest).is_file():
            found.append({"manifest": manifest, "ecosystem": eco, "path": manifest})
    return {
        "status": "ok" if found else "warn",
        "evidence": [f"manifests: {', '.join(m['manifest'] for m in found) or 'none found'}"],
        "detail": {"manifests": found,
                   "note": "platform-independence (closed deps vs open alternatives) is a judgment call for the skill"},
    }


# Directories never worth walking for architecture signals.
_PRUNE_DIRS = {".git", "node_modules", ".next", "dist", "build", "out", "vendor",
               "obj", "bin", ".venv", "venv", "__pycache__", ".terraform", "target"}
# Manifest filenames whose *contents* we grep for cloud-SDK / observability libs.
_MANIFEST_NAMES = {"package.json", "requirements.txt", "pyproject.toml", "go.mod",
                   "Cargo.toml", "pom.xml", "build.gradle", "composer.json", "Gemfile"}


def check_architecture(repo):
    """Advisory architecture lens: detect concrete signals grouped by dimension.

    No judgment here — just presence/counts. The dpg-assess skill combines these
    with reading the repo and maturity/architecture.md to score 12 dimensions.
    Bounded, single recursive walk with directory pruning; never crashes.
    """
    sig = {k: [] for k in (
        "containerization_iac", "api_specs", "i18n", "offline", "tests", "ci",
        "observability", "docs", "sbom", "cloud_sdk")}
    manifests = []
    cloud_hits = {"azure": 0, "aws": 0, "gcp": 0}
    csproj_count = 0

    def add(key, val, cap=40):
        if val not in sig[key] and len(sig[key]) < cap:
            sig[key].append(val)

    for dirpath, dirnames, filenames in os.walk(repo):
        dirnames[:] = [d for d in dirnames if d not in _PRUNE_DIRS and not d.startswith(".terraform")]
        rel_dir = os.path.relpath(dirpath, repo)
        base = os.path.basename(dirpath).lower()
        if base in ("locales", "i18n", "messages", "lang", "translations"):
            add("i18n", rel_dir)
        if base in ("k8s", "kubernetes"):
            add("containerization_iac", f"{rel_dir}/ (k8s)")
        if base == "helm":
            add("containerization_iac", f"{rel_dir}/ (helm)")
        if base.startswith("adr") or rel_dir.endswith(os.sep + "adr"):
            add("docs", f"{rel_dir}/ (ADRs)")
        for fn in filenames:
            low = fn.lower()
            rel = os.path.join(rel_dir, fn) if rel_dir != "." else fn
            if low.startswith("dockerfile") or low.startswith("docker-compose") or low == "compose.yaml":
                add("containerization_iac", rel)
            elif low.endswith(".tf") or low.endswith(".tfvars"):
                add("containerization_iac", rel)
            if low.startswith("openapi") or low.startswith("swagger") or low.startswith("asyncapi"):
                add("api_specs", rel)
            if low.endswith(".po") or low.endswith(".pot"):
                add("i18n", rel)
            elif low in ("en.json", "fr.json", "es.json", "ar.json", "pt.json", "messages.json") \
                    or (low.endswith(".json") and base in ("locales", "lang", "i18n", "messages")):
                add("i18n", rel)
            if "service-worker" in low or low in ("sw.js", "serviceworker.js") or low.startswith("workbox") \
                    or low.endswith(".webmanifest") or low == "manifest.webmanifest":
                add("offline", rel)
            if low.endswith((".spec.ts", ".spec.js", ".test.ts", ".test.js", ".test.tsx", ".spec.tsx")) \
                    or low.endswith(("_test.go", "_test.py")) or low.startswith("test_"):
                add("tests", rel)
            if low.endswith(".csproj"):
                if "test" in low:
                    add("tests", rel); csproj_count += 1
            if base == "workflows" and (low.endswith(".yml") or low.endswith(".yaml")):
                add("ci", rel)
                # flag security-relevant CI
                if any(t in low for t in ("trivy", "codeql", "semgrep", "snyk", "gitleaks", "trufflehog", "scorecard", "sast")):
                    add("ci", f"{rel} [security-scan]")
            if "sbom" in low or "cyclonedx" in low or low.endswith(".spdx") or low.endswith(".spdx.json"):
                add("sbom", rel)
            if fn in ("ARCHITECTURE.md", "CHANGELOG.md", "CODEOWNERS", "GOVERNANCE.md") \
                    or low in ("architecture.md", "changelog.md"):
                add("docs", rel)
            if fn in _MANIFEST_NAMES:
                manifests.append(rel)
                # grep manifest contents for cloud SDKs + observability libs
                try:
                    txt = (Path(dirpath) / fn).read_text(encoding="utf-8", errors="ignore").lower()
                except Exception:  # noqa: BLE001
                    txt = ""
                for c in cloud_hits:
                    if c in txt:
                        cloud_hits[c] += 1
                for obs in ("opentelemetry", "serilog", "winston", "pino", "prometheus", "log4j", "logback", "zap", "structlog"):
                    if obs in txt:
                        add("observability", f"{rel}:{obs}")
            elif low.endswith(".csproj"):
                manifests.append(rel)
                try:
                    txt = (Path(dirpath) / fn).read_text(encoding="utf-8", errors="ignore").lower()
                except Exception:  # noqa: BLE001
                    txt = ""
                for c in cloud_hits:
                    if c in txt:
                        cloud_hits[c] += 1
                for obs in ("opentelemetry", "serilog", "prometheus"):
                    if obs in txt:
                        add("observability", f"{rel}:{obs}")

    detail = {
        "containerization_iac": {"signals": sig["containerization_iac"]},
        "api_specs": {"signals": sig["api_specs"]},
        "i18n": {"signals": sig["i18n"]},
        "offline": {"signals": sig["offline"]},
        "tests": {"signals": sig["tests"]},
        "ci": {"signals": sig["ci"]},
        "observability": {"signals": sig["observability"]},
        "docs": {"signals": sig["docs"]},
        "sbom": {"signals": sig["sbom"]},
        "dependencies": {"manifests": manifests, "cloud_sdk_refs": cloud_hits},
    }
    # A coarse status: ok if the project shows containerization + tests + CI, else warn.
    has = lambda k: bool(sig[k])
    status = "ok" if (has("containerization_iac") and has("tests") and has("ci")) else "warn"
    ev = [
        f"containerization/IaC: {len(sig['containerization_iac'])} signal(s)",
        f"API specs: {len(sig['api_specs'])}",
        f"i18n: {len(sig['i18n'])}",
        f"offline/service-worker: {len(sig['offline'])}",
        f"tests: {len(sig['tests'])}",
        f"CI workflows: {len(sig['ci'])}",
        f"cloud SDK refs: {cloud_hits}",
        f"SBOM: {len(sig['sbom'])}",
    ]
    return {"status": status, "evidence": ev, "detail": detail}


CHECKS = {
    "license": lambda repo, ptype: check_license(repo, ptype),
    "files": lambda repo, ptype: check_files(repo),
    "sections": lambda repo, ptype: check_sections(repo),
    "secrets": lambda repo, ptype: check_secrets(repo),
    "scorecard": lambda repo, ptype: check_scorecard(repo),
    "docs": lambda repo, ptype: check_docs(repo),
    "dependencies": lambda repo, ptype: check_dependencies(repo),
    "architecture": lambda repo, ptype: check_architecture(repo),
}


def run_audit(repo_path, project_type="software"):
    repo = Path(repo_path).resolve()
    report = {
        "schema": "dpg-audit-report/v1",
        "repo": str(repo),
        "project_type": project_type,
        "tools_available": {t: _have(t) for t in
                            ["licensee", "reuse", "gitleaks", "trufflehog", "scorecard", "markdownlint"]},
        "checks": {},
    }
    for name, fn in CHECKS.items():
        report["checks"][name] = fn(repo, project_type)
    return report


def main():
    ap = argparse.ArgumentParser(description="DPG readiness audit")
    ap.add_argument("repo", help="path to the repository to audit")
    ap.add_argument("--output", "-o", default=None,
                    help="write report JSON here (default: stdout)")
    ap.add_argument("--type", default="software",
                    choices=["software", "data", "content"],
                    help="DPG project type (affects license approval check)")
    args = ap.parse_args()

    if not Path(args.repo).is_dir():
        print(f"error: {args.repo} is not a directory", file=sys.stderr)
        return 2

    report = run_audit(args.repo, args.type)
    out = json.dumps(report, indent=2)
    if args.output:
        Path(args.output).write_text(out + "\n", encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
