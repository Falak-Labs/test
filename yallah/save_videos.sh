#!/usr/bin/env bash
# Put finished Shorts where they are used.      bash yallah/save_videos.sh <lab|media>
# Expects got/<dialect><lesson>/ as yallah/make.py left it, one folder per dialect, and GH_TOKEN with write access.
#   lab    everything there is to look at goes to the yallah-lab branch under produce/<dialect><lesson>/ (tests)
#   media  only videos whose report says ok go to the yallah-media branch, where the posting links point
set -euo pipefail
DEST="$1"
case "$DEST" in lab) BR=yallah-lab;; media) BR=yallah-media;; *) echo "dest must be lab or media"; exit 1;; esac
ls got/*/report.json >/dev/null 2>&1 || { echo "nothing was made"; exit 1; }
URL="https://x-access-token:${GH_TOKEN}@github.com/${GITHUB_REPOSITORY}.git"
for attempt in 1 2 3 4; do
  rm -rf br
  if ! git clone -q --depth 1 --branch "$BR" "$URL" br 2>/dev/null; then
    mkdir br && ( cd br && git init -q && git checkout -q --orphan "$BR" && git remote add origin "$URL" )
  fi
  ( cd br && git config user.name "github-actions[bot]" && git config user.email "41898282+github-actions[bot]@users.noreply.github.com" )
  for d in got/*/; do
    slug="$(basename "$d")"
    ok="$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['ok'])" "$d/report.json")"
    if [ "$DEST" = lab ]; then
      mkdir -p "br/produce/$slug"
      for f in "$d"/yallah-say-*.mp4 "$d/report.json" "$d/sheet.jpg" "$d/page/script.js" "$d/page/tl.js"; do
        [ -e "$f" ] && cp "$f" "br/produce/$slug/"
      done
      echo "$slug: ok=$ok, copied to produce/$slug"
    elif [ "$ok" = True ]; then
      cp "$d"/yallah-say-*.mp4 br/
      echo "$slug: published"
    else
      echo "$slug: NOT published, its report has problems"
    fi
  done
  ( cd br && git add -A && { git diff --cached --quiet && echo "nothing new" || git commit -q -m "yallah videos ($DEST) $(date -u +%Y-%m-%dT%H:%MZ) [skip ci]"; } )
  if ( cd br && git push -q origin "HEAD:refs/heads/$BR" ); then echo "saved to $BR"; exit 0; fi
  sleep $((RANDOM % 6 + 2))
done
echo "could not save"; exit 1
