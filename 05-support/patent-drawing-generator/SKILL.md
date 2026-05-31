---
name: patent-drawing-generator
description: "Internal drawing and figure specialist under patent-cn-draft and patent-cn-review for Chinese patent drawings, method flowcharts, structural line drawings, block diagrams, figure legends, and DOCX/PDF-ready patent figure assets. Direct use is allowed for standalone 专利附图、流程图、结构示意图、框图、附图说明、说明书附图 tasks."
---
# Patent Drawing Generator

## New Architecture Role

`patent-cn-draft` is the preferred public drafting orchestrator, and `patent-cn-review` may call this skill for figure checks. This skill is the internal `06_figures` drawing specialist. Direct use is appropriate only for standalone drawing/figure tasks or older prompts that explicitly name this skill.

## Scope

Use this skill to create or revise Chinese patent drawings and their matching figure legends. It covers:

- method flowcharts
- structural schematic drawings
- system or module block diagrams
- process route diagrams
- figure legends and reference numeral consistency
- DOCX/PDF-ready figure insertion checks

For filing-oriented drawings, favor formal black-and-white line art over decorative rendering.

## Intake

Before drawing, collect or infer:

- invention title and claim subject
- independent claim steps or structure features
- terms that must appear verbatim in the figure
- whether the figure is for preview, DOCX insertion, or filing-ready output
- required file format, usually PNG for raster preview or SVG/PDF for cleaner line art

If a claim set exists, mirror claim terminology exactly. Do not leave stale scope terms in figures after a subject change, such as `鞋用`, `中底`, `中底模具`, or `发泡中底坯体`, unless the claims still require them.

## Drawing Rules

- Use black lines and black text on a white background.
- Avoid color, gradients, shadows, texture, perspective decoration, icons, or background images.
- Use simple rectangular boxes, arrows, leader lines, and reference numerals.
- Keep Chinese text short and legible. Do not let text overflow boxes.
- Keep figure legends consistent with the drawing and the specification.
- For exact Chinese text, check for wrong characters, missing characters, OCR-like artifacts, and punctuation drift before delivery.
- If inserting into DOCX, create a new document copy unless the user explicitly asks to overwrite, and then validate the package and render or preview the page.

## Method Flowcharts

When the drawing includes a process, method, preparation route, or steps `S1/S2/S3`, use this route:

1. Extract the ordered method steps from the independent claim or confirmed technical solution.
2. Simplify only if the user asks; otherwise preserve the step content verbatim enough to identify the claimed step.
3. Draw one step per rectangular box.
4. Arrange boxes vertically from top to bottom and connect adjacent boxes with downward arrows.
5. Do not add a title, explanatory note, watermark, decorative element, or unrelated icon inside the image.

### Deterministic Flowchart Tool

For filing-oriented method flowcharts, prefer the local deterministic renderer before using image generation:

```bash
patent-flowchart \
  --steps-file steps.txt \
  --out output/图1_方法流程图.svg \
  --png output/图1_方法流程图.png
```

If the `patent-flowchart` command is not on `PATH`, call `~/.codex/skills/patent-drawing-generator/scripts/patent-flowchart` directly.

The input file should contain one step per line, for example:

```text
S1、将聚醚多元醇、扩链剂、催化剂和发泡剂混合，得到第一混合物；
S2、向第一混合物中加入异氰酸酯组分并搅拌，得到发泡反应料；
S3、将发泡反应料注入成型模具中进行发泡成型，得到发泡材料坯体；
S4、对发泡材料坯体进行熟化处理，得到聚氨酯发泡材料。
```

Use `--layout-json layout.json` when the geometry needs to be inspected or reused. If the PNG will be inserted into a DOCX, use the PNG output as the primary asset and keep the SVG as the editable source.

The renderer calculates Chinese text wrapping using a local Songti/SimSun-style font, fixes each arrow from the lower center of one box to the upper center of the next box, and increases canvas height from the actual wrapped text. This route should avoid floating arrows, crossed connectors, and text overflow for ordinary vertical method flowcharts.

Useful tuning options:

- `--font-size 30` for dense claim text.
- `--box-width 1200 --canvas-width 1680` for longer steps.
- `--gap 100` when arrows should have more white space.
- `--font /path/to/font.ttc` when a specific filing font is required.

### Flowchart Image Prompt

When using image generation for a method flowchart, use the following prompt template and replace the placeholder with the actual steps:

```text
请根据以下方法步骤，绘制一张中国专利附图风格的方法类流程图图片。

【方法步骤】
在此处粘贴方法步骤，例如：
S1、……
S2、……
S3、……
S4、……

【绘图要求】
1. 图片内容为“方法类专利流程图”，整体风格应符合中国专利附图的正式、规范、简洁要求；
2. 所有步骤内容均使用简体中文显示；
3. 字体使用宋体风格，字形端正、清晰、规整，不得出现字体变形、拉伸、模糊、错字、漏字或乱码；
4. 字号适当，保证步骤文字清楚可读；文字较长时可在方框内自然换行，但不得超出方框边界；
5. 每一个方法步骤单独放置在一个规则的矩形方框内；
6. 方框线条为黑色实线，粗细均匀，边角规整，整体干净工整；
7. 所有方框按照方法步骤顺序自上而下竖向排布，整体居中，间距均匀；
8. 相邻两个方框之间使用竖直向下的箭头连接，箭头方向清楚，连接关系准确；
9. 流程图仅体现方法步骤及其先后顺序，不添加无关图案、图标、装饰元素、背景纹理、阴影、渐变或彩色效果；
10. 图片采用黑白线稿风格，白色背景，黑色文字、黑色方框、黑色箭头；
11. 版面应留有适当空白边距，整体布局清晰、稳定、对称，适合作为专利说明书附图使用；
12. 仅输出流程图图片，不要添加标题、说明文字、水印或额外标注。
```

If exact filing text matters, prefer deterministic drawing through SVG, PIL, Word/OOXML, Mermaid-to-SVG, or another code-based renderer. Use the generated image as a preview unless its Chinese text has been manually checked and is fully correct.

## Structural Or Block Drawings

For structure or system figures:

- Identify all parts/modules and their relationships before drawing.
- Assign simple reference numerals when needed, preferably `1, 2, 3...`.
- Use one name for each component across the figure, legend, and specification.
- Use leader lines only when they improve clarity.
- Do not draw realistic textures or commercial product styling unless the user asks for a reference-style schematic.

For block diagrams:

- Put each module in a rectangle.
- Use arrows to show material, signal, force, fluid, or data flow.
- Label arrows only when the label is necessary to understand the technical relationship.

## Figure Legend Rules

Write figure legends in patent style:

- `图1为本发明实施例涉及的...流程示意图。`
- `图2为本发明实施例涉及的...结构示意图。`
- `图3为图2中A处的局部放大示意图。`

Keep legends tied to what is actually visible. Do not leave placeholders such as `图1为本发明实施例涉及的；` or `图3位`.

## Quality Checks

Before final delivery:

- The figure matches the independent claim or confirmed embodiment.
- All Chinese text is accurate and readable.
- No stale technical subject terms remain after retitling or broadening.
- No decorative or colored elements appear in formal patent figures.
- Every referenced figure has a matching legend.
- If a DOCX is produced, the image is embedded and the DOCX opens or validates.
