# Changelog

All notable changes to ClaudeKit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- Expanded README skills section to document all 8 skills
- Added skill categorization (user-invocable, self-improvement loop, maintenance)
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

[Unreleased]: https://github.com/Nnnsightnnn/claudekit/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/Nnnsightnnn/claudekit/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/Nnnsightnnn/claudekit/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/Nnnsightnnn/claudekit/releases/tag/v1.0.0
