# Native hotfix v8 — Scottish, kit, OVR và sân nhà

Bản này tiếp nối v7.1, thêm đường cập nhật bản sao Team đang dùng khi chuẩn bị trận. Đây là thay đổi cần kiểm tra trên điện thoại; kiểm thử ARM64/gateway không thay thế kiểm tra hình ảnh và vào trận thật.

## Cài bằng MT Manager

1. Buộc dừng efootxi trước khi thay file.
2. Sao lưu 7 file đang chạy trong `73efootball 资源/files/embedded-gateway/work/tools/`.
3. Giải nén ZIP, chép đè đủ **7 file** trong `install/work/tools/` vào đúng thư mục trên: `gateway_runtime.py`, `select_team_runtime.py`, `libselect_team.so`, `myleague_realism.py`, `myleague_worlds.py`, `myleague_balance.py`, `myleague_custom.json`.
4. Mở lại game. `select-team-status.json` phải ghi `version: native-hotfix-v8`, `state: HOOK_ACTIVE`; `presentation_error` và `environment_error` nên là `null`, `ovr_balance_failures` bằng0.
5. Vào Scottish, xem Real Madrid và Manchester City, sau đó thử trận với hai đội này. `cached_team_applies` tăng khi game đọc bản sao đội bóng cần cập nhật. Đối chiếu [danh sách đội hình](DOI_HINH_CO_DIEN.md).

Không thay dt200, CPK, APK hoặc DB. ZIP không chứa dữ liệu tài khoản. Không cần xóa save hoặc bắt đầu lại mùa để thử; kết quả các trận đã đá được giữ. Muốn quay lại, buộc dừng app rồi chép đè đủ7 file đã sao lưu của v7.1.

## Những thay đổi của Scottish

- Tên12 đội bỏ năm phía sau. 186 vị trí dùng176 ID thật từ nguồn Android; không tạo cầu thủ giả tên huyền thoại bị thiếu.
- Real: RonaldoLWF, BenzemaCF, BaleRWF; CarvajalRB, VaraneCB. Ramosđội trưởng; Ronaldođápenalty/phạtxa/phạtgần; Kroosđácảhai góc.
- Roma: bỏSalah, đưaCandreva vào; TottiCF, ElShaarawyRMF. Candreva ở cánh trái trong sơ đồ này, DzekoSS hỗ trợ Totti.
- Juve: bỏInzaghi/Nedved, đưaBentancur/Vidal từ dự bị lên. City: Gündoğan thayYaya, KompanyCB/WalkerRB, AgüeroCF/SilvaAMF/SanéRMF.
- Barça: NeymarLWF/SuárezCF. Liverpool: VanDijkCB/TrentRB. PSG: CavaniLWF/IbraCF/DiMariaRWF/DraxlerAMF.
- Tottenham: LucasRMF/EriksenAMF/KaneCF, bỏWalker, đưaDierCB lên và dùng ba trung vệ; DaviesLMF. Không gánDier làmRB để thế chỗ một cách máy móc.
- Số áo duy nhất trong mỗi đội; captain và sáu người thực hiện bóng chết được tính lại theo ID, sau mọi thay người. Các ngoại lệ lịch sử/cầu thủ nguồn được ghi ở danh sách chi tiết.
- RiêngScottish: toàn bộ12 vị trí ngoài sân đạt mức thông thạo đầy đủ; cầu thủ ngoài sân không được cấpGK. Thủ môn giữ độ thông thạoGK vốn có. Không áp dụng thay đổi này cho giải khác.

## OVR và kỹ năng

OVR **nền trung lập**, tính bằng công thức engine gốc tại vị trí chính được bố trí: mặc định90; nhóm ngôi sao bạn liệt kê92–94; Ronaldo96 vàMessi97. Việc bốc giá trị cố định theo ID giúp đọc lại menu không đổi OVR. OVR khi cóHLV/booster hoặc khi đổi vị trí có thể khác giá trị nền.

Ronaldo/Messi giữ Dribbling, BallControl, TightPossession, Finishing, Acceleration vàSpeed từ90 trở lên. Cả hai cóMomentumDribbling; Ronaldo thêmBulletHeader/SnapStrike/DippingShot/KnuckleShot, Messi thêmBlitzCurler/MagneticFeet/EdgeCrossing và giữCurl94/Dribbling94.

Kỹ năng theo phong cách/vai trò được cộng thêm, không xóa các kỹ năng khác. Scottish tiếp tục đổiChopTurn thànhTapTrick, MarseilleTurn thànhMomentumDribbling; các ô kỹ năng học thêm bị bỏ giữ vị trí trống74, không dồn làm mất ô khác. Không bậtPowerTackle chưa có mapping xác minh. GiảiBỉ vẫn OVR80–86, cácMyLeague khác87–95; logic kết quảLigue122 và các card chỉnh riêng trước đây được giữ.

## Sửa đường đọc đội hình và kit

DBTeam và bản saoTeam dùng cho trận là hai đối tượng khác nhau. Bản cũ chỉ sửaDBTeam nên bản sao đang lưu có thể còn đội hình/kit cũ. V8 cập nhật hai accessor của bản sao, kiểm tra đầy đủ ID trước khi ghi, rồi sửa vai trò/tọa độ, thứ tự, số áo, captain/taker và blockkit. Bộ nhớ đã đúng được bỏ qua; nếu game chép lại dữ liệu cũ tại cùng địa chỉ thì bản vá phát hiện và sửa lại.

Hàm3a5586c trước đây gọi làkitpath thực ra chỉ trả màu áo. V8 thêm alias ở bộ phân giải resource team ID82446d8, được các bộ dựng áo3D68fe7a4/697a1b4 dùng để tạo tênu0173p1 choManCity, u0108p1 choBarça... Đồng thời giữ uniform IDs trongSTART và blockuniform cùng trỏ đúng CLB gốc. Bản vá dùng **áo hiện tại có sẵn của CLB trong bản game**, không nhập áo lịch sử mới. Trong các container đã cung cấp, tìm thấy textureBarça/PSG nhưng chưa tìm thấyu0173 (ManCity), u0179 (Tottenham), u0172 (Atlético). Vì vậy bản này sửa được đường chọn và bản sao dữ liệu kit; chưa thể cam kết áo3D chuẩn của ba đội nếu máy không có gói texture tương ứng. Hình ảnh áo cuối cùng vẫn cần bạn kiểm tra trên máy.

## Sân nhà và thời tiết

76đội của Scottish518, Ligue122, Belgium566, Portugal128, Danish549 có sân nhà được chọn ổn định theo ID từ:

- st001GiuseppeMeazza; st007OldTrafford; st030SanSiro;
- st051SignalIdunaPark; st052Emirates; st085SpotifyCampNou.

NativeTeam.home_stadium được ghi đúng bitfield; bản saoTeam cũng được cập nhật. Mỗi trận dùng sân của đội chủ nhà thật trong lịch, không lấy sân của người chơi khi đá sân khách. Hai bộ chọn sân của game trả ID được phân bổ; không trả sân mặc định100 khi ngữ cảnhMyLeague đã chuẩn bị.

**V8 không gọi lại accessor sân không có đối tượng từng làm v7 crash.** Gateway chỉ gửiCID/ID vào setter nguyên tử, không truy vấn đối tượngUE. Hai selector là member hook do game gọi; ngoàiMyLeague chúng chuyển tiếp nguyên con trỏthis về hàm gốc. Đã tái hiện lỗi v7 và kiểm tra đường mới không đọc0x28.

`myleague-environment-status.json` ghi `HOME_STADIUM_ASSIGNED_WEATHER_ENUMS`, `home_team_id`, `stadium_id`, `season_type`, `time_zone`. `select-team-status.json.selected_stadium` ghi sân đang được chọn sau khi mở thông tin mùa/chuẩn bị trận. Bộ nạp tài nguyên sân vẫn là của game gốc; việc máy có đủ các gói3D của sáu sân chưa được kiểm chứng trong môi trường này.

Cấu hình mùa hè/mùa đông và ngày/đêm được chọn ổn định cho từng vòng, giữ nguyên khi thử lại. Vòng8–14 luôn gửi mùa đông. **Mưa và tuyết chưa bật**: sáu bản ghiStadium.bin được cung cấp đều báo khả năng tương ứng bằng0. `snow_applied:false` là đúng, không phải báo đã có tuyết khi engine chưa hỗ trợ. Hiệu ứng mùa/ánh sáng thực tế cần kiểm tra trên điện thoại.

## Bằng chứng kiểm tra

MãARM64 gốc được chạy trongUnicorn với DB giả lập:18roster,12đội x4biến thể, bản saoTeam cũ trên cả hai phía sân, bộ đọc vị trí trận82bfb2c, ID64bit/số áo/vai trò, alias resourcekit, sân nhà76đội và phạm viOVR. Có kiểm tra công thức trên14330thẻ thật, gateway chọn đội/mởMyLeague/prepare/START trên DB dùng một lần và bảo toàn dữ liệu gốc. Các báo cáo nêu rõ phần giả lập/stub; chưa có kiểm thửAndroid/render trên điện thoại.
