# Spider-Man v3: closed mask head + real Ronaldo 2006 neck

Target ONLY full card ID 88044950524330. Android efootxi 1.3.2 with the exact supported engine SHA from v4a. Experimental device trial: NOT confirmed working on a phone. Exact film likeness is not verified.

## Install Android trial
Force stop efootxi. Extract SpiderMan-v3-ANDROID-TRIAL-88044950524330.zip. Merge BOTH work/ and livedata/ into files/embedded-gateway/, overwriting all eight files. Do not delete app/save data. Start game and Download Latest Data if prompted. Test this exact card in a match, goal replay, missed chance and celebration. Other cards must remain unchanged.

Expected log: files/embedded-gateway/work/tools/noodle-hair-status.json, version spiderman-head-v3-human-neck. Check state, payload_verified, manifest_advertised, target_calls, redirects, mesh_path_redirects, nonnull_callbacks, null_callbacks, restore_requests. Send full log + in-game screenshot if appearance/loading fails. A non-null callback is not proof of correct Android rendering.

## Restore
To return to the original game head without deleting saves: force stop, overwrite work/tools/noodle_hair.json with {"enabled":false}, restart. The separate Tat-dau-SpiderMan.zip does this. To return to the earlier working noodle-hair PC head, reinstall the full Ronaldo v4a eight-file bundle after force stop:
https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/ronaldo-pc-mesh-v4a/Ronaldo-PC-mesh-v4a-88044950524330.zip

## Blender
Open SpiderMan_v3_HUMAN_NECK.blend in Blender 4.3.2. Packed original neck texture; no addon needed. This is the editable source scene, not a file to copy into the APK. The game uses the lower tessellation mesh and baked ETC2 atlas built from this scene. All previews are actual Blender renders, not generated illustrations. cooked_asset_preview.png is rendered from the independently re-exported cooked Android mesh and its decoded ETC2 atlas, using a Blender preview material, NOT the Android renderer.

## What changed
Replaced the parametric egg/jug profile. The mask is a closed smooth outer shell fitted to head-anatomy dimensions, not the original human facial mesh with red texture. Bare lips/nostrils/ears/eyeballs are not exposed. Lenses, black rims and raised web curves are separate geometry. Original 2006 neck mesh and lower throat use the user's original skin texture/UVs. Visible lower neck remains unchanged; only upper hidden overlap is trimmed/tucked under the mask to eliminate intersections and gaps. Neck is not covered in Spider-Man material.

The anatomical shell remains an artistic approximation based on the user's references. Do not describe this as an exact film scan or verified production asset.

## Android implementation and limitations
Uses the v4a scoped FSoftObjectPath runtime, keeping original player/Face IDs. Four private mesh variants retain the native 166-bone rig and original inverse bind matrices. Visible mask/lenses/web are 100% sk_head; no facial jaw/lip deformation is assigned to the rigid mask. Neck weights are explicitly retargeted. Seven draw bones, normalised byte weights sum 255; 56,738 visible vertices and 65,516 triangles. This is substantially heavier than the previous head; phone performance has not been measured.

A hidden internal 3-vertex face-slot triangle preserves the two-section layout; ALL visible mask and skin geometry use the same private baked atlas material slot. This prevents the native face-texture callback from replacing the mask or real neck colour. Atlas 2048 ETC2 RGBA, 12 mips; existing mobile hair-MQ material/shader reused. Its Android lighting/specular appearance needs device testing. No new shader permutation is claimed.

Container pc9298_mobile_and replaces the prior private noodle-head container. Login manifest revision +23; original manifest entries retained. Gateway bootstrap remains 2441 bytes. My League squads/stats/save/dt200 are not edited.

## Checks performed
Independent UEViewer parses and exports all four cooked meshes. Position data matches the baked source; UVs in range; native 166-bone inverse binds byte-identical; mask head-only influence and all weight sums verified. Container and bulk readback, private material dependencies and ETC2 error checks pass. 30 ARM64 hook checks, five Python install paths and delivery/manifest regression checks pass; engine bodies modeled at the test boundary. NONE substitutes for an Android match/replay test. Do not promise a device crash or rendering defect cannot occur.

2006 neck source was uploaded by user; original author not identified in supplied archive. Preserve attribution if known. No film-reference image or watermark is included in the textures.
