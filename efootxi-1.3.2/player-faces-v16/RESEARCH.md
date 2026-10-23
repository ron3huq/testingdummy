# V16 research and limits

## Device evidence

Video Screen_Recording_20261023_121618.mp4 (3.7808s,2340x1080) was decoded with ffmpeg and reviewed at0,1.25,2.75s. Ronaldo2017 skin shows black/red speckling and visible skin triangles; hair and hands retain color. This is compatible with depth/shadow interference but does NOT prove a specific shadow mechanism. No diagnostic packet from the GPU is available. V15 log confirms7680 MQ-parent checks,0 mismatches,3 dynamic MIDs: changing HQ to MQ did not solve the phone bug. All prior renderer-success assumptions are rejected.

## Scoped render change

UHT descriptor0x977b518 bReceiveMobileCSMShadows -> SetBit0x62fc718 sets bit44 of PrimitiveComponent+0x210 (byte0x215/mask0x10). Clear only that bit on a component holding the exact confirmed private head mesh and one of the four black IDs. Notify using0x5887ef0, the actual tail of engine SetCastShadow and SetRenderInMainPass. Do not change bone data or body flags.

Reflected actor arrays: face_components+0x1a80, stencil_shadow_components+0x1ad0. Bounds-check both arrays. A secondary component is changed only if its SkeletalMesh+0x468 equals the exact private head mesh, it differs from selected main component, and main-pass bit18 is set. UHT SetRenderInMainPass exec0x62f3fe0 calls0x58ef708; execute this setter withfalse, retaining cast-shadow flags. Components with a different mesh, including body/boots/arms, are untouched. Native setter body executes in Unicorn; RHI dirty/update boundary is modeled. This is a candidate render fix requiring phone confirmation.

## Native names

Player record constructor0x341ce1c initializes typed XOR identity+0x38 and four adjacent61byte char buffers at0x4c,0x89,0xc6,0x103, ending exactly before data at0x140. Getter0x82a1e48 uses+0x89. Hook lower full-player lookup0x823be04 (v18 already hooks public0x823c8d4). Validate returned identity through0x68fe720 against requested full ID/kind0 and schema(null terminators in all four buffers), then write ONLY these name buffers. Native record diffs verify ID/stat bytes untouched. Wrong ID/kind and invalid string layouts fail closed; no shared baseID/player database edits.

Actor vtable0x90a47a8 slot0x838 resolves0x39bc5d0: FString->UTF8->slot0x720=0x39bc5ac. This native std::string setter only assigns actor+0x16e0 using0x2f46d10. It does not regenerate a rendered jersey texture. V15 late calls therefore were not enough.

Native char setter0x39bc570 and std::string setter0x39bc5ac are intercepted per exact actor ID. More importantly slot0x860=0x39c0420 hashes the FIRST FString in shirt-text render config. At0x39d1538 that config is passed to the key function, then its same FString is copied at0x39d15ec..0x39d1640 into the glyph actor. V16 changes this FString BEFORE hash/cache lookup, preserving remainingfont/color/number metadata. Use engine FStringResizeTo0x286ff60; engine retains buffer ownership. Tests exercise hook ABI/input preservation, but glyph rendering is not a phone verification.

## Art and packaging

All277 head/hair chunks compared byte-for-byte with v15;22 UI textures replaced only, preserving nativeIDs/mips/imports and ETC2 layout. Independent UEViewer PNGs compared with finished source dimensions184x256/128x128. 2006/2008 photo source references are deliberately exchanged;3D heads remain untouched. Original photos used where available, stadium replacement/edit via imagegen. Source sheets are included to make formatting reproducible, not dependent on the old generated_images directory. No neon/faceted background, no baked labels/ratings/stars.

## Rebuild

This is not a standalone toolkit: restore v15 full ZIP to container using prepare_v15_baseline.py; restore original APK/libUE4 and pc1000/pc1001 containers and patched UEViewer as documented in v14/v15. Reuse same venv requirements and Zig0.13. Current entrypoints: prepare_v16_art.py, build_v16_assets.py, build_native.sh, export_v16_assets.py, validate_v16_assets.py, validate_native.py, validate_install.py, prepare_deploy.py, validate_runtime.py, package_release.py, package_sources.py. Inherited older scripts are history and not a run-all workflow.

No claim of100% renderer success: device_verified=false, phone_tested=false. New shadow/record/glyph counters are execution diagnostics, not proof of visible correctness.
