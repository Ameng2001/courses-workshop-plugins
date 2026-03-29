---
name: init
description: Initialize a course workshop studio in the current project for project-based, multi-methodology course development (PBL, Five-Step, etc.). Use when starting course design in a new repo, when someone says "set up workshop", or when the workspace is missing. Creates a git-tracked studio with project workspaces and knowledge base support.
allowed-tools: Read, Write, Bash, Glob
user-invocable: true
---

# Workshop Init

Initialize `studio/` directory in the current project for kindergarten course development. Supports multiple teaching methodologies (PBL, Five-Step, etc.) through pluggable templates. This directory is git-tracked — it holds project workspaces, planning records, and design documentation that have version control value.

The target users are kindergarten curriculum directors (课研主任) and classroom teachers (一线教师) who design and deliver courses.

## Pre-check

1. Check if `studio/` already exists at the project root
   - If yes: read `studio/config.yaml`, report current status, list active changes via `ls studio/changes/`, and **exit without creating anything**
   - If no: proceed with initialization
2. Confirm the current directory is a git repo (check for `.git/`). If not, warn: "studio/ is designed to be git-tracked. Consider running `git init` first." Proceed anyway if the user confirms.

## Steps

### Step 1: Create directory structure

```
studio/
├── config.yaml          # workspace configuration (written in Step 2)
├── changes/             # active project workspaces and shared planning records
│   └── .gitkeep
├── agents/              # custom domain expert definitions (override built-ins)
│   └── .gitkeep
├── kb/                  # school-specific knowledge base (managed by workshop-kb)
│   ├── textbooks/       # 区编教材
│   │   └── .gitkeep
│   ├── philosophy/      # 园本理念
│   │   └── .gitkeep
│   ├── lesson-plans/    # 历年教案
│   │   └── .gitkeep
│   ├── research-records/ # 教研记录
│   │   └── .gitkeep
│   └── calendars/       # 学期主题日历
│       └── .gitkeep
└── archive/             # completed and archived project deliverables
    └── .gitkeep
```

Create `.gitkeep` files as empty files — they ensure git tracks the empty directories.

### Step 2: Write config.yaml

Write the following content verbatim to `studio/config.yaml`:

```yaml
# Workshop Studio Configuration
# Schema: course-workshop — Multi-methodology course design workspace

schema: course-workshop

defaults:
  # Default teaching methodology for the next deliverable in a project workspace
  methodology: pbl-huamei
  # Where promoted course deliverables are placed (relative to project root)
  target_collection: courses
  # Governance: who approves project deliverables before promote
  governance:
    approval_required: true
    approver_role: curriculum-director

# Lifecycle phases for project workspaces
# Each active project in studio/changes/ progresses through these phases
lifecycle:
  phases:
    - planning      # Ideation, theme exploration, domain analysis
    - designing     # Detailed course structure, lesson design, material planning
    - reviewing     # Expert review, curriculum alignment check, team review
    - approved      # Ready to promote/ship
    - shipped       # Promoted to target directory and archived
  initial_phase: planning
```

### Step 3: Print summary

```
Workshop studio initialized at studio/

  studio/config.yaml   — studio configuration (schema: course-workshop)
  studio/changes/      — active project workspaces and shared planning records
  studio/agents/       — custom domain expert definitions
  studio/kb/           — school-specific knowledge base
  studio/archive/      — shipped project deliverables

Default methodology: pbl-huamei (华美 PBL 五步法)
This directory is git-tracked — commit it to share with your team.
```

### Step 4: Suggest next steps

- "Run `/workshop-templates:template-list` to see available teaching methodologies"
- "Run `/workshop-templates:template-select <id>` to choose a methodology"
- "Run `/workshop-kb:kb-import <path>` to import school-specific materials"
- "Run `/workshop-designer:design <theme>` to start designing a PBL course"
- "Run `/workshop-planner:semester-plan <semester>` to create a semester plan"

## Notes

- `studio/` is meant to be committed to git — it contains design decisions and rationale
- `studio/changes/` holds active project workspaces and shared planning records; `studio/archive/` holds shipped work
- The default unit of work is a course-theme project workspace with `brief.md`, `status.json`, and one or more deliverables
- A single project workspace may contain both `proposal.md` and `lesson-plan.md`
- Semester/month/week planning remains a global asset layer and should be referenced by projects instead of duplicated when possible
- Recommended metadata:
  - project workspace: `type: "project"` + `plan_refs`
  - planning workspace: `type: "planning"` + `plan_level`
