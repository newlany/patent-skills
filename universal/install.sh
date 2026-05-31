#!/bin/bash
# Cross-platform patent skill installer
# Usage: ./install.sh [claude|codex|cursor|all]

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS=("patent-cn" "patent-cn-draft" "patent-cn-response" "patent-cn-review" "patent-cn-doctor" "code2patent")

install_claude() {
    echo "Installing for Claude Code..."
    CLAUDE_SKILLS="$HOME/.claude/skills"
    mkdir -p "$CLAUDE_SKILLS"

    for skill in "${SKILLS[@]}"; do
        if [ -d "$SCRIPT_DIR/$skill" ]; then
            ln -sfn "$SCRIPT_DIR/$skill" "$CLAUDE_SKILLS/$skill"
            echo "  Linked: $skill -> $CLAUDE_SKILLS/$skill"
        fi
    done

    # Copy CLAUDE.md if it doesn't exist
    if [ ! -f "$HOME/.claude/CLAUDE.md" ]; then
        cp "$SCRIPT_DIR/CLAUDE.md" "$HOME/.claude/CLAUDE.md"
        echo "  Copied CLAUDE.md"
    else
        echo "  CLAUDE.md already exists, skipping"
    fi

    echo "Claude Code installation complete."
}

install_codex() {
    echo "Installing for OpenAI Codex..."
    CODEX_SKILLS="$HOME/.codex/skills"
    mkdir -p "$CODEX_SKILLS"

    for skill in "${SKILLS[@]}"; do
        if [ -d "$SCRIPT_DIR/$skill" ]; then
            ln -sfn "$SCRIPT_DIR/$skill" "$CODEX_SKILLS/$skill"
            echo "  Linked: $skill -> $CODEX_SKILLS/$skill"
        fi
    done

    # Copy hooks
    if [ -f "$SCRIPT_DIR/hooks/hooks.json" ]; then
        mkdir -p "$HOME/.codex/hooks"
        cp "$SCRIPT_DIR/hooks/hooks.json" "$HOME/.codex/hooks/hooks.json"
        echo "  Copied hooks.json"
    fi

    echo "Codex installation complete."
}

install_cursor() {
    echo "Installing for Cursor..."
    CURSOR_SKILLS=".cursor/skills"
    mkdir -p "$CURSOR_SKILLS"

    for skill in "${SKILLS[@]}"; do
        if [ -d "$SCRIPT_DIR/$skill" ]; then
            ln -sfn "$SCRIPT_DIR/$skill" "$CURSOR_SKILLS/$skill"
            echo "  Linked: $skill -> $CURSOR_SKILLS/$skill"
        fi
    done

    echo "Cursor installation complete."
}

case "${1:-all}" in
    claude)
        install_claude
        ;;
    codex)
        install_codex
        ;;
    cursor)
        install_cursor
        ;;
    all)
        install_claude
        install_codex
        install_cursor
        ;;
    *)
        echo "Usage: $0 [claude|codex|cursor|all]"
        exit 1
        ;;
esac

echo ""
echo "Installation complete. Skills are now available as symlinks."
echo "To verify, check the skill directories in each platform."
