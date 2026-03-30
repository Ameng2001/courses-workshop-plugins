# Course Workshop Plugins

AI 驱动的幼儿园课程设计平台插件集合，面向课研主任和一线教师，支持 PBL 预案、五步法教案、学期/月/周规划，以及校本知识库复用。

> 基于开放的 `SKILL.md` 插件规范构建，可在兼容运行时上使用。使用 [Astra Studio](https://github.com/VanLengs/astra-studio-plugins) 工具链开发。

## 概述

Course Workshop 已从单一 PBL 工具集演进为多方法论课程工作台：

- `workshop-designer` 负责 PBL 月度项目预案
- `workshop-lesson` 负责五步法单课时教案
- `workshop-planner` 负责学期 / 月 / 周全局规划
- `workshop-kb` 负责校本知识库导入、索引和检索
- `workshop-templates` 负责教学法 pipeline 注册与选择

系统的主工作对象是 **课程项目（project workspace）**，不是单个 plugin、skill 或文档类型。

一个 project workspace 对应一个具体课程主题，例如：
- `spring-flowers`
- `people-around-me`
- `my-body`

同一 project 内可以并存多种产物：
- PBL 预案 `proposal.md`
- 五步法教案 `lesson-plan.md`
- 资源规划与核验结果
- 质量检查与专家评审结果
- 与该主题相关的周计划引用

## Project Workspace First

当前仓库遵循以下实现原则：

1. 用户先创建或进入一个 `project workspace`，再选择要产出什么。
2. `workshop-*` 目录是唯一真实实现源。
3. `.workshop/projects/*` 中的目录默认表示项目工作区；`.workshop/plans/*` 是全局计划资产，不等同于课程项目。
4. 教学法 pipeline 是产物级选择，不锁定整个项目。
5. 学期 / 月 / 周计划是全局可复用资产，project 只引用相关切片，不复制完整计划。
6. 计划与课程设计是弱依赖：可以先做计划，也可以先做项目，后续再互相关联。
7. 领域专家使用单一事实源 `experts/`；runtime 只允许 `.workshop/agents/custom` 覆盖，`workshop-*/agents` 仅保留 plugin-local 专家。
8. 大阶段衔接点遵循 HIL（human-in-the-loop），不会默认无确认直通到 shipped。

## 插件分层

| 分层 | 插件 | 说明 |
|------|------|------|
| 平台底座 | `workshop-core` | 初始化 `.workshop/`、查看状态、归档交付物 |
| 平台能力 | `workshop-kb`, `workshop-templates` | 提供知识上下文与教学法 pipeline |
| 设计流水线 | `workshop-designer`, `workshop-lesson`, `workshop-planner` | 生成 PBL 预案、五步法教案和全局计划 |
| 辅助能力 | `workshop-insight`, `workshop-quality`, `workshop-resource` | 前期分析、质量保障、资源规划 |

## 插件一览

| 插件 | 说明 | 技能 |
|------|------|------|
| **workshop-core** | 项目工作区管理 | `init`, `config`, `onboarding`, `status`, `link-plan`, `approve`, `promote` |
| **workshop-insight** | 项目前期分析 | `theme-analysis`, `prior-knowledge`, `competency-mapping` |
| **workshop-designer** | PBL 项目预案设计 | `driving-question`, `network-map`, `inquiry-scaffold`, `activity-design`, `proposal-generate` |
| **workshop-quality** | 质量检查与专家评审 | `standards-check`, `proposal-review` |
| **workshop-resource** | 教学资源规划与核验 | `resource-planner`, `resource-check` |
| **workshop-lesson** | 五步法单课时教案 | `lesson-objective`, `lesson-scaffold`, `lesson-detail`, `lesson-generate` |
| **workshop-planner** | 学期 / 月 / 周规划 | `semester-plan`, `month-plan`, `week-plan` |
| **workshop-kb** | 校本知识库 | `kb-import`, `kb-index`, `kb-query` |
| **workshop-templates** | pipeline 注册与选择 | `pipeline-list`, `pipeline-select` |

## 快速开始

### 前置条件

- 任意支持 `SKILL.md` 插件规范的 AI 运行时
- Git（推荐，用于版本管理 `.workshop/` 下的课程项目与计划资产）

### 安装

本地加载全部插件目录：

```bash
claude --plugin-dir ./workshop-core \
       --plugin-dir ./workshop-designer \
       --plugin-dir ./workshop-insight \
       --plugin-dir ./workshop-quality \
       --plugin-dir ./workshop-resource \
       --plugin-dir ./workshop-lesson \
       --plugin-dir ./workshop-planner \
       --plugin-dir ./workshop-kb \
       --plugin-dir ./workshop-templates
```

### 推荐使用顺序

```text
1. /workshop-core:init
2. /workshop-core:config show
3. /workshop-core:onboarding
4. 创建或进入一个 project workspace（一个课程主题）
5. /workshop-templates:pipeline-list
6. /workshop-templates:pipeline-select <id>
7. 按需要继续：
   - /workshop-designer:design <theme>
   - /workshop-lesson:lesson <theme>
   - /workshop-planner:semester-plan <semester>
   - /workshop-kb:kb-import <path>
```

### 典型项目路径

PBL 项目：

```text
/workshop-insight:theme-analysis
/workshop-insight:competency-mapping
/workshop-designer:driving-question
/workshop-designer:network-map
/workshop-designer:inquiry-scaffold
/workshop-designer:activity-design
/workshop-designer:proposal-generate
/workshop-quality:standards-check
/workshop-resource:resource-planner
```

五步法教案：

```text
/workshop-lesson:lesson-objective
/workshop-lesson:lesson-scaffold
/workshop-lesson:lesson-detail
/workshop-lesson:lesson-generate
```

## 项目结构

```text
├── workshop-core/          # 项目工作区与交付管理
├── workshop-designer/      # PBL 项目预案流水线
├── workshop-insight/       # 项目前期分析
├── workshop-quality/       # 质量检查与评审
├── workshop-resource/      # 资源规划与核验
├── workshop-lesson/        # 五步法教案流水线
├── workshop-planner/       # 全局学期 / 月 / 周规划
├── workshop-kb/            # 校本知识库
├── workshop-templates/     # 教学法 pipeline 注册中心
├── studio/                 # Astra Studio 插件研发目录
├── .workshop/
│   ├── config.yaml         # 课程工作台运行配置
│   ├── projects/           # 项目工作区
│   ├── plans/              # 全局规划记录
│   ├── agents/
│   │   └── custom/         # 园所/项目自定义专家
│   ├── kb/                 # 校本知识库内容
│   └── archive/            # 已归档课程完整历史
├── courses/                # 已发布课程 release bundles
├── experts/                # 共享领域专家单一事实源
├── studio/
│   ├── roles/              # Astra Studio 专用流程角色
│   └── ...                 # 其余 plugin 研发资产
└── docs/                   # 白皮书、原则说明与参考文档
```

`studio/` 与 `.workshop/` 职责不同：
- `studio/` 用于 Astra Studio 的 plugin / skill 研发
- `.workshop/` 用于真实课程项目、计划、知识库与归档运行时
- `courses/` 用于最终课程 release bundle，不保存完整设计过程

agent 作用域也分层：
- `experts/` 是共享领域专家的单一事实源
- `.workshop/agents/custom/` 用于园所或项目自定义专家
- `workshop-*/agents/` 仅用于单个 plugin 的私有专家
- `studio/roles/` 用于 plugin 研发专用流程角色，如产品经理、架构师

## 领域专家 Agent

内置 3 位领域专家参与多角色协作评审：

- **幼儿发展心理学家**：年龄适切性、认知发展阶段判断
- **幼儿园课程专家**：课程标准、PBL 合规性、主题适配
- **教学设计师**：活动编排、可执行性、学习体验设计

## 方法论基础

- **华美 PBL 五步路径图**
- **三阶段九要素**
- **驱动问题六原则**
- **4C 能力框架**
- **《3-6 岁儿童学习与发展指南》**
- **五步教学法结构化教案方法**

更多原则见 `docs/project-workspace-principles.md`。
HIL 规则见 [docs/hil-checkpoint-model.md](/Users/liuyameng/.codex/worktrees/8a4e/courses-workshop-plugins/docs/hil-checkpoint-model.md)。
脚本化边界见 [docs/skill-script-boundary.md](/Users/liuyameng/.codex/worktrees/8a4e/courses-workshop-plugins/docs/skill-script-boundary.md)。

## 许可证

Apache-2.0
