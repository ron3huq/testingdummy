# Native hotfix v9

Bản cập nhật theo yêu cầu mới: phục hồi độ thông thạo vị trí gốc, thay thứ tự cầu thủ theo các ô đang hiển thị trên máy, gán lại đội trưởng/penalty, sửa các đường tên giải và cấu hình bốn điều kiện thời tiết.

## Cài bằng MT Manager

1. Buộc dừng efootxi.
2. Sao lưu đủ 7 file đang dùng trong `73efootball 资源/files/embedded-gateway/work/tools/`.
3. Giải nén ZIP, chép đè đủ **7 file** từ `install/work/tools/` vào đúng thư mục trên: `gateway_runtime.py`, `select_team_runtime.py`, `libselect_team.so`, `myleague_realism.py`, `myleague_worlds.py`, `myleague_balance.py`, `myleague_custom.json`.
4. Mở game và đọc `select-team-status.json`: version phải là `native-hotfix-v9`, state `HOOK_ACTIVE`, `presentation_error` và `environment_error` là `null`, `ovr_balance_failures` là 0.
5. Vào My League, kiểm tra tên giải, Real/Barça/City, đội trưởng và penalty. Thử bốn vòng liên tiếp để quan sát bốn cấu hình thời tiết.

Không thay dt200/CPK/APK/DB, không xóa dữ liệu lưu hoặc bắt đầu lại mùa để thử. Nếu cần quay lại bản đang dùng trước khi cập nhật, buộc dừng app rồi khôi phục đủ 7 file đã sao lưu. Không trộn file giữa các phiên bản vì có kiểm tra hash.

## Thông thạo vị trí

**Đã gỡ hoàn toàn tính năng thông thạo mọi vị trí.** Bản vá giữ nguyên vị trí chính và 13 trường độ thông thạo từ dữ liệu nguồn, bao gồm GK. Cầu thủ sở hữu giữ dữ liệu thông thạo hiện có của chính thẻ đó; không cấp thêm hoặc xóa độ thông thạo đã luyện trước đây. Việc gán vị trí trong đội hình được thực hiện bằng đội hình/thứ tự cầu thủ, không bằng cách sửa độ thông thạo.

OVR và các chỉ số/kỹ năng ở bản trước vẫn được giữ: OVR nền Scottish mặc định 90, ngôi sao 92–94, Ronaldo 96/Messi 97. OVR được tính tại vị trí chính gốc; khi đặt cầu thủ sang vị trí khác hoặc có HLV/booster, OVR hiển thị có thể khác.

## Đội hình và vai trò

V8 đã ghi vị trí nhưng trên điện thoại vẫn lệch. V9 thay **thứ tự roster cùng với formation và các tham chiếu theo ID**, dựa trên chính các ô vị trí bạn báo. Không chỉ thay chữ LWF/CF trong cấu hình. Captain và người đá bóng chết được tính lại sau khi đảo thứ tự.

- Real: Ronaldo LWF, Benzema CF, Bale RWF; Carvajal RB, Varane CB.
- Barça: Neymar LWF, Suárez CF; Sergi Roberto RB, Umtiti CB.
- Bayern: Kimmich RB, Hummels CB.
- City: Agüero CF, Silva AMF, Sané RMF; Kompany CB, Walker RB. **Ederson bắt chính**, Bravo xuống dự bị.
- Liverpool: Coutinho AMF, Firmino CF; Van Dijk CB, Trent RB.
- PSG: Ibrahimović CF, Cavani LWF; Draxler AMF, Di María RWF; Dani Alves RB, Marquinhos CB.
- Tottenham: Kane CF, Lucas Moura RMF, Eriksen AMF.

Đội trưởng/penalty của cả 12 đội theo danh sách mới, xem bảng chi tiết trong [DOI_HINH_CO_DIEN.md](DOI_HINH_CO_DIEN.md). Tất cả số áo được đối chiếu theo ID và không trùng trong một đội. Liverpool dùng Coutinho #10 và Mané #19, là các số cả hai từng mang tại Liverpool, thay số #18 gán tạm cho Coutinho.

Các đội retro vẫn pha trộn thời kỳ do thiếu một số cầu thủ trong nguồn. Những trường hợp trùng số giữa các thời kỳ vẫn dùng số thay thế đã được bạn cho phép trước đây: ví dụ Griezmann/Forlán cùng có số gốc #7, Pirlo/Thuram cùng #21. Không thể coi toàn bộ đội pha trộn là một đội hình lịch sử tuyệt đối chính xác của cùng một mùa.

## Năm tên giải

| Giải gốc | Tên mới |
|---|---|
| Scottish Premiership (518) | Y17 Champion League |
| Danish League (549) | Asia-Pacific League |
| Ligue 1 McDonald's (122) | Uefa Champion League |
| Liga Portugal Betclic (128) | World Nation League |
| Belgian League (566) | AFC Nation League |

Bản cũ chỉ chặn GetCompetitionName thông thường. Giao diện còn các đường `GetCompeNameAllCaps`, `GetLeagueKnockoutNameAllCaps`, `GetCompeNameAllAllCaps` với ABI khác, cùng trường tên trong native competition record. V9 bổ sung các đường này và cập nhật registry gateway. Không thêm trường tên giả vào phản hồi không có schema. ID giải và tiến trình mùa được giữ.

`competition_name_applies` trong `select-team-status.json` tăng khi các đường tên mới được dùng. Kiểm thử có kiểm tra entry detour, FString tái sử dụng, con trỏ/kích thước bộ đệm và đường gốc của giải không đổi tên. Kết quả trên giao diện Android vẫn cần bạn xác nhận.

## Sân nhà và thời tiết

76 đội của năm giải trên có sân nhà được phân bổ ổn định từ `st001`, `st007`, `st030`, `st051`, `st052`, `st085`. Đá sân khách dùng sân của đội chủ nhà trong lịch. Hai selector My League đã chuẩn bị trả về ID được phân bổ, không trả sân mặc định 100. Không gọi lại accessor sai kiểu từng gây crash v7; gateway chỉ ghi setter nguyên tử, không dò đối tượng UE.

Thời tiết xoay vòng qua bốn cấu hình:

1. Ban ngày, trời quang.
2. Ban ngày, trời mưa.
3. Ban đêm, trời mưa.
4. Ban đêm, trời quang.

Mỗi mùa có điểm bắt đầu chu kỳ riêng; xem lại menu hoặc thử lại cùng vòng không bốc lại thời tiết/sân. Mỗi bốn vòng liên tiếp có đủ bốn trạng thái. Giữ mùa đông ở vòng 8–14 theo cấu hình trước; **không yêu cầu tuyết**.

Nguồn gốc báo cờ khả năng bằng 0. V9 bật đúng native parameter **9 (IsNightPossible)** và **10 (IsRainPossible)** cho sáu sân được chọn trong năm giải. Không sửa các trường khác, không ghi lại Stadium.bin, không bật snow parameter 11 hoặc đổi sân ngoài danh sách.

`myleague-environment-status.json` ghi `weather`, `time_zone`, `season_type`, `stadium_id` và `home_team_id`. `selected_stadium` trong status chính ghi ID đang được selector chọn. Cấu hình mưa và kiểm tra cho phép mưa đã bật; **hình ảnh mưa, ánh sáng và tải tài nguyên sân chưa được kiểm chứng trên điện thoại**, nên không báo là đã thấy hiệu ứng thực tế.

## Kiểm tra và giới hạn

- 14.330 thẻ nguồn: các trường vị trí/thông thạo giữ nguyên, OVR và kỹ năng giữ phạm vi.
- Mã ARM64 gốc trong Unicorn: roster, 4 biến thể đội hình, số áo, captain/taker, bản sao Team trên cả hai phía sân và các detour mới.
- Hợp đồng vị trí độc lập lấy từ những ô bạn báo; đội trưởng và penalty được so tên thật theo ID, không chỉ kiểm tra số thứ tự do bộ tạo sinh ra.
- 55 trường hợp tên UI/native, 1.365 trường hợp tham số sân; bốn cấu hình thời tiết trên cả năm giải.
- Gateway thật trên DB dùng một lần: chọn đội, mở My League, prepare, START và bảo toàn dữ liệu mùa/kho cầu thủ.

Đây vẫn là kiểm tra mã/gateway, chưa chạy game Android/render trên thiết bị. Áo đấu không được nhập mới trong v9; giới hạn thiếu texture Man City/Tottenham/Atlético của nguồn v8 vẫn còn. Cần kiểm tra trực tiếp tên giải, vị trí và hiệu ứng sau khi cài; các báo cáo ghi rõ phần giả lập và stub.
