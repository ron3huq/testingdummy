# 73 V16 · UI7.8

Bản Part2 Main tích lũy cho **eFootball73 V16**, không dùng cho efootxi1.4.1. Gồm thay đổi Main từ các bản trước; Part1 Faces và bộ Resource73 gốc vẫn là các thành phần riêng.

- **[Tải UI7.8 FULL Part2 Main](V25-73-UI7.8-FULL-Part2-Main-MT.zip)**
- **[Danh sách ID ăn mừng dễ đọc, có tìm kiếm (tải HTML rồi mở)](celebration-ids.html)**
- **[Danh sách ID ăn mừng dạng CSV](celebration-ids.csv)**
- [Mã SHA256](SHA256SUMS.txt)

Áp Main này vào APK73 đang dùng thay Main cũ trong MT Manager, ký bằng **đúng khóa đang dùng**, rồi cài đè. **Không cần gỡ game/xóa dữ liệu**. Nếu bắt đầu từ APK73 sạch, áp cả [Part1 Faces giữ nguyên](../73-v16-ui7/V25-73-UI7-FULL-Part1-Faces-MT.zip) và Main vào cùng APK trước khi ký; Resource73 vẫn phải được cài. ZIP này không phải APK đã ký và không đóng gói save cá nhân.

## Thay đổi

- Bỏ nút Physics và hai API Physics của UI7.7. Các chỉ số thuộc tính cầu thủ khác vẫn dùng trình chỉnh cũ.
- Chiều cao **140–220cm**, cân nặng **40–130kg**, khôi phục giới hạn cũ ở cả UI, lưu dữ liệu và native. Nếu đã lưu mức quá giới hạn bằng UI7.7, lần nâng cấp đầu tự phục hồi trường vượt mức về số gốc của đúng thẻ trong bảng73, đồng thời lưu bản sao SQLite tại `embedded-gateway/backups/ui78-measurements-before.sqlite3` trên máy. Các giá trị hợp lệ được giữ.
- **Skills → Edit Innate Skills** dùng64 tên tiếng Anh người dùng cung cấp, gắn với mã native hiện có; đánh dấu skill đang sở hữu. Áp dụng đổi cờ innate, giữ riêng5 ô Additional Skills và dữ liệu level/progression. Không đổi số thứ tự skill để khớp thứ tự trong tin nhắn.10 mã nội bộ chưa được đối chiếu tên không được đặt tên bừa; nếu thẻ có sẵn mã đó, hiện `Unmapped native skill N` để không tự xóa khi lưu.
- **Appearance & Motion → Celebration IDs** chọn riêng Main (`parameter59`) và Memorial (`parameter60`), hiển thị ID hiện tại và một thẻ sở hữu để tham khảo. Lưu vào đúng thẻ được chọn; nội dung hai trường cũng được đưa vào cấu hình native và dữ liệu gửi tới game. Chỉ nhận giá trị thực sự xuất hiện trong bảng73, tránh mã bị cắt bit.
- **Appearance & Motion → Skin · Body Palette** chọn Original hoặc6 palette thân người gốc. Lựa chọn được áp dụng theo full64 cardID trước native bake bằng callback đã có; không thêm entry/trampoline và không gọi Python/SQL mỗi khung hình. Có bộ đếm `skin_palette_status` trong Runtime Diagnostics.

**Giới hạn màu da:** phần trên đổi palette **thân người**, không tô lại texture khuôn mặt riêng. **Màu custom RGB và đồng bộ màu da toàn bộ khuôn mặt chưa được triển khai/xác minh.** Không có bộ chọn RGB giả hoặc tự quy đổi RGB thành palette gần nhất. Vì thế yêu cầu màu custom chưa hoàn tất trong bản này.

Chỉnh trước khi bấm Enter Game. Sau khi lưu, đóng/mở lại ứng dụng trước khi vào trận để native nạp cấu hình mới. Nếu libUE4 đã được tải, editor từ chối sửa và giải thích cần mở lại app.

## Danh sách ăn mừng và độ chính xác

Đã quét toàn bộ **46.623 bản ghi**, chạy bộ nhập dữ liệu gốc `0x82aa124` và getter gốc `0x82a84d4`, không suy luận mã từ tên cầu thủ. Tên đọc từ trường English tại offset332, bổ sung các bí danh mod đã dùng trong bản73.

- Main: **286 giá trị thực sự xuất hiện**, nhỏ nhất0, lớn nhất342.
- Memorial: **32 giá trị thực sự xuất hiện**, nhỏ nhất0, lớn nhất33.
- Tổng **318 nhóm**, **1.544 dòng thẻ**. Tối đa6 ID thẻ khác nhau mỗi nhóm; ưu tiên tên khác nhau, rồi các phiên bản thẻ khác của cùng người. **97 nhóm có ít hơn6 thẻ** trong dữ liệu; liệt kê đúng số có thật.
- Cột trình bày rõ **ID ăn mừng | ID cầu thủ | Tên cầu thủ**; hai loại được tách thành hai bảng.0 là giá trị mặc định, không chứng minh một động tác riêng.
- Hai trường này **không phải mã số trong tên file animation**. Không xác nhận542/571/595 là ID lưu trực tiếp của các trường trên hoặc gán chúng cho cầu thủ nếu chưa có bằng chứng.
- Đã kiểm tra **tất cả318 giá trị** đọc lại đúng qua setter/getter gốc. Danh sách xác minh giá trị sở hữu trong dữ liệu; **chưa chạy từng animation trên điện thoại**, nên không tuyên bố tất cả ID là318 động tác độc lập.

## Kiểm tra

[storage-validation.json](storage-validation.json): nâng cấp dữ liệu chiều cao/cân nặng có backup, giới hạn cũ, cờ skill, Additional Skills, lựa chọn ăn mừng, sở hữu thẻ, rollback khi ghi lỗi, các phép chiếu dữ liệu không phát sinh SQL.

[native-validation.json](native-validation.json): chạy thư viện ARM64 thực qua Unicorn, đọc tham số bằng hàm gốc73, cả318 giá trị ăn mừng, phạm vi giải đấu,6 palette theo full64ID và callback trước bước bake gốc. Ranh giới bake được mô phỏng, chưa chạy GPU Android.

[package-validation.json](package-validation.json): ZIP CRC, manifest đầy đủ, hash runtime, DEX giữ các lớp cũ, không thêm trampoline, tìm kiếm giữ nguyên, không đóng gói save. [login-validation.json](login-validation.json): bộ gateway73 thực khởi tạo và CMD_LOGIN mã hóa trả NOERR; các phần Android được mô phỏng trên host.

Chưa kiểm thử render màu da/động tác và độ trễ UI trên điện thoại. Search/index cũ không đổi; dữ liệu lựa chọn tải theo yêu cầu, cache trong RAM; các lần đọc dữ liệu cầu thủ không thêm truy vấn SQL cho các mục mới.

Giữ các thay đổi trước: kits Y08/Y17, áo ngắn riêng89138556572074 và áo dài các Ronaldo đã yêu cầu, face aliases, giỏ catalogue, nhiều thẻ cùng cầu thủ, sửa nạp tài nguyên/đăng nhập, Player Model và giao diện Earth. Assets mặt/kits và thư viện face được giữ nguyên byte.
