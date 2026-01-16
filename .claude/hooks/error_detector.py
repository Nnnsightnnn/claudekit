#!/usr/bin/env python3
"""PostToolUse hook: Detects and tracks error fingerprints for self-improvement."""
import json
import sys
import re
from datetime import datetime
from pathlib import Path

# Error patterns to detect
ERROR_PATTERNS = [
    r"\berror\b",
    r"\bfailed?\b",
    r"\bdenied\b",
    r"\bnot\s+found\b",
    r"\btimeout\b",
    r"\bexception\b",
    r"\b[45]\d{2}\b",  # HTTP 4xx/5xx
    r"\bpermission\b",
    r"\brefused\b",
    r"\brejected\b",
    r"\bunable\s+to\b",
    r"\bcannot\b",
    r"\bno\s+such\b",
]

# Threshold for creating pain point
CATALOG_THRESHOLD = 2

# Find project root (where .claude directory is)
PROJECT_ROOT = Path.cwd()
HISTORY_FILE = PROJECT_ROOT / ".claude" / "pain-points" / "ai-error-history.json"


def detect_errors(output: str) -> list[str]:
    """Find error patterns in output."""
    lower_output = output.lower()
    return [p for p in ERROR_PATTERNS if re.search(p, lower_output)]


def create_fingerprint(tool: str, errors: list[str], output: str) -> str:
    """Create consistent fingerprint for error categorization."""
    # Use first detected error type
    error_type = errors[0].upper().replace(" ", "_").replace("\\B", "").replace("\\S+", "_") if errors else "UNKNOWN"
    error_type = re.sub(r'[^A-Z_0-9]', '', error_type)

    # Extract meaningful context from output (first recognizable keyword)
    context_match = re.search(r'[\w/.-]+', output[:100])
    context = context_match.group(0)[:30] if context_match else "unknown"

    return f"[{tool.upper()}]-[{error_type}]-[{context}]"


def load_history() -> dict:
    """Load error history file."""
    if not HISTORY_FILE.exists():
        return {"errors": {}, "metadata": {"created": datetime.now().isoformat()}}
    try:
        with open(HISTORY_FILE) as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"errors": {}, "metadata": {"created": datetime.now().isoformat()}}


def save_history(history: dict):
    """Save error history file."""
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    history["metadata"] = history.get("metadata", {})
    history["metadata"]["updated"] = datetime.now().isoformat()
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def update_history(fingerprint: str, tool: str, output: str) -> tuple[int, bool]:
    """Update error history and return (count, is_new)."""
    history = load_history()
    now = datetime.now().isoformat()

    is_new = fingerprint not in history["errors"]

    if is_new:
        history["errors"][fingerprint] = {
            "count": 1,
            "first_seen": now,
            "last_seen": now,
            "tool": tool,
            "contexts": [output[:200]]
        }
    else:
        entry = history["errors"][fingerprint]
        entry["count"] += 1
        entry["last_seen"] = now
        # Keep last 5 contexts for debugging
        contexts = entry.get("contexts", [])
        contexts.append(output[:200])
        entry["contexts"] = contexts[-5:]

    save_history(history)
    return history["errors"][fingerprint]["count"], is_new


def main():
    try:
        data = json.load(sys.stdin)
        tool = data.get("tool_name", "unknown")
        output = str(data.get("tool_output", ""))

        # Only process if there's output to analyze
        if not output:
            print(json.dumps({}))
            sys.exit(0)

        # Detect error patterns
        errors = detect_errors(output)

        if not errors:
            # No errors detected
            print(json.dumps({}))
            sys.exit(0)

        # Create fingerprint and update history
        fingerprint = create_fingerprint(tool, errors, output)
        count, is_new = update_history(fingerprint, tool, output)

        # Build response based on threshold
        if count >= CATALOG_THRESHOLD:
            response = {
                "additionalContext": f"**Recurring error detected** (occurrence #{count}): `{fingerprint}`\nConsider using ai-error-learner to catalog this pattern."
            }
        else:
            # First occurrence - silent logging, no output
            response = {}

        print(json.dumps(response))

    except Exception:
        # NEVER block on errors - fail open
        print(json.dumps({}))
        sys.exit(0)


if __name__ == "__main__":
    main()
