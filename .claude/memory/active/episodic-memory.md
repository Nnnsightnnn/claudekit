# Episodic Memory

*Session summaries and discoveries - provides context for what has been worked on and learned*

---

## Session: 2026-01-16

### Context
Initial setup of ClaudeKit self-improvement loop and complete template implementation.

### Key Discoveries
- Self-improvement architecture requires four coordinated components: error detection, pain point cataloging, skill creation, and skill monitoring
- Hooks must fail open (never block on errors) to maintain system reliability
- Error fingerprinting needs consistency: same error should always produce same fingerprint

### Patterns Used
- Skill template structure from transfer guide
- Hook script patterns with JSON output
- Soft limits philosophy for bloat management

### New Patterns Created
- AI error fingerprint format: `[TOOL]-[TYPE]-[CONTEXT]`
- Escalation thresholds: 2 for catalog, 3 for escalate
- Skill metrics tracking: invocations, successes, failures, success_rate

### Skills Created
- bloat-manager: System health and artifact growth management
- ai-error-learner: Recurring error cataloging
- skill-builder: Pain point to skill transformation
- skill-improver: Skill effectiveness monitoring and improvement

### Hooks Created
- skill_suggester.py: UserPromptSubmit - suggests skills based on prompt keywords
- security_gate.py: PreToolUse - blocks edits to sensitive files
- error_detector.py: PostToolUse - tracks error fingerprints
- skill_monitor.py: PostToolUse - tracks skill effectiveness

### Blockers Encountered
- None

---

## Template: Session Entry

```markdown
## Session: YYYY-MM-DD

### Context
[What was being worked on]

### Key Discoveries
- [Discovery 1]
- [Discovery 2]

### Patterns Used
- [Pattern name]: [How it was applied]

### New Patterns Created
- [Pattern name]: [Brief description]

### Skills Created
- [skill-name]: [Purpose]

### Blockers Encountered
- [Blocker and resolution]
```

---

*Last updated: 2026-01-16 | Retention: 30 days active, then archived*
