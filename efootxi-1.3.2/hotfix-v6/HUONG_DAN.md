# Native hotfix v6 — kết quả Super League, cầu thủ và Scottish cổ điển

**V6 chưa thử trên điện thoại.** Đã kiểm tra các thành phần ARM64 bằng hàm tra cứu/getter/setter gốc trên DB tổng hợp, gateway trên bản sao seed DB và mô phỏng. Kiểm tra gateway dùng cầu nối native giả lập; không phải thử trận thực. Gói giữ cơ chế Bayern127 đã chạy được ở v4.1, mở rộng hỗ trợ ID thẻ64 bit cho đội cổ điển.

## Cài bằng MT Manager

1. Buộc dừng game, sao lưu sáu file tools đang dùng và save/gateway.
2. Giải nén ZIP. Chép đè **đủ sáu file** trong `install/work/tools/` vào nơi đã dùng: `73efootball 资源` → `files/embedded-gateway/work/tools`.
3. Bộ gồm `gateway_runtime.py`, `select_team_runtime.py`, `libselect_team.so`, `myleague_realism.py`, `myleague_worlds.py`, `myleague_custom.json`. Không thay riêng JSON hoặc trộn binary cũ.
4. Mở lại game; `select-team-status.json` phải có `version: native-hotfix-v6`, `state: HOOK_ACTIVE`; `myleague-realism-status.json` phải có `state: INSTALLED`, cùng version.
5. `presentation_error:null` nghĩa là các hook tên/logo/kit đã cài, chưa chứng minh render/texture trên máy bạn. `native_team_results` giờ có18 ID đội. Mã1 là preflight roster đạt; chưa chứng minh trận đã tải thành công.
6. Thử trận Bayern hiện đại127 trước. Sau đó mở Scottish Premiership để kiểm tra tên12 đội cổ điển, đội hình, áo đấu và thử trận. Có thể kiểm tra roster trong mùa Scottish hiện có; không cần xóa save.

Nếu lỗi, gửi toàn bộ `select-team-status.json` và `myleague-native-error.json` nếu có, kèm bước gặp lỗi. Trường mới `native_last_player_full_id` giữ đủ ID thẻ; trường cũ có thể chỉ hiện low32. Không thay dt200/CPK/APK/manifest hay DB để thử bản này.

## Kết quả Super League / UEFA Champions League122

Giữ18 CLB, Dortmund126 thay Lyon. Nhóm1 Arsenal/PSG/Barcelona; nhóm2 Real/City/Bayern; nhóm3 Liverpool/Inter/Atletico/Chelsea/Milan/Juventus; nhóm4 Tottenham/Galatasaray/Napoli/Dortmund/Roma/MU.

| Cặp đấu CPU | Thắng / Hòa / Thua từ phía đội mạnh |
|---|---|
| Nhóm1 gặp nhóm2, trừ El Clasico | 70% /20% /10% |
| Nhóm1 gặp nhóm4 | 90% /7% /3% |
| Nhóm1/2 gặp nhóm3 | Giữ85% /10% /5% từ yêu cầu trước |
| Nhóm2 gặp nhóm4 | Giữ95% /4% /1% từ yêu cầu trước |
| Barcelona–Real Madrid | Cân bằng hai bên, có hòa; phong độ và sân nhà tác động |

Theo xác nhận của bạn, El Clasico là ngoại lệ của70%. Các tỷ lệ là xác suất trên nhiều trận, không bảo đảm một chuỗi ngắn. Với Roma/Dortmund/Gala/Napoli, cửa ngáng đường ông lớn tăng khi họ đá sân nhà và giảm ở lượt sân khách; trung bình hai chiều sân vẫn giữ tỷ lệ đã cấu hình. Roma/Dortmund còn có lợi thế sân nhà ở các cặp dưới nhóm đầu. MU yếu nhất, thường chịu cách biệt lớn hơn khi thua.

Tỷ số và thắng/hòa/thua được chọn riêng. Đại chiến nhóm đầu và El Clasico dùng0–0,1–1,1–0,2–1,2–0,3–1. Đội mạnh gặp đội dưới có cả1–0/2–0,2–1,3–0/3–1,4–0; cú sốc thường1–0 hoặc2–1 từ phía đội yếu. **Không sinh7–4 hay4–2 trong mô phỏng giải122.** Giới hạn mới không cắt hay sửa tỷ số trận bạn đã đá/chốt, và không thay mô hình các giải khác.

Chỉ điều khiển kết quả CPU. Không giả lập pressing, phạt đền hay thời điểm ghi bàn trong trận thật. Giao thức kết quả CPU hiện không có phút bàn thắng, nên chưa triển khai yêu cầu MU thủng lưới phút cuối như một sự kiện có thời gian.

## Card105820209653455, luật chung và số áo Bayern hiện đại

Fabián Ruiz105820209653455: Acceleration88, Speed88, Tackling90, Defensive Awareness90. Giữ toàn bộ20 Card ID đã cấu hình, gồm các yêu cầu cũ.

- Kicking Power **>84**: +7, ví dụ85→92,94→101. Đúng84 không cộng. Giới hạn127 theo trường packed7 bit; không tự cắt xuống99. Native ghi cùng giá trị đích qua nhiều lần lookup. Python lấy dữ liệu DB gốc cho từng phản hồi, giữ khác biệt giữa các serial và cập nhật huấn luyện sau đó; không ghi thêm7 vào save.
- Tiền vệ/tiền đạo (DMF/CMF/LMF/RMF/AMF/LWF/RWF/SS/CF): thêm Dipping Shot **khi không có cả Low Screamer lẫn Blitz Curler**. Kiểm tra cả skill có sẵn và skill học thêm trên thẻ sở hữu. Có sẵn một trong hai thì không thêm theo luật này; không xóa Dipping Shot vốn có.
- Bayern127: Kane9, Díaz14, Olise17, Musiala10. Giữ22 người, Musiala giữa/Olise phải/Díaz trái. Không đưa lại ID59835 từng gây lỗi.

Các luật+4 hậu vệ, +6 chuyền dưới84, thay đổi20 thẻ và các Base trước đây được giữ. Kỹ năng Power Tackle từ yêu cầu cũ vẫn chưa gán vì chưa xác minh flag riêng.

## Scottish Premiership518 —12 CLB cổ điển

Bạn đã chọn **dùng người thay tạm** cho những vị trí thiếu dữ liệu, và tự xử lý số áo trùng. Bản này có175 vị trí, dùng128 vị trí đã tìm được trong nguồn và47 chỗ thay tạm; tổng172 ID khác nhau do có người xuất hiện ở hai CLB.

Xem **[toàn bộ đội hình, người thay, số áo và ID](DOI_HINH_CO_DIEN.md)**; máy đọc được ở `classic-replacements.json`. Không đổi tên/face của người thay để giả thành cầu thủ thiếu. Ví dụ Demichelis thay Boateng, Gnabry thay Robben, Guti thay Zidane, Zamorano thay Raúl; Xabi Alonso vào ôCMF thay Hierro/Clayton. Các ID Messi17592722922839, Suárez88044145248321, Neymar88044145253792, Kaká88045755829934, Pato88038776539586, Rooney88039044943928, Totti88045755960771 được giữ nguyên.

| Đội gốc / ID | Tên mới |
|---|---|
| Falkirk5317 | Bayern Munchen |
| Hibernian1222 | FC Barcelona |
| Dundee United1220 | Real Madrid CF |
| Motherwell1986 | PSG |
| Aberdeen1219 | AC Milan |
| Rangers132 | Man United |
| Celtic131 | Man City |
| St Johnstone2365 | Juventus |
| St Mirren1987 | Liverpool FC |
| Hearts1221 | Chelsea FC |
| Dundee2621 | AS Roma |
| Kilmarnock1985 | Inter Milan |

Giữ nguyên12 ID đội và lịch22 vòng của gói Android đang có; không tự thêm vòng chia nhóm hay đổi thể thức Scottish. Mỗi đội dùng đúng11 người đầu theo yêu cầu và dự bị đã liệt kê. Vị trí/tọa độ được đặt vào bốn biến thể formation native, cùng thứ tự cầu thủ để không chỉ thay danh sách rồi để engine gán nhầm ô. RB/LB và RWB/LWB được biểu diễn bằng các vai native có sẵn; RWB/LWB của Chelsea dùngRMF/LMF trong sơ đồ3 hậu vệ.

Theo yêu cầu cụ thể, Motherwell/PSG, Celtic/City và St Mirren/Liverpool lấy logo và áo đấu từ PSG114, City173, Liverpool103. Sao chép đúng80 byte định nghĩa uniform đã xác minh, đồng thời alias đường texture theo CLB gốc. Không sao chép đè cả record đội. Các đội khác được đổi tên/đội hình; không tuyên bố có áo cổ điển theo mùa hay logo đã thay nếu chưa yêu cầu/kiểm tra.

## OVR và skill cổ điển — chỉ hồ sơ NPC Scottish

Trần tính bằng công thức OVR gốc và trọng số đối chiếu đúng libUE4 hiện tại. Sau +7 Kicking Power và gán skill/vị trí, giảm đều các chỉ số thể thao/kỹ thuật còn lại cho tới khi **OVR nền≤89 ở cả13 vị trí**; giữ chiều cao, chân thuận/yếu, proficiency và mức Kicking Power đã cộng. Không chỉ sửa con số OVR hiển thị. Native giữ snapshot kết quả cho từng ID, không giảm thêm mỗi lần tra cứu.

Đây là trần OVR nền của NPC, không sửa chỉ số lưu/serial thẻ đang sở hữu. Boost HLV, booster điều kiện hoặc cách UI thực tế hiển thị cần xác nhận trên điện thoại; không coi kiểm tra OVR nền là bằng chứng mọi giá trị có boost trong trận đều≤89.

Tất cả hồ sơ cổ điển tắt Marseille Turn. Messi17592722922839 có Blitz Curler và Momentum Dribbling. Giữ kỹ năng gốc còn lại, thêm nhóm kỹ năng theo vai/phong cách: hậu vệ Interception/Long-Reach Tackle, CB Fortress; biên Edge Crossing; kiến thiết Phenomenal Pass/Visionary Pass; rê dắt Momentum/Acceleration Burst/Tap Trick; một số chân sút Low Screamer/Knuckle Shot/Snap Strike/Attack Trigger. **Attack Trigger đã xác minh flag128 trên28 thẻ nguồn**, Phenomenal Passing122 trên163 thẻ, Fortress115 trên119 thẻ. Không dùng tên skill để đoán flag.

## Kiểm tra và khôi phục

Có báo cáo đi kèm: native roster18 đội/full64 IDs/áo/formation/OVR/đồng bộ repeated lookup; preflight từ chối cầu thủ thiếu;20 Card ID qua handler thật;390 trường hợp luật chung;80.000 trận CPU;12 đội Scottish chọn/prepare/START với bridge giả lập; ranking không tạo cầu thủ ngoài roster; hồi quy save/inventory; Asia-Pacific8 đội21 vòng vẫn hoạt động ở bài gateway. Tên/logo/kit kiểm tra đường hàm và allocator/X8, chưa chạy renderer thật.

Giữ Asia-Pacific ở Danish549,8 đội3 lượt; Eredivisie125 đã khôi phục18 đội Hà Lan. Mùa đã lưu giữ snapshot/kết quả cũ. Tóc/áo dài từ yêu cầu cũ chưa áp dụng. Khôi phục bằng bộ sáu file đã sao lưu sau khi buộc dừng; không xóa save để thử.
