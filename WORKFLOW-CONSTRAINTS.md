# Patent Workflow Constraints & Guardrails

## Problem Statement

Patent workflows fail when agents:
1. Skip mandatory stages (e.g., jump from disclosure to claims without prior-art search)
2. Claim "filing-ready" without running QC
3. Call internal specialists directly instead of through orchestrators
4. Let manifest.json drift from actual artifacts
5. Ignore mandated DOCX templates
6. Produce inconsistent output formats

## Constraint Architecture

### Layer 1: SKILL.md Frontmatter Constraints

Each skill's SKILL.md frontmatter defines:
- `allowed-tools`: Restricts available tools per skill
- `description`: Precise trigger phrases to avoid wrong-skill activation
- `user-invocable`: false for all internal skills (prevents direct user invocation)

### Layer 2: Gate Conditions (Hard Stops)

Every stage transition requires a gate check. If the gate fails, the agent MUST stop.

#### Drafting Workflow Gates

```
Stage 1: Disclosure Analysis
  INPUT GATE:  disclosure file exists AND is readable
  OUTPUT GATE: 01_技术交底分析报告.md exists AND manifest.json updated
  BLOCKS:      Stage 2 (Prior-Art Search)

Stage 2: Prior-Art Search
  INPUT GATE:  disclosure analysis complete (Stage 1 output gate passed)
  OUTPUT GATE: search memo exists AND closest reference identified
  BLOCKS:      Stage 3 (Solution Reconstruction)

Stage 3: Solution Reconstruction
  INPUT GATE:  disclosure analysis + search memo both exist
  OUTPUT GATE: drafting strategy package exists AND case route decided
  BLOCKS:      Stage 4 (Claims)

Stage 4: Claims
  INPUT GATE:  drafting strategy package exists
  OUTPUT GATE: claims draft exists AND Claim 1 feature breakdown done
  BLOCKS:      Stage 5 (Specification)

Stage 5: Specification
  INPUT GATE:  claims draft exists AND is stable
  OUTPUT GATE: background + invention content + embodiments all exist
  BLOCKS:      Stage 6 (QC)

Stage 6: QC
  INPUT GATE:  all Stage 1-5 output gates passed
  OUTPUT GATE: validation has no hard-fail
  BLOCKS:      Completion declaration
```

#### OA Response Workflow Gates

```
Stage 1: OA Breakdown
  INPUT GATE:  OA notice PDF/text exists
  OUTPUT GATE: OA issues extracted AND D1/Dx identified
  BLOCKS:      Stage 2

Stage 2: D1/Dx Verification
  INPUT GATE:  OA breakdown complete
  OUTPUT GATE: comparison documents downloaded AND verified
  BLOCKS:      Stage 3

Stage 3: Amendment Decision
  INPUT GATE:  D1/Dx verification complete
  OUTPUT GATE: amendment strategy decided (amend or argue)
  BLOCKS:      Stage 4

Stage 4: Response Drafting
  INPUT GATE:  amendment strategy decided
  OUTPUT GATE: 意见陈述 draft exists AND uses mandated template
  BLOCKS:      Stage 5

Stage 5: Replacement Pages & QC
  INPUT GATE:  response draft exists
  OUTPUT GATE: replacement pages generated AND QC passed
  BLOCKS:      Completion declaration
```

### Layer 3: Output Contracts

Every skill that produces artifacts must follow these contracts:

#### Manifest Contract
```json
{
  "case_title": "string",
  "case_dir": "string",
  "created_at": "ISO-8601",
  "updated_at": "ISO-8601",
  "execution_mode": "guided|autonomous",
  "route_confidence": "high|medium|low",
  "stages": {
    "<stage_id>": {
      "status": "pending|in_progress|completed|blocked",
      "started_at": "ISO-8601",
      "completed_at": "ISO-8601",
      "artifacts": [
        {
          "path": "relative/path/to/file",
          "kind": "disclosure-analysis|search-memo|claims|specification|...",
          "stage_status": "completed|failed"
        }
      ]
    }
  }
}
```

#### Stage Boundary Report Contract
After every stage, the agent MUST output:
```
STAGE BOUNDARY REPORT
- stage: <stage_name>
- status: completed|blocked|failed
- artifacts created: <list>
- confirmed findings: <list>
- suspected issues: <list>
- assumptions: <list>
- blockers: <list or none>
- next stage: <stage_name>
```

### Layer 4: Hook-Based Enforcement

#### PreToolUse Hook: Stage Order Enforcement
```bash
#!/bin/bash
# hooks/patent-stage-gate.sh
# Runs before Write/Edit tools to validate stage ordering

MANIFEST="$CASE_DIR/manifest.json"
CURRENT_STAGE=$(jq -r '.current_stage' "$MANIFEST" 2>/dev/null)

# Check if trying to write artifacts for a blocked stage
if echo "$TOOL_INPUT" | grep -q "04_权利要求"; then
  if ! jq -e '.stages.search.status == "completed"' "$MANIFEST" >/dev/null 2>&1; then
    echo "BLOCKED: Cannot write claims before prior-art search is complete"
    exit 1
  fi
fi
```

#### PostToolUse Hook: Artifact Registration
```bash
#!/bin/bash
# hooks/patent-artifact-register.sh
# Runs after Write tool to remind agent to register artifact in manifest

if echo "$TOOL_INPUT" | grep -q "输出/"; then
  echo "REMINDER: Register this artifact in manifest.json via patent_workflow.py add-artifact"
fi
```

#### Stop Hook: Completion Validation
```bash
#!/bin/bash
# hooks/patent-completion-gate.sh
# Runs before agent stops to validate completion claims

if echo "$AGENT_OUTPUT" | grep -qi "filing-ready\|drafting-complete"; then
  MANIFEST="$CASE_DIR/manifest.json"
  VALIDATION=$(python3 patent_workflow.py validate --case-dir "$CASE_DIR" --json 2>/dev/null)
  HARD_FAILS=$(echo "$VALIDATION" | jq -r '.hard_fails // 0')
  if [ "$HARD_FAILS" -gt 0 ]; then
    echo "BLOCKED: Cannot declare completion. $HARD_FAILS hard-fail issues remain."
    exit 1
  fi
fi
```

### Layer 5: CLAUDE.md Global Rules

These rules apply to ALL patent skills and cannot be overridden:

```markdown
## Patent Workflow Invariants

1. **Stage ordering is mandatory**: Disclosure -> Search -> Reconstruction -> Claims -> Specification -> QC. No stage may be skipped.

2. **Orchestrator-first**: All patent work MUST enter through `patent-cn`. Never call `patent-entry-*` or `patent-stage-*` skills directly.

3. **Manifest is truth**: Every artifact must be registered in manifest.json. The manifest IS the case state.

4. **Template compliance**: All 意见陈述 DOCX must use the mandated template. All application DOCX must use `专利撰写模板文件.docx`.

5. **Validation before completion**: Never declare `drafting-complete` or `filing-ready` without running `patent_workflow.py validate`.

6. **Chinese naming**: All human-readable files use Chinese names. English only for tool contracts, JSON keys, and script-expected names.

7. **Lazy directory creation**: Only create the immediate parent directory of the file being written. Never pre-create stage folders.

8. **Stop at uncertainty**: When route confidence is low, ask one focused question. Do not guess.

9. **Output format is contract**: Stage boundary reports, manifest entries, and tool-run JSON must follow the defined contracts exactly.

10. **No direct DOCX patching in router**: The router (`patent-cn`) chooses workflows. It does not do drafting, legal argument, or DOCX editing.
```

### Layer 6: Completion Declaration Rules

Only these exact terms may be used:

| Term | Meaning | Gate |
|------|---------|------|
| `drafting-complete` | All draft-stage artifacts exist, no hard-fail in validation | All stage output gates passed |
| `filing-ready` | Final DOCX/package present, no hard or soft fail | All stage output gates + final QC passed |
| `blocked` | Cannot proceed, needs user input | Specific blocker identified |
| `needs-fix` | QC found issues that must be resolved | QC gate failed |

NEVER use: "ready", "done", "complete", "finished" without the exact prefix above.

### Layer 7: Error Recovery Protocol

When a gate fails:
1. Log the failure in `00_case_events.jsonl`
2. Update manifest with `status: "blocked"`
3. State the specific blocker
4. If recoverable: suggest the fix
5. If not recoverable: ask the user for input

When an agent crashes mid-stage:
1. Read manifest.json to determine last completed stage
2. Check `00_case_events.jsonl` for the last event
3. Resume from the last completed stage boundary
4. Do NOT re-run completed stages unless validation explicitly requires it
