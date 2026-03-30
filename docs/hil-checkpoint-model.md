# Human-in-the-Loop Checkpoint Model

`course-workshop-plugins` treats major workflow handoff points as explicit human-in-the-loop (HIL) checkpoints.

The goal is not to let the system silently flow from setup to shipped deliverables. Instead, major transitions should pause for human confirmation.

## 1. Core Principle

At every major stage boundary:

1. the system generates or updates artifacts
2. a human reviews the result
3. only after confirmation does the workflow move to the next major stage

## 2. Standard Checkpoints

### A. `project-framing`

Purpose:
- confirm the project is correctly framed before deep design starts

Typical inputs:
- pipeline selection
- project naming
- age group
- plan linking

Typical outcome:
- project is ready to enter design work

### B. `design-scaffold`

Purpose:
- confirm the design backbone is sound before detailed content generation

Examples:
- PBL: driving question, network map, inquiry clues
- lesson: objectives and five-step scaffold
- planning: semester/month/week structure

Typical outcome:
- direction is approved for full artifact generation

### C. `deliverable-draft`

Purpose:
- confirm the first complete draft is ready to enter review

Examples:
- `proposal.md`
- `lesson-plan.md`

Typical outcome:
- draft enters quality check and expert review

### D. `approval-gate`

Purpose:
- confirm the reviewed deliverable is approved for shipping

Examples:
- review comments complete
- quality checks complete
- curriculum director approves

Typical outcome:
- workspace can move from `reviewing` to `approved`

## 3. Suggested Status Shape

Project workspaces should reserve a `hil` field in `status.json`:

```json
{
  "hil": {
    "checkpoint": "design-scaffold",
    "status": "awaiting_review",
    "requested_at": "2026-03-29T10:00:00+08:00",
    "approved_at": null,
    "approved_by": null,
    "notes": ""
  }
}
```

## 4. Allowed Values

### `hil.checkpoint`

- `project-framing`
- `design-scaffold`
- `deliverable-draft`
- `approval-gate`

### `hil.status`

- `not_started`
- `awaiting_review`
- `changes_requested`
- `approved`

## 5. Relationship to Phase

`phase` remains the high-level lifecycle:

- `planning`
- `designing`
- `reviewing`
- `approved`
- `shipped`

`hil` gives the finer-grained human gate inside that lifecycle.

Recommended mapping:

| Phase | Typical HIL checkpoint |
|------|-------------------------|
| `planning` | `project-framing` |
| `designing` | `design-scaffold` |
| `reviewing` | `deliverable-draft` or `approval-gate` |
| `approved` | `approval-gate: approved` |

## 6. Command Expectations

- `init` should not create a HIL state
- `config` should not create a HIL state
- `onboarding` may recommend the first HIL gate but should not auto-approve it
- artifact-producing skills should present results and wait for confirmation at the relevant checkpoint
- `approve` is the explicit HIL command for the final approval gate

## 7. Implementation Guidance

Short term:
- keep HIL as a documentation and status-field contract

Next step:
- add helper commands that update `hil.checkpoint` and `hil.status`

Long term:
- make core transitions reject auto-progression unless the required HIL gate is approved
