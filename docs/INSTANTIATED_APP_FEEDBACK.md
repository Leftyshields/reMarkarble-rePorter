# Instantiated App Feedback Log

Changelog of workflow improvements derived from real app development (postmortems). Use when updating Genesis templates and Cursor commands.

---

## 2026-07-28 — reMarkarble-rePorter (Weekly Notes Pipeline, EPH-20260728-RJ01)

**Source:** Greenfield instantiate from project-genesis; `/genesis_run` autonomous (capture → postmortem). Product is Python CLI alongside Node organism scaffold.

### Friction observed

| Area | Issue |
|------|--------|
| Dual test stacks | Default `npm test` (Node) did not run product `pytest` until package.json updated mid-review |
| PEP 668 | Host blocked system `pip install`; `.venv` required |
| Live adapters | Autonomous greenfield cannot validate unofficial reMarkable cloud shapes without tokens |
| Open questions | Autonomous defaults for categories/auth/week/packaging without Creator pause |
| Git bootstrap | Instantiated dish had no `git init`; Path A feedback PR blocked |

### Root cause (process)

Genesis QA gate assumes `npm test` is the product truth. Instantiated apps whose product language is not Node need an explicit test-wiring step before `/qa_checklist`.

### Suggested Genesis template updates (Path B — not yet upstreamed)

- `/pre_implementation_checklist` or `/execute_plan`: “If product ≠ Node, wire `package.json` `test` (or document dual suites) so genesis-run QA covers product tests”
- `DEV_RUNBOOK_TEMPLATE`: Python/`venv`/PEP 668 note
- Instantiation docs: recommend `git init` immediately after `instantiate.sh`

### Reference

- Closure: [docs/CLOSURE_EPH-20260728-RJ01.md](CLOSURE_EPH-20260728-RJ01.md)
- Postmortem: `.ai/context/postmortem_EPH-20260728-RJ01.md`

---

## 2026-05-31 — Wallet Watcher (Transactions, EPH-20260531-H3M8)


**Source:** Greenfield feature after MVP; full Genesis workflow (capture → explore → design → plan → execute → code review → QA → postmortem).

### Friction observed

| Area | Issue |
|------|--------|
| Local dev parity | Runbook referenced seed script before it existed in `package.json` |
| Execute handoff | Feature “done” but UI empty without user-driven seed/debug |
| Monorepo | API imported shared package from `dist/`; edits silent until rebuild |
| Emulator lifecycle | Port conflicts, duplicate emulator instances blocked QA |
| Planning order | `/design_decisions` before `/create_plan`; stale plan file passed gate |
| Multi-source data | Seed + vendor API data indistinguishable until late QA |
| QA scope | Relink, source column, subscription fixes added ad-hoc during validation |

### Root cause (process)

Local dev parity was documented aspirationally but not treated as part of “done.” Demoability should be a deliverable, not a QA surprise.

### Changes incorporated into Genesis (PR `improve/workflow-postmortem-h3m8` — #14)

- `/execute_plan` — Local Dev Verification gate
- `/pre_implementation_checklist` — Monorepo & local runtime section; plan ID must match capture
- `/workflow` — Flexible design/plan order; closure docs; common mistakes expanded
- `/qa_checklist` — Automated tests + manual checklist split
- `/postmortem` — Required closure artifact outputs
- `/capture_issue` — Optional `# Environment` field
- `/design_decisions` — Data provenance subsection
- `DEV_RUNBOOK_TEMPLATE` — Script integrity rule + terminology table
- Expression profiles — Happy-path handoff gates

---

## 2026-06-07 — AI Tastemakers (Daily Digest, EPH-20260606-DIG1)

**Source:** Greenfield instantiate → deploy (capture → explore → design → plan → execute → GitHub Actions + GitHub Pages).

### Friction observed

| Area | Issue |
|------|--------|
| External APIs | Deprecated Anthropic model ID in `.env.example` → 404 on all narrations |
| Git | Placeholder remote `YOU/repo`; push failed until `gh repo create` |
| GHA vs local git | Bot commit caused non-fast-forward push; needed `git pull --rebase` |
| GitHub Pages | Root-absolute `/assets/style.css` → unstyled site on project URL |
| MVP definition | Local CLI success treated as “done”; production URL/CSS not verified |
| Ranking UX | Bootstrap mode surfaced mega-repos; cold-start not documented upfront |

### Root cause (process)

**Production parity** missing from MVP definition. Scheduled/automated products need deployment verification (secrets, GHA dispatch, public artifact) — not just local run + unit tests.

### Changes incorporated into Genesis (PR `improve/tastemakers-postmortem-dig1`)

- `/execute_plan` — Deployment verification gate
- `/design_decisions` — External API identifiers; cold-start / bootstrap caveat
- `/postmortem` — List skipped workflow phases
- `/workflow` — Common mistakes (Pages paths, git remote, API IDs, GHA rebase, production parity)
- `DEV_RUNBOOK_TEMPLATE` — Scheduled job section; script integrity rule
- `docs/GITHUB_PAGES_CHECKLIST.md` — New template
- `README.md` — Post-instantiate git + GitHub block

---

## 2026-06-07 — AI Tastemakers (Copy + Brief Format, EPH-20260607-COPY)

**Source:** Follow-on feature; design_decisions before create_plan; local same-day digest used for verification.

### Friction observed

| Area | Issue |
|------|--------|
| Planning order | Checklist blocked on stale DIG1 plan; `/create_plan` run late |
| Verification | Same-day `npm run digest` reshuffled rankings (soft-dedup) |
| Data provenance | Enrich overwrote snapshot star counts in digest output |
| Deploy chain | GHA digest commit did not auto-trigger Pages deploy |
| Scope | “Copy only” expanded to two pipeline stability fixes |

### Root cause (process)

**Scheduled pipeline re-runs are not idempotent** for date-stamped output. Verification strategy for prompt/format changes was undocumented.

### Changes incorporated into Genesis (PR `improve/copy-postmortem-eph20260607`)

- `docs/WORKFLOW_COURSE.md` — follow-on case study + idempotency section
- `/workflow` — common mistakes 18–20; flexible design/plan order; closure doc in postmortem step
- `DEV_RUNBOOK_TEMPLATE` — same-day re-run + post-bot deploy rows
- `/execute_plan` — same-day pipeline warning; post-digest Pages verification

---

## 2026-07-02 — AI Tastemakers (Landing Layout v2, EPH-20260701-LAND)

**Source:** [ai-tastemakers](https://github.com/Leftyshields/ai-tastemakers) — full workflow through QA close; flag-gated static layout experiment.

### Friction observed

| Area | Issue |
|------|--------|
| Direction drift | Partial v2 implemented sidebar-heavy synthesis; revised capture required reflow-first refactor |
| Experiment JSON | Hypothesis/`change_summary` lagged capture until mid-implementation |
| Footer UX | Tailwind utilities in TS HTML strings did not guarantee spacing; adjacent links collided |
| QA gap | Automated tests green; layout/footer bug found only by browser check |
| Git | Local main behind GHA bot commits; rebase conflict on push |

### Root cause (process)

Static HTML generators treated Tailwind class strings like JSX utilities, but Tailwind v4 content scanning does not reliably emit rules from dynamic TS template literals.

### Changes incorporated into Genesis (PR `improve/tastemakers-postmortem-land` — #17)

- `/explore` — partial/WIP conflicts table in snapshot
- `/design_decisions` — static HTML generator styling section
- `/qa_checklist` — automated tests + browser gate for generated HTML
- `/execute_plan` — static HTML special check
- `/postmortem` — Path A (app repo) + Path B (Genesis) required outputs
- `/workflow` — common mistakes 21–24
- `docs/WORKFLOW_COURSE.md` — case study C (LAND)

### App-repo reference

- Closure: [CLOSURE_EPH-20260701-LAND.md](https://github.com/Leftyshields/ai-tastemakers/blob/main/docs/CLOSURE_EPH-20260701-LAND.md)
- Shipped: `d8c3492`, QA closed: `160da7c`

---

## 2026-07-06 — Project Genesis (Autonomous Loop Mode, EPH-20260702-AL01)

**Source:** Meta-workflow feature in Genesis upstream; full nine-step loop (capture → postmortem).

### Friction observed

| Area | Issue |
|------|--------|
| Step naming | Early drafts used "Reflection" as step 9; corrected to postmortem + optional `/reflection` |
| Hybrid orchestration | Interactive pauses skipped `step-complete` until QA batched steps 1–8 |
| Mode switch | `init --autonomous` rejected without deleting `run_config.json` |
| Dogfooding | Feature shipped in interactive mode; autonomous e2e in Cursor not validated |
| Meta-workflow rework | Build handoff moved to after QA; multiple command files updated |

### Root cause (process)

Defining the workflow while implementing it; hybrid state (JSON + LLM steps) made gate recording easy to defer.

### Changes incorporated into Genesis (this PR)

- `scripts/genesis-run.js` + tests — orchestrator for run state, gates, tests
- `.cursor/commands/genesis_run.md`, `reflection.md` — master entry + optional doc handoff
- Nine command files — mode-awareness and step chain
- `README.md` — workflow modes, orchestrator CLI, mode-reset note
- `/workflow` — common mistakes 25–26 (`step-complete`, mode reset)
- `docs/CLOSURE_EPH-20260702-AL01.md`, `postmortem_EPH-20260702-AL01.md`

### Reference

- Closure: [docs/CLOSURE_EPH-20260702-AL01.md](CLOSURE_EPH-20260702-AL01.md)

---

## How to add entries (after `/postmortem`)

1. **App repo (Path A):** Append a dated section above; update `docs/CLOSURE_<ISSUE_ID>.md` and workflow commands as needed; open PR or push.
2. **Genesis (Path B):** When templates should change, open a PR here updating `.cursor/commands/` and `docs/`; link the app-repo feedback entry and add a **Changes incorporated into Genesis** line with the PR branch name.
