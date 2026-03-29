---
name: promote
description: Promote approved project deliverables from a workspace to the target directory and archive the development records. Use when a project has been approved and is ready to ship.
allowed-tools: Read, Write, Bash, Glob
user-invocable: true
---

# Workshop Promote

Move approved course deliverables from the development workspace (`studio/changes/`) to their production location, then archive the development record.

## Pre-conditions

1. If `$ARGUMENTS` is empty, scan `studio/changes/` for project workspaces with phase `approved` and list them. If exactly one, use it. If multiple, ask the user to choose. If none, explain what's needed and exit.
2. Read `studio/changes/$ARGUMENTS/status.json`
3. Verify the workspace is a project:
   - If `type == "planning"`, stop and tell the user planning records are not shippable course deliverables
   - If `type` is missing, treat it as legacy and proceed only if course deliverables are present
4. Verify `phase` is `approved` — if not, show the current phase and explain:
   - `planning` → "This project is still in the planning phase. Continue the design work before promoting."
   - `designing` → "This project is still being designed. Complete the design before promoting."
   - `reviewing` → "This project is under review. Complete the review and set phase to approved first."
   - `shipped` → "This project has already been shipped."
5. Read `target_collection` from status.json (fallback to `studio/config.yaml` `defaults.target_collection`)
6. Run:

```bash
python3 workshop-core/scripts/workspace_status.py validate-project {workspace} --required-phase approved
```

This validates:
- final deliverables exist
- required skill statuses are complete
- the project is in the `approved` phase

If pre-conditions fail, print a clear message about what needs to happen first and exit.

## Promote Steps

### Step 1: Execute Promote

Run:

```bash
python3 workshop-core/scripts/workspace_status.py promote-project {workspace}
```

This performs the full promote flow:
- resolve `target_collection`
- copy final deliverables into `{target_collection}/{project-name}/`
- copy supporting artifacts when present
- remove the project from any legacy domain workspace metadata
- move the source workspace into `studio/archive/{YYYY-MM-DD}-{name}/`
- update archived `status.json` with:
  - `phase = "shipped"`
  - `shipped_at`
  - `shipped_to`

If the target directory already exists, ask the user whether to rerun with overwrite:

```bash
python3 workshop-core/scripts/workspace_status.py promote-project {workspace} --overwrite
```

### Step 5: Report

Print:
- What was promoted and where (e.g., "Promoted `spring-flowers` to `courses/spring-flowers/`")
- Archive location (e.g., "Development records archived to `studio/archive/2026-03-28-seasons-pbl/`")
- Remind user to review and commit: "Review the promoted deliverables, then commit when ready."

## Does NOT

- Run `git add` or `git commit` — the user decides when to commit
- Delete source files — they're archived, not deleted
- Run validation — that should have happened before approval
