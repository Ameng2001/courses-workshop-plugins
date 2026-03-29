# Agent Scope Model

`course-workshop-plugins` uses one shared expert source, one runtime override scope, one plugin-local scope, and one separate studio-role scope.

## Scope Layers

1. `experts/`
   - Single source of truth for reusable domain experts
   - Shared by both studio design flows and course runtime flows

2. `.workshop/agents/custom/`
   - School- or project-specific runtime experts
   - Highest runtime priority

3. `workshop-*/agents/`
   - Plugin-local experts
   - Used only when a plugin has specialized needs not suitable for the shared layer

4. `studio/roles/`
   - Studio-only workflow roles such as product manager or solution architect
   - Not loaded by course runtime skills

## Runtime Load Order

Course runtime skills should resolve experts in this order:

1. `.workshop/agents/custom/`
2. `experts/`
3. `current-plugin/agents/`

If two experts share the same filename, the earlier layer overrides the later one.

## Usage Rules

- Put reusable domain experts in `experts/`
- Put school-specific or project-specific overrides in `.workshop/agents/custom/`
- Keep `workshop-*/agents/` only for plugin-local logic
- Put plugin-design-only workflow roles in `studio/roles/`

## Typical Shared Experts

- `early-childhood-curriculum-expert.md`
- `child-development-psychologist.md`
- `instructional-designer.md`

## Design Guidance

- Prefer `experts/` before creating a plugin-local expert
- Use the custom layer for overrides, not for copying the same shared expert into every project
- A skill should explicitly state which experts are required and which scopes it scans
