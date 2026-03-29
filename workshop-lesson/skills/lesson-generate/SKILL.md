---
name: lesson-generate
description: Compile all lesson design artifacts into a standard-format lesson plan document. Use after lesson details are complete, when a teacher needs the final formatted lesson plan, or when someone says "generate the lesson plan" or "compile the lesson".
allowed-tools: Read, Write, Glob
user-invocable: true
---

# Lesson Generate

Assemble lesson objectives, scaffold, and details into a complete, standard-format lesson plan document ready for submission or classroom use.

## Pre-check

1. Read required input files from the workspace:
   - `lesson-objective.md` — learning objectives
   - `lesson-scaffold.md` — five-step structure
   - `lesson-detail.md` — detailed scripts and materials
   - If any missing, list what's missing and suggest running the corresponding skill
2. Read the output format spec from `workshop-templates/references/templates/five-step/output-format.md`

## Step 1: Assemble Basic Info

Extract and compile the header section:

```markdown
# 教案: {活动名称}

| 项目 | 内容 |
|------|------|
| 活动名称 | {name_cn} ({name_en}) |
| 适用年龄 | {age_group} ({age_range}) |
| 活动领域 | {primary_domain} + {secondary_domains} |
| 活动时长 | {duration} 分钟 |
| 活动类型 | {type} |
| 设计教师 | {teacher_name} |
| 设计日期 | {date} |
```

## Step 2: Compile Teaching Objectives

From `lesson-objective.md`, format as:

```markdown
## 教学目标

### 认知目标
1. {cognitive_1}
2. {cognitive_2}

### 技能目标
1. {skill_1}

### 情感目标
1. {affective_1}
```

## Step 3: Compile Preparation Section

From `lesson-detail.md`, aggregate the material checklist:

```markdown
## 教学准备

### 环境准备
- {space_setup}

### 材料准备
| 材料 | 数量 | 准备方式 |
|------|------|---------|
| {material_1} | {qty} | {source} |

### 经验准备
- {prior_experience_needed}
```

## Step 4: Compile Teaching Process

From `lesson-scaffold.md` and `lesson-detail.md`, generate the main teaching table:

```markdown
## 教学过程

| 环节 | 时长 | 教师行为 | 幼儿行为 | 材料 | 设计意图 |
|------|------|---------|---------|------|---------|
| **S1 导入** | {min} min | {teacher_actions} | {child_responses} | {materials} | {intent} |
| **S2 探究** | {min} min | {teacher_actions} | {child_responses} | {materials} | {intent} |
| **S3 操作** | {min} min | {teacher_actions} | {child_responses} | {materials} | {intent} |
| **S4 总结** | {min} min | {teacher_actions} | {child_responses} | {materials} | {intent} |
| **S5 延伸** | {min} min | {teacher_actions} | {child_responses} | {materials} | {intent} |
```

For each step, include the full teacher scripts from lesson-detail, formatted for readability.

## Step 5: Add Differentiation Section (if present)

```markdown
## 分层指导

| 层级 | 幼儿特征 | 指导策略 |
|------|---------|---------|
| 基础层 | {description} | {strategy} |
| 发展层 | {description} | {strategy} |
| 提高层 | {description} | {strategy} |
```

## Step 6: Add Reflection Template

```markdown
## 教学反思

> 课后填写

- **目标达成情况**:
- **幼儿表现亮点**:
- **需要改进的环节**:
- **后续跟进计划**:
```

## Step 7: Write Output

Write the complete lesson plan to `studio/changes/{workspace}/lesson-plan.md`.

Update `studio/changes/{workspace}/status.json`:
- Preserve all existing fields
- Set `skills.lesson-generate = "done"`
- Set `phase` to `reviewing`
- Ensure the workspace remains `type: "project"`

Present a summary to the user:

```
✅ 教案已生成: lesson-plan.md

📋 {活动名称} | {年龄段} | {时长}分钟
目标: {objectives_count} 条 | 环节: 5 步 | 材料: {materials_count} 项

下一步:
- /workshop-quality:standards-check — 自动质量检查
- /workshop-format:format-lesson — 格式标准化（如需要）
- /workshop-resource:resource-planner — 资源规划
```

## Out of Scope

- This skill is an assembly skill — it does NOT create new content
- It does NOT export to Word/PDF (future capability)
- It does NOT run quality checks (use workshop-quality for that)
