# Nguồn v6

Dùng checkout đã có; không tạo Git worktree. Tham khảo quy trình công cụ/cached inputs ở `../ronaldo-dual-v5/TAI_TAO.md`. `source/requirements-build.txt`, `prepare_inputs.py` và `input-inventory.json` giữ cùng nguồn APK/resources/FMDL và commit reader đã xác minh. Source ZIP có ZIP 2006 gốc và reference v18 cần cho kiểm tra áo dài tay; không chứa các archive Android cỡ GB. Không phải bộ standalone không cần dependency.

Khác v5:

- build_assets.py: normal PC, giải mã DXT5nm alpha=X/green=Y, mask normal cổ; weld shading normals nhưng giữ vị trí; lấy weights thấp cổ từ native, loại alias vai khỏi đầu.
- mesh_tools.py: RequiredBones của cả hai LOD và ActiveBoneIndices là closure các xương thực sự dùng, có đầy đủ cha; 15 active/required, reference skeleton/bind vẫn 166 nguyên byte.
- Hair 2006 thực tế là **2048×512**, không phải 1024 vuông. Giữ kích thước và alpha nguồn trước nén; unsharp RGB nhẹ; shader HQ ở cả hai slot; TextureGroup Character. Không thêm chi tiết bằng upscale.
- myleague_editor_runtime.py: overlay long sleeve cho hai full Card ID mới trong một bản sao config khi cài editor; không ghi thay file config hoặc đổi các trường khác. Dựa trên API hotfix v18.
- Native hook thay đầu C giữ nguyên logic giới hạn hai ID của v5; native 58 case vẫn chạy. Bundle kiểm tra thêm hash module editor. Revision live data tăng 24, idempotent khi đã nhận đúng manifest.

Sau prepare_inputs và build_assets, tạo `v6-reader/` từ các symlink nguồn của reader-input, thêm ba file container v6. Xuất tám head vào `v6-export`, log `v6-<ND01 hoặc ND06><suffix>.log`; cùng các tùy chọn UEViewer của v5. Xuất thêm PNG từ hai head ep00v0313 và T_ND01ep00v0313_Face_D. V4a texture reference vẫn ở v4a-texture-export.

Các lệnh đã chạy trong phiên:

```bash
python source/build_assets.py /workspace/ronaldo-work
bash source/build_native.sh
python source/prepare_deploy.py
python source/validate_native.py
python source/validate_install.py
python source/validate_runtime.py
python source/validate_assets.py /workspace/ronaldo-work
python source/validate_textures.py /workspace/ronaldo-work
python source/validate_quality.py /workspace/ronaldo-work
python source/validate_sleeves.py
python source/preview_mesh.py /workspace/ronaldo-work
python source/package_release.py
```

Bộ đọc thật đọc tám mesh, cả normal/diffuse/hair và các material HQ từ container. Kiểm tra bind matrices, pose closure/ancestor order, không có limb bones trong active palette, source geometry/diffuse còn nguyên, trọng số 255, jaw/eyes/eyelid còn tác động, checksum/imports và cấu trúc package. validate_quality kiểm tra vùng normal cổ theo UV của các đỉnh cổ, alpha tóc, kích thước thật và HQ/texture group.

validate_sleeves thực thi libselect_team ARM64 v18 thật qua Unicorn, cài overlay bằng API editor, chạy 30 trường hợp qua native shirt hook trong năm context. Loader áo UE được stub; test so toàn bộ actor để bảo đảm chỉ word sleeve đổi và negative ID không đổi. Đây không phải thử shader/cloth trên điện thoại.

Chưa mô phỏng renderer Android hoặc phát được replay thật; thay đổi active bones là biện pháp sửa có kiểm tra cấu trúc, chưa chứng minh hết biến dạng trên máy người dùng. Ảnh CPU không có shader game, normal-map lighting hoặc renderer/cutscene thật. Không lấy ảnh đó làm bằng chứng các vệt cổ hoặc lỗi tay/chân đã hết trên điện thoại.
