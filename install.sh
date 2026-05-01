#!/bin/bash
# ClaudeKit Installer (lean scaffold — v2.0.0)
#
# Scaffolds a new repo with a Claude-Code-instrumented .claude/ directory.
# Skills now live at user-level (~/.claude/skills/) — they are NOT scaffolded
# per-repo to prevent the duplication pattern we cleaned up in 2026-04-30.
#
# Usage: ./install.sh [target_directory]
#    or: curl -fsSL https://raw.githubusercontent.com/USERNAME/claudekit/main/install.sh | bash

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

REPO_URL="https://github.com/Nnnsightnnn/claudekit"
TARGET_DIR="${1:-.}"

echo -e "${GREEN}ClaudeKit Installer (lean v2.0.0)${NC}"
echo "===================================="
echo ""

if [ ! -d "$TARGET_DIR" ]; then
    echo -e "${RED}Error: Target directory '$TARGET_DIR' does not exist${NC}"
    exit 1
fi

cd "$TARGET_DIR"
TARGET_DIR=$(pwd)

echo -e "Installing to: ${YELLOW}$TARGET_DIR${NC}"
echo ""

# Pre-flight: warn about user-level skills dependency
if [ ! -d "$HOME/.claude/skills" ]; then
    echo -e "${YELLOW}Note:${NC} ~/.claude/skills/ doesn't exist yet."
    echo "  Skills (project-builder, pain-point-manager, investigation-analysis,"
    echo "  ai-error-learner, etc.) are now installed at user level — not per-repo."
    echo "  This scaffold only creates the per-repo .claude/ structure (memory,"
    echo "  pain-points, hooks, commands, settings)."
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    [[ ! $REPLY =~ ^[Yy]$ ]] && exit 0
fi

# Existing-files checks
if [ -d ".claude" ]; then
    echo -e "${YELLOW}Warning: .claude/ directory already exists${NC}"
    read -p "Overwrite? (y/N) " -n 1 -r
    echo
    [[ ! $REPLY =~ ^[Yy]$ ]] && { echo "Cancelled."; exit 0; }
    rm -rf .claude
fi

if [ -f "CLAUDE.md" ]; then
    echo -e "${YELLOW}Warning: CLAUDE.md already exists${NC}"
    read -p "Overwrite? (y/N) " -n 1 -r
    echo
    [[ ! $REPLY =~ ^[Yy]$ ]] && SKIP_CLAUDE_MD=true
fi

echo "Creating directory structure..."

# Per-repo .claude/ structure (NO skills/ — those are at user level)
mkdir -p .claude/{commands,hooks,memory/{active,structured/patterns,indexes,archives,maintenance},pain-points/archives,templates,specs}

echo "Downloading template files..."

download_file() {
    local src="$1"
    local dest="$2"
    if command -v curl &> /dev/null; then
        curl -fsSL "$REPO_URL/raw/main/$src" -o "$dest" 2>/dev/null || echo "  Skipped: $dest (offline or repo unreachable)"
    elif command -v wget &> /dev/null; then
        wget -q "$REPO_URL/raw/main/$src" -O "$dest" 2>/dev/null || echo "  Skipped: $dest"
    fi
}

# Commands (slash commands the repo gets)
echo "  Commands..."
for cmd in focus investigate deep-investigate brainstorm-design plan-as-group sprint-plan orchestrate-tasks bootstrap-project update-template hooks-analyzer coherence; do
    download_file ".claude/commands/$cmd.md" ".claude/commands/$cmd.md"
done

# Hooks (per-repo hooks — generic, use $CLAUDE_PROJECT_DIR)
echo "  Hooks..."
for hook in error_detector security_gate skill_monitor skill_suggester; do
    download_file ".claude/hooks/$hook.py" ".claude/hooks/$hook.py"
done
download_file ".claude/hooks/README.md" ".claude/hooks/README.md"

# Memory templates
echo "  Memory templates..."
download_file ".claude/memory/active/quick-reference.md" ".claude/memory/active/quick-reference.md"
download_file ".claude/memory/active/procedural-memory.md" ".claude/memory/active/procedural-memory.md"
download_file ".claude/memory/active/episodic-memory.md" ".claude/memory/active/episodic-memory.md"
download_file ".claude/memory/CONTRIBUTION_GUIDELINES.md" ".claude/memory/CONTRIBUTION_GUIDELINES.md"

# Pain-points templates
echo "  Pain-points scaffold..."
download_file ".claude/pain-points/active-pain-points.md" ".claude/pain-points/active-pain-points.md"
download_file ".claude/pain-points/ai-pain-points.md" ".claude/pain-points/ai-pain-points.md"
download_file ".claude/pain-points/USAGE_GUIDE.md" ".claude/pain-points/USAGE_GUIDE.md"

# Initialize empty error history (the canonical empty shape)
cat > .claude/pain-points/ai-error-history.json <<'JSON'
{
  "errors": {},
  "metadata": {
    "created": "TODAY_PLACEHOLDER",
    "updated": "TODAY_PLACEHOLDER",
    "version": "1.0.0",
    "description": "Tracks error fingerprints for self-improvement loop",
    "thresholds": { "catalog": 2, "escalate": 3 }
  }
}
JSON

# Settings — ONLY the template ships; user copies to settings.local.json
echo "  Settings template..."
download_file ".claude/settings.template.json" ".claude/settings.template.json"

# CLAUDE.md template
if [ "$SKIP_CLAUDE_MD" != "true" ]; then
    echo "  CLAUDE.md template..."
    download_file "CLAUDE.md" "CLAUDE.md"
fi

# .gitignore additions (extend, don't overwrite)
echo "  Extending .gitignore..."
GITIGNORE_BLOCK="
# --- ClaudeKit ---
.claude/pain-points/ai-error-history.json
.claude/skills/*/SKILL.md.bak-*
.claude/skills/*/evals/runs/
.claude/skills/*/evals/candidates/
.claude/worktrees/
.claude/settings.local.json
# --- /ClaudeKit ---
"
if [ -f ".gitignore" ]; then
    if ! grep -q "ClaudeKit" .gitignore; then
        echo "$GITIGNORE_BLOCK" >> .gitignore
        echo "    appended ClaudeKit block to existing .gitignore"
    else
        echo "    .gitignore already has ClaudeKit block — skipped"
    fi
else
    echo "$GITIGNORE_BLOCK" > .gitignore
    echo "    created .gitignore with ClaudeKit block"
fi

# README + VERSION
echo "  Documentation..."
download_file ".claude/README.md" ".claude/README.md"
download_file "VERSION" ".claude/VERSION"

# .gitkeep files for empty dirs
touch .claude/memory/archives/.gitkeep
touch .claude/memory/indexes/.gitkeep
touch .claude/memory/structured/patterns/.gitkeep
touch .claude/memory/maintenance/.gitkeep
touch .claude/pain-points/archives/.gitkeep
touch .claude/templates/.gitkeep
touch .claude/specs/.gitkeep

# Substitute today's date in placeholder fields
TODAY=$(date +%Y-%m-%d)
NEXT_WEEK=$(date -v+7d +%Y-%m-%d 2>/dev/null || date -d "+7 days" +%Y-%m-%d 2>/dev/null || echo "[DATE + 7 days]")

if [[ "$OSTYPE" == "darwin"* ]]; then
    SED_INPLACE=("sed" "-i" "")
else
    SED_INPLACE=("sed" "-i")
fi

find .claude -name "*.md" -exec "${SED_INPLACE[@]}" "s/\[DATE\]/$TODAY/g" {} \;
find .claude -name "*.md" -exec "${SED_INPLACE[@]}" "s/\[DATE + 7 days\]/$NEXT_WEEK/g" {} \;
"${SED_INPLACE[@]}" "s/TODAY_PLACEHOLDER/${TODAY}T00:00:00/g" .claude/pain-points/ai-error-history.json
[ -f "CLAUDE.md" ] && "${SED_INPLACE[@]}" "s/\[DATE\]/$TODAY/g" "CLAUDE.md"

INSTALLED_VERSION=$(cat .claude/VERSION 2>/dev/null || echo "unknown")

echo ""
echo -e "${GREEN}Installation complete.${NC}"
echo -e "Version: ${YELLOW}$INSTALLED_VERSION${NC}"
echo ""
echo "What you got (per-repo):"
echo "  CLAUDE.md                    # Customize for THIS project"
echo "  .claude/commands/            # 11 slash commands"
echo "  .claude/hooks/               # 4 hook scripts (use \$CLAUDE_PROJECT_DIR)"
echo "  .claude/memory/              # Memory templates (active, structured, archives)"
echo "  .claude/pain-points/         # Friction tracking (with empty error history JSON)"
echo "  .claude/settings.template.json # Hooks + permission template"
echo "  .gitignore                   # Extended with ClaudeKit block"
echo ""
echo -e "${BLUE}What you DID NOT get (these are user-level now):${NC}"
echo "  ~/.claude/skills/            # Skills (project-builder, ai-error-learner, etc.)"
echo "  ~/.claude/commands/          # User-level slash commands (e.g. /meta-iterate)"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "  1. cp .claude/settings.template.json .claude/settings.local.json"
echo "  2. Edit settings.local.json to add project-specific Bash/WebFetch permissions"
echo "  3. Edit CLAUDE.md with this project's tech stack and guard rails"
echo "  4. Verify user-level skills: ls ~/.claude/skills/"
echo "  5. (Optional) Run /bootstrap-project to analyze your codebase"
echo ""
echo "To update later:"
echo "  /update-template --check   # Check for updates"
echo "  /update-template           # Interactive update"
echo ""
echo -e "For more info: ${YELLOW}.claude/README.md${NC}"
