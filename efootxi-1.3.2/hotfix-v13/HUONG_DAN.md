# Hotfix v13 — tay dài tại bước nạp áo

Người dùng xác nhận v12 vẫn tay ngắn sau khi vào sân. Cả ba hook cài được, builder gọi24 lần nhưng không gặp đúng ID thẻ, entity không gọi. Không kết luận ID114758 là Ronaldo: Player.bin xác nhận đó là Marc Cardona, chỉ là ID cuối trong log.

V13 thêm hook ngay trước hàm nạp áo UE: đọc ID của nhân vật đang nạp áo, ghi chế độ tay dài trước khi game chọn tài nguyên áo ngắn/dài. Đã kiểm tra mã ARM64 đến lệnh gọi LoadUniShirt; **chưa có xác nhận hình ảnh trên Android**.

## Cài MT Manager

1. Buộc dừng hoàn toàn efootxi.
2. Sao lưu đủ7 file trong `files/embedded-gateway/work/tools/`.
3. Giải nén ZIP, chép đủ **7 file trong `install/work/tools/`** đè vào thư mục trên, không tạo thư mục `tools/tools`.
4. Mở game và vào trận mới có thẻ **89138556572074**.
5. Xem tay áo trong trận, sau đó mở `files/embedded-gateway/work/tools/select-team-status.json`.

## Trường cần kiểm tra

- `version`: `native-hotfix-v13`.
- `appearance_hooks.shirt`: `INSTALLED`.
- `appearance_shirt_calls`: tổng số lần gọi hàm nạp áo, không riêng Ronaldo.
- `appearance_shirt_matches`: khớp trực tiếp ID thẻ89138556572074.
- `appearance_shirt_alias_matches`: khớp ID Ronaldo dùng chung4522 hoặc16781738.
- `appearance_shirt_applies`: số lần đã ghi tay dài ở bước nạp áo.
- `appearance_shirt_before` / `appearance_shirt_after`: chế độ trước/sau ghi; sau phải là1 khi đã ghi. Đây là giá trị cấu hình, không phải chứng nhận hình ảnh.
- `appearance_build_ids` / `appearance_shirt_ids`: các ID xuất hiện trong tối đa64 lượt gọi gần nhất mỗi đường. Dùng để điều tra nếu vẫn không áp dụng.
- `appearance_error`: lỗi cài từng hook nếu có.

Nếu vẫn tay ngắn, gửi các trường trên **sau khi đã vào sân**, đặc biệt hai danh sách ID. Việc entity_calls vẫn0 không tự nó là lỗi nếu game đi đường nạp áo khác.

## Phạm vi và giới hạn

Ba ID được nhận diện: thẻ89138556572074 và hai bản ghi4522/16781738 đều tên Cristiano Ronaldo trong Player.bin. Không dùng phép cắt bit để nhận diện mọi ID. Nếu game dùng ID chung4522/16781738 cho các thẻ Ronaldo khác, các thẻ đó cũng có thể nhận tay dài; lúc đó riêng ID dựng hình không đủ phân biệt thẻ. Các thẻ full64 Ronaldo khác vẫn không khớp nếu game giữ nguyên full64 ID.

Không đổi tóc/mặt, chỉ số, roster, lịch, save, dt200, APK hay CPK. Mã mô phỏng giữ nguyên v10. Phục hồi bằng cách buộc dừng và chép lại đủ7 file đã sao lưu.
