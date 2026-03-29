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
6. Verify all required skills in status.json have status `done` or `approved`

Required skills by deliverable type:
- If `proposal.md` exists: `driving-question`, `network-map`, `inquiry-scaffold`, `activity-design`, `proposal-generate`
- If `lesson-plan.md` exists: `lesson-objective`, `lesson-scaffold`, `lesson-detail`, `lesson-generate`
- If both exist, validate both sets

If pre-conditions fail, print a clear message about what needs to happen first and exit.

## Promote Steps

### Step 1: Determine target

```
{target_collection}/{project-name}/
```

Where `target_collection` is the path from status.json (e.g., `courses/nature` or just `courses`).

If the target directory already exists, ask the user whether to overwrite.

### Step 2: Build production deliverable structure

Create the target directory by copying the finalized course deliverables:

```
{target_collection}/{project-name}/
├── proposal.md                 # copy if present
├── lesson-plan.md              # copy if present
├── quality-report.md           # copy if present
├── review-comments.md          # copy if present
├── resource-plan.md            # copy if present
├── resource-check-report.md    # copy if present
├── theme-analysis.md           # copy if present
├── prior-knowledge.md          # copy if present
├── competency-mapping.md       # copy if present
├── driving-question.md
├── network-map.md
├── inquiry-clues.md
└── activities/
    ├── clue-1.md
    ├── clue-2.md
    └── clue-3.md
```

Rules:
- At least one final deliverable must exist: `proposal.md` or `lesson-plan.md`
- If neither exists, stop and tell the user to run `/workshop-designer:proposal-generate` or `/workshop-lesson:lesson-generate`
- Copy supporting artifacts when present so the shipped project keeps its review and planning context
- Do not transform the project into a plugin package; this skill ships course deliverables, not SKILL.md plugins

### Step 3: Update domain workspace

If the project's `status.json` contains a legacy `domain` field:
1. Read `studio/changes/{domain}/status.json`
2. Remove the project name from the domain's `plugins` list
3. Write the updated status.json back

This keeps the legacy domain workspace metadata accurate.

### Step 4: Archive development record

Move `studio/changes/{name}/` to `studio/archive/{YYYY-MM-DD}-{name}/`

Update the archived `status.json`:
- Set `phase` to `shipped`
- Add `shipped_at` timestamp (ISO 8601 format)
- Add `shipped_to` path (the target directory)

### Step 5: Report

Print:
- What was promoted and where (e.g., "Promoted `spring-flowers` to `courses/spring-flowers/`")
- Archive location (e.g., "Development records archived to `studio/archive/2026-03-28-seasons-pbl/`")
- Remind user to review and commit: "Review the promoted deliverables, then commit when ready."

## Does NOT

- Run `git add` or `git commit` — the user decides when to commit
- Delete source files — they're archived, not deleted
- Run validation — that should have happened before approval
