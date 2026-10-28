set -e
export ZIG_GLOBAL_CACHE_DIR=/tmp/ui712-zig-global ZIG_LOCAL_CACHE_DIR=/tmp/ui712-zig-local
py=/workspace/.setup-testingdummy/venv/bin/python
for unit in select_team noodle_hair; do
 "$py" -m ziglang cc -target aarch64-linux-musl -mno-outline-atomics -c -fPIC -O2 -fvisibility=hidden -fno-stack-protector -fno-builtin /workspace/73-ui712/build/native/$unit.c -o /workspace/73-ui712/build/$unit.o
 "$py" -m ziglang build-lib /workspace/73-ui712/build/$unit.o -target aarch64-linux-musl -dynamic -Bsymbolic -fno-compiler-rt -femit-bin=/workspace/73-ui712/build/apk/assets/gateway-release/work/tools/lib$unit.so
done
