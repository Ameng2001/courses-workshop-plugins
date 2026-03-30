# 导出目标模型 / Export Targets

## local-markdown-bundle

用途：
- 本地交付审核
- release bundle 二次整理

输出：
- `.workshop/exports/{workspace}/`
- 保留 Markdown 源文件

## word-ready-bundle

用途：
- 为后续 `.docx` 生成器准备输入

输出建议：
- `manifest.yaml`
- `lesson-plan.formatted.md`
- `assets/`

## pdf-ready-bundle

用途：
- 为后续 PDF 渲染器准备输入

输出建议：
- 与 `word-ready-bundle` 相同
- 可附加页眉页脚和版式参数占位

## remote-bundle-placeholder

用途：
- 为后续 MCP/COS/S3 发布保留统一打包结构

注意：
- 当前阶段只定义目录与 manifest 结构
- 不直接接远端发布能力
