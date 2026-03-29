---
name: status
description: Show the current state of all course design workspaces — proposals and lesson plans in progress, their phase, active methodology, and what's next. Use when checking progress, when someone asks "what's the status", or when resuming work.
allowed-tools: Read, Glob
user-invocable: true
---

# Workshop Status

Display a dashboard of all active course design workspaces, knowledge base status, and recent archives.

## Steps

### Step 1: Check studio/ exists

If `studio/` doesn't exist, suggest running `/workshop-core:init`.

### Step 1b: Check Knowledge Base

1. Check if `studio/kb/` exists
2. If yes: count documents per category by globbing `studio/kb/{category}/*.md` (excluding .gitkeep)
3. If `studio/kb/index.yaml` exists, read its `stats` section for summary
4. Show knowledge base status in the dashboard

### Step 1c: Check Active Methodology

1. Read `studio/config.yaml` — extract `defaults.methodology` (global default)
2. For each active workspace, check `studio/changes/{name}/config.yaml` for workspace-specific methodology override

### Step 2: Scan active changes

For each directory in `studio/changes/` (excluding `.gitkeep`):
1. Read `status.json` — if missing, show the entry with phase "unknown"
2. Read `config.yaml` — if present, show the workspace's active methodology
3. Check `type` field to distinguish workspace types:
   - `"type": "domain"` — domain-level workspace (theme exploration, domain analysis). Show domain name and its `plugins` list (the course proposals it spawned).
   - `"type": "plugin"` (or no `type` field for legacy) — plugin-level workspace (individual course proposal). Show proposal name, phase, skill completion, methodology, target.
4. For plugin workspaces: extract proposal name, phase, target_collection, methodology, skill statuses. Calculate completion: count skills with status `done` or `approved` vs total.
5. Check for planning artifacts: `semester-plan.md`, `month-plan.md`, `week-plan.md` — if present, show planning status.

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

📋 Default Methodology: pbl-huamei (华美 PBL 五步法)

📚 Knowledge Base (studio/kb/)
  区编教材: 3 | 园本理念: 1 | 历年教案: 12 | 教研记录: 5 | 学期日历: 2
  (Run /workshop-kb:kb-index to refresh)

📅 Planning (if semester-plan.md / month-plan.md exist)
  学期计划: 2026-春季 (4 月主题: 春天的花)
  月度计划: 3月已完成, 4月进行中

Domains (studio/changes/)
  nature-exploration    planning    proposals: seasons-pbl, garden-life

Proposals & Lesson Plans (studio/changes/)
┌──────────────────┬────────────┬──────────────┬────────────────┬──────────────┐
│ Workspace        │ Phase      │ Methodology  │ Skills         │ Target       │
├──────────────────┼────────────┼──────────────┼────────────────┼──────────────┤
│ seasons-pbl      │ designing  │ pbl-huamei   │ 2/5 done       │ courses/     │
│ spring-flowers   │ designing  │ five-step    │ 1/4 done       │ courses/     │
│ weather-watch    │ approved   │ pbl-huamei   │ 4/4 done       │ courses/     │
└──────────────────┴────────────┴──────────────┴────────────────┴──────────────┘

Recently Shipped (studio/archive/)
  2026-03-25-animal-friends → courses/animal-friends
  2026-03-18-color-lab      → courses/color-lab
```

### Step 5: Suggest next actions

Based on current state, suggest what to do next:
- If a proposal is `approved`: "Run `/workshop-core:promote {name}` to ship it"
- If a proposal is `designing` with `pbl-huamei`: "Continue with `/workshop-designer:design {name}`"
- If a proposal is `designing` with `five-step`: "Continue with `/workshop-lesson:lesson {name}`"
- If a proposal is `reviewing`: "Complete the review, then set phase to approved"
- If a proposal is `planning`: "Choose a methodology with `/workshop-templates:template-select` then start design"
- If no active changes: "Run `/workshop-templates:template-list` to see methodologies, or `/workshop-planner:semester-plan` to plan a semester"
- If knowledge base is empty: "Run `/workshop-kb:kb-import <path>` to import school materials"

## Notes

- This skill is read-only — it does NOT modify any files or state
- Skill status breakdown counts files in the workspace's `skills/` directory
- Phase values follow the lifecycle defined in `studio/config.yaml`: planning → designing → reviewing → approved → shipped
