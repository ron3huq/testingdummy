# V23 — dựng lại đầu từ nguồn, Özil V2 và căn tâm miniface

**Gói đầy đủ duy nhất:** `Faces-v23-source-heads-OzilV2-centered-minis.zip`.

1. Buộc dừng game trong Cài đặt Android.
2. Giải nén; dùng MT Manager gộp **cả `work/` và `livedata/`** vào `files/embedded-gateway/`, chép đè tệp trùng tên.
3. Mở game. Log `work/tools/noodle-hair-status.json` phải ghi `player-faces-v23-source-rebuild-stability`, `HOOK_ACTIVE`, `error: null`.

Không cài chồng v22 sau gói này. Không xóa save hoặc dữ liệu ứng dụng. Gói không sửa libUE4 và không ghi đè cấu hình My League cá nhân.

## Crash v22

Log bạn gửi khớp đúng SHA của v22 đã phát hành: có 9 redirect nhưng ảnh chụp log chưa ghi nhận callback tải mesh hoàn tất. Không có fatal backtrace nên **chưa xác định được chính xác lệnh gây crash**.

V23 bỏ toàn bộ probe gọi truy vấn mesh/material/texture mới trong v22, bỏ asset NT01 và tám atlas Ex mới của v22. Native trở lại đúng mã v21, chỉ thêm hàm thuần đọc để báo ID 64 bit không bị cắt. Không còn đọc các mảng component để làm probe hoặc gọi các truy vấn material mới sau callback. Vẫn giữ sửa ABI builder Đội hình đủ 23 đối số và 15 điểm cài hook đã kiểm tra. Đây là giảm phạm vi thay đổi so với bản gây lỗi, **không phải xác nhận đã hết crash trên máy**.

Việc rút atlas Ex cũng rút thay đổi font thử nghiệm của v22. Font A–Z và kit v21 giữ nguyên; v23 không tuyên bố đã sửa phần tên áo còn thiếu.

## Đầu đen và nguồn model

Nguồn 2017/2027 mới nhất đã gửi là `Ronaldo Noodle Hair 2017.rar` và `Ronaldo 2027.rar`, chứa FMDL/texture PES, không có `.blend`. Đã đối chiếu với nguồn 2006; chưa có bằng chứng nguồn bị thiếu texture hoặc Blender hỏng.

Khác biệt thực tế: nguồn có các pass FOX skin/scalp, eyeline, collar AO và head shell khác nhau. Trong nguồn 2027, toàn bộ đỉnh hai lớp shell nằm cách lớp skin không quá 0,05 cm; chúng không được ghép thành một lớp da đục thứ hai. Nguồn Özil V2 dùng `face_bsm` và texture scalp `hair_bsm_alp` riêng, không thể xử lý bằng giả định chỉ có `face_bsm_alp`.

V23 dựng lại **11 biến thể** từ hình học nguồn cho:

- Ronaldo 2017 `88044950524330`; thẻ thử `105807861630781` dùng cùng đầu này trở lại, không còn vật liệu đối chiếu 2006.
- Ronaldo 2027 `106734785925546`.
- Ronaldo Jr `105765448873424`.
- Nguyen Hoang Duc `105643042189511`.
- Mesut Özil `106778792700170`, thay bằng **Mesut_OZIL_V2.rar** vừa gửi.

Không nội suy hình mặt theo UV của 2006 như bản trước. Giữ vị trí đỉnh và tam giác skin/scalp của nguồn, chuyển trọng số theo tên xương Android, dựng lại tangent frame phù hợp UV nguồn. Không đưa các pass eyeline/collar-AO/shadow-shell của FOX thành da đục. Scalp Özil dùng ô texture riêng, tránh lấy nhầm texture da mặt.

Giữ skeleton/inverse bind 166 xương và RequiredBones LOD0/LOD1 166/153, tối đa 4 ảnh hưởng/đỉnh, tổng trọng số byte 255, palette dưới 75. Mắt và trong miệng dùng 135 đỉnh native, căn theo nguồn. Không ép material hoặc cờ bóng mỗi frame lên bốn đầu lỗi. Các mặt khác đang hoạt động tốt, bao gồm Đình Bắc với sửa cằm v22, giữ nguyên.

**Chưa xác nhận hết mặt đen trên renderer Android.** Thay đổi lần này là dựng lại asset từ nguồn và bỏ các can thiệp mới của v22; kiểm tra host không chứng minh GPU đã hiển thị đúng.

## Miniface

Bốn mini Ronaldo 2017/2006/2008/2013 giữ tư thế khác nhau. Căn theo vùng đầu đã đo, không lấy tâm toàn bộ ảnh có cánh tay: tâm ngang 64 trên texture 128×128, mép tóc trên 8 px, chiều cao vùng đầu 85 px. Dùng một hệ số phóng đồng đều cho mỗi ảnh, không nén/giãn riêng hai chiều. Nền alpha; không nhúng rating/khung/tên vào ảnh. Vẫn cần kiểm tra trong layout game thực tế.

**Tất cả ảnh thẻ lớn và nền v21 giữ nguyên từng byte.** Không thay nền bạn đã đánh giá đẹp. Các kit, màu tên/số, tên cầu thủ, quốc tịch/CLB, vị trí/chỉ số và áo dài tay giữ thiết lập v21/v22 ngoài các atlas Ex đã rút nêu trên.

## Kiểm tra và cách báo kết quả

Đã đọc lại độc lập 11 mesh và bốn mini bằng UEViewer; kiểm tra khớp vị trí/tam giác nguồn, skeleton/bone palette, trọng số, normal, phạm vi chunk thay đổi và nền cũ. Native chạy 578 kiểm tra nền, kiểm tra không còn probe, ID 64 bit, cài hook và hồi quy crash builder. ZIP kiểm tra CRC/SHA và fallback khi payload hỏng. Chưa có thiết bị Android nối trực tiếp.

Sau khi cài, thử màn hình trước trận và vào trận với đầu 2017/2027. Báo giúp **còn văng không và đầu nào còn đen**, kèm log v23 mới nếu còn lỗi. Không cần gửi lại nguồn cũ. Nếu vẫn văng, buộc dừng game rồi tạm đổi `work/tools/noodle_hair.json` thành `{"enabled":false}` để tắt redirect mặt; không xóa dữ liệu game. Log status không thay thế fatal crash trace.
