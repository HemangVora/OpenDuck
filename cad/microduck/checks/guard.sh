#!/bin/bash
# run a command, kill it if its memory passes LIMIT_MB (default 4000) — keeps the 16 GB Mac usable
LIMIT_MB=${LIMIT_MB:-4000}
nice -n 10 "$@" & P=$!
while kill -0 $P 2>/dev/null; do
  R=$(ps -o rss= -p $P 2>/dev/null | tr -d ' '); R=${R:-0}
  if [ $((R/1024)) -gt $LIMIT_MB ]; then echo "GUARD: killed at $((R/1024)) MB" >&2; kill -9 $P; exit 99; fi
  sleep 1
done
wait $P
