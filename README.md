# Patent Skills Backup & Organization

## Date: 2026-05-30

## What's Here

This folder contains a reorganized, deduplicated, and optimized version of all patent-related skills from the original `~/.codex/skills/` directory.

### Directory Structure

```
patent-skills-backup/
├── README.md                    # This file
├── DEDUPLICATION-REPORT.md      # What was merged/removed and why
├── WORKFLOW-CONSTRAINTS.md      # Constraint architecture design
├── universal/                   # Optimized skills (cross-platform)
│   ├── CLAUDE.md                # Global rules for Claude Code
│   ├── INSTALL.md               # Installation instructions
│   ├── install.sh               # Automated installer
│   ├── patent-cn/               # Main router
│   ├── patent-cn-draft/         # Drafting orchestrator
│   ├── patent-cn-response/      # Response orchestrator
│   ├── patent-cn-review/        # Review orchestrator
│   ├── patent-cn-doctor/        # System health check
│   ├── code2patent/             # Code-to-patent pipeline
│   └── hooks/                   # Workflow enforcement hooks
├── 01-entry/                    # Original entry points (6 skills)
├── 02-workflow/                 # Original workflow orchestrators (8 skills)
├── 03-stage/                    # Original stage specialists (10 skills)
├── 04-method/                   # Original method specialists (8 skills)
├── 05-support/                  # Original support skills (6 skills)
├── 06-qc/                       # Original QC skills (3 skills)
├── 07-research/                 # Original research skills (2 skills)
├── 08-doc-output/               # Original document output (2 skills)
├── 09-tools/                    # Original runtime infrastructure (1 skill)
└── *.toml                       # Original agent definitions (11 files)
```

### Quick Start

1. **Read the deduplication report**: `DEDUPLICATION-REPORT.md`
2. **Read the constraint design**: `WORKFLOW-CONSTRAINTS.md`
3. **Install universal skills**: `cd universal && ./install.sh all`

### Key Improvements

1. **Deduplication**: Removed 7 redundant skills, kept best implementations
2. **Proper SKILL.md format**: All skills use Claude Code frontmatter with `allowed-tools`, `hooks`, `user-invocable`
3. **Stage gate enforcement**: Hooks block writes to later stages if earlier stages incomplete
4. **Completion validation**: Hooks block completion declarations without validation
5. **Artifact registration reminders**: Hooks remind agent to register artifacts in manifest
6. **Cross-platform compatibility**: Skills work in Claude Code, Codex, and Cursor via symlinks

### Original Skills (Unchanged)

The `01-entry/` through `09-tools/` directories contain exact copies of the original skills. The `*.toml` files are the original agent definitions. Nothing in the original `~/.codex/skills/` directory was modified.

### Agents

The 11 `.toml` agent files define a linear drafting pipeline:
```
file_intake_specialist → disclosure_analyst → prior_art_searcher →
solution_reconstructor → claim_drafter → spec_writer → application_qc
```

With parallel specialists for:
- OA response (`oa_responder`)
- Invalidity (`invalidity_strategist`)
- Topic research (`topic_researcher`)
- Overall orchestration (`drafting_orchestrator`)
