---
name: week-plan
description: Generate a detailed weekly schedule with daily time slots, activity assignments, and material lists. Use when a teacher needs the daily breakdown for a specific week, or when someone says "plan this week" or "what do I teach each day".
allowed-tools: Read, Write, Glob, Agent
user-invocable: true
---

# Week Plan

Generate a detailed daily schedule for one week, mapping activities to time slots and preparing material lists.

## Expert Discovery

1. **Primary role**: Load `instructional-designer.md` (feasibility, scheduling)
2. **Scan project experts**: Glob `studio/agents/*.md`

## Pre-check

1. Verify `studio/` exists
2. Look for `studio/changes/{workspace}/month-plan.md` — read the target week's sub-theme and methodology
3. Look for existing activity files:
   - PBL activities: `studio/changes/{workspace}/activities/clue-*.md`
   - Lesson plans: `studio/changes/{workspace}/lesson-plan*.md`
   - If activities already designed, map them to daily slots
   - If not yet designed, create placeholder slots with suggested topics

## Step 1: Gather Context

Auto-populate from month-plan if available. Otherwise ask:

> **请提供以下信息：**
> 1. **周次**: 第几周？（如"第2周"）
> 2. **子主题**: 本周的教学重点（如"花的颜色和形状"）
> 3. **日期范围**: 起止日期
> 4. **教学法**: 本周使用什么教学法？
> 5. **特殊安排**: 是否有节假日、园所活动等占用？

## Step 2: Generate Daily Schedule

Following the format in `references/weekly-schedule-template.md`, generate:

### 每日时段表

| 时段 | 周一 | 周二 | 周三 | 周四 | 周五 |
|------|------|------|------|------|------|
| 晨间活动 | {activity} | {activity} | {activity} | {activity} | {activity} |
| 集体教学 | {coded_activity} | {coded_activity} | {coded_activity} | {coded_activity} | {coded_activity} |
| 区角活动 | {area_activity} | {area_activity} | {area_activity} | {area_activity} | {area_activity} |
| 户外活动 | {outdoor} | {outdoor} | {outdoor} | {outdoor} | {outdoor} |
| 午后活动 | {afternoon} | {afternoon} | {afternoon} | {afternoon} | {afternoon} |

### 编排原则

- 集体教学时段安排核心教学活动（PBL 活动或五步法教案）
- 区角活动投放与当日集体教学呼应的材料
- 户外活动可融入主题元素但不强制
- 周五留出分享/回顾时间
- 每天的集体教学活动使用对应方法论的编码（PBL-Cx-y 或 FS-Sx-y）

## Step 3: Material Preparation List

Compile a daily material checklist:

| 日期 | 活动 | 所需材料 | 数量 | 来源 |
|------|------|---------|------|------|
| 周一 | {activity} | {material} | {qty} | PBL Box / 自备 / 班级常备 |

## Step 4: Teacher Notes

Generate practical reminders:
- 提前准备事项（需要提前一天准备的材料或布置）
- 关注要点（本周需要重点观察记录的幼儿行为）
- 家园互动（需要发给家长的通知或亲子任务）

## Step 5: User Confirmation and Write

Present the week plan. Wait for approval. Write to `studio/changes/{workspace}/week-{N}-plan.md`.

Suggest next steps:
> **下一步:**
> - `/workshop-lesson:lesson {主题}` — 为某天的集体教学编写教案
> - `/workshop-resource:resource-planner` — 统一规划本周资源

## Out of Scope

- This skill does NOT write individual lesson plans (use workshop-lesson)
- This skill does NOT design PBL activities (use workshop-designer)
