# Skill Map: workshop-templates

> Date: 2026-03-29

## Skills

### template-list
- **Description**: List all available teaching methodology templates with pipeline info
- **Inputs**: (none)
- **Outputs**: Terminal summary of all registered templates
- **Complexity**: Simple
- **allowed-tools**: Read, Glob

### template-select
- **Description**: Select and activate a methodology template for the current workspace
- **Inputs**: template ID
- **Outputs**: Updates workspace config.yaml with selected methodology
- **Complexity**: Simple
- **allowed-tools**: Read, Write, Glob

## Data Flow

```
template-list → (user picks) → template-select → updates config
                                                       ↓
                                               (workshop-designer or
                                                workshop-lesson reads)
```

## Implementation Order

1. **template-list** — discovery
2. **template-select** — activation
