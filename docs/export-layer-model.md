# Export Layer Model

## 目标

将“运行时语义源”和“客户视觉交付”分开，避免在课程设计阶段直接把 Markdown 产物绑死到某一版式。

## 三层模型

### 1. Runtime Source

位置：
- `.workshop/projects/`
- `.workshop/archive/`

特征：
- Markdown 语义源
- 包含完整设计过程
- 由设计技能直接读写

### 2. Release Bundle

位置：
- `courses/`

特征：
- 面向交付消费
- 不保留全部设计过程
- 只保留最终主交付物和必要附件

### 3. Export Bundle

位置：
- `.workshop/exports/`

特征：
- 面向格式化交付
- 准备 Word/PDF/远端发布输入
- 不替代 runtime source 或 release bundle

## Why

客户当前给出的参考模板体现的是“视觉交付格式”，而平台当前产物主要是“结构化 Markdown 语义源”。如果直接在 lesson 生成阶段绑定双栏版式，会造成：

- 生成层与导出层耦合
- 不同客户模板难以并存
- release bundle 语义不稳定

因此建议：

- `workshop-5step` / `workshop-activity` 负责生成结构化内容
- `workshop-format` 负责格式标准化与导出包准备

## 当前阶段的实现原则

1. 先输出 Markdown 语义源
2. 再用 `format-lesson` 选择布局 profile
3. 再用 `export-bundle` 准备 Word/PDF/远端输入目录
4. 真正的 `.docx` / `.pdf` 二进制导出后续再补
