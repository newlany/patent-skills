# Autonomous Mode

This reference defines when the drafting workflow may continue without stopping after every stage.

## Default

The default execution mode is `guided`.

Use `guided` when:

- the user has not explicitly asked for an uninterrupted run
- route selection is uncertain
- claim scope, filing strategy, or applicant instruction is likely to change the downstream work
- the task involves legal/procedural filing decisions rather than drafting support

Initialize guided mode explicitly when useful:

```bash
python3 /Users/chrynos/.codex/skills/patent-entry-drafting/scripts/patent_workflow.py init \
  --case-dir /path/to/case \
  --title "案件名称" \
  --source /path/to/disclosure.docx \
  --mode guided
```

## Autonomous Trigger

Use `autonomous` only when the user clearly asks for continuous drafting, for example:

- “一口气做完初稿”
- “先不要每一步问我”
- “自动跑完整个流程”
- “先给我一个完整 first pass”

Set or switch the mode with:

```bash
python3 /Users/chrynos/.codex/skills/patent-entry-drafting/scripts/patent_workflow.py set-mode \
  --case-dir /path/to/case \
  --mode autonomous \
  --json
```

## Autonomous Responsibilities

In autonomous mode, still keep a visible case trail:

- mark each stage with `stage-start` and `stage-end`
- log script calls, dependency calls, and any manual interruption with `log-event`
- register each stage artifact with `add-artifact`
- use JSON outputs for deterministic helper scripts when available
- keep `00_case_status.md`, `manifest.json`, and `输出/定稿/验证报告.md` current
- run `patent_workflow.py validate --json` before saying the draft is complete
- label assumptions and unresolved facts in the stage memo instead of hiding them in prose

Autonomous mode may produce a complete first-pass drafting package, but it must not silently claim `filing-ready`.

## Stop Conditions

Stop and ask the user before continuing when any of these occur:

- route confidence is low and two drafting routes would produce materially different claim structures
- the closest prior art forces a meaningful claim-scope or fallback-position choice
- the disclosure lacks a critical technical fact needed for enablement, support, or effect
- a formula, parameter range, experiment, or sequence listing cannot be safely interpreted
- applicant/filer identity, inventor information, priority, secrecy review, fee, deadline, or filing-channel facts are needed
- official procedural requirements must be applied and the current source has not been verified
- validation reports a hard fail that cannot be fixed mechanically

When stopping, preserve momentum: state the blocker, show the safest default, and ask only the minimum question needed to continue.
