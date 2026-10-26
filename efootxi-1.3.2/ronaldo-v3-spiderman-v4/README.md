# Ronaldo v3 Blender + Spider-Man v4 Android trial

## Ronaldo: Blender ONLY
Open Ronaldo_2017_v3_EYES_NECK.blend in Blender 4.3.2. Original archive lacked complete common eyeballs. Two separate UV-mapped eyeball globes and the common PC eye image (warm iris tint) were added. Eye height follows the neck controller. This is visible geometry restored for inspection; Android eye animation/rig compatibility is NOT verified. No Ronaldo Android package is supplied; existing game Spider-Man is not automatically replaced by this blend.

00_EDIT_CONTROLS > Object Properties > Custom Properties:
- Face2017_strength = 1, same underlying likeness study as previous revision.
- Neck_shortening_mm = 8 (1mm more than v2).
- Adam_apple_mm = 2 (previous 1.2).
- Intense_expression = 0.8. Set 0 for neutral. This shape key lowers/advances inner brow and narrows upper eyelids slightly. Mouth opening is not frozen. It does NOT lock the expression against Android animation.
Whole unified face/neck image is an additional 3% darker than v2. Hair style unchanged. Eyes are newly added geometry, not a claim that missing common source assets were found complete. Same upper-lip weight candidate from v2, still not verified fixed in game.

## Spider-Man v4: Blender + Android trial
Only full Card ID 88044950524330; exact supported efootxi Android 1.3.2 libUE4 SHA remains guarded by the v4a-derived runtime. NOT device verified. Keep a working version to restore.

Source neck was incomplete independently of the game body. Earlier whole-triangle cutoff also removed large posterior polygons. V4 replaces that incomplete collar with one continuous reconstructed human-skin neck surface using the 2006 skin atlas. It is NOT an exact unchanged original 2006 neck. There is no Spider-Man texture on the neck. 21 horizontal side/rear ray checks hit the new neck surface; bottom collar rim remains intentionally open to attach to body. Exact body join, clipping and replay need phone testing.

The complete head assembly is lowered 20mm with smooth compression of the neck, anchored near its base. Head profile was revised: rounder rear cranium/crown, reduced lower jaw projection, slightly narrower lower head. This is an artistic anatomical fit to user reference images, NOT an exact film asset or FaceBuilder reconstruction. No claim of exact film proportions. FaceBuilder plugin was not run. The user's video is a landmark-fitting tutorial for human heads; no automated mask fitting is claimed here.

### Install
Force stop game. Extract SpiderMan-v4-ANDROID-TRIAL-88044950524330.zip. Merge BOTH work/ and livedata/ into files/embedded-gateway/, overwrite all eight files. Do not clear app/save data. Start game; download data if requested. Test this exact card in a match, replay and celebration. Verify rear neck on camera rotations. Other cards must remain unchanged.

Log: files/embedded-gateway/work/tools/noodle-hair-status.json, version spiderman-head-v4-profile-neck20. Check redirects, mesh_path_redirects, nonnull_callbacks and restore_requests. Keep original Face ID; only private asset paths are redirected.

### Disable / restore
Force stop, merge work/ from Tat-dau-SpiderMan.zip into files/embedded-gateway/, restart. To return to the previous v3 Spider-Man head, reinstall its full eight-file bundle:
https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/spiderman-head-v3-human-neck/SpiderMan-v3-ANDROID-TRIAL-88044950524330.zip

### Checks and limits
4 private cooked meshes independently parsed and exported by UEViewer. Vertex positions, UV bounds, normalised skin weights and original 166 native bone inverse bind matrices verified. Rigid mask/lenses/web are head-only; neck uses head/neck blend. 61,366 visible vertices, 75,696 triangles: mobile performance unmeasured. Existing MQ shader reused, atlas ETC2 RGBA2048 12mips. Container/bulk roundtrip and checksum tests, 30 ARM64 hook checks, Python installer and manifest tests pass. Engine bodies modeled at test boundary; none is an Android match test.

Gateway remains 2441 bytes. Private pc9298 container replaces previous trial; manifest revision +24. Runtime and metadata must be installed together.

All PNGs are actual Blender renders. cooked_asset_preview.png uses the re-exported cooked mesh and decoded ETC2 atlas in Blender, NOT Android rendering. No image-generation picture is used as proof. Exact likeness and in-game reliability are NOT guaranteed before user device feedback.
