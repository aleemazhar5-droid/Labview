#!/bin/sh
# Serialise chapter builds when several agents work at once:  sh tools/build_locked.sh 30
cd "$(dirname "$0")/.." && mkdir -p build && exec flock build/.build.lock python3 tools/build.py --only "$@"
