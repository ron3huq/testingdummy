# Dựng lại v7

Mã trong `source/` dùng cached APK/resources/Fmdl/UEViewer của v5/v6; không giả định đường dẫn workspace cũ tồn tại ở tài khoản mới. Xem `../ronaldo-dual-v5/TAI_TAO.md`, `input-inventory.json` và `source/prepare_inputs.py`. `prepare_inputs` tải khoảng 4GB nếu cache rỗng. Cần Python3, C++ build toolchain để dựng UEViewer, libarchive.so và các gói trong requirements-build.txt; ARM64 dùng ziglang0.13, không cần Android NDK.

1. Cài Python requirements; chuẩn bị input v4a/native và 2006 ZIP qua `prepare_inputs.py`. Patch UEViewer ở `../ronaldo-dual-v6/source/ueviewer-v5.patch` (source ZIP kèm patch riêng).
2. Chạy `prepare_new_inputs.py WORK 2013.rar 2027.rar`. Extractor chặn path traversal, không chạy văn bản/script đính kèm. Nguồn FPK có record48-byte/offset64-bit; Ftex chuyển DDS và PNG. `new-input-analysis.json` ghi mesh/material/texture đã đọc và SHA các RAR.
3. `python source/build_assets.py WORK`: dựng 108 package/16head/32LOD và container. `--reuse-unchanged-textures` chỉ dùng khi đã có build hoàn chỉnh và không đổi input/texture logic; bản clean build không dùng tùy chọn này. `--refresh-neck-sro` ép dựng SRO khi tái sử dụng các texture còn lại.
4. `bash source/build_native.sh`, script tự cập nhật HOOK_SHA của select_team_runtime.py theo libselect_team.so. `prepare_deploy.py` tự cập nhật hash libnoodle_hair.so, manifest/native/editor/runtime, lấy gateway2441byte từ v4aZIP.
5. `export_assets.py WORK`: UEViewer đọc hai LOD mỗi head và export glTF LOD gần; export vật liệu/PNG của bốn head gần. UEViewer exporter glTF chỉ xuất LOD đầu dù -lods; log RANGE đọc cả hai LOD, validator đọc và đối chiếu cả hai buffer.
6. Chạy validate_native.py, validate_install.py, validate_assets.py WORK, validate_quality.py WORK, validate_textures.py WORK, validate_sleeves.py, validate_runtime.py. Native head engine bodies modeled; shirt test thực thi branch resource selector engine thật, resource availability/callback modeled. Không có Android renderer hoặc phát replay.
7. Tạo preview bằng preview_mesh.py WORK nếu cần; CPU diagnostic không phải bằng chứng cổ/cutscene hết lỗi. `package_release.py`, `package_sources.py` tạo ZIP/CRC/SHA256 và tài liệu.

V7 sửa sai lầm v6 khi xem RequiredBones và ActiveBoneIndices là cùng một phạm vi. RequiredBones của LOD thấp có các xương thân dù mesh đầu chỉ có weights đầu/cổ; không được cắt bỏ chúng vì không xuất hiện trong draw BoneMap. V7 giữ chính xác danh sách theo LOD của native; LOD1 loại facial weights bằng chuyển về head giống native, LOD0 render thật giữ facial controls. Đây là sửa hợp đồng dữ liệu được kiểm chứng; chưa chứng minh toàn bộ nguyên nhân lỗi cutscene của v4/v5/v6.

Library áo là source v18 với một ưu tiên exact64 cho 2006 và Messi trong appearance_mode, trước editor override. Không thay chính sách/DB nhận diện khác. Cặp runtime+library được đóng gói đồng bộ; giữ cấu hình JSON ngoài gói.

Kiểm tra property tag cooked FPerPlatformInt/Float: MinLod=0 và ScreenSize=[0.30,0.05], tránh LOD0 dựng xong bị MinLod=1 của asset gốc khóa. Không thay MinLOD hay asset body dùng chung.
