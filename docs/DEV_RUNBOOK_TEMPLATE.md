# Dev Runbook (template)

Copy to **`docs/DEV_RUNBOOK.md`** in your instantiated project. Fill in stack-specific commands and symptom/fix rows as you debug.

> **Script integrity rule:** Do not document an `npm run …` command until it exists in root `package.json`. If deferred, mark as `(planned)` — not as a hard requirement.

## Terminology (customize for your stack)

| Term | Example meaning |
|------|-----------------|
| **Local dev** | localhost frontend + API + emulators |
| **Vendor sandbox** | Third-party test API (not production) |
| **Seed / fixture data** | Scripts that populate local DB for demos |
| **Scheduled job** | Cron, GitHub Actions, or worker that runs unattended |
| **Staging** | Hosted pre-production environment (if you have one) |

## Start commands

| Service | Command | URL / port |
|---------|---------|------------|
| Backend | _e.g. `npm run dev:api`_ | _e.g. `http://localhost:3001/api`_ |
| Frontend | _e.g. `npm run dev:web`_ | _e.g. `http://localhost:5173`_ |
| Database / emulators | _e.g. `npm run dev:emulators`_ | _ports_ |
| Scheduled / CLI job | _e.g. `npm run digest`_ | _writes to `briefings/`_ |

## Hard requirements

| Rule | Why |
|------|-----|
| _e.g. Use localhost, not LAN IP for OAuth_ | _Firebase authorized domains_ |
| _e.g. Run seed script after emulator start_ | _Empty catalog_ |
| _e.g. Root `.env` loaded by API_ | _Missing credentials_ |
| Never commit `.env` | Secrets |

## Scheduled job / GitHub Actions (if applicable)

| Step | Command / location |
|------|-------------------|
| Workflow file | _e.g. `.github/workflows/digest.yml`_ |
| Required secrets | _e.g. `ANTHROPIC_API_KEY`_ |
| Manual test | _e.g. `gh workflow run "Daily Digest"`_ |
| Expected artifact | _e.g. commit to `briefings/`, Pages deploy_ |
| Public URL | _e.g. `https://USER.github.io/REPO/`_ |

**Deployment verification (MVP):**

1. Set secrets on GitHub repo
2. Run workflow manually once
3. Confirm artifact on `main`
4. Load public URL; verify CSS/UI (not unstyled HTML)
5. After bot commits artifacts: verify deploy workflow ran (or dispatch manually)
6. See [GITHUB_PAGES_CHECKLIST.md](GITHUB_PAGES_CHECKLIST.md) for static sites

**Same-day re-run warning (dated output folders):**

Re-running a scheduled job when `briefings/YYYY-MM-DD/` (or equivalent) already exists can change rankings (soft-dedup) or metrics (live API refresh). For prompt/format-only changes, prefer unit tests + GHA dispatch over local same-day re-run. See [WORKFLOW_COURSE.md](WORKFLOW_COURSE.md).

## Symptom → fix

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| _API empty response / crash_ | Unhandled error in handler | Global error handler; check API logs |
| _Auth redirect 401_ | Cross-origin auth on localhost | Popup in dev or auth proxy; see Firebase redirect best practices |
| _404 on API in production_ | Path prefix / hosting rewrite mismatch | Document in `docs/ARCHITECTURE.md`; align router mount with hosting |
| _GitHub Pages unstyled_ | Root-absolute `/assets/…` on project site | Use relative paths; see GITHUB_PAGES_CHECKLIST |
| _API 404 model not found_ | Deprecated provider model ID | Verify current ID in provider docs; update `.env` |
| _git push rejected (non-fast-forward)_ | GHA bot pushed commits | `git pull --rebase origin main` then push |
| _Same-day job reshuffled output_ | Soft-dedup penalized today's existing folder | Exclude current date from dedup or use GHA as source of truth |
| _Output metrics ≠ snapshot_ | Later stage re-fetched live API values | Document provenance; preserve snapshot fields on merge |
| _Public site stale after bot commit_ | Deploy workflow did not run | `gh workflow run` deploy workflow; hard-refresh URL |

Add a row here whenever debugging takes more than 30 minutes.

## QA gate

Before the next feature: run `/qa_checklist` → `/code_review` → `/postmortem`.
