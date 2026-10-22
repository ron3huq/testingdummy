# Ronaldo v4a — sửa đường dẫn làm mất tóc ở v4

Chỉ Card ID **88044950524330**, Android efootxi 1.3.2, MT Manager không root.

## Cài

1. Buộc dừng game.
2. Giải nén `Ronaldo-PC-mesh-v4a-88044950524330.zip`.
3. Gộp cả **work/** và **livedata/** vào **files/embedded-gateway/**, ghi đè đủ 8 tệp. Không dán bên trong work/tools và không cài chồng bản v4 cũ sau đó.
4. Mở game, tải dữ liệu nếu có yêu cầu, vào sân bằng đúng thẻ 88044950524330.
5. Kiểm tra tóc và cả cảnh replay/ăn mừng. Chưa có xác nhận hết lỗi tay/giày kéo dài trên điện thoại.

Không xóa dữ liệu/save. Gateway giữ nguyên bản tương thích 2441 byte; không thay dt200, đội hình hay cấu hình My League. Container/mesh/texture giống v4, chỉ sửa runtime/native và checksum liên quan. Không cần sửa APK.

## Vì sao tóc biến mất

Log điện thoại v4: HOOK_ACTIVE, target_calls=1, skipped_face_id=1, redirects=0. Đã gặp đúng thẻ nhưng không thay asset.

Đối chiếu mã engine thật cho thấy hàm mesh 0x39cd71c nhận FSoftObjectPath 24 byte (FName + subpath FString), không phải FString 16 byte như v4 đọc. V4 vì vậy không nhận diện đường dẫn và chuyển thẳng đầu gốc. Kiểm tra v4 trước đây mô hình hóa sai kiểu đối số này nên không phát hiện lỗi.

V4a giữ đối số loader như một cấu trúc opaque, không đọc hay tự tạo FName. Việc thay đường dẫn được chuyển sang FSoftObjectPath::SetPath tại 0x45b58b0: game nhận chuỗi UTF-16 có độ dài xác định rồi tự tạo đối tượng native. Hỗ trợ cả đường dẫn object trần và class reference, chỉ đúng bốn biến thể 4522 ở RealFace, trong scope của đúng actor/thẻ/thread. Giữ nguyên Face ID và callback gốc. Nếu private mesh trả null, nạp lại đầu gốc trong scope chặn redirect để tránh vòng lặp.

Đây là bản sửa lỗi nhận diện đường dẫn. Không tuyên bố đã xác nhận tóc, màu da/biểu cảm hoặc biến dạng replay trên thiết bị. Giữ nguyên mesh PC và bảng retarget của v4; xem hướng dẫn v4 để biết giới hạn chuyển rig PC sang Android.

## Log sau khi vào sân

`files/embedded-gateway/work/tools/noodle-hair-status.json`

- version: **ronaldo-pc-face-v4a-softpath**.
- Cần quan sát `mesh_path_redirects`, `redirects`, `nonnull_callbacks` tăng khi đầu mới tải.
- `last_face_profile` vẫn là 4522... là đúng: không thay nhận diện cầu thủ.
- `last_asset_path`, `last_actor_type`, `scoped_path_calls` bổ sung chẩn đoán.
- Với actor dùng vật liệu gắn sẵn, không nhất thiết có callback texture riêng; chỉ số texture=0 không tự kết luận mesh thất bại.
- Nếu tóc vẫn không xuất hiện hoặc replay lỗi, gửi toàn bộ log và ảnh.

## Tắt đầu thử

Buộc dừng game, dán work/ từ `Tat-dau-thu-Ronaldo.zip` vào files/embedded-gateway/, mở lại. Chỉ đặt enabled=false, không xóa save. Bật lại bằng gói đầy đủ v4a.

## Kiểm tra

30 trường hợp thực thi native ARM64 trong Unicorn: plain/class path, cả bốn biến thể, length có/không NUL, đúng full Card ID, thẻ khác, opaque FSoftObjectPath 24 byte có FName không thể dùng như con trỏ, giữ nguyên nhận diện, cách ly scope/thread, disabled, callback và fallback cả inline/async. Các thân hàm engine vẫn mô hình hóa tại biên; không chạy renderer Android.

Năm đường cài detour Python, SHA/prologue engine thật, worker HOOK_ACTIVE, manifest/hash/idempotence và gateway được kiểm tra. Asset không đổi so với v4 và được đối chiếu byte trước đóng gói. ZIP kiểm tra CRC và checksum đủ 8 tệp.

Nguồn PC người dùng cung cấp (NEUBE), chưa xác minh trên điện thoại.
