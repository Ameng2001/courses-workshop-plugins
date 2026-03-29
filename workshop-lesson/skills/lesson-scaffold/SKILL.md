---
name: lesson-scaffold
description: Design the five-step teaching structure (导入→探究→操作→总结→延伸) with time allocation and activity types for each step. Use after lesson objectives are set, when a teacher needs to structure a lesson, or when someone says "help me design the teaching flow".
allowed-tools: Read, Write, Glob, Agent
user-invocable: true
---

# Lesson Scaffold

Design the five-step teaching structure for a single lesson. Each step gets a time allocation, activity type, key questions, and expected child behaviors.

## Expert Discovery

1. **Primary role**: Load `instructional-designer.md` (teaching flow, time management)
2. **Secondary role**: Load `early-childhood-curriculum-expert.md` (pedagogy alignment)
3. **Scan project experts**: Glob `studio/agents/*.md`

## Pre-check

1. Verify `studio/` exists
2. Read `studio/changes/{workspace}/lesson-objective.md` — if present, use objectives as the design anchor
   - If not present, warn: "建议先运行 `/workshop-lesson:lesson-objective` 设定教学目标" but proceed if user insists
3. Read the five-step methodology guide from `workshop-templates/references/templates/five-step/methodology-guide.md`
4. Read age-appropriate time allocation from the methodology guide

## Step 1: Determine Parameters

From objectives file or user input, confirm:
- **课题**: Lesson topic
- **年龄段**: Age group (determines total duration and step time ratios)
- **教学目标**: The 3-4 objectives to address
- **主要领域**: Primary learning domain

Time allocation reference:

| 年龄段 | 总时长 | S1 导入 | S2 探究 | S3 操作 | S4 总结 | S5 延伸 |
|--------|--------|---------|---------|---------|---------|---------|
| 小班 | 15-20 min | 2-3 | 5-8 | 3-5 | 2-3 | 1-2 |
| 中班 | 20-25 min | 3-4 | 8-10 | 5-7 | 3-4 | 2 |
| 大班 | 25-30 min | 3-5 | 10-12 | 5-8 | 3-5 | 2-3 |

## Step 2: Design Five Steps

For each step, generate:

### S1 导入 / Introduction ({time} min)
- **方式**: {导入策略 — 实物/情境/问题/游戏/回顾}
- **核心问题**: {引导幼儿进入主题的开放性问题}
- **预期反应**: {幼儿可能的回应}
- **设计意图**: {为什么选择这种导入方式}

### S2 探究 / Exploration ({time} min)
- **方式**: {探究策略 — 观察/实验/讨论/调查}
- **核心问题**: {引导深入探究的关键问题，2-3 个}
- **预期反应**: {幼儿在探究中的典型行为}
- **目标对应**: {本环节主要达成哪个教学目标}

### S3 操作 / Practice ({time} min)
- **方式**: {操作策略 — 创作/练习/游戏/合作}
- **任务描述**: {幼儿需要完成的具体操作}
- **分层设计**: 基础层 / 发展层 / 提高层
- **目标对应**: {本环节主要达成哪个教学目标}

### S4 总结 / Summary ({time} min)
- **方式**: {总结策略 — 作品分享/关键提问/经验梳理}
- **核心问题**: {帮助幼儿回顾关键发现的问题}
- **目标对应**: {检验哪个教学目标}

### S5 延伸 / Extension ({time} min)
- **方式**: {延伸策略 — 区角/家园/生活/下课预告}
- **延伸内容**: {具体延伸活动或任务}

## Step 3: Objective Coverage Check

Verify every learning objective is addressed by at least one step:

| 教学目标 | 对应环节 | 达成方式 |
|---------|---------|---------|
| {objective_1} | S2 探究 | 通过观察比较达成 |
| {objective_2} | S3 操作 | 通过动手实践达成 |
| ... | ... | ... |

If any objective is not covered, adjust the step design.

## Step 4: Expert Review

Invoke instructional designer to check:
- Time allocation reasonableness for the age group
- Smooth transitions between steps
- Activity variety (not all steps are "teacher talks")
- Differentiation adequacy in S3

## Step 5: User Confirmation and Write

Present the scaffold overview. Wait for approval.

Write to `studio/changes/{workspace}/lesson-scaffold.md`.

Update `studio/changes/{workspace}/status.json`:
- Preserve all existing fields
- Set `skills.lesson-scaffold = "done"`
- If `phase` is missing, initialize it to `planning`
- If `lesson-objective.md` and `lesson-scaffold.md` both exist, `phase` may remain `planning`

Suggest next steps:
> **下一步:**
> - `/workshop-lesson:lesson-detail` — 为每个环节编写具体话术和材料清单

## Out of Scope

- This skill does NOT write detailed teacher scripts (use lesson-detail)
- This skill does NOT generate the final formatted lesson plan (use lesson-generate)
