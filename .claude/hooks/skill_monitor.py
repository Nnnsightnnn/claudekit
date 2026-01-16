#!/usr/bin/env python3
"""PostToolUse hook: Tracks skill metrics for effectiveness monitoring."""
import json
import sys
import re
from datetime import datetime
from pathlib import Path

# Find project root
PROJECT_ROOT = Path.cwd()
METRICS_FILE = PROJECT_ROOT / ".claude" / "skills" / "skill-metrics.json"

# Outcome detection patterns
FAILURE_INDICATORS = [
    r"\bfailed\b",
    r"\berror\b",
    r"\bunable\s+to\b",
    r"\bcannot\b",
    r"\bexception\b",
    r"\brejected\b",
]

SUCCESS_INDICATORS = [
    r"\bsuccess(?:fully)?\b",
    r"\bcomplete[d]?\b",
    r"\bdone\b",
    r"\bfinished\b",
    r"\bcreated\b",
    r"\bupdated\b",
]


def load_metrics() -> dict:
    """Load skill metrics file."""
    if not METRICS_FILE.exists():
        return {
            "skills": {},
            "metadata": {
                "created": datetime.now().isoformat(),
                "version": "1.0.0"
            }
        }
    try:
        with open(METRICS_FILE) as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {
            "skills": {},
            "metadata": {
                "created": datetime.now().isoformat(),
                "version": "1.0.0"
            }
        }


def save_metrics(metrics: dict):
    """Save skill metrics file."""
    METRICS_FILE.parent.mkdir(parents=True, exist_ok=True)
    metrics["metadata"] = metrics.get("metadata", {})
    metrics["metadata"]["updated"] = datetime.now().isoformat()
    with open(METRICS_FILE, "w") as f:
        json.dump(metrics, f, indent=2)


def detect_outcome(output: str) -> str:
    """Determine if skill execution was success, failure, or partial."""
    lower_output = output.lower()

    failure_count = sum(1 for p in FAILURE_INDICATORS if re.search(p, lower_output))
    success_count = sum(1 for p in SUCCESS_INDICATORS if re.search(p, lower_output))

    if failure_count > success_count:
        return "failure"
    elif success_count > 0:
        return "success"
    else:
        return "partial"


def extract_failure_pattern(output: str) -> str:
    """Extract a brief failure pattern from output."""
    lower_output = output.lower()

    for pattern in FAILURE_INDICATORS:
        match = re.search(pattern, lower_output)
        if match:
            # Get surrounding context
            start = max(0, match.start() - 20)
            end = min(len(output), match.end() + 30)
            return output[start:end].strip()

    return "unknown"


def main():
    try:
        data = json.load(sys.stdin)

        # Only process Skill tool invocations
        if data.get("tool_name") != "Skill":
            print(json.dumps({}))
            sys.exit(0)

        tool_input = data.get("tool_input", {})
        skill = tool_input.get("skill", "unknown")
        output = str(data.get("tool_output", ""))

        # Determine outcome
        outcome = detect_outcome(output)

        # Load and update metrics
        metrics = load_metrics()

        if skill not in metrics["skills"]:
            metrics["skills"][skill] = {
                "invocations": 0,
                "successes": 0,
                "failures": 0,
                "partials": 0,
                "first_invoked": datetime.now().isoformat(),
                "last_invoked": None,
                "failure_patterns": [],
                "improvements": []
            }

        entry = metrics["skills"][skill]
        entry["invocations"] += 1
        entry["last_invoked"] = datetime.now().isoformat()

        if outcome == "success":
            entry["successes"] += 1
        elif outcome == "failure":
            entry["failures"] += 1
            # Track failure pattern (keep last 5)
            pattern = extract_failure_pattern(output)
            patterns = entry.get("failure_patterns", [])
            if pattern not in patterns:
                patterns.append(pattern)
            entry["failure_patterns"] = patterns[-5:]
        else:
            entry["partials"] = entry.get("partials", 0) + 1

        # Calculate success rate
        total_decisive = entry["successes"] + entry["failures"]
        if total_decisive > 0:
            entry["success_rate"] = round((entry["successes"] / total_decisive) * 100, 1)
        else:
            entry["success_rate"] = 100.0

        save_metrics(metrics)

        # Alert if skill is struggling
        response = {}
        if entry["success_rate"] < 80 and total_decisive >= 3:
            response["additionalContext"] = f"**Skill health alert**: `{skill}` has {entry['success_rate']}% success rate. Consider using skill-improver."
        elif entry["failures"] >= 2:
            response["additionalContext"] = f"**Skill has {entry['failures']} failures**. Consider reviewing with skill-improver."

        print(json.dumps(response))

    except Exception:
        # NEVER block on errors - fail open
        print(json.dumps({}))
        sys.exit(0)


if __name__ == "__main__":
    main()
