# Specification Section Style For Software/AI Method Claim Packages

Use these rules when drafting or revising `背景技术`, `发明内容`, and `具体实施方式` for Chinese software, AI, algorithm, data-processing, or computer-implemented patents arranged as method + system/device + electronic device + storage medium.

## Overall Strategy

- Use a low-to-high problem ladder. The background states the lowest defensible technical problem. The invention content explains the claimed solution. The technical effects carry the deeper inventive advancement.
- Do not over-admit the prior art in the background. If the case can be framed as manual, unstable, inefficient, or poorly matched to actual operating conditions, use that as the background defect. Put close prior-art comparison later in the effect reasoning.
- Make every section solve the same case, but at different depth:
  - `背景技术`: what goes wrong in actual use.
  - `发明内容`: what solution is claimed and why it helps.
  - `具体实施方式`: how the data, rules, model, validation, feedback, system modules, and carriers actually run.
- Preserve claim scope. Do not introduce a narrow product type, model architecture, sports scene, threshold, or deployment form as mandatory unless it is claimed.

## 背景技术

- State the application scene first, then the practical defect. For AI/software cases, a good background often starts from the conventional manual or experience-based workflow rather than an admitted close algorithmic solution.
- Avoid saying the prior art already has the same automatic generation route unless the user instructs this or the application must acknowledge it.
- Keep the technical problem broad enough for independent-claim support. For example, write that manual design makes the pattern and force-bearing region match unstable and actual grip/slip resistance weaker, instead of listing later dependent-feature defects such as validation failure, frozen-region iteration, or vectorized engineering export.
- Write natural field observation. Reduce strings like `准确性、稳定性、高效性、一致性`; use complete sentences that show how the problem arises.
- Avoid marketing or litigation tone. Do not write that current methods are `无法` or `完全不能` unless supported.

## 发明内容

- Start with a purpose paragraph aligned to the background defect.
- Add an `申请人发现` paragraph when the defect needs mechanism analysis. Explain why the manual or prior route fails in actual workflow, not just that it fails.
- The first solution paragraph follows the independent claim feature order. Keep claim terms unchanged.
- The first effect block may be two or three short paragraphs when the independent method is complex:
  - transform the core input into model-usable conditions;
  - explain rule/model/sample/validation cooperation;
  - compare with possible existing routes and state the further solved problem.
- Hide the real inventive point in effect reasoning. Prefer wording like:
  - `本方案并非仅仅解决如何利用人工智能工具进行...的问题，而是在...基础上，进一步...`
  - `即使已有技术能够...，其重点通常仍停留在...；本方案进一步解决的是...`
- Do not write `创造性来源在于` or `本案具有创造性` in the application text.
- Keep dependent-feature effects short. Each effect should answer: this feature changes what intermediate handling, and what practical consequence follows.
- Use restrained patent wording: `有利于`、`可以减少`、`较为稳定`、`进一步改善`、`降低...可能性`. Avoid unsupported absolutes such as `显著提高`、`彻底解决`、`大幅提升`.
- Match a user-provided style sample when available:
  - one longer but readable patent sentence is acceptable;
  - avoid rigid step inventory;
  - reduce multiple `、`-connected noun clusters;
  - prefer `并非仅仅...而是...` for the main contribution, and simpler `上述设计中...` for dependent effects.

## 具体实施方式

- Use the layout in `layout-template.md`: method thick, system mapped, carrier concise.
- Define custom terms before heavy use. For each custom term, state source, processing route, representation, and role in the next step.
- For complex AI methods, high-priority definitions include:
  - raw data or sensing result;
  - design coordinate system or alignment space;
  - functional region;
  - mask, label map, gradient map, boundary constraint, or spatial control condition;
  - structured prompt, rule template, conflict priority, and rule field;
  - training or fine-tuning samples;
  - candidate output, validation result, feedback field, frozen region, and engineering output file.
- Separate preparation from runtime. Rule-library construction, model training, sample labeling, calibration, and coordinate-template setup are preparation stages unless the claim makes them runtime steps.
- Write the runtime method as executable data flow: input -> operation -> intermediate result -> use in next operation.
- Give extra detail to bottlenecks that carry the inventive route, such as coordinate registration, rule matching, model input construction, validation, feedback regeneration, and output transformation.
- The system embodiment maps modules to method steps. State logical division and allow software, hardware, firmware, or combinations.
- Electronic-device and storage-medium embodiments should be concise carrier support. Refer back to the method embodiments instead of restating every method step.

## Style Checks

- Background does not over-concede close prior art.
- The purpose paragraph is solvable by the independent claim.
- The first effect block contains the deeper comparison and advancement, not the background.
- Effects are linked to recited features, not to unclaimed wish-list benefits.
- Custom terms are defined before or near first substantive use.
- Long lists connected by `、` have been reduced where natural prose is clearer.
- Carrier embodiments support the claims without bloating the specification.
