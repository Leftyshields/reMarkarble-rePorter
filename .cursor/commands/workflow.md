# Application Development Workflow (Project Genesis)

This document outlines the recommended workflow for building features in a **Genesis-instantiated application** (your product repo). It is copied from [Project Genesis](https://github.com/Leftyshields/project-genesis) via `instantiate.sh` — **customize** backend paths and doc links for your stack after instantiating.

See also: [Product vs genome mission](docs/PRODUCT_VS_GENOME_MISSION.md).

---

## 🔄 Genesis Nine-Step Loop (`/genesis_run`)

Mandatory order for Interactive and Autonomous modes (only pause behavior differs):

| # | Step | Command |
|---|------|---------|
| 1 | Capture | `/capture_issue` |
| 2 | Explore | `/explore` |
| 3 | Design | `/design_decisions` |
| 4 | Create Plan | `/create_plan` |
| 5 | Pre-Implementation | `/pre_implementation_checklist` |
| 6 | Execute | `/execute_plan` |
| 7 | Code Review | `/code_review` |
| 8 | QA | `/qa_checklist` |
| 9 | Postmortem | `/postmortem` |

**Entry:** `/genesis_run` (interactive) or `/genesis_run --autonomous` (or `GENESIS_AUTONOMOUS=true`). Add **`--autonomous` on any step** to upgrade mid-run and finish remaining steps hands-off. Optional after step 9: `/reflection` (documentation handoff), `/security_scan`, `/peer_review`, deploy.

| Optional | Command | When |
|----------|---------|------|
| Reflection | `/reflection` | Hand off **updated documentation** (README, workflow, runbooks) — not required every run |
| Security | `/security_scan` | Sensitive data, pre-release |
| Peer review | `/peer_review` | Complex/high-impact changes |
| Wrap-up | `/project_wrap_up` | Full repo handover audit |

---

## 🔄 Complete Feature Development Workflow

### Phase 1: Planning & Design

1. **Capture the Issue** (`/capture_issue`)
   - Document the problem, current behavior, desired behavior
   - Assign issue ID and priority
   
   **Next:** Run `/explore` to analyze requirements

2. **Explore Requirements** (`/explore`)
   - Analyze the problem in detail
   - Define success criteria
   - Identify constraints and risks
   - List open questions
   
   **Next:** Run `/design_decisions` to document design choices

3. **Document Design Decisions** (`/design_decisions`)
   - Answer all open questions from planning
   - Define field update strategies
   - Specify rendering approaches (if formatted content)
   - Document integration points
   - **For multi-source data:** document provenance (API vs seed vs manual) and reconnect cleanup
   
   **Next:** Run `/create_plan` to create execution plan

4. **Create Execution Plan** (`/create_plan`)
   - Generate detailed implementation plan
   - Include field mappings (if data transformations)
   - Include format conversions (if needed)
   - Include local dev parity checks (if API endpoints)
   - **Issue ID in `last_plan.md` must match `last_capture.md`**
   
   **Next:** Run `/pre_implementation_checklist` to verify readiness

5. **Pre-Implementation Checklist** (`/pre_implementation_checklist`)
   - Verify design decisions exist
   - Verify field mappings are documented
   - Verify format conversions are specified
   - Verify local dev parity plan (if needed)
   - Verify rendering strategy (if needed)
   
   **Next:** Run `/execute_plan` to begin implementation

---

### Phase 2: Implementation

6. **Execute Plan** (`/execute_plan`)
   - Follow the execution plan step-by-step
   - Reference design decisions for guidance
   - Apply backend changes to **all documented entry points** (see `docs/ARCHITECTURE.md`)
   - Use functional state updates when updating state based on props/state
   - Implement format conversions as documented
   - **Ship local dev tooling** (seed scripts, npm scripts, runbook rows) when UI needs data to demo
   
   **Optional:** Run `/tdd` for complex logic (test-driven development)
   
   **Required before next feature:** Run `/code_review`, then `/qa_checklist` (do not skip after MVP milestones)

---

### Phase 3: Quality Assurance

7. **Code Review** (`/code_review`) — *standard*
   - Automated security check, correctness, architecture, code quality, performance
   - Review specified scope (file, recent changes, or feature)
   - When changing README or docs that describe code (e.g. runtime steps, API order), verify step order and names against the actual source.
   
   **Next:** Fix any issues found, then run `/security_scan` (optional) or `/qa_checklist`

8. **Security Scan** (`/security_scan`) — *optional*
   - Dedicated pass: secrets, dependencies, input safety, auth, data at rest, encryption, proprietary/IP
   - Use when handling sensitive data, before release, or for compliance; complements code_review
   
   **Next:** Fix critical/high findings, then run `/qa_checklist`

9. **QA Checklist** (`/qa_checklist`) — *standard*
   - **Automated:** agent runs `npm test` and builds for affected workspaces
   - **Manual:** checklist for happy path, edge cases, error handling, visual/UX
   - **Build handoff:** after QA, run organism build when genome/runtime changed (`node scripts/build.js`) — see qa_checklist completion response
   - Save issue-scoped checklist to `.ai/context/qa_checklist_<feature>.md` when helpful
   
   **Next:** Run `/postmortem` (and optional build before postmortem when `.genome/` changed)

10. **Peer Review** (`/peer_review`) — *optional*
   - Human code review for complex or high-impact changes
   - Evaluate suggestions critically; accept or reject with rationale
   
   **Next:** Address review feedback, then proceed to deployment

---

### Phase 4: Deployment & Reflection

11. **Deploy**
    - Test in staging (if available)
    - Deploy to production
    - Monitor for issues
   
   **Next:** Run `/postmortem` to reflect on the process

11b. **Ship / Push to Git**
    - To push to GitHub, run in **your terminal**: `git add -A && git commit -m 'Description' && git push origin main`. Staging (`git add -A`) must be done before commit so your changes are included. The agent may not have access to push to your remote.
   
   **Next:** Verify on GitHub; then run `/postmortem` if not already done

12. **Postmortem** (`/postmortem`) — *standard*
    - Analyze friction points, rework, missing docs
    - Document lessons learned; propose workflow/doc updates
    - Create `docs/CLOSURE_EPH-*.md` for the issue
    
    **Next:** Run `/project_wrap_up` (optional) or start next feature

13. **Project Wrap-up** (`/project_wrap_up`) — *optional*
    - Final handover: security audit, context synthesis, onboarding docs, next-op briefing
    - Use when handing off, releasing, or preparing for the next contributor or AI agent
    
    **Next:** Start next feature or hand off

### Backlog / GitHub sync

- When a backlog story is already satisfied (deliverable exists and meets “Done when”): verify the deliverable, close the corresponding GitHub issue, then run `/postmortem` if desired.
- When a story is completed in a run: close (or update) the matching GitHub issue so the tracker stays in sync with progress.

---

## 🚀 Quick Start Workflow

For smaller changes or bug fixes:

1. `/capture_issue` - Document the issue
2. `/execute_plan` - Implement the fix
3. `/code_review` - Automated review
4. `/security_scan` - Optional, if the change touches auth, secrets, or sensitive data
5. `/peer_review` - Review changes (optional for trivial fixes)
6. Deploy

---

## 📋 Standard vs optional steps

| Step | Type | What it does |
|------|------|----------------|
| `/genesis_run` | Standard | Master entry: nine-step loop; interactive or `--autonomous` |
| `/capture_issue` | Standard | Log the problem, current/desired behavior, priority; get issue ID |
| `/explore` | Standard | Deep-dive requirements, constraints, risks; persist exploration snapshot |
| `/create_plan` | Standard | Turn exploration into atomic implementation steps |
| `/design_decisions` | Standard | Lock design choices, field mappings, integration points before coding |
| `/pre_implementation_checklist` | Standard | Confirm plan and design are complete; gate before coding |
| `/execute_plan` | Standard | Implement step-by-step using plan and design decisions |
| `/tdd` | Optional | Red–green–refactor for complex logic during implementation |
| `/code_review` | Standard | Automated review: security, correctness, architecture, quality, performance |
| `/security_scan` | Optional | Dedicated security pass: secrets, deps, auth, data at rest, encryption, proprietary/IP |
| `/qa_checklist` | Standard | Automated tests + human manual-test checklist (happy path, edge cases, UX) |
| `/peer_review` | Optional | Human review of changes; accept/reject feedback with rationale |
| `/postmortem` | Standard | Reflect on friction and rework; closure doc; improve process and docs |
| `/reflection` | Optional | **Documentation handoff** — update README, workflow, runbooks, command prompts for the next contributor |
| `/project_wrap_up` | Optional | Handover: security audit, onboarding docs, next-op briefing |
| `/learning_opportunity` | Optional | Capture insights anytime |
| `/show_context` | Utility | Show current context files |
| `/workflow` | Utility | Show this workflow |

**Standard** = recommended for every feature or bugfix. **Optional** = use when scope, risk, or handover justifies it.

---

## After instantiating a new project

1. Copy [docs/ARCHITECTURE_TEMPLATE.md](docs/ARCHITECTURE_TEMPLATE.md) → `docs/ARCHITECTURE.md` and fill in entry points.
2. Copy [docs/DEV_RUNBOOK_TEMPLATE.md](docs/DEV_RUNBOOK_TEMPLATE.md) → `docs/DEV_RUNBOOK.md` as you debug.
3. Add a **“This repo”** subsection below with your backend paths and runbook link.
4. Read [Product vs genome mission](docs/PRODUCT_VS_GENOME_MISSION.md).
5. If shipping GitHub Pages: read [GITHUB_PAGES_CHECKLIST.md](docs/GITHUB_PAGES_CHECKLIST.md).

### This repo — reMarkable Weekly Notes

| Concern | Path |
|---------|------|
| Product package | `src/remarkable_weekly/` |
| Tests | `tests/` (`pytest`); Genesis Node suite via `npm run test:node` |
| CLI | `remarkable-weekly` / `python -m remarkable_weekly` |
| Output | `weekly-notes/` |
| Architecture | [docs/ARCHITECTURE.md](../../docs/ARCHITECTURE.md) |
| Runbook | [docs/DEV_RUNBOOK.md](../../docs/DEV_RUNBOOK.md) |
| Product mission | [docs/MISSION.md](../../docs/MISSION.md) |

`npm test` runs Node organism tests **then** `pytest -q`. Use `.venv` + `pip install -e ".[dev]"` on PEP 668 hosts.

---

## ⚠️ Common Mistakes to Avoid

1. **Skipping Design Decisions** - Always run `/design_decisions` before implementation
2. **Forgetting backend parity** - Document all HTTP entry points in `docs/ARCHITECTURE.md`; update every entry point that mounts your API router (not a fixed pair of filenames)
3. **Skipping MVP QA gate** - After `/execute_plan` on a milestone, run `/qa_checklist` and `/code_review` before the next `/capture_issue`
4. **Confusing product mission with `.genome/mission.md`** - App goals live in capture/plan/closure docs; genome mission is framework metadata
5. **Stale Closures** - Use functional state updates when updating state based on props/state
6. **Missing Format Conversions** - Document and implement all format conversions
7. **Skipping Pre-Implementation Checklist** - Verify all requirements before coding
8. **Forgetting to stage before commit** - Run `git add -A` before `git commit` when shipping changes
9. **Documenting npm scripts that don't exist** - Runbook must not require scripts missing from `package.json`
10. **Stale `last_plan.md`** - Plan issue ID must match current capture before `/execute_plan`
11. **Monorepo shared package drift** - Rebuild shared workspace packages after editing `src/` if consumers import `dist/`
12. **QA-driven silent scope** - New requests during QA need a mini capture or plan note, not ad-hoc patches
13. **Local-only “done” for scheduled products** - MVP includes secrets, GHA dispatch, and verifying the public artifact
14. **GitHub Pages root-absolute paths** - On `username.github.io/repo/`, use relative asset paths (`assets/style.css`), not `/assets/`
15. **Placeholder git remote** - Replace `YOU/repo` with `gh repo create` before first push
16. **Stale external API IDs** - Verify LLM/vendor model names at implement time; provider IDs retire
17. **GHA bot vs local git** - Run `git pull --rebase` after Actions commits before pushing locally
18. **Same-day pipeline re-run** - Re-running a dated job when today's output folder already exists can reshuffle rankings (soft-dedup) and drift metrics (live API refresh). Prefer tests + GHA dispatch for prompt/format verification
19. **Stale plan on follow-on issues** - Run `/create_plan` for the new issue ID; do not reuse a closed issue's `execution_plan.md`
20. **GHA artifact without deploy** - Bot commits to `briefings/` or `dist/` may not trigger Pages; verify deploy workflow or dispatch manually
21. **Tailwind in HTML generators** - Spacing/layout in TS string templates must use **component classes in scanned CSS** (e.g. `site/assets/input.css`), not utility strings alone; add explicit HTML separators for inline link rows; verify with rebuild + browser refresh
22. **Partial implementations vs revised capture** - Before `/execute_plan`, reconcile flag-gated or WIP code against capture; update experiment JSON and design doc in the same milestone when direction changes
23. **Automated tests ≠ layout UX** - Unit/integration green does not verify footer spacing, column balance, or mobile order; `/qa_checklist` must include browser checks for static HTML layout changes
24. **Overwriting `last_capture.md`** - Do not start a new issue capture until the prior issue has a closure doc (or use issue-scoped capture filenames)
25. **Forgetting `step-complete`** - In `/genesis_run` flows, call `node scripts/genesis-run.js step-complete <step>` after each step in interactive mode; otherwise `validate-gate` and QA will fail on step order
26. **Mode switch without reset** - `init --autonomous` upgrades interactive mid-run (keeps steps); delete `run_config.json` only for a fresh run or autonomous → interactive downgrade
27. **Expecting autonomous without the flag** - `/genesis_run` alone is interactive; pass `--autonomous` (or set `GENESIS_AUTONOMOUS=true`) for end-to-end; the agent should ask which mode you want if the flag is omitted on `/genesis_run` entry
28. **Mid-run takeover** - Append `--autonomous` to any step command (`/explore --autonomous`) after starting interactive; agent runs `init --autonomous` and completes remaining steps without pause

---

## 📚 Related Documentation (templates — copy into your app repo)

- [Workflow course](docs/WORKFLOW_COURSE.md) — case studies and anti-patterns
- [Architecture template](docs/ARCHITECTURE_TEMPLATE.md)
- [Dev runbook template](docs/DEV_RUNBOOK_TEMPLATE.md)
- [GitHub Pages checklist](docs/GITHUB_PAGES_CHECKLIST.md)
- [Product vs genome mission](docs/PRODUCT_VS_GENOME_MISSION.md)
- [Instantiated app feedback log](docs/INSTANTIATED_APP_FEEDBACK.md)
- [Blueprint](docs/BLUEPRINT.md) — Genesis framework architecture

---

**Last Updated:** 2026-07-02
