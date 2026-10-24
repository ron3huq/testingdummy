# V25 controlled single-card mobile test

Baseline: published V24 complete container and working ND06 mesh/materials.
Accepted Blender source: Ronaldo_2017_REPAIR_V3.blend, published in Blender
repair V3. No original bad 2017 facial geometry/materials are reused.

Pipeline: export_blender.py -> bake_textures.py -> build_assets.py ->
verify_assets.py -> review_raster.py -> stage.py -> validate_runtime.py.
Build native with build_native.sh; validate_native.py and validate_install.py.

Native C differs from V24 only in TARGET's profile string NX01 -> NV17.
The other 16 mappings and every engine call/ABI are unchanged. Original
23-argument squad builder, native material lifecycle and trampoline allocator
are retained. Native engine boundaries are modeled in the host harness;
578 tests do not certify Android rendering.

The 2369 original PC skin vertices match the working ND06 UV/topology order.
Apply only accepted sculpt deltas to the adapted ND06 positions; preserve
its native neck fitting. Transform the original tangent frame with the
sculpt Jacobian. Preserve 135 native eye/oral accessory vertices unchanged.
Preserve each native LOD's skin weights independently: re-quantizing LOD1
from LOD0 would otherwise change 12 neck rows. Full skeleton/required bones
remain166/153. Hair source geometry and both source UVs are exported; a new
non-overlapping UV is baked from source colour UV1 + alpha UV0. Export
reacquires Blender UV RNA after exiting edit mode; finite/range checks
reject stale UV pointers. Atlas overlap is9 shared edge pixels.

Face D remains PF_ETC2_RGB as the working asset, with unchanged RGB blocks
retained. Face N/SRO content is byte exact to ND06. Hair D remains its native
PF_ETC2_RGBA2048x512/mip layout; comparisons use the native-sized reference,
not the2048-square intermediate atlas. No source DXT normal is substituted.
All material properties match ND06 after reversing private asset names.

The container adds40 NV17/NVH1 assets. Every V24 asset chunk is retained byte
exact. Source Blenders/PC assets are not Android skeletons and are not copied
into live data; the existing Android mesh format and skeleton are reused.

All device_verified flags remain false. Package only after all reports pass.
