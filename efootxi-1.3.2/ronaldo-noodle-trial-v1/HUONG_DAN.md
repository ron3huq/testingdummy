> Nếu đã vào game nhưng log báo thiếu `struct`, dùng [bản vá v1b](../ronaldo-noodle-hook-fix-v1b/HUONG_DAN.md).

> **Bản v1 gây lỗi kiểm tra gateway lúc khởi động.** Dùng [gói khôi phục và v1a đã sửa](../ronaldo-noodle-startup-fix/HUONG_DAN.md). ZIP tắt tóc cũ không sửa được lỗi khởi động.

# Bản thử tóc mì tôm Ronaldo — 88044950524330

Đây là bộ thử cho Android efootxi 1.3.2 ARM64, không cần root hoặc ký lại APK. **Chưa được chạy trên điện thoại**. Đã kiểm tra định dạng asset bằng UEViewer và logic chuyển hướng/fallback bằng thực thi ARM64 mô phỏng; các kiểm tra này không thay thế kiểm tra hình ảnh hoặc độ ổn định trong game.

Bản này giữ mặt Android theo 4 biến thể đầu đã trích, thay hình học tóc và dùng texture alpha ETC2 riêng. Chỉ thẻ **88044950524330** được chuyển sang asset riêng. Các thẻ Ronaldo khác và cầu thủ khác giữ đường nạp cũ. Không sửa dt200, dữ liệu save, chỉ số, đội hình, số áo hoặc cấu hình tay áo.

Tóc bản thử dùng màu tối và vật liệu Android một lớp. Hiệu ứng màu ngọn tóc/lớp màu thứ hai của mod PC chưa được tái tạo đầy đủ.

## Cài bằng MT Manager

1. Buộc dừng game. Sao lưu file hiện tại `files/embedded-gateway/work/tools/gateway_runtime.py` ra chỗ khác.
2. Giải nén `Ronaldo-noodle-trial-v1-88044950524330.zip`. Trong đó có hai thư mục `work` và `livedata`.
3. Chép **nội dung hai thư mục này** vào `files/embedded-gateway/` của game. Gộp thư mục và ghi đè file trùng tên; không xóa thư mục cũ.
4. Kiểm tra các file nằm đúng chỗ:
   - `files/embedded-gateway/work/tools/gateway_runtime.py`
   - `files/embedded-gateway/work/tools/noodle_hair.py`
   - `files/embedded-gateway/work/tools/libnoodle_hair.so`
   - `files/embedded-gateway/work/tools/noodle_hair.json`
   - `files/embedded-gateway/work/tools/noodle_bundle.json`
   - `files/embedded-gateway/livedata/pc9298_mobile_and.pak`
   - `files/embedded-gateway/livedata/pc9298_mobile_and.utoc`
   - `files/embedded-gateway/livedata/pc9298_mobile_and.ucas`
5. Mở game, chờ bước cập nhật dữ liệu hoàn tất. Dùng **đúng thẻ 88044950524330**, vào trận và quan sát tóc ở góc cận/replay. Không dùng thẻ Ronaldo khác để đánh giá bản này.

Bộ ZIP không có `myleague_editor.json`, `libselect_team.so` hoặc các file cấu hình giải đấu nên không ghi đè dự án đội hình hiện có. Nếu sau này thay `gateway_runtime.py` bằng bộ cũ, tính năng tóc có thể không được nạp; giữ ZIP này để cài lại khi cần.

## Xem kết quả / gửi log

Đọc file `files/embedded-gateway/work/tools/noodle-hair-status.json` sau khi vào sân:

- `state: HOOK_ACTIVE`: hook được cài, chưa tự chứng minh tóc hiển thị đúng.
- `payload_verified: true`: bộ file nguồn trên máy khớp mã kiểm tra; chưa tự chứng minh container được game mount.
- `manifest_advertised > 0`: gateway đã thêm gói pc9298 vào danh sách dữ liệu cho client.
- `target_calls > 0`: đã gặp actor có đúng full Card ID mục tiêu.
- `redirects > 0`: đã yêu cầu đầu riêng ND01, giữ nguyên hậu tố biến thể nguồn.
- `nonnull_callbacks > 0`: callback yêu cầu đó nhận được object; vẫn cần quan sát hình ảnh.
- `null_callbacks` / `restore_requests > 0`: tải mới trả null hoặc bị tắt giữa lúc tải; hook gọi đường nạp mặt gốc. Không tự thử lặp vô hạn.
- `last_face_id`: tên biến thể đầu mà game đã yêu cầu.
- `error`: lỗi ABI, chữ ký engine, checksum hoặc cài hook, nếu có.

`device_verified` luôn để false trong bản thử. Không đổi thành true chỉ vì các bộ đếm tăng.

Nếu chưa thấy tóc mới, gửi nội dung file status này cùng mô tả đã vào sân hay chỉ ở menu. Nếu lỗi gateway thêm gói, có thể xuất hiện `noodle-advertise-error.txt` cùng thư mục.

## Tắt / quay lại mặt cũ

Giải nén `Tat-noodle-hair.zip`, chép thư mục `work` vào cùng `files/embedded-gateway/`, ghi đè `noodle_hair.json`, sau đó **buộc dừng rồi mở lại game**.

Hoặc tự sửa `work/tools/noodle_hair.json` thành:

```json
{"enabled": false}
```

Bản tắt chỉ tắt chuyển hướng tóc; giữ danh sách gói tải ổn định để tránh đổi qua lại phiên bản livedata. Không cần xóa dữ liệu hoặc cache game. Tắt không làm mất đội hình/save. Nếu muốn bỏ hoàn toàn bộ thử, khôi phục `gateway_runtime.py` đã sao lưu khi game đã dừng; để lại các file gói không được tham chiếu không làm đổi các thẻ khác.

## Nguồn

Hình tóc và alpha chuyển từ mod PES 2021 PC NEUBE do người dùng cung cấp. Đầu/skeleton/material mẫu Android lấy từ dữ liệu người dùng gửi. UEViewer dùng để kiểm tra đọc asset; Etc2Comp dùng để nén ETC2. Không cài Sider PC.
