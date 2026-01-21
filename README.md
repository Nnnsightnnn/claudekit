# ClaudeKit

[![Version](https://img.shields.io/badge/version-1.2.0-blue.svg)](https://github.com/Nnnsightnnn/claudekit/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Compatible-blueviolet.svg)](https://claude.ai/code)

**The ultimate context system for Claude Code** — supercharge your AI coding assistant with persistent memory, automated workflows, and self-improving skills.

A production-ready framework for Claude Code projects. Provides memory management, pain point tracking, hooks automation, and reusable slash commands.

## Why ClaudeKit?

Claude Code is powerful, but starts fresh every session. ClaudeKit solves this with:

| Challenge | ClaudeKit Solution |
|-----------|-------------------|
| **Lost context between sessions** | Persistent memory system with tiered storage |
| **Repeating the same instructions** | Reusable slash commands (`/focus`, `/investigate`) |
| **No workflow automation** | Hooks system for auto-formatting, security gates |
| **Scattered project knowledge** | Structured patterns and quick-reference docs |
| **Recurring mistakes** | Self-improving skills that learn from errors |

**Perfect for:** AI-assisted development, agentic coding workflows, Claude Code power users, and teams wanting consistent AI interactions.

## Quick Start

### Option 1: Use as GitHub Template
1. Click "Use this template" on GitHub
2. Clone your new repository
3. Open with Claude Code - context system is ready!

### Option 2: Install Script
```bash
# From your existing project
curl -sL https://raw.githubusercontent.com/YOUR_USERNAME/claudekit/main/install.sh | bash
```

### Option 3: Manual Copy
```bash
# Clone and copy
git clone https://github.com/YOUR_USERNAME/claudekit.git /tmp/claudekit
cp -r /tmp/claudekit/.claude /path/to/your/project/
cp /tmp/claudekit/CLAUDE.md /path/to/your/project/
rm -rf /tmp/claudekit
```

> **Note:** If `.claude/` or `CLAUDE.md` already exist, the installer prompts before overwriting.

## Updating

Already have ClaudeKit installed? Update to the latest version:

### First Time Update (if you installed before v1.1.0)
Run this command to get the update mechanism:
```bash
curl -fsSL https://raw.githubusercontent.com/Nnnsightnnn/claudekit/main/update.sh | bash
```

### Future Updates
Once you have the update mechanism, use either:
```bash
# Via Claude Code
/update-template --check    # Check for updates
/update-template            # Interactive update
/update-template --auto     # Auto-update without prompts
/update-template --rollback # Restore from backup

# Or via script
./update.sh                 # Interactive (default)
./update.sh --check         # Check only
./update.sh --auto          # Auto-update
./update.sh --rollback      # Restore from backup
```

**What Gets Updated:**
| Category | Files | Behavior |
|----------|-------|----------|
| Auto-Update | Commands, skill definitions | Always updated |
| Interactive | Contribution guidelines | Shows diff, asks to merge |
| Never Touch | Memory, pain-points, CLAUDE.md | Your data preserved |

## What's Included

### Commands (`.claude/commands/`)
| Command | Purpose |
|---------|---------|
| `/focus [task]` | Load context and concentrate on a task |
| `/investigate [question]` | Search and analyze codebase |
| `/deep-investigate [problem]` | Multi-agent parallel investigation |
| `/brainstorm-design [element]` | Generate design concepts with research |
| `/plan-as-group [problem]` | 3-expert collaborative planning |
| `/sprint-plan [week]` | Weekly sprint planning |
| `/orchestrate-tasks` | Parallel task execution |
| `/bootstrap-project [dir]` | Full codebase analysis and setup |
| `/update-template` | Check for and apply template updates |
| `/hooks-analyzer` | Analyze CLAUDE.md for hook automation opportunities |

### Hooks System (`.claude/hooks/`)
Automate workflows with Claude Code hooks. Run `/hooks-analyzer` to discover opportunities based on your CLAUDE.md rules.

**Hook Types:**
| Hook | When It Fires | Use Case |
|------|---------------|----------|
| PreToolUse | Before tool runs | Block dangerous commands, validate inputs |
| PostToolUse | After tool completes | Auto-format, lint |
| Stop | Before Claude finishes | Run tests, quality gates |

**Templates included:**
- `format.sh` - Auto-format code after edits
- `validate-bash.sh` - Block dangerous bash commands
- `block-secrets.sh` - Prevent writing to sensitive files
- `run-tests.sh` - Run tests before completion

**Python Hooks (v1.2.0):**
- `skill_suggester.py` - Suggests skills based on prompt keywords
- `security_gate.py` - Blocks edits to sensitive files
- `error_detector.py` - Tracks recurring errors
- `skill_monitor.py` - Tracks skill success rates

### Skills (`.claude/skills/`)
Auto-invoked capabilities that activate based on context.

**User-Invocable Skills:**
| Skill | Purpose | Triggers |
|-------|---------|----------|
| `project-builder` | Break down projects into task lists | "build/implement" requests |
| `pain-point-manager` | Track development friction | Friction, blockers, workarounds |
| `investigation-analysis` | Analyze feature requests for ROI | "Should we build this?" |
| `bloat-manager` | Prevent system artifact growth | Mondays (auto), "check for bloat" |

**Self-Improvement Loop (v1.2.0):**
| Stage | Skill | Purpose |
|-------|-------|---------|
| 1 | `ai-error-learner` | Catalogs recurring errors as AI pain points |
| 2 | `skill-builder` | Transforms pain points into working skills |
| 3 | `skill-improver` | Monitors and fixes skills with <80% success |

**Maintenance Skills:**
| Skill | Purpose |
|-------|---------|
| `memory-consolidation` | Maintain clean memory system (manual) |

### Memory System (`.claude/memory/`)
```
memory/
├── active/
│   ├── quick-reference.md    # Top 20 patterns (check FIRST)
│   ├── procedural-memory.md  # Active patterns
│   └── episodic-memory.md    # Sprint summaries
├── structured/patterns/      # Domain-specific patterns
└── CONTRIBUTION_GUIDELINES.md
```

### Pain Point Tracking (`.claude/pain-points/`)
Track development friction with priority-based management.

## Customization

### 1. Update CLAUDE.md
Edit the root `CLAUDE.md` to match your project:
- Tech stack
- Project structure
- Custom guard rails

### 2. Configure Task System (Optional)
Commands support multiple task systems. Edit the `allowed-tools` in commands:

| System | Tools |
|--------|-------|
| Dart.ai | `mcp__dart__*` |
| GitHub Issues | `gh issue *` |
| TodoWrite | `TodoWrite` (built-in) |

### 3. Add Your Patterns
As you work, add patterns to:
- `.claude/memory/active/quick-reference.md` - Most-used patterns
- `.claude/memory/active/procedural-memory.md` - All active patterns

## File Structure

```
your-project/
├── CLAUDE.md                    # Main context file
└── .claude/
    ├── commands/               # /command files
    ├── skills/                 # Auto-invoked capabilities
    ├── hooks/                  # Hook scripts & templates
    │   ├── README.md          # Hook documentation
    │   └── templates/         # Script templates
    ├── memory/
    │   ├── active/            # Hot memory
    │   ├── structured/        # Domain patterns
    │   └── CONTRIBUTION_GUIDELINES.md
    ├── pain-points/
    │   ├── active-pain-points.md
    │   └── USAGE_GUIDE.md
    ├── specs/                  # Detailed specifications
    └── templates/              # Reusable templates
```

## Maintenance

| Frequency | Task |
|-----------|------|
| Daily | Check for stale tasks |
| Weekly | Pain point review |
| Monthly | Memory consolidation |
| Quarterly | Full audit |

## Contributing

1. Fork this repository
2. Add your improvements
3. Submit a pull request

## License

MIT License - Use freely in any project.

---

*Based on patterns from production Claude Code usage.*

---

<details>
<summary>Keywords</summary>

claude code, claude code context, anthropic claude, ai coding assistant, agentic coding, claude cli, ai pair programmer, claude code memory, claude code hooks, claude code skills, claude code commands, ai developer tools, llm context management, claude code template, claude code framework, ai workflow automation, persistent ai memory, claude code setup, ai coding workflow

</details>
