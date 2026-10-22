> Nếu đã vào game nhưng log báo thiếu `struct`, dùng [bản vá v1b](../ronaldo-noodle-hook-fix-v1b/HUONG_DAN.md).

# Sửa lỗi khởi động sau gói tóc Ronaldo v1

Lỗi `本地支持文件校验失败：work/tools/gateway_runtime.py` xảy ra trước khi nạp tóc.
Gói thử v1 đã thay tệp gateway thành 3081 byte. Manifest APK được phân tích khai báo 2441 byte; GatewayGuard.prepare thấy khác kích thước sẽ chạy nhánh sửa từ asset rồi kiểm tra SHA. Nếu asset trong APK đã chỉnh mà manifest chưa cập nhật thì nhánh này báo lỗi như ảnh. Chưa có APK đang cài của người dùng để xác nhận hash asset bên trong.

## Khôi phục khởi động trước

1. Buộc dừng efootxi. Không xóa dữ liệu, không gỡ cài đặt.
2. Tải `Khoi-phuc-khoi-dong.zip`, giải nén.
3. Trong MT Manager, gộp thư mục `work/` vào **`files/embedded-gateway/`** của ứng dụng. Cho phép ghi đè hai tệp `work/tools/gateway_runtime.py` và `work/tools/noodle_hair.json`.
4. Mở lại game. Gói này khôi phục logic gateway v18, tắt thử tóc, giữ các module My League và cấu hình hiện có. Không chứa save, database, dt200 hoặc đội hình.

## Thử lại tóc sau khi game mở được

Tải `Ronaldo-noodle-trial-v1a-startup-fixed.zip`, giải nén rồi gộp `work/` và `livedata/` vào **`files/embedded-gateway/`**, buộc dừng/mở lại ứng dụng. Không cài lại ZIP v1 cũ. Cơ chế tóc chỉ nhắm Card ID `88044950524330`. Mọi giới hạn hình ảnh của v1 vẫn giữ nguyên: tóc tối, chưa tái tạo lớp màu ngọn tóc PC, chưa xác nhận hiển thị trên điện thoại.

Gói v1a giữ nguyên AST Python của gateway v1, rút gọn khoảng trắng và thêm comment để đủ đúng 2441 byte. Đã đối chiếu nhánh kiểm tra của DEX và manifest APK nguồn, xác nhận kích thước, cú pháp, AST không đổi, kiểm tra gateway manifest/delivery lại và CRC ZIP. Không sửa DEX hoặc tắt trình kiểm tra; không sửa manifest trong APK. **Đây là kiểm tra trên máy phân tích, chưa xác nhận khởi động trên điện thoại.**

Nếu vẫn hiện cùng lỗi, cần nội dung dòng `work/tools/gateway_runtime.py` trong `assets/gateway-release/release-manifest.json` của **APK đang cài** (mở APK bằng MT Manager) và dung lượng tệp sau chép. Không xóa save để thử sửa.

`Tat-noodle-hair.zip` cũ chỉ tắt hook, không sửa tệp gateway và không chữa được lỗi khởi động này.
