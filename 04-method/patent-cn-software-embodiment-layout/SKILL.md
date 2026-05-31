---
name: patent-cn-software-embodiment-layout
description: "Draft or revise Chinese software, AI, algorithm, data-processing, computer-implemented, or platform patent specification sections when claims are arranged as method plus system/device/apparatus plus electronic device plus computer-readable storage medium or program product. Use for 背景技术 framing, 发明内容 effect drafting, 具体实施方式 layout, execution-subject wording, custom-term definition, module-to-step mapping, and concise electronic-device/storage-medium support."
---
# CN Software Embodiment Layout

## Role

Use this skill as a companion to `patent-cn-draft`, `cn-patent-invention-content`, or `patent-stage-embodiments` when the case is a computer-implemented invention and the claim package includes:

- a method independent claim;
- a system, device, apparatus, or module claim;
- an electronic device claim; and
- a computer-readable storage medium or program-product claim.

The goal is to write the software-patent specification like a mature Chinese patent: keep `背景技术` low and controlled, place the real inventive contribution in the `发明内容` effect logic, make the method embodiment substantive, map system modules to method steps, and let electronic-device and storage-medium embodiments inherit the same executable route without repeating every step mechanically.

## Required Baseline

Before drafting or revising, identify:

- the low-level background defect that the independent claim can at least solve;
- any known route or admitted prior-art capability that should be discussed in the effect section rather than over-admitted in the background;
- the independent method step chain and dependent-claim feature groups;
- the system/module claim and its module names;
- the electronic-device and storage-medium claim wording;
- the figures, especially flowchart, system block diagram, and data/sample diagram;
- custom terms that are not ordinary claim language.

If claim scope or a custom term is unclear, draft a provisional definition that preserves breadth and flag it to the user.

## Default Layout

Use this order unless the user asks for no local headings or the existing filing style forbids them:

1. General implementation statement and execution subject.
2. Term definitions for custom data objects, intermediate results, rules, models, thresholds, and output artifacts.
3. System/application environment overview.
4. Optional or pre-executed preparation stage, such as model training, rule-library construction, calibration, registration, or template setup.
5. Main method flow by step labels, following the independent claim.
6. Key sub-process embodiments for complex or inventive links.
7. End-to-end example that demonstrates the whole method.
8. System/device/module embodiment mapped to the method steps.
9. Electronic-device embodiment.
10. Computer-readable storage-medium or program-product embodiment.
11. Variant, deployment, and combination statements.

For the detailed template and paragraph-level drafting pattern, read [references/layout-template.md](references/layout-template.md).

When the task includes `背景技术`, `发明内容`, or style normalization from a user sample, also read [references/spec-section-style.md](references/spec-section-style.md).

## Spec-Wide Strategy

- Keep the background problem low enough that the independent solution solves it. Do not admit a close automatic, AI, or platform route in `背景技术` unless the user or source material requires it.
- Put the real inventive advancement in the first technical-effect block. Use the pattern `并非仅仅...而是在...基础上进一步...` when it naturally fits, but avoid calling the contribution `创造性` inside the application text.
- Treat prior-art comparison as effect reasoning, not background self-attack: state what other routes may do, then explain what the present solution further solves through claimed feature cooperation.
- Match the user's natural patent style when a sample is provided. Prefer complete sentences over dense `、` lists, avoid over-precise AI-like chains, and use restrained effect language such as `较为稳定`、`减少`、`有利于`、`进一步改善`.
- Keep `技术方案段 -> 效果段` alignment. Do not let a dependent-feature effect rely on a later or unclaimed feature.

## Drafting Rules

- Put definitions before heavy use of custom terms when the case has many self-defined algorithmic objects. Do not leave key definitions hidden inside late validation steps.
- Define a custom term by source, processing route, representation, and role in the next step. For example, define a mask by how it is generated, what its values mean, and how it constrains the model.
- Distinguish a runtime method from a preparation stage. Model training, rule-template maintenance, database construction, calibration, and sample labeling are preparation stages unless the claims make them required runtime steps.
- Write method steps as executable data flow: input object -> operation -> intermediate result -> use in next step.
- Write system/device embodiments as module mapping. State that modules may be software, hardware, or a combination, and that modules may be merged or split while performing the same functions.
- Write electronic-device and storage-medium embodiments as carrier embodiments. Do not restate the whole method unless needed for support; refer back to the method embodiment and identify processor, memory, program instructions, and execution result.
- Avoid importing an example's narrow scenario into claim support. Mark concrete sports, product types, thresholds, model architectures, and deployment forms as examples unless the claims require them.
- Keep the inventive path visible in every major part: data transformation, rule/model cooperation, validation, feedback, and output.

## Output Checklist

Before finishing, verify:

- every independent method step has a concrete implementation and output;
- every dependent feature is integrated into the relevant method paragraph or preparation paragraph;
- every custom term used in claims has a definition or an understandable first-use explanation;
- system modules map cleanly to method steps without creating unsupported extra modules;
- electronic-device and storage-medium paragraphs support the corresponding claims without bloating the section;
- examples are concrete enough for enablement but not written as mandatory limitations;
- training/preparation and runtime generation are not confused.
