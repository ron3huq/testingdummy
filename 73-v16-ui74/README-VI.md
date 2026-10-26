# UI7.4 Earth — bộ Main đầy đủ cho 73 V16

Dành cho APK 73 V16, không dùng cho efootxi 1.4.1. Đây là Part 2 đầy đủ; Part 1 Faces giữ nguyên bản UI7.

Log trên điện thoại UI7.3 xác nhận cả 40 hook đã cài, CMD_LOGIN thành công, sau đó dừng ở màn hình đầu. Người dùng đã thử Check & Repair Resources mà vẫn loading. Log cũ chưa ghi tải HTTP nên chưa xác định được chính xác file gây dừng.

## Thay đổi

- Đóng gói lại dt870 theo cấu trúc CPK gốc: giữ kiểu cột UTF, giá trị NULL, mã hóa UTF và thứ tự 101 hàng gốc; giữ nguyên nội dung và ID của toàn bộ 142 tài nguyên mod. Đổi URL và phiên bản để client nhận bản mới.
- Máy chủ tài nguyên nội bộ hỗ trợ HEAD, Range/206, tải tiếp, If-Range, 304 và 416. Thêm nhật ký truyền file giới hạn 32 mục, tối đa ghi mỗi giây khi truyền.
- Kiểm tra file asset pack thực tế theo phiên bản APK và kích thước trước khi tin dấu đã cài. Không dùng file Download có thể thay đổi làm điều kiện, không xóa save.
- Runtime Diagnostics thêm resource-presence-status.json và http-resource-status.json; tăng lịch sử RPC khởi động từ 8 lên 64 lệnh.
- Giữ bộ sửa 40 hook UI7.3, face, My League, kits, khôi phục HLV gốc, áo dài mặc định, Earth UI, tìm tên không dấu và chỉnh chiều cao/cân nặng theo yêu cầu trước.

## Cài bằng MT Manager

1. Sao lưu save qua Save Manager nếu truy cập được. Giữ ứng dụng và resource V9 đang có; không gỡ game hoặc xóa dữ liệu.
2. Mở APK 73 V16 đã có Part 1 Faces. Chép đè toàn bộ nội dung ZIP Part 2 UI7.4 vào gốc APK; không tạo thêm thư mục bọc ngoài. ZIP là gói áp vào APK, không phải APK cài trực tiếp.
3. Ký bằng cùng khóa đã dùng cho ứng dụng hiện tại và cài đè. Nếu Android báo xung đột chữ ký, dừng để kiểm tra khóa, không gỡ game để vượt lỗi.
4. Đóng hẳn rồi mở lại, xác nhận UI7.4 Earth. Không cần áp nối tiếp UI6/UI7.1/UI7.2/UI7.3.

Nếu bắt đầu lại từ APK 73 V16 gốc: áp cả Part 1 Faces UI7 và Part 2 UI7.4 trước khi ký. Giữ resource V9 để nhập tài nguyên nếu cần.

## Kiểm tra và giới hạn

Các báo cáo JSON kèm theo ghi kết quả kiểm tra trên máy: đăng nhập gateway 73 thật, khôi phục CPK gốc, URL/hash, toàn bộ manifest 7382 mục, 46 file quan trọng, DEX giữ 267 lớp gốc và không đưa stub kiểm thử vào APK; HTTP GET/HEAD/Range thực qua NanoHTTPD, ráp lại file đúng SHA256; kiểm tra asset pack thiếu/sai kích thước/sai phiên bản.

Chưa chạy trên điện thoại Android. Các thay đổi sửa những điểm xử lý tài nguyên tìm thấy khi kiểm tra mã, nhưng chưa chứng minh đây là nguyên nhân duy nhất của lần loading hiện tại. Nếu vẫn kẹt, mở lại Runtime Diagnostics → Copy và gửi toàn bộ log UI7.4; hai nhật ký mới sẽ cho biết yêu cầu/file và số byte máy chủ đã đọc. Đọc xong file ở máy chủ không chứng minh game đã mount tài nguyên thành công.

Mã nguồn thay đổi và bản diff smali trong source/. ResourceInstaller-test-fixture.java chỉ phục vụ kiểm thử, không nằm trong DEX phát hành. Các script tham chiếu workspace xây dựng hiện tại.
