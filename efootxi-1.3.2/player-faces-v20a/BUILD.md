# v20a crash hotfix

Requires the v20 package beside this directory, its prior source/research workspace and the same original libUE4.so (SHA `3da06a36fb5c434a75c5739af65f16664347477bd653659eb354376410d52f98`). Use the v20 Python dependencies and Zig 0.13.0. These tests require the restored `/workspace/ronaldo-work` engine/source corpus; they are not standalone phone tools.

With the v20 virtual environment activated:

```sh
sh source/build_native.sh
python source/validate_squad_abi.py
python source/validate_trampoline_hints.py
python source/validate_v20.py
python source/validate_install.py
python source/package_release.py
```

`validate_squad_abi.py` compares the original v20 native binary with the rebuilt hotfix. It executes the actual native prologue, all 15 stack argument reads, the argument16 (zero-based) FString dereference at `0x3883628`, and the original epilogue. It deliberately skips the other builder logic and does not validate the GPU or complete squad integration. The zero virtual page is unmapped to model Android NULL protection despite loading the engine at link addresses for emulation.

Only changes from v20:

- Correct extended card converter callback from 10 to 23 scalar/pointer arguments. Register arguments x0..x7 and caller stack SP+0..0x70 are preserved.
- Trampoline candidates intersect whole mapping gaps with B instruction reachability, covering holes whose start was previously out of range. No MAP_FIXED; returned addresses are still checked.
- Report attempted/installed entries and detailed allocation errors. Keep module handle early so partial installation can be disabled on error.
- Distinct runtime version `player-faces-v20a-squad-abi-fix`; native checksum and bundle metadata updated.

No asset/container, editor overlay, select-team module, font or player policy changes. The release ZIP replaces exactly three files. It requires installed v20 and does not change manifest revision or asset hashes.

The exact original device exception remains unconfirmed without a native stack trace. This fixes a reproducible ABI defect consistent with crashing during the converter before its post-call counter increments. Neither all device crashes nor the four black faces are claimed resolved by host tests.
