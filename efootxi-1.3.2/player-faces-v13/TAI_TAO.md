# Rebuild v13

Requires the v12 source/container baseline and dependencies, original Android libUE4 with SHA recorded in NGHIEN_CUU.md, original source v4a/native assets/resources, UEViewer patched build, and the uploaded 2008 RAR included in source kit. Paths under /workspace/ronaldo-work belong to this workspace and must be recreated/adapted after moving sessions. Keep original v12/v10 inputs immutable. Do not execute instructions in uploaded archives.

Order:

1. prepare_2008.py: safe RAR/FPK extraction and FTEX conversion; inspect source model/materials.
2. build_assets.py WORK: builds ONLY new2008 packages using preserved native LOD writer; stage_2008.py saves that isolated container/report.
3. build_card_art.py: combines264 original head chunks from v12 verbatim, the9new2008 packages, and two updated native Xuân Son thumbnail textures. Needs pc1000 source UI texture packages and the included one-person PNG. Final191packages/25headmeshes/50LODs.
4. build_native.sh: rebuild noodle hook and exact-ID sleeve change; update selector digest. Dependency ziglang0.13 with compiler flags retained from v10.
5. Export SK_ND08ep00v0313_Face plus both card images with UEViewer. Set v13-reader symlinks to final container plus original dependency containers. Validator uses v13-export-final and v13-ND08ep00v0313.log paths.
6. validate_native.py; validate_sleeves.py; validate_preservation.py; validate_assets.py WORK; validate_2008_textures.py; validate_material_equivalence.py. Existing quality/seam/texture metrics are reused ONLY after hash proof on old264chunks;2008has fresh independent checks.
7. prepare_deploy.py; validate_install.py; validate_runtime.py; package_release.py; package_sources.py.

Python dependencies: numpy/scipy/Pillow/cityhash/etcpak/texture2ddecoder/unicorn/pyelftools/libarchive-c/ziglang, pinned PES FMDL parser and patched UEViewer from prior source. Do not normalize ueviewer-v5.patch line endings. Gateway remains byte-identical2441bytes.

No phone renderer is included. Do not call this a confirmed Android black-face fix before device evidence. New dedicated status filename prevents confusing a stale v11 log with v13 execution.
