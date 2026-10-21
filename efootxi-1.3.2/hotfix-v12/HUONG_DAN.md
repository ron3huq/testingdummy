# Hotfix v12 — tay dài Ronaldo 89138556572074

V11 trên thiết bị đã báo `appearance_sleeve_applies: 0` và Ronaldo vẫn tay ngắn. V12 thêm đường sửa cấu hình ngoại hình theo ID thẻ được yêu cầu và bước chuyển cấu hình vào nhân vật, kèm bộ đếm từng bước. Đã kiểm tra mã ARM64 bằng Unicorn; **chưa xác nhận hình ảnh trên điện thoại**.

## Cài bằng MT Manager

1. Buộc dừng hoàn toàn efootxi, không chỉ thoát ra màn hình chính.
2. Sao lưu đủ 7 file hiện tại trong `files/embedded-gateway/work/tools/`.
3. Giải nén ZIP, chép **toàn bộ 7 file trong `install/work/tools/`** đè vào thư mục trên. Không chép thành thư mục con `tools/tools`.
4. Mở lại game, đưa đúng thẻ **89138556572074** vào đội hình và vào trận mới. Nhân vật đã được dựng trước khi cài phải được tải lại.
5. Mở `files/embedded-gateway/work/tools/select-team-status.json` bằng trình soạn thảo MT Manager.

## Kiểm tra

- `version` phải là `native-hotfix-v12`.
- `appearance_hooks`: ba mục `serialize`, `build`, `entity` phải là `INSTALLED`; `appearance_error` là `null` nếu cả ba cài được.
- `appearance_build_calls` / `appearance_entity_calls`: số lần game gọi hai bước mới, tính cả cầu thủ khác.
- `appearance_build_matches` / `appearance_entity_matches`: số lần nhận đúng ID thẻ Ronaldo. Không gộp tất cả thẻ Ronaldo.
- `appearance_sleeve_applies`: số lần ghi chế độ tay dài, có thể tăng nhiều lần cho cùng một cầu thủ; **không phải chứng nhận hình ảnh đã đúng**.
- `appearance_build_before` / `appearance_entity_before`: chế độ trước khi ghi, `0` tay ngắn, `1` tay dài. Bản sửa ghi `1` vào cấu hình.
- `appearance_last_build_id` / `appearance_last_entity_id`: ID của lần gọi gần nhất, có thể là cầu thủ khác vì game dựng cả đội.

Nếu vẫn tay ngắn, gửi phần từ `version` đến các trường `appearance_*` **sau khi đã vào trận mới có đúng thẻ**. Bộ đếm mới phân biệt hook không được gọi, không gặp đúng ID, và cấu hình đã sửa nhưng khâu dựng áo còn bỏ qua.

Bản này giữ nguyên mã mô phỏng v10, đội hình, chỉ số, lịch và save của v11. Không thay dt200, CPK, APK hoặc cơ sở dữ liệu. Tóc chưa được ghép. Muốn phục hồi, buộc dừng rồi chép lại đủ 7 file đã sao lưu.
