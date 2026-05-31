#!/usr/bin/env python3
"""
Patent Skills Sync Tool
Syncs skills between GitHub repo and local Claude Code / Codex directories.

Usage:
    python3 sync_patent_skills.py status
    python3 sync_patent_skills.py pull [--skills SKILLS] [--target TARGET] [--force]
    python3 sync_patent_skills.py push [--message MSG] [--skills SKILLS] [--dry-run]
    python3 sync_patent_skills.py diff [--skills SKILLS]
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Configuration
REPO_URL = "https://github.com/newlany/patent-skills"
REPO_BRANCH = "main"
LOCAL_CLONE = Path("/Users/chrynos/.codex/patent-skills-backup")
CLAUDE_SKILLS = Path.home() / ".claude" / "skills"
CODEX_SKILLS = Path.home() / ".codex" / "skills"

# Skills to sync (from universal/ directory)
UNIVERSAL_SKILLS = [
    "patent-cn",
    "patent-cn-draft",
    "patent-cn-response",
    "patent-cn-review",
    "patent-cn-doctor",
    "code2patent",
    "patent-skills-sync",
]

PROXY = {
    "http": "http://127.0.0.1:7897",
    "https": "http://127.0.0.1:7897",
}


def run_git(args, cwd=None):
    """Run a git command and return output."""
    env = os.environ.copy()
    env.update(PROXY)
    result = subprocess.run(
        ["git"] + args,
        cwd=cwd or str(LOCAL_CLONE),
        capture_output=True,
        text=True,
        env=env,
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def ensure_clone():
    """Ensure the local clone exists and is up to date."""
    if not (LOCAL_CLONE / ".git").exists():
        print(f"Error: Local clone not found at {LOCAL_CLONE}")
        print("Please clone the repo first:")
        print(f"  git clone {REPO_URL} {LOCAL_CLONE}")
        sys.exit(1)


def get_skill_source(skill_name):
    """Get the source path for a skill in the universal directory."""
    return LOCAL_CLONE / "universal" / skill_name


def install_skill(skill_name, target, force=False):
    """Install a skill to the target platform via symlink."""
    source = get_skill_source(skill_name)
    if not source.exists():
        print(f"  [SKIP] {skill_name}: source not found at {source}")
        return False

    if target in ("claude", "all"):
        dest = CLAUDE_SKILLS / skill_name
        _link_skill(source, dest, "Claude Code", force)

    if target in ("codex", "all"):
        dest = CODEX_SKILLS / skill_name
        _link_skill(source, dest, "Codex", force)

    return True


def _link_skill(source, dest, platform, force):
    """Create a symlink from source to dest."""
    if dest.is_symlink():
        if dest.resolve() == source.resolve():
            print(f"  [OK] {dest.name} -> {platform} (already linked)")
            return
        if force:
            dest.unlink()
        else:
            response = input(f"  [WARN] {dest.name} exists in {platform}. Overwrite? [y/N] ")
            if response.lower() != "y":
                print(f"  [SKIP] {dest.name} -> {platform}")
                return
            dest.unlink()
    elif dest.exists():
        if force:
            shutil.rmtree(dest)
        else:
            response = input(f"  [WARN] {dest.name} exists in {platform} (not a symlink). Overwrite? [y/N] ")
            if response.lower() != "y":
                print(f"  [SKIP] {dest.name} -> {platform}")
                return
            shutil.rmtree(dest)

    dest.parent.mkdir(parents=True, exist_ok=True)
    os.symlink(source, dest)
    print(f"  [LINKED] {dest.name} -> {platform}")


def cmd_status(args):
    """Show sync status."""
    ensure_clone()

    print("=" * 60)
    print("Patent Skills Sync Status")
    print("=" * 60)
    print(f"Repository: {REPO_URL}")
    print(f"Local clone: {LOCAL_CLONE}")
    print()

    # Check git status
    code, out, _ = run_git(["status", "--porcelain"])
    if out:
        print("[LOCAL CHANGES]")
        for line in out.split("\n")[:10]:
            print(f"  {line}")
    else:
        print("[LOCAL] Clean, no uncommitted changes")
    print()

    # Check remote
    code, out, _ = run_git(["fetch", "--dry-run", "origin"])
    if "From" in out:
        print("[REMOTE] New changes available on GitHub")
    else:
        print("[REMOTE] Up to date")
    print()

    # Check each skill
    print("[SKILLS]")
    for skill in UNIVERSAL_SKILLS:
        source = get_skill_source(skill)
        claude_link = CLAUDE_SKILLS / skill
        codex_link = CODEX_SKILLS / skill

        status_parts = []
        if source.exists():
            status_parts.append("source OK")
        else:
            status_parts.append("source MISSING")

        if claude_link.is_symlink():
            if claude_link.resolve() == source.resolve():
                status_parts.append("claude: linked")
            else:
                status_parts.append("claude: WRONG TARGET")
        elif claude_link.exists():
            status_parts.append("claude: copy (not symlink)")
        else:
            status_parts.append("claude: not installed")

        if codex_link.is_symlink():
            if codex_link.resolve() == source.resolve():
                status_parts.append("codex: linked")
            else:
                status_parts.append("codex: WRONG TARGET")
        elif codex_link.exists():
            status_parts.append("codex: copy (not symlink)")
        else:
            status_parts.append("codex: not installed")

        print(f"  {skill}: {', '.join(status_parts)}")

    print()
    print("=" * 60)


def cmd_pull(args):
    """Pull latest from GitHub and install to local directories."""
    ensure_clone()

    skills = args.skills.split(",") if args.skills else UNIVERSAL_SKILLS
    target = args.target or "all"
    force = args.force

    print("Pulling latest from GitHub...")
    code, out, err = run_git(["pull", "origin", REPO_BRANCH])
    if code != 0:
        print(f"Error pulling: {err}")
        sys.exit(1)
    print(f"  {out}")
    print()

    print("Installing skills...")
    for skill in skills:
        skill = skill.strip()
        install_skill(skill, target, force)

    print()
    print("Pull complete.")


def cmd_push(args):
    """Push local changes to GitHub."""
    ensure_clone()

    skills = args.skills.split(",") if args.skills else None
    message = args.message or f"Update patent skills ({datetime.now().strftime('%Y-%m-%d %H:%M')})"
    dry_run = args.dry_run

    # Check for changes
    code, out, _ = run_git(["status", "--porcelain"])
    if not out:
        print("No changes to push.")
        return

    # Filter to specific skills if requested
    if skills:
        filtered_lines = []
        for line in out.split("\n"):
            for skill in skills:
                if skill.strip() in line:
                    filtered_lines.append(line)
                    break
        if not filtered_lines:
            print(f"No changes found for skills: {skills}")
            return
        out = "\n".join(filtered_lines)
        print("Changes found:")
        print(out)
    else:
        print("Changes found:")
        print(out)

    print()

    if dry_run:
        print("[DRY RUN] Would commit and push the above changes.")
        return

    # Stage changes
    if skills:
        for skill in skills:
            run_git(["add", f"universal/{skill.strip()}/"])
    else:
        run_git(["add", "-A"])

    # Commit
    code, out, err = run_git(["commit", "-m", message])
    if code != 0:
        print(f"Error committing: {err}")
        sys.exit(1)
    print(f"Committed: {out}")

    # Push
    code, out, err = run_git(["push", "origin", REPO_BRANCH])
    if code != 0:
        print(f"Error pushing: {err}")
        sys.exit(1)
    print(f"Pushed: {out}")

    print()
    print("Push complete.")


def cmd_diff(args):
    """Show differences between local and remote."""
    ensure_clone()

    skills = args.skills.split(",") if args.skills else UNIVERSAL_SKILLS

    # Fetch latest
    run_git(["fetch", "origin"])

    for skill in skills:
        skill = skill.strip()
        code, out, _ = run_git(["diff", "--stat", f"origin/{REPO_BRANCH}", "--", f"universal/{skill}/"])
        if out:
            print(f"[{skill}]")
            print(out)
            print()

    if not any(True for _ in []):
        # Check local uncommitted changes
        code, out, _ = run_git(["diff", "--stat", "--"] + [f"universal/{s.strip()}/" for s in skills])
        if out:
            print("[LOCAL UNCOMMITTED]")
            print(out)
        else:
            print("No differences found.")


def main():
    parser = argparse.ArgumentParser(description="Patent Skills Sync Tool")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # status
    subparsers.add_parser("status", help="Show sync status")

    # pull
    pull_parser = subparsers.add_parser("pull", help="Pull from GitHub and install locally")
    pull_parser.add_argument("--skills", help="Comma-separated list of skills to sync")
    pull_parser.add_argument("--target", choices=["claude", "codex", "all"], default="all",
                             help="Target platform (default: all)")
    pull_parser.add_argument("--force", action="store_true", help="Overwrite without asking")

    # push
    push_parser = subparsers.add_parser("push", help="Push local changes to GitHub")
    push_parser.add_argument("--message", "-m", help="Commit message")
    push_parser.add_argument("--skills", help="Comma-separated list of skills to push")
    push_parser.add_argument("--dry-run", action="store_true", help="Show what would be pushed")

    # diff
    diff_parser = subparsers.add_parser("diff", help="Show differences")
    diff_parser.add_argument("--skills", help="Comma-separated list of skills to check")

    args = parser.parse_args()

    if args.command == "status":
        cmd_status(args)
    elif args.command == "pull":
        cmd_pull(args)
    elif args.command == "push":
        cmd_push(args)
    elif args.command == "diff":
        cmd_diff(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
