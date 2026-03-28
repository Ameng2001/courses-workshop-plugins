---
name: init
description: Initialize a course workshop workspace in the current project for PBL course development. Use when starting course design in a new repo, when someone says "set up workshop", or when the workspace is missing. Creates a git-tracked workspace.
allowed-tools: Read, Write, Bash, Glob
user-invocable: true
---

# Workshop Init

Initialize `studio/` directory in the current project for PBL (Project-Based Learning) course development. This directory is git-tracked — it holds course design documentation (briefs, proposals, status) that has version control value.

The target user is a kindergarten curriculum director (课研主任) who manages course design workflows from ideation through approval and shipping.

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
├── changes/             # active course design workspaces (one dir per domain or plugin)
│   └── .gitkeep
├── agents/              # custom domain expert definitions (override built-ins)
│   └── .gitkeep
└── archive/             # completed and archived proposal records
    └── .gitkeep
```

Create `.gitkeep` files as empty files — they ensure git tracks the empty directories.

### Step 2: Write config.yaml

Write the following content verbatim to `studio/config.yaml`:

```yaml
# Workshop Studio Configuration
# Schema: pbl-course — PBL (Project-Based Learning) course design workspace

schema: pbl-course

defaults:
  # Where promoted proposals are placed (relative to project root)
  target_collection: courses
  # Governance: who approves proposals before promote
  governance:
    approval_required: true
    approver_role: curriculum-director

# Lifecycle phases for course proposals
# Each proposal in studio/changes/ progresses through these phases
lifecycle:
  phases:
    - planning      # Ideation, theme exploration, domain analysis
    - designing     # Detailed course structure, activity design, material planning
    - reviewing     # Expert review, curriculum alignment check
    - approved      # Ready to promote/ship
    - shipped       # Promoted to target directory and archived
  initial_phase: planning
```

### Step 3: Print summary

```
Workshop studio initialized at studio/

  studio/config.yaml   — workspace configuration (schema: pbl-course)
  studio/changes/      — active course design workspaces
  studio/agents/       — custom domain expert definitions
  studio/archive/      — shipped proposal records

This directory is git-tracked — commit it to share with your team.
```

### Step 4: Suggest next steps

- "Run `/workshop-designer:design <theme>` to start designing your first PBL course"
- "Or create a workspace manually: `mkdir studio/changes/my-course`"

## Notes

- `studio/` is meant to be committed to git — it contains design decisions and rationale
- `studio/changes/` holds active work; `studio/archive/` holds shipped work
- Each course proposal gets its own directory under `changes/` with brief.md, status.json, and design drafts
- Domain workspaces (type: "domain") can hold shared analysis across multiple course proposals
- Plugin workspaces (type: "plugin") hold individual course proposal designs
