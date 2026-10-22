# Ronaldo noodle v1b — sửa lỗi thiếu import struct

Người dùng xác nhận đã vào game được sau bản trước, nhưng tóc chưa đổi. Log điện thoại ghi `state: ERROR`, `error: name 'struct' is not defined`. `payload_verified: true` chỉ xác nhận tệp đủ và đúng checksum, chưa xác nhận hook hay tóc hiển thị.

## Cài bản vá nhỏ

1. Buộc dừng efootxi.
2. Giải nén `Ronaldo-noodle-v1b-sua-hook.zip`.
3. Gộp thư mục `work/` vào **`files/embedded-gateway/`** trong MT Manager, cho phép ghi đè. Không tạo thêm tầng thư mục `embedded-gateway/work/work`.
4. Mở game, vào sân với **đúng Card ID `88044950524330`**. Thẻ Ronaldo khác không được đổi.
5. Đọc `files/embedded-gateway/work/tools/noodle-hair-status.json`: phiên bản mới phải là `ronaldo-noodle-trial-v1b`. Khi hook cài xong, `state` là `HOOK_ACTIVE`, `error` là `null`. `redirects` tăng mới cho biết có yêu cầu tải đầu đúng thẻ đi qua hook; điều này vẫn chưa xác nhận hình ảnh đã render đúng.

ZIP có ba tệp: `gateway_runtime.py` (byte-identical bản v1a 2441 byte), `noodle_hair.py` (thêm import struct, đổi nhãn phiên bản log), `noodle_hair.json` (enabled true). Cần có sẵn bundle/assets/native từ v1 hoặc v1a, vì log vừa gửi đã xác nhận payload_verified true. Không cài lại gói khôi phục sau bản vá vì gói đó tắt thử tóc. Không sửa save, đội hình, dt200, dt870, manifest dữ liệu hoặc asset tóc trong bản vá này.

Đã tái hiện NameError của mã cũ, chạy được jump() mới, chạy đầy đủ hai nhánh Python install và worker tới HOOK_ACTIVE với biên ctypes/native được mô hình hóa; đối chiếu SHA/prologue với libUE4.so Android nguồn. **Chưa chạy bản vá v1b trên điện thoại, chưa xác nhận tóc hiển thị.** Đây không phải khẳng định đã sửa mọi vấn đề Live Update hoặc renderer.

Nếu tóc vẫn không đổi, chép log mới nguyên vẹn sau khi vào sân, đặc biệt state, version, error, manifest_advertised, target_calls, redirects, null_callbacks, nonnull_callbacks, restore_requests, last_face_id. Không cần xóa dữ liệu ứng dụng.
