# Release Bundle Model

`courses/` is the release bundle directory for shipped course outputs.

It is **not**:
- the active project workspace
- the full design history
- a mirror of `.workshop/archive/`

## Directory Roles

- `.workshop/projects/`
  - active project workspaces
  - draft artifacts, intermediate files, HIL state, and in-progress collaboration
- `.workshop/archive/`
  - full historical project record after ship
  - complete traceability and audit trail
- `courses/`
  - final course release bundle for local consumption or later remote publishing

## What Belongs in `courses/`

Main deliverables:
- `proposal.md`
- `lesson-plan.md`

Optional supporting deliverables:
- `resource-plan.md`
- `quality-report.md`
- `review-comments.md`
- `resource-check-report.md`

Conditional structured attachment:
- `activities/` when the project ships a PBL proposal and the activity cards are part of the release bundle

## What Does Not Belong in `courses/`

Design-process artifacts stay in `.workshop/archive/`, for example:
- `theme-analysis.md`
- `prior-knowledge.md`
- `competency-mapping.md`
- `driving-question.md`
- `network-map.md`
- `inquiry-clues.md`
- `lesson-objective.md`
- `lesson-scaffold.md`
- `lesson-detail.md`

## Rationale

This separation keeps the shipped output small and clear:
- `courses/` serves consumers
- `.workshop/archive/` serves governance, traceability, and future revision

If the project later publishes to COS, S3, or another MCP-backed target, the remote target should receive the same release bundle semantics by default.

## Relationship to Export Layer

`courses/` is still the shipped release bundle, but it is not the same thing as a client-specific export package.

- `courses/` keeps the final canonical deliverables
- `.workshop/exports/` can prepare:
  - Word-ready bundles
  - PDF-ready bundles
  - client-specific layout packages

This keeps:
- release semantics stable
- export styling customizable
