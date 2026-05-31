# Drafting Workflow Graph

This is the public drafting stage graph. Internal specialists may vary by case type, but the graph should remain stable.

## Stages

| Runtime Stage | Drafting Stage | Main Internal Specialist | Main Artifact |
|---|---|---|---|
| `01_disclosure` | intake and disclosure analysis | `patent-stage-disclosure-analysis` | `输出/过程/01_交底分析/交底分析.md` |
| `02_search` | prior-art Checkpoint A | `patent-stage-prior-art-search` | `输出/过程/02_现有技术检索/检索纪要A.md` |
| `03_reconstruction` | technical-solution reconstruction | `patent-entry-drafting` + route specialist | `输出/过程/03_方案重构/方案重构备忘录.md` |
| `03_reconstruction` | route-specific cleanup | `patent-method-process-route` / `patent-method-formula-model` / `patent-method-runtime-boundary` | `输出/过程/03_方案重构/路线基线.md` |
| `02_search` | prior-art Checkpoint B | `patent-stage-prior-art-search` | `输出/过程/02_现有技术检索/检索纪要B.md` |
| `03_reconstruction` | inventive-step strategy | drafting engine + search baseline | `输出/过程/03_方案重构/创造性策略.md` |
| `04_claims` | claims drafting | drafting engine / claim drafter | `输出/过程/04_权利要求/权利要求当前稿.md` |
| `05_specification` | specification sections | `patent-stage-invention-content`, `patent-stage-embodiments` | `输出/过程/05_说明书/说明书当前稿.md` |
| `06_figures` | figures and figure descriptions | `patent-drawing-generator` | `输出/过程/06_附图/附图说明.md` |
| `07_qc` | QC and validation | `patent-cn-review` internals | `输出/定稿/验证报告.md` |
| `08_filing_package` | package assembly | DOCX/support specialists | `输出/定稿/提交清单.md` |

For both `02_search` checkpoints, the search memo must include a `Reference Drafting Quality` section, or register a companion artifact at `输出/过程/02_现有技术检索/参考文献撰写质量.md`. This artifact follows the case into reconstruction, claims, and specification drafting when high-quality comparison documents are found.

## Checkpoints

Guided mode pauses at:

- after disclosure analysis if critical technical facts are missing
- after Checkpoint A if closest prior art changes the route
- after reconstruction if claim scope choices are strategic
- after Checkpoint B if inventive-step path is weak
- before final package if filing-channel facts or final DOCX choices are needed

Autonomous mode may continue through these points only if no stop condition is triggered.

## Route Specialists

Select by drafting bottleneck:

- process/preparation/material/formulation: `patent-method-process-route`
- formula/model/simulation/optimization: `patent-method-formula-model`
- runtime chain/control/recognition/boundary: `patent-method-runtime-boundary`
- structure/device/product/material structure: remain in the drafting engine and use support specialists as needed
