---
name: Project Builder
description: Automatically analyze project plans and generate comprehensive task breakdowns persisted to the local .claude/ directory. Use when user describes a project, feature set, or asks to build/implement something complex requiring multiple tasks.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, TodoWrite
---

# Project Builder Skill

## Purpose
Transform high-level project plans into actionable, well-organized task breakdowns. Persist the breakdown as durable, git-trackable documentation under `.claude/plans/` and `.claude/tasks/` so it survives across sessions and stays alongside the code.

## Storage Model

All output is written to the **local `.claude/` directory** of the current repo (no external task system). The layout mirrors conventions already used elsewhere in the system:

| Path | Purpose | Format |
|------|---------|--------|
| `.claude/plans/{slug}.md` | Human-readable project plan: epic, phases, full task list | Markdown |
| `.claude/tasks/{slug}/{N}.json` | One file per task — granular, machine-readable | JSON |
| `.claude/tasks/{slug}/index.json` | Task ordering, dependencies, status roll-up | JSON |

**Slug rule:** kebab-case derived from the project title (e.g. "Auth Refresh Tokens" → `auth-refresh-tokens`). If a slug collides, append `-2`, `-3`, etc.

If `.claude/plans/` or `.claude/tasks/` does not exist, create it with `mkdir -p` before writing.

## Auto-Activation Triggers
Activates when the user:
- Describes a multi-step project or feature set
- Says "build a [complex feature]" / "implement [system]" / "create a project plan"
- Mentions work that clearly needs multiple components or phases

## Workflow

### Phase 1: Plan Analysis
Extract from the user's description:
- Core objectives and deliverables
- Technical requirements (API, database, frontend, auth, infra, etc.)
- Complexity (Low / Medium / High)
- Natural project phases

### Phase 2: Area Selection
Pick the work areas the project actually needs — do not pad:
- **backend** — API, server, database work
- **frontend** — UI, components, UX
- **security** — Authentication, authorization, encryption
- **testing** — Unit, integration, E2E
- **data** — Schema, migrations, pipelines
- **infrastructure** — Docker, deployment, CI/CD
- **performance** — Optimization, caching, scaling
- **mobile** — Native apps, responsive design
- **ai_ml** — Machine learning, AI integration
- **devops** — Monitoring, logging, automation
- **project_management** — Coordination tasks for high-complexity efforts

### Phase 3: Task Generation
For each task, capture:
- **title** — clear, actionable
- **description** — context + acceptance criteria
- **priority** — Critical / High / Medium / Low
- **size** — XS / S / M / L / XL
- **phase** — phase number (1, 2, 3, ...)
- **area** — one of the areas above
- **estimated_hours** — numeric
- **risk** — low / medium / high
- **dependencies** — array of task IDs this blocks on
- **acceptance_criteria** — bullet list of measurable outcomes

**Context integration:**
- Read `.claude/memory/active/quick-reference.md` and `procedural-memory.md` if present — reuse proven patterns
- Read root `CLAUDE.md` for project-specific guard rails
- Grep existing code for utilities/patterns the new tasks should reuse rather than reinvent

### Phase 4: Compliance Review
Before writing files, verify:
- Every task has a title, description, priority, size, phase, and acceptance criteria
- Workload is balanced across phases (no single phase carries all Critical tasks)
- Dependencies form a DAG (no cycles) and reference real task IDs
- Security tasks exist for any feature touching auth, secrets, or PII
- Test tasks exist for every implementation task

### Phase 5: File Generation

**Step 1 — derive the slug** from the project title and confirm `.claude/plans/{slug}.md` does not already exist (suffix `-2` etc. if it does).

**Step 2 — ensure directories exist:**
```bash
mkdir -p .claude/plans .claude/tasks/{slug}
```

**Step 3 — write the plan markdown** to `.claude/plans/{slug}.md` using the template below.

**Step 4 — write per-task JSON** to `.claude/tasks/{slug}/{N}.json` (one file per task, N = 1, 2, 3, ...).

**Step 5 — write the index** to `.claude/tasks/{slug}/index.json` summarizing IDs, statuses, and the dependency graph.

**Step 6 — call TodoWrite** with the Phase-1 critical tasks so the current session can start working immediately.

### Phase 6: Project Summary
Print a short summary back to the user:
- Slug + paths to the plan and tasks dir
- Task counts by priority and phase
- Critical path (longest dependency chain)
- The first few suggested tasks to start on

## Plan Markdown Template

Write this to `.claude/plans/{slug}.md`:

```markdown
---
name: {Project Title}
slug: {slug}
created: {YYYY-MM-DD}
complexity: {Low|Medium|High}
estimated_duration_days: {N}
total_tasks: {N}
areas: [backend, frontend, ...]
status: planned
---

# {Project Title}

## Context
{1–2 sentences on what is being built and why. Include the user's original ask.}

## Analysis
- **Complexity:** {Low|Medium|High}
- **Areas involved:** {comma-separated list}
- **Estimated duration:** {N} days
- **Critical path:** {phase → phase → phase summary}

## Existing code to reuse
- `{path/to/file.ts:LINE}` — {function name} — {why it matters}
- ...

## Phases

### Phase 1 — {Phase Name}
| ID | Task | Area | Priority | Size | Depends on |
|----|------|------|----------|------|------------|
| 1  | {title} | backend | Critical | M | — |
| 2  | {title} | testing | High | S | 1 |

### Phase 2 — {Phase Name}
...

## Tasks
Per-task detail lives in `.claude/tasks/{slug}/{N}.json`. Index: `.claude/tasks/{slug}/index.json`.

## Verification
- [ ] All tasks in `.claude/tasks/{slug}/` reference back to this plan
- [ ] Phase 1 critical tasks are in the active TodoWrite list
- [ ] Acceptance criteria are testable
```

## Task JSON Schema

Each `.claude/tasks/{slug}/{N}.json` file:

```json
{
  "id": "1",
  "slug": "{slug}",
  "title": "{Brief title}",
  "description": "{Detailed context and acceptance criteria}",
  "activeForm": "{Gerund form for status display, e.g. 'Adding refresh-token endpoint'}",
  "priority": "Critical|High|Medium|Low",
  "size": "XS|S|M|L|XL",
  "phase": 1,
  "area": "backend",
  "estimated_hours": 4,
  "risk": "low|medium|high",
  "dependencies": [],
  "acceptance_criteria": [
    "Criterion 1",
    "Criterion 2"
  ],
  "status": "pending|in_progress|completed",
  "blocks": [],
  "blockedBy": []
}
```

The `id`, `subject`/`title`, `activeForm`, `status`, `blocks`, `blockedBy` fields match the existing `~/.claude/tasks/` JSON convention so other tooling can consume them.

## Index JSON Schema

`.claude/tasks/{slug}/index.json`:

```json
{
  "slug": "{slug}",
  "plan": ".claude/plans/{slug}.md",
  "created": "{YYYY-MM-DD}",
  "tasks": [
    { "id": "1", "title": "...", "phase": 1, "priority": "Critical", "status": "pending" }
  ],
  "phases": {
    "1": { "name": "Foundation", "task_ids": ["1", "2"] },
    "2": { "name": "Polish", "task_ids": ["3", "4"] }
  }
}
```

## Best Practices

### Memory-driven planning
Always read `.claude/memory/active/quick-reference.md` and `procedural-memory.md` first if they exist. Reference matching patterns in the plan's "Existing code to reuse" section so future-you doesn't reinvent.

### Realistic estimation
- Use historical velocity from similar tasks (check older `.claude/plans/`)
- Add 15–20% buffer for unknowns
- Mark `risk: high` on anything new to the codebase

### Progressive elaboration
- Phase 1: Core functionality
- Phase 2: Enhancement and polish
- Phase 3: Optimization and scaling
- Phase 4: Documentation and deployment

### Idempotency
If `.claude/plans/{slug}.md` already exists, do **not** silently overwrite. Either suffix the slug or ask the user whether to update in place.

## Integration with Other Workflows

**After project building:**
- `/orchestrate-tasks` can pick up `.claude/tasks/{slug}/` for parallel execution
- `/sprint-plan` can pull tasks from any active `.claude/tasks/*/index.json`
- `/focus` can load a single task by `{slug}/{N}` for deep work

**Updating tasks during execution:**
- Edit the per-task JSON to flip `status` from `pending` → `in_progress` → `completed`
- Update `index.json` task entries to match
- The plan markdown is the source of intent and rarely needs edits after generation

## Error Handling

### Plan unclear
Ask one targeted clarifying question about scope, then proceed with explicit assumptions noted in the plan's Context section.

### Complexity hard to estimate
Default to Medium, mark uncertain tasks `risk: high`, and call out the assumption in the plan.

### Slug collision
Suffix `-2`, `-3`, ... and tell the user which slug was used.

### Cannot create directories
Surface the error to the user (likely a permissions or git-init issue) — do not fall back to inline-only output.

## Skill Metadata

**Version:** 2.0.0
**Category:** Project Management & Planning
**Storage:** Local `.claude/` directory (no external task system)
