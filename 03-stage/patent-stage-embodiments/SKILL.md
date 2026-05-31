---
name: patent-stage-embodiments
description: "Internal specification-section specialist under patent-cn-draft for drafting, revising, or checking 具体实施方式, embodiments, examples, comparative examples, testing design, result analysis, formulas, drawings, and figure legends. Direct use is allowed for standalone embodiment-section work."
---
# Method Patent Embodiment Agent

## New Architecture Role

`patent-cn-draft` is the preferred public drafting orchestrator. This skill is the internal `05_specification` embodiments specialist. Direct use is appropriate only for standalone embodiment/example drafting or checking requests, or older prompts that explicitly name this skill.

## Skill Position

- 类型：线性撰写说明书阶段 / embodiments stage。
- 中文入口：具体实施方式、实施例、对比例、测试设计、测试结果、公式说明、附图说明。
- 输入：权利要求书、发明内容、技术方案重构、实验数据、附图或流程图。
- 输出：实施方式正文、实施例/对比例、测试方法和结果分析。
- 支撑能力：可调用 `patent-support-docx-math`、`spreadsheet`、`doc`、`minimax-docx`。
- 边界：不得改变权利要求的核心保护边界；若发现权利要求无法被实施例支持，应反馈给撰写/QC 阶段。

## Scope

Use this skill for method-type patent application embodiments, including `具体实施方式`, `实施例`, process examples, comparative examples, testing descriptions, and results-analysis text.

This is a general embodiment-writing skill. It can be used independently, or as a companion skill when a specialized method-patent workflow reaches the embodiment/examples stage.

Do not use this skill as the sole guide for device-only cases, office-action responses, invalidity work, or claim drafting unless the user specifically asks for embodiment-related work in those contexts.

## Trigger Phrases

- 实施例
- 具体实施方式
- 方法类专利实施例
- 工艺细化
- 实施例设计
- 对比例设计
- 测试设计
- 结果分析
- 附图/图例一致性
- 公式修复
- 根据权利要求写实施例
- 检查实施例是否支持权利要求

## Baseline Rule

Before drafting or revising, identify the operative baseline:

- confirmed claim set, especially the independent claim step chain and dependent-claim features
- confirmed invention content / summary and technical-effects main line
- final technical disclosure or process-detail section
- figures, figure labels, result curves, tables, formulas, and prior Q&A
- user style constraints, such as no small headings, natural paragraphs, or a required embodiment count

If the prerequisite baseline is missing, proceed only with a clear provisional assumption and state the downstream risk.

## Drafting Order

1. Build an embodiment outline before writing the prose.
2. Use the independent claim steps as the backbone. Explain each step in order.
3. Fold dependent-claim features, formulas, ranges, parameters, materials, devices, control conditions, detection steps, transfers, and step linkages into the relevant step.
4. For preparation-heavy or material-preparation cases, default to a three-part structure: `方案详细说明 -> 实施例和对比例 -> 性能测试`.
5. Add concrete examples after the general step explanation. Examples should be centered on the independent claim and meaningful fallback ranges.
6. Add comparative examples only when they directly test the inventive main line.
7. Add testing and results analysis only after examples and retained result tables are fixed.
8. Finish with a support check against claims, formulas, figures, legends, and result terminology.

## Embodiment Writing Rules

- Write in specification style, not claim style. Do not cite claim numbers inside the embodiment unless the user specifically wants that.
- Explain the method as an executable technical route, not a restatement of the claims.
- Unless the user asks for a different structure, after one brief application-scene paragraph first write the full independent-claim step chain such as `S1`, `S2`, `S3` in order, and only then move into fuller explanation of each step.
- For every step, clarify the object being processed, the operation performed, the technical condition or parameter used, and the output that feeds the next step.
- Do not front-load a standalone glossary before the step chain unless the user explicitly asks for that format.
- In Chinese patent-style drafting, do not use double quotes around self-defined terms unless the user explicitly asks for quoted presentation or a cited source requires it.
- When a custom term, derived intermediate quantity, or internal process label first appears in the detailed step explanation, define it naturally in the paragraph where it is used so that a skilled person can understand its meaning without relying on drafting shorthand. Vary the lead-in wording naturally; do not repeatedly lean on one fixed phrase such as `这里所称`.
- If explaining one custom term requires subordinate terms or process labels, explain those subordinate terms there as well, preferably with a brief technical example.
- For self-defined parameters or non-routine feature quantities, explain how they are obtained, measured, calculated, or represented in physical or algorithmic terms rather than naming the quantity alone.
- If a feature quantity comes from image analysis, signal processing, or model input construction, specify the source signal, the basic processing route, and the resulting representation form that enters the next step.
- When a step relies on a physical device or module, explain the device in industrial-implementation terms, including where it is arranged, what signal or energy it receives, what concrete mechanical or electrical action it performs, and how that action realizes the claimed step.
- For control-system embodiments, explain the division of work among PLC controllers, industrial control computers, embedded computing modules, sensors, drives, valves, and positioning mechanisms rather than stopping at functional labels alone.
- For execution devices such as motors, cylinders, valves, sliders, guide hooks, rollers, or clamps, write how the control instruction is converted into speed change, torque change, pressure change, position change, path-length change, wrap-angle change, or other concrete physical effects.
- For preparation-heavy or material-preparation cases, open the detailed-description part with `本发明提供一种...方法，包括如下步骤：步骤一...步骤二...` and then explain each step in order with fuller process detail.
- For preparation-heavy or material-preparation cases, the detailed scheme must state how each step is actually implemented in industrial practice: name the equipment or device type used for the step, explain the material feed or transfer operation, state the operating flow such as heating, vacuumizing, metering, stirring, pumping, extrusion, cooling, cutting, drying, sampling, or detection, and identify the output that enters the next step.
- If the user asks for no small headings, keep only `实施例1/2/...` and `对比例1/2/...` style labels as local headings. Write the detailed-scheme part, raw-material paragraph, testing methods, and results analysis as ordinary specification paragraphs rather than subheaded blocks.
- If the user asks for no small headings in `具体实施方式`, do not use local headings such as `方案详细说明`, `实施例和对比例`, `性能测试`, `测试项目和方法`, `测试数据表`, or `结果分析`. Keep the statutory section heading `具体实施方式` and only the `实施例1/2/...` and `对比例1/2/...` labels unless the user explicitly asks otherwise.
- In that no-small-heading mode, the opening step-chain paragraph should directly restate the full independent-claim route with retained parameters and ranges rather than hiding them in a later paragraph.
- When a case is range-driven, the general step explanation should naturally absorb the dependent-claim ranges and preferred process details instead of leaving them detached.
- If the user asks for natural patent paragraphs, avoid internal small headings. It is still acceptable to refer to `S1`, `S2`, and similar step labels in prose.
- After the step-by-step detailed explanation, add at least one concrete end-to-end example unless the user explicitly asks to omit examples.
- For multiple embodiments, make the first embodiment the most complete version unless the user instructs otherwise. Later embodiments may focus on differences, but must still be technically self-contained enough to avoid ambiguity.
- If a user instruction conflicts with the confirmed case logic, resolve the conflict from the baseline and state the correction briefly.
- Do not introduce unclaimed technical routes, parameter directions, or comparison schemes as if they were part of the invention.
- When the claim subject has been broadened or retitled, synchronize embodiment objects, equipment names, examples, test objects, and drawing legends with that subject. For example, if the claim is `聚氨酯发泡材料`, do not keep `鞋用中底材料`, `中底模具`, or `发泡中底坯体` as required wording; use generic wording such as `成型模具`, `发泡材料坯体`, and `聚氨酯发泡材料`, while leaving application scenes only as optional examples when useful.
- If the user asks to reduce AI-like tone, shorten overly long sentences, reduce unnecessary `、` stacking, and keep the wording plain and specification-like rather than ornate.
- If a module or algorithm is conventional in the art, it is acceptable to note briefly that its concrete internal structure belongs to common technical knowledge and will not be expanded, but use that shortcut sparingly and do not use it to avoid explaining self-defined terms, key feature quantities, or the industrial implementation chain.
- Do not isolate terminology explanations into inventor-note style lists unless the user explicitly asks for that format; by default, weave the definitions into the detailed-description paragraphs.

## Examples And Comparative Examples

When drafting concrete examples:

- For preparation-heavy or material-preparation cases, begin the examples section with a prose raw-material paragraph rather than a raw-material table unless the user explicitly asks otherwise.
- Place the raw-material paragraph or compact raw-materials section before `实施例` and `对比例` unless the user explicitly forbids it.
- In that raw-material paragraph, state raw-material name, commercial grade or model, and supplier for the main raw materials when supported by the baseline or by evidence-backed technical completion.
- Prefer commercially available domestic Chinese products when they technically fit the disclosure and claim scope.
- When completing supplier and grade/model information through market research, rely on real web evidence such as a supplier page, TDS, SDS, catalog page, product manual, manufacturer page, or credible marketplace/manufacturer listing. Do not invent commercial sources.
- Treat each market-researched grade as an embodiment example, not as a protection-boundary limitation. Add a generic fallback such as the same chemical type, the same key functional property, and the same moisture or purity control when that is needed to preserve claim scope.
- If reliable source evidence is missing or ambiguous, write generic technical wording or flag the item for inventor confirmation instead of fabricating a supplier or grade.
- Match each commercial raw material to the functional claim feature it is supposed to support. Do not equate broader product wording with a narrower claim feature; for example, `active hydrogen` is not automatically `hydroxyl`, and `high nonvolatile content` is not automatically `low water content`.
- If the inventive main line depends on a commercial color paste, dispersion, additive, or carrier being non-aqueous, hydroxyl-bearing, reactive, or low-moisture, rely on a TDS/COA or supplier source where possible. If the source is incomplete, write the embodiment conditionally and operationally, such as `使用前经取样确认或预处理为含羟基有机载体体系，并控制含水率不高于...`, rather than using absolute wording such as `水分为无`.
- Equipment may be described in the detailed scheme explanation or within the examples; do not automatically create a separate equipment table unless the user asks for one.
- Use specific values to demonstrate the method, but do not collapse broad claim ranges into one mandatory value.
- When the user wants range coverage, default to at least three implementation examples arranged around the lower bound, an optimized value, and the upper bound of the retained parameter window, while keeping the technical route otherwise consistent.
- Explain how each example executes the general method and where its parameters come from.
- Comparative examples must compare against the inventive distinction. Avoid random variations that do not support the inventive-step logic.
- Comparative examples may be written briefly as differences from one anchor embodiment when this avoids repetition, but do not create hidden contradictions with unchanged conditions.
- When comparing pigments, color pastes, color masterbatches, fillers, or other active dispersed components, define the comparison basis. Prefer `按有效成分/有效颜料含量折算为相同用量` when the comparison is meant to isolate the preparation route, and avoid ambiguous `等量` wording unless total added mass is truly the intended basis.
- Keep comparative examples compatible with later testing design. Do not create a comparison that cannot be measured or explained.

## Testing And Results

When adding tests or result analysis:

- Select only test items that support the claimed distinctions and technical-effects logic.
- Use only real, usable test standards whose number and scope match the tested metric. Do not invent standard numbers or force a standard that does not cover the property.
- Prefer official or industry standards where appropriate; for Chinese patent drafts, prefer current GB or GB/T standards when they exist for the test item. Include standard number, test conditions, sample size, equipment, environment, and calculation method when available.
- Verify standard numbers and names from reliable public sources, standard platforms, official notices, standards databases, manufacturer/application notes, or other credible references before citing them.
- If the user asks that testing be based on Chinese national standards, do not invent a nonstandard test item just because the draft uses a commercial metric. For high-rebound foamed polymer materials, prefer GB/T-backed metrics such as `GB/T 6670` rebound resilience, `GB/T 6669` compression set, `GB/T 18941` constant-load impact fatigue, and `GB/T 3512` heat-air aging; add `GB/T 10807` indentation hardness, `GB/T 6343` apparent density, `GB/T 6342` dimensions, or `GB/T 12811` cell size only when they support the claimed effect. If a custom `能量回归率` test is retained, label it as an internal or disclosed test method and define it separately.
- For preparation-heavy or material-preparation cases, keep the test section limited to `测试项目和方法 -> 测试数据表 -> 结果分析`.
- When the user asks for test results, include an actual result table or a clearly described result set, not only the test method. If no measured data are provided, mark the values as draft or to-be-confirmed in the response to the user, and keep the document wording technically restrained.
- Use tables for all retained test data, but do not use tables for the raw-material list unless the user asks for that format.
- Design result-table columns around measured metrics, not around argument labels or process labels, unless the user explicitly wants the label column. If a column or metric is removed, scan the surrounding paragraphs and analysis for stale references to the deleted wording.
- When tests compare colorants, fillers, additives, or dispersed components with different commercial concentrations, state the normalization basis before analyzing the table, such as equal effective pigment content, equal active ingredient content, or equal total addition amount.
- Use technically standard units and symbols in tables where practical, such as `kg/m³` for apparent density, and keep symbol formatting consistent across the test method, table, and analysis.
- Keep designed or hypothetical draft data distinct from real measured data.
- If the disclosure does not provide full test data, drafted example data may be completed from field knowledge and retained technical logic, but the response should make that status clear.
- Analyze only retained tables and retained metrics. Do not cite deleted metrics or infer effects that the results cannot support.
- Connect metric differences back to the method route, not merely to the fact that one example is "better".
- In results analysis, do not say that the test results `prove inventiveness` or equivalent. Instead, briefly identify which technical means played the key role in achieving the retained effects.

## Formulas

For formula-heavy method embodiments:

- Preserve material formulas from claims and technical disclosure. Claim formulas should appear in the detailed embodiment unless intentionally placed elsewhere.
- Keep formulas as native Word math objects when editing `.docx`; do not flatten formulas into plain text.
- Define every variable in proximity to the formula unless already clearly defined.
- If a disclosure formula conflicts with the adopted claim formula, omit the conflicting version and state the reason in the response.
- If formulas are embedded as images or duplicate a formula already written as native math, state the limitation or duplicate status when reporting formula completeness.

## Figures And Legends

Treat figures as part of the technical disclosure.

- Every figure referenced in the embodiment must be tied to the method step, structure, parameter, model, test, or result it supports.
- For a method-flowchart drawing, mirror the independent claim step chain exactly and keep only the ordered method steps. Use black text, black rectangular boxes, vertical downward arrows, white background, and no title or decorative elements when the figure is intended as a Chinese patent drawing.
- When exact Chinese text in a patent flowchart matters, prefer deterministic drawing through Word/OOXML, SVG, PIL, or another code-based renderer over generative image output. Generative images may be used as a preview, but the filing-ready figure should be checked for missing characters, wrong characters, overflow, and OCR-like artifacts before inserting into the DOCX.
- Every important visible label in a figure should be explained in the text, especially input/output ports, boundaries, coordinate axes, sample structures, model domains, data-series legends, and result-curve legends.
- If a model or simulation figure shows ports, sources, probes, sensors, fixtures, boundary conditions, or measurement positions, describe their location, function, relationship to the modeled method step, and whether they are operating conditions, measurement settings, or model boundary settings.
- If a result figure uses internal comparison labels from the disclosure, replace them with neutral patent labels and define them before analyzing the curves or tables.
- Use descriptive figure legends that identify the source and role of each data series, such as measured result, reference result, comparative result, or embodiment result. Avoid unexplained labels that only make sense inside the inventor's draft.
- When comparison curves or tables are retained, state which are part of the invention's embodiment and which are only for comparison. Comparative labels should not imply that the comparison route is a required step of the claimed method.

## Internal Label Cleanup

Do not directly migrate disclosure or Q&A labels into the application text, including:

- internal scheme numbers or shorthand labels from the disclosure
- labels that merely say "the invention scheme" without defining the actual technical route
- issue-list, meeting-note, or Q&A labels
- inventor-facing notes
- old chapter, table, figure, or section labels from the disclosure

If such labels are needed to preserve a comparison, redefine them in neutral patent language before using them.

## DOCX Handling

When the deliverable is a Word file:

- Create a new copy unless the user explicitly asks to overwrite.
- Prefer formula-preserving DOCX tooling, such as `patent-support-docx-math` for inspection/extraction and `minimax-docx` or deterministic OOXML edits for writeback.
- After writing, inspect for native equations, drawings, embedded objects, tracked changes, comments, and package validity.
- Run a text scan for stale internal terms, formula drift, figure-reference drift, and embodiment-object confusion.

## Output Contract

For text-only drafting:

1. provide the final embodiment paragraph(s) ready to paste
2. state where the text should be inserted
3. list any figure-legend or terminology changes the user should make

For DOCX drafting:

1. create or update the requested document copy
2. report the output path
3. report the checks performed
4. mention any warnings or unresolved limitations

For review/checking:

1. list issues first, ordered by importance
2. provide exact text or figure-label corrections
3. distinguish required fixes from optional improvements

## Final Checklist

Before finishing, check:

- every independent-claim step is explained in order
- dependent-claim features are naturally integrated
- concrete examples support the inventive main line and fallback ranges
- preparation-heavy examples include evidence-backed raw-material names, grades/models, and suppliers before `实施例` / `对比例` when that information is completed
- comparative examples, if any, are defined as comparison only
- tests and results support, rather than overstate, the technical effects
- cited testing standards are real, usable, and matched to the tested metric
- retained test data are presented in tables
- all important formulas are present and correctly displayed
- every cited figure and visible key label is explained
- figure legends use patent-suitable terms
- no stale internal labels or contradicted embodiment objects remain
