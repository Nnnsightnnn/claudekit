---
name: Bloat Manager
description: Prevent unbounded growth of skills, memory, error logs, metrics, and documentation. Enforces retention policies, suggests consolidation, and maintains cognitive load limits. Use when checking system health, consolidating files, or managing archives.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Bloat Manager Skill

## Purpose

Help the system grow sustainably. Provide visibility into scale, suggest consolidation opportunities, and maintain awareness of growth patterns by implementing soft limits and managing archives. **Never blocks, only advises.**

## Philosophy

- **Grow organically**: Artifacts should expand to meet real needs
- **Warn early**: Surface metrics before they become problems
- **Suggest, don't enforce**: Recommendations, not restrictions
- **Archive liberally**: Keep history accessible, just tiered
- **Delete reluctantly**: Only after extended dormancy

Soft limits educate rather than frustrate. They allow justified exceptions while building awareness over time.

## Auto-Activation Triggers

- Weekly maintenance review (every Monday)
- User says "check for bloat", "cleanup review", "consolidate", or "clean up skills"
- Any tracked file exceeds size or count thresholds
- Monthly archival cycle / quarterly consolidation review

## The Bloat Problem

Self-improving systems naturally accumulate skills, error history, metrics, documentation, and archives. Without management, context windows overflow, cognitive load rises, and effectiveness decreases.

## Threshold Architecture

```
HEALTHY → APPROACHING (80%) → EXCEEDED (100%) → CRITICAL (120%)
```
- **Healthy** (< 80%): No action
- **Approaching** (80–99%): Suggest review
- **Exceeded** (100–119%): Recommend action
- **Critical** (120%+): Escalate priority

## Tiered Storage Architecture

- **Tier 1 — Active (always loaded):** CLAUDE.md (< 400 lines), quick-reference.md (< 100 lines), active skills.
- **Tier 2 — Warm (on demand):** procedural-memory.md (< 300KB), active pain points, error-history.json (last 30 days), skill-metrics.json (last 90 days).
- **Tier 3 — Cold (archived):** `.claude/archives/` (older than 90 days), deprecated skills, historical metrics.
- **Tier 4 — Delete (after retention):** duplicate entries, superseded skills (6 months archived), transient error logs (1 year).

## Soft Limits Reference

### File Size Limits

| Artifact | Soft Limit | Review Trigger | Critical |
|----------|------------|----------------|----------|
| CLAUDE.md | 400 lines | 450 lines | 500 lines |
| quick-reference.md | 100 lines | 120 lines | 150 lines |
| procedural-memory.md | 500 lines / 250KB | 600 lines / 300KB | 750 lines |
| episodic-memory.md | 200 lines | 250 lines | 300 lines |
| Individual SKILL.md | 300 lines | 350 lines | 400 lines |
| ai-pain-points.md | 50 active | 75 active | 100 active |
| ai-error-history.json | 100 entries | 150 entries | 200 entries |
| skill-metrics.json | 500KB | 750KB | 1MB |

### Count Limits

| Category | Soft Limit | Review Trigger | Critical |
|----------|------------|----------------|----------|
| Active skills | 30 | 40 | 50 |
| Skills per category | 5 | 8 | 10 |
| Active pain points | 50 | 65 | 80 |
| Error history entries | 100 | 150 | 200 |
| Patterns in quick-ref | 20 | 25 | 30 |
| Unused skills (90 days) | 3 | 5 | — |
| Low success skills (< 60%) | 2 | 4 | — |

### Retention Policies

| Content Type | Hot | Warm | Cold (Archive) | Delete |
|--------------|-----|------|----------------|--------|
| Patterns | Rolling 6 months | — | Unused 6 months | Never |
| Session summaries | 30 days | — | After 30 days | After 1 year |
| Error history | 7 days | 30 days | 90 days | 1 year |
| Skill metrics | 30 days | 90 days | 1 year | 2 years |
| Resolved pain points | 30 days | 90 days | 6 months | 1 year |
| Archived skills | — | — | 6 months | 1 year |
| Improvement logs | 90 days | 1 year | 2 years | Never |

## Core Workflow

### Step 1: Gather Metrics

Collect current state of all monitored artifacts:

```bash
# Count lines in key files
wc -l .claude/CLAUDE.md
wc -l .claude/memory/active/quick-reference.md
wc -l .claude/memory/active/procedural-memory.md
wc -l .claude/memory/active/episodic-memory.md

# Count skills
find .claude/skills -name "SKILL.md" | wc -l

# Count active pain points
grep -c "^### " .claude/pain-points/active-pain-points.md

# Count error history entries
python3 -c "import json; print(len(json.load(open('.claude/pain-points/ai-error-history.json')).get('errors', {})))"
```

### Step 2: Assess Health Status

For each metric, determine status:
- **Healthy**: Below 80% of soft limit
- **Approaching**: 80–99% of soft limit
- **Exceeded**: 100–119% of soft limit
- **Critical**: 120%+ of soft limit

### Step 3: Generate Health Report

Present findings in clear format:

```markdown
## System Health Report - YYYY-MM-DD

### Summary
- Overall Status: [Healthy / Needs Attention / Action Required]
- Items Approaching Limits: N
- Items Exceeding Limits: N

### Detailed Metrics

| Artifact | Current | Limit | Status |
|----------|---------|-------|--------|
| CLAUDE.md | 385 lines | 400 | Approaching (96%) |
| Skills | 28 | 30 | Approaching (93%) |
| Pain Points | 42 | 50 | Healthy (84%) |

### Recommended Actions
1. [Specific action for exceeded items]
2. [Specific action for approaching items]
```

### Step 4: Propose Consolidation (if needed)

For items needing attention:

**For CLAUDE.md bloat:**
- Identify sections that can move to `.claude/specs/` or linked docs
- Find redundant or outdated rules
- Suggest merging related specifications

**For skill bloat:**
- Identify similar skills that can merge (overlapping triggers, sequential invocation patterns)
- Find unused skills (no invocations in 90 days)
- Suggest deprecating obsolete skills

**For memory bloat:**
- Identify patterns to archive (unused 6+ months)
- Find duplicate or near-duplicate entries
- Suggest consolidating related patterns

**For pain point bloat:**
- Identify resolved pain points to archive
- Find stale pain points (no updates in 60 days)
- Suggest closing or escalating old items

### Step 5: Execute Approved Actions

Only after user approval:
- Move content to archives
- Consolidate files
- Update references
- Document changes in episodic memory

## Specialized Workflows

### Skill Consolidation Review (Monthly)

Identify skills that should be merged.

**Consolidation Criteria:**
- Overlapping triggers (> 50% similarity)
- Same error category
- Sequential invocation pattern (A always followed by B)
- Low individual usage but combined usage is high

**Consolidation Process:**
1. Identify candidate skills
2. Analyze trigger overlap
3. Design merged skill
4. Migrate functionality
5. Deprecate originals
6. Update all references

**Output:** Per-candidate block listing overlap %, combined invocations, and recommendation (MERGE / KEEP SEPARATE / DEPRECATE). See Example 3 below for the full shape.

### Error History Pruning (Weekly)

```python
# Pseudo-logic for error history pruning
for fingerprint in error_history:
    if fingerprint.last_seen > 90_days_ago:
        if fingerprint.resolved:
            move_to_archive(fingerprint)
        else:
            keep_but_flag_stale(fingerprint)

    if fingerprint.last_seen > 1_year_ago:
        delete(fingerprint)

    if fingerprint.count == 1 and fingerprint.age > 30_days:
        delete(fingerprint)  # One-off errors, not patterns
```

### Documentation Consolidation (Quarterly)

**CLAUDE.md Maintenance:**
- Remove references to deprecated skills
- Consolidate similar spec IDs
- Move detailed explanations to linked docs
- Keep only actionable, current content

**Pattern:**
```markdown
# Before (bloated)
**[SPEC-001]** Long detailed explanation of feature A with
multiple lines of context and examples that could be in a
separate document...

# After (lean)
**[SPEC-001]** Feature A: [one-line summary] → See `docs/feature-a.md`
```

### Archive Workflow (Monthly)

1. Identify items past retention threshold
2. Create archive file: `.claude/archives/YYYY-MM-[type].md`
3. Move items with full context preserved
4. Update source files to remove archived content
5. Add archive reference for traceability

**Archive file format:** Header with metadata (date, source, item count, reason), then each archived item with full original content preserved plus its original location and archive reason.

## Cognitive Load Management

### Progressive Disclosure Pattern

Three levels keep cognitive load low:
- **Level 1 (always visible)** — one-line summaries in CLAUDE.md, e.g. `**[SPEC-001]** Detect-Decide-Act on every tool failure → .claude/skills/error-learner/`
- **Level 2 (on demand)** — paragraph explanations in the skill file's Purpose section
- **Level 3 (deep dive)** — full documentation with examples in linked docs

### Limit Active Context

**Rule:** No more than 20 active items in any tracking document.

When limit approached:
1. Force prioritization
2. Archive lowest priority items
3. Consolidate similar items
4. Question if all items are still relevant

## Skill Lifecycle States

`CREATED → ACTIVE → DEPRECATED → ARCHIVED → DELETE`, with `Any → MERGED` available during consolidation.

- **CREATED → ACTIVE**: After first successful invocation
- **ACTIVE → DEPRECATED**: 90 days no use, OR < 50% success after improvements
- **DEPRECATED → ARCHIVED**: 30 days after deprecation
- **ARCHIVED → DELETE**: 6 months after archival
- **Any → MERGED**: Functionality absorbed into another skill during consolidation review

## Automatic Review Triggers

**Note**: These are suggestions, not blocks. The system warns and recommends but doesn't prevent growth.

| Trigger | Action |
|---------|--------|
| CLAUDE.md > 400 lines | Gentle reminder to consider refactoring |
| CLAUDE.md > 450 lines | Suggest moving content to linked docs |
| Skills > 30 | Suggest quarterly consolidation review |
| Skills > 40 | Recommend consolidation review this week |
| Error history > 100 | Suggest pruning oldest resolved entries |
| Error history > 150 | Auto-archive entries > 90 days old |
| Pain points > 50 active | Suggest prioritization review |
| Any skill 0 invocations in 90 days | Flag for review (keep if intentional) |
| Any skill < 60% success rate | Prioritize for skill-improver attention |

## Edge Cases

### Monday Falls on Holiday
**Condition**: Weekly check lands on a holiday
**Handling**: Run check on next working day, note delay in report

### Multiple Items Critical
**Condition**: Several artifacts exceed critical thresholds
**Handling**: Prioritize by impact — CLAUDE.md > skills > memory > pain points

### New Project (Few Artifacts)
**Condition**: Project is new, most metrics near zero
**Handling**: Skip check, note "healthy — early stage project"

### Archive Directory Missing
**Condition**: Archive target doesn't exist
**Handling**: Create archive structure before moving files

## Integration Points

### With Pain Point Manager
- Archive resolved pain points
- Track bloat-related friction as new pain points

### With Memory System
- Log consolidation actions in episodic memory
- Update procedural memory with new patterns discovered

### With Skill Metrics
- Use invocation data to identify unused skills
- Track bloat manager effectiveness over time

### With Skill Builder (gate before creation)
- Check: Would new skill exceed limit? If yes, suggest consolidation first.

### With Skill Improver (gate after improvement)
- Check: Did improvement increase file size significantly? If yes, flag for review.

### With Error Learner (gate during cataloging)
- Check: Would new entry exceed history limit? If yes, prune oldest resolved entries first.

## Output Examples

### Example 1: Healthy System

**Trigger**: Weekly Monday check
**Response**: One-paragraph "all artifacts within limits, no action required" plus the metrics table from Step 3. Note next scheduled check date.

### Example 2: Action Required

**Trigger**: User says "check for bloat"
**Response**:
```markdown
## System Health Report - 2026-01-16

Overall Status: **Action Required** — 2 items exceeding limits, 1 approaching.

| Artifact | Current | Limit | Status |
|----------|---------|-------|--------|
| CLAUDE.md | 456 lines | 400 | **Exceeded (114%)** |
| Skills | 35 | 30 | **Exceeded (117%)** |
| Pain Points | 45 | 50 | Approaching (90%) |

### Recommended Actions

1. **CLAUDE.md (High):** Move deployment specs (lines 180–250) to `.claude/specs/deployment.md`; archive deprecated 2025 rules (lines 312–340). Expected reduction: ~100 lines.
2. **Skills (High):** Merge `data-validator` + `input-checker`; archive `legacy-formatter` (0 invocations in 60 days). Expected reduction: 5 skills.
3. **Pain Points (Medium):** Review 12 pain points older than 30 days; 5 appear resolved but not archived.

Shall I proceed?
```

### Example 3: Skill Consolidation

```markdown
## Skill Consolidation Review - 2026-01-31

**MERGE RECOMMENDED**
- `error-learner` + `skill-improver` — Trigger overlap 35%, sequential pattern 78%.
  Recommendation: **Keep separate** — distinct responsibilities (detection vs improvement); overlap is intentional pipeline stages.

**DEPRECATE RECOMMENDED**
- `legacy-data-checker` — last invoked 112 days ago, absorbed by data-pipeline skill. Action: move to deprecated, archive in 30 days.
```

## Maintenance Schedule

| Frequency | Task |
|-----------|------|
| Weekly (Monday) | Size check, error history prune |
| Monthly (1st) | Skill consolidation review, archive cycle |
| Quarterly | Documentation consolidation, full audit |
| Yearly | Deep archive review, permanent deletions |

## Best Practices

### 1. Prefer Consolidation Over Accumulation
When adding new content, first ask: "Can this be merged with existing content?"

### 2. Delete Aggressively, Archive Conservatively
- If something might be needed: Archive
- If something is definitely obsolete: Delete
- If unsure: Archive with 6-month review flag

### 3. Maintain Cognitive Load Limits
The system should remain understandable. If it takes more than 5 minutes to explain the skill ecosystem, it's too complex.

### 4. Review Limits Periodically
Limits should evolve. If 30 skills is consistently too few, the real problem may be skill granularity, not the limit.

## Error Handling

### If File Read Fails
1. Log the error
2. Mark that artifact as "Unable to assess"
3. Continue with other artifacts
4. Note incomplete assessment in report

### If Archive Write Fails
1. Do not delete original
2. Report failure to user
3. Suggest manual intervention
4. Log in error history

### If Metrics File Corrupted
1. Back up corrupted file
2. Initialize fresh metrics file
3. Note data loss in report
4. Continue with available data

## Skill Metadata

**Version:** 1.1.0
**Created:** 2025-12-31
**Last Updated:** 2026-05-08 (consolidation merge — absorbed playmakers fork)
**Category:** System Maintenance & Governance
**Integration:** Memory System, Pain Points, Skill Metrics, Skill Builder, Skill Improver, Error Learner
**Schedule:** Weekly checks, Monthly reviews, Quarterly audits
