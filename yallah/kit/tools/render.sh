#!/bin/bash
# render3.sh <first_piece> <last_piece>: render pieces of episode 1 (520 frames each), two at a time.
# A piece is written under a temporary name and only renamed when ffmpeg exits 0 (shoot.py does that).
set -u
cd /home/claude/video
NF=${NF:?}; PER=520; mkdir -p ${OUTD:?}/vid
one() {
  i=$1; a=$((i * PER)); n=$PER; [ $((a + n)) -gt $NF ] && n=$((NF - a))
  out=$(printf "${OUTD}/vid/p%02d.mp4" "$i")
  [ -s "$out" ] && { echo "$out kept"; return; }
  python3 tools/shoot.py video ${PAGE:?} "$out" "$(python3 -c "print($a/30)")" "$(python3 -c "print($n/30)")" 2>&1 | tail -1
}
export -f one; export NF PER PAGE OUTD
seq "$1" "$2" | xargs -P 2 -I{} bash -c 'one {}'
