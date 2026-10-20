> **V4 CÒN LỖI BAYERN59835:** log Android xác nhận127:13/reason2. ID59835 đã bị cắt từ thẻ52776558193083. Xem [bản thử v4.1](../hotfix-v4.1/HUONG_DAN.md), Bayern22, giữ nguyên11 người chính; chưa thử trận trên điện thoại.

# Native hotfix v4 — Bayern To Match, Card ID, AjaxE và ba giải

**Bản mới chưa thử trên điện thoại.** Đã kiểm tra thành phần ARM64, gateway trên bản sao DB và mô phỏng. Người dùng xác nhận v3 không còn văng ở To Match nhưng báo C_RTMC_9999; log v3 có `127:13`, `native_last_player_error:33185` (Neuer). V4 sửa nguyên nhân từ mã và log đó; cần thử trận Bayern trên Android để xác nhận toàn bộ đường vào trận.

## Cài trên máy không root

1. Buộc dừng game. Sao lưu sáu file tools hiện tại và save/gateway trước khi cập nhật. Nếu có trận khác đang đá, hoàn tất trận trước khi thay roster.
2. Giải nén ZIP. Trong MT Manager vào đúng vùng nội bộ đã cài Select Team thành công: `73efootball 资源` → `files/embedded-gateway/work/tools`.
3. Chép đè **cùng bộ sáu file** từ `install/work/tools/`: `gateway_runtime.py`, `select_team_runtime.py`, `libselect_team.so`, `myleague_realism.py`, `myleague_worlds.py`, `myleague_custom.json`.
4. Giữ dt200 gốc đang chạy được, APK, manifest và DB hiện tại. Không ký lại APK, không chép sang Android/data, không thay save bằng DB seed.
5. Mở game. `select-team-status.json` cần có `version:native-hotfix-v4`, `state:HOOK_ACTIVE`; `myleague-realism-status.json` cần `state:INSTALLED`, `version:native-hotfix-v4`. Nếu còn ghi v3, kiểm tra đúng thư mục/sáu file và buộc dừng mở lại.
6. **Thử To Match với Bayern ngay ở mùa hiện tại.** Không cần xóa mùa để thử sửa lỗi. Sau khi chuẩn bị, `native_team_results["127"]` cần là `1`. Điều này chứng minh kiểm tra roster đã đạt, chưa chứng minh trận đã tải và đá được.
7. Để có thành phần Eredivisie mới và lịch bốc mới, bắt đầu mùa mới bằng chức năng trong game. Mùa đang chơi giữ snapshot/lịch/kết quả cũ. Chỉ số/skill và chính sách CPU mới áp dụng sau khởi động lại; không viết lại kết quả/vua phá lưới đã chốt.

Nếu vẫn lỗi, lấy `select-team-status.json`, `myleague-realism-status.json`, `myleague-native-error.json` nếu có; phân biệt lỗi tại To Match, sau Bắt đầu hay đang tải sân. Nếu văng cần thêm log crash Android. Không khẳng định đổi mạng sẽ giải quyết lỗi gateway này.

## Nguyên nhân và bản sửa Bayern

Trong v3, hàm `0x823cfd0` nhận ID32 nhưng trả về một họ bản ghi khác, không phải cầu thủ. Hàm cầu thủ đúng là `0x823c8d4`, nhận khóa 16 byte `(kind, raw ID)` qua X1/X2. Ngoài ra raw ID lưu ở `player+0x40` đã được bảo vệ XOR, không thể so trực tiếp với ID thường. V4 dùng getter gốc `0x68fe720` để giải mã rồi kiểm tra.

Gateway v3 trả lỗi khi kiểm tra giả đó thất bại, khiến game hiển thị Network Error. V4 sửa hàm và cách đọc ID; **giữ kiểm tra dữ liệu, không ép NOERR để vượt qua đội hình lỗi**. Bayern vẫn là München RW ID127 với roster native23 người, không dùng Monaco giả hay đội hình CPU inline v2.

V4 đã chạy hàm tra cứu gốc, native lower_bound, getter ID với khóa XOR khác0, detour/trampoline thật và các getter/setter packed parameter. Bản ghi DB native trong bài kiểm tra được dựng tổng hợp; đây không phải bản chụp RAM điện thoại. Bài kiểm tra v3 dùng stub tra cứu nên đã bỏ sót lỗi này; kiểm tra v4 thay thế stub ở phần tra cứu cầu thủ bằng mã gốc của engine.

Mã roster: `1` đạt; `10` hook/context chưa sẵn sàng; `11` sai bản ghi đội/hook; `12` số người không hợp lệ; `13` không xác minh được cầu thủ; `14` khóa roster khác kiểu base. Khi `13`, `native_last_player_reason`: `1` null, `2` ID/kind không khớp, `3` vị trí không hợp lệ, `4` chiều cao không hợp lệ. `native_last_player_error` và `native_last_team_error` là lỗi cuối được ghi, có thể thuộc đội khác. `menu_calls:0` bình thường nếu tiếp tục mùa cũ mà chưa mở Select Team.

## Chỉ số và kỹ năng theo Card ID

Giữ các yêu cầu trước, cập nhật toàn bộ 16 Card ID trong tin nhắn mới; tổng cộng cấu hình đang có **18 Card ID** gồm Dembélé/Doué cũ. Xem `card_overrides` trong JSON để đối chiếu từng giá trị.

- Félix: thêm Finishing93, Kicking Power94.
- Ronaldo89138556572074: Jumping95, Speed95, Acceleration97; giữ các chỉ số đã yêu cầu trước.
- Kvaratskhelia: bỏ Marseille Turn/Double Touch, thêm Scissor Feint/Edge Crossing.
- Leão: bỏ Chop Turn/Double Touch, thêm Scissor Feint/Acceleration Burst.
- Nuno Mendes: bỏ Chop Turn/Double Touch, thêm Edge Crossing/Scissor Feint.
- Cancelo, Mané, Coman, Yamal, Raphinha, Adeyemi, hai Bale, Benzema, Marcelo và Samu Costa: các chỉ số/đổi skill đúng cấu hình yêu cầu. Coman có Pinpoint Crossing, không nhầm với Edge Crossing.

V4 đồng thời sửa ánh xạ chỉ số Android trong bản trước: Speed34, Acceleration38, Physical Contact35, Kicking Power37, Jumping39, Aggression25; Balance36 không được dùng thay Physical Contact. Đối chiếu độc lập khớp trên 200 payload nguồn. Các phép ghi chỉ số/flag native được kiểm tra bằng getter thật, giữ nguyên các field không yêu cầu.

Skill Chop Turn đối chiếu nhãn nguồn `crossOverTurn`/flag108; Scissor Feint70; Double Touch107; Marseille Turn72; Pinpoint Crossing84; Edge Crossing119; Acceleration Burst124. Bỏ cả learned skill tương ứng; ô trống dùng74 để giữ nguyên vị trí các ô còn lại. START chỉnh lần cuối sau learned-skill overlay nên skill bị bỏ không tự bật lại ở bước đó.

ID64 và serial giữ nguyên. Chỉnh tại lớp xuất LOGIN/list/detail/START và dữ liệu native base; không ghi đè thẻ trong DB. Giá trị hiển thị cuối có thể còn chịu booster/level/đội trưởng hoặc cơ chế engine. Không coi kiểm tra data là thử mọi hiệu ứng skill trên máy thật.

**Không thêm Power Tackle/Long Range Tackle**, tiếp tục theo yêu cầu đã hủy. Các skill vốn có không bị xóa chỉ vì yêu cầu thêm đã hủy.

## AjaxE và đội hình

- Ajax giữ ID116, tên native đổi AjaxE, short AJE khi bản ghi tên nguồn khớp Ajax; tên trong dữ liệu gateway cũng đổi. Không lấy danh tính Lyon thay Ajax.
- Hook đường tạo `GetTeamEmblemPath` chuyển riêng asset ID116 sang181 (Lyon). Giữ X8 trả FString và các tham số khác; không cấp phát/giải phóng chuỗi C++ bằng allocator khác. **Chưa kiểm tra logo hiển thị trên điện thoại; cache texture, lối tải khác và logo trên áo không được bảo đảm bởi hook này.** `presentation_error` khác null cho biết hook logo chưa cài được; phần sửa Bayern vẫn hoạt động độc lập.
- Bento bản CLB Saudi16906726 rời roster Al Nassr18961 sang Ajax116. Ajax32 người, Al Nassr31 người; không nhân đôi Bento ở cả hai CLB. Bản tuyển Brazil129510 và thẻ đang sở hữu khác ID giữ nguyên.
- Các thay đổi đội hình Barcelona/PSG và Bayern23 ở v3 được giữ. Mô phỏng cũng ưu tiên đúng 11 người đầu của các roster này. Cầu thủ bị thay của Barça/PSG vẫn ở dự bị, không trùng ID.
- AjaxE **không nằm trong Eredivisie mới**, vì người dùng yêu cầu thay toàn bộ18 đội giải đó. Ajax vẫn tồn tại trong dữ liệu đội bóng, không bị biến thành CLB khác. Đội bạn trực tiếp điều khiển vẫn dùng các thẻ/đội hình đã chọn.

## Kết quả mô phỏng và ba giải mới

**Chỉ sửa kết quả các trận CPU tự sinh, không điều khiển pressing, chiến thuật, phạt đền hoặc phút ghi bàn trong trận bạn tự đá.** Tên mô tả lối đá được chuyển thành sức mạnh, lợi thế sân nhà, phong độ và phân bố tỷ số. Đây là chính sách mô phỏng theo yêu cầu, không phải dữ liệu phong độ ngoài đời cập nhật trực tiếp.

**Super League122 — 18 CLB:** Arsenal, PSG, Barcelona; Real Madrid, Manchester City, Bayern; Liverpool, Inter, Atletico, Chelsea, AC Milan, Juventus; Tottenham, Galatasaray, Napoli, Lyon, Roma; MU yếu nhất. Lyon181 giữ chỗ thay Dortmund theo yêu cầu. Roma/Lyon có lợi thế sân nhà lớn hơn; Gala/Napoli/Tottenham biến động mạnh hơn và có khả năng gây bất ngờ. El Clasico cân bằng trước lợi thế sân nhà/phong độ. Bỏ quy tắc top5 bất bại97% cố định của v3.

**Liga Portugal128 — 20 tuyển:** Spain/Argentina/France/England top1, Spain nhỉnh hơn; Brazil/Portugal/Netherlands/Germany/Belgium/Italy top2; USA/Morocco/Norway top3; Croatia/Uruguay/Colombia/Mexico top4; Sweden/Senegal/Georgia cuối. Top đầu có ưu thế nhưng vẫn hòa/thua bất ngờ. Kane/Mbappé/Haaland ưu tiên vua phá lưới; Olise/Yamal có trọng số kiến tạo cao nhất.

**Eredivisie125 — 18 CLB chốt theo trả lời mới:** Al Nassr, Al Hilal, Inter Miami, **Jeonbuk/Jeonju G**, **Los Angeles FC**, **LA Galaxy**, Vissel Kobe, Gamba Osaka, Urawa Reds, Al Ahli Saudi, Buriram, FC Seoul, **Al Ittihad**, Nam Dinh, Cong An Hanoi, Bangkok United, Shanghai Port, Beijing FC.

Nhóm đầu: Al Nassr, Al Hilal, Al Ahli, Al Ittihad, Gamba, LA Galaxy, Vissel; nhóm2 Miami/LAFC/Urawa/Shanghai; nhóm3 Beijing/Seoul/Jeonbuk; nhóm cuối Bangkok/Nam Dinh/CAHN/Buriram. Jeonbuk và Buriram là cách xếp tạm cho hai vị trí chưa được chỉ định; có ghi trong JSON. Ronaldo/Messi/Son được ưu tiên bàn thắng theo đúng roster.

Theo lựa chọn **giữ roster**, không tự chuyển Lewandowski/Benzema/Mitrovic vào giải và không tạo bàn cho họ khi vắng khỏi18 roster. Các đội Al Qadsiah, Al Ain, Chicago/Seongnam không được dùng sau những lần bạn thay lựa chọn.

Belgian566 và các quy tắc70% ở nhóm giữa giữ từ yêu cầu trước. Bốn menu có18/18/20/18 đội; lịch34/34/38/34 vòng. Lịch bốc ngẫu nhiên một lần rồi giữ nguyên khi mở lại mùa.

Tỷ số dùng nhiều chế độ: thắng sát nút, trận mở, thắng đậm và hòa từ0-0 đến3-3; cùng cặp đấu có thể thay đổi qua mùa/phong độ. Không gắn lời kể giả như “phạt đền phút90” vào dữ liệu vốn không chứa sự kiện đó. Bàn/kiến tạo thuộc cầu thủ thực sự trong roster, tổng bàn cầu thủ khớp tỷ số, không cộng lại receipt khi mở menu.

## Hai yêu cầu ngoại hình chưa áp dụng

**Áo dài Ronaldo89138556572074 theo Bale88041729329832 và tóc17592186048938 theo88038776539586 chưa được sửa.** Đã tìm thấy đủ bốn Card ID trong PlayerAppearance.bin của dt870, record64 byte, nhưng chưa xác minh bit/trường riêng cho sleeve và tóc trong đường nạp Android. Các record khác nhau ở nhiều byte; chép cả record sẽ đổi cả những phần ngoại hình khác. Chưa có cơ sở dùng slot49..60 như công tắc áo/tóc.

`appearance-research.json` ghi nguồn, hash và các byte khác biệt, không chứa bản vá ngoại hình đoán. Chưa thay CPK hoặc tài nguyên face/hair; hai phần này cần tiếp tục xác định getter/bitfield và thử hiển thị trên thiết bị.

## Kiểm chứng và giới hạn

- `native-validation.json`: public player resolver + native lower_bound + XOR getter, detour/trampoline thật, các phép ghi packed field, roster, AjaxE và shim logo. DB native tổng hợp; phần logo downstream loader chưa chạy.
- `menu-validation.json`: getter ARM64 gốc qua detour cho cả4 menu; Portugal18→20 dùng bộ cấp phát/destructor engine.
- `worlds-validation.json`: gateway thật trên bản sao seed DB, chuẩn bị/START HOME và AWAY, chặn roster không đạt và cất active inline v2 cũ. Bridge readiness được stub trong bài kiểm tra gateway; không giả làm kết quả tích hợp Android.
- `card-handlers-validation.json`:18 fixture thẻ qua handler detail/bulk LOGIN và learned overlay của home_entries rồi chiếu START; giữ ID64, serial và thứ tự ô skill.
- `corpus-validation.json`: ánh xạ stat/skill đối chiếu với payload nguồn.
- `simulation-validation.json`:40 mùa mỗi giải122/128/125, tổng120 mùa; roster/goal totals và đa dạng tỷ số;10.000 seed cho các cặp đại diện.
- `regression-validation.json`: giữ lịch/snapshot cũ có Monaco,10 vòng, receipt, inventory và DB gốc.

Các script dùng dữ liệu game người dùng đã cung cấp, không được đóng gói DB/CPK vào bản tải. Có mã C và build.sh để dựng lại thư viện ARM64 bằng ziglang0.13.0. Đừng sửa native_rosters/base_overrides/thành phần giải trong JSON riêng lẻ: có pin khớp binary; phải tạo lại C/thư viện và pin tương ứng. Card overrides, tier và trọng số Python cần khởi động lại sau khi sửa.

Khôi phục: buộc dừng rồi dùng backup cá nhân đã lưu. V2 từng crash và v3 từng lỗi kiểm tra roster; không dùng chúng như một bản sửa Bayern. Khôi phục code không hoàn tác snapshot mùa đã tạo. Không xóa save để thử.
