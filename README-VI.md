# APK73 V19.1 · FULL-8 RC1 · nền FULL-7

Gói tích lũy mới từ FULL-7 `74a1cd8100c8ecd022af9f16ef1f9f98cffcfc96`, gồm sửa ở bản ứng viên `7357d203` và sửa native/face lần này. Không chuyển sang efootxi/FULL-6. **RC1 chưa được xác nhận trên điện thoại; không phải cam kết đã hết mọi lỗi thực tế.**

## Transfer và dữ liệu vào native

Đã tái hiện lỗi bằng hàm engine gốc: trong DB mode 2, truy vấn `{0, full ID}` lấy record ở cache index 0, không tìm cầu thủ theo ID. Bridge mới phân biệt key theo ngữ cảnh, tìm lại record có đúng full ID và chỉ chuẩn hóa key cho lớp editor. Giữ cặp cache index/full ID khi engine lấy đội hình; không ghi tất cả index thành 0.

Đã kiểm tra trên record tổng hợp bằng lookup/decoder ARM64 gốc: đổi ô, đội trưởng và cả sáu người đá phạt theo ID; chỉ số vào đúng record; record index 0 và cầu thủ khác giữ nguyên. Hồ sơ đội hình DB được khôi phục vào runtime sau khi tài nguyên bị thay lại. Giữ xử lý không ép đổi kit khi chỉ sửa đội hình.

Trường hợp thêm một ID chưa có trong pool roster cache vẫn cần kiểm chứng riêng; native hiện có nhánh từ chối thay vì dùng key sai. Các bài kiểm tra này chưa thay thế màn hình đội hình/trận đấu trên máy.

## Single Player · AI

Mở nút **Single Player · AI** ngay trong launcher WebView. Chọn tên hoặc full ID, bật **Control one player when AI is on**, Save, đóng/mở lại ứng dụng rồi Enter Game. Nút AI xanh trong trận là công tắc AI native; lựa chọn cầu thủ và công tắc Single Player được lưu riêng.

Sửa tìm cầu thủ sở hữu: key trong đội hình có serial thực, trong khi module trước tra serial 0. Shim mới lấy key của đúng full ID trong 11 cầu thủ đang đá của đội được điều khiển rồi dùng lookup native. Không sửa roster, không chọn dự bị/đối thủ theo ID gần giống. Đã tái hiện serial 0 không tìm thấy và serial thực tìm đúng bằng code roster gốc; kiểm tra đổi ô, rời sân và collision full64. Cho nhập full ID hợp lệ cả khi catalogue chưa liệt kê.

Giữ nguyên `libsingle_player.so` SHA256 `2e1ef1970c5c48544992d7cfaa8c08e3e1c0e53a696eeb568aacf0f677c0a459`, gồm xử lý AI bật/tắt, pause/replay và khôi phục trạng thái. Không dùng bản 60e8a5. Shim chỉ tác động lookup gọi từ module này. Hiệu lực điều khiển trên điện thoại vẫn cần xác nhận.

## Ronaldo V8 → 89138556572074

Dùng mặt **và tóc V8** theo lựa chọn mới, namespace `RV08/HVR8`, bốn biến thể native. Nguồn là RAR V8 người dùng vừa gửi, không đánh đồng với ZIP Android2027 cũ bị thiếu.

FULL-7 có LOD0 cooked-out, MinLOD1 và skin LOD1 không dùng bone hàm/mắt. Bản này có LOD0 thật, MinLOD0, trọng số hàm/mí/nhãn cầu; giữ skeleton, thứ tự bone, parent và bind pose cơ thể native4522. LOD thấp dùng skin native4522 cùng RequiredBones153 gốc, không dồn toàn bộ bone mặt PC về head để qua kiểm tra. Cổ dưới được nội suy lên bề mặt/trọng số native; các điểm chung được đồng bộ trọng số. Môi trên không còn nhận cố định 50% ảnh hưởng của lip-volume vào hàm. Giữ eye socket offset; chỉ làm tối texel tối của khoang miệng trong đúng UV, không tô mặt/cổ để che hình học.

UEViewer độc lập đọc được cả hai LOD của cả bốn biến thể. Kiểm tra CPU cho thấy hàm/mí có chuyển động, cổ dưới không bị kéo bởi bone mặt, không có bone tay trong skin weights của face. Đây không phải kiểm tra va chạm đầy đủ hoặc xác nhận cổ/tay/mắt/miệng khi engine dựng trận/cutscene trên máy.

## Accessories và bandage

Giữ pack ba kiểu/180 texture pc9327, chọn riêng trái/phải. Đồng bộ cấu hình mở rộng/khôi phục DB và sửa đường danh tính mode2. Đã kiểm tra lựa chọn theo giải đến vector renderer native, trái bật/phải giữ nguyên, màu và cầu thủ khác; kiểm tra đầu vào loader native với mười loại phụ kiện. Không thay mesh cơ thể chỉ để thêm bandage, không gộp scope bandage với cắt tay áo và không sửa key sau hash.

**Chưa xác nhận pack bandage/phụ kiện đã xuất hiện đúng trong trận trên điện thoại.** Các bài test đầu vào loader/vector không chứng minh renderer và cache trên máy đã sử dụng tài nguyên đó.

## Cài và kiểm chứng

Chép toàn bộ `assets/` và `classes5.dex` vào APK73 V19.1 nền đúng, ký bằng khóa đang dùng. Giữ dữ liệu ứng dụng. Resource revision **19006**; manifest, inventory và checksum đã cập nhật; giữ kiểm tra toàn vẹn/readiness và CPK sửa đăng nhập gốc.

Giữ Spider V1 `106782819217056`, Miles `88035555413452`; không thêm hai Ronaldo Vol9 đã hủy. Không đóng gói save/DB cá nhân, log riêng hoặc RAR/ZIP nghiên cứu. Báo cáo `full8-*` nêu rõ phạm vi, fixture và `phone_verified:false`; các báo cáo FULL-7 cũ chỉ là lịch sử nền.
