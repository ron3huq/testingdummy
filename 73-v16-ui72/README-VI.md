# UI7.2 — sửa xung đột dt870 gây C_NAJM_0009

[Tải Main UI7.2 — 31,1 MiB](https://raw.githubusercontent.com/ron3huq/testingdummy/chat-downloads/73-v16-ui72/V25-73-UI7.2-FULL-Part2-Main-MT.zip)

## Nguyên nhân đã xác định

Log điện thoại cho thấy cả hai worker native đã HOOK_ACTIVE và startup READY. CMD_LOGIN lỗi khi `kits_runtime.verified()` kiểm tra `dt870_mobile_and.cpk`.

UI7/UI7.1 đặt CPK kits đã sửa vào cùng đường dẫn mà `legends_v10._resources()` của bản73 quản lý. Java kiểm tra file trước khi Python khởi tạo; sau đó hàm gốc phục hồi CPK73 vào đường dẫn này. Đến lúc đăng nhập, checksum của CPK đang có khác checksum gói kits mod và request bị chặn. Đây là xung đột đóng gói của bản vá.

Đã tái hiện đúng thông báo lỗi bằng hàm phục hồi tài nguyên73 thật và CPK gốc thật. Không cần thay kết nối Internet để giải quyết xung đột này.

## Sửa trong UI7.2

- CPK mod giữ nguyên nội dung, chuyển sang file riêng `livedata/dt870_ui72_mobile_and.cpk`.
- Tên tài nguyên game nhận vẫn là `dt870_mobile_and.cpk`; URL loopback trỏ tới file riêng. Hash/kích thước quảng bá khớp đúng byte được tải.
- APK cũng phục hồi CPK gốc ở đường dẫn cũ để cập nhật từ APK UI7 đã sửa không để lại file nền sai.
- Cơ chế sửa file bất biến quản lý file CPK mod riêng. Bộ phục hồi gốc của73 tiếp tục quản lý file gốc.
- Giữ kiểm tra checksum. File CPK mod bị hỏng vẫn bị từ chối; không bỏ kiểm tra lỗi để tiếp tục vào game.
- Giữ face, native hooks, các giải/đội hình, kits, áo dài tay mặc định, tìm không dấu, Height & Weight, UI Earth, Card Designer và nút Diagnostics từ các bản trước. Không thay thư viện native hay nội dung CPK mod.

## Cách cập nhật từ UI7/UI7.1

1. Sao lưu save trước khi cập nhật.
2. Dùng APK đã áp đủ UI7/UI7.1. Trong MT Manager, chép `assets` và `classes5.dex` của Main UI7.2 vào gốc APK, hợp nhất và thay file trùng.
3. Ký bằng đúng key MT đang dùng rồi cài đè. Không gỡ game hoặc xóa dữ liệu để xử lý lỗi này.
4. Launcher phải hiện **UI7.2 Earth**. Thử Enter Game.

**Giữ nguyên Part 1 đã áp và resource V9**, không cần tải lại chúng. Không áp Main UI7/UI7.1 lên trên UI7.2.

Nếu làm từ APK73 V16 gốc, dùng [Part 1 của UI7](https://raw.githubusercontent.com/ron3huq/testingdummy/chat-downloads/73-v16-ui7/V25-73-UI7-FULL-Part1-Faces-MT.zip) cùng Main UI7.2; cả hai phần tạo thành bộ FULL, không cần các bản vá cũ.

Diagnostics giữ lại lỗi cuối từ lần chạy trước. Nếu mở sau khi cập nhật, thông báo UI7.1 cũ có thể còn trong `mod-last-error.json`; xem thời điểm và trạng thái của yêu cầu mới trong `ui71-gateway-startup.json`. Nếu còn lỗi khi Enter Game trên UI7.2, lấy Diagnostics mới sau lần thử đó.

## Kiểm tra

- Tái hiện đúng lỗi UI7.1 sau khi hàm `legends_v10._resources()` gốc thay CPK mod bằng CPK73.
- Chạy lại chính hàm phục hồi này khi dùng file riêng: gói mod giữ nguyên và kiểm tra checksum qua. Kiểm tra làm hỏng file riêng vẫn bị chặn.
- Chạy `initialize`, CMD_LOGIN và kiểm tra wire bằng các module gateway73 thật, SQLite fixture tách biệt. Hàm phục hồi dt870 gốc thực sự chạy trong initialize; CMD_LOGIN trả NOERR và wire_roundtrip PASS.
- Kiểm tra `_local_urls` đệ quy thật giữ URL file riêng, hash trùng byte tải, gọi lại không thêm tài nguyên hoặc tăng phiên bản sai.
- Kiểm tra đủ 7.381 dòng manifest so với APK gốc, đủ nguồn cho 45 file bất biến, DEX giữ 267 lớp gốc, manifest Card Designer và các phần native còn lại giữ nguyên.

Các bước nhập player pack/DIY chỉ có trên Android được tách khỏi fixture máy chủ. Chưa thử lại trực tiếp trên điện thoại sau sửa; kiểm tra máy chủ đã tái hiện và xử lý đúng xung đột được log thiết bị chỉ ra.

CPK gốc SHA-256: `eabf680adb54b909241cb0d484f87a79bc9d50b752d002c509abccf3e2a66497`.
CPK mod riêng SHA-256: `6595e6667dc40a6b6333886f919a52d75446d27c1f01670afa6854cc13918f84`.

SHA ZIP nằm trong [SHA256SUMS.txt](SHA256SUMS.txt); mã nguồn và báo cáo trong `source` / `validation`.
