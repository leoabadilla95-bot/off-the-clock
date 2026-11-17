#!/bin/bash
# run_v3.sh <ep...>: v2 script + audio plan -> tagged voices, animatic, TV-drama mix
cd "$(dirname "$0")"
python build_v2.py > /dev/null
for e in "$@"; do
  echo "== episode $e"
  V2=1 timeout 1200 python gen_voices.py $e 2>&1 | grep -E 'episode|created|runtime|Error|Traceback' 
  V2=1 python animatic.py $e
  timeout 1800 python mix_v3.py $e 2>&1 | tail -3
done
