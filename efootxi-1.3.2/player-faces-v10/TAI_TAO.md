# Tái tạo v10 và giới hạn kiểm chứng

Môi trường Python 3.12 và source/requirements-build.txt. Giữ mesh_tools.py byte-identical v9/v7. Nguồn Android, UEViewer đã vá và parser FMDL theo hướng dẫn các bản trước. Không coi script có đường dẫn /workspace/ronaldo-work là công cụ độc lập sẵn chạy.

V10 dùng nguyên asset đã phát hành v9, không dựng lại các mặt tốt. source/prepare_v9_baseline.py xác minh SHA-256 ZIP v9 af9915e6d22316351abd3ba2a05f92666fabdb19b86406f43cd407b4d786b47f rồi phục hồi container, asset và metadata baseline. Gói nguồn v10 có RAR Speed và reference v9 cần thiết; nguồn PC cũ nằm ở gói nguồn v8/v9 của cùng repo, không nhân đôi trong ZIP v10.

Các bước sau khi dựng WORK với template v4a/native, log reader, model và texture cũ:

```
python source/prepare_v9_baseline.py ../player-faces-v9/Faces-v9-11-cards.zip
python source/prepare_speed.py WORK original-inputs/ISHOWSPEED.rar
python source/build_assets.py WORK
python source/export_assets.py WORK
python source/tone_three.py
python source/preserve_native_diffuse.py
python source/decode_asset_textures.py
python source/repack_container.py
sh source/build_native.sh
python source/prepare_deploy.py
python source/export_assets.py WORK
python source/validate_assets.py WORK
python source/validate_quality.py WORK
python source/validate_textures.py WORK
python source/validate_seams.py WORK
python source/validate_preservation.py WORK
python source/validate_native.py
python source/validate_install.py
python source/validate_sleeves.py
python source/validate_runtime.py
python source/preview_mesh.py WORK
python source/package_release.py
python source/package_sources.py
```

tone_three.py và một số validator còn dùng đường dẫn WORK cố định của phiên hiện tại; đổi chúng khi chuyển môi trường. Các asset baseline phải lấy từ ZIP đã xác minh, không từ một rebuild khác byte. Thêm Speed là phần build mới duy nhất. Tone hậu xử lý chỉnh XS/PQ/Speed, rồi khôi phục nguyên block ETC nửa dưới atlas của native mắt/miệng ở mọi mip >=8; không nén lại các block native đã đạt yêu cầu. Mip cuối chung block không thể tách nửa ảnh.

Unicorn chạy sáu detour và thực thi thân helper engine 0x39c728c. Hàm bake, FName interning và cập nhật material được mô hình hóa tại biên. Không mô phỏng renderer Android hoặc shader. Đã kiểm tra ABI của helper, hai nhánh material, callback thành công/texture cũ/sai ID/tắt chức năng. Không gọi đó là kiểm chứng đã hết mặt đen trên điện thoại.

Kiểm tra bảo vệ so sánh từng byte mọi asset v9; chỉ cho phép Face_D XS/PQ thay đổi. Tất cả mesh/rig/LOD cũ giữ nguyên. Native mới chỉ ghi texture parameter của bảy ID giới hạn trong HUONG_DAN.md, không ghi nhận diện cầu thủ hoặc trạng thái xương.

Ảnh thẻ: card-art-research/ có ảnh Pato xuất thật từ hai texture đúng ID, cùng log và đường dẫn. Không chứa bản thay artwork chưa kiểm chứng. Mẫu Đình Bắc do người dùng gửi là ảnh thẻ hoàn chỉnh, cần phân tách lớp khi triển khai tiếp; v10 chưa thay artwork.
