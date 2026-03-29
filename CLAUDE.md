# Course Workshop Plugins

Multi-methodology course design toolkit for kindergarten curriculum directors (课研主任) and classroom teachers (一线教师). Supports PBL proposals, Five-Step lesson plans, semester/month/week planning, and school knowledge base management.

## Repository Structure

```
├── workshop-core/         # Workspace management (init, status, promote) — 3 skills
├── workshop-designer/     # PBL course design pipeline (driving-question → proposal) — 5 skills
├── workshop-insight/      # Pre-analysis toolkit (theme, prior-knowledge, 4C) — 3 skills
├── workshop-quality/      # Quality assurance (standards-check, proposal-review) — 2 skills
├── workshop-resource/     # Resource management (resource-planner, resource-check) — 2 skills
├── workshop-lesson/       # Five-Step lesson plan pipeline (objective → scaffold → detail → generate) — 4 skills
├── workshop-planner/      # Hierarchical curriculum planning (semester → month → week) — 3 skills
├── workshop-kb/           # School knowledge base (import, index, query) — 3 skills
├── workshop-templates/    # Teaching methodology template registry (list, select) — 2 skills
└── studio/                # Design workspace (planning artifacts, git-tracked)
```

## Plugin Dependencies

```
workshop-core       (zero deps)
workshop-insight    (zero deps)
workshop-quality    (zero deps)
workshop-templates  (zero deps)
workshop-kb         (depends on workshop-core)
workshop-designer   (depends on workshop-core, workshop-templates)
workshop-lesson     (depends on workshop-core, workshop-templates)
workshop-planner    (depends on workshop-core, workshop-templates)
workshop-resource   (depends on workshop-core)
```

## Design Pipelines

### PBL Pipeline: `/workshop-designer:design`

```
driving-question → network-map → inquiry-scaffold → activity-design ×3 → proposal-generate
      ↑                                                    ↑                      ↑
  (workshop-insight                                   (workshop-resource     (workshop-insight
   optional input)                                     optional input)       optional input)
```

### Five-Step Lesson Pipeline: `/workshop-lesson:lesson`

```
lesson-objective → lesson-scaffold → lesson-detail → lesson-generate
      ↑                  ↑                                  ↑
  (workshop-kb      (workshop-templates              (workshop-quality
   optional)         five-step template)              optional check)
```

### Curriculum Planning Pipeline: `/workshop-planner:plan`

```
semester-plan → month-plan → week-plan
     ↑              ↑            ↓
 (workshop-kb   (workshop-kb   (feeds into workshop-lesson
  calendars)     textbooks)     or workshop-designer)
```

## Domain Experts

3 built-in agents in each plugin's `agents/` directory:
- **early-childhood-curriculum-expert** — PBL methodology, curriculum standards, age-appropriateness
- **child-development-psychologist** — developmental stages, 4C mapping, prior knowledge
- **instructional-designer** — activity feasibility, resource planning, teacher instructions

## Development Workflow

1. Edit SKILL.md files directly — changes take effect immediately
2. Test with: `claude --plugin-dir ./workshop-core --plugin-dir ./workshop-designer --plugin-dir ./workshop-insight --plugin-dir ./workshop-quality --plugin-dir ./workshop-resource --plugin-dir ./workshop-lesson --plugin-dir ./workshop-planner --plugin-dir ./workshop-kb --plugin-dir ./workshop-templates`
3. Key test flows:
   - PBL: `/workshop-designer:design 我周围的人`
   - Five-Step: `/workshop-lesson:lesson 认识春天的花`
   - Planning: `/workshop-planner:plan 2026春季学期`

## Key References

| File | Plugin | Purpose |
|------|--------|---------|
| pbl-methodology-guide.md | designer | PBL 方法论 + 三阶段九要素 |
| activity-coding-spec.md | designer | PBL-Cx-y 编码规范 |
| guidelines-3-6.md | insight, quality, lesson | 《指南》五大领域摘要 |
| 4c-framework.md | insight | 4C 能力矩阵 + 误分类表 |
| age-ability-matrix.md | quality | 年龄×能力查询表 |
| pbl-box-catalog.md | resource | PBL Box 物料目录 |
| resource-categories.md | resource | 资源分类规则 + 决策树 |
| methodology-guide.md | templates/five-step | 五步法方法论指南 |
| coding-spec.md | templates/five-step | FS-Sx-yy 编码规范 |
| output-format.md | templates/five-step | 五步法教案输出格式 |
| semester-calendar-template.md | planner | 学期日历模板 |
| weekly-schedule-template.md | planner | 周日程模板 |
| kb-schema.md | kb | 知识库文档结构定义 |
