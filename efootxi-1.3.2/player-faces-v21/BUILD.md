# V21 build and research

Baseline: v20 install SHA `5d754379d28f2c625e8dab42effbdee90907ba2d2d7a9c115dca5029b874b974`, with v20a 23-argument converter and whole-gap trampoline fix. Requires the restored v20 workspace/dependencies and original ARM64 libUE4.so SHA `3da06a36fb5c434a75c5739af65f16664347477bd653659eb354376410d52f98`. Python/UEViewer paths here belong to this workspace; the scripts are not standalone Android tools.

The source ZIP contains the supplied Diomande archive, converted/extracted source, authored portrait sheets, native runtime and checks. Other baseline assets/dependencies remain in the v20 source release/repository. No instructions from attached archives are executed.

Order with the existing virtual environment:

```sh
python source/prepare_diomande_input.py
python source/build_diomande.py
python source/build_seams.py
python source/build_kit_letters.py
python source/build_cards.py
sh source/build_native.sh
python source/validate_native_v21.py
python source/validate_squad_abi.py
python source/validate_install.py
python source/validate_trampoline_hints.py
python source/verify_assets.py
python source/prepare_deploy.py
python source/validate_runtime.py
python source/package_release.py
```

`verify_assets.py` uses `/workspace/ronaldo-work/v21-reader`, a set of symlinks to the v20 native reader files with the v21 container in place. Complete writes before launching independent readers. Its glTF check accounts for UEViewer's vertex reorder by matching coordinate clouds; the coordinate transform is independently inferred before native-bind synthetic jaw poses.

Runtime change for black heads: remove the four cards from the legacy post-bake static-material/shadow override. Original bake and mesh callbacks execute; no replacement MID or shader is introduced. The four assets themselves are byte-identical to v20. This is a scoped alternative to the previous failed interventions, not a proven GPU fix. The source of the phone log supplied this turn was still v20, before any head load; it does not establish v20a or v21 device state.

Yan Diomande needed its own original topology/UVs. A donor-UV attempt showed a wrong-colored chin in the studio preview and was rejected. The final asset uses 2766 supplied skin vertices, 135 native accessories, 5181 source hair vertices, named bone retarget and original native RequiredBones per LOD. Its two hair materials receive separate atlas tiles. Source XY normal data is reconstructed into native XYZ normals; native accessory atlas remains intact.

Özil/Đình Bắc only: unify nearby skin seam weights below the mouth, preserve mouth/eyes/accessories, rebuild jaw normals. Whole rigs, indices and UVs remain exact. Posed seam gaps are measured with native inverse binds; this is synthetic geometry validation only.

Image generation performed the creative portrait edits. The asset step extracts sprite cells, preserves aspect ratios, crops large art from the top to retain hair and encodes exact native dimensions. No stretching a full card into a mini.

Jersey glyph masks/dimensions are retained literally; colors follow the supplied historical kits. The name resource path is observed, never rewritten. Actual name visibility remains a device validation item.

Every report preserves `phone_tested: false`. No host check substitutes for Android gameplay/replay/rendering.
