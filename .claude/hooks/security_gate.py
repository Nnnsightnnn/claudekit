#!/usr/bin/env python3
"""PreToolUse hook: Blocks edits to sensitive files."""
import json
import sys

SENSITIVE_PATTERNS = [
    '.env',
    'secrets',
    'credentials',
    '.git/',
    'id_rsa',
    'private_key',
    'password',
    'token',
    'api_key',
    '.pem',
    '.key',
    'oauth',
    'auth.json',
    'config.secret'
]

def main():
    try:
        data = json.load(sys.stdin)
        tool_input = data.get("tool_input", {})

        # Handle both file_path (Edit/Write) and path patterns
        file_path = tool_input.get("file_path", "") or tool_input.get("path", "")
        file_path_lower = file_path.lower()

        for pattern in SENSITIVE_PATTERNS:
            if pattern in file_path_lower:
                print(json.dumps({
                    "continue": False,
                    "message": f"Blocked: Cannot edit sensitive file matching '{pattern}'. If this is intentional, please confirm explicitly."
                }))
                sys.exit(2)

        # Allow the operation
        print(json.dumps({"continue": True}))

    except Exception:
        # Fail open - never block on hook errors
        print(json.dumps({"continue": True}))
        sys.exit(0)

if __name__ == "__main__":
    main()
