---
name: patent-cn-response
version: 2.0.0
description: |
  Public orchestrator for Chinese patent response work. Use for 审查意见答复、D1/D2/D3分析、创造性答复、
  补正通知书、替换页、无效答辩、无效宣告、口审准备. Routes internally to OA, correction, invalidity,
  fixed-patent analysis, PDF bundle, and DOCX specialists.
  Trigger phrases: "审查意见", "OA", "答复", "无效", "补正", "口审", "替换页", "意见陈述".
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Agent
  - AskUserQuestion
hooks:
  PreToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: |
            # Enforce template compliance for 意见陈述
            if echo "$TOOL_INPUT_FILE_PATH" | grep -q "意见陈述"; then
              echo "REMINDER: 意见陈述 must use the mandated template, not be built from scratch"
            fi
  Stop:
    - hooks:
        - type: command
          command: |
            # Block if response draft exists but no QC
            if echo "$AGENT_OUTPUT" | grep -qi "意见陈述.*完成\|response.*complete"; then
              echo "REMINDER: Ensure replacement pages generated and QC passed"
            fi
---
# CN Patent Response Orchestrator

## Role

Public response-work entry. Handles procedural matters after or outside initial drafting.

Use for:
- OA response (审查意见答复)
- D1/D2/D3 analysis
- Claim amendment strategy
- Correction notices (补正通知书) and replacement pages
- Invalidity requests or responses (无效宣告)
- Oral hearing preparation (口审准备)

## Startup

Always read:
- [references/response-routing.md](references/response-routing.md)

## Response Type Routing

| Response Type | Internal Workflow |
|--------------|-------------------|
| OA response | `patent-entry-oa-response` |
| Correction notice | `patent-support-correction-docx` |
| Invalidity | `patent-entry-invalidity` |

Support specialists:
- `patent-analysis-fixed-patent` for claim-focused comparison
- `patent-support-google-patents-pdfs` for cited-document collection
- `patent-support-docx-math` for DOCX/formula support

## OA Response Workflow Gates

```
Stage 1: OA Breakdown
  INPUT:  OA notice exists
  OUTPUT: OA issues extracted + D1/Dx identified
  GATE:   breakdown complete → Stage 2

Stage 2: D1/Dx Verification
  INPUT:  Stage 1 gate passed
  OUTPUT: comparison documents downloaded + verified
  GATE:   verification complete → Stage 3

Stage 3: Amendment Decision
  INPUT:  Stage 2 gate passed
  OUTPUT: strategy decided (amend or argue)
  GATE:   decision made → Stage 4

Stage 4: Response Drafting
  INPUT:  Stage 3 gate passed
  OUTPUT: 意见陈述 draft using mandated template
  GATE:   draft exists → Stage 5

Stage 5: Replacement Pages & QC
  INPUT:  Stage 4 gate passed
  OUTPUT: replacement pages + QC passed
  GATE:   QC passed → Completion
```

## OA Case Folder Layout

```
<case-folder>/
  01-审查意见/
  02-申请文件/
  03-既往答复/
  04-对比文件/
  05-处理结果/
  06-提交文件/
  记录/
```

## Template Compliance

When producing 意见陈述 DOCX:
1. Use `意见陈述-有修改.docx` when claims are amended
2. Use `意见陈述-无修改.docx` when argument-only
3. Copy the template, then fill/replace sections
4. Preserve template section settings, styles, numbering definitions
5. Never rebuild from scratch

## Output Protocol

```
CN RESPONSE ROUTE
- response type: <oa|correction|invalidity|unknown>
- confidence: <high|medium|low>
- internal workflow: <skill>
- first required material: <file>
- first output: <artifact>
```

Continue when confidence is high or medium. Ask one question when low.
