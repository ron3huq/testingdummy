# Nghiên cứu: nhịp trận đấu, phong độ, bandage và điều khiển một người

## Nhịp chơi trên Samsung A56

Thông tin người dùng: A56 Android; Player Max, Stadium Medium, chọn FPS120; không cắm sạc; giảm sáng xuống thấp nhất và chơi2–5giờ sáng cảm thấy chạy/xoay người/dính bóng nhanh, mượt hơn. Hiện tượng có cả ở eFootball chính thức.

Đây là nhịp thao tác/chuyển động, không phải số phút hay đồng hồ trận đấu. Chưa có phép đo trên điện thoại để xác định nguyên nhân. Các khả năng cần tách: độ ổn định từng khung hình, trễ cảm ứng, nhiệt/giới hạn điện năng/GameBooster, phong độ/thể lực/đối thủ và mạng ở trận online. Màn hình120Hz và mục tiêuFPS120 không chứng minh game duy trì120khung hình/giây. FPS trung bình giống nhau cũng có thể có độ giật từng khung rất khác.

Không tìm thấy quy tắc giờ thực2–5sáng hoặc độ sáng màn hình trong các đường MyLeague/condition đã kiểm tra của bản mod. Điều này không chứng minh toàn bộ engine không có ảnh hưởng gián tiếp. Không thêm điều chỉnh tốc độ vật lý hoặc hệ số thời gian dựa trên cảm giác chưa đo.

Phép đối chiếu cần giữ cùng cầu thủ, mũi tên phong độ, thể lực, đội hình, camera, sân, đối thủ, độ khó và chế độ offline. Ban ngày đổi sáng thấp/cao trong cùng điều kiện rồi so với ban đêm; giữ GameBooster/chế độ tiết kiệm pin cố định, ghi nhiệt và làm nóng máy tương đương. Đo thời gian thực chạy một đoạn sân cố định, độ trễ từ chạm chuyền đến bóng rời chân, thời gian bóng đi một quãng cố định và độ đều khung hình. Lặp lại để tách biến thiên AI; không dùng số phút trận làm thước đo duy nhất. Quay màn hình có thể tự làm tăng tải nên phải giữ cách đo nhất quán.

## Phong độ MyLeague

Runtime gốc editor_condition có ba hook riêng cho truy vấn/màn thông tin/trận đấu tại82b80f0,330b158,82c11b4; bảnmod giữ các hook sẵn có. Chọn0=E,1=D,2=C,3=B,4=A;-1 là game tự chọn. Cấu hình này độc lập với các chỉ số147tham số và quy tắc giảm OVR cho NPC. Không suy ra một hệ số tăng tốc cố định hay phần trăm tăng chỉ số khi chưa đo engine thực.

Mô phỏng CPU còn có một khái niệm form khác: trọng số ghi bàn/kiến tạo thay đổi ổn định theo từng nhóm4lượt, hệ số0.65–1.4. Đây là xác suất phân bổ sự kiện trong các trận máy tự mô phỏng; không phải mũi tên phong độ trong trận, cũng không phải hệ số tốc độ chạy hoặc xử lý bóng của đội người dùng. Không dùng giờ thực hay độ sáng làm đầu vào.

BảnFULL5 đã sửa cả native lẫn hai wrapperSTART_GAME để đội hình chính/dự bị người dùng không bị quy tắc cân bằng NPC kéo chỉ số xuống. Chỉnh thông số cụ thể do người dùng chọn vẫn được áp dụng. Diagnostics bổ sung trạng thái form của tiến trình hiện tại và báo cáo mục tiêuFPS có sẵn; ghi rõ đó không phải FPS render đo được. PID của launcher sau khi đóng game không phải PID của trận trước.

## MEGA BANDAGE PACK FWC2026 FL26V7AIO

Đã tải đúng asset ở releasee; SHA2567636a10f7c6b3f74c7595847d9aa473e85478715ac962c78f5f8cce1d7e82399. Archive1079entry,200SiderID,199arm_bsm và103thigh_bsm,326FTEX. Đã giải mã mẫu arm/thigh2048×2048. Đây chủ yếu là texture body PC theo từng cầu thủ, có cả hình xăm và màu da; không phải bộmesh bandage mobile độc lập. MobileT_Sk1_Skin_D512×256 dùng atlas tay/chân khác;T_Base_Body_D còn có phần kit.

Chép thẳng texture sẽ tô nhầm da/quần/áo và ảnh hưởng hình xăm. Chưa nhập gói này vào menu vì chưa có UVtransfer và vòng đời material riêng từng cầu thủ được chứng minh trên máy. Cần tách mặt nạ bandage khỏi da/hình xăm, đối chiếu UV/cơ thể PC và mobile, dựng assetmobile riêng, kiểm tra skinning/chuyểnLOD và cô lập material. Các wrist/ankle tape sẵn có vẫn là phụ kiện native; không đổi nhãn thành bandagepack để giả như đã chuyển đổi.

## Điều khiển đúng một cầu thủ khi AI bật

CameraPlayer và quyền điều khiển một cầu thủ là hai phần khác nhau. Camera runtime hiện có trục/type/reset; không có APIchọnplayerID và chuyển inputownership đã xác minh. Có enumEPesCameraType::Player nhưng nó không chứng minh điều khiển hỗn hợp AI/người. ThunkOnPressedAutoPlayButton4035574 gọi base33c74c0(RET); logic thực có thể nằm ởBlueprint/gameplay khác. Hook vào nút đó không đủ để bảo đảm chuyển quyền.

Chưa bật chức năng giả trong menu và không cài hookđịa chỉ đoán. Thiết kế cần kiểm chứng: AIoff→chế độ điều khiển gốc; AIon+lockon→duy nhấtIDđãchọn nhận inputngười, các cầu thủ còn lại AI; tắtlock→trả lạiAIgốc; tắtAI→nhảlocktrước rồi game điều khiển bình thường. Cầu thủ ra sân/chấn thương/đổi trận phải nhảownership, không tự chiếm cầu thủ khác. Cần trace controller/possession/input thực trong trận trên máy để triển khai và kiểm tra bật/tắtAI, pause, replay, thay người, đổi camera. Phần này chưa hoàn tất triển khai.

## Bổ sung FULL6

Đã đối chiếu trực tiếp mesh4522 vàSK_Base_Face gốc: RefSkeleton166 xương, nhưng danh sách RequiredBones là166 ởLOD0 và153 ởLOD1. LOD1 bỏ các mục8–20 trước vai/tay; ví dụ xương upperarm_l73 ở vị trí60 trong pose compact gốc, còn danh sách166 đặt nó ở73. Các face nhập đã dùng danh sách166 ởLOD1. FULL6 sửa5 profile đang xử lý về đúng danh sách từngLOD, remap trọng số bị loại và xác minh bằng trình đọc độc lập cho cả4 biến thể. Đây là sửa cấu trúc payload; việc hết kéo tay trong trận vẫn cần kiểm tra trên máy.

Hai Spider có đúng tài nguyên từ trước nhưng thiếu2ID trong điều kiện cho phép redirect face ngoài4522. Đã tái hiện bằng thư viện cũ và chạy lại160 trường hợp qua hàmARM64 đã biên dịch sau sửa. Không đổiFaceID/ID cầu thủ để ép nhận face.

Tiếp tục xem đường camera/AI: đăng kýOnPressedAutoPlayButton thứ hai tại4035b34 là hàm tạo/đăng kýUFunction, không phải setter nhận input của cầu thủ. Nhánh dùng chuỗiSwitch_PlayerID tại2fbfcd4 dựngFName và đi vào đườngUI; chưa tìm thấy ở đó thao tác gán quyền điều khiển. Vì thế chưa có căn cứ an toàn để coi hai tên này là hàm khóa cầu thủ. Không triển khai chế độ điều khiển hỗn hợp chỉ dựa trên tênenum/chuỗiUI.
