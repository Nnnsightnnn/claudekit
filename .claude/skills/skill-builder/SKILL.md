---
name: Skill Builder
description: Master skill that transforms AI pain points into working skills. Uses /deep-investigate for research, creates skill files, and updates pain point tracking.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Skill, Task
---

# Skill Builder Skill

## Purpose

The capstone of the self-improvement system. This skill takes cataloged AI pain points, conducts deep investigation to understand the problem thoroughly, builds a comprehensive skill to solve it, and updates all tracking documents.

## Auto-Activation Triggers

This skill activates when:
- An AI pain point has been cataloged and is ready for skill creation
- AI Error Learner escalates a pain point (3+ occurrences) — auto-trigger for high-priority issues
- User says "build a skill for [pain point]" or "create skill from AI pain point"
- User approves a proposed skill from ai-error-learner
- Weekly review identifies unaddressed AI pain points
- Manual invocation with pain point ID

## The Complete Self-Improvement Loop

```
┌────────────────────────────────────────────────────────────────┐
│                    SELF-IMPROVEMENT SYSTEM                      │
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐     │
│  │   Error      │    │  AI Error    │    │    Skill     │     │
│  │   Occurs     │───▶│   Learner    │───▶│   Builder    │     │
│  │              │    │  (Catalog)   │    │  (Create)    │     │
│  └──────────────┘    └──────────────┘    └──────────────┘     │
│         ▲                                       │              │
│         │                                       ▼              │
│  ┌──────────────┐                        ┌──────────────┐     │
│  │    Skill     │                        │     New      │     │
│  │   Improver   │◀───────────────────────│    Skill     │     │
│  │  (Refine)    │     (if fails)         │   Created    │     │
│  └──────────────┘                        └──────────────┘     │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

## Core Workflow

### Phase 1: Pain Point Selection

**Input**: AI Pain Point ID or description

```markdown
1. Read `.claude/pain-points/ai-pain-points.md`
2. Identify target pain point by:
   - Explicit ID (e.g., "AI-PAIN-0001")
   - Highest occurrence count
   - User selection
   - Priority level
3. Extract pain point details:
   - Error fingerprint
   - Occurrence count
   - Contexts encountered
   - Existing proposed skill (if any)
```

**Helpers:**

By ID:
```bash
grep -A 20 "AI-PAIN-0012" .claude/pain-points/ai-pain-points.md
```

By highest occurrence:
```bash
python3 -c "
import json
data = json.load(open('.claude/pain-points/ai-error-history.json'))
sorted_errors = sorted(data.get('errors', {}).items(), key=lambda x: x[1].get('count', 0), reverse=True)
for fp, info in sorted_errors[:5]:
    print(f\"{info.get('count', 0):3d} | {fp} | {info.get('pain_point_id', 'N/A')}\")
"
```

### Phase 2: Deep Investigation

**Use `/deep-investigate` skill for comprehensive research**

```markdown
Invoke: /deep-investigate

Investigation Prompt:
"Investigate the recurring error pattern: [error fingerprint]

Context:
- Error type: [type]
- Occurrences: [count]
- Contexts: [list of contexts]

Research needed:
1. Root cause analysis - why does this error occur?
2. Existing solutions - are there patterns in the codebase that handle this?
3. Best practices - how do similar projects solve this?
4. Edge cases - what variations of this error exist?
5. Prevention strategies - how can we avoid triggering this error?
6. Recovery strategies - when error occurs, what's the best response?

Output needed:
- Comprehensive understanding of the problem
- Recommended skill approach
- Required tools and integrations
- Potential edge cases to handle
- Success criteria for the skill"
```

If `/deep-investigate` is unavailable, perform basic investigation manually:

1. **Reproduce the error context** — what actions trigger it, what environment conditions, what files/tools are involved
2. **Analyze root cause** — knowledge gap (needs documentation), process gap (needs workflow), or tool gap (needs automation)
3. **Review existing solutions** — similar skills, related patterns in memory, prior approaches

### Phase 3: Skill Planning

**Design the skill based on investigation findings**

```markdown
## Skill Plan: [Skill Name]

### Problem Statement
[Clear description of what this skill solves]

### Trigger Conditions
[When this skill should activate - be specific]

**Good Triggers:**
- "When user runs `pytest` and tests fail with import errors"
- "When creating files in `/scripts/` directory"
- "When git push is rejected due to hooks"

**Bad Triggers:**
- "When something goes wrong" (too vague)
- "When user is frustrated" (not observable)
- "When appropriate" (undefined)

### Workflow Steps
1. [Detection step]
2. [Analysis step]
3. [Action step]
4. [Verification step]

Each step should be atomic (one clear action), include decision points, show concrete commands, and handle branches (what if step fails?).

### Required Tools
- [Tool 1]: [Why needed]
- [Tool 2]: [Why needed]

### Edge Cases
- [Edge case 1]: [How to handle]
- [Edge case 2]: [How to handle]

### Success Criteria
- [Criterion 1]
- [Criterion 2]

### Integration Points
- [With skill X]
- [With system Y]

### Failure Modes
- [What could go wrong]
- [How skill-improver would detect failure]
```

### Phase 4: Skill Creation

**Build the actual skill file**

1. **Create skill directory**
   ```bash
   mkdir -p .claude/skills/[skill-name]/
   ```

2. **Write SKILL.md** using the standard template:

```markdown
---
name: [Skill Name]
description: [One-line description]. [When to use].
allowed-tools: [comma-separated tool list]
---

# [Skill Name] Skill

## Purpose
[Detailed purpose from investigation]

## Auto-Activation Triggers
This skill activates when:
- [Observable trigger 1]
- [Observable trigger 2]
- [User phrase triggers]

## CRITICAL: [Key Protocol Name]

**[Key behavioral requirement]**

### [Subsection as needed]
[Content based on investigation]

## Core Workflow

### Step 1: [First Step]
[Detailed instructions with commands]

### Step 2: [Second Step]
[Detailed instructions with commands]

### Step 3: [Third Step]
[Detailed instructions with commands]

## Edge Cases

### [Edge Case 1]
**Condition**: [When this occurs]
**Handling**: [What to do]

### [Edge Case 2]
**Condition**: [When this occurs]
**Handling**: [What to do]

## Integration Points

### With [System/Skill]
[How it integrates]

## Output Examples

### Example 1: [Scenario]
**Trigger**: [What triggers it]
**Response**: [What skill does]

## Error Handling

### If [Failure Mode]
1. [Recovery step 1]
2. [Recovery step 2]
3. [Fallback behavior]

## Skill Metadata

**Version:** 1.0.0
**Created:** YYYY-MM-DD
**Created From:** [AI-PAIN-XXXX]
**Category:** [Category]
**Integration:** [Systems it integrates with]
```

3. **Create any supporting files** (JSON configs, templates, etc.)

### Phase 5: Documentation Updates

**Update all tracking documents**

#### Update AI Pain Points

Edit `.claude/pain-points/ai-pain-points.md`:

```markdown
### [AI-PAIN-XXXX] [Description]

- **Status**: RESOLVED
- **Resolution Date**: [Today's date]
- **Skill Created**: `[skill-name]/`
- **Skill Location**: `.claude/skills/[skill-name]/SKILL.md`
- [Rest of original content preserved]
```

Move to "Recently Resolved" section.

#### Update CLAUDE.md

Add new skill to `[SKILL-00002]` (if frequently used):

```markdown
**[SKILL-00002]** Available Skills: ... • `[skill-name]/` ([brief description])
> TRIGGER: [When to use]
```

#### Update Skill Metrics

Initialize in `.claude/skills/skill-metrics.json`:

```json
{
  "[skill-name]": {
    "invocations": 0,
    "successes": 0,
    "failures": 0,
    "success_rate": null,
    "created_from": "AI-PAIN-XXXX",
    "created_at": "[timestamp]",
    "failure_patterns": [],
    "improvements": []
  }
}
```

#### Update Error History

Edit `.claude/pain-points/ai-error-history.json`:

```json
{
  "[fingerprint]": {
    ...
    "resolved": true,
    "resolved_by_skill": "[skill-name]",
    "resolved_at": "[timestamp]"
  }
}
```

#### Log in Episodic Memory

```markdown
### New Skill Created
- Skill: [skill-name]
- Origin: AI-PAIN-NNNN
- Purpose: [brief description]
```

### Phase 6: Verification

**Confirm skill is properly created and integrated**

```bash
# Check skill file exists and has valid frontmatter
head -10 .claude/skills/[skill-name]/SKILL.md

# Verify YAML is valid
python3 -c "import yaml; yaml.safe_load(open('.claude/skills/[skill-name]/SKILL.md').read().split('---')[1])"

# Check metrics file updated
cat .claude/skills/skill-metrics.json | python3 -m json.tool
```

```markdown
## Skill Creation Verification Checklist

□ Skill directory exists: `.claude/skills/[skill-name]/`
□ SKILL.md has valid YAML frontmatter
□ All required sections present in SKILL.md
□ Triggers are specific and actionable
□ Workflow is complete and logical
□ Edge cases documented
□ AI Pain Point marked resolved
□ CLAUDE.md updated with new skill
□ Skill metrics initialized
□ Error history updated

## Integration Test

□ Manually trigger skill scenario
□ Verify skill activates
□ Confirm desired outcome achieved
□ Check for any errors
```

## Skill Quality Standards

### Required Sections
Every skill MUST have:
1. YAML frontmatter (name, description, allowed-tools)
2. Purpose statement
3. Auto-Activation Triggers (specific, testable)
4. Core Workflow (step-by-step)
5. Edge Cases
6. Output Examples
7. Error Handling
8. Skill Metadata

### Trigger Quality
Triggers must be:
- Specific (not "when appropriate")
- Observable (can detect in real-time)
- Actionable (can verify activation)
- Non-overlapping (don't conflict with other skills)

### Workflow Quality
Workflows must be:
- Complete (cover the full solution)
- Sequential (clear order of operations)
- Verifiable (can confirm each step worked)
- Recoverable (handle failures gracefully)

## Edge Cases (Skill-Builder Itself)

### Pain Point Has No Clear Solution
**Condition**: Investigation doesn't reveal automated solution
**Handling**: Create documentation pattern instead of skill, mark pain point as "documented"

### Similar Skill Already Exists
**Condition**: Existing skill covers 80%+ of use case
**Handling**: Extend existing skill rather than create new one

### Solution Requires External Changes
**Condition**: Fix requires config/environment changes, not automation
**Handling**: Document in quick-reference, create setup skill if applicable

### Skill Would Be Too Complex
**Condition**: Solution requires >400 lines or multiple sub-skills
**Handling**: Break into smaller skills with clear dependencies

## Output Format

### Successful Skill Creation

Report back with: skill name, location, source pain point ID, summary, triggers, key workflow steps, list of updates made (pain points / CLAUDE.md / metrics / error history), and next steps (test, monitor, check skill-improver). Close with: "The self-improvement loop is now complete for this pain point."

### Example: Full Workflow

**Input**: "Build a skill for AI-PAIN-0001 (Python module import fails)"

| Phase | Output |
|-------|--------|
| 1. Selection | AI-PAIN-0001 — `ModuleNotFoundError` for project deps, 3 occurrences, contexts: scripts run outside project venv |
| 2. Investigation | Root cause: deps live only in a project-specific venv (e.g., `~/.venvs/<project>`). Solution: auto-detect imports, activate venv. Edge cases: mixed imports, already-active venv. Tools: Bash, Read |
| 3. Planning | Skill `python-venv-runner` — trigger on Python execution with project-specific imports; workflow: detect → activate → execute → report; success: no `ModuleNotFoundError` |
| 4. Creation | `.claude/skills/python-venv-runner/SKILL.md` written — all required sections, 5 triggers, 4-step workflow, 3 edge cases |
| 5. Docs | `ai-pain-points.md` resolved, CLAUDE.md updated, `skill-metrics.json` initialized, `ai-error-history.json` marked resolved |
| 6. Verify | Files valid, YAML parses, structure correct, ready for use |

## Integration with Other Skills

### Inputs From
- **ai-error-learner**: Provides AI Pain Points to build skills for
- **User**: Direct requests to build skills

### Outputs To
- **skill-improver**: New skills to monitor and improve
- **All skills**: New capabilities added to the system

### Invokes
- **/deep-investigate**: For comprehensive research before building

### With Memory System
- Logs skill creation in episodic memory
- May discover related patterns in procedural memory
- Updates quick-reference for common skills

## Automatic Triggers

| Condition | Action |
|-----------|--------|
| AI Pain Point at 3+ occurrences | Auto-invoke skill builder |
| User approves proposed skill | Invoke skill builder |
| Weekly review finds unaddressed pain points | Suggest skill building |
| High-priority pain point created | Notify user, suggest immediate build |

## Error Handling

### If /deep-investigate Fails
1. Fall back to basic investigation using Read/Grep
2. Check memory system for similar patterns
3. Proceed with limited information, note gaps

### If Skill Write Fails
1. Save content to temp file
2. Report failure with content
3. Suggest manual creation

### If YAML Frontmatter Invalid
1. Validate before writing
2. Use template defaults if needed
3. Log validation warnings

### If Pain Point Not Found
1. Search for similar entries
2. Offer to create new pain point
3. Proceed with available context

### If Skill Creation Fails
1. Log error to skill-metrics.json
2. Preserve investigation findings
3. Create partial skill with TODO markers
4. Notify user of incomplete creation

### If Documentation Update Fails
1. Complete skill creation first
2. Retry documentation updates
3. Log any remaining gaps
4. Manual intervention notice

## Best Practices

### 1. Thorough Investigation
Don't skip /deep-investigate — understanding the problem fully leads to better skills.

### 2. Specific Triggers
Vague triggers lead to skills that don't activate when needed. Be precise.

### 3. Test Mentally
Before creating, mentally walk through: "If this error occurs, will this skill catch it?"

### 4. Plan for Failure
Every skill will need improvement. Design for the skill-improver to understand it.

### 5. Complete the Loop
Always update all documentation. Incomplete updates break the self-improvement system.

## Skill Metadata

**Version:** 1.1.0
**Created:** 2025-12-31
**Last Updated:** 2026-05-08 (consolidation merge — absorbed playmakers fork)
**Category:** Meta-Skills & Self-Improvement
**Role:** Capstone of self-improvement system
**Invokes:** /deep-investigate
**Integration:** ai-error-learner, skill-improver, pain-point-manager, Memory System
**Maintenance:** Weekly review for unaddressed pain points; on-demand triggered by pain point escalation
