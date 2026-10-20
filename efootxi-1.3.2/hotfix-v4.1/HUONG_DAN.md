# Native hotfix v4.1 — Bayern59835, Dembélé và tỷ lệ85%/95%

**Chưa thử trên điện thoại.** V4 đã được bạn xác nhận các menu và roster khác đạt, nhưng Bayern vẫn bị chặn ở `127:13`, `native_last_player_error:59835`, `native_last_player_reason:2`. V4.1 sửa mục roster gây lỗi này, không tắt kiểm tra dữ liệu hay ép NOERR.

## Cài bằng MT Manager

1. Buộc dừng game. Sao lưu sáu file tools đang dùng và save/gateway.
2. Giải nén ZIP, chép đè **đủ sáu file** trong `install/work/tools/` vào vùng nội bộ đã dùng: `73efootball 资源` → `files/embedded-gateway/work/tools`. Không chép sang Android/data.
3. Bộ sáu file gồm `gateway_runtime.py`, `select_team_runtime.py`, `libselect_team.so`, `myleague_realism.py`, `myleague_worlds.py`, `myleague_custom.json`. Dùng cùng bộ vì có kiểm tra hash/config; không chỉ thay JSON.
4. Giữ dt200 gốc, APK, manifest và save. Mở lại game, kiểm tra `select-team-status.json` có `version:native-hotfix-v4.1`, `state:HOOK_ACTIVE`; `myleague-realism-status.json` có `version:native-hotfix-v4.1`, `state:INSTALLED`.
5. **Thử To Match Bayern ở mùa hiện tại**, không cần xóa/tạo mùa mới. `native_team_results["127"]` cần thành `1`; sau đó thử Bắt đầu và vào trận. Mã1 chỉ là kiểm tra roster đạt, chưa chứng minh trận tải được.

Nếu còn lỗi, gửi lại toàn bộ `select-team-status.json` và `myleague-native-error.json` nếu có; ghi rõ lỗi tại To Match hay sau Bắt đầu. Nếu file vẫn ghi v4 thì game đang nạp bộ cũ hoặc chưa buộc dừng. Không lấy việc menu_calls bằng0 làm lỗi nếu bạn chỉ tiếp tục mùa đang chơi.

## Bayern: vì sao59835 không hợp lệ?

Đọc đủ8 byte ID trong Player.bin cho thấy record Guerreiro mang ID thẻ **52776558193083** (`0x30000000e9bb`). Số59835 là phần low32 của ID đó, không có record base đúng bằng59835. V4 đã chọn nhầm nó khi đọc ID32; hàm tra cứu native trả bản ghi không khớp nên chặn ở reason2. Đây là lỗi dữ liệu roster, không phải kết luận Internet bị hỏng.

V4.1 bỏ mục dự bị59835, giữ **Bayern ID127,22 người và nguyên11 người đá chính**. Không đưa thẻ tuyển Guerreiro vào đội CPU dưới một ID base giả. Còn Neuer/Urbig làm thủ môn; giữ các dự bị Kim, Pavlović, Gnabry, Jackson, Stanišić, Ito, Karl, Kusi-Asare, Boey, Wisdom Mike. Không xóa hay sửa thẻ Guerreiro đang sở hữu.

Đã đối chiếu ID64 đầy đủ của tất cả roster native chỉnh sửa và các roster CLB mô phỏng với Player.bin thực. Kiểm tra ARM64 cũng tái hiện lỗi v4 `13/reason2/59835` với record Guerreiro đầy đủ, rồi kiểm tra roster22 của v4.1 thành công bằng cùng hàm tra cứu gốc. Dữ liệu DB native trong bài kiểm tra là tổng hợp; vẫn cần xác nhận trên Android.

## Dembélé88039313485858

- Bỏ **Chop Turn**: flag108 và learned skill ID5 nếu có.
- Thêm **Tap Trick**: flag135, đối chiếu tên `tapTrick` trong payload thẻ nguồn.
- Giữ nguyên toàn bộ chỉ số đã yêu cầu trước.

Áp dụng ở LOGIN/list/detail và tham số vào trận sau learned-skill overlay; ô skill bị bỏ dùng marker74 để giữ vị trí các ô còn lại. Không ghi đè thẻ/serial trong DB. Việc ánh xạ đã kiểm tra bằng handler thật trên bản sao DB, chưa thử hiệu ứng Tap Trick trên thiết bị.

## Ligue1 / Super League: chính sách mới

Chỉ áp dụng trận CPU tự mô phỏng, không ép tỷ số trận bạn trực tiếp điều khiển. Tỷ lệ là xác suất mỗi trận; một chuỗi vài trận ngắn không nhất thiết có đúng tỷ lệ đó.

| Cặp đấu | Nhóm1–2 thắng | Hòa | Nhóm1–2 thua |
|---|---:|---:|---:|
| Nhóm1–2 gặp Nhóm3 |85%|10%|5%|
| Nhóm1–2 gặp Nhóm4 |95%|4%|1%|

Phần hòa/thua còn lại được phân bổ như trên vì bạn chỉ chỉ định tỷ lệ thắng. Quy tắc này áp dụng cho từng đội top, cả sân nhà và sân khách, ưu tiên trước dao động phong độ/lợi thế sân nhà của mô hình cũ.

- **Nhóm1:** Arsenal, PSG, Barcelona.
- **Nhóm2:** Real Madrid, Manchester City, Bayern.
- **Nhóm3:** Liverpool, Inter, Atletico, Chelsea, AC Milan, Juventus.
- **Nhóm4:** Tottenham, Galatasaray, Napoli, Lyon, Roma, MU. **Giữ Lyon thay Dortmund theo lựa chọn trước**, không đổi thành phần giải ở bản này. MU tiếp tục là đội yếu nhất trong mô hình khi gặp các đội khác.

Đối đầu giữa các đội top vẫn dùng sức mạnh/phong độ/sân nhà của v4, nhóm1 nhỉnh hơn nhóm2; El Clasico giữ quy tắc cân bằng trước phong độ/sân nhà. Sau khi bốc thắng/hòa/thua, tỷ số vẫn đa dạng: sát nút, thắng đậm hoặc trận mở. Không gắn tỷ số thắng cố định cho mọi trận.

Tỷ lệ mới có hiệu lực cho các trận CPU chưa được chốt sau khi khởi động lại. Lịch, kết quả và receipt vua phá lưới đã lưu giữ nguyên. Không cần tạo mùa mới chỉ để nhận xác suất này.

## Các phần giữ từ v4 và giới hạn

Giữ các Card ID khác, Base edits, đội hình Barça/PSG, AjaxE/Bento, hook logo Ajax→Lyon và thành phần hai giải tuyển/Eredivisie đã chốt. Không thêm Power Tackle hoặc Long Range Tackle theo yêu cầu hủy trước. Áo dài Ronaldo và tóc riêng của17592186048938 vẫn **chưa áp dụng** vì chưa xác minh trường dữ liệu riêng; bản này không có sửa ngoại hình đó. Logo vẫn cần kiểm tra hiển thị/cache trên thiết bị.

Không thay CPK, APK hoặc DB bằng file seed. Cấu hình native được pin khớp binary; thay roster/base/đội giải cần build lại và cập nhật pin. `club_outcome_policy` ghi rõ xác suất mới. Khôi phục bằng backup cá nhân; không dùng v4 như một bản đã sửa xong Bayern59835.

## Kiểm chứng kèm gói

- `roster-source-validation.json`: so đủ ID64 trong Player.bin thực;59835 thiếu,52776558193083 tồn tại; chỉ bỏ một dự bị và giữ11 người chính.
- `native-validation.json`: tái hiện lỗi v4 bằng native resolver và full64 Guerreiro; roster22 đạt; kiểm tra detour/trampoline/getter/setter và từ chối dữ liệu thiếu. DB native tổng hợp, không phải RAM chụp từ điện thoại.
- `club-policy-validation.json`:576 kiểm tra biên cho144 cặp có cả hai chiều sân;40.000 trận mô phỏng, đo85,29% và95,07% thắng. Cả85% lẫn95% đều có tỷ số đa dạng và còn khả năng hòa/thua theo phần còn lại.
- `card-handlers-validation.json`:18 thẻ qua handler detail/bulk và learned overlay, có đổi skill Dembélé mới; nguồn DB không đổi.
- `corpus-validation.json`: đối chiếu Tap Trick/Chop Turn cùng các ánh xạ stat/skill.
- `worlds-validation.json`, `regression-validation.json`: chuẩn bị/START HOME–AWAY trên DB sao chép, bridge readiness được stub; giữ snapshot,10 vòng cũ, receipt và inventory.
- `menu-validation.json`: bốn menu qua getter ARM64 thật và bộ cấp phát/destructor.

Kiểm tra trên máy chủ không thay thế việc vào trận thực tế trên điện thoại.
