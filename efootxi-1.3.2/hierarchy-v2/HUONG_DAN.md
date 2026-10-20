> **DỪNG DÙNG BẢN V2 NÀY:** người dùng xác nhận văng ngay sau Bắt đầu khi gặp Bayern127. Các kiểm tra payload dưới đây không chứng minh consumer Android chơi được trận. Xem [bản thử sửa v3](../hotfix-v3/HUONG_DAN.md), chưa xác nhận trên điện thoại.

# My League Hierarchy v2 — 3 giải và phân cấp theo yêu cầu

**BẢN MỚI CHƯA KIỂM CHỨNG TRÊN ĐIỆN THOẠI.** Bản Select Team v1 trước đã được bạn xác nhận chạy tốt. V2 mở rộng native hook đó; đã kiểm tra ARM64, cấp phát/giải phóng khi tăng danh sách lên 20 đội, gateway trên DB sao chép và mô phỏng. Bayern/Brazil inline cần thử màn hình đội hình và trận thực tế.

## Cài trên máy không root bằng MT Manager

1. Hoàn tất trận đang đá, buộc dừng game. Sao lưu các file đang chạy tốt và giữ bản backup save/thư mục gateway hiện có trước khi bắt đầu mùa mới. Gói không chứa save và không ghi đè DB.
2. Vào đúng vùng nội bộ `73efootball 资源` → `files/embedded-gateway/work/tools` như lần cài Select Team thành công. Không chép nhầm sang `Android/data`.
3. Chép **cả 6 file** trong `install/work/tools/` vào tools: `gateway_runtime.py`, `myleague_realism.py`, `myleague_worlds.py`, `myleague_custom.json`, `select_team_runtime.py`, `libselect_team.so`. Bốn file cũ được cập nhật, hai file worlds/config được thêm. Không trộn `.so` v2 với loader v1 vì hash khác.
4. Giữ nguyên `dt200`, `dt870`, APK, `release-manifest.json`, `installed-release.txt` và save. Không cần ký lại APK. Mở game, kiểm tra `myleague-realism-status.json` có `state: INSTALLED`; nếu có lỗi xem `myleague-realism-error.txt` mới nhất.
5. Mở Select Team. `select-team-status.json` có `league_results` cho `122`/`566`/`128`: `1` hoặc `2` nghĩa là danh sách đã sửa/đã đúng. `5` nghĩa là không tìm thấy danh sách nguồn; `9` là trùng nguồn; `10` là không cấp phát được danh sách lớn hơn. Gửi hai file chẩn đoán nếu menu chưa đúng. Không thử thay CPK để khắc phục.
6. **Bắt đầu mùa mới bằng chức năng trong game** để nhận thành phần giải mới và lịch mới. Mùa đang chơi giữ snapshot cũ, lịch và kết quả đã chốt. Phân cấp CPU và trọng số ghi bàn mới có hiệu lực cho trận CPU chưa chốt; không sửa ngược bảng thống kê 10 vòng cũ.

## Thành phần giải

- **Ligue 1 / 122:** giữ Super League 18 đội, thay Monaco112 bằng **München RW / Bayern127**. Bayern dùng đúng ID127, không đổi tên Monaco. Có roster thử 15 base card có payload trong dữ liệu: Neuer, Upamecano, Tah, Kim, Davies, Laimer, Kimmich, Goretzka, Pavlovic, Musiala, Gnabry, Olise, Luis Díaz, Kane, Jackson. Đây là đội hình tùy chỉnh từ dữ liệu sẵn có, không phải danh sách đăng ký chính thức đầy đủ.
- **Belgian League / 566:** Vietnam, Indonesia, Thailand, Singapore, Malaysia, China, Japan, Korea Republic, Uzbekistan, Australia, Iran, Iraq, UAE, Qatar, Saudi Arabia, Hong Kong, Jordan, Korea DPR. **18 đội, 34 vòng, 306 trận.**
- **Liga Portugal / 128:** Spain, Argentina, France, England, Brazil, Portugal, Netherlands, Belgium, Germany, Italy, Croatia, Uruguay, Colombia, Mexico, Morocco, United States, Norway, Sweden, Senegal, Georgia. **20 đội, 38 vòng, 380 trận.** Native list đã được mở rộng từ 18 thành 20 bằng bộ cấp phát của engine.

Đội tuyển dùng ID thật và native roster có sẵn. Riêng **Brazil45**: roster gốc không có Vinícius117047. V2 có roster inline thử 21 người gồm 20 cầu thủ từ tuyển gốc có base payload và Vinícius, để anh thực sự có mặt trong đội hình/payload; không chỉ tạo tên giả trên bảng ghi bàn. Một số cầu thủ trong danh sách gốc thiếu payload không được đưa vào roster inline này. Danh sách đầy đủ nằm ở `custom_rosters`.

Tên/logo vỏ hai giải vẫn là Belgian League/Liga Portugal từ tài nguyên game; gói thay thành phần thi đấu, chưa thay logo giải.

## Phân cấp CPU

**Chỉ tác động trận CPU được tự mô phỏng. Không thay tỷ số trận bạn trực tiếp điều khiển hoặc tăng độ khó đối thủ trong trận.** Vì vậy tỷ lệ dưới đây không bảo đảm cho trận bạn tự đá.

### CLB

- Dẫn đầu: PSG, Barcelona, Arsenal.
- Kế tiếp trong top 5: Real Madrid, Manchester City.
- Nhóm sau: Liverpool, Chelsea, Inter, Atlético.
- Các đội khác: nhóm tiếp theo, gồm Bayern vì yêu cầu không chỉ định Bayern ở nhóm cao hơn.
- MU: hạn chế thắng tối đa.

Top 5 gặp đội ngoài top 5: mô phỏng **97% thắng, 3% hòa, không thua**. Trong top 5, ba đội dẫn đầu được ưu tiên trước Real/City; các trận cùng nhóm có lợi thế sân nhà và vẫn có thắng/thua. MU gặp đội ngoài top 5 chỉ có 2,5% cơ hội thắng; gặp top 5 không thắng. Đây là chính sách phân cấp theo yêu cầu, không phải mô hình dự báo bóng đá thực tế.

### Châu Á

Japan mạnh nhất: **90% thắng, 8% hòa, 2% thua** khi CPU mô phỏng; Korea/Uzbekistan xếp kế. Sau đó Iraq/Saudi Arabia/Australia; Iran/Qatar/UAE/Korea DPR; Indonesia/Vietnam/Thailand/Jordan/Malaysia; China/Hong Kong; cuối là Singapore.

Uzbekistan xuất hiện hai lần trong yêu cầu: dùng nhóm cao hơn. Australia không được chỉ định nhóm: tạm cùng Iraq/Saudi Arabia. Có thể chỉnh tier trong JSON và khởi động lại nếu muốn đổi.

### Thế giới

Spain mạnh nhất; Argentina/France/England kế tiếp; rồi Brazil/Portugal/Netherlands/Germany/Belgium/Italy; tiếp United States/Morocco/Norway; tiếp Croatia/Uruguay/Colombia/Mexico; cuối Sweden/Senegal, Georgia yếu nhất.

Các cặp khác nhóm được ưu tiên theo khoảng cách tier; cùng nhóm vẫn cạnh tranh. Số bàn có ngẫu nhiên và đội thắng được bảo đảm phù hợp kết quả đã bốc theo chính sách.

## Cầu thủ ghi bàn

Tăng trọng số Kane, Mbappé, Haaland, Raphinha; các ưu tiên khác gồm Messi, Ronaldo, Vinícius, Yamal, Dembélé, Kvaratskhelia. Đội hình chính, vị trí và chất lượng vẫn được xét; không viết sẵn tên vào bảng xếp hạng. Bàn/kiến tạo cầu thủ CPU cộng khớp tỷ số đội và được lưu bằng receipt gốc, không cộng lại khi mở menu.

CLB/đội tuyển bạn chọn dùng đội Dream Team và bàn thắng thật của bạn. Ví dụ chọn Brazil không tự thêm bàn cho Vinícius/Raphinha nếu bạn không dùng họ trong trận. Các số liệu mô phỏng toàn CPU dưới đây không áp dụng cho đội do bạn điều khiển.

## Kiểm chứng và giới hạn

- `native-validation.json`: chạy hàm ARM64 gốc qua detour/trampoline, kiểm tra cả 3 danh sách; Portugal tăng 18→20, buffer cũ được giải phóng một lần và destructor native giải phóng buffer mới một lần. Kiểm tra từ chối sai lớp/vector và gọi lại không cấp phát lặp.
- `regression-validation.json`: giữ nguyên snapshot mùa Super League cũ có Monaco112, 10 vòng đã chơi và active match; kiểm tra lịch, byes, receipts, DB copy, inventory và prepare.
- `worlds-validation.json`: 200 mùa **cho mỗi giải** (600 mùa toàn CPU); chọn giải/chuẩn bị đội tuyển thật qua gateway, payload prepare/START của Bayern/Brazil, thử override stat/skill trên bản sao cầu thủ.

Kết quả tham khảo từ benchmark: Nhật thắng ~89,7%, MU ~1,6%. CLB: Mbappé ~60,1 bàn/mùa, Haaland ~70,5, Raphinha ~50,1. Giải tuyển thế giới: Kane ~72,4, Mbappé ~64,4, Haaland ~52,8. Đây là kết quả mô phỏng theo cấu hình cố ý mạnh, **không phải kết quả đã đo trên điện thoại hoặc cam kết cho save của bạn**.

Bayern/Brazil được gửi qua đường đội hình inline đã có ở giao thức VS COM; đã kiểm tra tính nhất quán ID/serial/plan và vị trí HOME/AWAY của payload START. Chưa xác nhận consumer My League trên điện thoại áp dụng/render đầy đủ. Nếu chọn/đối đầu Bayern hoặc Brazil bị lỗi, dừng thử và gửi chẩn đoán; không khẳng định chỉ vượt qua kiểm tra gateway là đã chơi được trận.

## Sửa skill, chỉ số, tay áo và logo

Đọc [EDIT_CAU_THU_VA_LOGO.md](EDIT_CAU_THU_VA_LOGO.md). V2 có cấu hình `player_overrides` tùy chọn cho cầu thủ CPU trong đội inline, mặc định rỗng. Đã kiểm tra ví dụ Kane dứt điểm99 + skill18 xuất hiện đúng trong wire payload và không sửa thư viện/owned DB. Field áo dài chưa xác minh nên chưa thêm công tắc. Logo cần thay đúng asset Android.

Không sửa danh sách `teams` trong JSON một mình: native binary phải được tạo lại theo cùng ID. Bộ kiểm tra từ chối danh sách JSON khác bản native đã đóng gói. Có thể chỉnh `tiers`, `scorer_boosts`, roster inline và overrides trong giới hạn kiểm tra; cần khởi động lại và chuẩn bị trận mới.

## Khôi phục bản đang hoạt động trước v2

Buộc dừng game. Khôi phục bốn file đã sao lưu hoặc bốn file trong `restore/` (bản Select Team v1 + Realism v1 đã gửi trước đây). Xóa `myleague_worlds.py`, `myleague_custom.json` và file chẩn đoán v2. Không xóa DB.

**Nếu đã tạo mùa mới có Bayern/đội tuyển, restore code v1 không chuyển mùa đó thành giải cũ.** Mùa vẫn giữ snapshot mới; v1 thiếu roster inline Bayern/Brazil và thành phần giải mới. Cần dùng save backup trước khi đổi mùa để quay lại chính xác, hoặc quay về bản v2 để chơi tiếp sau khi xử lý lỗi. Không tự sửa/xóa mùa đã lưu nhằm giả lập rollback.
