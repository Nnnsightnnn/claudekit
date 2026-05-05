---
name: repo-skill-inventory
description: Walk all .claude/skills/ directories on the user's Mac and produce a structured inventory of every Claude Code skill across every repo and the user-level skills dir. Detect duplicates, drift, staleness, orphans, and worktree bloat. Use when the user asks to audit their skills, find duplicate skills, see which skills have drifted across repos, identify stale skills, or generate a cross-repo skill report. Outputs JSON to ~/.claude-desktop/exports/ and a human-readable markdown summary to stdout.
allowed-tools: Read, Bash, Write, Glob, Grep
---

# repo-skill-inventory

A Claude Code user-level skill that produces a comprehensive cross-repo inventory of all `.claude/skills/` directories on the local machine. Designed to give the user (and the meta-agent) a single source of truth about which skills exist where, which have drifted, and which need attention.

## When to use

Invoke this skill when the user asks any of:

- "What skills do I have across all my repos?"
- "Are any of my skills duplicated or drifted?"
- "Which skills are stale / haven't been touched in a while?"
- "Audit my Claude Code skills."
- "Generate a skill inventory."
- "Are there any orphaned or broken skill dirs?"
- "Is the `.claude/worktrees/` dir bloated anywhere?"

Also invoke proactively before any large-scale skill refactor (e.g. "promote skill X to user level", "delete unused trackers", "deduplicate skills"), so the agent has accurate, current ground truth.

## Invocation

The skill ships with a Python 3 scanner that uses only the standard library (no external deps). Run it from any working directory:

```bash
python3 ~/.claude/skills/repo-skill-inventory/scanner.py
```

Optional flags:

- `--json-only` — suppress markdown summary, only write JSON
- `--quiet` — suppress per-repo progress output
- `--no-export` — skip writing `~/.claude-desktop/exports/...` (still print to stdout)

The scanner writes a timestamped JSON file to `~/.claude-desktop/exports/skill-inventory-<ISO>.json` and atomically updates the symlink `~/.claude-desktop/exports/skill-inventory-latest.json` to point at the latest scan.

Exit codes: `0` on success, `1` if any I/O or parse errors were encountered (the scan still completes — exit code signals attention needed).

## What it scans

1. **The 15 known tracked repos** under `~/`:
   `autonomous-drive`, `braves-tracker`, `claude-econ`, `claudekit`, `colony_mvp`, `falcons-tracker`, `family-recipes`, `gameday-playsheet`, `hawks-tracker`, `job-hunter`, `liverpool-tracker`, `playmakers-data`, `shell-odyssey`, `web-pulse`, `workout-app`.

2. **Auto-discovers** any additional repos via:
   ```bash
   find ~/ -maxdepth 3 -type d -name '.claude'
   ```
   Excluding `~/.claude` itself, `~/.claude-worktrees`, and `playmakers-data/.claude/worktrees` (those are not skill homes).

3. **The user-level skills dir** `~/.claude/skills/` (e.g. the `meta-agent-trial` skill).

For each `SKILL.md` file the scanner extracts the YAML frontmatter (`name`, `description`, `allowed-tools`), counts lines, computes a sha256 of the content, captures the file mtime, and records absolute path.

## Tier detection heuristics

Each repo is bucketed into a tier based on its `.claude/` shape:

| Tier | Heuristic |
|---|---|
| **Production** | 24+ skills AND a `hooks/` dir AND an `audits/` dir |
| **Advanced** | 5+ skills AND a `hooks/` dir (but not Production) |
| **Expanded** | 5-9 skills, no `hooks/` dir |
| **Tracker** | Has a skill named `*-tracker-update` |
| **Base** | Only the 4 baseline skills or fewer |

Tier classification is single-pick, evaluated top-down (Production > Advanced > Expanded > Tracker > Base). Edge cases (e.g. a tracker repo that also has 6 skills) are reported as their highest matching tier.

## Output schema

```json
{
  "scan_date": "2026-04-30T12:34:56",
  "scan_duration_ms": 1234,
  "total_skills_found": 65,
  "total_repos_scanned": 15,
  "user_level_skills_count": 1,
  "skills": [
    {
      "name": "string",
      "location": "/abs/path/SKILL.md",
      "sha256": "hex",
      "mtime": "ISO-8601",
      "line_count": 0,
      "size_bytes": 0,
      "description": "string",
      "allowed_tools": ["Read", "Write"],
      "duplicates": ["/other/path/SKILL.md"],
      "drift_status": "identical | drifted | unique",
      "stale_days": 0,
      "tier": "user-level | production | advanced | expanded | tracker | base"
    }
  ],
  "repos": [
    {
      "name": "string",
      "path": "/abs/path",
      "skills_count": 0,
      "size_bytes": 0,
      "worktree_size_bytes": 0,
      "last_modified": "ISO-8601",
      "tier": "string"
    }
  ],
  "alerts": [
    {
      "severity": "high | med | low",
      "kind": "stale | drift | orphan | bloat",
      "details": "human-readable string",
      "path": "/abs/path"
    }
  ]
}
```

## Alert kinds

- **stale** (low/med): skill mtime > 90 days. Med if > 180 days.
- **drift** (med/high): same skill `name` appears in 2+ locations with different sha256. High if 3+ drifted copies.
- **orphan** (med): empty skill dir (dir exists, no `SKILL.md`).
- **bloat** (high): any `.claude/worktrees/` dir > 100 MB.

## Integration with the meta-agent-trial pattern

This skill is the eyes-and-ears layer for the **meta-agent-trial** pattern: the meta agent reasons about *which skills should exist where*, but it can only do that if it knows what currently exists. `repo-skill-inventory` is the deterministic, no-LLM scanner that feeds the meta-agent its ground truth.

Typical flow:

1. User asks the meta-agent for a cross-repo refactor (e.g. "promote my best testing skill to user level, delete the duplicates").
2. Meta-agent invokes `repo-skill-inventory` first, reads the latest JSON from `~/.claude-desktop/exports/skill-inventory-latest.json`.
3. Meta-agent uses the `skills[]` array (with `drift_status` and `duplicates`) to identify candidates, the `alerts[]` array to surface problems, and `repos[].tier` to understand each repo's maturity.
4. Meta-agent proposes a plan grounded in real paths and real sha256s — no hallucinated skill names, no guessed repo tiers.
5. After the refactor, meta-agent re-runs this skill to verify the change landed.

Because the scanner is pure stdlib Python and writes JSON to a stable path, it can be cron'd, hooked into pre-commit, or invoked from any other skill via `Bash`. The `latest.json` symlink means downstream consumers never need to know the scan timestamp.
