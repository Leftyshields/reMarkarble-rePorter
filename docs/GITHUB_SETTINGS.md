# GitHub repository settings

Recommended settings for [Leftyshields/project-genesis](https://github.com/Leftyshields/project-genesis).

---

## Branch protection for `main` (configured 2026-06-07)

**Goal:** Block accidental force-push/delete on `main`; require PR review + CI for merges, with **Leftyshields** bypass so you can still push directly.

### Active rules

**Classic branch protection** on `main`:

| Setting | Value |
|--------|--------|
| Allow force pushes | **No** |
| Allow deletions | **No** |

**Repository ruleset:** [Main: require PR + CI (owner bypass)](https://github.com/Leftyshields/project-genesis/rules/17372340)

| Setting | Value |
|--------|--------|
| Require pull request | Yes (1 approval; author does not count) |
| Required status check | `test` (from `.github/workflows/ci.yml`) |
| Bypass | **Leftyshields** — always |

### CI

Workflow: `.github/workflows/ci.yml` — runs `npm test` on push/PR to `main`.

Optional local e2e: `npm run test:instantiate` (copy + run-path smoke test).

### Result

- **You (Leftyshields):** Can push directly to `main` (bypass).
- **PR merges:** Need 1 non-author approval + green `test` check.
- **Everyone:** Cannot force-push or delete `main`.

---

## Backlog ↔ GitHub Issues mapping

When a story ships, close the matching GitHub issue and link closure docs in the app repo.
