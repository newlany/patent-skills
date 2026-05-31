---
name: patent-cn
version: 2.0.0
description: |
  Canonical top-level entry for Chinese patent work. Use when the user asks to handle a patent matter:
  drafting, review/QC, OA response, correction, invalidity, prior-art search, research, filing package,
  inventor questions, external communication brief, or system doctor. Routes to patent-cn-draft,
  patent-cn-review, patent-cn-response, patent-cn-doctor, or internal specialists. Trigger phrases:
  "专利", "patent", "交底", "审查意见", "OA", "无效", "补正", "撰写", "查新", "检索", "权利要求", "说明书".
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Agent
  - WebFetch
  - WebSearch
  - AskUserQuestion
hooks:
  PreToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: |
            # Enforce directory layout: files must go under 输出/ or 记录/ or be manifest/config files
            FILE_PATH="$TOOL_INPUT_FILE_PATH"
            if [[ "$FILE_PATH" == *"/"* ]] && [[ "$FILE_PATH" != *"输出/"* ]] && [[ "$FILE_PATH" != *"记录/"* ]] && [[ "$FILE_PATH" != *"manifest.json"* ]] && [[ "$FILE_PATH" != *"00_case"* ]] && [[ "$FILE_PATH" != *".md"* ]]; then
              echo "WARNING: File should be under 输出/ or 记录/ directory"
            fi
  Stop:
    - hooks:
        - type: command
          command: |
            # Block completion if agent declares filing-ready without validation
            if echo "$AGENT_OUTPUT" | grep -qi "filing-ready"; then
              echo "REMINDER: Ensure patent_workflow.py validate was run before declaring filing-ready"
            fi
---
# CN Patent Command Center

## Role

This is the public front door for local Chinese patent work.

Use it when the user says things like:
- "用专利系统处理这个案子"
- "这个交底帮我走流程"
- "检查这套申请文件"
- "处理这个审查意见"
- "看这个专利任务该怎么做"

Do not ask the user to choose among low-level skills unless the task is genuinely ambiguous.

## Architecture Rule

External users see a small product surface:
- `patent-cn`: top-level intent router (THIS SKILL)
- `patent-cn-draft`: new Chinese application drafting
- `patent-cn-review`: filing-draft review and QC
- `patent-cn-response`: OA, correction, and invalidity response routing
- `patent-cn-doctor`: system health and dependency checks

Internal skills (`patent-entry-*`, `patent-stage-*`, `patent-method-*`, `patent-support-*`, `patent-qc-*`) are called ONLY by the above orchestrators, never directly.

## Startup

Always read:
- [references/routing-architecture.md](references/routing-architecture.md)
- [references/intent-routing.md](references/intent-routing.md)
- [references/internal-specialists.md](references/internal-specialists.md)

## Routing Decision

Analyze the user's request and determine:
1. **Intent**: drafting | review | response | doctor | research | support
2. **Confidence**: high | medium | low
3. **Target workflow**: which `patent-cn-*` skill to use

## Routing Output

Before continuing, emit:

```
CN PATENT ROUTE
- normalized request: <translated or none>
- intent: <drafting|review|response|doctor|research|support>
- confidence: <high|medium|low>
- public workflow: <patent-cn-*>
- stage specialists: <skill list or none yet>
- delivery specialists: <skill list or none yet>
- first action: <what will be done next>
```

If confidence is high or medium, continue into the chosen workflow.
If confidence is low, ask one focused question.

## External Communication Routes

For inventor question lists:
1. Route content to `patent-inventor-questions`
2. Route DOCX delivery to `patent-external-brief-docx`

For other external-facing briefs (驳回分析, 复审分析, 检索简报, etc.):
1. Draft content in Markdown first
2. Call `patent-external-brief-docx` only if DOCX needed

## Case Directory Layout

Minimum after initialization:
```
<case-folder>/
  00_case_status.md
  00_case_events.jsonl
  manifest.json
```

Create directories lazily. Use Chinese names for human-readable directories.

## State Discipline

- Use `patent_workflow.py init` or locate existing `manifest.json`
- Create case under `<project-root>/专利工作区/<中文案件名>`
- Register all artifacts in `manifest.json`
- Log events in `00_case_events.jsonl`
- Run validation before completion declarations

## Boundaries

- Do NOT do detailed drafting inside this router
- Do NOT do detailed legal argument inside this router
- Do NOT directly patch DOCX files inside this router
- The router chooses the workflow and hands control to the workflow orchestrator
