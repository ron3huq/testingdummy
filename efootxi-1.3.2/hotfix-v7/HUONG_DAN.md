> **V7 có lỗi văng ngay khi mở My League. Dùng [bản sửa v7.1](../hotfix-v7.1/HUONG_DAN.md).**

# My League native hotfix v7 — Android efootxi1.3.2

Bản mới dựng lại12 đội Scottish: AC Milan/Aberdeen thành Atletico2017; Inter/Kilmarnock thành Tottenham2020. Cập nhật Liverpool2019, Real2017 (đúng hai Card ID Ronaldo70373039149482 và Bale88045755861672), Bayern2018, PSG/Chelsea2018, City/Juventus2017, vị trí MU/Roma. Có190 vị trí với179 ID riêng. Xem DOI_HINH_CO_DIEN.md cho từng ID, đội hình, số áo, người thay và vai trò đá phạt/đội trưởng.

## Cài bằng MT Manager

1. Buộc dừng game. Sao lưu các file đang chạy tốt.
2. Giải nén ZIP, lấy **đủ7 file** trong `install/work/tools/` và chép đè vào thư mục đang dùng: `73efootball 资源/files/embedded-gateway/work/tools/` (hoặc chính thư mục `files/embedded-gateway/work/tools/` nơi bạn cài v6).
3. Bảy file là `gateway_runtime.py`, `select_team_runtime.py`, `libselect_team.so`, `myleague_realism.py`, `myleague_worlds.py`, `myleague_balance.py`, `myleague_custom.json`. Không trộn thư viện hoặc JSON của v6 với v7.
4. Mở lại game. Kiểm tra `select-team-status.json`: version `native-hotfix-v7`, state `HOOK_ACTIVE`. `presentation_error` và `environment_error` nên là `null`. My League đang mở được ghi tại `active_competition`; sân được hook chọn nằm ở `selected_stadium`; `ovr_balance_failures` nên bằng0.
5. Thử một trận Bayern127 trước, sau đó vào Scottish. Đội hình/kit/sân vẫn cần kiểm tra trên điện thoại. Không cần thay dt200, CPK, APK hay dữ liệu lưu; ZIP không chứa tài khoản hoặc DB cá nhân.

Nếu lỗi, khôi phục đủ6 file v6 đã sao lưu, gỡ riêng `myleague_balance.py` của v7 và buộc dừng/mở lại. Không xóa save hoặc cài lại game để thử.

## Đội hình và kit

V7 bỏ những người hiện đại từng thay tạm như Doué, Palmer, Gvardiol, Enzo, Koné, Wesley, De Ligt, Wan-Bissaka, Yıldız, McKennie, Douglas Luiz, Matheus Nunes, Araújo, Frimpong, Mac Allister và Konaté. Các cầu thủ đang thi đấu hiện nay nhưng thực sự thuộc đội hình giai đoạn đó (Kane, Salah, Koke...) vẫn được giữ.

Không có đầy đủ mọi người trong nguồn: chẳng hạn Robben, Boateng, Aurier, Dele Alli, Fernandinho đúng người và nhiều thành viên Juventus2017. Đội thiếu dùng cựu cầu thủ cùng CLB; các ngoại lệ được ghi từng đội. Không dùng Fernandinho LWF trùng tên để giả tiền vệ Man City, không dùng Albert Ferrer RB đá CB. Liverpool giữ Coutinho, PSG giữ Ibrahimović, Chelsea giữ Costa theo xác nhận ưu tiên của bạn dù pha trộn mùa.

Toàn bộ12 đội trỏ logo và kit về CLB gốc trong game. Đặc biệt Tottenham/Liverpool/Barcelona/Atletico được sửa cả block uniform native, đường texture và uniform ID trong START. Dùng bộ áo hiện có của bản game, không phải texture áo đúng năm2017/2018/2020. Logo gốc có thể vẫn là logo chung nếu bản game thiếu bản có bản quyền; không tự tạo logo thay thế. Phần render chưa kiểm chứng trên máy thật.

## OVR và kỹ năng

- OVR nền theo vị trí chính của bản ghi: **87–95** ở My League, **80–86** ở giải Bỉ/AFC Nation League566. Chính sách mới thay trần Scottish89. Không ghi lại chỉ số vào DB thẻ sở hữu; cầu thủ của người chơi được chiếu lại tại START. OVR có HLV, booster và OVR khi kéo sang vị trí khác có thể khác dải nền.
- Những chỉ số thành phần cũ, kể cả Kicking Power+7, là đầu vào trước cân bằng OVR. Chúng có thể tăng/giảm thêm để đạt dải OVR mới. Riêng Messi giữ Curl94, Dribbling94 và Blitz Curler/Momentum Dribbling.
- Scottish: cộng kỹ năng theo vai trò, gồm kỹ năng chuyền/kiến tạo, rê bóng/cánh, dứt điểm, phòng ngự và phát bóng/cản penalty cho thủ môn. Chop Turn đổi Tap Trick; Marseille Turn đổi Momentum Dribbling. Giữ các skill khác, kể cả slot skill bổ sung của thẻ người chơi. Captaincy được thêm cho đội trưởng retro.
- Ligue122: hậu vệ CB/LB/RB thêm Fortress115, Sliding Tackle113, Interception106, Blocker111 bằng phép hợp, không xóa skill cũ. Kiểm tra trên14330 bản ghi và các trường hợp learned-skill.
- Không bật Power Tackle chưa có mapping đủ bằng chứng; không sửa tóc/áo tay dài từ các yêu cầu cũ trong gói này.

## Kết quả CPU Ligue122

Tỷ lệ giữ như trước: nhóm1 gặp nhóm2 thắng70%, riêng Barcelona–Real cân bằng; nhóm1 gặp nhóm cuối90%, nhóm đầu gặp nhóm3 là85%; nhóm2 gặp nhóm cuối95%. Chênh lệch sân nhà/khách của các đội khó chịu vẫn được giữ. V7 thay đổi trọng số giữa các kiểu thắng sát nút, bế tắc, hiệu quả dứt điểm và thắng cách biệt, vẫn giới hạn tỷ số hợp lý. Không sửa kết quả đã chốt hoặc trận bạn trực tiếp đá; không giả phút ghi bàn hay cách pressing.

## Sân và thời tiết — có giới hạn chưa hoàn thành

Whitelist sân: Giuseppe Meazza1, Old Trafford7, San Siro30, Signal Iduna Park51, Emirates52, Camp Nou85. Hook lựa chọn chỉ chọn trong số sân engine xác nhận đã cài/selectable; khi có sân phù hợp sẽ bỏ eFootball Stadium100. Chỉ mục hay tên sân trong DB không tạo ra gói sân3D.

**Nếu máy chưa có bất kỳ sân nào trong whitelist hoặc hook môi trường chưa cài được, v7 giữ selector gốc để trận vẫn chạy. Vì vậy chưa thể cam kết loại100 hoàn toàn trên mọi máy.** Kiểm tra `myleague-environment-status.json` để biết `stadium_applied`, `available_stadium_ids`, `requested_stadium_id` và lỗi hook nếu có. Không đưa ID sân thiếu tài nguyên vào trận để rồi gây màn hình đen hoặc lỗi mạng.

Cấu hình trận bốc thời tiết, mùa và ngày/đêm theo mùa giải+vòng; mở lại menu hoặc retry không bốc lại. Vòng8–14 yêu cầu mùa đông+tuyết. **Bảng Stadium.bin bản gốc lẫn dt870 hiện có đặt cờ hỗ trợ tuyết bằng0 ở cả sáu sân.** Engine còn kiểm tra IsSnowPossible. V7 chỉ dùng SNOW nếu engine thực tế xác nhận hỗ trợ; nếu không, ghi `requested_weather: WEATHER_TYPE_SNOW`, chuyển về trời quang và `snow_applied:false`, giữ yêu cầu mùa đông. Tuyết rơi thực sự hiện **chưa áp dụng được với nguồn sân đã kiểm tra**. Không giả bật bằng cách sửa enum hoặc ghi đè cờ capability.

Mưa, mùa đông và ngày/đêm có giá trị schema hợp lệ, nhưng hiệu ứng hình ảnh còn phụ thuộc gói sân và engine Android; chưa xác minh render. `CONFIGURED_NOT_DEVICE_VERIFIED` chỉ là đã đặt cấu hình; `PARTIAL_ASSETS_OR_EFFECTS_PENDING` nghĩa là sân hoặc hiệu ứng đang thiếu. Không hiểu các trạng thái này là đã chạy mưa/tuyết trên điện thoại.

## Kiểm tra đã thực hiện

Hàm ARM64 gốc trên dữ liệu giả lập: full64 ID,18 roster,12 đội hình x4 biến thể, số áo, captain/taker, alias logo/kit, OVR chuyển ngữ cảnh và hook sân. Gateway thật trên DB dùng một lần: chọn đội/prepare/START, dải OVR của cầu thủ, uniform donor, thời tiết giữ ổn định và fallback không gây lỗi khi thiếu sân/tuyết. Kiểm tra14330 thẻ thật và mô phỏng80000 trận CPU. Không có kiểm thử vào trận/render trên điện thoại trong môi trường này.
