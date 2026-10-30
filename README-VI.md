# UI7.19 FULL · Private Football · Một ZIP, không Part3

Chỉ dành cho 73 V16 versionCode311010108. Giữ toàn bộ payload/tính năng tích lũy của UI7.18 ngoài Part3/pc9308. Không dùng cho efootxi.

## Cài cập nhật

Mở thư mục bọc `testingdummy-<commit>/` trong ZIP tải từ GitHub. Chép **assets/** và **classes5.dex** vào gốc APK, thay thế rồi ký một lần. Dùng cùng khóa ký để cài cập nhật và giữ save. Không áp chồng thêm UI/Part cũ; không cần gỡ game hoặc xóa dữ liệu. **extras/** là file Blender cho máy tính, không chép vào APK. Lần đầu vào game cần để bộ tài nguyên ảnh mới được cập nhật.

## Sửa ảnh và lỗi có thể gây văng khi mở đội hình

UI7.18 có lỗi cụ thể đã tái hiện: ảnh mini khai báo BGRA128×128 nhưng bảy mip phía dưới còn dữ liệu ETC2, sai kích thước bộ nhớ của BGRA. Ví dụ mip64×64 chỉ có4096byte thay vì16384byte. Game thu nhỏ/stream ảnh thẻ có thể đọc sai dữ liệu, gây sọc và có thể gây lỗi native. UI7.19 dựng lại đầy đủ tám mip128→1, đúng kích thước/màu/alpha, dùng lọc có trọng số alpha để tránh viền đen. Template cũng được làm sạch. Toàn bộ44texture ảnh đi kèm đã được đọc lại độc lập và kiểm tra từng mip.

Một lỗi khác là nhận nhầm asset có ID trong tên: `0501_f01_<ID>_` là nền, `f09` chứa chữ sự kiện, `m01` là nền mini; chúng không phải ảnh người. UI7.18 đã thay nhầm những lớp này bằng chân dung, khiến ảnh chồng lên nhau và che nền. Bản này chỉ thay asset chân dung riêng, giữ nền/chữ. Mảng native `m_front` dùng ảnh lớn184×256; `m_mini` dùng miniface128×128; mặt sau giữ nguyên. Copy Background chỉ ghép đúng lớp nền/khung tương ứng, không lấy ảnh người hoặc chữ sự kiện của donor.

Ảnh nhập được giữ thành hai crop độc lập, không kéo giãn. Đã thử bấm Mini/Large, zoom khác nhau và lưu trong Chromium, rồi gửi đúng PNG đó qua gateway thật, đối chiếu từng pixel của crop và PNG Editor. Ảnh mini mặc định của Ronaldo2017 **88042803047215** được phóng từ chiều cao đầu78 lên88px, giữ tỉ lệ nguồn. Crop custom của người dùng vẫn có ưu tiên.

Bộ ảnh đi kèm pc9323 được dựng lại; tăng revision tài nguyên để yêu cầu cập nhật. Ảnh custom đã lưu được dựng sang schema19 từ chính crop SQLite cũ. Không sửa đè đường generation tải cũ, không xóa save. Giữ PAK chuẩn365byte, SHA/AES, GET/HEAD/range và integrity. Không tắt kiểm tra để né Live Update.

## Tối ưu và làm gọn giao diện

Ảnh Editor được giải mã trên tối đa hai worker, queue48, cache8MiB, gộp yêu cầu trùng theo ID/revision và kiểm tra tag trước khi gán ảnh, tránh gán nhầm khi cuộn. Ảnh custom có PNG nhỏ được tạo lúc import hoặc nâng cấp, sau đó đọc trực tiếp; ảnh11thẻ đi kèm có PNG trong assets. Không chuyển Base64 qua Python cho từng lần hiện ảnh thông thường. Cache có revision riêng nên ảnh mới đồng bộ trong danh sách và chi tiết.

Bỏ việc giải mã ảnh nền sân vận động/khung trang trí nặng trên luồng UI của Editor; dùng panel nhẹ sẵn có. Giữ Earth tĩnh. Bỏ phần liên hệ Telegram, callback mở link và giới thiệu gốc trên launcher; đổi tiêu đề giao diện thành Private Football. Không đổi package, quyền truy cập save hay đường dữ liệu game.

## Yan Diomande và chẩn đoán

Đặt Yan về **palette5/6, màu áp chót**. Áp dụng sáu ID alias native đã xác minh của cùng cầu thủ:176104,84062184,105863243280360,105877118037992,52904065150952,56164297650152. Nâng cấp một lần có backup phần appearance cũ, chỉ sửa skin của Yan, giữ cầu thủ khác và lựa chọn người dùng thay đổi sau đó. Giữ face Diomande hiện có.

Runtime Diagnostics thêm lịch sử thoát của chính ứng dụng do Android lưu, nếu phiên bản Android hỗ trợ; có reason/status và trace khi hệ thống cho phép đọc. Chỉ đọc khi bấm Diagnostics, không cài signal handler và không chạy trong trận. Nếu vẫn văng, mở lại ứng dụng và Copy Diagnostics để có dấu vết lần thoát, thay vì chỉ trạng thái WAITING_FOR_LIBUE4 của lần mở mới. Một số tên file diagnostics giữ tên cũ để tương thích.

## Kiểm chứng và giới hạn

Báo cáo validation gồm native ARM64 layer routing bằng tên asset thật, đầy đủ mip/BulkData, đọc IoStore độc lập, UEViewer xuất PNG đối chiếu pixel, browser crop, gateway import→login, nâng cấp giữ crop, Editor đồng bộ, cache/integrity, GamePlan/captain và palette. Báo cáo phần không đổi ghi rõ baseline; kiểm thử cấu trúc DEX không phải đo tốc độ điện thoại.

**Chưa thử trên Android/GPU.** Lỗi dữ liệu mip và nhận nhầm lớp ảnh đã được sửa và kiểm thử trên máy build; chưa có crash trace từ thiết bị để khẳng định đó là nguyên nhân duy nhất của lần văng. Cần thử mở đội hình trên máy bạn để xác nhận. Không cam kết100% không crash/không lag khi chưa thử thiết bị.

Giữ Transfer bốn giải, Accessories10type/màu, skills/cart, level100, skin native, copy model/motion, tám trường animation và các face cũ; giữ file Blender NQ27 đã ghép trong extras. SOUND đổi riêng từng thẻ vẫn chưa triển khai; animation độc nhất khóa theo danh tính chưa được chứng minh chuyển riêng bằng tám trường motion.
