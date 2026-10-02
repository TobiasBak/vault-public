#!/usr/bin/env bash
# Link every skills/<name>/ into each agent skill directory.
# Default target ~/.agents/skills serves Codex and Pi; dotfiles links ~/.claude/skills to it.
# Override with SKILLS_TARGETS="dir1:dir2". Without --fix, mismatches are errors.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_ROOT="$REPO_ROOT/skills"

if [[ "${OS:-}" == "Windows_NT" ]] || uname -s | grep -qiE 'mingw|msys|cygwin'; then
  powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$(cygpath -w "$REPO_ROOT/scripts/install-skills.ps1")" ${1:+-Fix}
  exit $?
fi

FIX=0
[[ "${1:-}" == "--fix" ]] && FIX=1
IFS=':' read -ra TARGETS <<< "${SKILLS_TARGETS:-$HOME/.agents/skills}"

mapfile -t NAMES < <(find "$SKILLS_ROOT" -mindepth 2 -maxdepth 2 -name SKILL.md -printf '%h\n' | xargs -n1 basename | sort)

for target_dir in "${TARGETS[@]}"; do
  mkdir -p "$target_dir"
  for name in "${NAMES[@]}"; do
    source="$SKILLS_ROOT/$name"
    target="$target_dir/$name"
    if [ -L "$target" ] && [ "$(realpath "$target")" = "$(realpath "$source")" ]; then
      echo "OK: $target"
      continue
    fi
    if [ -e "$target" ] || [ -L "$target" ]; then
      [ "$FIX" -eq 1 ] || { echo "Wrong or unmanaged entry: $target. Re-run with --fix." >&2; exit 1; }
      rm -rf "$target"
    fi
    ln -s "$source" "$target"
    echo "Linked: $target -> $source"
  done
  # Remove links into this repo whose skill no longer exists.
  for target in "$target_dir"/*; do
    [ -L "$target" ] || continue
    case "$(readlink "$target")" in
      "$SKILLS_ROOT/"*)
        [ -f "$target/SKILL.md" ] && continue
        [ "$FIX" -eq 1 ] || { echo "Stale link: $target. Re-run with --fix." >&2; exit 1; }
        rm "$target"; echo "Removed stale: $target" ;;
    esac
  done
done
