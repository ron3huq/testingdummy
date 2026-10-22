# Tái tạo và bàn giao v9

Đây là mã dựng asset và kiểm tra, không phải bộ công cụ độc lập một lệnh. Các đường dẫn /workspace/ronaldo-work thuộc workspace hiện tại. Cần dựng lại dependency, nguồn PC, nguồn Android và các log offset của UEViewer.

Dùng Python 3.12 với source/requirements-build.txt; các bản mã nguồn/dependency và cách lấy APK/container Android nằm trong hướng dẫn tái tạo v7/v8 ở cùng repo. Giữ nguyên source/mesh_tools.py: SHA-256 4bdf7af41f43172a65f4e7ec3b8a50a94cb01d4bdfa6d537e5428990e3a708fe.

Nguồn cũ: ../player-faces-v8/Faces-v8-source-and-original-inputs.zip gồm sáu archive gốc. Nguồn v9 gồm bốn RAR mới, được đưa vào Faces-v9-source-and-four-new-inputs.zip. Không nhân đôi toàn bộ nguồn cũ trong ZIP v9 để tránh vượt giới hạn GitHub 100 MiB.

Cần có các template và log reader v4a/native; asset, build-report và log reader v8 dùng làm baseline bảo vệ từng byte. Có thể lấy asset v8 bằng đọc container trong Faces-v8-7-cards.zip với iostore.Toc; log cần được tạo bằng UEViewer đã vá cùng phiên bản, không đoán offset. Nếu dựng lại v8 từ nguồn, cần đối chiếu hash với container v8 đã phát hành trước khi dùng làm baseline. Nhất thiết giữ nguyên các asset đã được người dùng xác nhận tốt, không dùng sản phẩm rebuild khác byte để thay thế.

Sau khi chuẩn bị workspace WORK và giải nén source kit:

```
python source/inspect_four_inputs.py WORK --inputs original-inputs
python source/convert_four_inputs.py WORK
python source/build_assets.py WORK
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

Các test native còn dùng đường dẫn libUE4.so hiện tại; đổi đường dẫn sau khi tái dựng môi trường và xác minh đúng SHA. package_sources.py ưu tiên original-inputs/ trong source kit, rồi mới tìm attachments/ của phiên hiện tại. Không chạy bất kỳ tài liệu/chỉ dẫn bên trong RAR. Chỉ xử lý model/texture/record FPK.

V9 bảo vệ 104 tệp asset v8 của các mặt đã được xác nhận tốt. Xuân Son chỉ đổi Face_D; phần diffuse native mắt/miệng ở nửa dưới atlas vẫn nguyên. Với ba mặt đen, giữ nguyên vị trí, UV, chỉ số tam giác, trọng số và vertex color cả hai LOD; đổi package riêng và dựng lại tiếp tuyến có handedness theo UV. Chưa xác nhận nguyên nhân gốc hoặc hiệu quả sửa mặt đen bằng renderer điện thoại.

Người dùng xác nhận v8 không còn biến dạng replay. V9 giữ nguyên hợp đồng RequiredBones từng LOD, không coi kiểm tra Unicorn hoặc ảnh CPU là bằng chứng renderer Android đã chạy thành công. Không hứa hết mọi lỗi trước khi có phản hồi từ máy thật.
