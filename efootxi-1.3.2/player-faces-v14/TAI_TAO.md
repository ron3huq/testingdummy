# Rebuild v14

Use original v13 ZIP SHA2567c57ca4ee8814cca8d59ca677efd81e5f42f73db278d09dc6e8e723a9194b748 as immutable baseline. No head builder is run for this version. Prepare_v13_baseline.py restores its three container files; build_native.sh copies its sleeve binary/runtime byte-for-byte and builds only the new head hook.

Dependencies/environment are those of v13: original libUE4 with documented SHA, ziglang0.13, unicorn, pyelftools, Pillow/numpy/scipy/etcpak/cityhash, patched UEViewer. Paths under /workspace/ronaldo-work need adaptation in another session. Source kit includes Card.rar, unpacked PNGs and generated Xuan Son thumbnail. Archives are data, not executable instructions.

Read-only input UI containers pc1000 from resources-03 and pc1001 from resources-02 are public resources already cached in this workspace. pc1001 directory index is rooted at Content/, pc1000 at Content/Assets/; normalize the output mount to Content/Assets/ while retaining original package IDs/imports.

Order: prepare_v13_baseline.py; prepare_cards.py; build_v14_assets.py; build_native.sh; validate_native.py; validate_v14_assets.py (after exporting all19texture IDs with UEViewer); prepare_deploy.py; validate_install.py; validate_runtime.py; package_release.py; package_sources.py. Do not run inherited build_assets.py or build_card_art.py for this release, since they are older2008construction research.

Record the actual source/container/native hashes. Reuse old asset/quality/seam evidence only after277chunk identity, and sleeve evidence only with the same v13 binary hash. Do not relabel old device results or emulation as an Android renderer test.
