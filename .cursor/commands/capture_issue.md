**MODE LOCK — INTAKE + LOG ONLY**

You are in **INTAKE + LOG ONLY** mode.

Your job is to capture an issue and log it. Nothing else.

---

## HARD CONSTRAINTS

You MUST NOT:

* Modify any project code or configuration files
* Create or update application code
* Explore the codebase in any way
  (no searching files, no reading source, no browsing directories)
* Create a plan
* Propose implementation steps

You MAY:

* Write **exactly one file**:
  `.ai/context/last_capture.md`
* Create the directory `.ai/context/` **only if it does not exist**

**HARD GUARDRAIL**

The ONLY file you are allowed to change is:

* `.ai/context/last_capture.md`

If any other file would be changed, **STOP** and instead output the markdown in chat only.

---

## ISSUE ID

* Generate a new **Issue ID** for this capture
* Format: `EPH-YYYYMMDD-XXXX`
  (date + short random or pseudo-random suffix)
* Generate the Issue ID **once**
* If an Issue ID already exists in `last_capture.md`, reuse it, do NOT regenerate

This Issue ID will be used to join all downstream workflows.

---

## INTERACTION RULES

* Ask **only the minimum number of clarifying questions** required to create a clean issue
* Do NOT ask questions unless something critical is missing
* If the user asks to implement or plan, respond **exactly**:

```
Captured. Next run /explore or /create_plan.
```

---

## OUTPUT REQUIREMENTS

Produce a concise issue containing:

* Title
* TLDR (1–2 sentences)
* Current Behavior
* Desired Behavior
* Notes
* Priority (low / medium / high)
* Open Questions

---

## FILE FORMAT

Write the issue to `.ai/context/last_capture.md` using **exactly** this structure:

```markdown
# Issue ID
[generated issue id]

# Title
[title here]

# TLDR
[1–2 sentences]

# Current Behavior
[description]

# Desired Behavior
[description]

# Notes
[notes here]

# Priority
[low / medium / high]

# Environment
[optional: local-dev | staging | production | vendor-sandbox]

# Open Questions
[questions here]

# Timestamp
[ISO 8601 timestamp]
```

---

## CONFIRMATION

After writing the file, respond in chat **exactly**:

```
WROTE .ai/context/last_capture.md
```

### Interactive (default)

Then ask:

```
Is this ready to log, or do you want to tweak anything?
```

Do **not** run `/explore` until the user confirms.

### Autonomous (`run_config.json` → `mode: "autonomous"`)

- **Skip** the "ready to log?" question entirely.
- Run:
  ```bash
  npm run genesis:run -- step-complete capture --artifacts .ai/context/last_capture.md
  ```
- **Immediately** continue with step 2 (`/explore` logic) in the **same session** — do not wait for user input.

---

**Workflow Position:** This is the first step in the feature development workflow.

**Next:** Run `/explore` to analyze requirements and constraints. Cursor will guide you through the rest (design_decisions → create_plan → pre_implementation_checklist → execute_plan → code_review → qa_checklist → postmortem). See `.cursor/commands/workflow.md` for the full workflow.

---

This version is strict, deterministic, cheap to execute, and safe for Cursor and remote SSH environments.

---

## Run mode

Read `.ai/context/run_config.json` before choosing confirmation behavior.

If `mode` is `autonomous`:
- You are inside `/genesis_run --autonomous` — write capture as step 1.
- Follow **Autonomous** confirmation above (no pause; `step-complete`; continue to explore).
- Intake-only code restrictions still apply for this step (no codebase exploration during capture).

If `run_config.json` is missing, this command runs **standalone interactive** intake only.

**Mid-run `--autonomous`:** If the user message includes `--autonomous`, run `npm run genesis:run -- init --autonomous`, then continue remaining steps per [genesis_run.md](genesis_run.md) Agent behavior §1.
