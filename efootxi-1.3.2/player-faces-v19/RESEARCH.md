# V19 evidence and remaining uncertainty

## Phone evidence

The user confirmed that v17 comparison changed the four originally failing cards to the ND06 head and removed black rendering on those exact cards. V18 restored their own shapes/textures while cloning ND06 mesh prefixes, face MICs and Texture2D headers. The user now reports v18 still black. Thus card IDs can render a known working head stack; neither a particular texture defect nor duplicate geometry is proven. Prior material-object/name/parent counters did not test pixel output. V19 must not be described as a device-verified cure.

The latest screenshot also proves Vietnam nationality appeared while Milan and Serie A persisted. V18 record+0x140 no-club setter did not cover the actual card presentation data.

## Separate native common head

Original engine SHA256 remains3da06a36fb5c434a75c5739af65f16664347477bd653659eb354376410d52f98.

Native setter0x39c6b18 has a branch that installs the private head in actor+0x228 and subsequently installs actor+0x1900 (m_skcommon_mesh) into attachment[0] from actor+0x1a70 at0x39c6c94..0x39c6cac. The previous guard only matched secondary.mesh==private.mesh. Its zero duplicate-candidate counter therefore did not exclude a separate original head.

V19 examines ONLY this declared attachment, ONLY the four failing full Card IDs, ONLY when its mesh equals actor+0x1900 and differs from the successfully bound private head. Accepted FNames are exactly SK_Base_Face or SK_<actor original Face ID>[native profile suffix]_Face; a body mesh name is rejected. FName values are queried through native0x4414bec; no fabricated FName/path identity is written. Diagnostic name conversion uses0x4415ac8(FName*,FString*) and the engine allocator free0x42cc968. The original face string is never changed.

SK_Base_Face was exported independently: native head/neck and eyelash geometry, not torso/limbs. Its lower LOD has747 vertices/1222 triangles. A CPU occlusion comparison did NOT cleanly separate all good and bad heads, so it is not causal proof. The generated bRenderInDepthPass setter0x62fc300 (UHT property0x977afa0) proves depth flag bit19 atPrimitiveComponent+0x210; native CastShadow0x58e771c proves bit28. V19 clears depth bit19 and notifies MarkRenderStateDirty0x5887ef0, and uses native SetRenderInMainPass0x58ef708 and SetCastShadow0x58e771c on the accepted old attachment, leaving the private head visible and leaving animation/font configuration intact. The change is recorded and restored on actor reuse/disabled engine callbacks. The background Python poller never calls renderer methods. Shared bookkeeping uses the existing lock; renderer calls occur outside it. A real device result is still required. Existing v16 CSM guard remains; no shader bytecode is manufactured.

## Card UI affiliations

UHT metadata0x92f5f40..0x92f6018 defines PlayerCardData playerId+0x20, team+0x28, backTeam+0x2c, isTeamNational+0x30, competition+0x34, nationality+0x38; preference team+0x10c is also copied by builder0x38809bc. That builder sources initial team through0x7a88370 and unpacks it with >>14. Hence clearing the unrelated master-record team field alone is insufficient.

The GamePlan copy is built by0x330ae54(self,info,type,index,out): full ID atout+0x10; event-theme team+0x40, initial team+0x48, competition+0x50, initial club+0x54, club competition+0x58, initial national+0x5c, national competition+0x60, nation+0x64. Hooks call the original delegate unchanged, then modify only the finished presentation copy and only the six requested full Vietnam IDs or Speed. Jersey names/fonts, stats, identities, squads and saved rosters are untouched by these new hooks.

Unpacked no-team sentinel is0x3ffff (native packed0xffffffff >>14); absent competition0. Country internal codes remain Vietnam38 and Portugal228, not flag IDs231/49. Speed uses Al Nassr18961, verified against decoded Team.bin and the existing e_018961_r emblem assets. Team.bin has1600-byte rows, English name+396 and team ID+12; it identifies Sparta Rotterdam351 and Al Nassr18961. New UI behavior remains unverified on phone.

## Kits and reproducibility

Only native T_u0351p1_Uni_D and T_u0351p2_Uni_D packages are overridden. Their original package IDs, dependency-store entries, property headers, dimensions1024 and one-level mip layout are preserved. Every one of299 existing private-container asset chunks remains byte-identical to v18. The two source FTEX files are BC7,5120-square, with valid full-resolution levels and broken small-mip data. decode_ftex_top.py recovers the valid top level and deliberately ignores the bad small mips; build_sparta_kits.py resamples/natively encodes the two full atlases. Independent UEViewer readback equals the ETC2 decoder pixels exactly. This proves container/bitmap decoding, not actual uniform shader UV placement. No special body/kit geometry is invented. White home maps p1; supplied teal third maps p2. Source DDS exceeded the tool transfer limit32MiB and was not opened.

The source ZIP includes the two FTEX inputs, minimal SHA-pinned native Sparta template chunks/store records and scripts. It does not need another phone-file upload. The pinned v18 ZIP already in this repository reconstructs the prior container. Original engine/resource initialization is still required for native and UEViewer checks; old absolute workspace paths are not portable dependencies.

Rebuild: prepare_v18_source.py; prepare_country_sources.py; decode_ftex_top.py; build_sparta_kits.py; build_native.sh; validate_v19.py; prepare_deploy.py; validate_install.py; validate_runtime.py; verify_assets.py; package_release.py. Use Python3.12 with Pillow,numpy,etcpak,texture2ddecoder,cityhash,cryptography,pyelftools,unicorn,ziglang0.13; the restored original engine and patched UEViewer are used for checks. v19-reader links original resource containers plus the new private pc9298 container.

752 native cases include completed UI-copy whole-buffer comparisons with guards/full64 negative IDs/disabled behavior, original delegate argument forwarding, exact secondary head/body rejection, idempotence and actor-reuse restoration. The original main/shadow setters and generated depth SetBit execute; all eight combinations of their original flags are checked for suppression/restoration without changing unrelated bits. FName allocator/material/UI-source boundaries are modeled. Fourteen Python hook installations and worker startup execute against modeled mappings. Manifest version advances37 once and remains idempotent. Gateway2441 bytes and the existing selector/sleeve/font overlay remain unchanged. No phone renderer or GPU was run. Keep all device_verified fields false.
