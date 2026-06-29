---
name: dpg-assess
description: Assess a repository's Digital Public Good (DPG) readiness against the DPG Standard's 9 indicators. Runs an open-source audit (license, security, secrets, docs, file/section presence), classifies the repo's maturity tier (0-4), and produces an indicator-by-indicator gap report plus a machine-readable dpg-assessment.json. Use when asked to evaluate, score, or check a repo's DPG/open-source maturity or "how close is this to being a DPG".
allowed-tools: Bash, Read, Glob, Grep, Write
---

# DPG Readiness Assessment

Assess how close a repository is to being a **Digital Public Good** (per the [DPG Standard](https://www.digitalpublicgoods.net/standard)) and report exactly what blocks the next maturity tier.

## Inputs

- **Target repo**: the path to assess. Default to the current working directory unless the user names another path.
- **Project type**: `software` (default), `data`, or `content` — affects which license is "approved". Ask only if ambiguous.

## Procedure

0. **Locate the toolkit.** This skill ships inside the repo-scaffolder toolkit, which also holds the audit scripts and knowledge files. Set `TOOLKIT` = the directory three levels above this skill's base directory (the "Base directory for this skill" path ends in `/.claude/skills/dpg-assess`; `TOOLKIT` is the part before `/.claude/`). Everything below uses absolute paths under `$TOOLKIT`, so it works no matter which project is the current directory. (If this skill was installed separately from the toolkit repo, `$TOOLKIT` is wherever your repo-scaffolder checkout lives — confirm with the user if unsure.)

1. **Run the audit** on the target repo (the project being assessed — it can live anywhere and need not be the current directory):
   ```bash
   python3 "$TOOLKIT/scripts/audit/run_audit.py" <TARGET_REPO> --type <TYPE> -o /tmp/dpg-audit-report.json
   ```
   Then read `/tmp/dpg-audit-report.json`. Note which tools were `not_run` — the report says so under `tools_available` — and surface that as a confidence caveat.

2. **Load the knowledge core.** Read `$TOOLKIT/maturity/indicators.md` (what each indicator requires + how to detect it) and `$TOOLKIT/maturity/tier-model.md` (the tier ladder + classification algorithm). Read `rubric.md` in this skill's own directory for the scoring rules.

3. **Score each of the 9 indicators** (1, 2, 3, 4, 5, 6, 7, 8, 9A, 9B, 9C) as `met` / `partial` / `unmet` / `not-applicable`. For `auto`/`hybrid` indicators, lead with the audit signal; for `judgment` indicators (1 SDG relevance, 6 data export applicability, 9B content moderation), **read the actual repo** (README, source, docs) and reason — do not guess from the audit alone. Always attach evidence: a file path, URL, or audit finding.

4. **Classify the tier** using the algorithm in `tier-model.md`: current tier = highest fully-achieved tier; target = next up; blockers = mandatory indicators at the target tier that are not `met`/`not-applicable`.

5. **Architecture assessment (advisory).** Read `$TOOLKIT/maturity/architecture.md`. Combine the audit's `checks.architecture` signals with reading the repo to score the **12 architecture dimensions** (`strong`/`adequate`/`weak`/`n/a`) per the cues in `rubric.md`. This is a **diagnostic lens — it does NOT change the tier or the indicator statuses.** Its job is to explain *why* an indicator is fragile and surface architectural risks the binary indicators miss (e.g. cloud lock-in behind Indicator 4, no offline support, missing API spec). Where a dimension materially strengthens or weakens indicators 4/5/6/8/9A, say so explicitly. Skip this step only if the user asked for a quick indicator-only check.

6. **Emit two artifacts:**
   - A human-readable **gap report** (markdown) — see the template in `rubric.md`. Lead with the tier verdict, then a 9-row indicator table, then the prioritized "to reach Tier N+1, fix these" list, then the **advisory architecture section** (12-dimension table + strengths/risks).
   - A machine-readable **`dpg-assessment.json`** written to the target repo (or `/tmp` if read-only), shaped per `rubric.md` (including the `architecture` block) so `dpg-remediate` can consume it.

## Rules

- **Always run the FULL audit.** Before auditing, install any missing tools (`gitleaks`, `trufflehog`, `licensee`, `scorecard`, `markdownlint`) — see `$TOOLKIT/scripts/audit/README.md` for install commands — so no check reports `not_run`. Only fall back to a partial audit if an install genuinely fails, and say so.
- Be honest about confidence. If a tool truly could not run, say the related findings are partial.
- **Verify high-signal secret findings — don't trust "0 verified".** When `checks.secrets` returns high-signal hits (AWS `AKIA…`, SES SMTP config, tokens, committed `.env`/`appsettings`), attempt liveness verification with `python3 "$TOOLKIT/scripts/audit/verify_secrets.py" <repo> --authorize --gitleaks-report <report>`. It does read-only probes (SMTP `AUTH` then quit — **no mail**; AWS STS GetCallerIdentity; JWT decode; GET of public URLs) and catches what scanners miss — notably **TruffleHog does NOT verify AWS SES SMTP credentials**, so its "0 verified" is a false negative for them. **Only run `--authorize` on a repo the user owns or is authorized to test** (confirm if unsure). Report any **LIVE** credential as an urgent, time-sensitive finding (rotate at the provider → purge from history), and distinguish true secrets from public-by-design links (e.g. a PowerBI "publish to web" URL is a data-exposure question, not a key to rotate).
- **Never** call CC0-on-software acceptable — the audit flags `license-category-mismatch`; explain it (CC0 is fine for data/content, invalid for software under Indicator 2).
- Indicator 1 (SDG relevance) is a **gate**: a repo with zero plausible SDG link cannot reach Tier 2+, regardless of code quality.
- Do not modify the target repo. Assessment is read-only except for writing the report files. Remediation is the separate `dpg-remediate` skill — offer it as the next step.
