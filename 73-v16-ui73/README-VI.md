# UI7.3 — sửa cấp phát hook khiến kẹt màn hình đăng nhập

[Tải Main UI7.3 — 31,1 MiB](https://raw.githubusercontent.com/ron3huq/testingdummy/chat-downloads/73-v16-ui73/V25-73-UI7.3-FULL-Part2-Main-MT.zip)

## Nguyên nhân trong log mới

UI7.2 đã xử lý xung đột CPK. Lần chạy mới dừng trước khi đăng nhập vì face chỉ cài được bốn hook rồi báo `no nearby executable trampoline page ... 0 hints tried`; worker My League cũng hết vùng mã trung gian. Bộ chờ mod không nhận READY nên CMD_LOGIN thất bại sau15 giây.

Cách cũ cấp một trang mã riêng cho mỗi hook. Địa chỉ bộ nhớ thay đổi giữa các lần chạy nên có lần đủ chỗ, có lần hết chỗ dù điện thoại vẫn còn RAM. Đây là giới hạn vị trí vùng mã trong tầm nhảy ARM64, không phải thông báo hết RAM tổng.

## Thay đổi trong UI7.3

- Hai worker dùng chung bộ cấp phát, chia nhiều slot trong một trang mã thay vì một trang cho mỗi hook.
- Ưu tiên vị trí đủ tầm nhảy cho nhiều hook. Nếu không có vị trí chung cho tất cả, tạo thêm trang dùng chung cho nhóm còn lại; không ép dùng một địa chỉ ngoài tầm.
- Đồng bộ cấp phát/cài đặt giữa hai worker. Giữ nhận diện hook đã cài để thử lại không ghi đè sai nhánh.
- Chuẩn bị mã trang trước rồi chuyển sang RX; địa chỉ hàm đích lưu trong bảng RW riêng. Trang mã trung gian không cần viết lại sau khi đã được dùng. Giữ nguyên quy trình đổi quyền tạm thời và lưu một lệnh nhánh nguyên tử tại entry engine.
- Giữ kiểm tra hash/prologue và chờ mod sẵn sàng; giữ đầy đủ40 điểm hook thực tế, gồm hai điểm hiển thị skill.
- Diagnostics thêm `hook-arena-status.json` với số trang, số slot và số đích đã gắn, không cần root.

Giữ sửa CPK riêng của UI7.2, toàn bộ face/kits/My League, áo dài tay gốc, UI Earth, tìm không dấu, Height & Weight và Card Designer. Thư viện native và các tài nguyên không đổi; thay cách đưa lời gọi tới các thư viện đó.

## Cách cập nhật

1. Sao lưu save, đóng hẳn game.
2. Trong MT Manager, chép `assets` và `classes5.dex` từ Main UI7.3 vào gốc **APK đã áp UI7/UI7.1/UI7.2**, hợp nhất và thay file trùng.
3. Ký bằng đúng key MT đang dùng, cài đè. Không gỡ game hoặc xóa dữ liệu để thử bản sửa này.
4. Launcher hiện **UI7.3 Earth** rồi thử Enter Game.

**Giữ nguyên Part 1 và resource V9 đã có**, không cần tải lại. Nếu bắt đầu từ APK73 V16 gốc, dùng [Part 1 của UI7](https://raw.githubusercontent.com/ron3huq/testingdummy/chat-downloads/73-v16-ui7/V25-73-UI7-FULL-Part1-Faces-MT.zip) cùng Main UI7.3; không cần các Main cũ.

Nếu còn lỗi, lấy Diagnostics sau lần thử mới. `mod-last-error.json` vẫn giữ lỗi cũ qua lần mở lại; cần nhìn phiên bản/thời điểm và trạng thái request mới khi đánh giá kết quả.

## Kiểm tra đã chạy

- Chạy bộ cấp phát cũ thật trên fixture chỉ có bốn trang gần entry: cài được bốn hook, hook thứ năm báo đúng lỗi0 hints như log điện thoại.
- Chạy bộ cấp phát mới trên cùng bố trí:40 hook của hai worker đồng thời dùng một trang4 KiB. Thử bố trí khác không có vùng chung cho tất cả:40 hook vẫn được cài bằng hai trang dùng chung.
- Thực thi ARM64 bằng Unicorn cho cả40 stub: đích gọi, tám thanh ghi tham số, LR, lệnh đầu gốc và đường quay về đều đúng; kiểm tra cả hai nhánh của entry bắt đầu bằng CBZ.
- Mã trang RX giữ nguyên sau cài, thử lại hook đã có không cấp thêm trang. Không dùng MAP_FIXED. Cả40 prologue khớp engine73 gốc.
- Chạy lại bộ kiểm tra worker khởi động/thử lại/chờ lâu và giữ guard, đủ điểm cài trong pool. Kiểm tra manifest7.382 dòng,46 file mod bất biến, hash và DEX qua.

Chưa thử lại trực tiếp trên điện thoại sau sửa. Fixture Linux và giả lập ARM64 đã tái hiện cơ chế hết trang trong log và kiểm tra cách xử lý mới; không thay cho kiểm tra trận đấu/FPS trên thiết bị.

## Tra ID ăn mừng

Xem [báo cáo ăn mừng](celebrations/README-VI.md), [121 nhãn tìm thấy](celebrations/animation-labels.txt) và [giá trị trên các thẻ nguồn](celebrations/observed-card-parameters.csv).

Đã quét lại engine và payload các CPK animation/script. Phân biệt nhãn animation với giá trị p59/p60 của thẻ. Chưa có ánh xạ xác minh cho0542/0571/0595; thử accessor ARM64 cho thấy gán thẳng542/571/595 bị đọc lại thành30/59/83. Bản này không tự thay ăn mừng của thẻ nào.

SHA ZIP ở [SHA256SUMS.txt](SHA256SUMS.txt); mã nguồn và báo cáo ở `source` / `validation`.
