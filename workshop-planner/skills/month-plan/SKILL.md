---
name: month-plan
description: Break a monthly theme into 3-4 weekly sub-themes with methodology selection and learning focus for each week. This produces a shared planning record that project workspaces can later reference.
allowed-tools: Read, Write, Glob, Agent
user-invocable: true
---

# Month Plan

Break a monthly theme from the semester calendar into weekly sub-themes with methodology assignments and focus areas. This is a global planning asset, not a project deliverable by itself.

## Expert Discovery

1. **Primary role**: Load `early-childhood-curriculum-expert.md`
2. **Scan project experts**: Glob `studio/agents/*.md`

## Pre-check

1. Verify `studio/` exists
2. Look for `studio/changes/{workspace}/semester-plan.md` — if present, read it to get the month's theme, age group, and allocated methodology
3. Check knowledge base for related materials: `studio/kb/lesson-plans/*.md` with matching theme tags

## Step 1: Gather Context

If semester-plan exists, auto-populate from it. Otherwise ask:

> **请提供以下信息：**
> 1. **月度主题**: 本月的教学主题（如"春天的花"）
> 2. **年龄段**: 小班/中班/大班
> 3. **可用周数**: 通常 3-4 周
> 4. **教学法偏好**: PBL / 五步法 / 混合

## Step 2: Design Weekly Structure

For each week, generate:

```
Week {N}: {子主题名称}
  Focus: {本周教学重点}
  Methodology: {pbl-huamei / five-step / mixed}
  Domains: {核心领域}
  Key Activities:
    - {活动1概要}
    - {活动2概要}
    - {活动3概要}
  Materials Preview: {本周关键材料}
```

### 周次递进逻辑

- **第 1 周**: 感知导入 — 建立主题认知，激发兴趣（偏五步法）
- **第 2 周**: 深入探究 — 核心探究活动，多领域整合（偏 PBL 或五步法）
- **第 3 周**: 操作实践 — 巩固经验，动手创造（偏五步法或 PBL 线索 2-3）
- **第 4 周**: 展示总结 — 成果呈现，经验分享（可选，视主题复杂度）

## Step 3: Methodology Assignment

For each week, recommend a methodology and explain why:

| 周次 | 推荐教学法 | 理由 |
|------|-----------|------|
| Week 1 | five-step | 单课时导入适合快速建立认知 |
| Week 2-3 | pbl-huamei / five-step | 根据主题复杂度和探究深度选择 |
| Week 4 | five-step | 总结展示适合结构化教学 |

## Step 4: User Confirmation

Present the monthly plan. Wait for approval. If changes requested, adjust.

## Step 5: Write Output

Write to `studio/changes/{workspace}/month-plan.md`.

Update `studio/changes/{workspace}/config.yaml` with the month's methodology setting if the user specifies a preference.
Create or update `studio/changes/{workspace}/status.json`:
- Set `type = "planning"`
- Set `plan_level = "month"`
- Preserve `plan_name`, `created_at`, and `linked_projects` if already present
- If no file exists, initialize:

```json
{
  "type": "planning",
  "plan_level": "month",
  "plan_name": "{workspace}",
  "phase": "planning",
  "created_at": "{ISO-8601}",
  "linked_projects": []
}
```

Suggest next steps:
> **下一步:**
> - `/workshop-planner:week-plan {周次}` — 细化某周的每日安排
> - 为某个周主题创建或进入 project workspace
> - `/workshop-designer:design {主题}` — 在项目中开始 PBL 周的设计
> - `/workshop-lesson:lesson {主题}` — 在项目中开始五步法教案设计

## Out of Scope

- This skill does NOT design individual lessons or PBL projects
- This skill does NOT generate daily schedules (use `week-plan` for that)
