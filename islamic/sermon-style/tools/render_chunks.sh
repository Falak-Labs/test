#!/bin/bash
cd /home/claude/build/sermon
export REMOTION_CHROME=/usr/bin/google-chrome
N=16450; S=4120
for i in 0 1 2 3; do
  a=$((i*S)); b=$(( (i+1)*S-1 )); [ $b -ge $N ] && b=$((N-1))
  out=work/long01/part_$i.mp4
  [ -s $out ] && continue
  npx remotion render Long work/long01/tmp_part_$i.mp4 --muted --concurrency=2 --frames=$a-$b --browser-executable=/usr/bin/google-chrome > work/long01/render_$i.log 2>&1 && mv work/long01/tmp_part_$i.mp4 $out || { echo "chunk $i failed"; exit 1; }
  echo "chunk $i done"
done
echo ALLDONE
