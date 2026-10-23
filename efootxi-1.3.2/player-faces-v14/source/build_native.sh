#!/bin/sh
set -eu
cd "$(dirname "$0")"
export ZIG_GLOBAL_CACHE_DIR="${ZIG_GLOBAL_CACHE_DIR:-/workspace/ronaldo-work/zig-global}"
export ZIG_LOCAL_CACHE_DIR="${ZIG_LOCAL_CACHE_DIR:-/workspace/ronaldo-work/zig-local}"
python -m ziglang cc -target aarch64-linux-musl -mno-outline-atomics -c -fPIC -O2 -fvisibility=hidden -fno-stack-protector -fno-builtin -o noodle_hair.o noodle_hair.c
python -m ziglang build-lib noodle_hair.o -target aarch64-linux-musl -dynamic -Bsymbolic -fno-compiler-rt -femit-bin=libnoodle_hair.so
python - <<'PYBASE'
from pathlib import Path
import zipfile,hashlib
baseline=Path('../../player-faces-v13/Faces-v13-13-cards.zip')
assert hashlib.sha256(baseline.read_bytes()).hexdigest()=='7c57ca4ee8814cca8d59ca677efd81e5f42f73db278d09dc6e8e723a9194b748'
with zipfile.ZipFile(baseline) as z:
 for n in ['libselect_team.so','select_team_runtime.py','myleague_editor_runtime.py']:Path(n).write_bytes(z.read('work/tools/'+n))
PYBASE
