#!/usr/bin/env bash
# Refresh Matt Pocock's vendored skills byte-identical from upstream.
# Keeps each skill's local agents/openai.yaml and copies the upstream LICENSE in.
# Refuses to overwrite uncommitted changes unless --force.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
declare -A UPSTREAM=(
  [domain-modeling]=skills/engineering/domain-modeling
  [grill-with-docs]=skills/engineering/grill-with-docs
  [grilling]=skills/productivity/grilling
)
PATHS=(); SPARSE=(/LICENSE)
for name in "${!UPSTREAM[@]}"; do PATHS+=("skills/$name"); SPARSE+=("/${UPSTREAM[$name]}"); done

if [[ "${1:-}" != "--force" ]]; then
  pending="$(git -C "$REPO_ROOT" status --short -- "${PATHS[@]}")"
  [ -z "$pending" ] || { echo "Uncommitted changes in vendored skills:" >&2; echo "$pending" >&2; exit 1; }
fi

TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
git clone -q --depth 1 --filter=blob:none --sparse https://github.com/mattpocock/skills "$TMP/repo"
git -C "$TMP/repo" sparse-checkout set --no-cone "${SPARSE[@]}"

for name in "${!UPSTREAM[@]}"; do
  src="$TMP/repo/${UPSTREAM[$name]}"
  [ -f "$src/SKILL.md" ] || { echo "Missing upstream: ${UPSTREAM[$name]}" >&2; exit 1; }
  dest="$REPO_ROOT/skills/$name"
  meta="$TMP/$name.openai.yaml"
  [ -f "$dest/agents/openai.yaml" ] && cp "$dest/agents/openai.yaml" "$meta"
  rm -rf "$dest" && cp -R "$src" "$dest" && cp "$TMP/repo/LICENSE" "$dest/LICENSE"
  [ -f "$meta" ] && mkdir -p "$dest/agents" && cp "$meta" "$dest/agents/openai.yaml"
done

echo "Updated from mattpocock/skills@$(git -C "$TMP/repo" rev-parse --short HEAD). Review:"
git -C "$REPO_ROOT" status --short -- "${PATHS[@]}"
