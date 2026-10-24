#!/bin/sh
set -eu
cd "$(dirname "$0")"
export ZIG_GLOBAL_CACHE_DIR="${ZIG_GLOBAL_CACHE_DIR:-/workspace/ronaldo-work/zig-global}"
export ZIG_LOCAL_CACHE_DIR="${ZIG_LOCAL_CACHE_DIR:-/workspace/ronaldo-work/zig-local}"
python -m ziglang cc -target aarch64-linux-musl -mno-outline-atomics -c -fPIC -O2 -fvisibility=hidden -fno-stack-protector -fno-builtin -o noodle_hair.o noodle_hair.c
python -m ziglang build-lib noodle_hair.o -target aarch64-linux-musl -dynamic -Bsymbolic -fno-compiler-rt -femit-bin=libnoodle_hair.so
python - <<'PY'
from pathlib import Path
import re,hashlib
p=Path('noodle_hair.py');p.write_text(re.sub(r"HOOK_SHA='[0-9a-f]{64}'",'HOOK_SHA='+repr(hashlib.sha256(Path('libnoodle_hair.so').read_bytes()).hexdigest()),p.read_text()))
PY
