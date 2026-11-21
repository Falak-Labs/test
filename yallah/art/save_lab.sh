#!/usr/bin/env bash
# Put a job's pictures on the yallah-lab branch (kept apart from main, so main stays small and nothing there
# is triggered).   bash yallah/art/save_lab.sh <job>      expects the pictures in got/<job>/
set -euo pipefail
JOB="$1"
test -d "got/$JOB" || { echo "no pictures for $JOB"; exit 0; }
git config user.name "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
for attempt in 1 2 3 4; do
  rm -rf lab && git worktree prune
  if git fetch -q --depth=1 origin yallah-lab 2>/dev/null; then
    git worktree add -q --detach lab FETCH_HEAD
  else
    git worktree add -q --detach lab
    ( cd lab && git checkout -q --orphan yallah-lab-new && git rm -rfq . >/dev/null 2>&1 || true )
  fi
  mkdir -p "lab/art/$JOB"
  cp -r "got/$JOB/." "lab/art/$JOB/"
  ( cd lab && git add -A art && { git diff --cached --quiet && echo "nothing new" || git commit -q -m "art lab: $JOB $(date -u +%Y-%m-%dT%H:%MZ) [skip ci]"; } )
  if ( cd lab && git push -q origin HEAD:refs/heads/yallah-lab ); then echo "saved to yallah-lab"; exit 0; fi
  sleep $((RANDOM % 6 + 2))
done
echo "could not save"; exit 1
