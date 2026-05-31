# OA Stage Routing Map

Use this map to route a request to one stage unless the user clearly wants the full workflow.

| Stage | Typical requests | Must already be fixed | Primary outputs | Reference |
| --- | --- | --- | --- | --- |
| 1 | case baseline, 事实基线, 申请文件拆解 | none beyond application files | application-side fact baseline and support tables | `stages/01-case-baseline.md` |
| 2 | office-action breakdown, 审查意见拆解, 论证链恢复 | office action text | issue matrix and reasoning map | `stages/02-review-breakdown.md` |
| 3 | D1 check, D1核查 | D1 text and the cited office-action passages | D1 disclosure findings and Rule-2 pre-check | `stages/03-d1-check.md` |
| 4 | Dx check, D2/D3 核查 | each Dx text and the cited office-action passages | Dx disclosure, function, and combination-fit findings | `stages/04-dx-check.md` |
| 5 | claim amendment, 是否改权, 修改方案 | preliminary current-claim-1-vs-D1 difference snapshot | amendment recommendation, options, and amended-claim candidates | `stages/05-claim-amendment.md` |
| 6 | inventive-step analysis, 创造性主线 | current effective claim set and confirmed distinguishing features | feature-effect-problem map and ranked inventive-step lines | `stages/06-inventive-step.md` |
| 7 | amended draft, 修改后答复, replacement-page generation | final amended claim set, confirmed distinguishing features, confirmed technical problem | amended response draft and, when needed, replacement-page output | `stages/07-draft-amended.md` |
| 8 | unamended draft, 不修改答复 | current effective unamended claim set, confirmed distinguishing features, confirmed technical problem | unamended response draft | `stages/08-draft-unamended.md` |
| 9 | QC, 质检, 提交前审校 | near-final or final draft | prioritized issue list and fix directions | `stages/09-qc.md` |

If the user asks for a drafting stage without a fixed effective claim set, state the missing baseline and risk before proceeding.
If the user asks for inventive-step synthesis without confirmed distinguishing features for the current effective claim set, stop and obtain or reconstruct that baseline first.
