#!/bin/sh
set -eu
cd "$(dirname "$0")"
# Python package ziglang==0.13.0. No Android NDK or libc dependencies.
python -m ziglang cc -target aarch64-linux-musl -c -fPIC -O2 -fvisibility=hidden -fno-stack-protector -fno-builtin -o select_team.o select_team.c
python -m ziglang build-lib select_team.o -target aarch64-linux-musl -dynamic -fno-compiler-rt -femit-bin=libselect_team.so
