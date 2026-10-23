# V13: evidence and limits

The user reports v12 installed but supplied the exact same v11 counters as before (including face_bake_calls287200 and guard_skips34433). Artwork from v12 is visible in the new screenshot, but this does not establish which Python/native revision ran. Do not blame installation or declare v12 successful. V13 writes a dedicated timestamped/session-specific status file and reports module path/source hash/native expected hash before waiting for UE.

Normalized private Face MIC payloads for ND06/ND13 (working), NF01/NF27/NFJR/NDHD (reported black), NDXS/NDDB (working), and ND08 are byte-identical within HQ/MQ. This rules out differing static templates in those cases; it does not prove runtime binding or shading is correct. See material-equivalence-validation.json.

V13 retains v12 verified component binding and adds it immediately after a successful original mesh callback, not only after bake. Native SetMesh0x39c6b18 uses *actor[0x1a70] or actor[0x228]; accept a component only if SkeletalMesh+0x468 equals the exact class/name-validated private loaded mesh. GetMaterial virtual0x588 and SetMaterial0x590 are proven by exec0x62f86c4/0x62f85c8 in libUE4 SHA2563da06a36fb5c434a75c5739af65f16664347477bd653659eb354376410d52f98. Use normal engine API, do not edit shared MIC parameters or raw override arrays. Source face/hair data for existing12cards is unchanged, proven264 chunk hashes.

New 2008 source: face239neck+1789face; hair341skin+1082head-shell+7461hair. Head-shell contains11 collapsed pole vertices with zero normals. Recover nearest defined source normal before orthogonal tangent repair; no position/UV/weight edits for that repair. Existing neck/seam/retarget writer is preserved; required bones per LOD remain166/153 with native compact indices. Native135 eye/mouth accessory vertices adapted to the source openings. Source oral faces are not assumed present in skin meshes. Full hair alpha/resolution retained, independent decoder MAE~1.73.

Source archive is data only; no embedded instructions executed. Body appearance source differs from v12 only by adding exact ID106726716084650 to forced long sleeves. Full64 negative tests and1296 real UE selector cases cover other IDs and conflicting editor overrides.

Card artwork now contains one person. Both native thumbnail assets are updated, headers/IDs/dimensions/mip descriptors preserved. Existing UI overlays remain native. The v12 name hook is retained; screenshot still shows Adriano, so do not claim all UI name paths fixed.

479 ARM64 tests execute native hooks/getter/FString ResizeTo but model material API/allocator/bake/async boundaries. No phone renderer is available; black-face root cause remains unconfirmed until current-session v13 counters and phone image are available. Neither HOOK_ACTIVE nor a successful texture lookup proves rendering.
