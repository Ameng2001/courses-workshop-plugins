---
name: status
description: Show the current state of all PBL course design workspaces — which proposals are in progress, their phase, and what's next. Use when checking progress, when someone asks "what's the status", or when resuming work.
allowed-tools: Read, Glob
user-invocable: true
---

# Workshop Status

Display a dashboard of all active course design workspaces and recent archives.

## Steps

### Step 1: Check studio/ exists

If `studio/` doesn't exist, suggest running `/workshop-core:init`.

### Step 2: Scan active changes

For each directory in `studio/changes/` (excluding `.gitkeep`):
1. Read `status.json` — if missing, show the entry with phase "unknown"
2. Check `type` field to distinguish workspace types:
   - `"type": "domain"` — domain-level workspace (theme exploration, domain analysis). Show domain name and its `plugins` list (the course proposals it spawned).
   - `"type": "plugin"` (or no `type` field for legacy) — plugin-level workspace (individual course proposal). Show proposal name, phase, skill completion, target.
3. For plugin workspaces: extract proposal name, phase, target_collection, skill statuses. Calculate completion: count skills with status `done` or `approved` vs total.

If `studio/changes/` is empty (only `.gitkeep`), note "No active work" and skip to Step 3.

### Step 3: Scan recent archives

List the 5 most recent directories in `studio/archive/` by name (date-prefixed).
For each, read `status.json` to get `shipped_to` path if available.

If `studio/archive/` is empty, note "No shipped proposals yet".

### Step 4: Display dashboard

Format as a table:

```
Workshop Status
═══════════════

Domains (studio/changes/)
  nature-exploration    planning    proposals: seasons-pbl, garden-life, weather-watch

Proposals (studio/changes/)
┌──────────────────┬────────────┬────────────────┬───────────────────┐
│ Proposal         │ Phase      │ Skills         │ Target            │
├──────────────────┼────────────┼────────────────┼───────────────────┤
│ seasons-pbl      │ designing  │ 2/5 done       │ courses/          │
│ garden-life      │ planning   │ 0/3 draft      │ courses/          │
│ weather-watch    │ approved   │ 4/4 done       │ courses/          │
└──────────────────┴────────────┴────────────────┴───────────────────┘

Recently Shipped (studio/archive/)
  2026-03-25-animal-friends → courses/animal-friends
  2026-03-18-color-lab      → courses/color-lab
```

### Step 5: Suggest next actions

Based on current state, suggest what to do next:
- If a proposal is `approved`: "Run `/workshop-core:promote {name}` to ship it"
- If a proposal is `designing`: "Continue designing with `/workshop-designer:design {name}`"
- If a proposal is `reviewing`: "Complete the review, then set phase to approved"
- If a proposal is `planning`: "Continue with `/workshop-designer:design {name}` to move into design"
- If no active changes: "Run `/workshop-designer:design <theme>` to start a new course"

## Notes

- This skill is read-only — it does NOT modify any files or state
- Skill status breakdown counts files in the workspace's `skills/` directory
- Phase values follow the lifecycle defined in `studio/config.yaml`: planning → designing → reviewing → approved → shipped
