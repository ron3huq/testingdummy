# Ronaldo V2 — TAB / Basis display fix ONLY

Source is the original Ronaldo_2017_FACE_NECK_v2.blend. No v3/v4 face modifications, expression, eyes or colour changes were applied.

OPEN Ronaldo_V2_TAB_STABLE.blend in Blender 4.3.2 for direct editing. The evaluated v2 shape (including its existing shape-key settings) is stored as the base coordinates. Switching Object/Edit Mode therefore does not revert to the old Basis face. All 10 meshes preserve evaluated v2 vertex positions, original vertex/face order, UVs, skin weights and materials. Face edit-mode coordinates were checked against the captured v2 result. The frozen editing copy no longer has the old shape-key sliders. It is not a game installation file.

Ronaldo_V2_CONTROLS_EDIT_DISPLAY.blend is also included: retains original v2 keys/drivers/controllers, enables shape-key edit display and selects the face-shape key rather than Basis. Use this if you need the original sliders. Avoid editing Basis unintentionally.

Seeing triangles/vertices when pressing TAB is normal Edit Mode, not evidence of mesh corruption. The fix addresses the return-to-Basis shape mismatch, not removal of the triangle topology. Material Preview is set and camera/light extras hidden in viewport for easier viewing. Toggle Viewport Overlays to inspect without wire lines, or TAB back to Object Mode. No source triangles were deleted to hide wireframe. Original source common-eye limitations remain unchanged from v2.

# Spider-Man — ORIGINAL Ronaldo 2006 neck minus 20mm

This revision discards the generated neck/cylinder from v4/v5. Uses actual source neck, lower throat, rear scalp/neck and collar-base meshes from user CRISTIANO RONALDO 2006.zip. Upper triangles are intersected under the mask instead of removed whole. The original source boundary holes are repaired by filling source boundary loops using existing source vertices (not a new loft). Skin UVs/weights are retained/interpolated at cuts; collar AO geometry uses UV projection from original skin instead of its dummy AO material. Hidden upper overlap is fitted inside the mask so no bare skin pokes across the jawline. Visible source neck anatomy is retained apart from shortening 20mm with continuous deformation. Back/side Blender renders and posterior ray checks included.

This is a source-neck repair, not a byte-identical untouched source mesh: upper joins, boundary faces and smoothing had to be repaired. Bottom collar/body attachment needs Android testing. No synthetic cylindrical neck object is present.

Blender: open SpiderMan_v6_ORIGINAL_2006_NECK.blend. No addon required; texture packed. No other head-profile changes were added in this neck correction.

Android trial ONLY full Card ID 88044950524330, supported efootxi 1.3.2 exact libUE4 SHA. Force stop game. Extract SpiderMan-v6-ORIGINAL2006-NECK-ANDROID-TRIAL.zip; merge BOTH work/ and livedata/ into files/embedded-gateway/, overwrite all eight files. Restart and download data if requested. Test side/rear neck in a match/replay/celebration. No save/app data deletion. Runtime version in work/tools/noodle-hair-status.json: spiderman-head-v6-original2006-neck20.

To disable trial: force stop, install work/ from Tat-dau-SpiderMan.zip to embedded-gateway, restart. There is no Ronaldo mobile package here; its V2 shape is for Blender inspection/editing only.

Independent UEViewer re-export of all four native mesh variants; original 166-bone inverse binds, normalised weights, positions/UVs and container/bulk checks pass. Native hook/installer/manifest tests pass (engine bodies modeled). These do NOT prove Android renderer/animation/body seam correctness. No claim that phone tests have been run. Exact movie likeness / FaceBuilder fitting not claimed.

Images are actual Blender renders; cooked_asset_preview uses re-exported cooked mesh + decoded ETC2 atlas in Blender. Source neck archive author not identified. Game renderer still requires user confirmation.
