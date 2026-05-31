# Cross-Platform Patent Skill Installation

## For Claude Code

### Option 1: Global User Skills (Recommended)

```bash
# Copy skills to Claude Code global skills directory
mkdir -p ~/.claude/skills
cp -r /Users/chrynos/.codex/patent-skills-backup/universal/patent-cn ~/.claude/skills/
cp -r /Users/chrynos/.codex/patent-skills-backup/universal/patent-cn-draft ~/.claude/skills/
cp -r /Users/chrynos/.codex/patent-skills-backup/universal/patent-cn-response ~/.claude/skills/
cp -r /Users/chrynos/.codex/patent-skills-backup/universal/patent-cn-review ~/.claude/skills/
cp -r /Users/chrynos/.codex/patent-skills-backup/universal/patent-cn-doctor ~/.claude/skills/
cp -r /Users/chrynos/.codex/patent-skills-backup/universal/code2patent ~/.claude/skills/

# Copy CLAUDE.md for global rules
cp /Users/chrynos/.codex/patent-skills-backup/universal/CLAUDE.md ~/.claude/CLAUDE.md
```

### Option 2: Plugin (For Distribution)

Create a plugin structure:
```
patent-workflow-plugin/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── patent-cn/
│   │   └── SKILL.md
│   ├── patent-cn-draft/
│   │   └── SKILL.md
│   ├── patent-cn-response/
│   │   └── SKILL.md
│   ├── patent-cn-review/
│   │   └── SKILL.md
│   ├── patent-cn-doctor/
│   │   └── SKILL.md
│   └── code2patent/
│       └── SKILL.md
├── hooks/
│   └── hooks.json
├── CLAUDE.md
└── README.md
```

Plugin manifest (`.claude-plugin/plugin.json`):
```json
{
  "name": "patent-workflow",
  "version": "2.0.0",
  "description": "Chinese patent workflow automation",
  "skills": [
    "skills/patent-cn",
    "skills/patent-cn-draft",
    "skills/patent-cn-response",
    "skills/patent-cn-review",
    "skills/patent-cn-doctor",
    "skills/code2patent"
  ]
}
```

## For OpenAI Codex

### Symlink Strategy (Recommended)

```bash
# Create symlinks from Codex skills directory to universal skills
CODEX_SKILLS="/Users/chrynos/.codex/skills"
UNIVERSAL="/Users/chrynos/.codex/patent-skills-backup/universal"

# Symlink each skill
for skill in patent-cn patent-cn-draft patent-cn-response patent-cn-review patent-cn-doctor code2patent; do
  ln -sfn "$UNIVERSAL/$skill" "$CODEX_SKILLS/$skill"
done

# Copy hooks to Codex hooks directory
cp "$UNIVERSAL/hooks/hooks.json" "/Users/chrynos/.codex/hooks/hooks.json"
```

### Direct Copy

```bash
# Copy skills directly to Codex skills directory
CODEX_SKILLS="/Users/chrynos/.codex/skills"
UNIVERSAL="/Users/chrynos/.codex/patent-skills-backup/universal"

for skill in patent-cn patent-cn-draft patent-cn-response patent-cn-review patent-cn-doctor code2patent; do
  cp -r "$UNIVERSAL/$skill" "$CODEX_SKILLS/$skill"
done
```

## For Cursor

```bash
# Copy to Cursor skills directory
CURSOR_SKILLS=".cursor/skills"
mkdir -p "$CURSOR_SKILLS"

for skill in patent-cn patent-cn-draft patent-cn-response patent-cn-review patent-cn-doctor code2patent; do
  cp -r "/Users/chrynos/.codex/patent-skills-backup/universal/$skill" "$CURSOR_SKILLS/$skill"
done
```

## Verification

After installation, verify skills are discoverable:

### Claude Code
```bash
# In Claude Code, the skills should appear in the skill list
# Test with: /patent-cn
```

### Codex
```bash
# Verify skills exist
ls -la /Users/chrynos/.codex/skills/patent-cn/
ls -la /Users/chrynos/.codex/skills/patent-cn-draft/
```

## Notes

- The SKILL.md files are identical across platforms
- Hooks use the same format but may need path adjustments
- CLAUDE.md rules apply globally in Claude Code
- For Codex, the rules are embedded in each SKILL.md
