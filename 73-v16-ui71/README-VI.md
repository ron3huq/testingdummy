# UI7.1 — sửa báo lỗi khởi động và lấy log C_NAJM_0009

Ảnh C_NAJM_0009 chưa xác định được bước gây lỗi trên thiết bị. Bản này sửa việc bộ nạp Python bắt lỗi nhưng vẫn trả `ready`, đồng thời thêm cách đọc log ngay trên launcher không cần root. **Chưa xác nhận đã khắc phục nguyên nhân C_NAJM_0009 trên điện thoại.** Cần log thực tế để phân biệt lỗi bootstrap, hook native, tài nguyên và thời gian chờ đăng nhập.

## Tải và cập nhật

[UI7.1 Part 2 — Main (~15 MiB)](https://raw.githubusercontent.com/ron3huq/testingdummy/chat-downloads/73-v16-ui71/V25-73-UI7.1-FULL-Part2-Main-MT.zip)

Nếu đã áp đủ UI7 như đã xác nhận, giữ nguyên Part 1. Chép `assets` và `classes5.dex` trong ZIP mới vào gốc **APK đã áp UI7**, thay file trùng, ký bằng đúng key MT đang dùng rồi cài đè. Sao lưu save trước khi cập nhật; không gỡ ứng dụng hoặc xóa dữ liệu để thử lỗi này.

Nếu làm từ APK73 V16 gốc, dùng [Part 1 của UI7](https://raw.githubusercontent.com/ron3huq/testingdummy/chat-downloads/73-v16-ui7/V25-73-UI7-FULL-Part1-Faces-MT.zip) cùng Main UI7.1. Hai phần vẫn tạo thành bộ đầy đủ; Main UI7.1 thay cho Main UI7. Resource V9 giữ như cũ.

## Gửi đúng lỗi từ điện thoại

1. Launcher mới hiện **UI7.1 Earth** và nút **Runtime Diagnostics** trong phần đầu trang.
2. Thử Enter Game. Nếu vẫn báo lỗi, thoát game rồi mở lại launcher.
3. Bấm **Runtime Diagnostics → Copy**, dán nội dung vào cuộc trò chuyện. Nếu không sao chép được, chụp phần đầu có `stage`, `error`, `traceback` và `select-team-status.json`.

Log lỗi cuối được giữ qua lần mở lại để không mất khi tiến trình bị đóng. Nếu đã có lỗi cũ, xem `time_unix` để biết thời điểm; các trạng thái hiện tại cũng được liệt kê riêng. Không cần truy cập thư mục riêng của ứng dụng bằng MT/ADB.

## Những gì thay đổi

- Bootstrap lỗi sẽ được chuyển tới giao diện chuẩn bị với nguyên nhân, thay vì tiếp tục như đã sẵn sàng.
- Lưu traceback cho lỗi bootstrap, yêu cầu gateway và hai worker native. Giữ lỗi gần nhất qua lần mở lại.
- Ghi trạng thái/thời gian tối đa tám yêu cầu gateway đầu tiên để nhận ra yêu cầu bị kẹt hoặc xử lý lâu. Không ghi payload, query URL hoặc log liên tục trong trận.
- Nút đọc log chỉ hoạt động khi bấm, đọc trên luồng nền; danh sách file cố định, giới hạn 10.000 byte mỗi file. Không đọc/copy save. Chỉ sao chép ra clipboard khi người dùng bấm Copy.
- Giữ giao diện Earth, tìm không dấu, Height & Weight và các sửa face/kits/My League từ UI7. Thư viện native và tài nguyên giữ nguyên byte. Cơ chế chờ mod sẵn sàng vẫn giữ nguyên.

## Kiểm tra

Kiểm tra bootstrap thành công giữ kết quả gốc, lỗi bootstrap được đưa ra giao diện, lỗi request không bị nuốt, báo cáo lỗi có traceback và trạng thái native; lỗi ghi log không làm hỏng request vốn thành công. Collector Java thật đã chạy trên JVM với Context giả lập để kiểm tra whitelist, giới hạn đọc và loại trừ save. Kiểm tra gói đầy đủ theo manifest gốc, hash, DEX và giữ toàn bộ lớp gốc đều qua.

Thử lệnh CMD_LOGIN với các module gateway73 thật trên máy chủ trả NOERR và qua kiểm tra mã hóa/giải mã. Fixture máy chủ dùng SQLite tách biệt, bỏ bước nhập tài nguyên chỉ có trên Android; không thực thi hook ARM64 trong tiến trình điện thoại. Kết quả đó chưa xác nhận nguyên nhân hoặc việc sửa lỗi trên thiết bị.

SHA-256 trong [SHA256SUMS.txt](SHA256SUMS.txt); mã nguồn và các kiểm tra trong `source` / `validation`.
