# Remediation Templates ("parts bin")

DPG-grade artifacts the [`dpg-remediate`](../.claude/skills/dpg-remediate/SKILL.md) skill
instantiates into a repository to close gaps found by [`dpg-assess`](../.claude/skills/dpg-assess/SKILL.md).
They are also drawn on by the cookiecutter `tier*/` templates.

| Template | Closes indicator | Drop-in as |
|---|---|---|
| `PRIVACY.md` | 7, 9A | a top-level `PRIVACY.md` |
| `CONTENT_MODERATION.md` | 9B | a top-level `CONTENT_MODERATION.md` (only if user content) |
| `SDG_MAPPING.md` | 1 | a README section |
| `GOVERNANCE.md` | 3 | a top-level `GOVERNANCE.md` (replaces stub) |
| `DATA_EXPORT.md` | 6 | a README/docs section (only if data stored) |
| `PLATFORM_INDEPENDENCE.md` | 4 | a README/docs section |
| `CODE_OF_CONDUCT_additions.md` | 9C | appended to `CODE_OF_CONDUCT.md` |

Indicator **2** (license) is handled by the license chooser, not a template — pick an
approved SPDX license from `maturity/licenses.json` by project type. Indicators **5** and
**8** are remediated by editing the README / enabling CI & repo hygiene, not by a single file.

## Placeholder convention

Tokens use `{{ name }}` (Jinja-style, compatible with cookiecutter). Common tokens:
`{{ project_name }}`, `{{ contact_email }}`, `{{ date }}`. When `dpg-remediate` fills a
template it must replace every token with a real value (or a clearly-marked TODO), never
leave raw `{{ … }}` in the user's repo. The `…` prompts inside each template are meant to
be answered, not shipped verbatim.
