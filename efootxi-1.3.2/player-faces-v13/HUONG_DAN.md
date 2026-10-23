# Faces v13 — 13 Card ID, Ronaldo 2008, callback material và thumbnail Xuân Son

Cho efootxi Android 1.3.2 ARM64 + hotfix v18. Chưa xác minh renderer Android.

## Cài một gói đầy đủ

Dùng **Faces-v13-13-cards.zip**.

Buộc dừng game. Giải nén ZIP, gộp **cả work/ và livedata/** vào `files/embedded-gateway/`, ghi đè đủ **11 tệp**. Không lồng thêm thư mục `embedded-gateway` bên trong chính nó. Không xóa dữ liệu/save và không chép source/ vào game. Mở lại game, vào trận/chi tiết cầu thủ.

Đọc **work/tools/player-faces-v13-status.json**. Tệp này chỉ được v13 tạo; không dùng log v11 để đánh giá v13. Các mục `version`, `session_id`, `reported_at_unix`, `pid`, `runtime_path`, `runtime_sha256` và `expected_native_sha256` giúp xác nhận phiên/mã/tệp đang dùng. Log chung noodle-hair-status.json cũng được cập nhật nhưng có thể là tệp cũ nếu module mới không chạy.

Nếu không xuất hiện tệp log riêng v13 hoặc state=ERROR, gửi đúng thông tin đó; không xóa save hay toàn bộ thư mục game. Nếu v13 HOOK_ACTIVE mà đầu vẫn đen, gửi log riêng này và ảnh mới để kiểm tra binding/shader.

## Thay đổi

- Bốn đầu từng đen: Ronaldo2017 `88044950524330`, Ronaldo2027 `106734785925546`, Jr `105765448873424`, Hoàng Đức `105643042189511`. Gán Face MIC riêng ngay sau callback mesh, rồi kiểm tra lại sau bake. Chỉ slot0 trên component giữ **đúng mesh riêng**; không đụng slot tóc, material dùng chung, Face ID hay rig. Material tĩnh đã được đối chiếu với đầu tốt; giống nhau sau khi chuẩn hóa tên/texture paths, nên không thay template theo phỏng đoán.
- Thêm Ronaldo2008 **riêng `106726716084650`**, nguồn RAR người dùng gửi. 3451 đỉnh mặt/cổ/da đầu, 135 đỉnh mắt/miệng native, 7461 đỉnh tóc. Skeleton166 và inverse bind matrices native; hai LOD giữ danh sách RequiredBones native để tránh lỗi compact pose từng gây kéo dài tay/chân. Sửa 11 normal bằng0 ở cực da đầu nguồn; giữ geometry/UV nguồn và texture tóc đầy đủ độ phân giải. Biểu cảm được retarget sang rig Android, không chuyển đủ mọi biểu cảm PC.
- ID Ronaldo2008 luôn áo dài tay như 2006/2013; không sửa chính sách áo các thẻ khác.
- Thẻ Xuân Son `88045755960841`: bỏ chân dung nền thứ hai, chỉ giữ một người. Cập nhật cả texture128x128 và184x256, giữ lớp khung/OVR/vị trí/huy hiệu do game vẽ. Không sửa chỉ số.
- Giữ nguyên byte của toàn bộ264 chunk đầu/tóc của12thẻ trước. Màu da toàn thân Xuân Son/Pendant/Speed vẫn native index6.
- Giữ hook đổi tên Xuân Son từ v12; ảnh điện thoại cho thấy tên còn Adriano ở màn đó, vì vậy chưa coi việc đổi tên mọi màn hình là hoàn thành.

## Bộ đếm quan trọng

`mesh_callback_component_matches`: callback tìm đúng component; `head_material_rebinds`: số lần SetMaterial; `head_material_confirmed`: GetMaterial đọc lại đúng MIC; `head_material_rebind_failed`: không giữ được kết quả; `head_component_mismatch`: không có component mang đúng mesh. `bake_owner_missing`, `bake_texture_missing`, `bake_material_missing` phân biệt nguyên nhân bỏ qua. `last_material_card_id` xác định thẻ của snapshot mới nhất.

`head_binding_state_bits`: bit0 component gián tiếp có mặt, bit1 giữ đúng mesh; bit2 component alternate có mặt, bit3 giữ đúng mesh; bit4 cache MID thường có mặt; bit5 cache MID đặc biệt có mặt; bit6 cờ special bật.

## Đã kiểm tra / còn cần điện thoại

479 kiểm tra ARM64;1296 trường hợp chọn áo bằng thân selector UE thật;7 đường cài hook, checksum/manifest/idempotence; UEViewer đọc ngược mesh/texture2008 và hai ảnh thẻ; texture tóc alpha MAE~1.73; native RequiredBones/ActiveBones/weights/binds và mô phỏng jaw/eye/eyelid pass. Template material HQ/MQ của đầu tốt/đầu lỗi/2008 được đối chiếu18 trường hợp.

GetMaterial/SetMaterial, FMemory allocator, async loader và thân bake được mô hình hóa tại biên. Không có renderer Android trong workspace: **chưa thể bảo đảm hết mặt đen, không biến dạng cutscene hoặc áo đúng trên điện thoại trước khi người dùng xác nhận**. Bản này có sửa đường gán thực tế và chẩn đoán mới, không coi kiểm thử giả lập là kiểm thử điện thoại.

Kiểm tra bốn đầu lỗi và2008 trong gameplay/replay/cutscene, áo2008, thumbnail Xuân Son. `Tat-thay-dau-v13.zip` chỉ tắt thay đầu sau khi buộc dừng/cài cấu hình/mở lại; không gỡ artwork hay áo riêng. Quay lại bằng gói v12 đầy đủ nếu cần.
