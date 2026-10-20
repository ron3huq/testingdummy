# My League native hotfix v3 — bản thử sửa Bayern văng khi bấm Bắt đầu

**Chưa thử trên điện thoại.** Bạn đã xác nhận bản v2 văng ngay sau Bắt đầu khi gặp München RW. V3 bỏ cách gửi đội hình CPU inline của v2, dùng các hàm tra cứu đội/cầu thủ gốc để sửa roster trong bộ nhớ. Đây là phương án sửa mới đã kiểm tra thành phần ARM64 và gateway, chưa đủ bằng chứng khẳng định hết crash trên thiết bị. Chưa có logcat/tombstone để xác nhận nguyên nhân crash chính xác.

## Cài bằng MT Manager, không root

1. Buộc dừng game. Sao lưu sáu file hiện tại và dữ liệu gateway/save trước khi thay.
2. Giải nén ZIP. Chép đè **cả sáu file trong `install/work/tools/`** vào vùng nội bộ đã cài Select Team thành công: `73efootball 资源` → `files/embedded-gateway/work/tools`. Không dùng thư mục `Android/data`.
3. Sáu file: `gateway_runtime.py`, `select_team_runtime.py`, `libselect_team.so`, `myleague_realism.py`, `myleague_worlds.py`, `myleague_custom.json`. Phải dùng cùng bộ v3 vì loader kiểm tra hash thư viện.
4. Mở lại game. `myleague-realism-status.json` cần có `state: INSTALLED`, `version: native-hotfix-v3`. Nếu lỗi, xem `myleague-realism-error.txt` mới nhất và `select-team-status.json`.
5. Thử chuẩn bị lại trận gặp Bayern ở mùa hiện tại rồi Bắt đầu. Nếu trận v2 cũ còn lưu đội hình inline, v3 cất dữ liệu active đó vào meta `v3_quarantined_inline_<game_id>`, bỏ trạng thái active lỗi và chuẩn bị lại đúng vòng hiện tại. Lịch và kết quả các vòng đã chơi được giữ. Không cần xóa save hay tạo lại mùa chỉ để thử sửa crash.
6. Nếu không chuẩn bị được trận, kiểm tra `native_team_results` trong `select-team-status.json`. Mã `1` cho đội `127` nghĩa là kiểm tra roster đã đạt, **không phải chứng nhận trận chơi được**. Mã `10`: hook/context chưa sẵn sàng; `11`: sai bản ghi đội hoặc hook chưa sẵn sàng; `12`: số người không hợp lệ; `13`: thiếu/sai bản ghi cầu thủ; `14`: định dạng khóa cầu thủ không khớp. `native_last_player_error` ghi ID cần kiểm tra. V3 chặn bước chuẩn bị/Bắt đầu nếu kiểm tra không đạt. Khi vẫn văng, cần file chẩn đoán và log crash Android để khoanh vùng tiếp.

Giữ `dt200`, `dt870`, APK và manifest đang chạy được. Gói không chứa DB hoặc save. Không cần cài lại/ký lại APK. Nếu cần quay lại code, dùng backup đã lưu; bản v2 đã được xác nhận crash Bayern. Khôi phục code không hoàn tác các thay đổi mùa đã lưu. Không xóa DB để thử.

## Bayern, Barcelona và PSG

- München RW vẫn là **Bayern ID127**, thay Monaco112 ở giải 122. V3 nạp roster 23 cầu thủ có ID base trong dữ liệu gốc: Neuer, Upamecano, Tah, Davies, Laimer, Kimmich, Goretzka, Musiala, Olise, Luis Díaz, Kane; dự bị Kim, Pavlović, Gnabry, Jackson, Guerreiro, Stanišić, Hiroki Itō, Karl, Urbig, Kusi-Asare, Boey, Wisdom Mike. Đây là lựa chọn tùy chỉnh, không phải danh sách đăng ký chính thức đã xác minh. Có hai thủ môn, 11 vị trí chính và các cầu thủ dự bị.
- Barcelona: Pedri thay Gavi; Fermín thay Olmo; Gordon vào vị trí CF của Jesus; Raphinha vào vị trí cũ của Gordon; Cancelo thay Espart; Cubarsí thay Eric García. Các cầu thủ bị thay vẫn ở dự bị. Gordon được bổ sung độ thành thạo CF trong dữ liệu native.
- PSG: Kvaratskhelia thay Godts; Dembélé thay Ferran; Doué thay Akliouche; Vitinha thay Dro; Neves thay Beraldo; Nuno Mendes thay Digne. Giữ đủ 24 cầu thủ, không trùng ID.
- Brazil dùng roster gốc 26 người và thêm Vinícius, thành 27 người qua cùng cơ chế native; bỏ roster inline 21 người v2.

Các đội hình này áp dụng cho đội CPU/base. Đội bạn điều khiển vẫn dùng đội hình và thẻ của bạn. Việc nạp roster/khởi tạo trận thực tế cần xác nhận trên điện thoại; nếu engine dùng dữ liệu đã cache trước hook thì có thể chưa phản ánh đầy đủ.

## Kết quả CPU

Chỉ điều chỉnh các trận tự mô phỏng. Trận bạn tự đá và kết quả cũ đã chốt giữ nguyên.

**Belgian League, 18 tuyển:** Japan, Korea, Uzbekistan, Saudi Arabia ở nhóm đầu; Qatar, Iran, Iraq, UAE, Australia nhóm sau. Vietnam, Indonesia, Thailand, Malaysia, Jordan, North Korea ngang nhau: mỗi bên khoảng 40% thắng, 20% hòa khi gặp nhau. Gặp hai nhóm trên: 70% thua, 20% hòa, 10% thắng. Gặp China/Hong Kong/Singapore: 70% thắng, 30% hòa, không thua. Japan được ưu tiên mạnh nhất khi gặp các đội ngoài nhóm giữa. Quy tắc 70% mới được ưu tiên trước yêu cầu cũ Japan thắng 90% mọi đối thủ.

**Liga Portugal, 20 tuyển:** Spain, Argentina, France, England, Brazil, Portugal cùng nhóm đầu. Trong nhóm, mỗi bên 40% thắng, 20% hòa; riêng Spain có 58% thắng, 18% hòa, 24% thua trước nhóm đầu khác. Gặp Netherlands/Belgium/Germany/Italy: nhóm đầu thắng 88%, hòa 8%, thua 4%; gặp các nhóm yếu hơn: thắng 96%, hòa 4%. Sweden/Senegal và Georgia ở cuối, Georgia thấp nhất.

Phân cấp CLB và ưu tiên chân sút từ bản trước được giữ. PSG/Barcelona/Arsenal dẫn đầu, Real/City nằm trong top5; top5 áp đảo nhóm dưới. MU rất hiếm thắng. Kane/Mbappé/Haaland/Raphinha được ưu tiên ghi bàn, nhưng bảng vua phá lưới chỉ ghi sự kiện mô phỏng hợp lệ theo roster và tỷ số. Đội bạn chọn ghi nhận bàn bạn thực sự ghi.

Lịch bốc ngẫu nhiên khi tạo mùa được lưu cố định cho mùa đó; không đổi lịch mỗi lần mở menu. Các thành phần giải đã đổi giữ 18/18/20 đội, 34/34/38 vòng. Mùa cũ giữ snapshot của mùa cũ.

## Chỉ số và skill

Đã thêm cấu hình 13 cầu thủ Base và 7 Card ID đúng yêu cầu. Mbappé Speed/Acceleration94; Yamal Curl94; Olise Curl90. Các kỹ năng còn lại được đối chiếu tên/flag trên 14.330 payload thẻ. Toàn bộ giá trị của bảy Card ID nằm trong `card_overrides` của JSON; riêng Kvaratskhelia bỏ Marseille Turn cả flag và additional skill khi xuất dữ liệu, kể cả START sau khi gateway chồng learned skill.

**Đã hủy toàn bộ yêu cầu thêm Power Tackle và Long Range Tackle**, gồm Rodri, Haaland và các hậu vệ năm CLB. Không xóa kỹ năng vốn có của cầu thủ.

Base CPU dùng hook dữ liệu native, bao gồm các CLB bạn không chọn. Card ID dùng bản chiếu khi LOGIN/list/detail/START; giữ nguyên ID/serial và không ghi đè dữ liệu thẻ trong DB. Chỉ số chỉ định là giá trị được xuất tại lớp chỉnh sửa; level/booster hoặc hiệu ứng engine có thể làm màn hình cuối cùng khác. Chưa kiểm chứng hoạt ảnh/hiệu ứng mọi skill trên thiết bị.

`native_rosters`, `base_overrides` và thành phần các giải được khóa khớp với thư viện native. Muốn sửa phải build và cập nhật pin cấu hình; sửa JSON đơn lẻ sẽ bị từ chối. `card_overrides`, tier và trọng số ghi bàn là cấu hình Python, cần khởi động lại khi chỉnh. Đợt này không thay face, logo, tay áo.

## Kiểm chứng

- `native-validation.json`: chạy setter/getter packed parameter và getter roster ARM64 **gốc**, kiểm tra đủ 147 field, 4 roster, tính lặp lại, chặn thiếu cầu thủ. **Các bản ghi DB native trong kiểm tra là giả lập**, chưa đo từ RAM điện thoại.
- `menu-validation.json`: getter/detour/trampoline gốc, tăng Portugal 18→20 và destructor/bộ cấp phát.
- `worlds-validation.json`: gateway thật trên bản sao DB seed, chuẩn bị/Bắt đầu cả HOME/AWAY; phục hồi active inline cũ; kiểm tra bảy thẻ, 13 Base và 15.000 lần bốc cho từng cặp đại diện. **Cầu nối native sẵn sàng được giả lập trong kiểm tra gateway**, không phải thử tích hợp điện thoại.
- `regression-validation.json`: giữ snapshot cũ, 10 vòng, lịch, receipt, inventory và DB gốc.
- `skill-mapping-validation.json`: đối chiếu tên skill với flag trong thư viện thẻ được cung cấp; đây là bằng chứng dữ liệu, không phải thử hiệu ứng trong trận.

Mã nguồn và script kiểm tra được công bố cùng gói. Kết quả đạt trên máy chủ không xác nhận crash đã hết. Mốc xác nhận cần đạt là bạn bấm Bắt đầu và vào đá được trận Bayern trên Android.
