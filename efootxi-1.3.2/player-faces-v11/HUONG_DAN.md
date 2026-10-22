# Faces v11 — lấy texture từ mesh, màu da toàn thân native

Dành cho efootxi Android 1.3.2 ARM64, hotfix v18; chép bằng MT Manager, không cần root.

## Sửa lần này

Log người dùng v10: mesh chuyển thành công 26 lần nhưng target_texture_callbacks=0, private_texture_confirmed=0, face_texture_reapplied=0. Cơ chế chờ callback texture của v10 chưa chạy lần nào trên máy thật; HOOK_ACTIVE không chứng minh đã sửa mặt đen.

V11 lấy texture từ material đầu tiên của chính mesh vừa tải. Kiểm tra lớp USkeletalMesh bằng helper engine, đọc Materials theo metadata UHT (offset 0xd8, stride FSkeletalMaterial 0x28), gọi getter texture native, đối chiếu FName texture với tên asset riêng đúng ID. Chỉ sau khi hợp lệ mới dùng helper engine để gán texture sau bake. Không chờ callback texture riêng hoặc tự tạo FName giả. Chỉ áp dụng cơ chế gán texture mới cho bốn mặt đen. Ba đầu Speed/Xuân Son/Pendant đã đẹp không bị gán lại material bởi cơ chế này.

Ba ID đổi màu TOÀN THÂN qua bộ chọn skin native 6:

- 88033139360669 — IShowSpeed
- 88045755960841 — Nguyễn Xuân Son
- 105848932271764 — Pendant Quang Vinh

Selector skin_color ở actor+0x42c và cờ cập nhật skin+0x1a6b được đối chiếu metadata/disassembly. Engine tự chọn T_Sk6_Body_D, T_Sk6_Lowbody_D và T_Sk6_Skin_D; không tô màu lên áo hoặc thay texture trang phục. Cùng index 6 cho cả ba. Không ghi save hoặc dữ liệu chỉ số. Tất cả asset đầu, tóc, mắt/miệng và toàn bộ container giống hệt v10, bao gồm màu đầu bạn đã duyệt.

Giữ nguyên các thẻ đã tốt; không đổi Face ID/nhận diện cầu thủ/skeleton/RequiredBones/áo dài-ngắn. Bốn thẻ đang sửa mặt đen: 88044950524330, 106734785925546, 105765448873424 và 105643042189511.

## Cài đặt

Nếu đang dùng nguyên v10 như log đã gửi: chỉ cần Faces-v11-update-from-v10.zip. Buộc dừng game, gộp work/ vào files/embedded-gateway/, ghi đè bốn tệp rồi mở lại. Không cần chép lại container 62 MB. Gói cập nhật đã đối chiếu checksum các dependency với ZIP v10 gốc. Nếu thiếu tệp hoặc lỗi checksum, dùng gói đầy đủ theo các bước dưới.

1. Buộc dừng game hoàn toàn.
2. Giải nén Faces-v11-12-cards.zip. Gộp work/ và livedata/ vào files/embedded-gateway/, đồng ý ghi đè đủ 11 tệp.
3. Không xóa save/dữ liệu ứng dụng. Phải chép đủ runtime và manifest dù container giống v10.
4. Mở lại game, kiểm tra mặt đen, tay/chân/da toàn thân, áo và replay/cutscene. V11 chưa được kiểm tra renderer điện thoại.

Để tắt, chép Tat-thay-dau-v11.zip và khởi động lại game. Màu da là thay đổi actor trong RAM; cần khởi động lại để phục hồi actor gốc. Để quay lại v10, chép lại toàn bộ v10.

## Log cần xem

files/embedded-gateway/work/tools/noodle-hair-status.json

- version phải là player-faces-v11-material-seams.
- mesh_texture_inspections: đã kiểm tra material trong mesh.
- mesh_texture_confirmed: đã lấy đúng texture riêng, không phụ thuộc callback.
- mesh_texture_name_mismatches / mesh_texture_missing / mesh_material_invalid / mesh_texture_wrong_class: lý do không áp dụng.
- face_texture_reapplied: helper gán texture đã chạy.
- body_skin_index: 6 khi đã gặp một trong ba thẻ đổi màu.
- body_skin_changes / body_skin_last_card: theo dõi đổi màu toàn thân.

private_texture_confirmed vẫn có thể bằng 0 vì đường callback cũ không chạy; xem mesh_texture_confirmed mới. Nếu mặt vẫn đen, gửi log mới sau khi mở đúng thẻ và ảnh. Không cần lấy toàn bộ thư mục game.

## Ảnh thẻ Xuân Son

Chưa thay artwork. Đã trích xuất ảnh Adriano của đúng thẻ 88045755960841 và lập bố cục theo hai ảnh người dùng gửi: ảnh hô lớn làm nền, ảnh giơ tay ăn mừng làm chủ thể, giữ khung/hiệu ứng Epic xanh của thẻ gốc để giống thiết kế eFootball Adriano. Công cụ image_gen trả HTTP 400 Unknown parameter: reasoning, nên chưa tạo được artwork để đưa vào game. Không dùng ảnh người khác hoặc báo đã cài ảnh khi chưa làm được. Xem THIET_KE_THE_XUAN_SON.md và card-art-research/xuan-son/.
