---
name: theme-analysis
description: Analyze a monthly theme's educational value, background context, and curriculum standards alignment. Use when starting a new PBL project, when the curriculum director needs a project overview, or when someone says "analyze this theme". Produces a project overview with standards references.
allowed-tools: Read, Write, Glob, Agent
user-invocable: true
---

# Theme Analysis

Analyze a monthly theme to produce the "01 项目概览 Project Overview" section of a PBL proposal — theme background narrative, educational value, and alignment with《3-6岁儿童学习与发展指南》curriculum standards.

## Expert Discovery

This skill uses **dynamic expert loading**. On every run:

1. **Primary role**: Always load `early-childhood-curriculum-expert.md` (leads standards alignment)
2. **Scan project experts**: Glob `studio/agents/*.md` — load all custom experts
3. **Match by relevance**: Select experts whose domain touches the monthly theme (e.g., if theme is "My Body", load health-related experts)
4. **Skip template**: Do not load `_domain-expert-template.md`

The primary role validates curriculum standards mapping. Domain experts contribute theme-specific educational insights.

## Pre-check

1. Verify `studio/` exists. If not, tell the user to run `/workshop-core:init` first.
2. Determine the workspace path:
   - If `$ARGUMENTS` contains a workspace name, use `studio/changes/$ARGUMENTS/`
   - Otherwise, derive from the theme name (lowercase, kebab-case, 2-3 words)
3. Check if `studio/changes/{workspace}/theme-analysis.md` already exists:
   - If yes, read it and ask: "已有主题分析文档，是否需要重新生成或在此基础上修改？"

## Step 1: Gather Context

Ask the user for:

> **请提供以下信息：**
> 1. **月度主题**：本月的项目主题是什么？（如"我周围的人"、"交通工具"、"春天来了"）
> 2. **年龄段**：PreK-3 (2-3岁) / PreK-4 (3-4岁) / K (5-6岁)
> 3. **补充信息**（可选）：是否有园本特色、地域文化、季节关联、或已有的主题背景说明？

Extract:
- **Theme**: the monthly theme (Chinese + English)
- **Age group**: determines depth of analysis and standards scope
- **Context**: any additional focus, cultural hooks, or prior materials

## Step 2: Generate Theme Background Narrative

Write a **bilingual narrative (Chinese primary, English secondary)** of 2-3 paragraphs that explains WHY this theme matters for children's development. The narrative must:

### Narrative Structure

| Paragraph | Focus | Content |
|-----------|-------|---------|
| 1. 主题意义 | Why it matters | Connect the theme to children's lived experience. Explain what makes it meaningful — not a dictionary definition, but a developmental argument. |
| 2. 发展价值 | Developmental value | Articulate what cognitive, social, emotional, or physical growth this theme supports. Reference age-specific characteristics. |
| 3. 探究潜力 | Inquiry potential | Explain why this theme is suitable for PBL — what open questions it raises, what hands-on exploration it enables, what multiple perspectives it offers. |

### Narrative Quality Rules

| Rule | Good Example (✅) | Bad Example (❌) |
|------|------------------|-----------------|
| Explain WHY, not WHAT | "了解食物的来源帮助幼儿建立对自然界因果关系的初步理解" | "食物是人类生存的基本需求" |
| Ground in child's experience | "3-4岁幼儿每天都在经历'吃'这件事，但很少思考食物从哪里来" | "食物话题很重要" |
| Be specific to age group | "对于PreK-4幼儿，'我周围的人'可以从最熟悉的家庭成员开始延伸" | "这个主题适合各年龄段" |
| Show inquiry potential | "这一主题天然包含多个探究维度：谁种的？怎么长的？怎么变成食物的？" | "幼儿可以探索这个主题" |

### Bilingual Format

Write each paragraph in Chinese first, then provide the English version immediately below:

```
{Chinese paragraph}

{English translation}
```

## Step 3: Map to《指南》五大领域

Analyze which of the 5 domains this theme touches and to what degree.

### The Five Domains

| Domain | Chinese | Core Focus Areas |
|--------|---------|-----------------|
| Health | 健康 | 身心状况、动作发展、生活习惯与生活能力 |
| Language | 语言 | 倾听与表达、阅读与书写准备 |
| Social | 社会 | 人际交往、社会适应 |
| Science | 科学 | 科学探究、数学认知 |
| Art | 艺术 | 感受与欣赏、表现与创造 |

### Coverage Analysis Format

For each domain, assess:
- **Relevance level**: 核心 (Core — this theme deeply engages this domain), 关联 (Related — meaningful connection), 延伸 (Peripheral — possible but not central), 无关 (Not relevant)
- **Specific sub-domains touched**: cite the actual sub-domain categories
- **Example connection**: one concrete example of how this theme engages this domain

| 领域 Domain | 关联度 Relevance | 涉及子领域 Sub-domains | 举例 Example |
|-------------|-----------------|---------------------|-------------|
| 健康 Health | {核心/关联/延伸/无关} | {sub-domains} | {example} |
| 语言 Language | {核心/关联/延伸/无关} | {sub-domains} | {example} |
| 社会 Social | {核心/关联/延伸/无关} | {sub-domains} | {example} |
| 科学 Science | {核心/关联/延伸/无关} | {sub-domains} | {example} |
| 艺术 Art | {核心/关联/延伸/无关} | {sub-domains} | {example} |

### Coverage Validation Rules

- A well-chosen PBL theme should touch **at least 3 domains** at 核心 or 关联 level
- If fewer than 3 domains are engaged, flag it: "此主题领域覆盖较窄，建议扩展探究方向以覆盖更多领域"
- If ALL 5 domains are 核心, verify — it may mean the analysis is too generous. A theme rarely deeply engages every domain.

## Step 4: Identify Curriculum Standard Entries

For each domain marked 核心 or 关联, list the specific《指南》standard entries that apply.

### Standard Entry Format

```
### {Domain Chinese} / {Domain English}

**目标 {N}**: {standard title}

- **典型表现 ({age range})**: {age-appropriate behavioral indicator from《指南》}
- **与主题的关联**: {how this standard connects to the monthly theme}
```

### Age-Specific Standard Selection

Standards must be selected for the **target age group**:

| Age Group | 《指南》Age Band |
|-----------|----------------|
| PreK-3 (2-3岁) | 3-4岁（取低端表现） |
| PreK-4 (3-4岁) | 3-4岁 |
| K (5-6岁) | 5-6岁 |

List **3-8 standard entries** total across all relevant domains. Prioritize entries where the theme provides natural, concrete opportunities for children to demonstrate the standard.

### Standard Selection Rules

- ❌ Do not list standards just because they exist — only include standards this theme can genuinely address
- ❌ Do not fabricate standard numbers or text — use recognized categories from《指南》
- ✅ Focus on standards where the theme provides hands-on, experiential learning opportunities
- ✅ Include the specific age-band behavioral indicators (典型表现)

## Step 5: Expert Review

Use the Agent tool to have the `early-childhood-curriculum-expert` review the complete analysis.

Give the expert subagent:
- The agent definition from `studio/agents/early-childhood-curriculum-expert.md`
- The full theme analysis (narrative + domain coverage + standards)
- The monthly theme and age group
- The instruction: "Review this theme analysis for a PBL project. Evaluate: (1) Does the narrative genuinely explain WHY this theme matters for children's development, or is it generic? (2) Is the domain coverage analysis accurate — are relevance levels correctly assigned? (3) Are the curriculum standard entries appropriate for the target age group? (4) Are there important standards that were missed? (5) Is there enough depth here to support a full PBL project? Suggest specific improvements."

If additional domain experts were loaded, also ask them to review the narrative for domain-specific accuracy. For example, if the theme is "Healthy Eating" and a nutrition expert is loaded, ask: "Does the narrative accurately represent the nutritional education value? Are there misconceptions?"

### Common Expert Corrections

- "This narrative describes the theme but doesn't explain its developmental value — add specific developmental benefits"
- "The 科学 domain relevance is overstated — counting objects doesn't make this a 数学认知 theme"
- "Missing an important 社会 standard — this theme naturally involves 人际交往"
- "The behavioral indicators cited are for 5-6岁 but the target is PreK-4 — adjust to 3-4岁 norms"

Incorporate expert feedback before presenting to the user.

## Step 6: Present to User

Present the complete theme analysis:

> **主题分析：{Theme Chinese} / {Theme English}**
> **年龄段：{Age Group}**
>
> ---
>
> **主题背景 Theme Background**
>
> {Paragraph 1 — Chinese}
> {Paragraph 1 — English}
>
> {Paragraph 2 — Chinese}
> {Paragraph 2 — English}
>
> {Paragraph 3 — Chinese (if applicable)}
> {Paragraph 3 — English (if applicable)}
>
> ---
>
> **《指南》领域覆盖分析 Domain Coverage**
>
> | 领域 | 关联度 | 涉及子领域 | 举例 |
> |------|--------|-----------|------|
> | ... | ... | ... | ... |
>
> **覆盖统计**: 核心 {N} 个领域 / 关联 {N} 个领域 / 共覆盖 {N}/5 个领域
>
> ---
>
> **相关课程标准 Curriculum Standards**
>
> {Standard entries}
>
> ---
>
> **专家评价**: {expert feedback summary}
>
> 请确认分析内容，或指出需要修改的部分。

Wait for user confirmation. If the user wants changes, iterate.

## Step 7: Write Output

Once confirmed, create the workspace (if not exists) and write:

```
studio/changes/{workspace}/
└── theme-analysis.md
```

**Derive `{workspace}`** from the theme: lowercase, kebab-case, 2-3 words (e.g., "people-around-me", "healthy-eating").

Write `theme-analysis.md`:

```markdown
# Theme Analysis: {Theme Chinese} / {Theme English}

> Date: {YYYY-MM-DD}
> Age Group: {PreK-3 / PreK-4 / K}
> Theme: {Theme Chinese} / {Theme English}

## Theme Background / 主题背景

{Paragraph 1 — Chinese}

{Paragraph 1 — English}

{Paragraph 2 — Chinese}

{Paragraph 2 — English}

{Paragraph 3 — Chinese (if applicable)}

{Paragraph 3 — English (if applicable)}

## Domain Coverage / 《指南》领域覆盖

| 领域 Domain | 关联度 Relevance | 涉及子领域 Sub-domains | 举例 Example |
|-------------|-----------------|---------------------|-------------|
| 健康 Health | {level} | {sub-domains} | {example} |
| 语言 Language | {level} | {sub-domains} | {example} |
| 社会 Social | {level} | {sub-domains} | {example} |
| 科学 Science | {level} | {sub-domains} | {example} |
| 艺术 Art | {level} | {sub-domains} | {example} |

**Coverage Summary**: 核心 {N} / 关联 {N} / 延伸 {N} / 无关 {N}

## Curriculum Standards / 相关课程标准

### {Domain 1 Chinese} / {Domain 1 English}

**目标 {N}**: {standard title}
- 典型表现 ({age range}): {behavioral indicator}
- 与主题的关联: {connection to theme}

### {Domain 2 Chinese} / {Domain 2 English}

**目标 {N}**: {standard title}
- 典型表现 ({age range}): {behavioral indicator}
- 与主题的关联: {connection to theme}

{... more standards as applicable ...}

## Expert Review / 专家评审

- **{Expert name}**: {feedback summary and any adjustments made}

## Notes

- This analysis feeds into the "01 项目概览 Project Overview" section of the PBL proposal
- Domain coverage informs which 4C skills and learning goals to prioritize
```

Create or update `status.json`:

```json
{
  "type": "project",
  "project": "{workspace}",
  "theme": "{Theme Chinese} / {Theme English}",
  "target_collection": "courses",
  "phase": "planning",
  "created_at": "{ISO-8601}",
  "plan_refs": {
    "semester": null,
    "month": null,
    "week": null
  },
  "skills": {
    "theme-analysis": "done"
  }
}
```

Tell the user: "主题分析完成。建议接下来运行 `/workshop-insight:prior-knowledge {workspace}` 评估幼儿前期经验。"

## Validation Rules

Before finalizing output, verify:

1. **Narrative depth**: Each paragraph must be 3-5 sentences minimum, not a single generic line
2. **Bilingual completeness**: Every Chinese paragraph has an English counterpart
3. **Domain accuracy**: Relevance levels are justified, not inflated
4. **Standard specificity**: Each standard entry cites age-appropriate behavioral indicators
5. **At least 3 domains**: Theme touches 3+ domains at 核心 or 关联 level (flag if not)
6. **No fabricated standards**: Standard entries reference recognized《指南》categories, not invented ones

## Out of Scope

- Does NOT design driving questions (workshop-designer's responsibility)
- Does NOT assess prior knowledge (prior-knowledge's responsibility)
- Does NOT map 4C competencies (competency-mapping's responsibility)
- Does NOT generate the full proposal (proposal-generate's responsibility)
