# Ronaldo 2017 face/neck refinement v2 — Blender only

Open Ronaldo_2017_FACE_NECK_v2.blend in Blender 4.3.2. Textures packed. Game Spider-Man and saves are not changed.

Changes: all skin sections use one skin material and the same packed skin image, RGB multipliers 0.95 / 0.945 / 0.94 for a subtly darker/warmer tone. Source mesh comparison found overlap pixels almost identical (mean absolute error <1/255); the hard back-neck patch was primarily inconsistent shading between neck and scalp. Smooth normals now use one welded reference across face, neck AND scalp, without changing original mesh topology/UVs. Please check back_neck.png, which is a real Blender render, not a generated image.

00_EDIT_CONTROLS > Object Properties > Custom Properties:
- Face2017_strength = 1 (same mature structure study as v1).
- Neck_shortening_mm = 7 (only 1 mm shorter than v1).
- Adam_apple_mm = 1.2 (subtle bulge, adjustable 0–3 mm).
Hair style unchanged; all head meshes move together with the neck key.

Upper lip: user reports deformation already existed in original 2006 game face. A local SOURCE WEIGHT CANDIDATE is applied only to upper-lip vertices with skf_lip_volume influence. That weight is redistributed proportionally to existing skf_lip_t_* controls. Mapping skf_lip_volume globally to half lower jaw can pull these upper-lip vertices during mouth opening. This is a candidate mechanism, not a confirmed diagnosis of the user's unknown converter/native rig. Lower lip/jaw and all other vertex groups remain unchanged. Original weights and per-vertex edits are recorded in validation.json for restoration. This .blend edit does NOT automatically repair a face already installed in game.

Checks: file reopen, topology/UV exact match, normalised nonnegative weights, edits restricted to listed upper-lip vertices, unified skin material. Not a native facial animation or game test. Check the export tool preserves new custom normals, packed skin image, current shape keys AND edited weights; an export ignoring them will keep the old problem. No mobile installation bundle is supplied here, per user's earlier Blender-only choice.

FaceBuilder video was inspected via extracted frames; FaceBuilder fitting has NOT been performed. Do not call this an exact 2017 reconstruction or claim the game mouth issue is verified fixed. Source eye/common assets remain incomplete as in v1. Skin/head texture is still derived from the supplied 2006 source, with a subtle colour correction; hairstyle was not replaced.

Sources/scripts/reports included. Original 2006 source author not identified. Public comparison PNGs are the actual edited .blend render.
