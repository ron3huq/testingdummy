# UI7.12 full — 73 V16

Bộ **áp vào APK nền 73 V16 / com.efootball.revival.local**, gồm đủ bốn ZIP bên dưới. Không phải APK cài độc lập và không dùng cho efootxi1.4.1. Không cần áp chồng các UI cũ.

1. `V25-73-UI7.12-FULL-Part1-Faces-MT.zip`
2. `V25-73-UI7.12-FULL-Part2-Main-MT.zip`
3. `V25-73-UI7.12-FULL-Part3-Prior-Faces-MT.zip`
4. `V25-73-UI7.12-FULL-Part4-New-Faces-Sleeves-MT.zip`

Trong MT Manager, mở từng ZIP và **chép các mục ở thư mục gốc của ZIP vào gốc cùng một APK**, chọn thay thế; không chép nguyên ZIP vào APK. Áp đủ bốn phần rồi mới ký APK. Dùng cùng khóa ký đang dùng để cài cập nhật và giữ dữ liệu. Sao lưu save trước khi thay APK; không cần gỡ game/xóa dữ liệu. Đối chiếu SHA256 SUMS.txt nếu tải gặp lỗi.

Màn hình khởi động phải hiện **UI7.12 Earth**. Các chỉnh sửa được lưu trước khi nhấn Enter Game; sau khi sửa hãy đóng hẳn và mở lại ứng dụng. Không hỗ trợ đổi tài nguyên/đội hình giữa trận.

## Thay đổi mới

- **Sáu face đúng ID:** Ronaldo2018→88042803047215; R9→105634720685845; Zidane→105565464400480; Henry→105625593957752; RonaldoMulletV8→89138288266704; YanDiomande của Real Madrid My League→176104. Giữ face cũ của84062184. Không nạp mã chạy thử trong các gói người dùng gửi. Đã đọc lại độc lập24 biến thể mesh, cả hai LOD, skin weights và166 xương.
- **Player Attributes:**26 chỉ số, ghi số thật vào dữ liệu/native của đúng thẻ. Mỗi ô ghiMin0/Max127. Đây là giới hạn **lưu trữ native 7 bit**;128 quay về0 nên bị từ chối. Không khẳng định127 vượt mọi mức trần hiệu lực của gameplay. Không đổi chiều cao/cân nặng vượt giới hạn140–220 cm/40–130 kg đã giữ từ bản trước.
- **Import photo · Crop & Preview** trongCard Background: chọn ảnh trên máy, kéo/zoom độc lập cho miniface128 ×128 vàảnh lớn184 ×256, hướng dẫn vị trí mặt, xem hai crop. Giữ tỉ lệ, hỗ trợPNG trong suốt, ghi texture native trong gói riêngpc9311 theo từng phiên bản tài nguyên, không ghi đè face/nền. Tối đa256 thẻ. **Preview hiện tại là crop và khung căn ảnh, chưa mô phỏng pixel-chuẩn toàn bộ khung/nhãn/chữ/OVR mà game thêm vào.** Có thể chọn lại nền và nhập ảnhPNG trong suốt để nền hiện qua.
- **Transfer** tạiPlay&Manage:835 đội trong danh mục dữ liệu native; chọn đúng giải trước khi chỉnh. Thêm/bỏ cầu thủ dự bị, đổi người trong11 vị trí, kéo tọa độ đội hình, số áo1–99, đội trưởng/sáu người đá phạt, chuyển cầu thủ dự bị giữa hai đội bằng một giao dịch, chọn áo có tài nguyên thật cho bốn slot. Không bịa đội hình hiện tại:22 đội cổ điển có cấu hình native đã kiểm; đội khác cần snapshot native thu khi vào game rồi đóng/mở lại. Các snapshot đội thường được lấy theo từng đợt nhỏ; đội chưa có snapshot sẽ báo chưa sẵn sàng. Tối đa128 đội được chỉnh đồng thời. Hai slot trắng/đen mặc định chưa có áo thật thì được ghi rõ làfallback; không giả thànhkitsđã tải.
- **Accessories:** sửa băng cổ tay ở dữ liệu packed trước bộ chuyển đổi và tiếp tục áp flags sau chuyển đổi. Tám điều khiển đã xác định: quần bó ngắn/dài, băng cổ tay trái/phải, băng cổ chân, găng cầu thủ, áo lót thường/cao cổ. Cao cổ dùng đúng cặpflag8+9. Có bảng màu minh họa, **màu riêng cho từng phụ kiện bằng#RRGGBB**, hoặc trả về màu gốc;alpha luôn255. Không đổi màu da. Không thêm găng thủ môn vào mục này. Đã khảo sát18 flag của converter và registrymesh; các flag nội bộ chưa định danh chắc chắn không được mở thành lựa chọn giả. Băng đội trưởng đi theo vai tròCaptain trongTransfer.
- **Animation · Copy native motion:** tìm theo tên/ID từ46464 recordnative; sao chép8 trường đã xác minh: kiểu rê bóng, tư thế/tay khi rê, tư thế/tay khi chạy, kiểu đá phạt, penalty, góc. Giữface/body/chỉ số/ăn mừng. **Chưa chứng minh sao chép được mọi animation độc quyền theo danh tính, như tất cả kiểu chuyền riêng củaBeckham.** Không giả đổi ID cầu thủ để tuyên bố đã sao chép toàn bộ.
- **Del Piero89139630444046** thêm vào nguồnCard Background.
- **World Nation League128:** thêm skill đặc biệt theo13 nhóm vị trí vào mọi cầu thủ trong giải, giữ skill gốc vàadditionalskills. Nhữngflag do tính năng này thêm được phục hồi khi ra khỏi giải.
- **Cut native long sleeves · forearm:** tùy chọn riêng trongSleeveLength, không thay thếLong sleeves · original shirt. Cắt phần vải dưới mức khoảng60%cẳng tay từ mesh áo dài native; bổ sung da cẳng tay từ template gốc tương thích, không kéo/scale tay.123 mesh áo dài gốc,246 LOD, giữ bind pose riêng và166 xương; đườngdetail/lowbody được giữ riêng. Chỉ áp dụng cho thẻ chọn tùy chọn này, mọikitsdùng các biến thể native được hỗ trợ. Model ngoài danh sách sẽ giữ áo dài nguyên bản và được đếm trongdiagnostics, không trỏ tới file thiếu.

Các tính năng từUI7.11 được giữ:face/thẻ trước đây, kits/đội hìnhY08/Y17, huấn luyện viên gốc, cartcatalogue, tìm không dấu, level100, kỹ năng gốc, skinpalettegốc, player model, tên/tuổi/chân thuận, ăn mừng và các sửa khởi tạo/tài nguyên. Các phân vùngSL0 T/CPKđược giữ riêng;pc9298/9305–9308 không bị gói face mới ghi đè.

## Kiểm chứng và giới hạn

Đã biên dịchJava/DEXvà hai thư việnARM64; chạy bộ getter/setter gốc73, kiểm tra giới hạn chỉ số, scopeID/giải/slotáo, copy motion và bảo toàn trường khác, thêm/phục hồi skill theo13 vị trí, màu phụ kiện/alpha, rollback/lưu dữ liệu, nativephotoIoStoređọc lại bằngUEViewer, cấu trúcface/cutmesh, đồng thời44 hookvàkhởi tạo gateway với bộ tài nguyên đầy đủ. Các báo cáo nằm trong`validation/`;sourceở`source/`.

**Chưa chạy trực tiếp APK trên điện thoại/GPU.** Các kiểm tra trên không thay cho việc kiểm tra trong trận, replay, ăn mừng và đoFPS trên thiết bị thật; không thể cam kết “100%không lỗi/không trễ dù1 giây”. Những giới hạn riêng vềpreview/animation/snapshot được ghi rõ bên trên. GửiRuntimeDiagnosticsmới nếu có lỗi; không cần xóa game để lấy log.
