# Workspace Status Schema

本文件定义 `course-workshop-plugins` 当前阶段推荐使用的 `status.json` 结构，用于统一：

- project workspace 的状态字段
- planning workspace 的状态字段
- phase 推进规则
- 各 skill 写回 `skills.*` 的约定
- `promote` 的最小完成条件
- major human-in-the-loop checkpoints

当前运行时根目录优先使用 `.workshop/`：

- `.workshop/projects/`
- `.workshop/plans/`
- `.workshop/kb/`
- `.workshop/archive/`

## 1. Workspace Types

当前只使用两种类型：

- `project`
- `planning`

规则：

1. `status.json.type` 是 workspace 分类的第一信号。
2. 如果 `type` 缺失，运行时才允许退回文件名启发式判断。
3. 不再为新实现创建 `type: "plugin"`。
4. `type: "plugin"` 和 `type: "domain"` 不属于运行时允许的 workspace 类型。

## 2. Project Workspace

一个 project workspace 对应一个具体课程主题，可包含一个或多个交付物，例如：

- `proposal.md`
- `lesson-plan.md`
- `resource-plan.md`
- `quality-report.md`
- `review-comments.md`

推荐结构：

```json
{
  "type": "project",
  "project": "spring-flowers",
  "theme": "春天的花 / Spring Flowers",
  "target_collection": "courses",
  "target": {
    "kind": "local",
    "path": "courses/spring-flowers"
  },
  "phase": "planning",
  "created_at": "2026-03-29T10:00:00+08:00",
  "hil": {
    "checkpoint": "project-framing",
    "status": "not_started",
    "requested_at": null,
    "approved_at": null,
    "approved_by": null,
    "notes": ""
  },
  "plan_refs": {
    "semester": null,
    "month": null,
    "week": null
  },
  "skills": {
    "lesson-objective": "done"
  }
}
```

### Required Fields

| Field | Type | Meaning |
|------|------|---------|
| `type` | string | Must be `project` |
| `project` | string | Workspace id, usually kebab-case |
| `target_collection` | string | Promote 目标目录，默认 `courses` |
| `phase` | string | 当前阶段 |
| `created_at` | string | ISO-8601 timestamp |
| `skills` | object | 各 skill 完成状态 |

### Recommended Fields

| Field | Type | Meaning |
|------|------|---------|
| `theme` | string | 人类可读主题名 |
| `target.kind` | string | 发布目标类型，当前推荐 `local`，未来可扩展为 `cos` / `mcp` |
| `target.path` | string | 本地发布路径；若未来切云端，可替换为目标服务字段 |
| `plan_refs.semester` | string or null | 关联学期计划 |
| `plan_refs.month` | string or null | 关联月计划 |
| `plan_refs.week` | string or null | 关联周计划 |
| `hil.checkpoint` | string | 当前等待的人类确认关口 |
| `hil.status` | string | `not_started / awaiting_review / changes_requested / approved` |
| `hil.requested_at` | string or null | 发起该关口确认的时间 |
| `hil.approved_at` | string or null | 该关口被确认通过的时间 |
| `hil.approved_by` | string or null | 谁确认通过 |
| `hil.notes` | string | 备注或变更要求 |

## 3. Planning Workspace

planning workspace 表示共享规划记录，不直接等同于课程交付项目。

推荐结构：

```json
{
  "type": "planning",
  "plan_level": "semester",
  "plan_name": "2026-spring",
  "phase": "planning",
  "created_at": "2026-03-29T10:00:00+08:00",
  "linked_projects": []
}
```

### Required Fields

| Field | Type | Meaning |
|------|------|---------|
| `type` | string | Must be `planning` |
| `plan_level` | string | `semester` / `month` / `week` |
| `plan_name` | string | 规划记录名 |
| `phase` | string | 当前阶段 |
| `created_at` | string | ISO-8601 timestamp |

### Recommended Fields

| Field | Type | Meaning |
|------|------|---------|
| `linked_projects` | array | 引用了该规划记录的项目列表 |

## 4. Phase Lifecycle

当前统一使用以下 phase：

- `planning`
- `designing`
- `reviewing`
- `approved`
- `shipped`

### Phase Meaning

| Phase | Meaning |
|------|---------|
| `planning` | 项目已建立，但核心设计产物尚未完成 |
| `designing` | 关键设计产物正在形成 |
| `reviewing` | 已有最终交付物，进入质量检查或专家评审 |
| `approved` | 已通过评审，可执行 promote |
| `shipped` | 已归档并交付到 target collection |

### Recommended Transitions

| Trigger | From | To |
|--------|------|----|
| 创建 project / 选择模板 | none | `planning` |
| lesson 三件套或 inquiry 主骨架完成 | `planning` | `designing` |
| `proposal.md` 或 `lesson-plan.md` 生成 | `designing` | `reviewing` |
| 人工确认通过评审 | `reviewing` | `approved` |
| `/workshop-core:promote` 完成 | `approved` | `shipped` |

注意：

1. `approved` 目前仍是人工或外部治理动作，不由 skill 自动设置。
2. planning workspace 通常停留在 `planning`，除非将来对规划本身引入评审流。

## 4a. Human-in-the-Loop Checkpoints

推荐 project 使用以下 HIL checkpoints：

- `project-framing`
- `design-scaffold`
- `deliverable-draft`
- `approval-gate`

推荐 HIL 状态：

- `not_started`
- `awaiting_review`
- `changes_requested`
- `approved`

推荐对应关系：

| Trigger | HIL checkpoint | Suggested HIL status |
|--------|----------------|----------------------|
| 模板选择 / 项目立项 | `project-framing` | `awaiting_review` |
| 骨架设计完成 | `design-scaffold` | `awaiting_review` |
| 完整初稿生成 | `deliverable-draft` | `awaiting_review` |
| 进入最终审批 | `approval-gate` | `awaiting_review` |
| 审批通过 | `approval-gate` | `approved` |

## 5. Skill Status Conventions

`skills` 对象用于记录完成度。推荐状态值：

- `done`
- `approved`

当前实现规范中，以下 skill 应写回 `skills.*`：

### PBL / Insight

| Skill | Status Key | Recommended Effect |
|------|------------|--------------------|
| `theme-analysis` | `theme-analysis` | create/update project status |
| `prior-knowledge` | `prior-knowledge` | preserve previous insight statuses |
| `competency-mapping` | `competency-mapping` | preserve previous insight statuses |
| `driving-question` | `driving-question` | keep phase `planning` |
| `network-map` | `network-map` | keep phase `planning` unless later artifacts exist |
| `inquiry-scaffold` | `inquiry-scaffold` | may move phase to `designing` |
| `activity-design` | `activity-design` | set phase `designing` |
| `proposal-generate` | `proposal-generate` | set phase `reviewing` |

### Lesson

| Skill | Status Key | Recommended Effect |
|------|------------|--------------------|
| `lesson-objective` | `lesson-objective` | create/update project status |
| `lesson-scaffold` | `lesson-scaffold` | keep phase `planning` |
| `lesson-detail` | `lesson-detail` | set phase `designing` |
| `lesson-generate` | `lesson-generate` | set phase `reviewing` |

### Quality / Resource

| Skill | Status Key | Recommended Effect |
|------|------------|--------------------|
| `standards-check` | `standards-check` | keep phase `reviewing` |
| `proposal-review` | `proposal-review` | keep phase `reviewing` |
| `resource-planner` | `resource-planner` | usually no phase change |
| `resource-check` | `resource-check` | keep phase `reviewing` if final deliverable exists |

## 6. Promote Requirements

`/workshop-core:promote` 只适用于 `type: "project"`。

如果 `type == "planning"`，必须拒绝 promote。

### Deliverable Rule

至少存在一个最终交付物：

- `proposal.md`
- `lesson-plan.md`

如果两者都不存在，不允许 promote。

### Target Rule

当前默认 shipped 行为是：

1. 将 release bundle 复制到本地 `target_collection`
2. 将原 project workspace 归档到 `.workshop/archive/`

推荐同时在 `status.json` 中预留 `target` 字段，便于未来扩展：

- `local`：本地目录
- `cos`：对象存储
- `mcp`：通过 MCP 服务发布

也就是说，`shipped` 的语义应理解为“已发布 release bundle 到目标介质并完成归档”，而不是复制完整工作区。

### Required Skills by Deliverable Type

#### PBL Proposal

如果存在 `proposal.md`，最小必需 skill 为：

- `driving-question`
- `network-map`
- `inquiry-scaffold`
- `activity-design`
- `proposal-generate`

#### Lesson Plan

如果存在 `lesson-plan.md`，最小必需 skill 为：

- `lesson-objective`
- `lesson-scaffold`
- `lesson-detail`
- `lesson-generate`

#### Mixed Project

如果同一 project 同时存在：

- `proposal.md`
- `lesson-plan.md`

则两组 skill 都必须满足。

### Phase Requirement

promote 前必须满足：

```json
{
  "phase": "approved"
}
```

并且：

```json
{
  "hil": {
    "checkpoint": "approval-gate",
    "status": "approved"
  }
}
```

`promote` 成功后，归档目录中的 `status.json` 应更新为：

```json
{
  "phase": "shipped",
  "shipped_at": "2026-03-29T18:00:00+08:00",
  "shipped_to": "courses/spring-flowers"
}
```

## 7. Plan Linking Rules

`plan_refs` 和 `linked_projects` 采用轻量引用，不要求复杂关系系统。

### 7.1 Project Side

project workspace 可在任意时刻补充：

```json
{
  "plan_refs": {
    "semester": "2026-spring",
    "month": "2026-april",
    "week": "2026-april-week-2"
  }
}
```

推荐时机：

1. 创建 project 时，如果用户明确说明来自某个 semester/month/week 计划，直接写入。
2. 如果先有 project、后有 planning，可在后续人工补挂。
3. 不要求所有 project 都必须有 `plan_refs`。

### 7.2 Planning Side

planning workspace 可选维护反向索引：

```json
{
  "linked_projects": [
    "spring-flowers",
    "garden-life"
  ]
}
```

规则：

1. `linked_projects` 是推荐字段，不是 promote 前置条件。
2. 只记录 project id，不复制 project 内容。
3. 同一个 project 不应在同一 planning record 中重复出现。

### 7.3 Conflict Rule

如果 project 的 `plan_refs` 与 planning 的 `linked_projects` 不一致：

1. 以 project 侧 `plan_refs` 为主。
2. planning 侧只作为便于浏览的反向索引。

## 8. Approval Checklist

`approved` 是人工治理状态，不由单个 skill 自动设置。

推荐的最小审批清单如下。

### 8.1 PBL Proposal Approval

在将 PBL project 从 `reviewing` 调整为 `approved` 前，至少确认：

1. `proposal.md` 已生成。
2. `skills` 中以下项已完成：
   - `driving-question`
   - `network-map`
   - `inquiry-scaffold`
   - `activity-design`
   - `proposal-generate`
3. 如已启用质量链路，以下文件应存在或已审阅：
   - `quality-report.md`
   - `review-comments.md`
4. 如已启用资源链路，以下文件应存在或已审阅：
   - `resource-plan.md`
   - `resource-check-report.md`
5. 审批人确认该项目可进入归档 / 发放阶段。

### 8.2 Lesson Plan Approval

在将 lesson project 从 `reviewing` 调整为 `approved` 前，至少确认：

1. `lesson-plan.md` 已生成。
2. `skills` 中以下项已完成：
   - `lesson-objective`
   - `lesson-scaffold`
   - `lesson-detail`
   - `lesson-generate`
3. 如有补充质量审阅结果，审批人已查看。
4. 审批人确认该教案可进入归档 / 发放阶段。

### 8.3 Mixed Project Approval

如果同一个 project 同时包含 PBL 与 lesson 交付物：

1. 必须同时满足 PBL 和 lesson 两组检查。
2. `approved` 只设置一次，但表示整个 project 已准备好 promote。

### 8.4 Approval Writeback

人工审批通过后，推荐将 `status.json` 至少更新为：

```json
{
  "phase": "approved"
}
```

如果需要保留审批痕迹，可扩展为：

```json
{
  "phase": "approved",
  "approved_at": "2026-03-29T18:00:00+08:00",
  "approved_by": "curriculum-director"
}
```

## 9. Strictness Rules

运行时要求：

1. 所有 workspace 必须显式写入 `type: "project"` 或 `type: "planning"`。
2. 若缺失 `plan_refs`，运行期应补齐为：

```json
{
  "plan_refs": {
    "semester": null,
    "month": null,
    "week": null
  }
}
```

4. 若 planning workspace 缺失 `linked_projects`，运行期应视为空数组。

## 10. Implementation Priority

后续真正在代码或脚本层落地时，优先顺序建议为：

1. 统一所有主 skill 写回 `status.json`
2. 统一新建 workspace 时的 `type`
3. 统一 `status` 的读取逻辑
4. 统一 `promote` 的验证逻辑
5. 最后再考虑是否把 project / planning 分目录存放
