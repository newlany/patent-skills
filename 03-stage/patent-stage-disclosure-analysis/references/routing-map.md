# 技术交底分析路由表

对外交底分析只保留 `patent-stage-disclosure-analysis` 这一个公开 skill。

## 路由规则

- 用户要 `01_技术交底分析报告`
  - 读取 `stages/01-analysis-report.md`
- 用户要 `02_技术交底逻辑重构与缺陷审查报告`
  - 读取 `stages/02-defect-review.md`
- 用户要 `03_需要发明人补充说明的问题清单`
  - 读取 `stages/03-supplement-questions.md`
- 用户要整套交底分析
  - 按 `01 -> 02 -> 03` 顺序执行

## 补充规则

- 如果用户只要求后续某一份文档，不强制重跑前面的全部阶段。
- 但如果前序文档明显缺失或基线不稳，要明确指出风险。
- 如果 disclosure 是公式敏感或版式敏感 Word 文件，先配合 `$patent-support-docx-math`。
