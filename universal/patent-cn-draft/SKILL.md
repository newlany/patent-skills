---
name: patent-cn-draft
version: 2.0.0
description: |
  Public orchestrator for Chinese patent application drafting from technical disclosure to draft package.
  Use for 交底分析、查新、方案重构、创造性判断、权利要求书、说明书、附图、QC.
  Supports guided/autonomous execution with case manifest management.
  Trigger phrases: "撰写", "drafting", "交底", "申请文件", "权利要求", "说明书", "专利申请".
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
            # Enforce stage ordering: claims cannot be written before search
            if echo "$TOOL_INPUT_FILE_PATH" | grep -q "04_权利要求"; then
              MANIFEST="$(dirname "$TOOL_INPUT_FILE_PATH")/../../../manifest.json"
              if [ -f "$MANIFEST" ]; then
                SEARCH_STATUS=$(jq -r '.stages.search.status // "pending"' "$MANIFEST")
                if [ "$SEARCH_STATUS" != "completed" ]; then
                  echo "BLOCKED: Cannot write claims before prior-art search is complete (status: $SEARCH_STATUS)"
                  exit 1
                fi
              fi
            fi
  PostToolUse:
    - matcher: "Write"
      hooks:
        - type: command
          command: |
            # Remind to register artifact in manifest
            if echo "$TOOL_INPUT_FILE_PATH" | grep -q "输出/"; then
              echo "REMINDER: Register artifact via patent_workflow.py add-artifact"
            fi
  Stop:
    - hooks:
        - type: command
          command: |
            # Block completion without validation
            if echo "$AGENT_OUTPUT" | grep -qi "filing-ready\|drafting-complete"; then
              if ! echo "$AGENT_OUTPUT" | grep -q "validate"; then
                echo "BLOCKED: Must run patent_workflow.py validate before declaring completion"
                exit 1
              fi
            fi
---
# CN Patent Drafting Orchestrator

## Role

User-facing drafting orchestrator. Owns the drafting workflow graph and dispatches internal specialists.

Use for new Chinese application drafting from:
- 技术交底书
- 发明人说明
- 研发材料
- 技术方案草稿
- inventor interview notes

Do NOT use for OA response, invalidity, correction-only work, or standalone DOCX repair.

## Mandatory Workflow Sequence

```
Stage 1: Disclosure Analysis (交底分析)
  ├── INPUT:  disclosure file exists
  ├── WORK:   patent-stage-disclosure-analysis
  ├── OUTPUT: 01_技术交底分析报告.md, 02_逻辑重构报告.md, 03_发明人问题清单.md
  └── GATE:   all 3 reports exist → Stage 2

Stage 2: Prior-Art Search (现有技术检索)
  ├── INPUT:  Stage 1 gate passed
  ├── WORK:   patent-stage-prior-art-search
  ├── OUTPUT: search memo, closest reference, drafting quality assessment
  └── GATE:   search memo exists + closest reference identified → Stage 3

Stage 3: Solution Reconstruction (方案重构)
  ├── INPUT:  Stage 1 + Stage 2 gates passed
  ├── WORK:   case route decision + inventive-step strategy
  ├── OUTPUT: drafting strategy package
  └── GATE:   strategy package exists → Stage 4

Stage 4: Claims (权利要求书)
  ├── INPUT:  Stage 3 gate passed
  ├── WORK:   claim drafting with feature breakdown
  ├── OUTPUT: claims draft + Claim 1 feature breakdown
  └── GATE:   claims exist + feature breakdown done → Stage 5

Stage 5: Specification (说明书)
  ├── INPUT:  Stage 4 gate passed + claims stable
  ├── WORK:   background + invention content + embodiments
  ├── OUTPUT: all specification sections
  └── GATE:   all sections exist → Stage 6

Stage 6: QC (质检)
  ├── INPUT:  all Stage 1-5 gates passed
  ├── WORK:   consistency check + formal check + validation
  ├── OUTPUT: QC report with no hard-fail
  └── GATE:   validation passed → Completion
```

## Case-Type Routing (Stage 3 Decision)

After disclosure analysis and prior-art search, determine case type:

| Case Type | Route To |
|-----------|----------|
| Material/formula/process/parameter | `patent-method-process-route` |
| Control/identification/matching/closed-loop | `patent-method-runtime-boundary` |
| Formula/model/simulation/optimization | `patent-method-formula-model` |
| Structural/device/product/component | `patent-entry-drafting` (default) |
| Software/AI/algorithm | `patent-cn-software-embodiment-layout` |
| Anta method cases | `anta-method-patent-agent` |

## Startup

Always read:
- [references/drafting-workflow-graph.md](references/drafting-workflow-graph.md)
- [references/case-workspace-layout.md](references/case-workspace-layout.md)
- [references/stage-contracts.md](references/stage-contracts.md)
- [references/stop-conditions.md](references/stop-conditions.md)

## Runtime Commands

Initialize case:
```bash
python3 patent_workflow.py init --case-dir <case-dir> --title "<title>" --source <source> --mode guided
```

Per stage:
```bash
python3 patent_workflow.py stage-start --case-dir <case-dir> --stage <stage> --json
python3 patent_workflow.py stage-report --case-dir <case-dir> --stage <stage> --name <name> --status completed --json
python3 patent_workflow.py add-artifact --case-dir <case-dir> --stage <stage> --path <path> --kind <kind> --stage-status completed --json
python3 patent_workflow.py stage-end --case-dir <case-dir> --stage <stage> --status completed --json
```

Before completion:
```bash
python3 patent_workflow.py validate --case-dir <case-dir> --json
```

## Output Protocol

At start:
```
CN DRAFTING PLAN
- execution mode: <guided|autonomous>
- case folder: <path>
- route confidence: <high|medium|low>
- stage graph: intake → disclosure → search → reconstruction → claims → specification → QC
- first deliverable: <artifact>
```

At each stage boundary:
```
STAGE BOUNDARY REPORT
- stage: <name>
- status: completed|blocked|failed
- artifacts: <list>
- confirmed findings: <list>
- suspected issues: <list>
- assumptions: <list>
- blockers: <list or none>
- next stage: <name>
```

## Completion Terms

- `drafting-complete`: all required artifacts exist, validation has no hard-fail
- `filing-ready`: final DOCX/package present, validation has no hard or soft fail

Do NOT call a text draft `filing-ready`.

## Reference Drafting Quality Carryover

At search checkpoints, require `patent-stage-prior-art-search` to evaluate drafting quality of comparison documents. High-quality references may be used as style aids only. Never copy unsupported technical content.
