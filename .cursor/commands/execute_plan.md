You are now executing the approved plan.

## ⚠️ Pre-Flight Check

**Before starting implementation, verify:**
- [ ] `/pre_implementation_checklist` has been run (or manually verified)
- [ ] Design decisions document exists: `.ai/context/design_decisions.md`
- [ ] Field mapping matrix is documented (if data transformations are involved)
- [ ] Data format specifications are clear (if API/formats are involved)

**If any items above are missing, stop and inform the user to complete them first.**

---

**Context Integration:**
First, check for and read context files:
- Read the plan file
- `.ai/context/design_decisions.md` (if exists) - use for design guidance
- `.ai/context/last_explore.md` (if exists) - use for validation and scope boundaries

At the start of execution:
- Restate "What we're building" in 3 bullets (derive from plan TLDR or `last_explore.md` Success Criteria)
- List explicit non-goals (derive from `last_explore.md` Constraints and what's explicitly out of scope)
- Reference design decisions document if it exists

Rules:
- Follow the plan exactly
- Follow design decisions from `.ai/context/design_decisions.md`
- Do not introduce new scope
- Do not refactor unrelated code
- If you discover missing information, pause and ask
- **When adding API endpoints:** Update every entry point in `docs/ARCHITECTURE.md`; prefer shared handlers over duplicated route files

Process:
- Implement one step at a time
- Mark completed steps clearly
- Explain briefly what was changed after each step
- **For data format conversions: Verify conversion logic matches documented formats**
- **For state updates: Use functional updates when updating state based on props/state**
- During execution, when making a tradeoff:
  - Check `last_explore.md` Constraints and Risks to avoid scope drift
  - Check `design_decisions.md` for documented decisions
  - Avoid decisions that contradict stated constraints

**Special Checks:**
- **API Endpoints:** Shared handlers + all entry points in `docs/ARCHITECTURE.md` updated
- **Data Formats:** When transforming data, verify format conversions match documented specs
- **React State:** When updating state that depends on props/state, use functional updates
- **Content Rendering:** If adding formatted content, implement rendering strategy from design decisions
- **Static HTML generators:** Layout/spacing uses component CSS in scanned `input.css` (or equivalent), not Tailwind utility strings alone in TS templates; rebuild + browser-check footers/nav rows before calling UI done

Validation (at the end):
- Validate implemented behavior against `last_explore.md` Success Criteria (if exists)
- Validate against Acceptance Criteria from plan or `last_explore.md` (if exists)
- Verify field mappings were implemented correctly (if applicable)
- Verify format conversions work as documented (if applicable)
- Ensure no constraints were violated

## Local Dev Verification (required before handoff)

- [ ] If feature reads persisted user/data store: **seed script or documented integration path** exists in `package.json` (do not document scripts that are not implemented)
- [ ] `docs/DEV_RUNBOOK.md` updated with new scripts, ports, or recovery steps
- [ ] Agent ran `npm test` and `npm run build` for affected workspaces (or stack-equivalent)
- [ ] Agent stated exact commands for the user to see the happy path (e.g. seed → open page)
- [ ] If editing shared workspace packages: noted whether consumers import `dist/` or `src/` — rebuild/restart as needed

## Deployment Verification (required when feature ships via GHA, cron, or static hosting)

Skip only if the feature has **no** automated deploy and **no** public URL.

- [ ] Repo secrets documented in runbook (e.g. `ANTHROPIC_API_KEY`); never committed
- [ ] Real git remote set (`gh repo create` / `git remote set-url`) — no `YOU/repo` placeholder
- [ ] Manual workflow dispatch succeeds (or cron path documented)
- [ ] Expected artifact exists on remote (commit, file, or deploy output)
- [ ] **Public URL loads correctly** (hard refresh): styled UI if applicable, not raw HTML
- [ ] **GitHub Pages project sites:** asset paths are **relative** (`assets/style.css`, `../assets/style.css`) — not root-absolute `/assets/…` (see [GITHUB_PAGES_CHECKLIST.md](docs/GITHUB_PAGES_CHECKLIST.md))
- [ ] Timezone consistency: commit messages and dated output folders use the same TZ
- [ ] After GHA bot commits: local push may need `git pull --rebase origin main`
- [ ] After bot commits dated artifacts (`briefings/`, reports): deploy workflow ran or was dispatched manually
- [ ] **Same-day pipeline re-run:** If verifying prompt/output-format changes, prefer `npm test` + GHA dispatch — local re-run when today's output folder exists can reshuffle rankings or drift metrics (see [WORKFLOW_COURSE.md](docs/WORKFLOW_COURSE.md))

If a step feels unsafe or unclear, stop and ask before proceeding.

---

## Run mode

If `.ai/context/run_config.json` has `mode: "autonomous"`:
- Do not run organism build here; build runs after `/qa_checklist` when applicable.
- Run `npm run genesis:run -- step-complete execute_plan` when done.
- **Immediately** continue with `/code_review` logic in the same session.

If interactive: wait for confirmation before `/code_review`. Do not prompt for build at this step.

**Mid-run `--autonomous`:** If the user message includes `--autonomous`, run `npm run genesis:run -- init --autonomous`, then continue remaining steps per [genesis_run.md](genesis_run.md) Agent behavior §1.

---

**During implementation (optional):**
- Run `/tdd` for complex logic requiring test-driven development

**After completion:**
- Review implementation against design decisions
- Document any deviations from the plan
- To push to remote: run in your terminal: `git add -A && git commit -m '...' && git push origin main`
- **Do not run the organism build here.** Build runs **after `/qa_checklist`** when tests pass and the genome/runtime deliverable changed (see qa_checklist.md **Build handoff**).
- **Next step:** Run `/code_review`, then `/qa_checklist`.

**Next:** When implementation is done, run `/code_review` then `/qa_checklist`. After QA, run the build if applicable (`node scripts/build.js`), then `/postmortem`. See `.cursor/commands/workflow.md` for the full workflow.
