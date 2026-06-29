---
name: dpg-remediate
description: Guide a repository toward Digital Public Good (DPG) readiness by closing the gaps found in a DPG assessment. Instantiates DPG-grade artifacts (privacy policy, governance, content-moderation, SDG mapping, license fix, code-of-conduct additions), fills in placeholders, re-audits to confirm each fix, and at full readiness produces a pre-filled DPG nominee package for submission to the DPGA registry. Use when asked to fix, improve, or "get this repo to DPG status / the next maturity tier".
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# DPG Remediation

Take a repository from its current maturity tier toward **DPG eligibility** by closing
the indicators that block the next tier. This skill **edits the target repo**, so work
incrementally and confirm before large or destructive changes.

## Procedure

1. **Get the assessment.** Look for a recent `dpg-assessment.json` (in the target repo or
   `/tmp`). If none exists or it's stale, run the `dpg-assess` skill first. Read it to get
   `current_tier`, `target_tier`, the per-indicator `status`, and `blockers`.

2. **Read the playbook.** Read `maturity/indicators.md` (the `remediate:` row for each
   indicator), `maturity/tier-model.md`, and `templates/README.md` (which template closes
   which indicator + the placeholder convention).

3. **Work the blockers** for `target_tier`, one indicator at a time, in the gap report's
   priority order. For each:
   - **Instantiate the template** from `templates/` into the target repo (see mapping
     below). **Fill every `{{ … }}` token** with a real value derived from the repo
     (project name, contact, today's date) — never leave raw tokens. Replace the `…`
     prompts with project-specific content where you can infer it; where you genuinely
     can't, leave a clearly-marked `TODO:` and tell the user what to supply.
   - **Re-run the relevant audit check** (`python3 scripts/audit/run_audit.py <repo> --type <type>`)
     and confirm the indicator now passes. Report before/after.

4. **Repeat** until `target_tier` is reached, then offer to continue to the next tier.

5. **At Tier 4 (all 9 indicators met)** generate the **DPG nominee package**: a JSON object
   validated against `maturity/nominee-schema.json`, written to `dpg-nominee.json` in the
   repo. Populate `name`, `description`, `license[]` (SPDX + URL), `organizations[]`,
   `SDGs[]` (with evidence), `type`, `stage: "nominee"`, and optional `sectors`/`repositories`.
   Then point the user to <https://app.digitalpublicgoods.net> to submit.

## Indicator → action map

| Blocker | Action |
|---|---|
| 1 SDG relevance | add `templates/SDG_MAPPING.md` as a README section; capture SDGs for the nominee package |
| 2 License | **license chooser**: ask code/content/data, pick an approved SPDX id from `maturity/licenses.json`, write the real license text to `LICENSE`. Never write CC0 for software. |
| 3 Ownership | install/expand `templates/GOVERNANCE.md`; add an ownership line to README |
| 4 Platform independence | add `templates/PLATFORM_INDEPENDENCE.md` section |
| 5 Documentation | scaffold missing README sections (about/install/usage) + `docs/` as needed |
| 6 Data export | add `templates/DATA_EXPORT.md` section (skip if no data → mark N/A) |
| 7 Privacy | install `templates/PRIVACY.md` |
| 8 Standards/best practices | enable Scorecard-recommended hygiene: branch protection, CI, signed releases, dependency review; add a "Standards & Best Practices" README section citing Principles for Digital Development |
| 9A Data privacy & security | remediate any leaked secret first; add the data-security section of `PRIVACY.md` |
| 9B Content moderation | install `templates/CONTENT_MODERATION.md` (skip if no user content → mark N/A) |
| 9C Harassment protection | append `templates/CODE_OF_CONDUCT_additions.md` to `CODE_OF_CONDUCT.md` |

## License chooser (Indicator 2 — do this carefully)

1. Determine project `type` (software / content / data). Ask if unclear.
2. Read `maturity/licenses.json` → `categories[type].recommended_default_prompt` for the
   shortlist, or the full `spdx` list on request.
3. Present the options with one-line trade-offs (e.g. MIT = simplest; Apache-2.0 = patent
   grant; AGPL-3.0 = network copyleft). **Do not pick for the user** — there is no default.
4. Write the canonical license text for the chosen SPDX id to `LICENSE`, with the correct
   copyright holder/year. Re-audit to confirm `checks.license.status == "ok"`.

## Rules

- **Incremental & reversible.** One indicator per step; show the diff/new file and confirm
  before writing many files at once. Don't overwrite a non-stub existing policy without
  asking.
- **No raw placeholders** left in the user's repo, ever.
- **Honest re-audit.** Only mark an indicator fixed after the audit (or clear manual
  evidence) confirms it. If a tool was `not_run`, say the confirmation is partial.
- **Don't fake substance.** SDG relevance, privacy specifics, and moderation processes are
  the project's real commitments — draft them, but flag anything the maintainer must verify.
