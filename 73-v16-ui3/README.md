# 73 V16 — UI3 Slim Cuffs + Y08 Champion League

[Tải ZIP MT Manager](https://raw.githubusercontent.com/ron3huq/testingdummy/chat-downloads/73-v16-ui3/V25-73-UI3-Slim-Cuffs-Y08-MT.zip)

Dành cho APK73 V16 đang chạy faceV25/UI1/UI2. Gói cập nhật giữ face, My League cũ, kits và các sửa lỗi UI2; không chứa save cá nhân.

## Cài bằng MT Manager

1. Xuất bản sao save và giữ APK đang hoạt động.
2. Mở APK đang dùng. Chép `classes5.dex` và **gộp toàn bộ `assets`** từ ZIP vào gốc APK; thêm tệp mới, ghi đè tệp trùng và giữ những assets khác.
3. Ký bằng **đúng khóa MT đã dùng cho bản đang cài**, rồi **cài đè**. Không gỡ game, không xóa dữ liệu và không gỡ resource app. Nếu báo xung đột chữ ký, chọn lại đúng khóa.
4. Đóng hẳn app và mở lại. Không cần tải lại resourceAPK lớn. Lần vào đầu, game có thể nhập lại container tay áo43MB đã đổi nội dung từ chính APK cục bộ.
5. Để nhận lịch Y08 gồm10 đội, **bắt đầu mùa My League mới của Y08**. Gói không sửa lịch/kết quả đã lưu của mùa Swiss12 đội đang chơi. Không cần xóa save toàn game.

## Áo Ronaldo

UI2 kéo dài ống tay ngắn nên giữ độ rộng của áo tay ngắn. UI3 dùng biên dạng áo dài tay gốc để thu nhỏ cả ống, bỏ độ phồng12%, chỉ để mép gập nhỏ và hạ mép áo khoảng3,4cm dọc cẳng tay ở mẫu015.

Giữ nguyên phạm vi: chỉ Ronaldo2017 `88044950524330`, Ronaldo2006 `89135066911146`, hai thẻ `89136418985303`/`89136418985302`, trên kits RM2017/Sparta351 và MU2008/Telstar352 ở slot0/1. Cầu thủ khác, kits khác và slot khác vẫn dùng đường nạp gốc. Băng trắng cổ tay trái của bốn thẻ được giữ.

Mesh riêng `pc9299`:356 biến thể, hai LOD mỗi biến thể. Giữ nguyên UV, chỉ mục, skeleton/bind pose; sửa hình dáng/trọng số phần áo và thu phần da **bị che hoàn toàn dưới áo** vào trong để tránh xuyên bề mặt. Da cẳng tay/cổ tay đang lộ, thân, cổ và mặt không đổi. Các biến thể không hỗ trợ giữ mesh native.

## Card Designer

- Nền video không còn tự vẽ lại cả editor30lần/giây. Preview động mặc định tắt; nút bật/tắt vẫn dùng được, video chạy qua lớp hiển thị của trình duyệt.
- Gộp các yêu cầu render/resize trong cùng một khung hình; không cấp lại canvas khi kích thước giữ nguyên.
- Chuỗi không có tiếng Trung bỏ qua regex dịch; tìm template được debounce120ms.
- Giữ thao tác sửa ảnh, chọn template, lưu và xuất. Kiểm tra Chromium với màn hình điện thoại, cả có/không bridge Android giả lập: khởi tạo/lưu/chuyển tab qua; khi không thao tác không có vòng vẽ liên tục;100 yêu cầu render được gộp.

## Y08 Champion League

Thay Swiss473 bằng10 đội theo đúng ánh xạ đã yêu cầu; bỏ Servette1958/Lugano4965 khỏi thành viên/lịch mới. Sao chép tên, logo và đường nạp áo đấu từ đúng CLB gốc.

- Top1: MU, Real Madrid, AC Milan, Barcelona.
- Top2: Arsenal, Chelsea, Inter, Juventus, Liverpool, Bayern.
-110 thẻ khác nhau; đối chiếu429 đội/13.003 ID ở các giải My League khác: **không trùng thẻ**. Hai Cannavaro, hai Ibrahimović, hai Vieira… dùng phiên bản ID khác nhau.
- Rooney `88037702766648`, Ronaldo2006 `89135066911146`; R9 dùng `88046292734664` theo xác nhận của bạn. Giữ Messi `89136409091415`, Ronaldinho `89067152870864`, Zidane `89136418985301`, Henry `88046312750111`, Adriano `89066884435465`.
- Đội hình có11 người/đội, vị trí và tọa độ riêng; số áo, đội trưởng và sáu vai trò đá phạt/phạt góc/penalty được áp dụng trong native, gồm cả đội hình cache của hai phía.
- OVR93–98 theo từng cầu thủ, chỉ trong Y08; trở về dữ liệu gốc khi rời phạm vi473. Milan được tăng chỉ số phòng thủ và có phân phối tỷ số CPU thiên về ít thủng lưới. R9/Messi là người nhận trọng số bàn thắng cao nhất ở CLB của họ. Kết quả thực tế và bảng vua phá lưới phụ thuộc trận đã chơi, không bị viết lại để ép kết quả.
- Dùng mô hình phân cấp hiện tại của Premier/Uefa. Lịch hai lượt:18 vòng, mỗi vòng5 trận.

[Đội hình, ID, vị trí, số áo, OVR và mọi trường hợp thay thế](ROSTERS.md).

Một số cầu thủ không có trong dữ liệu73: ưu tiên người cùng CLB thời2000s; chỉ vị trí còn thiếu mới dùng người cùng CLB thời2010s, theo xác nhận của bạn. Gerd Müller được giữ theo yêu cầu dù thuộc thời kỳ cũ hơn. Đội hình nhiều thời kỳ có xung đột số áo: Messi dùng số19 trước2008, Ronaldinho10; Adriano dùng29 thời đầu Inter, Sneijder10; Real giữ Zidane5/Carlos3, Cannavaro dùng13 tuyểnItaly và Pepe2 tuyểnPortugal. Các ngoại lệ được ghi rõ thay vì gán tên giả lên cầu thủ khác.

## Kiểm tra và giới hạn

- ARM64/Unicorn:28 roster,22 đội hình classic, các getter role/tọa độ/số áo gốc; phạm vi110 thẻ Y08 và OVR; khôi phục dữ liệu khi thoát phạm vi; logo/kit tailcall giữ con trỏ FString; menu Swiss12→10; hook tay áo/cổ tay và face không trùng nhau.
- API73 gốc: bảy giải, state/info, lịch18 vòng và scorer; save/kết quả cũ không bị ghi lại.
-36.000 trận CPU kiểm tra: top1 thắng top2 khoảng53,9%; Milan thủng lưới trung bình0,425 so với0,985 của các đội còn lại; đây là mẫu mô phỏng, không phải kết quả cố định.
- Đọc lại bốn mẫu mesh bằng UE Viewer; đối chiếu UV/skeleton/bind matrices và kích thước tay áo. DEX037 hợp lệ, giữ271 lớp, không có Body & motion.
- Toàn bộ manifest của APK nền+ZIP và các SHA256 được kiểm tra; face library/runtime/container `pc9298` giữ nguyên từng byte.

**Chưa chạy trực tiếp trên điện thoại/GPU của bạn.** Kiểm tra mã và mesh không thay cho kiểm tra render/chuyển động trong trận; không khẳng định100% trên mọi thiết bị.

Mã và phép thử trong `source/`; kết quả kiểm tra trong `validation/`. `SHA256SUMS.txt` và `inventory.json` dùng đối chiếu gói tải về. Không có yêu cầu root hoặc USB.
