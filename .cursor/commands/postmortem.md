We are performing a process postmortem.

Do NOT focus on code correctness.

Analyze:
- Where friction occurred
- Where rework happened
- What was misunderstood
- What instructions or documentation were missing

Then answer:
1. Root cause
2. What should change in prompts or docs
3. How to prevent this next time

**Also document:**
- Which workflow phases were **skipped** (e.g. `/code_review`, `/qa_checklist`, `/security_scan`) and whether that is acceptable for this milestone

Finally, propose updates to:
- System instructions
- Documentation
- Workflow rules

**Required outputs:**
1. `.ai/context/postmortem_<ISSUE_ID>.md` — friction analysis (this session)
2. `docs/CLOSURE_<ISSUE_ID>.md` — what shipped, deferred, ship commands
3. Update `.cursor/commands/workflow.md` or related commands if lessons apply
4. **Path A (app repo):** Append a section to `docs/INSTANTIATED_APP_FEEDBACK.md` and open a PR (or push) from your app repo
5. **Path B (Genesis upstream, when templates should change):** Open a PR to [Project Genesis](https://github.com/Leftyshields/project-genesis) updating commands/templates; link the app-repo feedback entry. See **How to add entries** in `docs/INSTANTIATED_APP_FEEDBACK.md`

### Autonomous run summary (when `run_config.json` mode is autonomous)

Add these sections to `postmortem_<ISSUE_ID>.md`:

```markdown
## Run Summary
- Mode, run_id, issue_id from run_config.json

## Design Decisions
- Key decisions + rationale (from design_decisions.md)

## Code Review Fixes
- From code_review_changelog.md

## QA / Tests
- From test_results.json (pass/fail, remediation)

## Manual Review Items
- From code_review_changelog manual_review_needed + deferred QA items
```

Run `npm run genesis:run -- step-complete postmortem --artifacts .ai/context/postmortem_<ISSUE_ID>.md,docs/CLOSURE_<ISSUE_ID>.md`

If `run_config.json` has `reflect: true`, **immediately** continue with `/reflection` in the same session.

If `mode` is `autonomous`, this is the final mandatory step — summarize the full run; do not ask the user to confirm or run another command.

**Mid-run `--autonomous`:** If the user message includes `--autonomous`, run `npm run genesis:run -- init --autonomous`, then continue remaining steps per [genesis_run.md](genesis_run.md) Agent behavior §1.

---

**Workflow Position:** Run this after feature deployment to reflect on the process and improve future workflows.

**Then — Close issue and ship:**
- Close the issue (e.g. create or update a closure doc such as `docs/CLOSURE_EPH-*.md`, or close the GitHub issue if applicable).
- Remind the user: to get changes on GitHub, run in **their terminal**: `git add -A && git commit -m 'Closes EPH-XXXX' && git push origin main`. The agent may not have access to push to the user's remote. Staging (`git add -A`) must be done before commit.

**Next Steps:**
1. Implement suggested documentation updates
2. Update workflow commands based on findings
3. Apply lessons learned to next feature development
4. **Optional:** Run `/reflection` when the deliverable includes updated documentation for handoff (README, workflow, runbooks)

See `.cursor/commands/workflow.md` for the complete development workflow.
