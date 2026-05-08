---
name: Pain Point Manager
description: Automatically capture, update, and manage development pain points. Use when user mentions friction, blockers, workarounds, or wants to track development obstacles. Auto-invokes during weekly reviews.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Pain Point Manager Skill

## Purpose
Automatically manage the pain points tracking system by capturing new pain points, updating existing ones, archiving resolved items, and extracting patterns for focus area identification.

## Auto-Activation Triggers
This skill activates when the user:
- Mentions "pain point", "friction", "blocker", "workaround"
- Says "that was frustrating" or similar sentiment
- Describes manual workarounds or repetitive tasks
- Mentions "we should fix this" or "this is annoying"
- Asks to add/update pain points
- Requests weekly pain point review
- Wants to archive resolved pain points
- Asks for pain point patterns or analysis

## Core Operations

### 1. Capture New Pain Point
**Trigger phrases:**
- "This is a pain point"
- "Add this to pain points"
- "We need to track this friction"
- "This keeps causing issues"

**Workflow:**
1. Read `.claude/pain-points/active-pain-points.md`
2. Determine next available PAIN-ID (increment last used)
3. Gather context automatically:
   - File paths if mentioned
   - Related local task file slugs (`.claude/tasks/<slug>.md`)
   - Frequency indicators from conversation
   - Impact scope from description
4. Classify priority based on:
   - **Critical**: "blocking", "can't deploy", "broken"
   - **High**: "daily", "multiple times", "significant delay"
   - **Medium**: "weekly", "annoying", "workaround exists"
   - **Low**: "occasionally", "nice to have"
5. Add new entry with complete metadata
6. Confirm capture with ID reference

**Template Application:**
```markdown
### [PAIN-XXXX] Brief action-oriented description
- **Impact**: Specific scope (derived from context)
- **Frequency**: Daily/Weekly/Occasional (from conversation)
- **First Noted**: YYYY-MM-DD (today's date)
- **Context**: File paths, task IDs, scenarios mentioned
- **Workaround**: Current approach (if mentioned)
- **Potential Solution**: Ideas if discussed
- **Task file**: Search `.claude/tasks/` for related slugs, link if found
```

### 2. Update Existing Pain Point
**Trigger phrases:**
- "Update pain point [ID]"
- "This happened again" (reference previous pain point)
- "Mark [PAIN-ID] as resolved"
- "Increase priority on [ID]"

**Workflow:**
1. Read active pain points file
2. Locate pain point by ID or description
3. Determine update type:
   - **Frequency increase**: User mentions recurrence
   - **Priority change**: New evidence of impact
   - **Status change**: "resolved", "fixed", "working now"
   - **Context addition**: New scenarios or files
   - **Solution progress**: "investigating", "found fix"
4. Edit entry with updated information
5. Add timestamp note for significant updates
6. Confirm update

**Update Types:**
- **Frequency**: Increment count, adjust priority if threshold crossed
- **Priority Escalation**: Move to higher tier, document reason
- **Resolution**: Move to "Recently Resolved" with solution details
- **Context Enrichment**: Add new file paths, task IDs, or scenarios
- **Solution Discovery**: Update potential solution field

### 3. Weekly Review Workflow
**Trigger phrases:**
- "Pain point review"
- "Review pain points"
- "What are our top pain points?"
- "Weekly pain point check"

**Workflow:**
1. **Read Current State**
   - Load active pain points
   - Read episodic memory for past week
   - Check recent local task files (`.claude/tasks/*.md`, `.claude/sprints/active/*.md`) for friction mentions

2. **Discover New Pain Points**
   - Grep episodic memory for keywords:
     - "workaround", "manually", "blocked", "had to"
     - "slow", "failing", "issue", "problem"
   - Grep task file `## Notes` sections for similar patterns
   - Present findings to user for confirmation

3. **Update Existing Items**
   - Identify pain points with activity this week
   - Suggest frequency increases if mentioned multiple times
   - Flag items for priority review if impact increased

4. **Generate Focus Areas**
   - Analyze Critical + High priority items
   - Calculate impact × frequency scores
   - Recommend top 2-3 focus areas
   - Check for quick wins (low effort, high impact)

5. **Suggest local task file creation**
   - Identify pain points without linked task files
   - Recommend `.claude/tasks/<slug>.md` creation for high-priority items
   - Provide draft outcome and acceptance check

6. **Update Review Metadata**
   - Set "Next Review" date (+7 days)
   - Update "Last Updated" timestamp
   - Add review summary comment

**Review Output Format:**
```markdown
## Weekly Pain Point Review - YYYY-MM-DD

### Current State
- **Total Pain Points**: X (Critical: X, High: X, Medium: X, Low: X)
- **New This Week**: X
- **Resolved This Week**: X
- **Escalated**: X

### Discoveries from Episodic Memory
1. [PAIN-XXXX] Description - Found in: [context]
2. [PAIN-YYYY] Description - Found in: [context]

### Updated Items
- [PAIN-XXXX]: Frequency increased (2→4/week)
- [PAIN-YYYY]: Priority escalated (Medium→High)

### Recommended Focus Areas

**Quick Wins** (High Impact, Low Effort):
1. [PAIN-XXXX]: Description
   - Estimated fix: 2 hours
   - Impact: Saves 30min/day

**Strategic Investments** (High Impact, High Effort):
1. [PAIN-XXXX]: Description
   - Estimated fix: 2 days
   - Impact: Eliminates major friction

### Suggested task files
- Create `.claude/tasks/pain-XXXX.md` for [PAIN-XXXX]: "Fix: [description]"
- Create `.claude/tasks/pain-YYYY.md` for [PAIN-YYYY]: "Improve: [description]"

### Next Steps
1. Approve new pain points
2. Create local task files for focus areas
3. Schedule work for quick wins
4. Next review: YYYY-MM-DD
```

### 4. Archive Resolved Items
**Trigger phrases:**
- "Archive resolved pain points"
- "Monthly pain point archival"
- "Move resolved items to archive"

**Workflow:**
1. Read active pain points "Recently Resolved" section
2. Check dates - items >30 days old qualify for archive
3. Read or create `archives/YYYY-MM-resolved.md`
4. Move qualified items with resolution details
5. Generate archival summary:
   - Count of items resolved
   - Common themes
   - Biggest wins
6. Clean up "Recently Resolved" section
7. Update active file

**Archive Entry Format:**
```markdown
### [PAIN-XXXX] Description
- **Original Priority**: High
- **First Noted**: YYYY-MM-DD
- **Resolved**: YYYY-MM-DD
- **Duration**: X days
- **Solution**: What fixed it
- **Impact**: Time saved or quality improved
- **Related**: Local task file slug (`.claude/tasks/<slug>.md`) or commit ID
```

### 5. Pattern Analysis (Quarterly)
**Trigger phrases:**
- "Analyze pain point patterns"
- "Quarterly pain point review"
- "What are the common themes?"

**Workflow:**
1. Read all active pain points
2. Read archives for past quarter
3. Analyze patterns:
   - **Category clustering**: Group by type (deployment, data, performance, etc.)
   - **Root cause analysis**: Identify systemic issues
   - **Resolution time**: Average time to fix
   - **Recurrence**: Track if similar pain points repeat
4. Generate pattern report
5. Update memory system:
   - Add patterns to `.claude/memory/structured/patterns/`
   - Update procedural memory with lessons
   - Update quick reference with top current issues
6. Create quarterly archive file

**Pattern Report Format:**
```markdown
# Pain Point Pattern Analysis - YYYY Q4

## Executive Summary
- **Total Pain Points**: X (Active: X, Resolved: X)
- **Most Common Category**: [category] (X items)
- **Average Resolution Time**: X days
- **Biggest Impact Area**: [area]

## Category Breakdown
### Deployment (X items)
- [PAIN-XXXX]: Description
- Common Theme: [theme]
- Recommendation: [systematic fix]

### Data Pipeline (X items)
[Similar structure]

## Root Cause Analysis
### Systemic Issue 1: [Description]
- **Manifestations**: [PAIN-XXXX], [PAIN-YYYY], [PAIN-ZZZZ]
- **Root Cause**: [underlying issue]
- **Architectural Fix**: [systematic solution]
- **Local epic doc**: [Create/link `.claude/sprints/active/<slug>-epic.md` for major refactor]

## Resolution Metrics
- **Quick Wins** (<1 day): X items
- **Medium Effort** (1-3 days): X items
- **Major Projects** (>3 days): X items
- **Deferred/Accepted**: X items

## Recommendations for Next Quarter
1. [Priority 1 recommendation]
2. [Priority 2 recommendation]
3. [Priority 3 recommendation]

## Memory System Updates
- Added pattern to: `.claude/memory/structured/patterns/[domain].md`
- Updated: `.claude/memory/active/procedural-memory.md`
- Updated: `.claude/memory/active/quick-reference.md`
```

## Advanced Features

### Smart Context Detection
When capturing pain points, automatically:
- **Extract file paths** from conversation using regex
- **Link local task files** by globbing `.claude/tasks/*.md` and matching outcome lines
- **Identify team impact** from scope keywords (all, team, deployment, etc.)
- **Detect urgency** from language (blocking, critical, asap)
- **Find similar pain points** to check for duplicates

### Priority Scoring Algorithm
Calculate priority score = (Impact × Frequency) + Urgency Modifier

**Impact Score (1-10):**
- 10: All deployments/team blocked
- 7-9: Major feature or multiple people affected
- 4-6: Single feature or occasional team impact
- 1-3: Individual developer, specific scenario

**Frequency Score (1-10):**
- 10: Multiple times per day
- 7-9: Daily
- 4-6: Weekly
- 1-3: Monthly or less

**Urgency Modifiers:**
- +5: Blocks production deployments
- +3: Causes data loss/corruption risk
- +2: Customer-facing impact
- +1: Technical debt accumulation

**Auto-Prioritization:**
- Score 15+: Critical
- Score 10-14: High
- Score 5-9: Medium
- Score <5: Low

### Duplicate Detection
Before creating new pain point:
1. Search active pain points for similar descriptions
2. Check keywords match existing entries
3. If 70%+ similarity:
   - Ask user if duplicate
   - Offer to update existing instead
   - Show similar entries for review

### Local task file integration
**Auto-link existing tasks:**
- Glob `.claude/tasks/*.md` and `.claude/sprints/active/*.md` for keywords from pain point
- Match `**Touches:**` file paths
- Link task slugs that address the pain point

**Auto-create task suggestions:**
- For Critical/High priority items without task files
- Draft title (H1 outcome): "Fix: [pain point description]"
- Draft body: "Addresses [PAIN-XXXX]\n\nSee .claude/pain-points/active-pain-points.md for context"
- Suggest `priority:` and `size:` frontmatter based on pain point metadata

**Track resolution:**
- When task frontmatter flips to `status: done`, suggest marking pain point resolved
- Add task slug to pain point resolution notes

### Memory Integration
**Read from memory:**
- Check `.claude/memory/active/episodic-memory.md` for friction mentions
- Search `.claude/memory/structured/patterns/` for known pain patterns
- Review `.claude/memory/active/quick-reference.md` for top issues

**Write to memory:**
- Add significant patterns to procedural memory
- Update quick reference with top 5 pain points
- Document resolutions in episodic memory

## Best Practices

### 1. Be Proactive
**Auto-capture during conversations:**
- Listen for friction language
- Offer to capture without being asked
- "I noticed you mentioned a workaround - should I add this as a pain point?"

### 2. Be Specific
**Require concrete details:**
- Don't accept "deployment is slow"
- Require measurable details (e.g., "deployment takes 8 minutes, 5 min is in the build cache step")
- Push for measurable impact

### 3. Keep It Current
**Regular hygiene:**
- Weekly reviews mandatory
- Monthly archival automatic
- Quarterly pattern analysis
- Remove outdated items

### 4. Link Evidence
**Always connect to reality:**
- File paths where problem occurs
- Local task files that encountered it
- Commits that worked around it
- Episodic memory references

### 5. Focus on Actionability
**Every pain point needs:**
- Clear description
- Measurable impact
- Potential solution (even if rough)
- Path to resolution (local task file slug)

## Integration with Other Workflows

### With local task files
- Reference pain point IDs in task body (`Addresses [PAIN-XXXX]`)
- Add pain point context to the `## Notes` section of each task
- Link task slug back from the pain point's "Task file" field (bidirectional)
- Use pain points to inform sprint planning

### With Git Commits
- Reference in commit messages: "Fix: [description] (PAIN-XXXX)"
- Track which commits resolve pain points
- Build resolution timeline

### With Memory System
- Episodic memory feeds pain point discovery
- Pain point patterns update procedural memory
- Top pain points inform quick reference
- Quarterly analysis feeds domain patterns

### With Weekly Reviews
- Pain points inform retrospectives
- Quick wins provide sprint tasks
- Strategic items become epics
- Trends inform architectural decisions

## Output Examples

### Example 1: Capture During Conversation
**User:** "I had to manually rerun the upload again because the object storage push step failed."

**Skill response:**
```markdown
I noticed a pain point. Let me capture this:

**Added Pain Point**
[PAIN-XXXX] Object storage push step fails requiring manual rerun
- **Impact**: Pipeline operations, manual intervention required
- **Frequency**: Weekly (based on "again")
- **First Noted**: YYYY-MM-DD
- **Context**: Upload step in deployment/sync pipeline
- **Workaround**: Manual rerun via the local CLI
- **Potential Solution**: Add retry logic and clearer error reporting to the upload step
- **Task file**: Searching for related slugs...

Found related task file: `.claude/tasks/<slug>.md` — linked

Updated: `.claude/pain-points/active-pain-points.md`
Priority: **High** (weekly frequency + manual intervention)
```

### Example 2: Weekly Review
**User:** "Let's do the weekly pain point review"

**Skill response:**
```markdown
## Weekly Pain Point Review - YYYY-MM-DD

### Current State
- **Total Pain Points**: 12 (Critical: 2, High: 4, Medium: 5, Low: 1)
- **New This Week**: 3
- **Resolved This Week**: 1
- **Escalated**: 2

### Discoveries from Episodic Memory
Found 3 potential new pain points:

1. **Container build cache misses** - Mentioned 3 times this week in deployment contexts
   - Impact: Adds several minutes to every deployment
   - Should we track this? [Yes/No]

2. **Database connection timeout during deploy** - Caused a deployment rollback this week
   - Impact: Deployment failures
   - Should we track this? [Yes/No]

3. **Missing test fixture for edge case** - Required manual fixture creation
   - Impact: Testing delays
   - Should we track this? [Yes/No]

### Updated Items
- [PAIN-XXXX]: Frequency increased Daily (was Weekly) - deploying 2x/day now
- [PAIN-YYYY]: Escalated Medium→High - blocked sprint work mid-week

### Recommended Focus Areas

**Quick Wins** (High Impact, Low Effort):
1. [PAIN-XXXX]: Add retry logic to the upload step
   - Estimated fix: 2 hours
   - Impact: Eliminates weekly manual intervention (saves ~30min/week)
   - Files: `<scripts/path/upload-script>`

**Strategic Investments** (High Impact, High Effort):
2. [PAIN-YYYY]: Optimize container build layer caching
   - Estimated fix: 1-2 days
   - Impact: Saves several minutes per deployment × ~10 deploys/week
   - Requires: Build configuration restructure

### Suggested task files
Would you like me to write `.claude/tasks/<slug>.md` files for these focus areas?
1. `pain-xxxx-upload-retry.md` — "Fix: Add retry logic to upload step (PAIN-XXXX)"
2. `pain-yyyy-build-cache.md` — "Improve: Optimize container build cache (PAIN-YYYY)"

### Next Steps
1. Confirm which discoveries to track
2. Approve local task file creation
3. Next review: YYYY-MM-DD
```

### Example 3: Mark Resolved
**User:** "Mark PAIN-XXXX as resolved - the upload retry logic is working now"

**Skill response:**
```markdown
**Pain Point Resolved**

[PAIN-XXXX] Object storage push step fails requiring manual rerun
- **Resolved**: YYYY-MM-DD
- **Duration**: 12 days (First noted: YYYY-MM-DD)
- **Solution**: Added exponential backoff retry logic with clearer error messages
- **Related**: Commit <sha>, task file `.claude/tasks/<slug>.md`

Moved to "Recently Resolved" section.
Will auto-archive to `archives/YYYY-MM-resolved.md` after 30 days.

**Impact**: No more manual reruns needed - saves ~30min/week
```

## Error Handling

### If Pain Points File Missing
1. Check if file exists at expected location
2. If not found, create from template
3. Initialize with ID counter at PAIN-0001
4. Notify user of initialization

### If ID Collision
1. Scan all IDs (active + archives)
2. Find true last used ID
3. Increment from there
4. Log warning about potential data issue

### If Archive Directory Missing
1. Create `.claude/pain-points/archives/`
2. Add .gitkeep
3. Proceed with operation

### If Memory File Unavailable
1. Skip memory-based discovery
2. Notify user of limitation
3. Offer manual entry mode
4. Continue with other operations

## Skill Metadata

**Version:** 1.1.0
**Last Updated:** 2026-05-08 (consolidation merge — absorbed playmakers fork)
**Integrations:** Local task files (`.claude/tasks/`, `.claude/sprints/`), Memory System, Git
**Category:** Development Experience & Quality
**Maintenance:** Weekly active use, Monthly archival, Quarterly analysis
