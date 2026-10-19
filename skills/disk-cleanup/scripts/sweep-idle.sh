#!/usr/bin/env bash
# Remove top-level entries of DIR in which nothing was written for MINUTES.
# Dry run by default; --apply removes. --keep takes an extended regex of entry names.
# Makes entries writable first: some tools leave read-only trees (conda metadata).
set -uo pipefail

apply=0 keep='^$'
args=()
while [ $# -gt 0 ]; do
  case $1 in
    --apply) apply=1 ;;
    --keep) keep=$2; shift ;;
    *) args+=("$1") ;;
  esac
  shift
done
[ ${#args[@]} -eq 2 ] || { echo "usage: $0 [--apply] [--keep REGEX] DIR MINUTES" >&2; exit 2; }
dir=${args[0]} minutes=${args[1]}

cd "$dir" || exit 1
shopt -s nullglob dotglob
for entry in *; do
  [[ "$entry" =~ $keep ]] && continue
  [ -n "$(find "$entry" -xdev -mmin "-$minutes" -print -quit 2>/dev/null)" ] && continue
  if [ "$apply" = 1 ]; then
    chmod -R u+w "$entry" 2>/dev/null
    rm -rf -- "$entry" && echo "REMOVED $dir/$entry"
  else
    echo "IDLE $dir/$entry"
  fi
done
