# Ronaldo: return to EXACT v2 base + focus / larynx / slightly darker skin

User rejected v3. This file loads v2 directly, NOT v3. No new v3 eyeballs, v3 neck setting or other v3 geometry included. Base topology, UVs and weights compared with v2 on all 10 original mesh objects and unchanged. Original v2 features and known source common-eye limitations remain.

Open Ronaldo_V2_BASE_FOCUS_LARYNX.blend in Blender 4.3.2. 00_EDIT_CONTROLS > Object Properties > Custom Properties:
- Face2017_strength = 1: existing v2 structure.
- Neck_shortening_mm = 7: retain v2 length.
- Intense_expression = 0.8: added concentrated brow / mild eyelid narrowing, adjustable 0–1.
- Adam_apple_mm = 3.5: increased prominence compared to v2 1.2; an extra 1mm narrow geometric ridge improves definition. Shape keys remain editable. Skin is an extra 3% darker than v2, unified face/neck material. Source upper-lip candidate from v2 unchanged and not verified fixed in game.

Only Blender is delivered for Ronaldo. There is NO Ronaldo mobile installation or forced in-game expression lock. The FaceBuilder workflow has not been run; likeness is not an exact photographic reconstruction. Hair style unchanged. Detailed neck render included so silhouette can be inspected.

# Spider-Man v5: straighten posterior neck

The v4 collar rail narrowed and then widened at its upper end, producing the unwanted posterior bulge. V5 uses separate smoothly interpolated anterior/posterior rails; the posterior rail is strictly monotone in the generated geometry. The 20mm shortening requested earlier is retained. New complete human-skin neck surface has no deleted posterior section; lower collar rim remains open for the game body.

Open SpiderMan_v5_STRAIGHT_NECK.blend to inspect front / side / rear. This is still an artistic reference fit, not FaceBuilder or a film scan. The head profile is otherwise v4; this revision focuses on the defective neck, not claiming a newly perfected film likeness.

Android trial ONLY full Card ID 88044950524330, exact supported efootxi 1.3.2 libUE4 guarded by hash/prologue. Force stop. Extract SpiderMan-v5-ANDROID-TRIAL-88044950524330.zip and merge BOTH work/ and livedata/ into files/embedded-gateway/, overwrite eight files. Start game and download data if prompted. No app/save deletion. Check side/rear in match/replay/celebration.

Log work/tools/noodle-hair-status.json: version spiderman-head-v5-straight-neck20. Send full log plus in-game side/rear view if clipping or deformation occurs. To disable, force stop and install work/ from Tat-dau-SpiderMan.zip into the same embedded-gateway directory. The separate disable zip sets enabled=false only.

Four Android variants independently parsed/exported; UV, positions, native inverse binds and normalised weights pass. 30 ARM64 hook tests and delivery checks pass (engine bodies modeled at boundary). Rear/side surface-ray checks and posterior-rail monotonicity pass. Decoded ETC2 atlas + cooked mesh preview rendered in Blender. These do NOT verify Android rendering, animation or body seam: phone test required. No unconditional game reliability guarantee.

All previews are actual Blender renders, not image-generation illustrations. Every source script/report and limitations are included. No FaceBuilder licensing or install was performed.
