# Plugin Brief: workshop-templates

> Created: 2026-03-29

## Business Context

教学法模板注册中心——管理可插拔的教学方法论模板（PBL、五步法等），每个模板定义自己的设计流水线、编码规范和输出格式。使系统支持多种教学方法论而无需修改核心插件。

## Plugin Candidates

2 个 skills：template-list（列出可用模板）、template-select（选择/切换模板）

## Success Criteria

- 教师能快速查看支持的教学方法论
- 切换模板后，整个设计流水线自动适配
- 新模板可通过添加目录扩展，无需修改代码

## Notes

- 模板存储在 references/templates/{template-id}/ 下
- 每个模板包含 manifest.yaml、methodology-guide.md、coding-spec.md、output-format.md
- 当前内置模板：pbl-huamei（华美 PBL）、five-step（五步法）
- 被 workshop-designer、workshop-lesson 引用
