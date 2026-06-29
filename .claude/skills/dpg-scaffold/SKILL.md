---
name: dpg-scaffold
description: Scaffold a new (greenfield) repository pre-populated with DPG-grade open-source files at a chosen maturity tier, using the cookiecutter templates in this project. Use when starting a brand-new project that should be DPG-ready from day one, or when the user asks to "create/bootstrap a new repo with the right open-source files". For assessing or fixing an EXISTING repo, use dpg-assess / dpg-remediate instead.
allowed-tools: Bash, Read, Glob
---

# DPG Greenfield Scaffold

Create a new repository seeded with the right governance, documentation, privacy, and
licensing files for its target DPG maturity tier.

## Procedure

0. **Locate the toolkit.** The cookiecutter templates live in the repo-scaffolder toolkit. Set
   `TOOLKIT` = the directory three levels above this skill's base directory (the "Base directory
   for this skill" path ends in `/.claude/skills/dpg-scaffold`; `TOOLKIT` is the part before
   `/.claude/`). The commands below use `$TOOLKIT` so they work from any current directory.
   (If installed separately from the toolkit, `$TOOLKIT` is your repo-scaffolder checkout.)

1. **Pick the tier.** Read `$TOOLKIT/maturity/tier-model.md` and help the user choose (0–4)
   based on intent. If unsure, walk them through `python3 "$TOOLKIT/tier-determiner.py"`.
   Higher tiers scaffold more files (privacy, governance, content-moderation as applicable).

2. **Run cookiecutter** for that tier, generating into the directory where the new project
   should live (cookiecutter creates a subfolder there):
   ```bash
   cookiecutter "$TOOLKIT" --directory=tier<N> --output-dir <DEST_DIR>
   ```
   Answer the prompts. Note the **license prompt** is mandatory and type-aware
   (software → OSI license; content → Creative Commons; data → Open Definition) — there is
   no CC0-for-software default. Allow-lists live in `$TOOLKIT/maturity/licenses.json`.

3. **Assess the result.** After generation, offer to run `dpg-assess` on the new repo to
   confirm it starts at the intended tier and to list any remaining judgment-based gaps
   (e.g. the maintainer still needs to write the real SDG relevance and privacy specifics).

## Notes

- Requires `cookiecutter` (`pip install -r "$TOOLKIT/requirements.txt"`). For GitHub repo creation the
  hooks use the `gh` CLI — that step is optional and prompted.
- This skill is for **new** repos. The bulk of the value for existing projects is in
  `dpg-assess` → `dpg-remediate`.
