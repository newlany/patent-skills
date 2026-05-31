# Fixed Output Spec

## Artifact Goal

Produce a customer-facing Chinese patent proposal list for project-level patent mining. The document should help the client IPR team see:

- which patent proposals are currently writable;
- how each proposal maps to original disclosures;
- what each proposal protects;
- the core technical problem, key technical means, and main technical effect;
- which figures support each proposal.

Do not make an IPR confirmation question list. Do not make a formal patent application draft.

## Required Document Structure

Use this exact order:

1. Centered title: `{项目名称}专利提案清单`.
2. Centered subtitle: `专利布局评估稿`.
3. Two short overview paragraphs.
4. `一、提案总览`.
5. A 7-column overview table.
6. `二、提案技术内容`.
7. One repeated proposal section per proposal.

No cover page, generation date, work directory, source-reading section, or process note.

## Overview Paragraphs

Use two paragraphs modeled on this pattern:

```markdown
本文件围绕{项目核心平台或技术主题}，对具备成案基础的技术方案进行整理。提案按照技术系统层级展开，先呈现{系统层级一}，再呈现{系统层级二}，以及{局部结构或可靠性层级}。

申请类型栏预留，由贵方结合公司布局策略、检索结论和产品公开状态确定。各提案的技术内容以可形成权利要求保护边界为目标，后续可据此进入检索、发明人确认和撰稿。
```

## Overview Table

Use exactly these columns:

| 序号 | 原始交底案号 | 原始交底名称 | 方案层级 | 当前提案名称 | 申请类型 | 对应关系及关键技术手段 |
|---:|---|---|---|---|---|---|

Rules:

- `申请类型` stays blank unless the user asks to fill it.
- `对应关系及关键技术手段` starts with `对应当前提案。`
- Keep the table customer-facing. Do not mention local file paths or stage report names.
- If one original disclosure is split into multiple proposals, repeat the original disclosure mapping in each row and distinguish the proposal name.

## Proposal Detail Section

For each proposal, use this fixed structure:

```markdown
### {序号}. {当前提案名称}

对应原始交底：{原始交底案号}，{原始交底名称}。

{一段摘要。}

#### 技术问题

{一段技术问题。}

#### 关键技术手段

- {手段一。}
- {手段二。}
- {手段三。}

#### 主要技术效果

{一段技术效果。}

#### 初步撰写

{当用户明确要求时，写入一至两段权利要求布局提示。}

#### 图示

![图 {序号}-1 {图题}]({图片路径})
```

If the user does not ask for preliminary drafting content, omit `初步撰写`. If no usable figure exists, omit `图示` instead of adding a blank placeholder. Do not add `后续确认事项` in the customer-facing proposal list unless the user explicitly asks to include it.

## Proposal Ordering

Prefer this order unless the project materials clearly dictate another system hierarchy:

1. `整机外循环风道`
2. `整机背部风道储备`
3. `内环温换热模块`
4. `功率散热均温储备`
5. `板级电气与散热协同`
6. `板级局部热点治理`
7. `装配可靠性细节`

Within the same layer, put the most mature or most central proposal first. Reserve directions with weaker materials can remain in the list if they have a clear claim route, but their summary should identify the protection focus rather than overstate maturity.

## Split and Merge Rules

- Split one disclosure into multiple proposals when it contains separate technical problems and separate independent-claim routes.
- Merge supplement points when they are alternative implementations of the same technical problem.
- Split derivative schemes when their airflow path, heat source target, installation position, or module boundary differs enough to support separate claims.
- Do not force every original filing form into exactly one proposal.
- Do not include a proposal that only repeats a common component location unless it has a specific technical problem and technical effect chain.

## DOCX Style

Use the same restrained style as the reference proposal list:

- Page: A4 landscape.
- Margins: top 1.5 cm, bottom 1.4 cm, left 1.5 cm, right 1.5 cm.
- Title: centered, Microsoft YaHei, 20 pt, bold, color `#1F4E79`.
- Subtitle: centered, Microsoft YaHei, 11 pt, color `#595959`.
- Body: SimSun, 10.5 pt, 1.25 line spacing, first-line indent 21 pt, space after 5 pt.
- Headings: Microsoft YaHei, bold, color `#1F4E79`.
- Heading 1: 15 pt.
- Heading 2: 12.5 pt.
- Heading 3: 11 pt.
- Overview table: `Table Grid`, 7 columns, header fill `#1F4E79`, header text white, body 8 pt.
- Table column widths in inches: `0.42, 1.35, 2.20, 0.95, 2.05, 0.70, 2.78`.
- Footer: centered, SimSun, 9 pt, gray; usually `{项目名称}专利提案清单`.
- Figure captions: centered, SimSun, 9 pt, italic.

## Proposal JSON For DOCX Builder

Use this shape with `scripts/build_proposal_list_docx.py`:

```json
{
  "title": "光伏大组串热设计系列案专利提案清单",
  "subtitle": "专利布局评估稿",
  "footer": "光伏大组串热设计系列案专利提案清单",
  "overview": [
    "本文件围绕……进行整理。",
    "申请类型栏预留……"
  ],
  "cases": [
    {
      "no": 1,
      "source_no": "ZLTA202605-14",
      "source_name": "SPI465K 风道布局专利01说明",
      "layer": "整机外循环风道",
      "title": "SPI465K 底部主风道与角部空空换热器侧向补冷布局",
      "application_type": "",
      "table_means": "由底部风机形成外循环主风道……",
      "summary": "面向 465K 整机热架构……",
      "problem": "SPI465K 的底部主风道需要同时服务……",
      "means": [
        "底部风机形成自下而上的外循环主风道。",
        "空空换热器布置在机箱角部或侧部。"
      ],
      "effect": "侧向补冷风道降低后级换热器入口温度。",
      "drafting": [
        "当用户要求初步撰写时，可在此写入主权利要求对象和从属优化点。",
        "该字段也可命名为 preliminary_drafting，DOCX 生成脚本会渲染为“初步撰写”。"
      ],
      "images": [
        {
          "path": "输出/过程/03_方案重构/报告图片/14-img-04.png",
          "caption": "图 1-1 后级空空换热器侧向补冷风道示意",
          "width_inches": 6.1
        }
      ]
    }
  ]
}
```

Image paths may be absolute, relative to the JSON file, or relative to the current working directory.
