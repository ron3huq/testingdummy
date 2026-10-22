# Ronaldo v7 — bốn đầu, sửa lại LOD và cổ; áo dài tay trên nền v18

**V6 đã bị người dùng xác nhận làm biến dạng thân trong replay/cutscene nặng hơn. Không tiếp tục dùng v6 làm bản sửa cutscene. V7 đã dựng và kiểm tra mã/asset nhưng chưa chạy renderer trên điện thoại.**

## Phạm vi

| Phiên bản | Full Card ID | Asset riêng |
|---|---|---|
| Ronaldo 2017 tóc mì tôm | 88044950524330 | ND01 |
| Ronaldo 2006 | 89135066911146 | ND06 |
| Ronaldo 2013, nguồn 2013.rar | 106781745353130 | ND13 |
| Ronaldo 2027, tên theo 2027.rar người dùng gửi | 106734785925546 | ND27 |

Chỉ thay đầu bốn ID chính xác này. Không đổi Face ID, hệ thống nhận diện, mặt Messi, save, APK hoặc dt200. Các bản 2013/2027 dùng model/texture trong RAR tương ứng, không lấy mặt 2006 đổi tên. Mắt/răng/khoang miệng dùng 135 đỉnh native Android được đặt theo hốc mắt nguồn PC, cùng jaw/eye/eyelid rig Android. `oral.fmdl` 2027 đã mở/kiểm tra; không đưa texture FOX dùng chung còn thiếu vào renderer Android.

## Cài đặt bằng MT Manager, không cần root

1. **Buộc dừng game**, không chỉ thoát về màn hình chính.
2. Giải nén `Ronaldo-v7-4-faces-native-lod.zip` ra thư mục tạm.
3. Gộp thư mục **work/** và **livedata/** trong ZIP vào thư mục **files/embedded-gateway/** của game, cho phép ghi đè **11 tệp**. Không tạo thêm lớp thư mục `embedded-gateway/work/work/`.
4. Mở game, để hoàn tất tải/cập nhật dữ liệu rồi thử bốn thẻ đúng ID.

Gói dành cho hotfix v18 người dùng đã xác nhận đang cài. Nó chứa cặp `select_team_runtime.py` và `libselect_team.so` đồng bộ checksum trên cùng nền v18 để ép áo dài tay cho Ronaldo 2006 **89135066911146** và Messi **17592722922839**, kể cả khi editor chưa khởi tạo hoặc có cấu hình áo ngắn. Giữ các chính sách v18 còn lại và áo dài tay Ronaldo 2017. Gói không chứa file JSON cấu hình editor/đội/giải đấu, không xóa các thiết lập đó.

## Thay đổi có thể kiểm tra trong mã

- **Bỏ thay đổi RequiredBones sai của v6.** V6 rút cả hai LOD xuống 15 xương, làm mất các xương thân/tay/chân trong danh sách cần cho pose. Các bản trước lại mở rộng LOD thấp lên 166. V7 giữ từng danh sách RequiredBones theo đúng asset Android gốc: LOD0=166 và LOD1=153, nguyên thứ tự. Toàn bộ reference skeleton 166 xương và inverse bind matrices giữ nguyên.
- Dựng **LOD0 có geometry và buffer thật** thay vì để cooked-out rồi chỉ thay LOD1. MinLod riêng được đổi từ 1 thành 0 để LOD0 không bị khóa; ngưỡng ScreenSize hai LOD là 0,30/0,05. LOD0 có jaw/eye/eyelid controls; LOD1 theo cơ chế native đầu/cổ, không thêm xương mặt vào giữa danh sách compact pose của thân. LOD xa không giữ đầy đủ biểu cảm như LOD gần; không hứa toàn bộ biểu cảm PC.
- Cổ: làm mượt hình học trong mesh cổ, giữ ranh giới và mặt/da đầu/tóc; giới hạn dịch chuyển cổ tối đa 0,65 cm. Tính lại normals/tangents trên cổ, mask **toàn vùng cổ**, gồm dưới hàm mà v6 bỏ sót. Normal cổ làm phẳng có chuyển tiếp. SRO cổ bỏ họa tiết UV Android không đúng vị trí; diffuse cổ làm mềm nhẹ. Giữ hình dáng mặt và tóc đã đạt yêu cầu.
- Tóc 2006 và 2013 giữ texture gốc **2048×512**, tăng nét RGB nhẹ, giữ alpha nguồn trước nén ETC2, dùng vật liệu tóc HQ. Không tạo chi tiết giả bằng phóng ảnh. Tóc 2013 gồm cả hai lớp hair và hair-transfer từ nguồn.
- Hook chỉ đổi đường dẫn mesh/texture RealFace hợp lệ trong scope đúng actor, thread và full Card ID; FSoftObjectPath được engine tự tạo. `gateway_runtime.py` vẫn đúng **2441 byte**.
- Container riêng pc9298 và checksum/manifest đều được cập nhật; không thay container native dùng chung.

## Kiểm tra đã chạy và giới hạn

Đọc `asset-validation.json`, `quality-validation.json`, `texture-validation.json`, `native-validation.json`, `sleeve-validation.json`, `runtime-validation.json` và `package-validation.json` trong thư mục GitHub của bản này.

- UEViewer đọc độc lập 16 mesh, cả hai LOD của mỗi mesh, cùng material/texture của bốn head gần.
- Kiểm tra reference skeleton/bind, RequiredBones từng LOD, thứ tự compact pose dùng chung với thân; phép kiểm tra này phát hiện v6 không đạt. Đây là kiểm tra dữ liệu/mô hình compact pose, **không phải phát cutscene thật**.
- 104 ca ARM64 Unicorn cho hook đầu. Phần thân các hàm engine của hook đầu được mô hình hóa tại biên.
- 792 ca chạy hook áo và mã ARM64 chọn tài nguyên áo thật từ 0x3a0b28c đến trước LoadUniShirt 0x3a0b5f8; so toàn bộ actor, chỉ word sleeve được phép đổi. Có cả editor chưa khởi tạo và cấu hình áo ngắn xung đột. Tài nguyên kit dùng sentinel và một số callback được mô hình hóa; không phải render áo thật.
- Kiểm tra skinning jaw/mắt/mí, weight byte tổng 255, BoneMap không vượt 75, nén texture/alpha, checksum ZIP, manifest/idempotence/disable và dữ liệu hỏng.

**Chưa thể bảo đảm hết biến dạng, vệt cổ hay áo ngắn trên điện thoại trước khi người dùng thử.** Cần kiểm tra điều khiển, replay bàn thắng, phạt góc, ăn mừng, cận mặt, mở miệng/chớp mắt cho từng thẻ. Ảnh `geometry-texture-diagnostic.png` là CPU diagnostic, không phải ảnh game và không có shader/ánh sáng Android.

## Nếu vẫn biến dạng

Buộc dừng game rồi chép `work/` từ **Tat-thay-dau-v7.zip** vào `files/embedded-gateway/`. Gói này tắt thay đầu cả bốn ID, giữ native head và các chính sách áo v18; không xóa save. Không dùng v6 để quay lại vì đã có lỗi nặng được xác nhận.

Log kiểm tra cài đặt:

- `files/embedded-gateway/work/tools/noodle-hair-status.json`: version phải là `ronaldo-four-v7-native-lods`, state HOOK_ACTIVE, payload_verified=true.
- `files/embedded-gateway/work/tools/select-team-status.json`: version `native-hotfix-v18-ronaldo-v7-sleeves`, appearance_hooks.shirt=INSTALLED. Có lỗi ở đây thì chưa thể kết luận áo đã được áp dụng.

Nếu cần điều tra tiếp, hai log trên cùng ảnh/video chỉ rõ thẻ và cảnh lỗi sẽ phân biệt lỗi nạp gói, hook và render. Không cần chép toàn bộ thư mục game.
