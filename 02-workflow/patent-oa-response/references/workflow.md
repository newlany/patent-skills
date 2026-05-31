# 审查意见答复工作流

Read this file together with:

- `core/invariants.md`
- `core/state-model.md`
- `core/checkpoints.md`
- `checks/seven-rule-check.md` when inventive-step or QC work is in scope
- `rendering/docx-templates.md` when formal `.docx` output is in scope

## 总流程

1. Stage 1 establishes the application-side fact baseline from the claims, specification, abstract, examples, comparative examples, and figures.
2. Stage 2 restores the office action into issue units, evidence layers, and reasoning chains.
3. Stage 3 verifies D1 against the examiner's attribution using the original text.
4. Stage 4 verifies each Dx separately for disclosure, function identity, and combination fit.
5. Build the preliminary current-claim-1-vs-D1 difference snapshot for amendment-decision use only.
6. Stage 5 evaluates whether amendment is needed, compares amendment paths, and waits for confirmation before fixing the live amendment decision.
7. If amendment is adopted, fix the final amended claim 1 and rebuild the full current effective claim set; if amendment is rejected, fix the current unamended claim set as the effective claim set.
8. Propose the final distinguishing features for the current effective claim set and wait for confirmation.
9. Propose the actual technical problem for the current effective claim set and wait for confirmation.
10. Stage 6 runs the three-step method and the seven-rule check on the current effective claim set only.
11. If amendment is adopted and a claims replacement-page template exists, generate the replacement-page `.docx` after the full amended claim set and numbering are fixed.
12. Stage 7 or Stage 8 drafts the formal response from the fixed case state and, when needed, fills the correct `.docx` template.
13. Stage 9 performs final consistency and risk review before submission.

## 可自动处理

- 文件阅读和技术事实整理
- 审查意见结构化拆解
- D1 和 Dx 的公开性、作用和结合难度核查
- 数据、实施例和对比例整理
- 缺失对比文件或本申请公开文本时，先调用 [$download-google-patents-pdfs](../../download-google-patents-pdfs/SKILL.md) 完成准备
- 基于既定模板的 `.docx` 排版填充

## 必经确认闸门

- 是否改权
- 改权时采用哪一路径
- 最终修改后的权利要求1文本
- 现行有效权利要求对应的最终区别技术特征
- 现行有效权利要求对应的实际解决的技术问题
- 敏感案件中的关键正式答复措辞

## 阶段衔接纪律

- 初步区别分析只服务于是否改权的判断，不得直接充当最终区别技术特征。
- 一旦现行有效权利要求组变化，所有基于旧权利要求组的最终区别技术特征、技术问题和论证主线都要重新检查。
- 改权案件在正式答复前必须先固定完整现行权利要求书，并统一后续权利要求编号和引用关系。
- 正式答复起草只能从已经固定的现行有效权利要求组出发。

## 成文与提交

- 先在纯文本中完成正文，再按 `rendering/docx-templates.md` 的映射规则填入模板。
- 有修改案件使用有修改模板；无修改案件使用无修改模板。
- 替换页、正式答复、现行权利要求、区别技术特征和技术问题必须保持一致。

## 提交前固定检查

1. 技术问题是否带入了区别特征
2. 区别特征是否与当前有效权利要求一致
3. 技术效果是否有说明书依据
4. 修改说明是否足以支撑专利法第33条
5. 结尾结论是否与前文论证力度匹配
