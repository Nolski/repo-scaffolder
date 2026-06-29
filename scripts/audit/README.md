# DPG Readiness Audit

`run_audit.py` runs open-source checks against a repository and emits a normalized
JSON report (`audit-report.json`) keyed to the [DPG Standard indicators](../../maturity/indicators.md).
It is the evidence-gathering engine behind the `dpg-assess` Claude skill.

## Usage

```bash
python3 scripts/audit/run_audit.py <repo_path> --type software -o audit-report.json
```

- `--type` is `software` (default), `data`, or `content` — it determines which
  license allow-list (`maturity/licenses.json`) the detected license is checked against.
- Output goes to stdout unless `-o/--output` is given.

The script uses **only the Python standard library** and never crashes: any check
whose tool is missing reports `"status": "not_run"`.

## Optional tools (more tools → richer report)

| Tool | Installs | Feeds indicator(s) | Notes |
|---|---|---|---|
| [licensee](https://github.com/licensee/licensee) | `gem install licensee` | 2 (license) | Best SPDX detection. Falls back to text-sniffing if absent. |
| [reuse](https://reuse.software/) | `pipx install reuse` | 2 (license) | Alternative SPDX / compliance. |
| [gitleaks](https://github.com/gitleaks/gitleaks) | `brew install gitleaks` | 9A (secrets) | Already used in this repo's CI. |
| [trufflehog](https://github.com/trufflesecurity/trufflehog) | `brew install trufflehog` | 9A (secrets) | Fallback secret scanner. |
| [OpenSSF Scorecard](https://github.com/ossf/scorecard) | `go install github.com/ossf/scorecard/v5@latest` | 8, 9A | `--local` mode is limited; full checks need a GitHub remote + token. |
| [markdownlint](https://github.com/igorshubovych/markdownlint-cli) | `npm i -g markdownlint-cli` | 5 (docs) | Documentation cleanliness. |

## Report shape

```jsonc
{
  "schema": "dpg-audit-report/v1",
  "repo": "/abs/path",
  "project_type": "software",
  "tools_available": { "licensee": false, ... },
  "checks": {
    "license":      { "status": "ok|warn|fail|not_run", "evidence": [...], "detail": {...} },
    "files":        { ... },   // README, LICENSE, PRIVACY, CODE_OF_CONDUCT, GOVERNANCE, ...
    "sections":     { ... },   // README section coverage (SDG, about, install, data export, ...)
    "secrets":      { ... },
    "scorecard":    { ... },
    "docs":         { ... },
    "dependencies": { ... },
    "architecture": { ... }   // advisory: signals grouped by the 12 architecture dimensions
  }
}
```

The `architecture` check feeds the **advisory architecture lens** (see [`maturity/architecture.md`](../../maturity/architecture.md)). It does a bounded recursive walk and reports detected signals — containerization/IaC, API specs, i18n, offline/service-workers, tests, CI (flagging security scans), cloud-SDK reference counts, observability libs, architecture docs, SBOM. It is informational (presence/counts), not a pass/fail judgment, and does **not** affect the DPG tier.

See [`maturity/indicators.md`](../../maturity/indicators.md) for how each `checks` key
maps to a DPG indicator and what the `dpg-assess` skill does with it.

## Live-credential verification — `verify_secrets.py`

Detection (`run_audit.py`/gitleaks/trufflehog) finds credential *patterns*; it can't reliably
tell you which are **live**. `verify_secrets.py` attempts safe, read-only liveness probes for
the classes a DPG repo most often leaks:

```bash
python3 scripts/audit/verify_secrets.py <repo> --authorize [--gitleaks-report report.json]
```

- **AWS SES SMTP** (Server `email-smtp.*.amazonaws.com` + `AKIA…` username + password): SMTP
  `AUTH` handshake then quit — **no email is ever sent**. *This is the key gap:* TruffleHog
  does **not** verify SES SMTP creds (the password is derived, not the raw secret key), so it
  reports them "unverified" even when active. Config is parsed structurally (JSON-aware) so the
  password is paired from the *same* block.
- **AWS access key + secret**: STS `GetCallerIdentity` (read-only) via boto3.
- **JWTs / public embed links** (e.g. PowerBI "publish to web"): base64 decode for type/expiry
  (no network) + HTTP GET of already-public URLs. Flags these as *public-by-design data
  exposure*, not keys to rotate.

**Safety:** requires `--authorize` (deliberate opt-in); only run it on repos you own or are
authorized to test. All probes are read-only — no mail, no mutation, secrets masked in output.
The `dpg-assess` skill invokes this automatically for high-signal findings.
