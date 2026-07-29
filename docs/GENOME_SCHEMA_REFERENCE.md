# Genesis Genome Schema Reference (v1)

Use this as context when working with the Genesis repo genome format. Schema only — not implementation.

## Format

- No JSON Schema, TypeScript types, protobuf, or YAML.
- Genome = a directory (default: `.genome/`) of markdown files.
- Roles are `## {RoleId}` sections with bullet fields.
- v1 has no machine schema enforcement (planned for v2 per docs/BLUEPRINT.md).
- Only optional policy files are parsed into structured values at load time.

---

## Genome directory layout

```
.genome/
├── mission.md                  # Objectives, Success Criteria, Out of Scope
├── constraints.md              # Global laws (prose)
├── decomposition_rules.md      # Hierarchy rules + Example chain
├── role_library/
│   ├── organs.md
│   ├── tissues.md
│   ├── cells.md                # cell role specs
│   └── molecules.md
├── contracts/
│   └── handoffs.md             # inter-layer contracts
├── repair_policy.md            # OPTIONAL: max_retries, delay_ms
├── guardrails.md               # OPTIONAL: allowed_path_prefix
└── expression_profiles/        # OPTIONAL: derived views, not source schema
```

---

## Cell spec fields (current)

A cell is a role entry in `.genome/role_library/cells.md`. There is no type named `CellSpec`.

Each cell role has six fields:

| Field | Type | Description |
|-------|------|-------------|
| id | string | Role identifier; matches the `##` heading |
| purpose | prose | What the cell does |
| inputs | prose | Expected inputs (e.g. handoff from tissue) |
| outputs | prose | Expected outputs (e.g. molecule result to tissue) |
| composition | prose + role ids | Which molecules this cell may invoke |
| health | prose | Health criteria for the cell |

Example (canonical genome):

```markdown
## Worker

- **id:** Worker
- **purpose:** Run molecules to fulfill the tissue's function; single role-bearing unit.
- **inputs:** Handoff from tissue (e.g. path, task).
- **outputs:** Molecule result (e.g. file contents) to tissue.
- **composition:** Invokes molecules (e.g. read_file).
- **health:** Per-molecule success/failure; cell healthy when required molecules succeed within policy.
```

### Related role shapes

- **Organ** and **tissue** roles use the same six fields in `role_library/organs.md` and `role_library/tissues.md`.
- **Molecule** roles add: preconditions, postconditions, permissions.

### Cell expression profile (derived, not a separate file format)

When a cell instance is resolved (e.g. `cell:Worker`), it also sees:

- mission slice — from `.genome/mission.md` (full mission in v1 single-chain genomes)
- role library entries — own cell entry + allowed molecule entries from composition
- contracts — handoffs in `.genome/contracts/` involving this cell
- health / adaptation boundaries — from the cell's health field

### Aspirational fields (design doc only, NOT in live .genome/)

Per docs/BLUEPRINT.md §8, future cell types may also have: triggers, allowed actions, dependencies, adaptation boundaries, communication surface, molecules. These are not in the current cell role file.

---

## Dependencies

There is NO dedicated `dependencies` field or dependency DAG in v1. Relationships are expressed three ways:

### 1. Composition (parent → child containment)

Each layer's composition field names child role ids:

```
Build (organ) --composition--> Implementation (tissue) --composition--> Worker (cell) --composition--> read_file (molecule)
```

| Layer | File | Composition meaning |
|-------|------|---------------------|
| Organ | role_library/organs.md | Contains tissues |
| Tissue | role_library/tissues.md | Contains cells |
| Cell | role_library/cells.md | Invokes molecules |

### 2. Handoff contracts (layer-to-layer obligations)

File: `.genome/contracts/handoffs.md`

| Field | Description |
|-------|-------------|
| From | Source role with layer, e.g. `Build (organ)` |
| To | Target role, e.g. `Implementation (tissue)` |
| Format | Payload shape |
| Obligation | Sender/receiver responsibilities |
| SLA | Service-level expectations (placeholder in v1) |

Example:

```markdown
## Build → Implementation (organ → tissue)

- **From:** Build (organ)
- **To:** Implementation (tissue)
- **Format:** Work package: at least a task identifier and optional payload (e.g. path, options).
- **Obligation:** Build assigns work to Implementation; Implementation acknowledges and returns completion or failure.
- **SLA:** (Placeholder for v1: no formal SLA; handoff is best-effort.)
```

### 3. Example chain (instantiation wiring)

File: `.genome/decomposition_rules.md`, section "Example chain"

| Token | Purpose |
|-------|---------|
| Organ: | Which organ role to instantiate |
| Tissue: | Which tissue under that organ |
| Cell: | Which cell under that tissue |
| Molecule: | Which molecule the cell invokes |

Current canonical chain:

```
Organ:    Build
Tissue:   Implementation (under Build)
Cell:     Worker (under Implementation)
Molecule: read_file (invocable by Worker)
```

Validation rule: every role id referenced in decomposition_rules or contracts must exist as a `## {id}` section in the matching role_library/*.md file.

NOT represented in genome files: explicit cross-organ dependency graphs, async/blocking dependency edges, or runtime dependency signaling.

---

## Multi-cell organism structure

### Structural model

Five-layer tree:

```
organism (roleId: null)
└── organ:{RoleId}
    └── tissue:{RoleId}
        └── cell:{RoleId}
            └── molecule:{RoleId}   # leaf, children: []
```

Each node has: id, layer (organism | organ | tissue | cell | molecule), roleId, children[].

### Canonical v1 instance (single linear chain)

```
organism
└── organ:Build
    └── tissue:Implementation
        └── cell:Worker
            └── molecule:read_file
```

### Multi-cell / multi-organ (design only, not implemented in v1)

| Aspect | v1 (live) | Future (documented) |
|--------|-----------|---------------------|
| Multiple cells per tissue | composition can name cells in prose; runtime parses one chain | multiple cells via composition + structured decomposition table |
| Multiple organs | documented in EXPRESSION_DERIVATION.md | mission slices per organ |
| Multiple paths per run | one path per runPath() invocation | scheduling layer |

---

## Other genome artifacts

### mission.md

Sections: Objectives, Success Criteria, Out of Scope (markdown headings).

### constraints.md

Global laws as prose.

### decomposition_rules.md

Prose rules for organism → organs → tissues → cells → molecules, plus Example chain.

### Optional policies

| File | Fields |
|------|--------|
| repair_policy.md | max_retries (number), delay_ms (number) |
| guardrails.md | allowed_path_prefix (comma-separated paths) |

---

## Loaded genome object shape (conceptual)

All core fields are raw markdown strings; only optional files are parsed:

```
{
  mission: string,
  constraints: string,
  decomposition_rules: string,
  role_library: {
    organs: string,
    tissues: string,
    cells: string,
    molecules: string,
  },
  contracts: {
    handoffs: string,
  },
  repair_policy?: { maxRetries: number, delayMs: number },
  guardrails?: { allowedPathPrefix: string[] },
}
```

---

## Key source files

| What | Path |
|------|------|
| Canonical example genome | `.genome/` |
| Cell role specs | `.genome/role_library/cells.md` |
| Decomposition / Example chain | `.genome/decomposition_rules.md` |
| Handoff contracts | `.genome/contracts/handoffs.md` |
| Expression derivation rules | `.genome/EXPRESSION_DERIVATION.md` |
| Aspirational / future schema | `docs/BLUEPRINT.md` (§8, §13) |

---

## Quick reference

- Cell spec fields: id, purpose, inputs, outputs, composition, health
- Dependencies: implicit via composition, handoff contracts (From/To/Format/Obligation/SLA), and Example chain — no dependency array
- Organism structure: five-layer tree (organism → organ → tissue → cell → molecule); v1 materializes one linear chain only
