# V22 — sửa cằm/miniface, bổ sung font áo và đối chiếu vật liệu đầu đen

**Chưa xác nhận sửa hết bốn đầu đen trên điện thoại.** V21 đã thất bại theo phản hồi thực tế, kể cả đầu 2017 đặt lên Nicolás González. Vì vậy v22 không gọi các bộ đếm `confirmed` là bằng chứng hình ảnh đúng.

Cài một gói đầy đủ: **Faces-v22-jaw-fonts-mini-material-probe.zip**. Đã gồm các nội dung v21 và sửa crash Đội hình v20a; không cần cài gói cũ sau nó.

1. Buộc dừng game trong Cài đặt Android.
2. Giải nén ZIP, dùng MT Manager gộp **cả `work/` và `livedata/`** vào `files/embedded-gateway/`, chép đè tệp trùng tên.
3. Mở game. `work/tools/noodle-hair-status.json` phải ghi `player-faces-v22-draw-probe-jaw-fonts`, `HOOK_ACTIVE`, `error: null`.

Không xóa save/dữ liệu ứng dụng. Gói không ghi đè cấu hình đội hình/chỉ số My League cá nhân, không sửa libUE4. `gateway_runtime.py` giữ nguyên 2441 byte.

## Đối chiếu đầu đen: chỉ một biến trên thẻ thử

Bốn thẻ lỗi gốc vẫn là Ronaldo 2017 `88044950524330`, 2027 `106734785925546`, Jr `105765448873424`, Hoang Duc `105643042189511`. Asset của cả bốn **giữ nguyên v21**; không tuyên bố đã sửa chúng bằng một lần ép material khác.

Riêng **thẻ thử Nicolás González `105807861630781`** dùng `NT01ep00v0313`: toàn bộ hình học, tóc, UV, trọng số và skeleton của đầu 2017 giữ nguyên; chỉ hai skin material trỏ trực tiếp tới material ND06 đang hoạt động trên đầu 2006. Texture redirect của thẻ thử cũng trỏ ND06. Màu/chi tiết da của thẻ thử có thể khác 2017; đây là đối chiếu vật liệu, không phải face hoàn chỉnh thay thế bốn đầu.

Sau cài, xem đầu 2017 gốc và thẻ thử trong trận/cutscene, chờ vài giây rồi gửi:

- Thẻ thử còn đen hay đã lên màu?
- Log **v22 mới** `work/tools/noodle-hair-status.json`, gồm phần `head_draw_probes`.

Không cần gửi lại toàn bộ nguồn hoặc thư mục game. Nếu thẻ thử có màu, kết quả khoanh vùng vào bộ material/texture của 2017; nếu vẫn đen thì chưa thể kết luận do texture. Log mới liệt kê mesh chính, các mesh phụ, material/parent và texture thực tế sau bake. Probe chỉ đọc, không tự ẩn mesh/thân người hoặc đổi cờ render. Nó giữ mẫu riêng theo thẻ; `consistent_snapshot: false` là mẫu đang được cập nhật, không dùng để kết luận. Đường dẫn đầu thẻ thử phải chứa **NT01**.

V22 cũng sửa cách xuất ID 64 bit trong log: những ID âm hoặc số bị cắt ở v21 là lỗi báo cáo, không chứng minh engine đã đổi ID thẻ.

## Cằm Đình Bắc và Özil

Sửa phân bố trọng số giữa xương đầu/hàm ở vùng dưới mặt, thay vì chỉ vá đường nối. Trong sáu tư thế xoay hàm tổng hợp theo bind native, tổng số tam giác đảo hướng vùng thử giảm Özil **718 → 52**, Đình Bắc **591 → 41**. Vẫn còn trường hợp gập ở góc thử lớn; đây không phải cam kết đã hết mọi biến dạng trên điện thoại.

Giữ nguyên vị trí đỉnh, UV, normal, hình tóc, 135 đỉnh mắt/miệng native, toàn bộ trọng số phần trên mặt và phụ kiện. Hàm vẫn cử động; không khóa cằm. LOD1 với rig giảm giữ nguyên. Skeleton/inverse bind 166 xương và RequiredBones 166/153 giữ nguyên để tránh tái phát lỗi kéo dài chi.

## Miniface và áo

Bốn miniface Ronaldo có tư thế riêng theo ảnh tham khảo: 2017 chỉ tai, 2006 đưa tay im lặng, 2008 ăn mừng áo đỏ, 2013 ăn mừng áo trắng. Texture mini đúng 128×128, cắt riêng người trên nền alpha; không ép ảnh thẻ dọc vào hình vuông. **Toàn bộ ảnh lớn và nền v21 giữ nguyên từng byte.** Không thay nền người dùng đã đánh giá đẹp.

Log v21 cho thấy game gọi `T_u0352p1_FontName_Ex_D`, trong khi gói chỉ có atlas A–Z thường. V22 bổ sung tám atlas `FontName_Ex_D` cho hai bộ áo của Sparta, Telstar, AZ, Heerenveen, giữ block alpha gốc native và màu chữ của v21. Atlas Ex là bộ ký tự Latin mở rộng, dùng họ font native dự phòng vì chưa có bản Ex đúng họ của bốn kit. **Font A–Z thường, kích thước và layout gốc giữ nguyên từng byte**; không cưỡng ép một font trong runtime. Chưa xác nhận việc bổ sung này làm tên áo hiện lại trên máy.

Các tên áo đầy đủ dạng `XUAN SON`, `DINH BAC`, `HOANG DUC`, `HOANG HEN`, `QUANG VINH`, `TAI LOC`, `ISHOWSPEED`, `RONALDO JR`, `OZIL` giữ quy tắc v21. Giữ màu số/tên theo từng kit, quốc tịch/CLB, chỉ số/vị trí và áo dài tay đã thiết lập. V22 không sửa các mặt khác đang hoạt động tốt.

## Kiểm tra đã thực hiện

Đọc lại container bằng UEViewer độc lập; so sánh chính xác phạm vi sáu chunk thay đổi/chín chunk mới, skeleton/UV/phụ kiện/LOD; mô phỏng hàm; kiểm tra EAC alpha và bốn mini. Native harness chạy 578 kiểm tra nền cùng probe chỉ đọc, ID 64 bit, fallback, đủ 23 đối số builder Đội hình và 15 điểm cài hook. ZIP có kiểm tra CRC/hash và thử runtime khi payload hỏng.

**Không có thiết bị Android nối trực tiếp trong môi trường build. Kết quả host không thay thế kiểm tra GPU/replay/tên áo trên máy.**
