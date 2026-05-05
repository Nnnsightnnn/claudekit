---
name: recycle-skills
description: Fan out /meta-iterate across every installed skill in parallel, applying candidates that produce a positive composite delta and honestly rejecting those that don't. Use when the user says "recycle skills", "iterate all skills", "run meta-iterate on every skill", "do a round across skills", or "batch improve". Spawns one parallel agent per target skill, each writing only to its own per-skill IMP-LOG.md (parallel-safe). Not for single-skill iteration — use /meta-iterate directly for that.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent, TaskCreate, TaskUpdate, TaskList
version: 1.0.0
---

# Recycle Skills — Parallel /meta-iterate fan-out

Run one /meta-iterate cycle on every installed skill, in parallel. Apply candidates with positive composite delta. Reject honestly when they don't move the needle.

## When to invoke

ON: "recycle skills", "iterate all skills", "run meta-iterate on every skill", "do a round across all", "batch improve skills".

OFF: single-skill iteration. Use `/meta-iterate <skill-name>` directly.

## Prerequisites

- `~/.claude/commands/meta-iterate.md` (per-skill procedure — authoritative)
- `~/.claude/skills/meta-agent-trial/SKILL.md` (harness scaffolder for missing-harness cases)
- A project root where harnesses live at `<project>/.claude/skills/<skill>/evals/`

## Procedure

### Phase 1 — Inventory + triage

1. List installed skills: `ls ~/.claude/skills/` (filter to dirs with SKILL.md).
2. Classify each skill's harness state under the current `<project>`:
   - **Ready**: `<project>/.claude/skills/<skill>/evals/baseline/score.json` has non-zero `composite_score`
   - **Bootstrap-needed**: harness exists, `labels.json` is `[]`, score.json has TODO
   - **Missing**: no `evals/` directory
3. For Ready skills, read `<project>/.claude/skills/<skill>/IMP-LOG.md` "Next iteration target" section.
4. `TaskCreate` one task per skill plus an aggregate task. Mark all in_progress when launching agents.

### Phase 2 — Fan-out (parallel)

Spawn N parallel `Agent` calls in **one message** (multiple tool uses). Each agent gets a self-contained prompt picked from the templates below, plus its skill's specific next-target text.

- Use **Template A** (Recycle) for Ready skills.
- Use **Template B** (Bootstrap) for Bootstrap-needed skills.
- For Missing, the agent's first job is to delegate to `meta-agent-trial` to scaffold the harness.

Constraint: every agent uses a skill-suffixed IMP id (e.g., `IMP-claudekit-<short>-NNNN`) and writes only inside its own skill folder.

### Phase 3 — Track + aggregate

- As notifications fire, `TaskUpdate` each completed task with metadata: `applied`, `composite_before`, `composite_after`, `delta`, `next_target`.
- When all complete, produce one aggregate report with:
  - Table sorted by composite Δ descending
  - Net composite gain across all skills
  - Honest rejects (with reason)
  - Live SKILL.md changes (which canonical user-level files were modified through symlinks)
  - IMP-NNNN+1 priority list ranked by ROI

## Honest-reject criteria

An agent SHOULD reject (not apply) when any of:
- Composite delta ≤ 0
- The targeted submetric didn't move significantly
- Tautology detected (labels coincide with executor's own rules → no discriminating power)
- Guardrail violated (a guarded submetric drops below floor)
- Candidate would regress a saturated dimension by more than the noise floor

Document the rejection reason in IMP-LOG. Honest rejects > cosmetic applies — they preserve future signal capacity.

## Constraints (every agent must follow)

- Write only inside `<project>/.claude/skills/<own-skill>/`. No cross-skill writes.
- Per-skill IMP-LOG.md (parallel-safe). Never write to a shared `skill-improvement-log.md` file.
- No fabricated labels, scores, or snapshots. Honest blocked-status > fake iteration.
- Live SKILL.md edits go through the symlink to `~/.claude/skills/<skill>/SKILL.md` ONLY in --apply mode.
- Always backup before applying: `cp -L ../SKILL.md baseline/inputs/rollback/SKILL.imp-PREV.md`.

## Template A — Recycle agent prompt

```
Run the next /meta-iterate cycle on `<SKILL>` in --APPLY mode.

Working dir: <PROJECT>/.claude/skills/<SKILL>/evals/
Read <PROJECT>/.claude/skills/<SKILL>/IMP-LOG.md — pick IMP id one greater than latest.

Documented next-target: <NEXT_TARGET_TEXT_FROM_IMP_LOG>

Steps:
1. Calibrate against baseline/score.json (must reproduce existing composite).
2. Single-file candidate edit per the documented target. Karpathy-Triplet rule: one editable file per iteration; pair SKILL.md+executor only when the skill's IMP-LOG explicitly documents that pairing is justified.
3. Save to candidates/. Run executor + grader. Compare composite + submetrics.
4. delta > 0: APPLY (backup live → baseline/inputs/rollback/, cp candidate → live, update baseline/score.json). delta ≤ 0: REJECT.
5. Append IMP-N entry to IMP-LOG with: target hypothesis, deltas, applied (yes/no), what-to-try-next.

Constraints: write only inside `<SKILL>/`. No fabrication. No writes to skill-improvement-log.md or skill-evolution.md.

Report under 250 words: composite delta, key submetric deltas, applied (yes/no), next-iteration target.
```

## Template B — Bootstrap agent prompt

```
Bootstrap a real first iteration for `<SKILL>` — labels.json is currently empty.

Working dir: <PROJECT>/.claude/skills/<SKILL>/evals/

Two paths — pick the one that produces honest signal:

PATH A — Real first calibration:
1. Mine real input data from the Mac (~/.claude-desktop, project trees, pain-point logs) matching this skill's domain. ≥30 entries with verifiable ground truth.
2. Hand-label only what's verifiable. No fabrication.
3. Run executor + grader. Capture as IMP-N+1 baseline.

PATH B — Honestly blocked:
Document at <PROJECT>/.claude/skills/<SKILL>/IMP-LOG.md: candidate sources searched, why blocked, cheapest unblock path.

Constraint: no fabricated labels, snapshots, or scores. Path B is more valuable than fake A.

Report under 300 words: path taken, real data assembled, label count, real composite if measured, blocking reasons if any.
```

## When the harness itself is the bottleneck

If two consecutive recycles produce zero deltas across the same skill, the harness has hit a structural ceiling, not a real saturation. Common causes:
- Tautology (labels mirror executor rules)
- Saturated rubric (composite pinned at 1.0 or 0.0)
- Noise floor exceeds plausible deltas (n too small)
- Grader can't see what executor improved (rubric blind spot)

Don't push another iteration through. Run a **harness-fix pass** instead: pivot grader, add adversarial labels, expand n, or add a new submetric. See the `meta-agent-trial` skill for harness scaffolding patterns.

## Reference

Worked example: claudekit commit `e355e2b`. 10 skills × 3 rounds (scaffold → IMP-0001/0002 → harness-fix → IMP-0003 recycle), net +0.575 composite gain with 7 applied, 2 honest rejects, 1 grader-only.
