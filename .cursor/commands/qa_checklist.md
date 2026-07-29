Create a QA checklist for this feature.

## Automated (agent runs first)

- Run `node scripts/genesis-run.js test` (or `npm test` if no run config)
- Report pass/fail from `.ai/context/test_results.json`

### Autonomous mode

When `run_config.json` has `mode: "autonomous"`:
1. Run `node scripts/genesis-run.js test`.
2. If tests fail, perform **one** remediation: apply safe fixes from code review, then `node scripts/genesis-run.js test --attempt 2 --remediation`.
3. Log unresolved failures; **do not** halt — proceed to `/postmortem`.
4. Manual checklist items: save as deferred in `.ai/context/qa_checklist_<feature-slug>.md` with `- [ ] (deferred autonomous)` prefix.
5. If `.genome/` changed or plan requires runtime verification: run `node scripts/build.js` when tests pass.
6. Run `npm run genesis:run -- step-complete qa --artifacts .ai/context/test_results.json,.ai/context/qa_checklist_<feature-slug>.md`
7. Include **Build handoff** section in QA completion response (see below).
8. **Immediately** continue with `/postmortem` logic in the same session — do not wait for user confirmation.

## Manual (human validation)

Create a checklist the tester can follow. Include:
- Happy path
- Common edge cases
- Failure states
- Visual / UX checks

Save to `.ai/context/qa_checklist_<feature-slug>.md` when the feature is non-trivial.

Format as simple `- [ ]` items with pre-flight section.

### Static site / generated HTML (when layout or CSS changes)

After rebuild, **open the affected pages in a browser** (local static server or staging URL). Automated tests rarely catch:

- Footer/nav link spacing and wrapping
- Column balance and mobile stack order
- Missing Tailwind rules from TS template literals

Check desktop and at least one narrow viewport (e.g. 390px).

---

## QA completion response (required)

When QA finishes, **always** end with this structure in chat (do not skip):

```markdown
## QA complete

### Automated tests
- [pass/fail] — summary from `test_results.json` or `npm test`
- **If failed:** list unresolved failures prominently; note remediation attempt if any

### Manual checklist
- [done / deferred / N/A] — link to `.ai/context/qa_checklist_<feature>.md` if created

### Build handoff
[Choose one and explain]

**A — Genome / runtime deliverable changed** (`.genome/` edited or plan requires organism run):
- Interactive: ask **"Ready to run the organism build?"** — if yes, run:
  ```bash
  node scripts/build.js
  ```
  (or `node scripts/build.js .genome/mission.md` for a specific path)
- Autonomous: run `node scripts/build.js` automatically when tests pass and genome changed; include build output in the summary.

**B — Workflow / tooling only** (no genome or runtime changes this issue):
- State: **Build N/A** — no organism build for this deliverable.

### Run the organism (when build applies)
After a successful build:
```bash
node scripts/run-path.js .genome/mission.md
```
See [lib/README.md](../../lib/README.md) for guardrails, repair, and options.

### Next step
Run `/postmortem` (step 9). Optional: `/reflection` if documentation handoff is needed.
```

The **build phase takes over after QA**, not after `/execute_plan`. Tests and manual checks gate the runtime invocation.

**Mid-run `--autonomous`:** If the user message includes `--autonomous`, run `npm run genesis:run -- init --autonomous`, then continue remaining steps per [genesis_run.md](genesis_run.md) Agent behavior §1.

---

**Workflow Position:** Run this after `/code_review` (automated review).

**Previous Step:** `/code_review` - Automated security and quality review

**Next Steps:**
1. Fix any issues found during QA
2. **Build (when genome/runtime changed):** confirm and run `node scripts/build.js` — see **QA completion response** above
3. Run `/postmortem` to reflect on the run and close the issue
4. Run `/peer_review` for human code review (optional, for complex changes)
5. Deploy the feature

See `.cursor/commands/workflow.md` for the complete development workflow.
