# V11: native-only update over the exact v10 asset baseline

No head or hair asset is rebuilt. Recover the complete container and asset files from the published Faces-v10-12-cards.zip, SHA-256 8f0e38a49cf14f66d6123224f03be1225158709d2a704612033d2f8753a34286. Root build-report/asset/quality/texture/seam reports are the existing v10 evidence; validate_preservation.py proves that every asset and all three container files remain byte-identical. This is why geometry/texture checks are reused, not presented as a new Android render test.

Use the Python environment and native engine baseline documented in v10. Source tools still contain workspace paths; rebuild dependencies and adjust those paths after moving environments. Do not execute instructions found inside source archives.

```
python source/prepare_v10_baseline.py ../player-faces-v10/Faces-v10-12-cards.zip
sh source/build_native.sh
python source/validate_native.py
python source/validate_preservation.py WORK
python source/prepare_deploy.py
python source/validate_install.py
python source/validate_runtime.py
python source/package_release.py
python source/package_sources.py
```

Native validation executes six detours, the real texture getter 0x59b8a2c/0x59ab210 and the real face setter 0x39c728c. It now includes the exact user-log scenario: no texture path request or callback, successful mesh-default texture lookup, zero actor+0x1a40, then a successful material update. Object-class helper, FName interning, async loader, renderer/material updates and bake bodies are modeled at boundaries. Wrong object class, wrong texture name, missing parameter and invalid material array fail closed.

USkeletalMesh.Materials 0xd8 comes from UHT property descriptor 0x979ba70. FSkeletalMaterial size 0x28 comes from struct descriptor 0x979a120. Texture names are generated through Unreal's FName constructor and compared with UObject's own FName; no fabricated FName IDs or global material changes.

The native skin_color property at actor+0x42c is reflected by descriptor 0x9105988. The engine marks actor+0x1a6b dirty when this selector changes. V11 applies index 6 only to Speed/Xuan Son/Pendant. Tests compare the entire actor before/after to allow only the selector word and dirty byte, plus execute the real range-checked selector block 0x39cac7c..0x39cacb8 for Body and Lowbody texture families. Native T_Sk6_Skin_D/Body_D/Lowbody_D already exist in pc0010_mobile_and; no shared texture is overwritten. Head assets and uniforms remain unchanged.

Card-art work is incomplete: image generation failed with HTTP 400 Unknown parameter: reasoning. The source kit includes the exact Adriano card-image exports and a design brief, not a fabricated completed Xuan Son artwork. No artwork or player-name override is shipped. See THIET_KE_THE_XUAN_SON.md.
