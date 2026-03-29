---
name: lesson-detail
description: Write detailed teacher scripts, material lists, and differentiation strategies for each teaching step. Use after the lesson scaffold is designed, when a teacher needs concrete "what to say and do" for each step, or when someone says "flesh out the lesson details".
allowed-tools: Read, Write, Glob, Agent
user-invocable: true
---

# Lesson Detail

Flesh out each teaching step with concrete teacher scripts (话术), material lists, child response predictions, and differentiation strategies. This is where the lesson becomes classroom-ready.

## Expert Discovery

1. **Primary role**: Load `instructional-designer.md` (classroom feasibility, teacher scripts)
2. **Secondary role**: Load `child-development-psychologist.md` (age-appropriate language)
3. **Scan project experts**: Glob `studio/agents/*.md`

## Pre-check

1. Read `studio/changes/{workspace}/lesson-scaffold.md` — required input
   - If not found: "请先运行 `/workshop-lesson:lesson-scaffold` 设计教学环节结构"
2. Read `studio/changes/{workspace}/lesson-objective.md` for objectives
3. Read coding spec from template: `workshop-templates/references/templates/five-step/coding-spec.md`

## Step 1: Detail Each Step

For each of the 5 steps in the scaffold, generate:

### Teacher Actions (教师行为)

Write **specific, verbatim teacher scripts**:
- Opening lines (第一句话怎么说)
- Key questions (each question written out in full, with follow-up prompts)
- Transition phrases between sub-activities
- Response strategies for common child answers (预设回应)

**Script quality rules:**
- Use child-friendly language appropriate for the age group
- Questions are open-ended, not yes/no
- Include wait time reminders ("给孩子 5 秒钟思考时间")
- Each step has 3-5 concrete teacher actions

### Child Responses (幼儿行为)

Predict what children will likely do/say:
- Expected correct responses
- Common misconceptions or unexpected answers
- Non-verbal behaviors to observe

### Materials (材料)

For each step, list specific materials:
- Name + quantity + specification (e.g., "A4 白纸 25 张" not "纸若干")
- Source: classroom stock / need to prepare / PBL Box
- Setup instructions (when to distribute, how to arrange)

### Design Intent (设计意图)

For each step, explain the pedagogical purpose in 1-2 sentences.

### Differentiation (分层指导)

For S2 (Exploration) and S3 (Practice), provide 3 tiers:

| 层级 | 特征 | 调整策略 |
|------|------|---------|
| 基础层 | 需要更多支持 | {降低难度, 增加示范, 一对一指导} |
| 发展层 | 大部分幼儿 | {标准任务, 开放性指引} |
| 提高层 | 能力较强 | {延伸任务, 创新挑战} |

## Step 2: Activity Coding

Assign codes to each activity within each step:

- S1 导入: `FS-S1-01` (usually just one activity)
- S2 探究: `FS-S2-01`, `FS-S2-02` (may have 2 sub-activities)
- S3 操作: `FS-S3-01`
- S4 总结: `FS-S4-01`
- S5 延伸: `FS-S5-01`

## Step 3: Compile Material Checklist

Aggregate all materials across all steps into a single preparation checklist:

| # | 材料名称 | 数量 | 用于环节 | 准备方式 |
|---|---------|------|---------|---------|
| 1 | {material} | {qty} | S{n} | 提前一天准备 / 当天准备 / 常备 |

## Step 4: Expert Review

Invoke instructional designer to check:
- Scripts are natural, not robotic
- Materials are specific and complete
- Differentiation is practical (not just "降低难度" with no detail)
- Total material prep time is reasonable

## Step 5: User Confirmation and Write

Present the detailed lesson. Wait for approval.

Write to `studio/changes/{workspace}/lesson-detail.md`.

Update `studio/changes/{workspace}/status.json`:
- Preserve all existing fields
- Set `skills.lesson-detail = "done"`
- If `lesson-objective.md`, `lesson-scaffold.md`, and `lesson-detail.md` all exist, set `phase` to `designing`

Suggest next steps:
> **下一步:**
> - `/workshop-lesson:lesson-generate` — 编译为标准教案格式

## Out of Scope

- This skill does NOT generate the final formatted document (use lesson-generate)
- This skill does NOT create multimedia materials (PPT, images, etc.)
