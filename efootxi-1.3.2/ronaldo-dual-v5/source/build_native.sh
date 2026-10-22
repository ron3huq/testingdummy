#!/bin/sh
set -eu
cd "$(dirname "$0")"
export ZIG_GLOBAL_CACHE_DIR="${ZIG_GLOBAL_CACHE_DIR:-/workspace/ronaldo-work/zig-global}"
export ZIG_LOCAL_CACHE_DIR="${ZIG_LOCAL_CACHE_DIR:-/workspace/ronaldo-work/zig-local}"
python -m ziglang cc -target aarch64-linux-musl -mno-outline-atomics -c -fPIC -O2 -fvisibility=hidden -fno-stack-protector -fno-builtin -o noodle_hair.o noodle_hair.c
python -m ziglang build-lib noodle_hair.o -target aarch64-linux-musl -dynamic -Bsymbolic -fno-compiler-rt -femit-bin=libnoodle_hair.so
