#!/usr/bin/env python3
"""UserPromptSubmit hook: Suggests skills based on prompt keywords."""
import json
import sys
import re

SKILL_TRIGGERS = {
    "investigation-analysis": {
        "patterns": [r"\binvestigat\w*\b", r"\banalyze?\b", r"\bfeasib\w*\b", r"\broi\b", r"\bshould we build\b"],
        "description": "Use /investigate for ROI analysis"
    },
    "pain-point-manager": {
        "patterns": [r"\bfriction\b", r"\bblocker\b", r"\bworkaround\b", r"\bpain\s*point\b", r"\bfrustrat\w*\b"],
        "description": "Pain point detected - will auto-catalog"
    },
    "bloat-manager": {
        "patterns": [r"\bbloat\b", r"\bclean\s*up\b", r"\bconsolidat\w*\b", r"\bsystem\s*health\b", r"\barchive\b"],
        "description": "Use bloat-manager for cleanup review"
    },
    "project-builder": {
        "patterns": [r"\bbuild\s+\w+\b", r"\bimplement\s+\w+\b", r"\bcreate\s+project\b", r"\bmulti.*task\b"],
        "description": "Use /project-builder for complex projects"
    },
    "ai-error-learner": {
        "patterns": [r"\brecurring\s+error\b", r"\bsame\s+error\b", r"\berror\s+pattern\b", r"\bkeeps?\s+fail\w*\b"],
        "description": "Recurring error detected - cataloging for improvement"
    },
    "skill-builder": {
        "patterns": [r"\bcreate\s+skill\b", r"\bnew\s+skill\b", r"\bbuild\s+skill\b", r"\bautomate\s+this\b"],
        "description": "Use skill-builder to create new skills"
    },
    "skill-improver": {
        "patterns": [r"\bskill\s+fail\w*\b", r"\bfix\s+skill\b", r"\bimprove\s+skill\b", r"\bskill.*not\s+work\b"],
        "description": "Use skill-improver to fix skill issues"
    }
}

def analyze_prompt(prompt: str) -> list[str]:
    """Analyze prompt for skill trigger patterns."""
    suggestions = []
    prompt_lower = prompt.lower()

    for skill, config in SKILL_TRIGGERS.items():
        for pattern in config["patterns"]:
            if re.search(pattern, prompt_lower):
                suggestions.append(f"- {config['description']}")
                break

    return suggestions

def main():
    try:
        data = json.load(sys.stdin)
        prompt = data.get("prompt", "")

        if not prompt:
            print(json.dumps({"continue": True}))
            return

        suggestions = analyze_prompt(prompt)

        if suggestions:
            context = "**Skill Suggestions:**\n" + "\n".join(suggestions)
            print(json.dumps({"continue": True, "additionalContext": context}))
        else:
            print(json.dumps({"continue": True}))

    except Exception:
        # NEVER block on errors - fail open
        print(json.dumps({"continue": True}))
        sys.exit(0)

if __name__ == "__main__":
    main()
