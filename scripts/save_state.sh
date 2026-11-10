#!/usr/bin/env bash
# Commit this job's changes under state/ on top of the latest main.  Other jobs may have pushed meanwhile, so the
# changed files are re-applied onto a fresh copy of main instead of rebasing (no merge conflicts, no lost code).
#   bash scripts/save_state.sh "commit message" [path ...]      (default path: state)
set -uo pipefail
msg="$1"; shift
paths=("${@:-state}")
git config user.name "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
mapfile -t changed < <(git status --porcelain --untracked-files=all -- "${paths[@]}" | awk '{print $NF}')
[ "${#changed[@]}" -eq 0 ] && { echo "nothing to save"; exit 0; }
tmp="$(mktemp -d)"
for f in "${changed[@]}"; do
  if [ -e "$f" ]; then mkdir -p "$tmp/$(dirname "$f")"; cp -a "$f" "$tmp/$f"; fi
done
for attempt in 1 2 3 4 5; do
  git fetch -q origin main && git reset -q --hard FETCH_HEAD
  for f in "${changed[@]}"; do
    if [ -e "$tmp/$f" ]; then mkdir -p "$(dirname "$f")"; cp -a "$tmp/$f" "$f"; else rm -f "$f"; fi
  done
  git add -A -- "${paths[@]}"
  git diff --cached --quiet && { echo "already up to date"; exit 0; }
  git commit -q -m "$msg"
  git push -q origin HEAD:main && { echo "saved (${#changed[@]} files)"; exit 0; }
  sleep $((RANDOM % 6 + 2))
done
echo "could not save state"; exit 1
