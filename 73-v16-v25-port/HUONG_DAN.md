# V25 chuyển cho 73 V16 — bản thử

Chỉ dùng APK `73efootball-V16.apk` bạn đã tải lên release `releasee`.
SHA-256 APK nguồn: `04f3e86e129bc7ef1705120caa93e43284f2033fffc376c4d597e5c7ddc15499`.
Resource V9+ giữ nguyên. Không dùng trên efootxi 1.3.2/1.4.0 hoặc Kipas.

## Dựng APK trên Windows

1. Giải nén gói này vào thư mục riêng; đặt **APK V16 gốc đã giải nén từ RAR** cạnh `BUILD_WINDOWS.cmd`. Giữ tên `73efootball-V16.apk`.
2. Máy cần Python 3 và Java 17 trở lên, khoảng **8 GB trống** để dựng/ký APK. Chạy `BUILD_WINDOWS.cmd`.
3. Khi báo DONE, APK đã ký nằm trong `output/`, tên kết thúc `aligned-debugSigned.apk`.

Script kiểm tra SHA của APK nguồn, bộ mod và công cụ ký; không sửa APK nguồn, không cài hoặc gỡ ứng dụng trên điện thoại. Không cần tải resource lại. Nếu máy thiếu Python/Java, cài từ python.org/adoptium.net; Python cần có lệnh `py` hoặc `python` trong PATH.

## Trước khi cài APK thử

**APK thử có chữ ký khác bản 73 gốc, nên Android thường không cho cài đè.** Dùng chức năng xuất save của bản 73 và chép file save ra máy tính trước. Không gỡ bản đang chơi nếu chưa có bản sao save kiểm tra được. Chỉ sau khi đã sao lưu, bạn mới tự quyết định thay ứng dụng bằng APK thử và nhập lại save. Gói không tự thực hiện các bước này.

Đừng gỡ APK resource V9+. Nếu bản thử không chạy, giữ file save đã xuất, cài lại APK V16 gốc cùng resource V9+ và nhập save. Việc nhập save giữa hai APK chưa được thử trên điện thoại.

## Kiểm tra

Mở Ronaldo 2017 ID `88044950524330`, rồi thử vào trận. Bản này giữ toàn bộ asset V25: đầu NV17 dùng nền mặt 2006 + tóc/sculpt Blender V3. Các đầu khác vẫn là asset V25, không phải lần sửa hình học mới.

Status ở thư mục dữ liệu nội bộ của **`com.efootball.revival.local`**:
`files/embedded-gateway/work/tools/noodle-hair-status.json`.
Version mong đợi: `player-faces-v25-73-v16-port-test`.
Nếu không có status, kiểm tra `v25-73-bootstrap-error.txt` cùng thư mục. Đường nội bộ này thường phải mở qua trình quản lý tài liệu của game hoặc quyền root; không mặc định nằm trong Android/data.

Đã kiểm tra hash payload, prologue đủ 15 hook trên engine 73 thật, bộ nạp và cấu trúc APK. **Chưa thử GPU/điện thoại; chưa xác nhận hết mặt đen hoặc crash.** Nếu phát hiện hook xung đột, bản này dừng trước khi cài hook đầu tiên.

Công cụ ký: [uber-apk-signer v1.3.0](https://github.com/patrickfav/uber-apk-signer/releases/tag/v1.3.0), SHA-256 `e1299fd6fcf4da527dd53735b56127e8ea922a321128123b9c32d619bba1d835`. Native V25 không đổi; không ghi save bằng mod.
