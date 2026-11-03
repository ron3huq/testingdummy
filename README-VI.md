# FULL-8 RC2 HF1 · sửa lỗi cài đặt trong ảnh

Bản FULL tích lũy trên nền FULL-7/APK73, nối tiếp RC2 86b01343. **Dùng bản này thay RC2.**

Nguyên nhân đã tái hiện: trình đóng gói RC2 ghi 18 file __pycache__ vào hai manifest rồi xóa các file đó trước khi xuất gói. Launcher cố mở appearance_choices.cpython-312.pyc không tồn tại và chặn chuẩn bị game, Single Player và Transfer. HF1 bỏ các yêu cầu dành cho cache sinh tự động, vẫn giữ kiểm tra size/SHA256 cho toàn bộ166 tài nguyên runtime thật; không thêm file cache để né lỗi.

Không xóa save hoặc DB, không cần gỡ ứng dụng. Ghép toàn bộ assets/ và classes5.dex vào APK73 nền đúng, ký bằng khóa đang dùng. Sau cập nhật mở lại app; nếu còn thông báo cũ, dùng Check & Repair Resources. Đây là payload FULL, không phải APK đã ký.

Resource revision19008, manifest/inventory/checksum cập nhật. Native libraries, face/tóc, assets accessories, logic Transfer và Single Player giữ nguyên RC2. Bản này sửa lỗi cài đặt, không chứng minh các tính năng trong trận đã hoạt động trên điện thoại. Kiểm tra installer được chạy bằng Java với AssetManager thay thế trên máy chủ; không phải test điện thoại.

Chi tiết thay đổi RC2 và các giới hạn còn mở được giữ bên dưới (revision19007 trong phần lịch sử là bản trước).

---

# APK73 V19.1 FULL-8 RC2 · tiếp tục FULL-7

Gói FULL tích lũy mới, nền FULL-7 74a1cd81; nối tiếp RC1 1fb35a66. **Chưa xác nhận bản RC2 trên điện thoại.** Các kết quả dưới đây là kiểm tra mã, dữ liệu tổng hợp và thực thi ARM64/đọc tài nguyên độc lập; không phải cam kết mọi lỗi thực tế đã hết.

## Single Player

Launcher có Single Player; chỉ tìm cầu thủ sở hữu đang được xếp trong đội hình chính hiện chọn (bao gồm dự bị), dùng đúng full ID và serial. Không liệt kê toàn bộ catalogue hoặc cầu thủ ngoài đội.

Trong GameActivity có nút **1P** ở mép trên, cách phải 110dp: chạm để bật/tắt; nhấn giữ để chọn cầu thủ. Lần đầu chưa chọn sẽ mở danh sách. Không cần bật nút AI xanh. Cầu thủ phải đang trên sân để nhận điều khiển; không tự thay cầu thủ dự bị vào sân. Save ở launcher trước Enter Game, hoặc đổi trực tiếp bằng nút 1P trong trận.

Giữ slot hook tra cầu thủ đã khai báo trong RC1, bổ sung hai slot GamePlan và kiểm tra an toàn khi slot chưa tồn tại. Log 57 slot lịch sử không đủ chứng minh hook Single Player đã thiếu trên máy. Launcher thực tế đăng ký callback vòng đời để gắn nút trong GameActivity. Live API gọi native configure và lưu giao dịch, lỗi native sẽ rollback. Hooks cài sẵn ở trạng thái tắt để nhận công tắc trong trận. Module xuất phát từ bản 2e1ef197 đã sửa AI restore; chỉ bỏ một lệnh chặn fixed-player khi AI native tắt. Không dùng bản 60e8a5. Các nhánh pause/replay/transition/restore giữ nguyên; việc bật/tắt trên máy, đổi phía và qua trận mới vẫn cần kiểm chứng.

Đã nghiên cứu OnePlayerRouter và hai module trong PES.2021LordzGaming.apk trên releasee: picker thuộc đội/side/order, hook điều khiển riêng. Không chép engine hoặc thư viện PES2021 vào gói.

## Transfer

Sửa thêm hai accessor GamePlan cache trực tiếp: trước đó UI và DB đã sửa nhưng game đọc GamePlan gốc từ cached root. Bridge mới nối cache đó vào editor scoped, giữ nguyên bản GamePlan gốc dùng chung. Thực thi ARM64 engine gốc trên cache tổng hợp xác nhận thứ tự đội hình, vị trí và đội trưởng nhận đúng ID qua bản clone đã sửa. Giữ bridge phân biệt hai word key/pool từ RC1, giữ sửa không ép kit khi chỉ đổi đội hình.

Thêm **Skills & Boosters** trong menu cầu thủ Transfer, cạnh Abilities/Accessories/Celebration IDs: thêm/bỏ 74 skill, ba ô booster có Off, cùng danh mục/giới hạn Player Editor. Lưu vào hồ sơ Transfer theo cầu thủ/giải, mở lại lấy overlay thực; skills đi qua native parameter flags, boosters ghi ba trường native144/145/146 vào đúng record. Ra khỏi scope giải sẽ phục hồi booster gốc. Booster có điều kiện vẫn cần điều kiện trong game. Kiểm tra lưu/mở lại/xóa và native ghi/khôi phục đã qua trên dữ liệu tổng hợp.

**Giới hạn còn lại:** thêm một ID hoàn toàn chưa tồn tại trong pool roster cache vẫn có nhánh native từ chối; chưa chứng minh sửa trường hợp này. GamePlan thật, mọi vai trò/thay người và hiệu lực chỉ số trong My League trên điện thoại chưa được xác nhận bởi bản RC2.

## Ronaldo V8 → 89138556572074

Giữ mặt và tóc V8 theo lựa chọn mới, namespace RV8B/HV8B, bốn container mới pc9332..9335. Tách mắt/răng/khoang miệng sang material native4522 riêng, UV native; lớp bake da ở slot0 không còn ghi đè material mắt/răng. LOD thấp giữ UV/da native4522, sửa cả LODMaterialMap. Da V8 trỏ đúng material riêng thay vì HQR7 kế thừa.

Tóc PC dùng UV0 cho alpha, UV1 cho màu; converter cũ lấy nhầm bản đồ alpha như màu. Bản này bake cả hai vào atlas native, giữ nguyên vị trí/normal/tam giác tóc, tách vertex ở UV seam cho từng tam giác sợi tóc. Không thay mesh cơ thể để sửa face.

UEViewer đọc/xuất được cả hai LOD của bốn biến thể; xác nhận material/texture4522 và V8 thực được nạp. MinLOD0, LOD0 có dữ liệu thật, mắt/hàm dùng bone riêng, không gom về head. Hierarchy/bind pose cơ thể byte-exact native4522; weight lane trùng được cộng, tổng255; face không dùng bone tay. Đây chưa chứng minh không xuyên môi/cổ ở mọi animation, hoặc hình mắt/tóc cuối cùng trên điện thoại. Không cam kết tuyệt đối từ kiểm tra offline.

## Accessories và cài gói

Giữ đường accessories/bandage đang được người dùng xác nhận hoạt động, không thay tài nguyên pc9327 hoặc gộp scope với cắt tay áo. Giữ Spider V1 106782819217056, Miles88035555413452; không thêm Ronaldo Vol9 đã hủy.

Chép toàn bộ assets/ và classes5.dex vào APK73 V19.1 nền đúng rồi ký bằng khóa đang dùng. Giữ dữ liệu ứng dụng; không xóa save. Đây là gói FULL tài nguyên/runtime để ghép APK73, không phải APK đã ký. Resource revision19007; checksum/manifests cập nhật, giữ nguyên CPK sửa đăng nhập và kiểm tra toàn vẹn. Không chứa save/DB người dùng, diagnostics riêng hoặc RAR/ZIP/APK nghiên cứu.

Các validation/source từ FULL-7 và RC1 là lịch sử. Báo cáo lần này có tiền tố full8-rc2; mỗi báo cáo nêu phạm vi thực thi và phone_verified:false.
