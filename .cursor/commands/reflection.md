# Reflection — Documentation Handoff (Optional)

Produce **updated documentation** for the next contributor or AI agent. This is **not** step 9 of the genesis loop — run **after** `/postmortem` when good handoff docs are part of the deliverable.

---

## Postmortem vs Reflection

| | `/postmortem` (required, step 9) | `/reflection` (optional) |
|---|----------------------------------|---------------------------|
| Focus | Process friction, rework, closure | **Documentation handoff** |
| Question | What went wrong in the workflow? | What should the next person read? |
| Typical outputs | `postmortem_<ISSUE_ID>.md`, `docs/CLOSURE_<ISSUE_ID>.md` | `reflection_<ISSUE_ID>.md`, edits to README, workflow, runbooks |

---

## When to Run

- Milestone or feature complete and docs drifted from reality
- Handing off to another developer or agent
- Template/command fixes should propagate (Genesis upstream or instantiated app)
- Autonomous run with `--reflect` on `/genesis_run` (after postmortem)

**Skip** when the change is trivial and existing docs are accurate.

---

## Inputs

Read from `.ai/context/` and repo as needed:

- `last_capture.md`, `last_explore.md`, `design_decisions.md`, `last_plan.md`
- `postmortem_<ISSUE_ID>.md`, `docs/CLOSURE_<ISSUE_ID>.md`
- `code_review_changelog.md`, `test_results.json`, QA artifacts
- Current `README.md`, `.cursor/commands/workflow.md`, relevant runbooks

---

## Outputs

1. **`.ai/context/reflection_<ISSUE_ID>.md`** — handoff summary:
   - What changed (product + workflow)
   - Which docs were updated and why
   - How to run / test / deploy (current commands only — verify against `package.json`)
   - Open items deferred to backlog

2. **Documentation updates** (as scope requires — edit files, do not only describe in chat):
   - `README.md` — quick start, modes, commands
   - `.cursor/commands/workflow.md` — step order, new commands
   - `docs/DEV_RUNBOOK.md` or template-derived runbook rows
   - Command prompts under `.cursor/commands/` if behavior changed

Use **replace/merge** intentionally: replace stale sections; merge new rows into runbooks.

---

## Autonomous Mode

When `run_config.json` has `mode: "autonomous"` and `--reflect` was set at run start:

- Run automatically after postmortem completes
- Apply doc updates in the same session
- Log all touched files in `reflection_<ISSUE_ID>.md`

Do **not** skip postmortem; reflection builds on its closure outputs.

---

## Rules

- Do not invent npm scripts or env vars — verify against repo
- Prefer minimal, accurate doc diffs over long narrative
- If no doc updates are needed, write `reflection_<ISSUE_ID>.md` stating "no doc drift" and exit

---

**Workflow Position:** Optional — after `/postmortem` (step 9).

**Previous Step:** `/postmortem`

**Next Steps:** Ship (`git add -A && git commit && git push`), `/project_wrap_up` (optional), or next `/capture_issue`

See `.cursor/commands/workflow.md` for the complete development workflow.
