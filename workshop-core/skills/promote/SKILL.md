---
name: promote
description: Promote a completed PBL proposal from the workspace to the target directory and archive the development records. Use when a proposal has been approved and is ready to ship.
allowed-tools: Read, Write, Bash, Glob
user-invocable: true
---

# Workshop Promote

Move a completed course proposal from the development workspace (`studio/changes/`) to its production location, then archive the development record.

## Pre-conditions

1. If `$ARGUMENTS` is empty, scan `studio/changes/` for proposals with phase `approved` and list them. If exactly one, use it. If multiple, ask the user to choose. If none, explain what's needed and exit.
2. Read `studio/changes/$ARGUMENTS/status.json`
3. Verify `phase` is `approved` — if not, show the current phase and explain:
   - `planning` → "This proposal is still in the planning phase. Run `/workshop-designer:design {name}` to develop it further."
   - `designing` → "This proposal is still being designed. Complete the design before promoting."
   - `reviewing` → "This proposal is under review. Complete the review and set phase to approved first."
   - `shipped` → "This proposal has already been shipped."
4. Read `target_collection` from status.json (fallback to `studio/config.yaml` `defaults.target_collection`)
5. Verify all skills in status.json have status `done` or `approved`

If pre-conditions fail, print a clear message about what needs to happen first and exit.

## Promote Steps

### Step 1: Determine target

```
{target_collection}/{proposal-name}/
```

Where `target_collection` is the path from status.json (e.g., `courses/nature` or just `courses`).

If the target directory already exists, ask the user whether to overwrite.

### Step 2: Build production plugin structure

Create the target directory with standard Claude Code plugin layout:

```
{target}/{proposal-name}/
├── .claude-plugin/
│   └── plugin.json         # finalized from plugin.json.draft
├── skills/
│   └── {skill-name}/
│       ├── SKILL.md         # from studio/changes/{name}/skills/{skill}/SKILL.md
│       ├── scripts/         # copy if present
│       └── references/      # copy if present
├── commands/                # copy if present
├── hooks/                   # copy if present
└── .mcp.json                # copy if present
```

When copying `plugin.json.draft` to `plugin.json`:
- Remove the `.draft` suffix
- Ensure `name`, `version`, `description` are present
- Set `skills` to `"./skills/"`
- Add `"commands": "./commands/"` if a commands/ directory exists
- Add `"hooks": "./hooks/hooks.json"` if a hooks/ directory exists
- Add `"mcpServers": "./.mcp.json"` if a .mcp.json file exists

### Step 3: Update domain workspace

If the proposal's `status.json` contains a `domain` field:
1. Read `studio/changes/{domain}/status.json`
2. Remove the proposal name from the domain's `plugins` list
3. Write the updated status.json back

This keeps the domain workspace's plugin list accurate.

### Step 4: Archive development record

Move `studio/changes/{name}/` to `studio/archive/{YYYY-MM-DD}-{name}/`

Update the archived `status.json`:
- Set `phase` to `shipped`
- Add `shipped_at` timestamp (ISO 8601 format)
- Add `shipped_to` path (the target directory)

### Step 5: Report

Print:
- What was promoted and where (e.g., "Promoted `seasons-pbl` to `courses/seasons-pbl/`")
- Archive location (e.g., "Development records archived to `studio/archive/2026-03-28-seasons-pbl/`")
- Remind user to review and commit: "Review the promoted proposal, then commit when ready."

## Does NOT

- Run `git add` or `git commit` — the user decides when to commit
- Delete source files — they're archived, not deleted
- Run validation — that should have happened before approval
