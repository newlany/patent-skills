---
name: patent-skills-sync
version: 1.0.0
description: |
  Sync patent skills between GitHub repo and local directories. Supports pull (GitHub → local),
  push (local → GitHub), status check, and selective sync. Works with both Claude Code and Codex.
  Trigger phrases: "同步技能", "sync skills", "更新技能", "pull skills", "push skills",
  "技能同步", "skill sync", "拉取技能", "推送技能".
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - AskUserQuestion
---
# Patent Skills Sync

## Role

Synchronize patent skills between the GitHub repository and local skill directories.
Ensures Claude Code (`~/.claude/skills/`) and Codex (`~/.codex/skills/`) always have the latest versions.

## Repository

- **GitHub**: `https://github.com/newlany/patent-skills`
- **Branch**: `main`
- **Local clone**: `/Users/chrynos/.codex/patent-skills-backup`

## Commands

### Check Status

Compare local skills with GitHub version:

```bash
python3 /Users/chrynos/.codex/patent-skills-backup/universal/patent-skills-sync/scripts/sync_patent_skills.py status
```

### Pull (GitHub → Local)

Download latest skills from GitHub and install to local directories:

```bash
python3 /Users/chrynos/.codex/patent-skills-backup/universal/patent-skills-sync/scripts/sync_patent_skills.py pull
```

Options:
- `--skills patent-cn,patent-cn-draft` — only sync specific skills
- `--target claude` — only install to Claude Code
- `--target codex` — only install to Codex
- `--target all` — install to both (default)
- `--force` — overwrite local changes without asking

### Push (Local → GitHub)

Upload local skill changes to GitHub:

```bash
python3 /Users/chrynos/.codex/patent-skills-backup/universal/patent-skills-sync/scripts/sync_patent_skills.py push
```

Options:
- `--message "description"` — commit message
- `--skills patent-cn` — only push specific skills
- `--dry-run` — show what would be pushed without actually pushing

### Diff

Show differences between local and GitHub:

```bash
python3 /Users/chrynos/.codex/patent-skills-backup/universal/patent-skills-sync/scripts/sync_patent_skills.py diff
```

## Workflow

### Typical Pull Flow
```
1. Fetch latest from GitHub
2. Compare with local clone
3. Copy changed files to ~/.claude/skills/ and/or ~/.codex/skills/
4. Report what was updated
```

### Typical Push Flow
``1. Detect local changes in the clone directory
2. Stage changed files
3. Commit with descriptive message
4. Push to GitHub
```

## Proxy Support

If behind a firewall, the script automatically detects and uses the proxy:
- `http://127.0.0.1:7897` (default local proxy)
- Or set `https_proxy` / `http_proxy` environment variables

## Skill Directories

The sync targets these local directories:

| Platform | Directory | Install Method |
|----------|-----------|----------------|
| Claude Code | `~/.claude/skills/` | Symlink |
| Codex | `~/.codex/skills/` | Symlink |

## Selective Sync

To sync only specific skills:

```bash
# Only pull the drafting skills
python3 scripts/sync_patent_skills.py pull --skills patent-cn,patent-cn-draft,patent-cn-response

# Only push changes to the QC skills
python3 scripts/sync_patent_skills.py push --skills patent-cn-review,patent-qc-cn-formality --message "Updated QC rules"
```

## Conflict Handling

- **Pull**: By default, asks before overwriting local changes. Use `--force` to skip confirmation.
- **Push**: Only pushes if there are actual changes. Reports conflicts if remote has changed.
- **Status**: Shows which skills are ahead, behind, or diverged.

## Boundaries

- This skill only syncs the `universal/` skills (the optimized versions)
- Original skills in `01-entry/` through `09-tools/` are not synced to local directories
- Agent `.toml` files are synced separately if needed
