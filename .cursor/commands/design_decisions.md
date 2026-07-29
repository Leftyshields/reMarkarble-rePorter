We are defining version 1 design decisions.

Do NOT write code yet.

**This document should be created BEFORE implementation begins** (`/execute_plan`).

Based on our discussion so far:

Produce:
- Proposed user flow (step-by-step)
- Resource/data implications (if any)
- External integrations or dependencies (if any)
- Explicit non-goals for v1
- Edge cases worth considering

## Required Sections

### 1. User Flow
Detailed step-by-step user journey through the feature.

### 2. Field Mapping & Update Strategy
If this feature involves data generation or transformation, specify:
```
Generated Item → Form Field → Update Strategy (replace/merge/append)
title → idea → replace
tags → tags → merge with existing
```

### 3. Data Format Conversions
If formats differ between systems, document:
- Source format (e.g., API response)
- Target format (e.g., form data)
- Conversion required (e.g., {task} → {text, link})

### 4. Content Rendering Strategy
If adding formatted content (markdown, HTML, rich text), specify:
- Where does it render? (view mode, edit mode, both)
- What library/component handles rendering?
- How does editing work? (WYSIWYG vs raw text/textarea)
- What dependencies are needed?

### 5. Integration Points
- Which existing components are affected?
- How does this integrate with existing features?
- What state management is involved?

### 6. State Management Patterns
If using React:
- Identify state updates that depend on props or other state
- Specify use of functional updates: `setState(prev => ...)` where needed
- Reference `docs/REACT_PATTERNS.md` for patterns

### 7. Backend entry points & parity

If adding API endpoints:

- Create/update **`docs/ARCHITECTURE.md`** (from [ARCHITECTURE_TEMPLATE.md](docs/ARCHITECTURE_TEMPLATE.md))
- List every HTTP entry point (local, production, preview)
- Prefer one shared handler module imported by all entry points — avoid duplicating route tables
- Document web client → API base URL for local and production builds

### 8. Integrations & dev environment

For auth, payments, email, or third-party APIs, document:

- **Sandbox vs production** credentials and env vars
- **Auth UX by environment** (e.g. OAuth popup on localhost vs redirect on hosted domain)
- **Required one-time deploys** (e.g. hosting for auth helper, webhooks)
- **Emulator / seed commands** and ports
- **SSH or remote dev** constraints (authorized domains, port forwarding)

Copy [DEV_RUNBOOK_TEMPLATE.md](docs/DEV_RUNBOOK_TEMPLATE.md) → `docs/DEV_RUNBOOK.md` and add rows as you learn.

### 9. Data provenance (when multiple sources)

If data comes from external APIs **and** local seed/fixtures:

- List sources (e.g. vendor API, seed script, manual entry)
- UI/API field for source or inference rule
- Cleanup behavior on reconnect/relink/re-auth

### 10. External API identifiers (verify at implement time)

For LLM, payment, or vendor APIs, document:

| Integration | Env var | Identifier (model, API version, etc.) | Verify at ship |
|-------------|---------|----------------------------------------|----------------|
| _e.g. Anthropic_ | `ANTHROPIC_API_KEY` | _e.g. `claude-sonnet-4-6`_ | _Provider docs — IDs retire_ |

Rules:
- **Do not treat design-doc model names as stable forever.** Check provider docs when implementing and in `.env.example`.
- Note rate limits and which token works in CI (e.g. `GITHUB_TOKEN` vs PAT for Search API).

### 11. Static HTML generators (Tailwind, build-time templates)

If UI is generated as HTML strings (e.g. `scripts/*-pages.ts`, email templates, static site builders):

- **Layout-critical spacing** (nav rows, footers, inline link groups): use **component classes** in a scanned CSS entry file (e.g. `site/assets/input.css`), not Tailwind utility strings alone inside TS template literals
- **Inline link rows:** add explicit HTML separators (`&middot;`, `<span aria-hidden>`) or flex `gap` via component CSS — adjacent `<a>` tags collapse without them
- **Tailwind v4 content scanning:** utilities in dynamic TS strings may not emit CSS; verify after `npm run build:pages` (or your compile step) + browser refresh
- Document which generator functions own which components

### 12. Cold-start / bootstrap behavior (ranking, ML, analytics)

If v1 quality depends on accumulated history (snapshots, training data, A/B baseline):

- Document bootstrap fallback behavior and when “real” mode activates
- Set user expectations in explore/capture: _“Rankings improve after ~N days of daily runs”_
- Avoid promising full product quality on day one unless technically accurate

Rules:
- Favor reversible decisions
- Avoid overengineering
- Call out any decision that would be hard to undo later
- Be explicit about what "generates" vs "enhances" vs "transforms"

End by asking:
"Are these the correct design boundaries for v1?"

---

## Run mode

If `run_config.json` has `mode: "autonomous"`:
- Include `Rationale:` for each major decision.
- Skip the confirmation question.
- Run `npm run genesis:run -- step-complete design_decisions --artifacts .ai/context/design_decisions.md`.
- **Immediately** continue with `/create_plan` logic in the same session.

If interactive: ask "Are these the correct design boundaries for v1?" and wait for confirmation.

**Mid-run `--autonomous`:** If the user message includes `--autonomous`, run `npm run genesis:run -- init --autonomous`, then continue remaining steps per [genesis_run.md](genesis_run.md) Agent behavior §1.

---

**Next:** Run `/create_plan` to create the execution plan, then `/pre_implementation_checklist` before `/execute_plan`. See `.cursor/commands/workflow.md` for the complete development workflow.
