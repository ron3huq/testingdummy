# Hotfix v14 — đúng ID Ronaldo đã xuất hiện trên thiết bị

Log v13 ở giải518 ghi nhận ID88044950524330 trong appearance_build_ids, không có89138556572074. Builder chạy24 lần, không khớp, shirt và entity đều0. **Không có bằng chứng hai ID thẻ này là alias của nhau.** V14 nhận đúng cả hai ID full64 một cách tường minh, thay vì đoán ID dùng chung.

## Cài bằng MT Manager

1. Buộc dừng hoàn toàn game, sao lưu đủ7 file trong files/embedded-gateway/work/tools/.
2. Giải nén ZIP. Chép đủ **7 file trong install/work/tools/** đè vào thư mục trên.
3. Mở lại và vào trận mới có Ronaldo88044950524330 hoặc89138556572074.
4. Kiểm tra áo trong trận rồi mở files/embedded-gateway/work/tools/select-team-status.json.

## Kết quả cấu hình cần thấy

- version: native-hotfix-v14.
- appearance_hooks.build: INSTALLED; appearance_error: null nếu cài tất cả hook được.
- appearance_build_matches_by_id.88044950524330: lớn hơn0 khi nhân vật với ID này đã được dựng.
- appearance_last_applied_id:88044950524330 nếu đó là ID vừa nhận thay đổi gần nhất, hoặc89138556572074 nếu thẻ kia vừa được dựng.
- appearance_build_after:1 sau lần ghi, là chế độ tay dài trong cấu hình native.
- appearance_sleeve_applies: lớn hơn0.

Shirt_calls hoặc entity_calls vẫn0 không ngăn đường builder áp dụng. Nếu sau khi vào sân vẫn tay ngắn, gửi các trường trên cùng appearance_build_ids; không dùng bộ đếm shirt làm điều kiện duy nhất nữa. Bộ đếm dương chỉ chứng minh ghi cấu hình, vẫn cần kiểm tra hình ảnh thực tế.

## Phạm vi

V14 chỉ nhắm hai thẻ89138556572074 và88044950524330. Đã **bỏ fallback ID chung4522/16781738 của v13**. Không đổi tóc, mặt, chỉ số, save, lịch hoặc mô phỏng. Không thay dt200/APK/CPK. Phục hồi bằng cách buộc dừng và chép lại đủ7 file đã sao lưu.

## Mã đội hình14 trong log

Mã14 ở1220 (Real Madrid cổ điển),1221 (Liverpool cổ điển) nghĩa là chốt kiểm tra đã bỏ qua ghi roster khi một slot cũ có PlayerKey.kind khác0. Đây là trạng thái của lần áp dụng roster, không phải lỗi cài tay áo. V14 giữ chốt này; không ép ghi cấu trúc chưa được xác minh. Log hiện tại chưa có dữ liệu từng slot để xác định vì sao kind khác0 trên hai bản ghi này.

Đã chạy thử22 ID từ log qua mã builder ARM64 gốc với boundary DB mô hình hóa: chỉ ID Ronaldo88044950524330 trong danh sách đó được đặt tay dài. Cả hai ID tường minh, bộ đếm riêng, serializer, chọn tài nguyên áo và các kiểm tra hồi quy đã qua. **Chưa kiểm chứng hình ảnh tay dài trên điện thoại.**
