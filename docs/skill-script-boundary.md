# Skill Script Boundary

This document defines which parts of the system should be implemented through shared scripts/helpers, and which parts must remain flexible in skills and human review.

The goal is to avoid two failure modes:
- too much free-form execution, which causes state drift and inconsistent runtime behavior
- too much hard-coded workflow logic, which makes course design rigid and brittle

## Core Rule

- scripts handle deterministic runtime mechanics
- skills handle course reasoning, content generation, and user interaction

In short:
- structure, status, validation, shipping = scriptable
- design thinking, pedagogy, iteration, review = flexible

## 1. What Should Be Scripted

These responsibilities should be centralized in helpers or scripts whenever possible.

### 1.1 Runtime structure

- locating `.workshop/projects/{name}`
- locating `.workshop/plans/{name}`
- creating minimal runtime directories
- creating minimal `status.json`
- creating minimal `config.yaml`

### 1.2 State updates

- writing `skills.*`
- writing `phase`
- writing `hil.*`
- writing `plan_refs`
- writing `linked_projects`
- writing `approved_at`, `approved_by`, `shipped_at`, `shipped_to`

### 1.3 Validation

- required file presence checks
- workspace type checks
- phase precondition checks
- deliverable precondition checks
- promote readiness checks

### 1.4 Shipping and archive

- release bundle assembly
- archive move
- local target write
- future remote target dispatch

### 1.5 Dashboard and summaries

- status aggregation
- HIL overview
- archive summaries
- structured JSON output for automation or future integrations

## 2. What Must Stay Flexible

These parts should remain in skill logic plus human-in-the-loop review.

### 2.1 Course reasoning

- theme interpretation
- prior knowledge analysis
- competency mapping
- methodology choice in context

### 2.2 Design generation

- driving question writing
- inquiry clue decomposition
- network-map structuring
- lesson objective drafting
- lesson scaffold design
- activity design
- proposal writing

### 2.3 Review judgment

- whether a design direction is good enough
- whether a draft should be revised
- how reviewer comments are resolved
- how a school adapts the workflow to local practice

### 2.4 Human collaboration

- user confirmation points
- changes requested after review
- choosing between multiple acceptable design options

## 3. Plugin-by-Plugin Boundary

### 3.1 `workshop-core`

Should be mostly scripted:
- init
- config
- onboarding summary
- status
- HIL state management
- approve
- promote
- archive

Skills remain responsible for:
- explaining results
- guiding user next steps

### 3.2 `workshop-templates`

Should script:
- pipeline selection writeback
- project config initialization
- project-framing HIL request

Should remain flexible:
- recommendation of which pipeline is best for a given context

### 3.3 `workshop-planner`

Should script:
- planning workspace initialization
- `status.json` writeback
- linked project updates

Should remain flexible:
- semester/month/week plan content generation

### 3.4 `workshop-insight`

Should script:
- required input checks
- project skill completion writeback

Should remain flexible:
- theme analysis
- prior knowledge interpretation
- competency mapping content

### 3.5 `workshop-designer`

Should script:
- phase progression
- design-scaffold HIL request/approval
- deliverable-draft HIL request/approval
- proposal delivery validation

Should remain flexible:
- driving question
- network map
- inquiry clues
- activities
- proposal content

### 3.6 `workshop-lesson`

Should script:
- phase progression
- design-scaffold HIL request/approval
- deliverable-draft HIL request/approval

Should remain flexible:
- lesson objectives
- lesson scaffold content
- detailed scripts
- final lesson plan wording

### 3.7 `workshop-quality`

Should script:
- review artifact writeback
- quality result status recording
- approval-gate preparation signals

Should remain flexible:
- review comments
- expert judgment
- standards interpretation in edge cases

### 3.8 `workshop-resource`

Should script:
- resource output paths
- resource check result writeback

Should remain flexible:
- resource estimation
- categorization judgment
- substitutions and local adjustments

## 4. Priority Order for Future Scripting

Recommended next scripting priorities:

1. `workshop-templates`
   - make project initialization and framing writeback fully script-driven
2. `workshop-planner`
   - make planning initialization and link behavior fully script-driven
3. `workshop-lesson` and `workshop-designer`
   - script common phase/HIL transitions
4. `workshop-quality` and `workshop-resource`
   - script review/result writeback

## 5. Anti-Patterns

Avoid these:

- writing ad-hoc `status.json` fields directly inside many different skills
- duplicating HIL logic in multiple skills
- hard-coding course design decisions into scripts
- turning design generation into rigid templates with no room for review or revision
- copying full project workspaces into `courses/`

## 6. Summary

The system should be built in two layers:

- scripts for runtime consistency
- skills for pedagogical intelligence

This preserves flexibility where course design needs judgment, while making the runtime reliable enough for collaboration, testing, and future cloud publishing.
