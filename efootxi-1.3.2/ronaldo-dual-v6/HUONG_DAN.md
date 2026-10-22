# Ronaldo v6 — sửa cổ, thử sửa biến dạng cutscene, tóc 2006 HQ và áo dài tay

Gói thử cho efootxi Android 1.3.2 ARM64, MT Manager, không root.

- 88044950524330: giữ mặt/tóc mì tôm, mắt và miệng v5; sửa shading/rig vùng cổ.
- 89135066911146: giữ mặt/mắt/miệng 2006, tóc dùng shader HQ và texture 2048×512 có tăng nét nhẹ; áo dài tay.
- 17592722922839 (Messi): chỉ thêm áo dài tay, không thay mặt/tóc.

## Cài

1. Buộc dừng game.
2. Giải nén **Ronaldo-v6-co-toc-cutscene-ao-dai.zip**.
3. Gộp cả **work/** và **livedata/** vào **files/embedded-gateway/**, ghi đè đủ **chín tệp**. Có thêm `work/tools/myleague_editor_runtime.py` cho áo dài tay; phải chép cả tệp này.
4. Mở lại game và nhận Latest Data nếu được hỏi. Không cài chồng v5/v4a lên sau đó.

Không xóa save/dữ liệu ứng dụng, không sửa APK hoặc chép cả thư mục game. Lớp áo dài tay dùng API editor ngoại hình đã có trong hotfix v18; file cấu hình editor người dùng được đọc và giữ nguyên, không chép đè `myleague_editor.json`, đội hình hoặc thông số cầu thủ.

## Thay đổi và lý do

**Hai vệt ở cổ:** v5 dùng normal map Android trên UV PC nên chi tiết gồ/lõm không nằm đúng vị trí. V6 dùng normal map PC đúng nguồn (giải mã DXT5nm cho bản mì tôm), làm dịu normal vùng cổ, làm mượt normal đỉnh qua seam và lấy trọng số cổ từ đầu native. Không di chuyển các đỉnh mặt/tóc. Màu diffuse mặt mì tôm vẫn giữ dữ liệu v4a, không vẽ lại mặt.

**Cutscene kéo dài tay/chân:** v5 khai báo cả 166 xương cơ thể là active/required cho đầu. V6 giữ nguyên skeleton và bind matrices 166 xương, nhưng chỉ khai báo tập xương đầu/cổ/mặt thực sự dùng cùng các xương cha; bỏ ảnh hưởng vai/tay/chân khỏi đầu riêng. Sửa này nhằm tránh đầu riêng tham gia điều khiển các xương chi khi đổi chế độ pose/LOD. Tất cả biến thể và cả hai LOD được kiểm tra. Đây là hướng sửa dựa trên dữ liệu; chưa chứng minh đó là nguyên nhân duy nhất hoặc đã hết lỗi trên máy người dùng.

**Tóc 2006:** giữ geometry và ảnh gốc 2048×512, tăng nét RGB nhẹ nhưng giữ alpha nguồn trước nén, chuyển cả slot HQ/MQ sang material masked HQ và dùng nhóm texture Character thay cho Project06. Không phóng to ảnh nhỏ để giả chi tiết.

**Áo dài tay:** áp dụng đúng hai full Card ID mới qua editor native, giữ áo dài tay 2017 và các thiết lập khác. Không dùng base ID để đổi toàn bộ Messi/Ronaldo.

## Cần thử ngay sau khi cài

- Cận cảnh cổ cả hai Ronaldo, nhìn thẳng và ngửa đầu; kiểm tra hai vệt có hết hoặc giảm rõ không.
- Tóc 2006 cận cảnh, ánh sáng trong/ngoài sân; kiểm tra alpha không bị răng cưa hoặc mất sợi.
- Replay ghi bàn, bỏ lỡ, phạt góc, ăn mừng: đặc biệt kiểm tra cả tay và chân.
- Kiểm tra áo dài tay của 89135066911146 và 17592722922839. Thẻ khác không được đổi theo.
- Mắt/miệng và hình dáng mặt/tóc mì tôm vẫn cần giữ đúng như bản trước.

**Chưa chạy trên điện thoại hoặc renderer Android. Không khẳng định đã hết lỗi cutscene.** Bộ kiểm tra máy dựng xác minh dữ liệu/rig/native hook, không thay thế thử replay trên thiết bị. Nếu còn lỗi, gửi ảnh và log dưới đây; không cần lấy toàn bộ dữ liệu game.

## Log và quay lại

Log đầu: `files/embedded-gateway/work/tools/noodle-hair-status.json`, version `ronaldo-dual-v6-neck-head-scope`.
Log áo dài tay/editor: `files/embedded-gateway/work/tools/select-team-status.json`, chú ý `editor_error`, `editor_status`, `appearance_last_applied_id`, `appearance_build_after` và `appearance_shirt_after`.

**Quay-lai-v5.zip** khôi phục trọn tám tệp v5 và module editor v18 gốc. Nó cũng gỡ lớp ép áo dài tay mới của gói v6. Cài bằng cách buộc dừng rồi gộp work/ và livedata/ như trên; không xóa save. V5 vẫn có các lỗi cổ/replay người dùng đã báo.
