# FULL8 RC21 · UCL hai lượt · nền v19.1 + FULL8 RC7

Gói FULL tích lũy dành cho APK v19.1 đã sign mà bạn đang áp FULL8-RC7-complete-APK73.zip bằng MT Manager. Bao gồm toàn bộ payload RC7 và phần UCL mới; không cần cài RC8–RC20. Đây là bản ứng viên để thử trên Android, chưa được xác nhận trên điện thoại. Không phải APK đã ký.

## Cách áp bằng MT Manager

1. Sao lưu APK đang chơi và dữ liệu/save theo cách bạn vẫn dùng. Giữ ứng dụng hiện tại.
2. Mở bản sao APK v19.1 đã sign trong MT Manager. Chép đè toàn bộ thư mục `assets/` và tệp `classes5.dex` từ ZIP này vào gốc APK; giữ các assets khác của APK nền.
3. Lưu ZIP/APK, ký bằng ĐÚNG khóa đã ký bản đang cài, rồi cập nhật đè. Không gỡ ứng dụng hoặc xóa data. Nếu không có khóa cũ, không thể bảo đảm cài đè giữ dữ liệu.
4. Mở game để các tài nguyên mới được cập nhật. Trong launcher chọn **UEFA Champions League**, chọn **Mùa mới**, CLB và độ khó, sau đó **Chọn UCL**. Vào game mở **My League** để thi đấu mùa UCL. Mùa My League thường dùng vùng lưu riêng.
5. Để về giải thường, hoàn tất trận đang chờ rồi chọn **Về My League thường** trong bảng UCL. Mùa UCL vẫn được lưu. Mùa UCL một lượt đã tạo từ prototype cũ được giữ thể thức; tạo mùa mới để dùng hai lượt.

## Thể thức

- 36 CLB, 8 vòng league phase, mỗi đội 4 sân nhà/4 sân khách; 1–8 vào thẳng vòng 1/8, 9–24 play-off, 25–36 bị loại.
- Play-off, vòng 1/8, tứ kết, bán kết: lượt đi–lượt về. Chung kết: một trận.
- Không luật bàn thắng sân khách. Lượt đi không hiệp phụ/luân lưu. Lượt về chỉ vào hiệp phụ nếu hòa TỔNG tỷ số sau 90 phút; hết hiệp phụ còn hòa thì luân lưu.
- Bàn lượt đi được chuyển đúng bên khi đảo sân. Tỷ số từng lượt lưu riêng; tổng tỷ số không cộng giả vào bàn trận hiện tại. Lịch đấu launcher có cột tổng ở lượt về.
- Có Como, Dortmund, Betis theo danh sách nghiên cứu. Nhóm hạt giống dùng sức mạnh trong game, không phải hệ số UEFA chính thức. Bảng ghi bàn/kiến tạo chỉ hiển thị dữ liệu có thật; độ phủ sự kiện cầu thủ/CPU còn hạn chế.

## Phần thực sự đã làm và giới hạn

RC21 có provider Python được nối vào bootstrap và thư viện ARM64 `libucl_rules.so`; không còn chỉ là mã mô phỏng mùa giải. Hook native dựng RuleInput ghi cả nhóm AI/HUD lẫn nhóm cờ/carry mà nhánh hết 90/120 phút thực sự đọc. Chỉ nhận engine v19.1 có SHA256 `efd257d9e41b622d6ecb8f51f7b0a8ee8820113fd427c5572025df1c8eecc7b8`; lệch engine/checksum sẽ không cho bật UCL.

Đã chạy nhánh native điều khiển hết 90/120 phút và setter chuyển giai đoạn bằng giả lập ARM64 với 405 tình huống. Đã kiểm tra entry branch, slot/trampoline, đảo sân, phiên trận, retry, khôi phục và lưu tổng tỷ số. Ngữ cảnh game, nguồn thống kê bàn thắng và thân hàm dựng RuleInput được cung cấp tại ranh giới fixture trong kiểm tra; chưa chạy toàn bộ vòng cập nhật gameplay, giao diện kết thúc trận hay Android thật. Vì vậy không gọi bản này là đã hoàn thiện/đã xác nhận trên điện thoại.

Giữ nguyên toàn bộ thư viện native và livedata của RC7, gồm Transfer, Single Player và bản Ronaldo2027 RG28. Không áp thêm sửa Ronaldo đang dang dở từ bàn giao: mí mắt/rig răng-lưỡi RC7 chưa được xác nhận SIUU và ánh sáng trên máy. Các báo cáo RC7–RC20 trong source/validation là lịch sử; kết quả mới có tiền tố `full8-rc21-`.

Nếu nút UCL chưa sẵn sàng, chờ native khởi động và mở lại bảng UCL; nếu vẫn không sẵn sàng thì dừng thử UCL để kiểm tra đúng APK/engine, không bỏ kiểm tra checksum. Khi thử lượt về: kiểm tra trường hợp thua lượt đi 0–1 rồi thắng lượt về 1–0 phải có hiệp phụ; hòa lượt về khi tổng không hòa phải kết thúc; hòa tổng sau hiệp phụ phải luân lưu. Chỉ kết quả thử điện thoại mới xác nhận trọn luồng.

Không chứa APK, libUE4.so, engine v25, save/DB cá nhân hoặc Blend. Không xuất bản môi trường hay đẩy GitHub. Source và kết quả host được kèm để truy vết và tiếp tục sửa nếu Android phản hồi lỗi.
