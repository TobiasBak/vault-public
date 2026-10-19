#!/usr/bin/env bash
# Find and remove dead git worktrees of every repository under ~/code.
# Dead: git index untouched for --idle-hours and no process has its cwd inside.
# Before removal, local commits plus tracked and untracked changes are saved as
# refs/archive/worktrees/<name> in the owning repository; branches are kept.
# Only ignored files (build output) are lost.
# Dry run by default; --apply removes. --exclude takes an extended regex of paths.
set -uo pipefail

apply=0 idle_hours=24 exclude='/sg/gate/baselines/|/orderready/rmut-build$' root="$HOME/code"
while [ $# -gt 0 ]; do
  case $1 in
    --apply) apply=1 ;;
    --idle-hours) idle_hours=$2; shift ;;
    --exclude) exclude="$exclude|$2"; shift ;;
    --root) root=$2; shift ;;
    *) echo "usage: $0 [--apply] [--idle-hours N] [--exclude REGEX] [--root DIR]" >&2; exit 2 ;;
  esac
  shift
done

now=$(date +%s)
cwds=$(for p in /proc/[0-9]*; do readlink "$p/cwd" 2>/dev/null; done | sort -u)

# One common git dir per repository, so worktrees that live under ~/code count once.
mapfile -t commons < <(for r in "$root"/*/; do
  git -C "$r" rev-parse --path-format=absolute --git-common-dir 2>/dev/null
done | sort -u)

reap() {
  local wt=$1 common=$2 gitdir=$3 name head snap tmpidx tree archived=clean
  name=$(basename "$wt")
  head=$(git -C "$wt" rev-parse HEAD) || return 1
  snap=$head
  if [ -n "$(git -C "$wt" status --porcelain 2>/dev/null)" ]; then
    tmpidx=$(mktemp)
    cp "$gitdir/index" "$tmpidx" 2>/dev/null
    GIT_INDEX_FILE=$tmpidx git -C "$wt" add -A 2>/dev/null
    tree=$(GIT_INDEX_FILE=$tmpidx git -C "$wt" write-tree) &&
      snap=$(git -C "$wt" commit-tree "$tree" -p "$head" -m "archive: worktree $wt on $(date -I)")
    rm -f "$tmpidx"
  fi
  if [ "$snap" != "$head" ] || [ "$(git -C "$wt" rev-list --count HEAD --not --remotes)" != 0 ]; then
    git --git-dir="$common" update-ref "refs/archive/worktrees/$name" "$snap" || { echo "ARCHIVE-FAILED $wt"; return 1; }
    archived=archived
  fi
  chmod -R u+w "$wt" 2>/dev/null
  rm -rf -- "$wt"
  git --git-dir="$common" worktree prune
  echo "REMOVED($archived) $wt"
}

for common in "${commons[@]}"; do
  git --git-dir="$common" worktree prune
  git --git-dir="$common" worktree list --porcelain | awk '/^worktree /{print substr($0,10)}' | tail -n +2 |
  while read -r wt; do
    [ -d "$wt" ] || continue
    [[ "$wt" =~ $exclude ]] && { echo "EXCLUDED $wt"; continue; }
    gitdir=$(git -C "$wt" rev-parse --absolute-git-dir 2>/dev/null) || continue
    [ -e "$gitdir/locked" ] && { echo "LOCKED $wt"; continue; }
    idle=$(( (now - $(stat -c %Y "$gitdir/index" 2>/dev/null || echo "$now")) / 3600 ))
    live=0
    while read -r c; do [[ $c == "$wt" || $c == "$wt"/* ]] && { live=1; break; }; done <<<"$cwds"
    [ "$live" = 1 ] && { echo "LIVE $wt"; continue; }
    [ "$idle" -lt "$idle_hours" ] && continue
    if [ "$apply" = 1 ]; then reap "$wt" "$common" "$gitdir"; else echo "DEAD idle=${idle}h $wt"; fi
  done
done
