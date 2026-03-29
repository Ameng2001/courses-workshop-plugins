---
name: template-select
description: Set the active teaching methodology template for the next deliverable in the current project workspace. Use when a user wants to choose a methodology (PBL, Five-Step, etc.) before starting course design, or when someone says "I want to use five-step method" or "switch to PBL".
allowed-tools: Read, Write, Glob
user-invocable: true
---

# Template Select

Set the active teaching methodology template for the next deliverable in the current project workspace. The selected template determines which design pipeline to use, what output format to generate, and which coding convention to follow. A single project may use different templates for different deliverables over time.

## Pre-check

1. Verify `.workshop/` exists. If not, tell the user to run `/workshop-core:init` first.
2. Determine the workspace path:
   - If `$ARGUMENTS` contains a recognized template ID, use it directly
   - Otherwise, list available templates and ask the user to choose

## Step 1: Validate Template ID

1. Read the user's requested template ID from `$ARGUMENTS`
2. Check if `workshop-templates/references/templates/{id}/manifest.yaml` exists
3. If not found:
   - Run template-list logic to show available options
   - Ask the user to pick one

## Step 2: Read Template Manifest

1. Read `workshop-templates/references/templates/{id}/manifest.yaml`
2. Parse the manifest and extract key fields:
   - `id`, `name`, `pipeline.plugin`, `output.document_type`, `coding.prefix`

## Step 3: Determine Project Workspace

1. If a project workspace is already active (check `.workshop/projects/*/status.json` for `phase: "designing"`), use that workspace
2. If no active workspace, ask the user:

> **请指定项目：**
> - 输入一个主题名称创建新项目工作区（如"春天的花"）
> - 或输入已有项目工作区名称

## Step 4: Write Configuration

1. Read `.workshop/projects/{workspace}/config.yaml` (or create if not exists)
2. Set or update the default methodology fields for the next deliverable:

```yaml
methodology: {template-id}
methodology_name: {template-name}
pipeline_plugin: {pipeline-plugin}
document_type: {document-type}
```

3. Write the updated config back
4. Clarify to the user that this sets the current default for the next deliverable, not an exclusive project-wide lock
5. If `.workshop/projects/{workspace}/status.json` does not exist, create a minimal project status file:

```json
{
  "type": "project",
  "project": "{workspace}",
  "theme": "{workspace or user-provided theme}",
  "target_collection": "courses",
  "phase": "planning",
  "created_at": "{ISO-8601}",
  "plan_refs": {
    "semester": null,
    "month": null,
    "week": null
  },
  "skills": {}
}
```

## Step 5: Confirm and Guide

Display confirmation:

```
✅ 已选择模板: {name} ({id})

设计流水线: {pipeline.plugin}
  {stage-1-name} → {stage-2-name} → ... → {final-stage-name}

输出格式: {document_type}
编码前缀: {coding.prefix}

下一步:
- PBL 预案设计: /workshop-designer:design {theme}
- 五步法教案设计: /workshop-lesson:lesson {theme}
- 层级规划: /workshop-planner:semester-plan {semester}
```

## Out of Scope

- This skill does NOT run the design pipeline — it only sets the default template for the next deliverable
- This skill does NOT create templates — it selects from existing ones
- This skill does NOT modify template content
