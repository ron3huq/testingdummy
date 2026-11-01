# V19.1 FULL-5.1 · Login + Joker
Bản này sửa lỗi đăng nhập C_NAJM_0009 được xác định từ Runtime Diagnostics: `unexpected noodle bundle identity`. Danh sách39ID đã được bổ sung trong metadataFULL5 nhưng bộ kiểm tra vẫn dùng danh sách36ID cũ. Runtime hiện dùng cùng một hằng ID cho kiểm tra và báo cáo; giữ các kiểm tra checksum/khởi tạo, không bật fallback gốc để che lỗi.

JokerV3 từ `JOKER-V3-105804908843755-ANDROID.zip` thay faceJoker hiện tại ở **106781476920663** (NJK3). Giữ geometry/UV/weights/skeleton/texture từ ZIP, chỉ đổi namespace và liên kết tài nguyên. Không đổi đích sangIDtrong tênfile, không chép .so/runtime đi kèm. Raiden/Ronaldo2017 và các facekhác giữ nguyên. Tài liệu diagnostics người dùng không nằm trong gói.

Gói tích lũy, không cần áp FULL5 rồi mới áp bản này. Cài theo hướng dẫn dưới. Đã tái hiện lỗi bộ kiểm tra ở bản cũ, xác nhận workerbản mới đi qua xác minh payload tới chờengine trên luồngARM64 giả lập điều kiện nền, kiểm tra5ca sửa sai bị từ chối; chưa xác nhận đăng nhập trực tiếp trên điện thoại.

Gói tích lũy dùng cho APK73efootballV19.1 gốc SHA256`9c0b249557eeab1543ce143af4d08269b6e9a5a965472242815dba5712c76469`. Giữ bản sửa loading đã được người dùng xác nhận của FULL-3. Không cần cài từng FULL cũ trước. Không áp vào APKV16/V20.2.

## Cài bằng MT Manager

1. Export Save để có bản sao lưu. Giữ dữ liệu ứng dụng/tài nguyên đang có.
2. Mở APKV19.1; trong ZIPGitHub mở thư mục bọc ngoài, chép `assets/` và `classes5.dex` vào gốc APK, thay tệp trùng.
3. Ký cùng khóa đang dùng rồi cài cập nhật. Không gỡ ứng dụng/xóa dữ liệu. Không chép README/validation/inventory vào APK.
4. Đóng game trước khi chỉnh. Lưu, đóng/mở ứng dụng rồi Enter Game để tạo các cấu hình native mới.

## Face đã tích hợp

| Thẻ | Face áp vào tài nguyên hiện tại |
|---|---|
|106782819217056|Spider-Man V1 từ spidermancurrently.zip|
|88035555413452|Miles Morales từ spiderman-milesmorales.zip|
|89138556572074|Ronaldo từ RONALDO-TOC-DEN-88045487528683-MAT-V3-ANDROID.zip|
|88039045074440|Mullet A: chỉ tóc56322; khuôn mặt/UV/weights giữ nguyên, sửa lớp da sau cổ|
|88042803047215|Ronaldo2017/Noodle/Honda: miệng/lưỡi tối và bớt đỏ/hồng|
|105568954067359|Raiden: maskPBR kim loại phản chiếu môi trường, roughness thấp|
|106781476920663|JokerV3 từ ZIP Android mới|
|105756321970183|WukongV4: dày thêm tóc trên/sau đầu, giữ đường bao/ngọn và vùng râu quanh mặt; nâu xám olive trầm|

Hai bản RonaldoVol9 đã hủy, không có trong gói và không gán bản vàng cho88036092284395. Ba ZIP mới chỉ lấy tài nguyên face, không chép thư viện/runtime cũ đi kèm. Thay face không sao chép thẻ/chỉ số/định danh cầu thủ. Raiden dùng phản chiếu môi trường của shader native; không phải camera phản chiếu phẳng realtime mới. Ảnh/Blender minh họa tách riêng khỏi gói APK.

## MyLeague và Transfer

- Đội hình chính và dự bị người dùng được bảo vệ khỏi giảmOVR ở cả7giải; sửa cả hooknative và hai đườngSTART_GAME.
- Thư viện Transfer cũ đã bị lệch với source. Bản xây dựng đúng giữ pool cầu thủ ổn định, táchGamePlan, đúng mộtGK, captain/6vai trò đá phạt/số áo bámID khi đổi chỗ.
- Trong Transfer chọn thành viên rồi **Abilities · Celebrations · Accessories** để chỉnh chỉ số, IDăn mừng và10loại phụ kiện native/tay áo. Áp đúngfullID trong giải đang chọn; không cần sở hữu thẻ NPC. Lưu bảnnháp đội trước khi chỉnh cầu thủ. Các ô chỉ số trống giữ giá trị hiện tại; không hiển thị một chỉ số gốc đoán khi chưa có bản chụp native.
- Y17/Y08: sửa kiến tạo bị giới hạn bằng0từ bảnglegacy, dùng lại trọng số ưu tiên ghi bàn/kiến tạo, gắn kiến tạo với từng bànCPU, loạiGK và tự kiến tạo. Không mô phỏng lại trận người dùng đang đá. Bảng là tối đa20người có thống kê thật; lượt đầu có thể ít hơn20. Bản vá không ghi lại kết quả/trận đã chơi hay bịa kiến tạo để lấp bảng cũ. LượtCPU mới dùng đường đã sửa.

## Giao diện và chỉnh cầu thủ

Giữ các sửa chân thuận/WeakFoot/names/cart của FULL4-FOOTFIX. Sửa màu phụ kiện: chọnOriginal xóa màu tùy chỉnh, chỉnh riêng từng tab không xóa lựa chọn khác. Accessories được gom nhóm và mở từng mục. Tra cứu nhãn được lập chỉ mục, dựng danh sách bằngfragment, gộp tìm kiếm nhanh thành yêu cầu đang chạy+cái mới nhất, xóa observerportrait khi rời danh sách, giới hạn tải ảnh đồng thời. Benchmark chỉ đo từng phần, không phải cam kết mọi thao tác nhanh106lần.

## Kiểm tra và giới hạn

Đã kiểm tra bằng gatewaythật trên DBthử tách riêng; hàmARM64 gốc; trình đọcmesh/material độc lập; Chromium. Có105caowned×league,128tổhợpfoottraits,68ca biên ability/motion,4giảiTransfer/13vị trí,12biến thể ba face mới và12biến thểMullet/NR17/Raiden,4Wukong×2LOD;525lớpDEX không có liên kết thiếu. CPK tại cả3đường giữ SHA6fa4b9050f0a125e9ee295a7260ca3f1b5f718cdca6d5af94e2cc697d215fc4a. Không có savecá nhân hay DBthử trong gói.

Chưa xác nhận bảnFULL5 trên điện thoại; phản chiếuGPU, hiển thị wristtape và tải các face nặng còn cần đối chiếu trên máy. Không cam kết100%khôngcrash/khônglag chỉ từ kiểm tra máy phát triển.

**Hai yêu cầu chưa hoàn tất triển khai:** chuyển bandagepackPC thành phụ kiệnmobile và chế độ người điều khiển duy nhất một cầu thủ khiAIbật. Không thêm nút bật giả/hookđoán vào game. Xem `RESEARCH-VI.md` về dữ liệu đã kiểm tra, khác biệtUV/bodytexture, inputownership/camera, cùng nghiên cứu nhịp trận/phong độ trênA56. Đây là giới hạn thực của gói hiện tại, không đánh dấu hai phần này là hoàn thành.
