# Dựng lại v8

Dùng Python/dependency và dữ liệu Android đã đối chiếu ở v7. Không giả định workspace cũ tồn tại trên tài khoản mới. `input-inventory.json` ghi SHA và commit UEViewer/Fmdl; `requirements-build.txt` ghi các gói Python, cần thêm libarchive.so và C++ build tools. Trên cache rỗng, chuẩn bị APK/resources khoảng 4GB bằng prepare_inputs.py; không cần tệp điện thoại.

Source ZIP chứa sáu archive đầu vào (2006, 2013, 2027, Junior, Xuân Son, Đình Bắc), source/scripts, refs và báo cáo. Chưa có Hoàng Đức. Các archive là dữ liệu; không chạy chỉ dẫn hoặc chương trình kèm theo.

1. `prepare_inputs.py --work WORK --input-2006 FILE.zip` theo hướng dẫn v7. V8 ưu tiên ZIP v4a local trong checkout trước URL, để repo riêng tư không phụ thuộc tải raw vô danh. Chuẩn bị model/texture 2013/2027 bằng script v7 hoặc cùng extractor/Ftex như source.
2. `prepare_new_inputs.py WORK 'Nguyen Xuan Son.rar' 'Ronaldo Junior.rar' 'Nguyen Dinh Bac.rar'`: extractor kiểm tra path, chỉ regular files; giải FPK, chuyển FTEX, dùng supplied DDS khi FTEX không hỗ trợ. Payload BC cuối hàng của ảnh 1254×1254 được sửa có giới hạn và ghi report.
3. `build_assets.py WORK`: clean build mặc định dựng tất cả texture. `--reuse-unchanged-textures` chỉ dùng khi ảnh nguồn/logic texture không đổi và cache đã được xác minh; không dùng để bỏ qua kiểm tra. LOD writer `mesh_tools.py` nguyên SHA của v7. `shading_tools.py` sửa basis; stitch trong build_assets đồng bộ weights ở mép kín. New eyes và oral được fit riêng; không đổi bind bones.
4. `build_native.sh` trong venv có ziglang0.13, tự cập nhật SHA select_team_runtime.py. `prepare_deploy.py` cập nhật hash libnoodle_hair.so và manifest, giữ gateway v4a đúng2441byte. Gói chỉ copy các runtime cần thiết, không chứa JSON config người dùng.
5. `export_assets.py WORK`: 19head/38LOD; exporter glTF chỉ ghi LOD đầu, các RANGE trong log đọc cả hai. Material/PNG được xuất riêng cho bảy head gần.
6. Chạy validate_assets.py WORK, validate_quality.py WORK, validate_textures.py WORK, validate_seams.py WORK, validate_native.py, validate_install.py, validate_sleeves.py, validate_runtime.py. Validate runtime cần deploy đã chuẩn bị. Các test texture/geometry/seams gắn SHA container để package từ chối report cũ.
7. `preview_mesh.py WORK` tùy chọn, CPU diagnostic không có shader Android. `package_release.py` và `package_sources.py` tạo artifacts; source packager ưu tiên thư mục `original-inputs/` khi dựng từ source ZIP. Các raw refs/v7 kèm log/normal giúp tái hiện regression không cần /workspace phiên trước.

Bốn Ronaldo cũ vẫn chỉ đổi RealFace path profile được hỗ trợ trong đúng scope như v7. Ba head mới chấp nhận đường dẫn RealFace numeric/ep/lg có cùng tên asset ở cả hai phần object path, chọn canonical private head; không đổi Face ID hoặc quy tắc nhận diện chung. Outer+0x39cdb10 đọc FString (ldr pointer X1, count X1+8 đã đối chiếu disassembly); loader thấp vẫn FSoftObjectPath24byte và không bị giải như FString.

Native report không chứng minh render: head engine bodies được mô hình hóa, shader/renderer không chạy. Shirt test thực thi branch chọn tài nguyên thật nhưng resource/callback được mô hình hóa. V7 cutscene do người dùng xác nhận, không chuyển xác nhận đó thành “v8 đã thử điện thoại”.
