> **Ronaldo v4 — mesh PC đầy đủ và thử sửa biến dạng replay:** [Tải bản thử](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/ronaldo-pc-mesh-v4/Ronaldo-PC-mesh-v4-cutscene-trial-88044950524330.zip) · [Tắt đầu thử](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/ronaldo-pc-mesh-v4/Tat-dau-thu-Ronaldo.zip) · [Hướng dẫn/giới hạn](efootxi-1.3.2/ronaldo-pc-mesh-v4/HUONG_DAN.md). Chỉ Card ID 88044950524330; chưa xác nhận sửa lỗi replay trên điện thoại.

> **Ronaldo PC face v3 — chuyển thử mặt từ 4522.cpk, giữ facial profile gốc:** [Tải gói thử](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/ronaldo-pc-face-v3/Ronaldo-PC-face-v3-88044950524330.zip) · [Hướng dẫn và kiểm tra biểu cảm](efootxi-1.3.2/ronaldo-pc-face-v3/HUONG_DAN.md). Mặt PC được thích nghi sang topology mobile; mắt/miệng v3 chưa xác nhận trên điện thoại.

> **Ronaldo v2 — màu tóc vàng theo nguồn PC, atlas chi tiết hơn và chỉnh nhẹ má/cằm:** [Tải bản thử](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/ronaldo-noodle-v2-color-face/Ronaldo-noodle-v2-color-face-88044950524330.zip) · [Quay lại v1b](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/ronaldo-noodle-v2-color-face/Quay-lai-Ronaldo-v1b.zip) · [Hướng dẫn và giới hạn](efootxi-1.3.2/ronaldo-noodle-v2-color-face/HUONG_DAN.md). V1b đã được người dùng xác nhận tải được đầu; v2 chưa thử trên điện thoại.

> **Ronaldo vào game được nhưng tóc chưa đổi, log `name struct is not defined`:** [Bản vá hook v1b](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/ronaldo-noodle-hook-fix-v1b/Ronaldo-noodle-v1b-sua-hook.zip) · [Hướng dẫn](efootxi-1.3.2/ronaldo-noodle-hook-fix-v1b/HUONG_DAN.md). Chỉ thẻ 88044950524330; chưa xác nhận renderer trên điện thoại.

> **Sửa lỗi khởi động gói tóc Ronaldo v1:** [Tải gói khôi phục](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/ronaldo-noodle-startup-fix/Khoi-phuc-khoi-dong.zip) · [Bản thử v1a đã sửa đóng gói](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/ronaldo-noodle-startup-fix/Ronaldo-noodle-trial-v1a-startup-fixed.zip) · [Hướng dẫn](efootxi-1.3.2/ronaldo-noodle-startup-fix/HUONG_DAN.md). Không xóa dữ liệu ứng dụng. Chưa xác nhận trên điện thoại.

# File trao đổi cùng Codex

Nhánh `chat-downloads` lưu file từ cuộc trò chuyện, độc lập với nhánh mã nguồn.

## Dừng dùng cả hai bản thử dt200

Người dùng xác nhận bản đầu và CRCFIX đều gây màn hình đen. Sửa checksum chỉ khắc phục một lỗi cấu trúc đã tìm được; chưa giải quyết lỗi khởi động. **Không cài lại hai bản dt200 thử.** Khôi phục dt200 gốc để dùng game đang hoạt động.

- [dt200 gốc để khôi phục](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/restore/dt200_mobile_all.cpk)
- [Hướng dẫn khôi phục](efootxi-1.3.2/KHOI_PHUC.md)

## Ronaldo tóc mì tôm — bản thử Android v1, chỉ Card ID 88044950524330

Đã tạo7 package Unreal riêng:4 biến thể đầu Android giữ phần mặt/skeleton gốc, hai material tóc và texture alpha ETC2. Có container pc9298 và hook giới hạn full Card ID; không thay dt200, save hoặc cấu hình đội hình. **Chưa chạy trên điện thoại; đây là bản thử, không phải xác nhận tóc đã hiển thị đúng trong game.** Tóc dùng màu tối, chưa tái tạo lớp màu thứ hai/hiệu ứng ngọn tóc của mod PC.

- [Tải bộ thử cho MT Manager (~0,7MB)](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/ronaldo-noodle-trial-v1/Ronaldo-noodle-trial-v1-88044950524330.zip)
- [Tải file tắt tóc thử, buộc dừng/mở lại game sau khi chép](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/ronaldo-noodle-trial-v1/Tat-noodle-hair.zip)
- [Hướng dẫn cài, đọc log và quay lại mặt cũ](efootxi-1.3.2/ronaldo-noodle-trial-v1/HUONG_DAN.md)
- [Bằng chứng và giới hạn kiểm tra](efootxi-1.3.2/ronaldo-noodle-trial-v1/NGHIEN_CUU.md)

Giải nén bộ thử, gộp work/ và livedata/ vào files/embedded-gateway/. Sao lưu gateway_runtime.py trước. Bộ ZIP không chứa myleague_editor.json hoặc libselect_team.so. Xem noodle-hair-status.json tại work/tools sau khi vào sân với đúng thẻ. Hook có nhánh gọi lại loader gốc khi callback tải mới trả null; nhánh này đã kiểm tra ARM64 với loader mô hình hóa, chưa kiểm tra I/O/renderer/GC thật của Android.

Đã kiểm tra UEViewer đọc4 mesh/material/texture mới, so sánh mọi thuộc tính mặt và bind pose với nguồn, kiểm tra ARM64 scope/trampoline/fallback và gateway manifest/checksum/idempotence. Nguồn tóc NEUBE do người dùng cung cấp.

## Ronaldo tóc mì tôm — đã ghép lên đầu Android trong Blender, CHƯA có bản cài

Đã giải nén đủ 8 phần RAR pc3700, trích 4 head Ronaldo đúng SHA1 theo TOC. Xuất đầu Android có166 xương, ghép5.005 đỉnh tóc PC vào sk_head của rig Android; xoay thử xương đầu, toàn bộ tóc đi theo. Giữ tọa độ đỉnh mặt Android. LOD0 được đánh dấu cooked_out, xuất phần LOD inline còn lại.

- [Bộ đầu Android + tóc ghép Blender/FBX/GLB (ZIP tham khảo, KHÔNG cài vào game)](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/ronaldo-android-fit/Ronaldo-ANDROID-head-noodle-REFERENCE-NOT-INSTALLABLE.zip)
- [Ảnh Blender — không phải ảnh game](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/ronaldo-android-fit/Android-head-PC-hair-reference.png)
- [Kết quả và phần còn thiếu](efootxi-1.3.2/ronaldo-android-fit/README.md)
- [Kiểm tra hash/geometry/rig](efootxi-1.3.2/ronaldo-android-fit/validation.json)

Mục tiêu chỉ thẻ88044950524330; chưa xác minh FaceId thực tế của thẻ, chưa port material, chưa tạo asset Android và chưa bật định tuyến theo thẻ. Không sửa dt200, APK, gateway hoặc đội hình v18. Mặt trong ảnh dùng clay; tóc dùng vật liệu xem trước. Nguồn tóc NEUBE do người dùng cung cấp.

## Ronaldo tóc mì tôm — nguồn PES đã chuyển đổi, CHƯA cài được trên Android

Mục tiêu riêng Card ID `88044950524330`. Đã trích xuất FMDL/FTEX và xuất Blender/FBX/GLB: 10 mesh, 10.705 tam giác, 12 texture. Lớp tóc xoăn 5.005 đỉnh chỉ gắn sk_head. **Chưa tạo asset Unreal Android, chưa sửa hay kiểm thử tóc trong game.** Cần đầu Ronaldo Android gốc, thích nghi rig/material và quy trình cook đúng game; không chép ZIP này đè vào game.

- [Tải bộ nguồn Blender/FBX/GLB — không phải bản cài](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/ronaldo-noodle-source/Ronaldo-noodle-88044950524330-SOURCE-NOT-INSTALLABLE.zip)
- [Kết quả, các giới hạn và hướng chuyển sang Android](efootxi-1.3.2/ronaldo-noodle-source/README.md)
- [Ảnh render nguồn — không phải ảnh game](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/ronaldo-noodle-source/Ronaldo_source_preview.png)

Nguồn mod NEUBE do người dùng cung cấp; giữ ghi công tác giả. Bộ đội hình v18 giữ nguyên.

## My League Studio v18 — đọc đội hình từ game, bỏ đội hình suy đoán

- [Bộ cập nhật lấy đội hình từ game (10 file, giữ myleague_editor.json đang có)](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/hotfix-v18/efootxi-v18-lineup-readback-update.zip)
- [Web editor v18 (ZIP; giải nén rồi mở MyLeagueEditor.html)](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/editor-v18/MyLeagueStudio-v18-offline.zip)
- [Hướng dẫn cài cập nhật → chép myleague-live-teams.json → nhập web → chỉnh/xuất](efootxi-1.3.2/editor-v18/HUONG_DAN.md)
- [Chi tiết nguồn dữ liệu và ánh xạ thứ tự cầu thủ](efootxi-1.3.2/editor-v18/NGHIEN_CUU.md)
- [Kiểm tra capture/order/bốn sơ đồ/captain/takers](efootxi-1.3.2/hotfix-v18/snapshot-validation.json)

Lỗi được xác nhận là đội hình web v17 không khớp game: roster tĩnh, sơ đồ suy ra khi thiếu plan, tự điền số áo và vai trò. v18 bỏ các đội hình này khỏi màn hình chỉnh. Đội phải đến từ bản đọc native hoặc dự án bạn chủ động nhập; đội chưa đọc được báo thiếu, không tự dựng thay.

Cài bộ cập nhật10 file, mở đội hình/đối thủ trong game rồi lấy files/embedded-gateway/work/tools/myleague-live-teams.json và nhập vào tab Đội hình của web. File chỉ chứa đội đã được game tra cứu; dữ liệu cache vào trận được ưu tiên. Bốn biến thể sơ đồ được giữ riêng, roster/order/taker/captain nối theo Card ID, giữ255 là chưa gán và giữ tham chiếu người dự bị. Nhập chưa tự ghi đè; sau khi sửa/lưu, ZIP do app xuất chứa đủ11 file để cài dự án mới.

Bộ cập nhật đầu tiên không chứa myleague_editor.json, đọc được dự án v17 mà không ghi lại file đó. Đọc snapshot chỉ copy record từ hook lookup/cache đã có; trình xuất Python không gọi engine. Chưa có file từ điện thoại người dùng để cam kết mọi CLB đã khớp; dữ liệu chỉ phản ánh những đội đã quan sát, không phải kết nối web trực tiếp hay bản sao DreamTeam sở hữu.

Đã kiểm tra web từng ID/số áo/captain/taker và44 ô thuộc bốn sơ đồ của fixture đảo order, không tự lưu khi chỉ xem; kiểm tra C→JSON→web→C và bộ tiêu thụ sơ đồ ARM64 gốc, cùng native/cache/crash/appearance/weather/gateway regressions. **Chưa kiểm tra tính năng mới trên Android.** Theo yêu cầu mới nhất, bản này chỉ sửa đội hình; không phát hành thay đổi tóc, mặt hoặc hình thể.

## My League Studio v17 — pack cầu thủ, tên skill chuẩn và preset chạy/rê bóng

- [Tải app v17 (ZIP; giải nén rồi mở MyLeagueEditor.html bằng Chrome/Edge)](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/editor-v17/MyLeagueStudio-v17-offline.zip)
- [Tải HTML tự chứa](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/editor-v17/MyLeagueEditor.html)
- [Hướng dẫn tạo pack, xuất10 file, MT Manager và trạng thái](efootxi-1.3.2/editor-v17/HUONG_DAN.md)
- [Kết quả nghiên cứu APK, skill, dáng chạy/rê bóng, tóc/mặt/cơ thể và tên](efootxi-1.3.2/editor-v17/NGHIEN_CUU.md)
- [Runtime v17 dự án trống](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/hotfix-v17/efootxi-1.3.2-native-hotfix-v17-editor-packs.zip)

Thêm tab Pack: tạo/nhập/xuất pack tuyển cầu thủ, chọn từ registry hiện có, tối đa32 pack ×300 thẻ. Không tự thêm thẻ giả hay thay DB/response của người khác. Gateway hiện tại thực hiện rút/cấp thẻ, serial, coin và receipt. Cài pack thêm định nghĩa pool vào DB local; không tự cấp cầu thủ. Các pool đã cài giữ nguyên membership; nhân bản ID mới để thay người, có thể đổi tên/ẩn. Lượt rút/reset và kho sở hữu được giữ. Banner mẫu, chưa tùy chỉnh ảnh.

Sửa64 tên skill theo mapping engine và APK; Attack Trigger đúng131, không phải AMAZON140. Defensive Fortress chưa có mã riêng được xác minh nên chưa khả dụng; Fortress vẫn có. Nhập dự án v16 có thông báo chuyển đổi skill, giữ bản JSON cũ và kiểm tra trước khi xuất.

Bổ sung5 trường preset native51–55: kiểu rê bóng, tư thế/tay khi rê bóng và tư thế/tay khi chạy. Đã kiểm tra đọc/ghi qua getter ARM64 gốc và hoàn nguyên theo phạm vi; chưa có preview hoặc kiểm chứng hình ảnh mọi preset trên Android. Chưa có chỉnh dáng đi bộ, ghép tóc/mặt, slider cơ bắp hay đổi tên native trong game. Tên trong app tham khảo được lưu riêng; không lấy ô nhập tên làm bằng chứng đã đổi tên trong trận.

Xuất ZIP từ app chứa đủ10 file để chép vào files/embedded-gateway/work/tools/. Sao lưu bộ file và save trước khi cài pack; không thay APK/dt200. Dự án mặc định trống; thời tiết/đội hình/buffs hiện có được giữ. Đã kiểm tra Chromium desktop/mobile, ZIP→native, gateway thật trên bản sao DB (list, draw, retry, reset, rollback) và các regression native/appearance/weather. **Chưa thử các tính năng mới trên Android.**

## My League Studio + native hotfix v16 — app chỉnh dữ liệu và lịch thời tiết

- [Tải app My League Studio v16 (ZIP, mở HTML trên Chrome/Edge)](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/editor-v16/MyLeagueStudio-v16-offline.zip)
- [Tải riêng file HTML tự chứa](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/editor-v16/MyLeagueEditor.html)
- [Hướng dẫn Android/MT Manager, xuất9 file và đọc trạng thái](efootxi-1.3.2/editor-v16/HUONG_DAN.md)
- [Runtime v16 mặc định: thời tiết mới, chưa thêm sửa cầu thủ/đội](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/hotfix-v16/efootxi-1.3.2-native-hotfix-v16-editor-weather.zip)
- [Kiểm tra ZIP xuất từ app qua mã native](efootxi-1.3.2/hotfix-v16/editor-validation.json)
- [Kiểm tra giao diện](efootxi-1.3.2/editor-v16/browser-validation.json)

App web tự chứa46.610 ID/tên cầu thủ và76 đội trong năm giải tùy chỉnh. Chỉnh chỉ số thành phần, thêm/xóa skill, chiều cao/cân nặng, tay dài/ngắn; thay người, dự bị, kéo vị trí, sơ đồ mẫu, vai trò và số áo. Xuất ZIP chứa đủ9 file runtime/cấu hình để chép vào files/embedded-gateway/work/tools/. Không cần root hoặc compiler; lưu và nhập lại dự án JSON để sửa tiếp. Phần đội hình là roster CLB native/đối thủ My League, không thay DreamTeam hoặc kho sở hữu. Chỉ dùng ID có trong engine hiện tại, chưa chỉnh mesh mặt/tóc/cơ bắp.

Thời tiết: ngày1–7 mùa hè, ngày8–14 mùa đông (ngày8 ưu tiên mùa đông do yêu cầu gốc chồng nhau), sau đó linh động. Mưa và sáng/tối thay đổi có seed ổn định; có thể chỉnh lịch/tỷ lệ trong app. Sương mù chưa có enum/đường điều khiển được xác minh nên không bật; không bật tuyết. **Thử nghiệm tay xắn Gullit đã bị tắt.**

Đã chạy giao diện Chromium (desktop/mobile390px), xuất/nhập/lưu dự án và ZIP. Đã nạp chính JSON từ ZIP đó vào thư viện C trong Unicorn rồi đọc lại bằng getter ARM64 gốc: stats/skill/cơ thể, tay dài/ngắn, bốn sơ đồ, số áo, captain/sáu taker, hoàn nguyên phạm vi/cache và chặn toàn bộ ghi đội khi thiếu cầu thủ. Native/cached/crash-entry/appearance/weather/gateway regression đều qua. **Chưa kiểm tra trực tiếp editor mới và hình ảnh thời tiết trên Android**; một số DB/resource boundary được mô hình hóa. File:// bị policy Chromium của môi trường chặn, nên app tự chứa được kiểm tra qua localhost. Tài nguyên app không cần mạng sau khi tải.

Giữ nguyên mã mô phỏng v10, không sửa APK/dt200/CPK/save. Buộc dừng, sao lưu và chép đủ9 file, mở lại My League/trận mới. Mỗi ZIP do app xuất đã kèm runtime v16; không cần cài runtime mặc định trước.

## Native hotfix v15 — tay dài theo giải, bản thử riêng Gullit

- [Tải bản tay dài thông thường](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/hotfix-v15/efootxi-1.3.2-native-hotfix-v15-long-sleeve.zip)
- [Tải bản thử giá trị tay áo riêng Gullit88045755960810 — chưa xác nhận là tay xắn](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/hotfix-v15/efootxi-1.3.2-native-hotfix-v15-gullit-sleeve-trial.zip)
- [Cài đặt, chọn bản và quay lại](efootxi-1.3.2/hotfix-v15/HUONG_DAN.md)
- [Phân tích tay xắn và giới hạn bằng chứng](efootxi-1.3.2/hotfix-v15/NGOAI_HINH.md)
- [Danh sách ID theo đúng tên/giải](efootxi-1.3.2/hotfix-v15/sleeve-targets.json)
- [Kiểm tra ARM64](efootxi-1.3.2/hotfix-v15/appearance-validation.json)

V14 đã được người dùng xác nhận tay dài hoạt động. V15 mở rộng cho Ronaldo/Messi trong Y17(518) và Kvaratskhelia/Dembélé/Bellingham/Mbappé/Haaland trong UEFA My League(122), giữ đúng phạm vi giải và hai thẻ Ronaldo v14. Nhận diện249 bản ghi đã xác minh tên chính xác, không dùng suy đoán lowbits. 1.024 ca builder kiểm tra phạm vi và32 ca bật/tắt giá trị thử đã qua cùng các kiểm tra native/cache/gateway/save.

Kiểu tay dài xắn ngang cẳng tay như ảnh **chưa có cờ/mesh được xác minh**. Bản ZIP thử bật packed mode3/config2 chỉ cho ID88045755960810, được bảng Android xác nhận là Ruud Gullit. Giá trị này được native chuyển tới LoadUniShirt nhưng không có trong các bản ghi nguồn và đi nhánh resource áo ngắn ở đường đã nghiên cứu; không thể tuyên bố nó tạo tay xắn. Bản thường để thử nghiệm tắt. Nhóm cầu thủ mới và thử nghiệm chưa được kiểm tra hình ảnh trên Android.

Mỗi ZIP chứa đủ7 file; chọn một, không cần cài lần lượt. Buộc dừng game, sao lưu rồi chép đủ7 file vào files/embedded-gateway/work/tools/, vào trận mới. Nếu muốn tắt thử nghiệm Gullit, cài lại ZIP thường v15. Hai ZIP chỉ khác cờ bật thử trong myleague_custom.json; không thay save, lịch, chỉ số, roster, tóc/mặt, dt200/APK/CPK. Mô phỏng giữ nguyên v10.

## Native hotfix v14 — sửa theo đúng ID Ronaldo đã ghi nhận

- [Tải ZIP v14 — cài đủ 7 file](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/hotfix-v14/efootxi-1.3.2-native-hotfix-v14-long-sleeve.zip)
- [Hướng dẫn và các trường kiểm tra mới](efootxi-1.3.2/hotfix-v14/HUONG_DAN.md)
- [Phân tích ID thực tế và giới hạn](efootxi-1.3.2/hotfix-v14/NGOAI_HINH.md)
- [Kiểm tra ARM64 và phát lại22 ID từ log](efootxi-1.3.2/hotfix-v14/appearance-validation.json)

Log v13 trong giải518 cho thấy builder chạy24 lần, có Ronaldo88044950524330 nhưng không có ID89138556572074. V14 bổ sung chính xác88044950524330 vào danh sách thẻ tay dài, giữ89138556572074; **không khẳng định hai ID là alias**. Sửa bản sao packed appearance và đầu ra builder vốn đã được gọi trên thiết bị. Bỏ fallback ID base4522/16781738 của v13. Không thêm điểm hook mới.

Thêm appearance_build_matches_by_id, appearance_last_applied_id và appearance_build_after. Đã phát lại22 ID từ log qua native builder với DB boundary mô hình, chỉ ID Ronaldo trong danh sách nhận thay đổi; kiểm tra hai thẻ, các ID khác, bộ đếm, serializer, chọn resource và hồi quy native/cache/gateway đều qua. **Chưa kiểm chứng hình ảnh tay áo trên Android.**

Mã roster14 ở Real1220/Liverpool1221 là nhánh bỏ ghi khi slot có PlayerKey.kind chưa hỗ trợ; giữ chốt kiểm tra, chưa sửa khi thiếu dữ liệu khóa slot. Giữ nguyên mô phỏng v10, đội hình, chỉ số, tóc/mặt, save và dt200. Buộc dừng game, sao lưu rồi chép đủ7 file vào files/embedded-gateway/work/tools/, vào trận mới.

## Native hotfix v13 — xử lý tay dài ngay lúc nạp áo UE

- [Tải ZIP v13 — cài đủ 7 file](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/hotfix-v13/efootxi-1.3.2-native-hotfix-v13-long-sleeve.zip)
- [Hướng dẫn MT Manager, phạm vi và bộ đếm mới](efootxi-1.3.2/hotfix-v13/HUONG_DAN.md)
- [Đường nạp áo và giới hạn kiểm chứng](efootxi-1.3.2/hotfix-v13/NGOAI_HINH.md)
- [Kiểm tra ARM64 và chọn tài nguyên áo](efootxi-1.3.2/hotfix-v13/appearance-validation.json)

V12 được người dùng xác nhận vẫn tay ngắn khi đã vào sân: builder gọi24 lần nhưng exact-ID match0, entity0. V13 thêm điểm xử lý trực tiếp trước khi UE chọn mẫu áo ngắn/dài và gọi LoadUniShirt. Nhận diện thẻ89138556572074 cùng hai alias4522/16781738, đều được xác minh đúng tên Cristiano Ronaldo trong Player.bin. **Các thẻ Ronaldo khác được renderer gom về cùng alias cũng có thể nhận tay dài.** Không dùng phép cắt lowbits cho ID tùy ý.

Đã chạy thêm67 ca mã ARM64 hàm nạp áo đến đúng lệnh gọi LoadUniShirt, kiểm tra cặp tài nguyên ngắn/dài và tham số tay áo; chỉ trường tay áo khác baseline ở ID khớp. Kit lookup dùng dữ liệu mô hình, chưa xác nhận mesh/texture thực tế hoặc hình ảnh trên Android. Các kiểm tra builder/serializer, đội hình, cache, chỉ số, gateway/save đều qua. Giữ nguyên mã mô phỏng v10, không sửa tóc, mặt hay dt200.

Bộ đếm mới: appearance_shirt_calls, appearance_shirt_matches, appearance_shirt_alias_matches, appearance_shirt_applies và danh sách appearance_build_ids/appearance_shirt_ids. Buộc dừng game, sao lưu rồi chép đủ7 file vào files/embedded-gateway/work/tools/, vào trận mới và đọc select-team-status.json phiên bản native-hotfix-v13.

## Native hotfix v12 — sửa đường áp dụng tay dài Ronaldo

- [Tải ZIP v12 — chép đủ 7 file](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/hotfix-v12/efootxi-1.3.2-native-hotfix-v12-long-sleeve.zip)
- [Cài đặt và đọc bộ đếm mới](efootxi-1.3.2/hotfix-v12/HUONG_DAN.md)
- [Phân tích và giới hạn kiểm chứng](efootxi-1.3.2/hotfix-v12/NGOAI_HINH.md)
- [Kiểm tra ARM64](efootxi-1.3.2/hotfix-v12/appearance-validation.json)

Người dùng xác nhận v11 vẫn tay ngắn, bộ đếm áp dụng bằng 0. V12 thêm hai điểm áp dụng theo full64 ID yêu cầu và ID nhân vật cho đúng thẻ **89138556572074**, sửa cấu hình tay áo sau bộ dựng gốc và trước bước dispatch vào nhân vật. Bổ sung bộ đếm gọi/khớp ID và tình trạng cài từng hook. Giữ đường serializer làm bổ sung. Chưa có kết quả hình ảnh trên thiết bị.

Đã kiểm tra 107 ca serialize, 16 ca toàn bộ hàm dựng, 13 ca dispatch, 6 ca mode/mùa và Python diagnostics. Kịch bản DB trả khóa trung gian khác ID yêu cầu đã được mô phỏng: v11 bỏ qua, v12 áp dụng đúng; đây chưa phải nguyên nhân đã xác nhận trên máy người dùng. Kiểm tra hồi quy đội hình, cache, chỉ số, save và gateway đã qua. Giữ nguyên mã mô phỏng v10; không sửa tóc, mặt, dt200 hoặc save.

Buộc dừng game, sao lưu rồi chép đủ 7 file vào `files/embedded-gateway/work/tools/`. Vào trận mới với đúng thẻ và đọc `select-team-status.json` phiên bản `native-hotfix-v12`. Bộ đếm dương xác nhận thao tác ghi, vẫn cần quan sát tay áo trong trận.

## Native hotfix v11 — bản thử tay dài Ronaldo, nghiên cứu ghép tóc

- [Tải ZIP v11 — cài đủ7 file](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/hotfix-v11/efootxi-1.3.2-native-hotfix-v11-long-sleeve.zip)
- [Cài đặt MT Manager và kiểm tra bộ đếm](efootxi-1.3.2/hotfix-v11/HUONG_DAN.md)
- [Kết quả tay áo, hướng ghép tóc và tài nguyên thiếu](efootxi-1.3.2/hotfix-v11/NGOAI_HINH.md)
- [Kiểm tra serialize/converter ARM64](efootxi-1.3.2/hotfix-v11/appearance-validation.json)

Chỉ thẻ Ronaldo89138556572074 nhận chế độ tay dài2, tham chiếu Bale88041729329832. Hook trên bản sao52 byte ngoại hình, xác thực full64 ID; không sửa bảng gốc, mặt, tóc hoặc chỉ số. Đã chạy serializer/converter gốc, kiểm tra6 trường hợp mùa/chế độ và107 trường hợp serialize cùng đường chuẩn bị tham số áo. **Chưa kiểm tra hình ảnh trên điện thoại.** Bộ đếm`appearance_sleeve_applies` và`appearance_error` nằm trong`select-team-status.json` phiên bảnv11.

TócPato88038776539586→Ronaldo88044950524330 **chưa áp dụng**. Đã xác định các asset real-face chứa mặt/tóc chung mesh, có dữ liệu phần tóc và bảng redirectPato0318→0290; chưa có đủ mesh/texture nguồn/đích để kiểm chứng ghép riêng tóc. Không đổi toàn bộ mặt hay gán tóc generic thay thế. Hướng nghiên cứu và dữ liệu cần bổ sung được ghi rõ trong báo cáo.

Giữ nguyên mô phỏngv10, đội hình, số áo, chỉ số, lịch mùa và save. Buộc dừng, sao lưu rồi chép đủ7 file vào`files/embedded-gateway/work/tools/`. Không thaydt200/CPK/APK/DB. Có thể phục hồi đủ7 filev10 khi cần.

## Native hotfix v10 — kết quả CPU đa dạng cho bốn giải My League

- [Tải ZIP v10 — đủ7 file](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/hotfix-v10/efootxi-1.3.2-native-hotfix-v10.zip)
- [Hướng dẫn MT Manager, phân nhóm và giới hạn](efootxi-1.3.2/hotfix-v10/HUONG_DAN.md)
- [Kết quả6.744 trận kiểm tra](efootxi-1.3.2/hotfix-v10/simulation-validation.json)
- [Trạng thái phát hành](efootxi-1.3.2/hotfix-v10/RELEASE_STATUS.json)

Ligue1 dùng7 nhóm mới; Scottish ưu tiên Real/Barça/Juventus; tuyển châu Á có xác suất đối đầu riêng của Nhật; tuyển thế giới ưu tiên Tây Ban Nha. Kết quả CPU kết hợp sân nhà, phong độ5 trận, pha phong độ theo giai đoạn và tính cách đội; bộ chọn cả vòng hạn chế tỷ số lặp và theo dõi phân bố5 vòng. Cú sốc lớn giới hạn2 trong10 vòng; đa dạng ghi bàn/kiến tạo đúng ID trong roster, không tạo cầu thủ hoặc sự kiện trận giả.

Trong6 mùa Ligue1 kiểm tra: hòa22,22%, chủ nhà44,44%, khách33,33%,2,806 bàn/trận;204/204 vòng đạt quota đa dạng. Các số điểm/bàn cuối mùa là mục tiêu xấp xỉ, không cam kết cố định. Giữ12 đội/22 vòng Scottish và các đội tuyển đang có. Trận người dùng chơi, lịch cũ, kết quả/biên nhận đã lưu được bảo toàn.

Buộc dừng app, sao lưu và chép đủ7 file vào `files/embedded-gateway/work/tools/`, kiểm tra `native-hotfix-v10`. Không thay dt200/APK/DB hoặc xóa save. Native binary giữ nguyên v9; báo cáo native cũ được ghi rõ baseline. **Chưa kiểm tra trên điện thoại.** Các giới hạn texture áo/sân/thời tiết từ v9 vẫn còn; bản này chỉ cập nhật mô phỏng CPU.

## Native hotfix v9 — phục hồi thông thạo vị trí gốc, đội hình và tên giải

- [Tải ZIP v9 — cài đủ 7 file](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/hotfix-v9/efootxi-1.3.2-native-hotfix-v9.zip)
- [Hướng dẫn MT Manager](efootxi-1.3.2/hotfix-v9/HUONG_DAN.md)
- [Đội trưởng, penalty, vị trí và số áo từng cầu thủ](efootxi-1.3.2/hotfix-v9/DOI_HINH_CO_DIEN.md)
- [Trạng thái và giới hạn](efootxi-1.3.2/hotfix-v9/RELEASE_STATUS.json)
- [Kiểm tra các đường tên UI/native](efootxi-1.3.2/hotfix-v9/ui-names-validation.json) · [Hợp đồng ô vị trí theo phản hồi người dùng](efootxi-1.3.2/hotfix-v9/live-contract-validation.json) · [Thời tiết](efootxi-1.3.2/hotfix-v9/weather-validation.json)

V9 gỡ tính năng thông thạo mọi vị trí, giữ nguyên các trường vị trí và độ thông thạo nguồn. Thứ tự roster được đảo cùng formation và các tham chiếu theo ID, dựa trên các ô sai mà người dùng báo: Real, Barça, Bayern, City, Liverpool, PSG, Tottenham. Ederson bắt chính cho City. Đội trưởng và penalty của đủ 12 đội được gán theo danh sách mới; số áo được kiểm tra không trùng. Đội retro pha trộn vẫn có các ngoại lệ số áo lịch sử đã ghi trong hướng dẫn.

Tên mới: **Y17 Champion League**, **Asia-Pacific League**, **Uefa Champion League**, **World Nation League**, **AFC Nation League**. Ngoài đường tên thường, bản này sửa ba đường AllCaps và trường tên trong native competition record để bao phủ cách giao diện My League đọc tên.

Sân nhà 76 đội vẫn lấy từ st001/007/030/051/052/085; selector My League đã chuẩn bị không trả sân 100. Cấu hình xoay qua ngày/quang, ngày/mưa, đêm/mưa, đêm/quang; bật đúng cờ native cho phép mưa và ban đêm trên sáu sân này. **Đã kiểm tra cấu hình và native accessor; chưa xác nhận hiệu ứng mưa/ánh sáng hay giao diện trên điện thoại.** Tuyết vẫn tắt; giữ mùa đông vòng 8–14.

Buộc dừng app, sao lưu rồi chép đủ 7 file vào `files/embedded-gateway/work/tools/`, mở lại và kiểm tra `native-hotfix-v9`. Không thay dt200/CPK/APK/DB hoặc xóa save. Các báo cáo ghi rõ phần giả lập/stub. Giới hạn texture áo còn thiếu từ bản v8 được giữ nguyên.

## Native hotfix v8 — Scottish: đội hình, OVR, kit và sân nhà

- [Tải ZIP v8 — chép đủ 7 file](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/hotfix-v8/efootxi-1.3.2-native-hotfix-v8.zip)
- [Hướng dẫn MT Manager và các giới hạn](efootxi-1.3.2/hotfix-v8/HUONG_DAN.md)
- [Đội hình, số áo, ID, vai trò và OVR từng cầu thủ](efootxi-1.3.2/hotfix-v8/DOI_HINH_CO_DIEN.md)
- [Phân bổ sân nhà của 76 đội](efootxi-1.3.2/hotfix-v8/home-stadiums.json)
- [Trạng thái và phần chưa hoàn thành](efootxi-1.3.2/hotfix-v8/RELEASE_STATUS.json)
- [Kiểm tra accessor bản sao Team qua detour thật](efootxi-1.3.2/hotfix-v8/cached-detours-validation.json) · [Kiểm tra chọn sân và con trỏ this](efootxi-1.3.2/hotfix-v8/stage-detours-validation.json)

V8 sửa cả DBTeam lẫn bản sao Team dùng khi chuẩn bị trận, gán lại vị trí/captain/người đá bóng chết/số áo, bỏ năm trong tên Scottish, thay người theo yêu cầu. Cầu thủ Scottish thông thạo mọi vị trí ngoài sân. OVR nền mặc định 90, ngôi sao 92–94, Ronaldo 96/Messi 97; bộ chỉ số 90+ và các kỹ năng đặc biệt được gán theo cấu hình. Giữ kết quả cũ và quy tắc các giải khác.

Kit được sửa ở bản sao dữ liệu, uniform ID và bộ phân giải tài nguyên 3D. **Trong các container hiện có, tìm thấy texture Barça/PSG nhưng chưa tìm thấy texture Man City/Tottenham/Atlético.** Chưa thể cam kết áo chuẩn của ba đội nếu máy cũng thiếu các gói tương ứng. V8 không tự tạo hoặc nhập texture áo mới.

Năm giải dùng sân nhà được phân bổ từ st001/007/030/051/052/085. Selector My League đã chuẩn bị không trả sân 100. Gateway chỉ ghi setter nguyên tử; member hook do game gọi giữ nguyên this ở đường gốc, tránh lỗi v7. Cấu hình ngày/đêm và hè/đông theo vòng; vòng 8–14 là mùa đông. **Mưa và tuyết chưa bật vì các bản ghi sân được cung cấp báo khả năng bằng 0.** Tài nguyên sân và hiệu ứng thực tế cần kiểm tra trên điện thoại.

Buộc dừng app, sao lưu rồi chép đủ 7 file vào `files/embedded-gateway/work/tools/`; mở lại kiểm tra `native-hotfix-v8`. Không thay dt200/CPK/APK/DB hoặc xóa save. Đã qua kiểm tra ARM64/gateway; chưa thử vào trận/render trên thiết bị Android. V7.1 bên dưới là bản quay lại nếu cần.

## Native hotfix v7.1 — sửa văng ngay khi mở My League

- [Tải ZIP v7.1](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/hotfix-v7.1/efootxi-1.3.2-native-hotfix-v7.1.zip)
- [Cài đủ7 file bằng MT Manager; buộc dừng app trước khi thay](efootxi-1.3.2/hotfix-v7.1/HUONG_DAN.md)
- [Bằng chứng tái hiện crash v7 bằng mã gốc và kiểm tra7.1](efootxi-1.3.2/hotfix-v7.1/entry-crash-validation.json)
- [Kiểm tra command mở My League thật, prepare và START](efootxi-1.3.2/hotfix-v7.1/environment-validation.json)
- [Đội hình/ID/vai trò](efootxi-1.3.2/hotfix-v7.1/DOI_HINH_CO_DIEN.md) · [Trạng thái](efootxi-1.3.2/hotfix-v7.1/RELEASE_STATUS.json)

V7 gọi một native member accessor không truyền đối tượng: lệnh thật `ldr x0,[x0,#0x28]` đọc0x28 khi X0=0. Đường này chạy trong CMD_GET_SEASON_INFO lúc mở My League. Kiểm thử v7 từng stub accessor nên bỏ sót ABI lỗi;7.1 đã tái hiện với mã thật và bỏ hẳn đường gọi sai.

**V7.1 tắt toàn bộ dò sân, hook chọn sân và thay đổi thời tiết mới.** Giữ sân do game gốc chọn, trời quang/mùa hè/ban ngày. Không random sân/mưa/tuyết trong bản sửa này. Đội hình retro, OVR, skill, kit và logic CPU của v7 được giữ.

Buộc dừng app, chép đủ7 file trong ZIP vào `files/embedded-gateway/work/tools/`, mở lại và kiểm tra `native-hotfix-v7.1`. Không xóa dữ liệu hoặc thay dt200. Bản sửa qua kiểm tra mã gốc/gateway; vẫn cần người dùng xác nhận trên điện thoại.

## Native hotfix v7 — bản lỗi crash, dùng v7.1 ở trên

**Không cài mới v7: đã xác định lỗi native khi mở My League. Dùng v7.1.**

- [Tải ZIP v7](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/hotfix-v7/efootxi-1.3.2-native-hotfix-v7.zip)
- [Hướng dẫn MT Manager: đủ7 file, giới hạn và khôi phục](efootxi-1.3.2/hotfix-v7/HUONG_DAN.md)
- [12 đội,190 vị trí: ID đầy đủ, vai trò, số áo, người thay và đá phạt](efootxi-1.3.2/hotfix-v7/DOI_HINH_CO_DIEN.md)
- [Cấu hình](efootxi-1.3.2/hotfix-v7/myleague_custom.json) · [Trạng thái và phần chưa hoàn thành](efootxi-1.3.2/hotfix-v7/RELEASE_STATUS.json)
- [Kiểm tra ARM64](efootxi-1.3.2/hotfix-v7/native-validation.json) · [14330 thẻ/OVR/kỹ năng](efootxi-1.3.2/hotfix-v7/v7-rules-validation.json) · [Gateway sân/thời tiết](efootxi-1.3.2/hotfix-v7/environment-validation.json)

Scottish đổi AC Milan thành Atletico2017, Inter thành Tottenham2020; dựng lại các đội retro theo yêu cầu. Hai ID Ronaldo/Bale2017 được giữ đúng. Bỏ các cầu thủ hiện đại dùng tạm v6; khi thiếu người, dùng cựu cầu thủ cùng CLB và công khai ngoại lệ, không đổi tên người thay. Đội hình không hoàn toàn trùng một mùa ở mọi CLB.

OVR nền My League87–95, riêng giải Bỉ566 là80–86; Messi Curl/Dribbling94. Scottish đổi Chop→Tap Trick, Marseille→Momentum, bổ sung kỹ năng theo vai; hậu vệ Ligue122 thêm Fortress/Sliding/Interception/Blocker và giữ skill khác. Tỷ lệ CPU cũ được giữ, tỷ số thay đổi trọng số để đa dạng hơn. Toàn bộ12 đội dùng logo/kit gốc, gồm sửa cả uniform ID gửi vào trận. Không nhập áo theo mùa lịch sử.

**Chưa có kiểm thử trên điện thoại. Tuyết chưa áp dụng được ở sáu sân nguồn (cờ snow=0); vòng8–14 yêu cầu đông/tuyết nhưng dùng trời quang khi engine không hỗ trợ.** Mưa/mùa/ngày đêm có cấu hình nhưng hiệu ứng render còn tùy Android. Sân chọn ngẫu nhiên trong1/7/30/51/52/85 mà engine xác nhận đã cài; thiếu toàn bộ sân/hook thì giữ selector gốc để không phá To Match, do đó chưa đảm bảo bỏ100 trên mọi máy. Xem `myleague-environment-status.json` để phân biệt phần đã áp dụng và phần đang thiếu. Không thay dt200, CPK, APK hay save.

## Native hotfix v6 — Super League thực tế, Scottish cổ điển, luật cầu thủ

**V6 đã kiểm tra thành phần ARM64/gateway, chưa thử trên điện thoại.** Có12 đội Scottish cổ điển,175 vị trí dùng172 ID thật,47 chỗ thay tạm theo lựa chọn của người dùng. Không đổi tên/face người thay để giả thành người còn thiếu.

- [Tải ZIP v6](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/hotfix-v6/efootxi-1.3.2-native-hotfix-v6.zip)
- [Hướng dẫn MT Manager và giới hạn](efootxi-1.3.2/hotfix-v6/HUONG_DAN.md)
- [Toàn bộ đội hình, số áo, ID và người thay](efootxi-1.3.2/hotfix-v6/DOI_HINH_CO_DIEN.md) · [47 chỗ thay JSON](efootxi-1.3.2/hotfix-v6/classic-replacements.json)
- [Cấu hình](efootxi-1.3.2/hotfix-v6/myleague_custom.json) · [Trạng thái](efootxi-1.3.2/hotfix-v6/RELEASE_STATUS.json)
- [Native18 roster/formation/OVR](efootxi-1.3.2/hotfix-v6/native-validation.json) · [Gateway12 CLB](efootxi-1.3.2/hotfix-v6/classic-gateway-validation.json) · [80.000 trận CPU](efootxi-1.3.2/hotfix-v6/club-policy-validation.json)

Nhóm1 thắng nhóm2 khoảng70%, riêng El Clasico cân bằng; nhóm1 gặp nhóm cuối90%. Tỷ số bóng đá được giới hạn hợp lý, không còn7–4/4–2 trong mô phỏng giải122. Giữ85% trước nhóm3 và95% cho nhóm2 trước nhóm4 từ cấu hình cũ. Roma/Dortmund và Gala/Napoli có khác biệt sân nhà/khách. Không sửa kết quả đã chốt hay trận người dùng đá; giao thức chưa có phút ghi bàn CPU, không giả sự kiện MU thủng lưới phút cuối.

Sửa Fabián Ruiz105820209653455: Acceleration88, Speed88, Tackling90, Defensive Awareness90. Kicking Power>84 được+7 (trần packed127), không cộng lặp; tiền vệ/tiền đạo thiếu cả Low Screamer lẫn Blitz Curler được Dipping Shot. Bayern127: Kane9, Díaz14, Olise17, Musiala10.

Scottish518 dùng12 CLB cổ điển, giữ lịch22 vòng của gói. Hồ sơ NPC cổ điển bỏ Marseille Turn, cân bằng **OVR nền≤89** ở13 vị trí; giữ dữ liệu/serial thẻ sở hữu. Messi chỉ định có Blitz Curler/Momentum; thêm kỹ năng theo vai và đã xác minh Attack Trigger128. PSG/City/Liverpool cổ điển alias logo/kit gốc. Boost HLV và render/trận thực vẫn cần xác nhận trên thiết bị. Không thay dt200/CPK/APK/save.

Cài đủ sáu file vào `files/embedded-gateway/work/tools`, buộc dừng mở lại. Kiểm tra `native-hotfix-v6`, `presentation_error:null`, rồi thử trận Bayern127 và Scottish. `native_last_player_full_id` mới giúp báo đúng lỗi thẻ64 bit. Giữ Asia-Pacific8 đội ở Danish549; Eredivisie125 là giải Hà Lan gốc. Tóc/áo dài và Power Tackle từ yêu cầu cũ vẫn chưa áp dụng.

## Native hotfix v5 — bản trước

Gói trước có Asia-Pacific8 đội/Danish, tên/logo và cầu thủ, chưa có12 đội Scottish cổ điển hay logic mới của v6.

- [Tải lại ZIP v5](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/hotfix-v5/efootxi-1.3.2-native-hotfix-v5.zip)
- [Hướng dẫn lịch sử v5](efootxi-1.3.2/hotfix-v5/HUONG_DAN.md)

## Native hotfix v4.1 — nền đã được người dùng xác nhận Bayern hoạt động

Người dùng xác nhận mọi thứ ổn và Bayern Munich đã hoạt động sau v4.1. Gói này giữ làm bản khôi phục khi cần, với22 cầu thủ Bayern, Dembélé Tap Trick và tỷ lệ CPU85/95. Chưa có các yêu cầu mới của v5.

- [Tải lại ZIP v4.1](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/hotfix-v4.1/efootxi-1.3.2-native-hotfix-v4.1.zip)
- [Hướng dẫn lịch sử v4.1](efootxi-1.3.2/hotfix-v4.1/HUONG_DAN.md)

## Native hotfix v4 — đã xác nhận còn lỗi Bayern59835

Các roster khác đạt trong log người dùng; Bayern chưa đạt do ID59835. [Trạng thái cập nhật](efootxi-1.3.2/hotfix-v4/STATUS.json). Gói v4 giữ để đối chiếu; dùng bản thử v4.1 phía trên cho lỗi này.

## Native hotfix v3 — đã xác nhận lỗi kiểm tra roster, giữ để đối chiếu

Không cài lại v3 để thử sửa To Match Bayern. [Trạng thái v3](efootxi-1.3.2/hotfix-v3/STATUS.json). V4 thay thế đường tra cứu sai; v3 được giữ trong lịch sử và không được khuyến nghị.

## Hierarchy v2 — đã xác nhận crash Bayern, giữ để đối chiếu lịch sử

Không cài lại v2 để thử sửa crash Bayern. [Trạng thái v2](efootxi-1.3.2/hierarchy-v2/STATUS.json). Tham khảo bản v4.1 phía trên; không tự xóa save hoặc thay CPK.

## My League Realism v1 — nâng cấp lịch, CPU và vua phá lưới

Bản Select Team trước đã được người dùng xác nhận hoạt động. Bản nâng cấp này **giữ nguyên native Select Team**, chỉ cập nhật hai file Python trong vùng nội bộ `embedded-gateway/work/tools`.

- [Tải ZIP My League Realism v1](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/myleague-realism/efootxi-1.3.2-myleague-realism-v1.zip)
- [Hướng dẫn cài/gỡ và ảnh hưởng đến mùa hiện tại](efootxi-1.3.2/myleague-realism/HUONG_DAN.md)
- [Mã mô hình](efootxi-1.3.2/myleague-realism/myleague_realism.py)
- [Kiểm chứng save/receipt và 300 mùa mô phỏng](efootxi-1.3.2/myleague-realism/validation.json)

Lịch mùa mới ngẫu nhiên một lần rồi lưu; mùa hiện tại giữ lịch và kết quả đã đá. CPU xét sức mạnh công/thủ, sân nhà và phong độ; phân bổ bàn/kiến tạo theo roster thật trong game, vị trí, chất lượng base card và đội hình chính/dự bị. Không tự cộng bàn cho CLB người chơi. Đã kiểm tra phía gateway trên DB sao chép và mô phỏng; **bản Realism mới chưa xác nhận trên điện thoại**.

## Sửa trực tiếp menu Select Team, không root — người dùng đã xác nhận hoạt động

**Người dùng xác nhận menu Select Team hoạt động ngày 20/10/2026 trên máy không root.** Bản sửa nạp qua gateway Python sẵn có, sửa danh sách My League trong bộ nhớ; không thay CPK, DB/save hoặc ký lại APK. Đã kiểm tra mã C và hàm ARM64 gốc, cả nhánh gọi mới/trampoline, với vector tổng hợp. Phần kiểm tra tự động không bao gồm Android UI; chưa có xác nhận riêng về toàn bộ luồng vào trận.

- [Tải ZIP bản thử native](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/select-team-native/efootxi-1.3.2-select-team-native-experimental.zip)
- [Hướng dẫn MT Manager và cách gỡ](efootxi-1.3.2/select-team-native/HUONG_DAN.md)
- [Phạm vi/phiên bản hỗ trợ](efootxi-1.3.2/select-team-native/BASELINE.json)
- [Kiểm tra hàm ARM64](efootxi-1.3.2/select-team-native/native-validation.json)

Khôi phục dt200 gốc trước, chỉ chép ba file của gói vào vùng **nội bộ** `embedded-gateway/work/tools` qua DocumentsProvider `73efootball 资源`. Nếu vẫn không đổi đội, file `select-team-status.json` cho biết bước nào chưa chạy. Đọc hướng dẫn trước khi thử. Menu đã được người dùng xác nhận hoạt động; giữ nguyên hai file native khi cài Realism.

## Hướng khác: chọn đội qua máy chủ/save, không sửa CPK

Công cụ này gọi đúng logic My League Android để tạo **một bản sao save mới** đã chọn đội. Đã kiểm tra Arsenal trong Ligue 1: 18 đội, 34 vòng, mở lại save/đọc thông tin mùa giải/chuẩn bị đối thủ thành công; bảng cầu thủ và vật phẩm không đổi. Từ chối ghi đè file hoặc thay mùa đã có khi chưa được yêu cầu.

**Chỉ mới xác minh phía máy chủ. Chưa chứng minh game Android mở mùa giải hoặc chơi trận thành công. Công cụ không thay danh sách Select Team nguyên bản. Cần save thực tế đang chơi và gateway đúng phiên bản; không dùng save seed trong APK để ghi đè save của bạn.**

- [Tải công cụ và hướng dẫn](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/server-team-selector/efootxi-server-team-selector.zip)
- [Đọc hướng dẫn](efootxi-1.3.2/server-team-selector/HUONG_DAN.md)
- [Xem mã công cụ](efootxi-1.3.2/server-team-selector/select_myleague.py)
- [Kết quả kiểm tra phía máy chủ](efootxi-1.3.2/server-team-selector/validation.json)

## Face, chỉ số và ngoại hình

[Phân tích mã iOS và đối chiếu Android](research/player-face-stats.md), đã cập nhật hai nhánh iOS người dùng gửi tại commit be7b0aa và f8dc2a8: phân biệt preset tham số 49–60, mesh/texture RealFace, chỉ số thẻ đang sở hữu và ngoại hình như tay áo. Có liên kết tới các dòng mã thực tế và ví dụ đường dẫn asset.

[SHA-256 các file](SHA256SUMS). Các bản thử thất bại được giữ để đối chiếu lịch sử và đánh dấu ngừng dùng; chúng không phải bản sửa được khuyến nghị.
