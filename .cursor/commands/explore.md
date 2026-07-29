We are now in exploration mode.

Do NOT write code.
Do NOT propose implementation yet.

Your job is to deeply understand the problem and capture an exploration snapshot that can feed planning and execution.

Steps (in THIS response):
1. Restate the problem in your own words
2. Identify the user and their job-to-be-done
3. Describe current behavior and desired behavior
4. Identify what success looks like
5. List constraints and risks
6. **Partial implementation / WIP check** (if flag-gated code, open PRs, or experiment branches already exist):
   - Compare capture **desired behavior** to what is already implemented
   - Document a **Conflicts with existing code** table: file/area | current behavior | capture says | action (keep / refactor / supersede)
   - Note stale experiment JSON, design docs, or plans that describe the old direction
7. **Architecture Check** (if backend/API changes):
   - Identify ALL backend entry points (document in `docs/ARCHITECTURE.md` — do not assume fixed filenames)
   - Document which environments each serves (local dev vs production)
   - Note whether a shared handler module should be updated once vs many entry points
8. Ask clarifying questions that materially affect planning or execution

Rules:
- Challenge unclear assumptions
- Push back if the problem is poorly defined
- Prefer questions over answers, but still produce a complete snapshot
- Think like a strong project manager or strategic planner
- Always produce a complete exploration snapshot in this response, even while asking questions
- You MUST persist a snapshot at the end of THIS response, even if questions remain unanswered

**Output Persistence (MANDATORY):**
After completing the exploration snapshot (including open questions), you MUST persist the findings to `.ai/context/last_explore.md` using this exact structure:

```markdown
# Restated Problem
[restated problem in your own words]

# User + JTBD
[user description and job-to-be-done]

# Current Behavior
[current state description]

# Desired Behavior
[desired state description]

# Success Criteria
[what success looks like, bullet list]

# Constraints
[list of constraints, bullet list]

# Risks / Unknowns
[risks and unknowns, bullet list]

# Conflicts with Existing Code (if partial/WIP exists)
| Area | Current | Capture desired | Action |
|------|---------|-----------------|--------|
| _e.g. layout v2 flag_ | _sidebar-heavy_ | _main-column reflow_ | _refactor in place_ |

# Architecture Impact (if backend changes)
[List all files that need changes and their environments]
- Local Dev: [files]
- Production: [files]
- Note any parity requirements

# Open Questions
[clarifying questions that materially affect design or architecture, bullet list]

# Acceptance Criteria (Draft)
[preliminary acceptance criteria if applicable, bullet list]

# Timestamp
[ISO 8601 timestamp]

After writing the file, confirm in chat exactly:
WROTE .ai/context/last_explore.md

Then end with:
Once these questions are answered, we can create a plan.

---

## Run mode

Read `.ai/context/run_config.json` before the closing message.

If `mode` is `autonomous`:
- Persist the snapshot; run `npm run genesis:run -- step-complete explore --artifacts .ai/context/last_explore.md`.
- **Immediately** continue with `/design_decisions` logic in the same session.
- Do **not** end with "Once these questions are answered, we can create a plan."

If interactive or no run config: end with "Once these questions are answered, we can create a plan."

**Mid-run `--autonomous`:** If the user message includes `--autonomous`, run `npm run genesis:run -- init --autonomous`, then continue remaining steps per [genesis_run.md](genesis_run.md) Agent behavior §1.

---

**Workflow Position:** This command follows `/capture_issue` and precedes `/design_decisions`.

**Next:** Run `/design_decisions` to document design choices before creating the plan. See `.cursor/commands/workflow.md` for the complete development workflow.

