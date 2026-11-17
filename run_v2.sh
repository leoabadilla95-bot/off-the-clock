#!/bin/bash
# run_v2.sh <ep...>: full v2 rebuild per episode: table + captions, new keyframes, voices (sets timing), animatic, soundtrack
cd "$(dirname "$0")"
python build_v2.py > /dev/null && python v2_jobs.py
for e in "$@"; do
  echo "== episode $e"
  timeout 900 python gen_agnes.py $e $e | tail -2
  V2=1 timeout 900 python gen_voices.py $e 2>&1 | grep -E 'episode|created|runtime|wrote|Error'
  V2=1 python animatic.py $e
  V2=1 timeout 900 python gen_sound.py $e 2>&1 | grep -E 'skip|wrote|Error'
done
