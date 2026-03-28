# Course Workshop Plugins

AI 驱动的幼儿园 PBL 课程研发工具集 —— 从月度主题到课堂预案的完整设计流水线。

> 基于开放的 SKILL.md 插件规范构建，可在任何兼容的 AI 运行时上使用。使用 [Astra Studio](https://github.com/VanLengs/astra-studio-plugins) 工具链开发。

## 概述

Course Workshop 将华美 PBL 方法论（五步路径、三阶段九要素、驱动问题六原则、4C 能力框架）内置为可执行的设计流水线，让课研主任从"白纸起步"变为"确认和调整"。

```
输入：月度主题 + 年龄段
  → 主题分析 → 驱动问题 → 网络图 → 线索拆分 → 活动设计 ×3 → 预案生成
输出：符合华美 PBL 五段式的完整课堂预案（含 4C 映射、资源清单、质量报告）
```

## 插件一览

| 插件 | 说明 | 技能 |
|------|------|------|
| **workshop-core** | 工作区管理 —— 初始化、状态追踪、归档 | init, status, promote |
| **workshop-insight** | 主题分析 —— 主题拆解、前置经验评估、4C 能力映射 | theme-analysis, prior-knowledge, competency-mapping |
| **workshop-designer** | 课程设计 —— 驱动问题、网络图、探究线索、活动设计、预案生成 | driving-question, network-map, inquiry-scaffold, activity-design, proposal-generate |
| **workshop-quality** | 质量保障 —— 课标检查、年龄适切性验证、专家评审 | standards-check, proposal-review |
| **workshop-resource** | 资源管理 —— 材料匹配、分类（PBL Box/探索袋/自备）、完整性校验 | resource-planner, resource-check |

每个插件可独立安装使用，也可全部安装获得完整流水线。

## 快速开始

### 前置条件

- 任意支持 SKILL.md 插件规范的 AI 运行时（如 Claude Code、或其他兼容平台）
- Git（推荐，用于版本管理设计产出）

### 安装

**方式一：本地加载（推荐初次体验）**

将以下 5 个插件目录加载到你的 AI 运行时：

```
./workshop-core
./workshop-designer
./workshop-insight
./workshop-quality
./workshop-resource
```

具体加载命令因平台而异，请参考你所使用运行时的插件加载文档。

**方式二：从 Marketplace 安装**

如果平台支持 Marketplace 机制：

```
1. 添加插件仓库: VanLengs/courses-workshop-plugins
2. 按需安装: workshop-core, workshop-designer, workshop-insight, workshop-quality, workshop-resource
```

### 典型流程

```
/workshop-insight:theme-analysis      # 1. 分析月度主题
/workshop-insight:competency-mapping  # 2. 4C 能力映射
/workshop-designer:driving-question   # 3. 生成驱动问题
/workshop-designer:network-map        # 4. 绘制网络图
/workshop-designer:inquiry-scaffold   # 5. 拆分探究线索
/workshop-designer:activity-design    # 6. 设计活动（×3）
/workshop-designer:proposal-generate  # 7. 生成完整预案
/workshop-quality:standards-check     # 8. 课标与质量检查
/workshop-resource:resource-planner   # 9. 资源清单规划
```

## 领域专家 Agent

内置 3 位领域专家参与多角色协作评审：

- **幼儿发展心理学家** —— 年龄适切性、认知发展阶段判断
- **幼儿园课程专家** —— 课标覆盖、PBL 方法论合规性
- **教学设计师** —— 活动编排、学习体验设计

## 项目结构

```
├── workshop-core/          # 工作区管理插件（已发布）
├── workshop-designer/      # 课程设计插件（已发布）
├── workshop-insight/       # 主题分析插件（已发布）
├── workshop-quality/       # 质量保障插件（已发布）
├── workshop-resource/      # 资源管理插件（已发布）
├── studio/                 # Astra Studio 开发工作区
│   ├── config.yaml         # Studio 配置
│   ├── changes/            # 开发中的插件
│   ├── agents/             # 自定义领域专家
│   └── archive/            # 已归档的插件
└── docs/                   # 白皮书与开发日志
```

## 方法论基础

- **华美 PBL 五步路径图** —— 控制设计流程阶段与产出物
- **三阶段九要素** —— 控制项目实施结构
- **驱动问题六原则** —— 控制问题生成质量
- **4C 能力框架**（Critical Thinking, Creativity, Communication, Collaboration）—— 控制能力映射准确性
- **《3-6 岁儿童学习与发展指南》** —— 控制年龄适切性与领域覆盖

## 许可证

Apache-2.0
