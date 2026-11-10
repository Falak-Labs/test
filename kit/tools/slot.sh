#!/usr/bin/env bash
# Run a heavy command when one of N slots is free (this box has 2 CPU cores, shared by every agent).
#   tools/slot.sh <command ...>          BIK_SLOTS=2 by default
N=${BIK_SLOTS:-2}
mkdir -p /tmp/bik_slots
while true; do
  for i in $(seq 1 "$N"); do
    exec {fd}>"/tmp/bik_slots/slot$i.lock"
    if flock -n "$fd"; then
      "$@"
      exit $?
    fi
    exec {fd}>&-
  done
  sleep $((RANDOM % 4 + 2))
done
