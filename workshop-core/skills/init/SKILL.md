---
name: init
description: Initialize a course workshop runtime in the current project for project-based, multi-methodology course development (PBL, Five-Step, etc.). Use when starting course design in a new repo, when someone says "set up workshop", or when the workspace is missing. Creates a git-tracked `.workshop/` runtime with project workspaces and knowledge base support.
allowed-tools: Read, Write, Bash, Glob
user-invocable: true
---

# Workshop Init

Initialize `.workshop/` in the current project for kindergarten course development. Supports multiple teaching methodologies (PBL, Five-Step, etc.) through pluggable templates. This directory is git-tracked — it holds runtime project workspaces, planning records, custom experts, and knowledge assets. `studio/` remains reserved for Astra Studio plugin development.

The target users are kindergarten curriculum directors (课研主任) and classroom teachers (一线教师) who design and deliver courses.

## Pre-check

1. Check if `.workshop/` already exists at the project root
   - If yes: read `.workshop/config.yaml`, report current status, list active projects via `ls .workshop/projects/`, and **exit without creating anything**
   - If no: proceed with initialization
2. Confirm the current directory is a git repo (check for `.git/`). If not, warn: "`.workshop/` is designed to be git-tracked. Consider running `git init` first." Proceed anyway if the user confirms.

## Steps

### Step 1: Create directory structure

```
.workshop/
├── config.yaml          # runtime configuration (written in Step 2)
├── projects/            # active course-theme project workspaces
│   └── .gitkeep
├── plans/               # shared semester / month / week planning workspaces
│   └── .gitkeep
├── agents/              # runtime expert definitions
│   └── custom/          # school/project custom experts
│       └── .gitkeep
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
└── archive/             # shipped and archived project deliverables
    └── .gitkeep
```

Create `.gitkeep` files as empty files — they ensure git tracks the empty directories.

### Step 2: Write config.yaml

Write the following content verbatim to `.workshop/config.yaml`:

```yaml
# Course Workshop Runtime Configuration
# Schema: course-workshop — Multi-methodology course runtime

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
# Each active project in .workshop/projects/ progresses through these phases
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
Course workshop runtime initialized at .workshop/

  .workshop/config.yaml   — runtime configuration (schema: course-workshop)
  .workshop/projects/     — active project workspaces
  .workshop/plans/        — shared planning records
  .workshop/agents/custom/ — school/project custom experts
  .workshop/kb/           — school-specific knowledge base
  .workshop/archive/      — shipped project deliverables

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

- `.workshop/` is meant to be committed to git — it contains runtime project state with collaboration value
- `studio/` remains the Astra Studio plugin-development workspace and should not be used as the runtime home for course projects
- `.workshop/projects/` holds active project workspaces; `.workshop/plans/` holds shared planning records; `.workshop/archive/` holds shipped work
- `experts/` stores reusable domain experts shared across studio and runtime
- `.workshop/agents/custom/` stores school- or project-specific experts and has the highest override priority at runtime
- `workshop-*/agents/` remains available for plugin-local experts that should not be promoted to platform-wide shared use
- `studio/roles/` stores plugin-design-only workflow roles such as product manager or solution architect
- The default unit of work is a course-theme project workspace with `brief.md`, `status.json`, and one or more deliverables
- A single project workspace may contain both `proposal.md` and `lesson-plan.md`
- Semester/month/week planning remains a global asset layer and should be referenced by projects instead of duplicated when possible
- Recommended metadata:
  - project workspace: `type: "project"` + `plan_refs`
  - planning workspace: `type: "planning"` + `plan_level`
