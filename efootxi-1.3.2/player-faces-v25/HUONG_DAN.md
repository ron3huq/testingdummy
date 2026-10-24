# V25 — thử Ronaldo 2017 Blender V3 trong game

Gói cài: **Faces-v25-Ronaldo2017-BlenderV3-test.zip**.
Thẻ được thay: **Ronaldo 2017 — 88044950524330**.

1. Buộc dừng game hoàn toàn trong Cài đặt Android.
2. Giải nén ZIP; gộp và chép đè **cả `work/` lẫn `livedata/`** vào
   `files/embedded-gateway/`, như các gói trước.
3. Mở lại game, xem đúng thẻ Ronaldo 2017 trên, sau đó kiểm tra trong trận
   và một cảnh replay/cắt cảnh.

Log `work/tools/noodle-hair-status.json` phải có:
- `version`: `player-faces-v25-2017-blender-v3-test`
- `state`: `HOOK_ACTIVE`, `error`: `null`
- Sau khi xem đúng thẻ, đường mesh mới có `SK_NV17..._Face`.

Nếu vẫn đen/tàng hình hoặc văng, gửi ảnh của đúng thẻ này và log V25 mới
sau lần thử. Không cần gửi lại file mặt nguồn.

## Nội dung bản thử

Dùng nền đầu/mặt 2006 đã hoạt động tốt, áp dụng phần chỉnh hàm/dưới cằm
và texture nối tóc/da đầu của Blender 2017 V3. Ghép tóc từ ronaldo2017.rar.
Hai bộ UV màu/alpha tóc được bake sang atlas UV riêng cho shader mobile.
Giữ mesh da, UV, topology, weight cổ từng LOD và mắt/miệng native của nền
2006; giữ skeleton/inverse bind và RequiredBones 166/153. Phần chỉnh hình
được áp dụng bằng delta nhỏ, không thay skeleton bằng skeleton PC.

Giữ shader/material da và normal/SRO đã dùng ở ND06. Bản thử đầu tiên này
không đưa shader procedural/mask độ bóng Blender vào engine. Chỉ cập nhật
RGB cần thiết trong atlas da, giữ các block texture không liên quan và
định dạng native. Vì thế ánh sáng trong game có thể khác render Blender.

Các face, kit, ảnh thẻ, tên áo, quốc tịch và chỉ số có sẵn trong V24 được
giữ nguyên. Bản 2014 vẫn là file Blender, không nằm trong gói thử này.
Gói chỉ chứa code/payload như V24, không chứa save hoặc cấu hình My League
cá nhân và không thay libUE4.so.

Đã kiểm tra đọc lại asset bằng UEViewer, trọng số cả hai LOD, material,
texture, phạm vi ID, hook và checksum ZIP. CPU-static-review.png là raster
mesh đã đóng gói, không phải ảnh chụp từ điện thoại. **Chưa xác nhận kết quả
render trên GPU Android; đây là gói để thử đúng một thẻ.**
