---
name: Investigation & Analysis
description: Analyze feature requests, refactor plans, or technical decisions to determine investment value and provide recommendations. Use when user mentions investigating, analyzing, evaluating feasibility, assessing ROI, or asks "should we build this" or "is this worth doing".
allowed-tools: Read, Grep, Glob
---

# Investigation & Analysis Skill

## Purpose
Analyze feature requests or refactor plans to determine investment value and provide actionable recommendations.

## Auto-Activation Triggers
This skill activates when the user:
- Mentions investigating a feature or idea
- Asks "should we build this?"
- Requests feasibility analysis
- Wants to evaluate ROI or cost/benefit
- Asks "is this worth doing?"
- Mentions analyzing a refactor plan
- Requests investment assessment

## Analysis Process

### 1. Context Gathering
**Automatically check:**
- Review relevant existing code/architecture
- Search memory patterns (`.claude/memory/`) for similar work
- Identify affected components and dependencies
- Check local task files (`.claude/tasks/`, `.claude/sprints/active/`) for related efforts
- Review procedural memory for proven patterns

**Tools to use:**
- `Grep` to search codebase for related functionality
- `Glob` to find relevant files (including `.claude/tasks/*.md` and `.claude/sprints/active/*.md`)
- `Read` to examine current implementation

### 2. Investment Assessment

Evaluate the request across three dimensions:

#### Technical Factors
- **Implementation Complexity** (1-10 scale)
  - Code changes required
  - System modifications needed
  - Integration points affected
- **Risk Assessment**
  - Breaking changes potential
  - Dependency impacts
  - Backward compatibility
- **Technical Debt Impact** (reduces/increases/neutral)
  - Code maintainability
  - Architecture alignment
  - Testing requirements
- **Performance Implications**
  - Resource usage
  - Scalability concerns

#### Business Factors
- **User Value Delivered**
  - Direct user benefit
  - Pain point addressed
  - Feature completeness
- **Alignment with Project Goals**
  - Strategic fit
  - Priority level
- **Time to Implement**
  - Hours/days/weeks estimate
  - Resource requirements
  - Opportunity cost
- **Return on Investment**
  - Value delivered vs. effort
  - Long-term benefits

#### Strategic Factors
- **Architecture Impact**
  - Long-term maintainability
  - System flexibility
  - Design pattern alignment
- **Reusability Potential**
  - Cross-feature applicability
  - Pattern establishment
- **Learning Value**
  - Skill development
  - Knowledge building
- **Future Flexibility**
  - Extensibility
  - Adaptability

### 3. Recommendation Framework

**Question 1: Is it worth the investment?**

Provide clear recommendation:
- **YES** - High value, reasonable cost, low risk
- **NO** - Low value, high cost, or high risk
- **CONDITIONAL** - Worth it if specific conditions met

Include:
- Executive summary (2-3 sentences)
- ROI analysis (value vs. cost)
- Critical success factors
- Risk mitigation strategies

**Question 2: What should we do with the request?**

Choose one:
- **KEEP AS-IS** - Plan is solid and well-conceived
- **MODIFY** - Suggest specific improvements with rationale
- **PIVOT** - Recommend alternative approach achieving similar goals
- **DEFER** - Not now, revisit when [specific conditions]
- **REJECT** - Clear reasons why this shouldn't be done

### 4. Response Format

```markdown
## Investigation: [Feature/Refactor Name]

### Investment Analysis

**Worth the Investment:** [YES/NO/CONDITIONAL]

[Executive summary explaining the recommendation in 2-3 sentences]

**Key Metrics:**
- Complexity: [X/10]
- Implementation Time: [estimate]
- Risk Level: [Low/Medium/High]
- Value Delivered: [Low/Medium/High]
- ROI: [High/Medium/Low]

### Recommendation: [KEEP/MODIFY/PIVOT/DEFER/REJECT]

[Detailed explanation of the recommendation with supporting evidence]

#### Technical Analysis
[Key technical findings from codebase investigation]

#### Business Justification
[Value proposition and alignment with goals]

#### Proposed Modifications (if MODIFY)
1. [Specific change with rationale]
2. [Specific change with rationale]

#### Alternative Approach (if PIVOT)
[Description of better approach that achieves similar goals]

#### Conditions for Approval (if CONDITIONAL/DEFER)
- [Required condition]
- [Required condition]

### Implementation Considerations

**Prerequisites:**
- [Required before starting]

**Success Criteria:**
- [Measurable outcome]
- [Measurable outcome]

**Potential Blockers:**
- [Risk] → Mitigation: [strategy]

**Dependencies:**
- [System/component/task dependency]

### Additional Insights
[Valuable observations or opportunities discovered during investigation]

### Evidence & References
- Code files examined: [file paths]
- Similar patterns in memory: [references]
- Related local task files: [`.claude/tasks/<slug>.md`, ...]
- Relevant specs: [spec IDs]
```

## Best Practices

### 1. Be Evidence-Based
- Reference actual code files examined
- Cite similar successful/failed attempts from memory
- Link to relevant local task files (`.claude/tasks/<slug>.md`)
- Include metrics where available

### 2. Be Pragmatic
- Focus on practical impact over theoretical benefits
- Consider current capacity and priorities
- Account for technical debt and maintenance burden
- Balance ideal solution vs. practical constraints

### 3. Provide Actionable Guidance
- Specific next steps if proceeding
- Clear reasons if not proceeding
- Concrete modifications if needed
- Measurable success criteria

### 4. Check Memory First
Always consult:
- `.claude/memory/active/quick-reference.md` - Top patterns
- `.claude/memory/structured/patterns/` - Domain patterns
- `.claude/memory/active/procedural-memory.md` - Proven procedures
- `.claude/memory/active/episodic-memory.md` - Similar past work

### 5. Leverage Existing Work
- Search for similar features already implemented
- Identify reusable patterns and components
- Check if request duplicates existing functionality
- Find opportunities to extend vs. rebuild

## Integration

**After Investigation:**
- If approved → Suggest `/orchestrate-tasks` for implementation
- If complex → Suggest `/plan-as-group` for collaborative planning
- If unclear → Suggest additional research or prototyping

**Update Context:**
- Document investigation results in the relevant local task file's `## Notes` section
- Add insights to procedural memory if pattern is reusable
- Update working knowledge if architecture implications discovered

## Examples

### Example 1: Feature Request
**User:** "Should we add real-time collaboration to the editor?"

**Skill:**
1. Searches codebase for existing editor architecture
2. Checks memory for similar feature implementations
3. Evaluates WebSocket/polling options
4. Assesses complexity vs. user value
5. Provides recommendation with implementation path

### Example 2: Refactor Plan
**User:** "I'm thinking about refactoring the data pipeline to use async/await"

**Skill:**
1. Examines current data pipeline implementation
2. Identifies sync vs. async bottlenecks
3. Assesses migration complexity and risk
4. Evaluates performance benefits
5. Recommends phased approach or alternative

### Example 3: Technical Decision
**User:** "Is it worth migrating from an ORM to raw SQL for performance?"

**Skill:**
1. Analyzes current database query patterns
2. Identifies performance bottlenecks
3. Compares maintainability trade-offs
4. Evaluates migration effort
5. Provides data-driven recommendation

## Skill Metadata

**Version:** 1.1.0
**Last Updated:** 2026-05-08 (consolidation merge — absorbed playmakers fork)
**Aliases:** investigation, analysis, feasibility, ROI assessment
**Category:** Planning & Decision Support
