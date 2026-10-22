# Faces v10 — 12 thẻ, sửa bước gán texture sau bake

Dành cho efootxi Android 1.3.2 ARM64, hotfix v18 đã cài. Không cần root. Đây là bản sửa cần xác nhận hiển thị trên điện thoại, không phải cam kết đã hết mặt đen.

## Thay đổi lần này

- Ronaldo 2017 88044950524330; Ronaldo 2027 106734785925546; Ronaldo Jr 105765448873424; Hoàng Đức 105643042189511: giữ nguyên toàn bộ mesh/texture/rig v9, thêm bảo vệ texture mặt ở runtime sau bước bake của engine.
- Xuân Son 88045755960841 và Pendant Quang Vinh 105848932271764: chỉ đổi Face_D và dùng cùng bảo vệ texture, chỉnh về tông da mặt sẫm hơn và cùng mẫu màu với Speed. Không đổi màu da toàn thân.
- IShowSpeed 88033139360669: thêm nguồn người dùng, gồm đầu/tóc, mắt/miệng native và trọng số mắt, hàm, mí; không chuyển đủ mọi biểu cảm PC. Màu da mặt dùng cùng tông tham chiếu với Xuân Son/Pendant.
- Giữ nguyên 2006 89135066911146, 2013 106781745353130, Đình Bắc 88038776539586, Hoàng Hên 106728863696709 và Tài Lộc 105874433662542; không áp dụng bước ghi material mới cho các thẻ này.

Tên, chỉ số, Face ID gốc và artwork thẻ không đổi. Chính sách áo vẫn như v9: 2017/2006/2013 và Messi 17592722922839 dài tay; 2027 ngắn tay; các thẻ khác theo cấu hình hiện tại.

## Cài bằng MT Manager

1. Buộc dừng game.
2. Giải nén Faces-v10-12-cards.zip, gộp work/ và livedata/ vào files/embedded-gateway/, ghi đè đủ 11 tệp.
3. Không xóa save hoặc dữ liệu ứng dụng. Không chép riêng thư viện hoặc riêng container vì checksum phải đồng bộ.
4. Mở lại game, kiểm tra bốn mặt đen, màu da và Speed ở cả điều khiển, góc cận và replay/cutscene.

Để tắt thay đầu: chép Tat-thay-dau-v10.zip cùng cách và khởi động lại game. Để quay lại v9: chép lại nguyên gói v9.

## Vì sao sửa khác v8/v9

Đã kiểm tra ARM64 của hàm 0x39cb75c: engine cập nhật trạng thái bake, nhận texture trung gian từ 0x3a10e5c rồi gọi UMaterialInstanceDynamic::SetTextureParameterValue 0x59b8644, với faceBaseColor hoặc BaseColorMap tùy kiểu đầu. Asset mặt đúng không bảo đảm texture đó tiếp tục được giữ sau bước này.

V10 vẫn chạy nguyên hàm gốc và giữ trạng thái bake. Chỉ với bảy ID nêu trên, sau khi xác nhận callback tải texture riêng thành công và pointer còn trùng actor+0x1a40, gọi lại helper engine 0x39c728c để gán đúng texture vào material mặt. Helper tự tạo FName, không tự chế FName; không đổi nhận diện cầu thủ, skeleton, RequiredBones hay shader dùng chung. Khi chưa xác nhận texture riêng, bị thay texture, sai ID hoặc đã tắt tính năng thì không ghi material.

Unicorn thực thi sáu detour và thân helper engine thực; FName interning, cập nhật material và phần bake còn được mô hình hóa. Chưa chứng minh đây là nguyên nhân duy nhất hoặc đã hết mặt đen trên renderer Android. Giữ nguyên hợp đồng LOD đã hết biến dạng theo xác nhận v9, nhưng vẫn cần kiểm tra replay cho bản mới.

## Nếu vẫn đen hoặc chưa đúng màu

Sau khi mở đúng thẻ bị lỗi, gửi files/embedded-gateway/work/tools/noodle-hair-status.json và ảnh. Log v10 có face_bake_calls, private_texture_confirmed, face_texture_reapplied, face_texture_guard_skips, last_target_id và last_asset_path. Chỉ cần tệp log này, không cần chép toàn bộ thư mục game.

## Ảnh thẻ Pato thành Đình Bắc

Đã xác định hai asset đúng ID và xuất ảnh gốc; xem NGHIEN_CUU_ANH_THE.md và card-art-research/. V10 chưa cài poster mẫu vào thẻ. Khung, rating, vị trí và tên là các lớp UI riêng; không thay khung dùng chung để tránh ảnh hưởng thẻ khác.
