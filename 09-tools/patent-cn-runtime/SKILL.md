---
name: patent-cn-runtime
description: "Internal runtime and tool adapter layer for the Chinese patent workflow. Use when orchestrators need a unified tool registry, JSON-first script invocation, case event logging, or normalized tool-run outputs for DOCX, QC, search, figure, validation, and doctor tools."
---
# CN Patent Runtime

## Role

This is an internal runtime layer for the `patent-cn` architecture. It is not a normal user-facing drafting or review skill.

Use it when an orchestrator needs to:

- list available deterministic patent tools
- run a tool by stable ID instead of remembering script paths
- force normalized JSON output
- log tool calls into a case event log
- write a tool-run JSON result for later validation or review

## Tool Runner

List tools:

```bash
python3 /Users/chrynos/.codex/skills/patent-cn-runtime/scripts/patent_tool_runner.py list
```

Run a tool:

```bash
python3 /Users/chrynos/.codex/skills/patent-cn-runtime/scripts/patent_tool_runner.py run qc.micro \
  --case-dir <case-dir> \
  --input <draft-file> \
  --result-output <case-dir>/记录/07_质检/工具运行/micro-qc-tool-run.json
```

Describe a tool:

```bash
python3 /Users/chrynos/.codex/skills/patent-cn-runtime/scripts/patent_tool_runner.py describe docx.inspect
```

## Registry

The registry lives at:

```text
scripts/tool_registry.json
```

Read [references/tool-registry.md](references/tool-registry.md) before adding or changing registry entries.

The internal specialist registry lives at:

```text
scripts/specialist_registry.json
```

It records the public `patent-cn-*` entries, the layered routing architecture, remaining internal compatibility entries, internal specialists, adjacent tool skills, and retired alias names.

Use the registry routing fields in this order:

- normalize explicit old skill names through `compatibility_entries`, then `retired_aliases`
- choose a public route from `routing_architecture.public_routes`
- select a stage specialist from `specialists`
- select a delivery specialist from `routing_architecture.delivery_routes`

Specialists that expose `agents/openai.yaml` should set `policy.allow_implicit_invocation` to `false` so the public orchestrators remain the normal entry surface. Retired alias directories should not exist under `skills/`.

## Output Contract

Every runner invocation prints `patent-tool-run/v1` JSON with:

- `tool_id`
- `ok`
- `returncode`
- `command`
- `stdout_json`
- `stderr`
- `outputs`
- optional `case_dir`
- optional `result_output`

If `--case-dir` is provided, the runner logs a `script-run` event via `patent_workflow.py log-event`.
