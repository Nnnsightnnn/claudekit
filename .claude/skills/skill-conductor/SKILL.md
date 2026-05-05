---
name: Skill Conductor
description: Orchestrates the entire Claude skill surface — audit, recommend, fix drift, start trials, upgrade existing skills, run the morning routine. The control plane for managing/fixing/upgrading skills using the tools already in place (repo-skill-inventory scanner, meta-agent-trial, /meta-iterate, bloat-manager, coherence, skill-builder, skill-improver, the 3 dashboards). Use when the user asks "what should I work on", "audit my skills", "fix drift", "upgrade <skill>", "morning routine", "weekly review", or any high-level question about the state and direction of the skill ecosystem.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Skill
version: 1.0.0
---

# Skill Conductor

## Purpose

You have ~10 user-level skills, ~28 repo-level skills, 3 live dashboards, scheduled scanner and retention tasks, an IMP log, a trial harness, and a templates library. **This skill is the control plane that uses all of that machinery to answer high-level questions about the skill ecosystem and execute the right next move.**

It does not replace any existing skill. It orchestrates them.

## When to use this skill

Trigger on any of these intents:

- "**Audit** my skill surface" / "what's the state of my skills" / "are there any drift issues"
- "**What should I work on next**?" / "recommend a trial" / "where's the leverage"
- "**Fix drift**" / "consolidate" / "clean up duplicates"
- "**Upgrade <skill-name>**" / "make <skill> better" / "this skill keeps failing"
- "**Start a trial** on <skill>" (delegates to meta-agent-trial)
- "**Morning routine**" / "weekly review" / "skill standup"
- "Show me **what's stale**" / "what hasn't been touched"
- "Has any skill **regressed**?"
- "Check the meta-agent **gates**" / "is anything stuck"

If the user asks for a single, focused skill action (e.g., "run iteration 6 on ai-error-learner"), delegate directly — invoke `/meta-iterate ai-error-learner` instead of running the full Conductor flow.

## Tool inventory (what the Conductor orchestrates)

| Tool | Path | Purpose |
|---|---|---|
| `repo-skill-inventory` scanner | `~/.claude/skills/repo-skill-inventory/scanner.py` | Walks every `.claude/skills/` dir, produces structured JSON inventory |
| `meta-agent-trial` skill | `~/.claude/skills/meta-agent-trial/` | Instantiates a Karpathy-Triplet eval harness for a new target skill |
| `meta-agent-trial/LESSONS.md` | same dir | 9 cross-trial structural lessons; consult before starting any trial |
| `meta-agent-trial/templates/` | same dir | Templates for fresh harness (evals.json, executor.py, grader.py, etc.) |
| `/meta-iterate` slash command | `~/.claude/commands/meta-iterate.md` | Single iteration on an existing trial (calibrate → propose → score → decide → log) |
| `bloat-manager` skill | `~/.claude/skills/bloat-manager/` | Detects + trims skill sprawl |
| `coherence` skill | `~/.claude/skills/coherence/` | Cross-skill contradiction check |
| `skill-builder` skill | `~/.claude/skills/skill-builder/` | Transforms pain points into new skills |
| `skill-improver` skill | `~/.claude/skills/skill-improver/` | Rewrites SKILL.md based on failure traces |
| `pain-point-manager` | `~/.claude/skills/pain-point-manager/` | Captures recurring friction |
| Skill DB artifact | `kenny-skill-database` (Cowork) | Live skill inventory dashboard |
| Stale Content artifact | `stale-content-detector` (Cowork) | Surfaces stale memory/skills/worktrees |
| Trial Status artifact | `trial-status-dashboard` (Cowork) | Per-skill trial state, IMP history, scores |
| Scanner output | `~/.claude-desktop/exports/skill-inventory-latest.json` | Fresh JSON from latest scan |
| IMP ledger | `~/playmakers-data/.claude/skills/skill-improvement-log.md` | Authoritative trial log |
| Trajectory memory | `~/.claude-desktop/memory/domains/skill-evolution.md` | Cross-trial patterns |
| Quick reference | `~/.claude-desktop/memory/active/quick-reference.md` | Operational state map |
| Security TODOs | `~/.claude-desktop/memory/domains/security-todo.md` | Manual follow-ups |
| Scheduled tasks | `~/Library/LaunchAgents/com.kenny.*.plist` | Weekly scanner + monthly worktree prune |
| Maintenance scripts | `~/.claude/scripts/` | rotate-claude-json.sh, prune-stale-worktrees.sh |

## Workflows

Each workflow is a discrete user intent. Pick the one that matches the user's request. Don't run all of them on every invocation.

### Workflow A — Audit (default for "what's the state of my skills")

1. Run `python3 ~/.claude/skills/repo-skill-inventory/scanner.py` — fresh JSON in `~/.claude-desktop/exports/skill-inventory-latest.json`.
2. Parse the JSON. Surface:
   - Total skills, user-level vs repo-level breakdown
   - Number of drifted vs identical vs unique
   - Count of high-severity alerts (drift / bloat / orphan / stale)
   - Trial coverage (skills with `evals/` dir vs without)
3. Read `~/playmakers-data/.claude/skills/skill-improvement-log.md` — extract `Last Improvement ID`, count of IMPs by status (applied / rejected / pending).
4. Output a concise audit: 5-8 bullet summary + a "needs attention" list (any high-severity alerts).
5. Recommend: tell the user which workflow to run next based on findings.

### Workflow B — Recommend ("what should I work on next?")

The leverage hierarchy, evaluated in this order:

1. **G2-rejected pending** — any IMP-XXXX in the log with status `pending` and a positive score delta unreviewed for >24h. **Highest urgency** — the loop is blocked.
2. **Active trial regressions** — any current trial with composite score declining for 2+ iterations. **High** — needs harness audit (Lesson #4 / #6).
3. **Drift > 30 days** between user-level and an "advanced fork" version (e.g., playmakers-data forks). Worth merging or formalizing.
4. **Untrialed skills with high data leverage** — skills that meet the meta-agent-trial Phase 0 criteria (data on disk, closed-form output, named failure mode) but have no `evals/` dir yet. Top candidates: `code-review` in workout-app, `liverpool-tracker-update`, `repo-skill-inventory` itself.
5. **Stale memory** in `~/.claude-desktop/memory/active/` (>14 days). Means the active-maintenance commitment from D1 has lapsed.
6. **Worktree bloat** — any repo's `.claude/worktrees/` over 100 MB (especially under 30d, those eligible for retention soon).
7. **Outstanding security TODOs** — any unactioned items in `~/.claude-desktop/memory/domains/security-todo.md`.

Output: top 3 recommended actions with concrete commands. NEVER more than 3 — the user asked for a recommendation, not a backlog.

### Workflow C — Fix drift / Consolidate

1. Run scanner. Identify all `drift_status: drifted` skills.
2. For each:
   - Show user-level vs repo-level hashes + mtimes + line counts
   - Classify: `claude-fork-pattern` (playmakers-data has its own advanced fork) or `genuine-drift` (someone edited a copy elsewhere)
3. For `genuine-drift`: invoke `coherence` skill to check whether the divergence is intentional. If not, propose merge.
4. For `claude-fork-pattern` (the dominant case in this surface): leave alone — it's by design.
5. After cleanup, re-run scanner; confirm drift count dropped.
6. Update the kenny-skill-database artifact (it auto-fetches from scanner).

### Workflow D — Upgrade <skill-name>

This is the end-to-end "make this skill better" flow.

1. Check whether the target skill has an `evals/` harness:
   - If YES: it's an existing trial. Run `/meta-iterate <skill-name>` for one iteration. Done.
   - If NO: it's a new trial. Continue.
2. Check Phase 0 of `meta-agent-trial` SKILL.md — does this skill have:
   - Accumulated runtime data on disk?
   - Closed-form output structure?
   - Named failure mode?
3. If any "no" — stop. Tell the user the skill isn't ready for the loop; recommend `skill-improver` instead for a one-shot rewrite based on a failure trace.
4. If all "yes" — invoke `meta-agent-trial` skill ("Start a meta-agent trial for `<skill-name>`"). It walks Phase 1-8 from the SKILL.md.

### Workflow E — Morning routine / Weekly review

A composite of A + B + status checks. Output structure:

```
## Skill Surface — Morning Brief

[Audit numbers, 1 line each]

## Active trials
[For each trial with an evals/: skill name, current composite, last IMP, gate phase, days since last activity]

## What to do today
[Top 3 from Workflow B's leverage hierarchy]

## Quiet alerts (not urgent but worth knowing)
[Any low-severity alerts that haven't been on the priority list]
```

Length cap: under 400 words. The point is signal, not exhaustiveness.

### Workflow F — Health check

For when the user wants to know "is the machinery actually running"?

1. Verify `launchctl list | grep com.kenny` — both LaunchAgents loaded?
2. Check `~/.claude-desktop/exports/scanner-cron.log` mtime — has the scheduled scanner run in the last 8 days?
3. Read `~/.claude-desktop/exports/skill-inventory-latest.json` — is it less than 7 days old?
4. Spot-check: open the kenny-skill-database artifact — does it render?
5. Verify all 3 dashboard artifacts exist via Cowork.
6. Report: green / yellow / red per check.

If anything's red, recommend the fix command directly.

## Meta-Agent gate awareness

The Conductor must respect governance gates:

- **G1** (first 5 IMPs require human approval): if a trial is in G1 phase, never auto-apply candidates. Always surface for review.
- **G2** (auto-reject if composite doesn't improve): tied scores are rejections. Document the rejection in the IMP log; don't whitewash it.
- **G3** (every accepted IMP appends to skill-evolution.md): when applying an IMP, ALSO update the trajectory memory.
- **G4** (after 5 successful gated iterations, "approved unless rejected within 24h"): trials past G1 can auto-apply. The 24h pending state is itself a Workflow B trigger.

If a trial's gate phase is unclear, default to G1 behavior (require explicit approval).

## Cross-trial lessons enforcement

When delegating to `meta-agent-trial`, ALWAYS surface a reminder to read `LESSONS.md` first. The 9 lessons are:

1. Hand-labeled prefixes must byte-match the snapshot
2. Contexts are wrapped python-repr dicts, not raw stdout
3. Cluster-pair lookups need exact keys
4. Question the harness as aggressively as the skill
5. Rubric weights are themselves a hypothesis
6. Stuck score → audit the harness, not the skill
7. Track candidates separately from live; never edit live
8. Ties are rejections under G2
9. Stripping rules can over-cluster; preserve enough signature

Lessons 1-3 and 7 are mechanically prevented by templates. Lessons 4-6, 8, 9 require operator vigilance — the Conductor surfaces them when invoking trials.

## Output style

- **Concise.** The Conductor's job is to surface signal. If the audit can be summarized in 8 bullets, don't write 30.
- **Concrete commands.** Every recommendation includes the exact command to run.
- **No "would you like me to" loops.** The Conductor recommends; the user decides; if the user says "do it," execute without asking again.
- **Cite sources.** Every assertion ties back to a file: scanner JSON, IMP log, dashboard artifact, etc.
- **Respect gates.** Never bypass G1-G4 for speed.

## Anti-patterns (don't do these)

- **Don't run all 6 workflows on every invocation.** Pick the one that matches the user's intent.
- **Don't re-derive findings the dashboards already show.** If the user can see it in the artifact, link to it instead of duplicating in chat.
- **Don't bypass `meta-agent-trial`'s Phase 0 checks** even if the user is impatient. The dry-run prevents wasted iteration budget.
- **Don't mutate without first running the scanner.** State that's stale by even a few hours can lead to surprising deletes.
- **Don't promote candidates without an IMP entry.** Every applied change must be logged.

## Skill metadata

**Version:** 1.0.0
**Created:** 2026-04-30
**Category:** Self-Improvement & Meta-Agent / Surface Management
**Companion:** `meta-agent-trial`, `repo-skill-inventory`, `bloat-manager`, `coherence`, `skill-builder`, `skill-improver`, `pain-point-manager`
**Reference:** `~/.claude-desktop/memory/active/quick-reference.md` (current state map)
