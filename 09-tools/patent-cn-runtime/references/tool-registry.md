# Tool Registry

`tool_registry.json` is the Phase-3 adapter layer between orchestrators and deterministic scripts.

## Principles

- Orchestrators call tools by ID, not by hard-coded script paths.
- Registered tools must produce JSON directly or be wrapped into normalized `patent-tool-run/v1` JSON by the runner.
- Use `--case-dir` whenever the tool run belongs to a case so the runner can log a `script-run` event.
- Use `--result-output` for durable tool-run JSON artifacts.

## Required Entry Fields

Each tool entry should include:

```json
{
  "description": "Human-readable purpose.",
  "category": "workflow|docx|qc|search|figure",
  "stage": "07_qc",
  "script": "/absolute/path/to/script.py",
  "argv": ["{python}", "{script}", "..."],
  "stdout_json": true,
  "required": ["input"]
}
```

`stage` is optional for system-level tools.

## Template Arguments

Supported built-ins:

- `{python}`: current Python executable
- `{script}`: registered script path
- `{case_dir}`: normalized `--case-dir`
- `{input}`: normalized `--input`
- `{output}`: normalized `--output`

Extra template values come from repeated `--arg key=value`.

For list-like positional values, add the key to `split_args`, then pass a shell-like string:

```bash
--arg "publication_numbers=CN101 CN102"
```

## Adding A Tool

1. Prefer an existing script that already supports JSON.
2. Add the registry entry.
3. Run `patent_tool_runner.py describe <tool-id>`.
4. Run a smoke test through `patent_tool_runner.py run`.
5. Add a regression test when the tool is part of a required workflow gate.
