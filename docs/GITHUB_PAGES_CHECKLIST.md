# GitHub Pages checklist (template)

Use when shipping a static site from an instantiated app (e.g. daily digest, docs site, landing page).

Copy relevant rows into `docs/DEV_RUNBOOK.md` when you deploy.

---

## URL shape

| Hosting | Example URL | Asset path rule |
|---------|-------------|-----------------|
| **Project site** | `https://USER.github.io/REPO/` | **Relative** paths only |
| User/org site | `https://USER.github.io/` | Root-absolute `/assets/…` OK |

Most instantiated apps use **project sites**. Root-absolute `/assets/style.css` resolves to `USER.github.io/assets/…` → **404** → unstyled HTML.

---

## Build checklist

- [ ] CSS/JS built in CI (`npm run build:pages` or equivalent) — do not rely on committed generated CSS unless intentional
- [ ] HTML uses relative paths:
  - From site root: `assets/style.css`, `briefings/2026-06-06.html`
  - From subfolder: `../assets/style.css`, `../index.html`
- [ ] Optional: `<base href="/REPO/">` only if **all** links are relative (no leading `/`)
- [ ] `site/.nojekyll` present if using folders starting with `_` or dotfiles
- [ ] Pages workflow verifies artifact exists (e.g. `test -s site/assets/style.css`)

---

## Deploy checklist

- [ ] Repo **Settings → Pages → Source**: GitHub Actions (or `/docs` on `main`)
- [ ] Workflow has `permissions: pages: write` and `id-token: write` for Actions deploy
- [ ] Push to `main` triggers deploy (or manual `workflow_dispatch`)
- [ ] Hard-refresh production URL — confirm styled layout
- [ ] Brief/deep links work from homepage (not 404)

---

## Common failures

| Symptom | Cause | Fix |
|---------|-------|-----|
| Unstyled HTML, default browser fonts | CSS 404 at domain root | Relative asset paths |
| CSS works locally, broken on GitHub | `npx serve site` uses `/` root; GitHub uses `/REPO/` | Same relative-path fix |
| Deploy succeeds, old content | CDN cache | Hard refresh; wait ~1 min |
| Pages 404 | Wrong branch/folder in Settings | Align with workflow artifact path |

---

## Tailwind / build-time CSS

GitHub Pages serves static files only. Compile Tailwind (or PostCSS) **in CI**:

```json
"build:pages": "tsx scripts/build-pages.ts && tailwindcss -i site/assets/input.css -o site/assets/style.css --minify"
```

Track `input.css` in git; gitignore generated `style.css` if CI always rebuilds.

---

## Related

- [GITHUB_SETTINGS.md](GITHUB_SETTINGS.md) — branch protection, issues
- [DEV_RUNBOOK_TEMPLATE.md](DEV_RUNBOOK_TEMPLATE.md) — scheduled jobs section
