---
name: status
description: Show the current state of all active project workspaces, shared planning records, and deliverables in progress. Use when checking progress, when someone asks "what's the status", or when resuming work.
allowed-tools: Read, Glob
user-invocable: true
---

# Workshop Status

Display a dashboard of active project workspaces, shared planning records, knowledge base status, and recent archives.

## Steps

### Step 1: Check studio/ exists

If `studio/` doesn't exist, suggest running `/workshop-core:init`.

### Step 1b: Build Status Summary

Run:

```bash
python3 workshop-core/scripts/workspace_status.py summarize-status
```

This returns a structured summary containing:
- default methodology
- knowledge base counts
- planning workspaces
- project workspaces
- recent archives

If no active workspaces exist, show "No active work".

### Step 4: Display dashboard

Format as a table:

```
Workshop Status
═══════════════

📋 Default Methodology: pbl-huamei (华美 PBL 五步法)

📚 Knowledge Base (studio/kb/)
  区编教材: 3 | 园本理念: 1 | 历年教案: 12 | 教研记录: 5 | 学期日历: 2
  (Run /workshop-kb:kb-index to refresh)

📅 Planning Records
  2026-spring   semester   linked: 2 projects
  april-2026    month      linked: 1 project

Projects (studio/changes/)
┌──────────────────┬────────────┬──────────────┬────────────────┬────────────────────┬──────────────────┐
│ Project          │ Phase      │ Methodology  │ Skills         │ Deliverables       │ Plan Refs        │
├──────────────────┼────────────┼──────────────┼────────────────┼────────────────────┼──────────────────┤
│ spring-flowers   │ reviewing  │ five-step    │ 4/4 done       │ lesson-plan        │ week: week-2     │
│ weather-watch    │ approved   │ pbl-huamei   │ 7/7 done       │ proposal, review   │ month: april     │
│ garden-life      │ designing  │ pbl-huamei   │ 4/7 done       │ proposal draft     │ —                │
└──────────────────┴────────────┴──────────────┴────────────────┴────────────────────┴──────────────────┘

Recently Shipped (studio/archive/)
  2026-03-25-animal-friends → courses/animal-friends
  2026-03-18-color-lab      → courses/color-lab
```

### Step 5: Suggest next actions

Based on current state, suggest what to do next:
- If a project is `approved`: "Run `/workshop-core:promote {name}` to ship its deliverables"
- If a project is `designing` with `pbl-huamei`: "Continue with `/workshop-designer:design {name}`"
- If a project is `designing` with `five-step`: "Continue with `/workshop-lesson:lesson {name}`"
- If a project is `reviewing`: "Complete the review, then set phase to approved"
- If a project is `planning`: "Choose the template for the next deliverable with `/workshop-templates:template-select`"
- If no active changes: "Run `/workshop-templates:template-list` to see methodologies, or `/workshop-planner:semester-plan` to plan a semester"
- If knowledge base is empty: "Run `/workshop-kb:kb-import <path>` to import school materials"

## Notes

- This skill is read-only — it does NOT modify any files or state
- Skill status breakdown reads the `skills` object from each workspace's `status.json`
- Phase values follow the lifecycle defined in `studio/config.yaml`: planning → designing → reviewing → approved → shipped
- Project workspaces are the primary unit of work; planning records are displayed as shared context
- `status.json.type` is authoritative when present; filename heuristics are fallback only
- `workspace_status.py summarize-status` is the canonical aggregation path for this dashboard
