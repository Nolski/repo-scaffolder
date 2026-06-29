# Scoring Rubric & Output Templates

Detailed rules for `dpg-assess`. Keep the main SKILL.md lean; this is loaded when needed.

## Status definitions

| Status | Meaning |
|---|---|
| `met` | Requirement satisfied with concrete evidence. |
| `partial` | Started but incomplete (e.g. a stub PRIVACY.md, or SDG mentioned without target linkage). Never satisfies a mandatory indicator. |
| `unmet` | No evidence found. |
| `not-applicable` | Indicator doesn't apply (e.g. 6/9B for a project that stores no data/user-content). Counts as satisfied for tier purposes — but justify why it's N/A. |

## Per-indicator scoring cues

- **1 SDG relevance** — `met` only if a specific SDG *and* a plausible link to its targets is statable. README mention without substance = `partial`. No conceivable link = `unmet` (this gates Tier 2+).
- **2 License** — driven by `checks.license`. `ok`→`met`; `license-category-mismatch` or no license→`unmet`. CC0-on-software is always `unmet`.
- **3 Ownership** — `met` if owner is unambiguous (LICENSE copyright line + README/GOVERNANCE ownership statement, or CODEOWNERS). Vague/absent→`partial`/`unmet`.
- **4 Platform independence** — read `checks.dependencies`; `met` if no hard proprietary lock-in OR open alternatives are documented. Undocumented closed deps→`partial`.
- **5 Documentation** — `checks.files.README` + `checks.sections` + `checks.docs`. `met` if README covers about/install/usage and complexity is matched by docs depth.
- **6 Data export** — `not-applicable` if no data stored; else `met` only with a documented non-proprietary export/API.
- **7 Privacy & laws** — `checks.files.PRIVACY`. `met` if a privacy policy covers the 6 Enhanced-Privacy-Framework questions; stub→`partial`; absent (and PII likely)→`unmet`.
- **8 Standards & best practices** — `checks.scorecard` (if run) + judgment vs Principles for Digital Development. No scorecard → score on observable CI/branch-protection/release hygiene and mark confidence partial.
- **9A Data privacy & security** — `checks.secrets` must be clean; PII handling documented. Any leaked secret→`unmet`.
- **9B Inappropriate/illegal content** — `not-applicable` if no user-generated content; else needs CONTENT_MODERATION policy (incl. CSAM)→else `unmet`.
- **9C Harassment protection** — `checks.files.CODE_OF_CONDUCT` + harassment/underage coverage. CoC present but silent on underage safety→`partial`.

## Gap report template (markdown)

```markdown
# DPG Readiness: <repo name>

**Current tier: <N> — <name>.  Target: Tier <N+1>.**
<one-line verdict>

> Audit confidence: <full | partial — tools not run: gitleaks, scorecard, ...>

## Indicators
| # | Indicator | Status | Evidence | Notes |
|---|-----------|--------|----------|-------|
| 1 | SDG relevance | ... | ... | ... |
| 2 | Approved open license | ... | ... | ... |
| 3 | Clear ownership | ... | ... | ... |
| 4 | Platform independence | ... | ... | ... |
| 5 | Documentation | ... | ... | ... |
| 6 | Non-PII data extraction | ... | ... | ... |
| 7 | Privacy & applicable laws | ... | ... | ... |
| 8 | Standards & best practices | ... | ... | ... |
| 9A | Data privacy & security | ... | ... | ... |
| 9B | Inappropriate/illegal content | ... | ... | ... |
| 9C | Protection from harassment | ... | ... | ... |

## To reach Tier <N+1>, fix (in priority order):
1. <indicator> — <what to do> → remediable via `dpg-remediate`
2. ...

## Already strong
- ...

## Architecture (advisory — does not change the tier)
| Dimension | Rating | Evidence | Related indicator |
|-----------|--------|----------|-------------------|
| Modularity & separation | ... | ... | 4,5,8 |
| API-first & interoperability | ... | ... | 4,5,8 |
| Platform independence / cloud-agnosticism | ... | ... | 4 |
| Scalability & performance | ... | ... | 8 |
| Offline & low-connectivity | ... | ... | 8 |
| Localization & accessibility | ... | ... | 7,8,9 |
| Security architecture | ... | ... | 7,8,9A |
| Data portability & open formats | ... | ... | 6,4,7 |
| Testing & CI/CD | ... | ... | 8,5,9A |
| Observability | ... | ... | 8,5 |
| Documentation | ... | ... | 5,8 |
| Maintainability & community | ... | ... | 3,5,8 |

**Architectural strengths:** ...
**Architectural risks:** ... (note which DPG indicator each endangers)
```

## `dpg-assessment.json` shape

```jsonc
{
  "schema": "dpg-assessment/v1",
  "repo": "<path>",
  "project_type": "software",
  "current_tier": 1,
  "target_tier": 2,
  "audit_confidence": "partial",
  "tools_not_run": ["gitleaks", "scorecard"],
  "indicators": {
    "1":  { "status": "unmet",   "evidence": "no SDG section", "remediation": "SDG_MAPPING" },
    "2":  { "status": "unmet",   "evidence": "CC0 on software", "remediation": "license-chooser" },
    "3":  { "status": "met",     "evidence": "LICENSE + README owner" },
    "4":  { "status": "partial", "evidence": "..." },
    "5":  { "status": "met",     "evidence": "..." },
    "6":  { "status": "not-applicable", "evidence": "stores no data" },
    "7":  { "status": "unmet",   "evidence": "no PRIVACY.md", "remediation": "PRIVACY" },
    "8":  { "status": "partial", "evidence": "..." },
    "9A": { "status": "met",     "evidence": "gitleaks clean" },
    "9B": { "status": "not-applicable", "evidence": "no user content" },
    "9C": { "status": "partial", "evidence": "CoC present, no underage policy", "remediation": "CODE_OF_CONDUCT" }
  },
  "blockers": ["1", "2"],
  "architecture": {
    "dimensions": {
      "modularity":               { "rating": "strong",   "evidence": "..." },
      "api_first":                { "rating": "adequate", "evidence": "..." },
      "platform_independence":    { "rating": "weak",     "evidence": "..." },
      "scalability":              { "rating": "adequate", "evidence": "..." },
      "offline_low_connectivity": { "rating": "weak",     "evidence": "..." },
      "localization_accessibility": { "rating": "strong", "evidence": "..." },
      "security_architecture":    { "rating": "weak",     "evidence": "..." },
      "data_portability":         { "rating": "adequate", "evidence": "..." },
      "testing_cicd":             { "rating": "adequate", "evidence": "..." },
      "observability":            { "rating": "weak",     "evidence": "..." },
      "documentation":            { "rating": "strong",   "evidence": "..." },
      "maintainability":          { "rating": "adequate", "evidence": "..." }
    },
    "strengths": ["..."],
    "risks": [{ "dimension": "platform_independence", "endangers_indicator": "4", "note": "..." }],
    "advisory_note": "Does not change current_tier/blockers."
  }
}
```

`remediation` keys map to `templates/` artifacts (see `dpg-remediate`).

## Architecture scoring cues (per dimension)

Rate `strong` / `adequate` / `weak` / `n/a`. Lead with the audit's `checks.architecture` signals, then read the repo. Full definitions in `maturity/architecture.md`.

- **modularity** — clear layer/module separation; no god-modules. Signal: directory structure.
- **api_first** — `strong` if a machine-readable API spec (OpenAPI/AsyncAPI) exists + versioning; `weak` if APIs exist but undocumented; `n/a` for non-service apps.
- **platform_independence** — `weak` if heavy single-cloud SDK refs (`detail.dependencies.cloud_sdk_refs`) with no abstraction/open alternatives; `strong` if containerized + IaC + cloud-agnostic.
- **scalability** — stateless + queues/cache; judgment.
- **offline_low_connectivity** — `strong` if service workers / sync; `weak` if none and the app is field-facing/low-connectivity; `n/a` if irrelevant (e.g. internal admin-only).
- **localization_accessibility** — i18n signals + WCAG evidence. `strong` if multi-locale files present.
- **security_architecture** — combine with `checks.secrets` + `checks.scorecard`: OIDC/RBAC good; committed secrets or low Scorecard → `weak`.
- **data_portability** — non-proprietary export + documented schema → `strong`; `n/a` if no data stored.
- **testing_cicd** — test signals + CI workflows (esp. security scans).
- **observability** — structured logging/metrics/tracing libs (`detail.observability`); often `weak`/undetected — say "not detected in manifests" rather than "absent".
- **documentation** — ARCHITECTURE.md/ADRs + README depth (cross-check `checks.docs`).
- **maintainability** — CODEOWNERS/GOVERNANCE, changelog, release cadence.

**Never let architecture change `current_tier`, `target_tier`, `blockers`, or any indicator `status`.** Instead, in `risks`, name the DPG indicator each weak dimension endangers.
