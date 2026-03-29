---
name: template-list
description: List all available teaching methodology templates with their pipeline stages and target audience. Use when a teacher or curriculum director wants to see what methodologies are supported, or when someone asks "what templates are available" or "what teaching methods can I use".
allowed-tools: Read, Glob
user-invocable: true
---

# Template List

Display all available teaching methodology templates registered in the system. Each template defines a complete design pipeline, output format, and coding convention.

## Step 1: Scan Templates

1. Glob `workshop-templates/references/templates/*/manifest.yaml`
2. For each manifest found, read and parse the YAML content

## Step 2: Build Template Overview

For each template, extract and display:

- **ID**: The template identifier
- **名称**: Chinese name
- **Name**: English name
- **描述**: One-line description
- **目标角色**: Target user roles
- **适用年龄**: Target age groups
- **时间跨度**: Time scope (lesson / week / month)
- **设计流水线**: Pipeline stages (ordered list)
- **输出类型**: Document type (proposal / lesson-plan)

## Step 3: Display

Present as a formatted comparison table:

```
┌─────────────────────────────────────────────────────────┐
│  📋 可用教学法模板 / Available Methodology Templates    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [1] pbl-huamei — 华美 PBL 五步法                       │
│      角色: 课研主任 | 周期: 月度 | 5 个设计阶段          │
│      产出: PBL 项目预案 (proposal)                      │
│                                                         │
│  [2] five-step — 五步教学法教案                         │
│      角色: 一线教师 | 周期: 单课时 | 4 个设计阶段         │
│      产出: 标准教案 (lesson-plan)                       │
│                                                         │
│  ... (additional templates as registered)               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Step 4: Guide Next Steps

After displaying the list, suggest:

> **下一步 / Next steps:**
> - 使用 `/workshop-templates:template-select {id}` 为当前工作区选择模板
> - 选择后，系统会自动路由到对应的设计流水线

## Out of Scope

- This skill does NOT create or modify templates
- This skill does NOT set the active template (use `template-select` for that)
