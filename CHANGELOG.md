# Changelog

All notable changes to ClaudeKit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.0] - 2026-05-04

### Added
- Canonical `SKILL.md` files for all 8 distributed skills, captured in-repo so `update.sh`'s distribution path (`.claude/skills/<skill>/SKILL.md`) actually resolves
- `ai-error-learner` upgraded to v2.2.0 — F7 false-positive filter + S8 pytest stripping rule (precision lifted 0.68 → 0.95 from a `/meta-iterate` cycle)
- `.gitignore.template` for cleaner per-project installs
- Per-skill `/meta-iterate` harness artifacts gitignored (`evals/`, `IMP-LOG.md`, `.bak`) so they stay local during skill development

### Changed
- **Breaking:** Installer now scaffolds skills at user-level (`~/.claude/skills/`) rather than per-project. Simplifies multi-repo workflows but changes where new installs put skills — existing per-project installs continue to work.
- Bumped `VERSION` to `2.0.0` to reflect the install-layout change
- Archived previous installer as `install.sh.v1-archive` for reference

### Removed
- Deprecated top-level `SKILL.md` and `skill-metrics.json` files (replaced by per-skill canonical files)
- `recycle-skills`, `repo-skill-inventory`, and `skill-conductor` from the distribution — these are meta-tools for iterating on skills, not skills the kit should ship. They live at user-level (`~/.claude/skills/`) for local use.

### Fixed
- `docs/index.html`: Removed defunct `memory-consolidation` skill card and bumped the hero version badge to v2.0.0 so the GitHub Pages site matches reality

## [1.3.0] - 2026-04-18

### Added
- `coherence` skill (v0.2.0): maintain a living, self-updating understanding of any repo through a decomposable document surface (`.claude/coherence/`)
- `/coherence` slash command for invoking the coherence skill
- Skill metrics tracking for coherence in `skill-metrics.json`

### Fixed
- install.sh: added missing v1.2.0 skills (bloat-manager, ai-error-learner, skill-builder, skill-improver) to directory creation and download steps
- install.sh: added missing `/hooks-analyzer` command (from v1.1.0) to command download loop and help text
- update.sh: added missing commands (hooks-analyzer, coherence) and skills (bloat-manager, ai-error-learner, skill-builder, skill-improver, coherence) to AUTO_UPDATE_FILES
- update.sh: added `.claude/coherence/` and `skill-metrics.json` to NEVER_TOUCH_PATTERNS to preserve user data during updates

### Changed
- Expanded README skills section to document all 9 skills
- Added skill categorization (user-invocable, self-improvement loop, maintenance, context)
- Documented all update.sh modes (--check, --auto, --rollback)
- Added file category table explaining what gets updated vs preserved
- Added Python hooks documentation to README
- Added install script interactive behavior note
- Added README badges (version, license, Claude Code compatible)
- Added "Why ClaudeKit?" section with feature comparison table
- Added SEO-friendly tagline and keywords footer for discoverability
- Improved README intro with keyword-rich description

## [1.2.0] - 2026-01-16

### Added
- Self-improvement loop with 4 interconnected skills:
  - `bloat-manager`: System health monitoring and artifact growth management
  - `ai-error-learner`: Automatic cataloging of recurring errors as pain points
  - `skill-builder`: Transforms pain points into working skills
  - `skill-improver`: Monitors and improves skill effectiveness
- Python hooks system with 4 production-ready hooks:
  - `skill_suggester.py`: Suggests relevant skills based on prompt keywords (UserPromptSubmit)
  - `security_gate.py`: Blocks edits to sensitive files like .env, secrets (PreToolUse)
  - `error_detector.py`: Fingerprints and tracks recurring errors (PostToolUse)
  - `skill_monitor.py`: Tracks skill invocations and success rates (PostToolUse)
- Episodic memory system for session summaries and discoveries
- AI-specific pain point tracking (`ai-pain-points.md`)
- Error fingerprint history (`ai-error-history.json`)
- Skill metrics tracking (`skill-metrics.json`)
- Full hooks configuration in `settings.local.json`

### Changed
- Updated `settings.local.json` with hooks configuration for all three hook types

## [1.1.0] - 2026-01-09

### Added
- `update.sh` script for updating existing installations
- `/update-template` command for guided updates via Claude Code
- `/hooks-analyzer` command for discovering hook automation opportunities
- Hooks system with templates (format, validate-bash, block-secrets, run-tests)
- Version tracking with `VERSION` file
- Automatic backup before updates
- Interactive diff/merge for customized files
- Rollback capability

### Changed
- `install.sh` now copies VERSION file during installation

### Fixed
- Interactive prompts now work when running via `curl | bash`

## [1.0.0] - 2025-01-09

### Added
- Initial release of ClaudeKit
- 8 slash commands: focus, investigate, deep-investigate, brainstorm-design, plan-as-group, sprint-plan, orchestrate-tasks, bootstrap-project
- 4 auto-triggered skills: project-builder, pain-point-manager, memory-consolidation, investigation-analysis
- Memory system with tiered storage (hot/warm/cool/cold)
- Pain points tracking system
- Guard rail specification system
- Comprehensive documentation

[Unreleased]: https://github.com/Nnnsightnnn/claudekit/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/Nnnsightnnn/claudekit/compare/v1.3.0...v2.0.0
[1.3.0]: https://github.com/Nnnsightnnn/claudekit/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/Nnnsightnnn/claudekit/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/Nnnsightnnn/claudekit/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/Nnnsightnnn/claudekit/releases/tag/v1.0.0
