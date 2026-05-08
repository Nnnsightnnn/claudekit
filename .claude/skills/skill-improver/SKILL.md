---
name: Skill Improver
description: Automatically improve skills when they fail to handle their intended scenarios. Triggers when a skill is unsuccessful, analyzing the failure and updating the skill definition.
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Skill Improver Skill

## Purpose

Monitor skill effectiveness and improve skills that fail. This skill is the third stage of the self-improvement loop, ensuring skills remain effective over time and adapt to changing requirements. The brain layer that watches all other skills (the muscle layer), detects failure patterns, and updates skill definitions to close the gap.

## Auto-Activation Triggers

This skill activates when:

**Metric-based:**
- Skill monitor reports a failure
- Skill success rate drops below 80%
- Same failure pattern occurs twice
- Weekly skill health review

**Scenario-based:**
- A skill fails to handle its intended scenario
- Claude uses a skill but still encounters the error it was meant to prevent
- A cataloged AI pain point recurs despite having a skill
- User says "that skill didn't work", "skill not working", or "skill failed"
- Skill produces incorrect or incomplete results
- Same error pattern appears after skill was supposed to address it

## CRITICAL: Improvement Protocol

**Fix root causes, not symptoms. Every improvement must be verified.**

### Continuous Skill Monitoring

After EVERY skill invocation, evaluate using OBSERVE → EVALUATE → IMPROVE:

```
┌─────────────────────────────────────────────────────────┐
│  SKILL INVOKED                                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │ 1. OBSERVE: Did the skill achieve its goal?     │   │
│  │    - Check if intended outcome occurred         │   │
│  │    - Check if error still present               │   │
│  │    - Check if manual intervention needed        │   │
│  └─────────────────────────────────────────────────┘   │
│                         ↓                               │
│  ┌─────────────────────────────────────────────────┐   │
│  │ 2. EVALUATE: Success or failure?                │   │
│  │    - Success: Log to metrics, continue          │   │
│  │    - Partial: Analyze gap, consider improvement │   │
│  │    - Failure: TRIGGER SKILL IMPROVER NOW        │   │
│  └─────────────────────────────────────────────────┘   │
│                         ↓                               │
│  ┌─────────────────────────────────────────────────┐   │
│  │ 3. IMPROVE: If failure detected                 │   │
│  │    - Analyze root cause immediately             │   │
│  │    - Generate targeted improvement              │   │
│  │    - Apply fix to skill definition              │   │
│  │    - Re-attempt if appropriate                  │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### Skill Failure Detection Signals

**Immediate Failure Indicators:**
- Same error occurs after skill was invoked
- User says "that didn't work", "still broken", "try again"
- Skill output contains error messages
- Manual workaround required after skill ran
- Skill aborted or timed out

**Partial Failure Indicators:**
- Goal achieved but with warnings
- Required multiple attempts
- User had to provide additional guidance
- Output was incomplete but usable

**Success Confirmation:**
- Intended outcome achieved
- No errors in subsequent operations
- User continues without mentioning issues
- Downstream operations succeed

### Brain / Muscle Architecture

This skill is the **brain layer** for skill management; all other skills are the **muscle layer**. Note: the "report outcomes back to brain" channel is a design intent, not wired plumbing — outcomes are observed during conversation, not by an automated reporting bus.

```
┌──────────────────────────────────────────────────────────┐
│  BRAIN LAYER (This Skill)                                │
│  • Analyzes all skill outcomes                           │
│  • Detects patterns in failures                          │
│  • Generates improvements                                │
│  • Updates skill definitions                             │
│  • Maintains success rate metrics                        │
│                          ↕                               │
│  MUSCLE LAYER (All Other Skills)                         │
│  • Execute their specific workflows                      │
│  • Outcomes observed during use                          │
│  • Receive updates from brain                            │
└──────────────────────────────────────────────────────────┘
```

### Proactive Skill Health Monitoring

Don't wait for failures — predict them:

1. **Success Rate Trending**: If skill drops below 90%, investigate immediately.
2. **Context Drift Detection**: If codebase changes, check if skills reference stale paths.
3. **Dependency Monitoring**: If a skill depends on another, verify chain integrity.
4. **Usage Pattern Analysis**: If skill stops being invoked, check if triggers are still valid.

### Improvement Decision Matrix

```
┌─────────────────┬────────────────────┬─────────────────────┐
│ Condition       │ Action             │ Priority            │
├─────────────────┼────────────────────┼─────────────────────┤
│ 1 failure       │ Log and analyze    │ Monitor             │
│ 2 same pattern  │ Apply improvement  │ High                │
│ 3+ failures     │ Escalate/redesign  │ Critical            │
│ <80% success    │ Health report      │ Medium              │
│ 0 invokes/7d    │ Check relevance    │ Low                 │
└─────────────────┴────────────────────┴─────────────────────┘
```

## Success / Failure Criteria

A skill invocation is **successful** if:
- The intended outcome is achieved
- No manual intervention needed
- User doesn't report the skill failed
- Error doesn't recur within the session

A skill invocation is a **failure** if:
- The error/scenario still occurs after skill runs
- Manual workaround is needed
- User explicitly indicates failure
- Skill produces incorrect output

## Failure Categories

| Type | Description | Fix Approach |
|------|-------------|--------------|
| **Coverage Gap** | Doesn't trigger for valid scenario | Add new trigger pattern |
| **Logic Error** | Wrong action taken | Fix workflow steps |
| **Missing Context** | Lacks needed information | Add context gathering step |
| **Tool Limitation** | Required tool unavailable or fails | Add fallback or alternate approach |
| **Edge Case** | Unusual input not handled | Add edge case section |
| **Outdated** | Stale file paths or references | Update paths and refs |
| **Integration** | Doesn't work with other skills | Fix integration points |

## The Self-Improvement Loop

```
   Error Occurs ──► AI Error Learner ──► Skill Created
        ▲                                      │
        │                                      ▼
        │                                Skill Used
        │                                      │
   Improved Skill ◄── Skill Improver ◄── Skill Fails?
                                                │
                                          Yes ──┴── No → Success
```

## Core Workflow

### Step 1: Load Skill Metrics

Review current skill health:

```bash
cat .claude/skills/skill-metrics.json | python3 -m json.tool
```

Identify skills needing attention:
- Success rate < 80%
- Recent failures
- Zero invocations in 7 days

**Manual triggers** (skip metrics, go directly to Step 2):
- User says "that skill didn't work"
- User says "improve the [skill_name] skill"
- User reports unexpected behavior

### Step 2: Analyze Failure Pattern

For failing skill, examine:

1. **Recent failure contexts**
   ```bash
   grep -A 5 "skill-name" .claude/skills/skill-metrics.json
   ```

2. **Skill definition**
   ```bash
   cat .claude/skills/[skill-name]/SKILL.md
   ```

3. **Related error history**
   ```bash
   grep "skill-name" .claude/pain-points/ai-error-history.json
   ```

### Step 3: Categorize Failure

Determine failure type using the categories above. Indicators:

**Coverage Gap:**
- "Skill didn't activate when expected"
- "Should have used [skill] but didn't"
- Trigger conditions not matching

**Logic Error:**
- "Skill ran but did wrong thing"
- Wrong output or action
- Steps executed in wrong order

**Missing Context:**
- "Didn't have enough information"
- Required data not gathered
- Assumptions failed

**Tool Limitation:**
- Required tool unavailable in environment
- Tool succeeded but returned unusable output
- Permissions or auth missing

**Edge Case:**
- "Works normally, but not for [specific case]"
- Unusual input not handled
- Special conditions not considered

**Outdated:**
- File paths don't exist
- Commands fail
- References broken

### Step 4: Design Improvement

Based on failure category:

**For Coverage Gap:**
```markdown
## Triggers Section Update

Add new trigger:
- [New specific trigger condition]
```

**For Logic Error:**
```markdown
## Workflow Section Update

### Step N (modified):
[Corrected instructions]

### Step N+1 (new):
[Additional step if needed]
```

**For Missing Context:**
```markdown
## Workflow Section Update

### Step 0 (new): Gather Context
1. Check [required information]
2. Read [needed file]
3. Verify [assumption]
```

**For Tool Limitation:**
```markdown
## Workflow Update

If [primary tool] is unavailable or fails:
- Fall back to [alternative tool/approach]
- Or escalate to user
```

**For Edge Case:**
```markdown
## Edge Cases Section Update

### [New Edge Case Name]
**Condition**: [When this occurs]
**Handling**: [What to do]
```

**For Outdated:**
```markdown
## Updates Required
- Line XX: Change `/old/path` to `/new/path`
- Line YY: Update command from `old-cmd` to `new-cmd`
```

### Step 5: Apply Improvement

Edit the skill file:

```bash
# Read current skill
cat .claude/skills/[skill-name]/SKILL.md

# Apply targeted edit
# (Use Edit tool for specific changes)
```

### Step 6: Update Metadata

Update skill metadata section:

```markdown
## Skill Metadata

**Version:** 1.0.1  (increment patch for fix)
**Last Improved:** YYYY-MM-DD
**Improvement:** [Brief description of change]
```

Update skill metrics — see "Skill Effectiveness Tracking" below for the full schema.

### Step 7: Verify Improvement

Confirm fix is valid:

1. **YAML frontmatter valid**
   ```bash
   python3 -c "import yaml; yaml.safe_load(open('.claude/skills/[skill-name]/SKILL.md').read().split('---')[1])"
   ```

2. **No syntax errors in workflow**
   - Commands are valid
   - File paths exist
   - References are correct

3. **Edge cases covered**
   - New case is documented
   - Handling is complete

### Step 8: Log Improvement

Record in episodic memory and in the improvement log (see "Improvement Log Format" below):

```markdown
### Skill Improvement
- Skill: [skill-name]
- Version: 1.0.0 → 1.0.1
- Failure Type: [category]
- Fix Applied: [brief description]
- Verified: Yes
```

## Skill Effectiveness Tracking

### Metrics Schema

For each skill, track in `.claude/skills/skill-metrics.json`:

```json
{
  "skills": {
    "ai-error-learner": {
      "invocations": 15,
      "successes": 12,
      "failures": 3,
      "success_rate": 0.80,
      "last_failure": "2025-12-31T14:00:00Z",
      "failure_patterns": [
        {
          "id": "F001",
          "date": "2025-12-31T14:00:00Z",
          "context": "Error fingerprinting failed for multi-line errors",
          "root_cause": "Regex didn't handle newlines",
          "improvement_applied": true,
          "improvement_id": "IMP-0001"
        }
      ],
      "improvements": [
        {
          "id": "IMP-0001",
          "date": "2025-12-31T14:30:00Z",
          "description": "Added multiline regex support",
          "success_rate_before": 0.80,
          "success_rate_after": 0.93
        }
      ]
    }
  }
}
```

## Improvement Log Format

Track all improvements in `.claude/skills/skill-improvement-log.md`:

```markdown
# Skill Improvement Log

## [IMP-XXXX] Improvement Title

- **Date**: YYYY-MM-DD
- **Skill**: [skill-name]
- **Failure ID**: F001
- **Failure Type**: Edge Case
- **Problem**: [What was failing]
- **Root Cause**: [Underlying cause]
- **Solution**: [What was changed]
- **Files Changed**: `.claude/skills/[skill-name]/SKILL.md`
- **Success Rate Impact**: 80% → 93%
- **Verified**: Yes — [how it was verified]
```

## Escalation Rules

### When to Escalate to User

1. **Fundamental Design Flaw**
   - Skill's core approach is wrong
   - Needs architectural redesign
   - >50% failure rate after improvements

2. **Conflicting Requirements**
   - Improvement would break other scenarios
   - Trade-offs require user decision

3. **External Dependency**
   - Needs new tools or permissions
   - Requires codebase changes
   - Needs user configuration

4. **Repeated Failures**
   - Same failure pattern 3+ times
   - Improvements haven't worked

### Escalation Format

```markdown
## Skill Improvement Escalation

**Skill**: [skill_name]
**Issue**: [description]
**Attempts**: [number of improvement attempts]
**Failure Rate**: [current rate]

**Why Escalating**:
[Reason this can't be auto-fixed]

**Options**:
1. [Option A] - [pros/cons]
2. [Option B] - [pros/cons]
3. [Option C] - [pros/cons]

**Recommendation**: [Which option and why]

**Action Needed**: [What user should decide/do]
```

## Skill Health Report

When generating health reports:

```markdown
## Skill Health Report - YYYY-MM-DD

### Summary
- Total Skills: N
- Healthy (>80%): N
- Needs Attention: N
- Critical: N

### Per-Skill Status

| Skill | Success Rate | Trend | Last Failure | Status |
|-------|--------------|-------|--------------|--------|
| ai-error-learner | 93% | ↑ | 7 days ago | Healthy |
| pain-point-manager | 91% | → | 3 days ago | Healthy |
| python-ml-runner | 72% | ↓ | Today | Needs Work |

### Skills Needing Attention

#### [skill-name] - 65% success rate
**Recent Failures**: 3
**Pattern**: Logic error in step 2
**Recommendation**: Review workflow logic

#### [skill-name] - 0 invocations
**Last Invoked**: 14 days ago
**Recommendation**: Verify triggers still relevant

### Recent Improvements
1. [IMP-0003] python-ml-runner - Added PYTHONPATH handling
2. [IMP-0002] ai-error-learner - Multi-line error support
3. [IMP-0001] pain-point-manager - Present tense triggers

### Recommended Actions
1. [Priority 1 action]
2. [Priority 2 action]
```

## Edge Cases

### Skill Is Fundamentally Broken
**Condition**: Success rate near 0%, multiple failure types
**Handling**: Flag for complete redesign, don't patch — use Escalation Format

### No Clear Failure Pattern
**Condition**: Failures are random, no common cause
**Handling**: Add more logging to skill, monitor for patterns

### Improvement Would Be Breaking Change
**Condition**: Fix would change skill behavior significantly
**Handling**: Increment minor version, document migration if needed

### Skill Has No Metrics
**Condition**: New skill, no data yet
**Handling**: Skip for now, ensure metrics are being collected

## Error Handling

### If Skill File Missing
1. Check if skill was archived
2. Report skill not found
3. Suggest recreating via skill-builder

### If Metrics Corrupted
1. Back up corrupted file
2. Rebuild from available data
3. Note data loss in report

### If Improvement Breaks Skill
1. Revert to previous version
2. Log failed improvement attempt
3. Escalate for manual review

## Integration Points

### With Skill Monitor Hook
- Receives failure notifications
- Updates metrics after improvements
- Tracks improvement effectiveness

### With Skill Builder
- May recommend rebuilding vs. improving
- Shares quality standards
- Uses same template structure

### With AI Error Learner

```
AI Error Learner creates skill → Skill used → Skill fails
                                                   ↓
                                         Skill Improver activates
                                                   ↓
                            Analyzes failure, improves skill definition
                                                   ↓
                            Updates AI Pain Point status if relevant
```

When improving a skill:
1. Check if skill was created from an AI Pain Point
2. If yes, update the AI Pain Point status
3. Track improvement in both systems

### With Memory System
- Logs improvements in episodic memory
- May update patterns in procedural memory
- References quick-reference for context

## Best Practices

1. **Minimal Changes** — make the smallest change that fixes the failure. Don't over-engineer.
2. **Preserve Behavior** — improvements should fix failures without breaking existing functionality.
3. **Test When Possible** — if the failing scenario can be reproduced, verify the fix works.
4. **Document Everything** — every improvement should have a clear record of what, why, and how.
5. **Watch for Patterns** — multiple failures in one area might indicate a deeper issue.

## Output Examples

### Example 1: Coverage Gap Fix (Auto-Detected)

**Trigger**: Skill "permission-fixer" didn't activate for .sh files

**Response**:
```markdown
## Skill Improvement: permission-fixer

### Failure Analysis
**Type**: Coverage Gap
**Pattern**: Skill only triggers for `/scripts/` but user created .sh in `/tools/`

### Improvement Applied

**Triggers Section Update:**
- When creating files in `/scripts/` directory
- When creating any `.sh` file (added)
- When bash command fails with "Permission denied"

### Verification
- YAML valid: Yes
- Triggers updated: Yes
- Version: 1.0.0 → 1.0.1

### Metrics Updated
- Logged improvement in skill-metrics.json
- Reset failure counter for this pattern
```

### Example 2: Tool / Logic Failure (Auto-Detected)

**Scenario**: AI Error Learner skill failed to catalog a Python import error

**Response**:
```markdown
## Skill Failure Detected

**Skill**: ai-error-learner
**Scenario**: Python import error not cataloged
**Root Cause**: Fingerprint regex didn't match `from X import Y` pattern

### Improvement Applied

Added new error pattern to fingerprinting logic:

**Before:**
```regex
ModuleNotFoundError: No module named '([^']+)'
```

**After:**
```regex
(ModuleNotFoundError|ImportError): (No module named|cannot import name) '?([^']+)'?
```

Updated `.claude/skills/ai-error-learner/SKILL.md` — see Error Fingerprinting section.

**Metrics Updated**: Success rate tracking reset for import error handling.
```

### Example 3: User-Triggered Improvement

**User says:** "The pain-point-manager skill keeps missing when I say 'this is frustrating'"

**Response**:
```markdown
## Analyzing Skill Failure

**Skill**: pain-point-manager
**Reported Issue**: Not triggering on "this is frustrating"

**Analysis:**
Checking trigger conditions in `.claude/skills/pain-point-manager/SKILL.md`...

Current triggers include:
- "that was frustrating" ✓
- "this is a pain point"
- "friction", "blocker", "workaround"

**Gap Found**: Present-tense "this is frustrating" not covered.

### Improvement Applied

Added trigger phrase to Auto-Activation Triggers:

- Says "this is frustrating" or similar present-tense frustration

**File Updated**: `.claude/skills/pain-point-manager/SKILL.md`

The skill should now trigger on "this is frustrating". Want me to test it?
```

### Example 4: Escalation

**Scenario**: Skill has failed 4 times on similar scenarios

**Response**:
```markdown
## Skill Improvement Escalation

**Skill**: python-ml-runner
**Issue**: Keeps failing on scripts with relative imports
**Attempts**: 3 improvements applied, still failing
**Failure Rate**: 45% (was 20% before issue started)

**Why Escalating**:
The skill's current approach (activate venv, run script) doesn't handle Python's relative import resolution. This is a fundamental limitation.

**Options**:
1. **Change execution method** - Run scripts as modules (`python -m`) instead of files
   - Pro: Fixes import issues
   - Con: Requires knowing module path

2. **Add PYTHONPATH setup** - Set PYTHONPATH before execution
   - Pro: Works with current approach
   - Con: Need to determine correct path per project

3. **Create wrapper script** - Generate temporary wrapper that sets up paths
   - Pro: Most reliable
   - Con: More complex, creates temp files

**Recommendation**: Option 2 — Use `PYTHONPATH=$(pwd)` before script execution

**Action Needed**: Confirm approach, or suggest alternative
```

### Example 5: Health Report

**Trigger**: Weekly skill health review

**Response**:
```markdown
## Skill Health Report - 2026-01-16

### Summary
- Total Skills: 8
- Healthy: 6 (75%)
- Needs Attention: 2 (25%)
- Critical: 0

### Detailed Status

| Skill | Invocations | Success Rate | Trend | Status |
|-------|-------------|--------------|-------|--------|
| pain-point-manager | 24 | 95.8% | → | Healthy |
| bloat-manager | 4 | 100% | ↑ | Healthy |
| permission-fixer | 12 | 75% | ↓ | Needs Attention |
| api-validator | 0 | N/A | — | Dormant |

### Recent Improvements
1. [IMP-0003] permission-fixer - Path validation step

### Recommended Actions

1. **permission-fixer** (Priority: High)
   - 3 recent failures with pattern "directory not found"
   - Investigate: May need path validation step

2. **api-validator** (Priority: Low)
   - No invocations in 14 days
   - Review: Are triggers still relevant?
```

## Skill Metadata

**Version:** 1.1.0
**Created:** 2026-01-16
**Last Updated:** 2026-05-08 (consolidation merge — absorbed playmakers fork)
**Category:** Self-Improvement & Meta-Skills
**Depends On:** ai-error-learner (for the feedback loop)
**Integration:** All skills (monitors and improves them)
**Maintenance:** Continuous (triggered by skill monitor) + Weekly health review
