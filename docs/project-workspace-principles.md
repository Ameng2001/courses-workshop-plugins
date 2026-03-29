# Project Workspace Principles

`course-workshop-plugins` uses **project workspace** as its primary working model.

## Core Rules

1. A project workspace represents one concrete course theme.
2. Users should enter through a project, not through a plugin list.
3. A single project can contain multiple deliverables:
   - `proposal.md`
   - `lesson-plan.md`
   - resource planning outputs
   - quality and review outputs
4. Templates are output-scoped defaults. They do not permanently lock a project to one methodology.
5. Semester, month, and week plans are global reusable assets. Projects should reference them rather than copy full plans.
6. Planning and course design have weak dependency: either may start first, but they should be linkable once both exist.
7. `workshop-*` directories are the only source of truth for runtime implementation.
8. `.workshop/` is the runtime home for course projects, planning records, knowledge assets, and archives.
9. `studio/` remains the Astra Studio plugin-development workspace and must not be used as the runtime home for course projects.
10. Runtime experts use layered scope: `.workshop/agents/custom` → `experts/` → `workshop-*/agents`.
11. `studio/roles/` is reserved for plugin-design-only workflow roles and is not part of runtime expert loading.

## Practical Consequences

- `workshop-core` manages project workspaces and shipped deliverables.
- `workshop-planner` produces global planning records that later projects may reference.
- `workshop-kb` provides shared school knowledge context.
- `workshop-templates` decides the pipeline and output format for the next deliverable.
- `workshop-designer`, `workshop-lesson`, `workshop-resource`, `workshop-quality`, and `workshop-insight` operate as project capabilities.
- Runtime storage should prefer:
  - `.workshop/projects/`
  - `.workshop/plans/`
  - `.workshop/agents/custom/`
  - `experts/`
  - `.workshop/kb/`
  - `.workshop/archive/`

## Non-Goals

- This principle does not make a plugin the primary user-facing object.
