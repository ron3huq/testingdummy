# FULL8 RC29.3 · Master League V32 + RC26 cho V19.1

Áp giống hệt FULL8 RC26: **chỉ chép đè `assets/` và `classes5.dex`** vào APK V19.1, ký khóa cũ, cập nhật đè. Không xóa data.
Hai artifact, chép cả hai (cùng gốc `assets/`):
- `FULL8-RC29-V32-ML-part1-core`: `classes5.dex` + phần lớn `assets/`
- `FULL8-RC29-V32-ML-part2-data`: các file model lớn trong `assets/gateway-release` (Java tự giải nén, nén hay không đều được)

## Chống màn hình đen
- **Không** thay bất kỳ file nào engine đọc thẳng từ APK: `dt270`, `dt500`, `pc0010` giữ nguyên bản V19.1.
  (V32 chỉ khác V19.1 ở 2 file âm thanh mở thẻ trong đó; bản V30 full và addon quỹ đạo trước đây đen màn hình vì thay đúng các file này.)
- Không thay `AndroidManifest.xml`, `resources.arsc`, `classes1–4.dex`.
- Không có quỹ đạo bóng / knuckle.

## RC29.12: Home → News tiếng Anh hấp dẫn, thanh màu bảng xếp hạng gọn
- Tab News (của V32): toàn bộ tin viết lại bằng tiếng Anh, tiêu đề đa dạng kịch tính, kèm lời HLV (Arteta, Guardiola, Flick, Kompany, Simeone...).
- Bảng xếp hạng: thanh màu dự cúp tách khỏi số thứ hạng.
- Europe: bỏ nhãn giải đấu cạnh tên CLB.

## RC29.11: giao diện theo V32, chỉ số cầu thủ, UCL thật, tiếng Anh
- Trang League (Season): bỏ Newsroom, giữ bố cục V32; Scorers/Assists không ảnh, tên viết tắt (K. Mbappé); mục Stats: trận, bàn, kiến tạo, MOTM, điểm trung bình; nút ⤢ mở bảng lớn (G+A và điểm TB cao nhất). Thanh tab vuốt ngang được.
- Bảng chi tiết trận giải khác: hộp gọn giữa màn hình, nút ✕, ảnh cầu thủ nhỏ, người ghi bàn dưới từng đội.
- Transfer: hiện tên cầu thủ, CLB chỉ logo, bỏ tuổi.
- Thanh bên cuộn được; Season ngay dưới Home; Fixtures ở cuối tab Season.
- UCL Master League: mùa đầu dùng 36 CLB thật; các mùa sau không có đội vô danh.
- Dịch thêm ~270 cụm tiếng Trung còn sót.
- Gỡ cúp UCL 2017/AFC khỏi save Master League. Tạm tắt thêm kỹ năng và đổi sân (an toàn khi vào trận).

## RC29.9: thêm cầu thủ mới vào CLB, tự đặt vai trò ghi bàn, UCL thực tế hơn
- **Editor → Find a player → "Add from game"**: tìm bất kỳ thẻ nào trong dữ liệu game (vụ chuyển nhượng ngoài đời mà Master League chưa có) và thêm vào CLB đang chọn (vị trí lấy từ thẻ). Cầu thủ đó ra sân, ghi bàn và kiến tạo như mọi người.
- **Cột Role (✎)**: đặt % số bàn và % số kiến tạo của đội cho một cầu thủ (ví dụ 30% bàn ≈ 25–30 bàn/mùa ở CLB mạnh), hoặc Auto (theo chỉ số + vị trí). Áp dụng cho giải quốc nội, UCL, Quả bóng vàng, tin tức.
- **UCL Master League**: chênh lệch giữa các giải nhỏ lại (đội Bồ/Thổ có cơ hội thật), trận châu Âu chặt hơn (~3 bàn/trận).

## RC29.8: ghi bàn / kiến tạo / Quả bóng vàng thực tế, mọi chỉnh sửa có hiệu lực ngay
- Trận của đội bạn (mô phỏng): bàn và kiến tạo chia theo tỉ lệ thật, không còn tiền đạo ghi 45 bàn. Người không phải chân sút số một tối đa ~14% số bàn của đội.
- Ngôi sao nhận diện theo họ tên đầy đủ (hết lỗi Isak Hien thành vua phá lưới, Ethan Mbappé, Jobe Bellingham...).
- Sửa lỗi Kane / Haaland / tiền đạo 0 kiến tạo (chuỗi bốc thăm kiến tạo trùng nhịp với bàn thắng; kiến tạo CPU lấy theo đội hình gốc thay vì đội hình thật).
- Số bàn mỗi trận từng giải gần thực tế (Serie A ~2,5, La Liga ~2,6, Ligue 1 ~2,8, Bundesliga ~3,1, Premier League ~2,9). Nhà vô địch ~80–95 bàn (Barça cao nhất như ngoài đời).
- UCL: đội hình lấy từ đội hình thật trong Master League; chân sút hàng đầu (Kane, Haaland, Mbappé) ~10–14 bàn khi đội đi sâu.
- **Tương lai thật / chỉnh sửa:** mọi thứ tính từ đội hình và chỉ số HIỆN TẠI trong save: hạ chỉ số Kane thì tỉ lệ ghi bàn và sức mạnh Bayern giảm ngay; chuyển nhượng thì CLB mới mạnh lên, CLB cũ yếu đi, cầu thủ mang tỉ lệ ghi bàn theo; nâng một cầu thủ thường lên đẳng cấp cao thì tự thành chân sút. Áp dụng cho tỉ số, vua phá lưới, kiến tạo, Quả bóng vàng, tin tức.
- UCL 2017: Ronaldo của Real là thẻ 88042803047215 (tên "Cristiano Ronaldo").
- Ảnh mặt nhỏ: bỏ bộ nhớ đệm cũ (3 ngày) nên ảnh thẻ đã đổi hiện đúng; làm mới sau 30 phút.

## RC29.7: Master League Transfer ở launcher, Editor trong Master League, launcher mới, phỏng vấn theo tính cách
- **Launcher → "Master League Transfer"**: mở đúng màn hình Transfer gốc (giao diện Java như mục Transfer của RC26) nhưng cho 96 CLB của 5 giải Master League: xem đội hình trên sơ đồ, đổi sơ đồ/vị trí/số áo/đội trưởng/người đá phạt, "Transfer to Another Team" (chuyển thật sang CLB khác, kể cả khác giải), Abilities · Celebrations · Accessories (sửa chỉ số thì sức mạnh của cầu thủ trong mô phỏng Master League cũng đổi theo). CLB của bạn chỉ xem (đội của bạn quản lý trong Master League).
- **Master League → mục Editor (thanh bên)**: chọn giải → CLB → cầu thủ; nút Move chuyển cầu thủ sang CLB khác; sửa CA (sức mạnh) bằng +/−; tìm cầu thủ ở cả 5 giải. Kết quả, vua phá lưới, kiến tạo, tin tức và diễn biến dài hạn thay đổi theo ngay.
- **Launcher mới**: tông màu giống Master League (đen than, đỏ, vàng), màn hình ngang chia 2 cột (nút vào game bên trái, toàn bộ công cụ bên phải, vừa 1 màn hình), bỏ hiệu ứng làm mờ gây lag, **chỉ tiếng Anh**.
- **Phỏng vấn theo tính cách thật**: Ronaldo, Messi, Zlatan, Neymar, Suárez, Griezmann, Kane, Salah, Lewandowski, Mbappé, Müller, Totti, Agüero, Cavani... và HLV Mourinho, Guardiola, Klopp, Simeone ("partido a partido"), Conte, Zidane, Ancelotti, Allegri ("corto muso"), Emery ("good ebening")...; HLV đối thủ cũng phản ứng sau trận.
- **Quả bóng vàng thực tế hơn**: tính cả đẳng cấp cầu thủ (CA) và tầm vóc CLB, không chỉ số bàn; danh sách 30 ứng viên chỉ gồm cầu thủ đẳng cấp. Sửa lỗi kiến tạo giải của bạn bị tính 0 cho người ngoài top 10.
- **Ghi bàn đội bạn thực tế hơn**: tiền đạo không phải "ngôi sao ghi bàn" không còn ghi 25+ bàn/mùa (Havertz ~12–15).
- **Cúp**: tự chuyển tab theo giai đoạn (League phase → Knockout → MVP).

## RC29.6: kỹ năng, sân, tin tức giải VĐQG, cúp gọn màn hình
- Master League: cầu thủ 9 CLB lớn (Arsenal, Real, Barça, Bayern, Man City, Liverpool, Chelsea, Atlético, PSG) được thêm kỹ năng đặc biệt thật; mọi tiền vệ và cầu thủ chạy cánh có Edge Crossing + Low Lofted Pass. Chỉ THÊM, không xoá kỹ năng nào; chỉ trong Master League (My League không đổi).
- Sân: mỗi trận Master League chọn ngẫu nhiên một sân có bản quyền theo danh sách RC26 (1, 7, 30, 51, 52, 85), không dùng sân mặc định. Chưa thử trên điện thoại.
- Trang 5 giải VĐQG có Newsroom (đua vô địch, chuỗi thắng/thua, cú sốc, đua vua phá lưới, kiến tạo, chuyển nhượng "Here we go").
- Cúp: lượt về hiện tổng tỉ số; đội bị loại gạch tên, màu xám; bỏ vạch dọc xanh/vàng; trang cúp luôn vừa màn hình (các ô tự cuộn bên trong); tự chuyển sang tab Knockout / MVP khi sang giai đoạn mới.

## RC29.5: thế giới Master League thay đổi theo thời gian, tin tức sống động hơn
- **Chơi lâu dài:** mùa 1 giữ đúng bức tranh hiện tại (Arsenal mạnh, Kane/Haaland/Mbappé...). Từ mùa 2, mỗi lần sang mùa sẽ ghi một "trang" mới (meta `rc29_dyn_v1`):
  - Sức mạnh CLB = điểm gốc × "thời kỳ" (lên xuống ngẫu nhiên nhưng có quán tính, CLB có giai đoạn hay và dở) × đội hình thật trong thế giới V32 (chuyển nhượng CPU, chỉnh sửa của bạn). Mua người giỏi thì mạnh lên, bán trụ cột thì yếu đi.
  - Phong độ ngôi sao ghi bàn lên xuống theo mùa (0,55–1,35 lần), nên cuộc đua vua phá lưới đổi chủ; ngôi sao chuyển CLB thì mang theo khả năng ghi bàn.
  - Mỗi hè có tới 3 tiền đạo/tiền vệ tấn công giỏi "bùng nổ" thành chân sút mới; họ có thể tiếp tục thăng hoa hoặc lụi tàn.
  - Ai được chỉnh chỉ số (CA) cao hơn sẽ ghi/kiến tạo nhiều hơn ngay, vì bảng ghi bàn tính theo CA hiện tại.
  - Mô phỏng 6 mùa: vô địch EPL Arsenal → Arsenal → Man City → Man City → Arsenal → Man City; La Liga Barça/Real thay nhau.
- **Tin tức:** tiêu đề đa dạng, giật gân hơn (bàn thắng phút cuối, lội ngược dòng, cú sốc, khẩu chiến, VAR...), không còn kiểu "X humiliated by Y". Newsroom là dải tin ngang dưới bảng xếp hạng, vừa một màn hình.
- **Matchdays** hiện cả các lượt knock-out (lượt đi/lượt về, tỉ số, người ghi bàn), tự cuộn tới lượt hiện tại, đánh dấu "Next".

## RC29.4: hai cúp mới, tin tức kiểu FM, tên CLB thật, logo AFC chính thức
- Mục **Cups** mới (thanh bên trái): **UCL 2017** (12 đội Y17, 4 trận vòng bảng 2 sân nhà / 2 sân khách, top 4 vào tứ kết, hạng 5–12 đá play-off; play-off, tứ kết, bán kết 2 lượt như UCL V32; chung kết 1 trận ở Cardiff) và **AFC Champions League Elite** (24 đội Saudi / Nhật / Hàn / Thái / Malaysia / Trung Quốc / Việt Nam, 8 trận vòng bảng, vòng 16 đội 2 lượt, tứ kết - chung kết 1 trận ở Jeddah). Chọn đội, đá từng lượt hoặc mô phỏng đến hết. Có bảng vua phá lưới / kiến tạo, MVP top 3, báo cáo từng trận.
- Barcelona luôn vào ít nhất bán kết, Messi 10–13 bàn (kiểm tra 30 giải: 10–13 bàn mọi lần, trung bình 2,6 bàn/trận).
- Đội hình UCL 2017: mỗi cầu thủ chỉ thuộc **một** CLB, đúng giai đoạn 2014–2019 (Bale chỉ ở Real, Pogba chỉ ở MU, Benatia ở Juventus, Alisson ở Liverpool...). Barcelona có thêm ghế dự bị 2014–19 (Cillessen, Semedo, Lenglet, André Gomes, Dembélé, Denis Suárez). Tab **Squads** hiện cầu thủ trên nền thẻ Big Time của Del Piero.
  Lưu ý: đội hình Y17 trong **My League** được RC26 biên dịch sẵn vào `libselect_team.so` (có khoá kiểm tra), sửa file JSON làm My League không khởi động được, nên bản này **không đổi My League Y17** và không đổi nền thẻ gốc trong game; các sửa chỉ áp dụng trong cúp UCL 2017.
- Tin tức kiểu Football Manager: tường thuật trận (phút ghi bàn, ai kiến tạo, lội ngược dòng, bàn thắng phút cuối), phỏng vấn cầu thủ ghi bàn, họp báo HLV (Zidane, Luis Enrique, Guardiola, Mourinho...), drama (khẩu chiến kình địch, cãi trọng tài, tiền đạo tịt ngòi, phòng thay đồ, giận dỗi khi bị thay ra), cầu thủ hay nhất lượt đấu, cuộc đua vua phá lưới. Có ở tab News và ô Newsroom dưới bảng xếp hạng. Ô Matchdays tự cuộn tới lượt đang đá, mỗi trận có danh sách người ghi bàn.
- Bảng xếp hạng: bỏ ô màu to, dùng vạch mảnh + huy hiệu số; cột phong độ W/D/L; trước khi đá xếp theo A–Z.
- Master League: tên thật cho các CLB không bản quyền (Real Madrid, Atlético, Real Sociedad, Real Betis, Sevilla, Juventus, Roma, Napoli, Bayern, Club Brugge, Young Boys, FC København...).
- Logo chính thức (Wikipedia/Wikimedia) cho Al Hilal, Al Nassr, Al Ahli, Al Ittihad, Công An Hà Nội, Thép Xanh Nam Định. Shanghai Port và Beijing Guoan tạm hiện huy hiệu chữ.
- Sửa dòng chữ Trung còn sót (ví dụ "欧冠决赛" → "Champions League Final", "38 轮" → "R38", 胜/平/负 → W/D/L).

## RC29.3: Master League thực tế hơn (chỉ ảnh hưởng Master League, My League RC26 giữ nguyên)
- Chỉ 5 giải hàng đầu: bỏ giải hạng 2, bỏ lên/xuống hạng.
- Bỏ tuổi: không lão hóa, không giải nghệ, không lò đào tạo trẻ (kể cả đội máy), ẩn mọi cột tuổi.
- Tỉ số máy với máy theo sức mạnh thực tế từng CLB + dao động theo mùa + phong độ theo đợt 5 vòng (Arsenal mạnh nhất EPL,
  đội vô địch EPL ~89–95 điểm; Barça–Real đua sát; Man Utd yếu, phong độ thất thường).
- Vua phá lưới thực tế: Kane ~30–36, Haaland ~27–33, Mbappé ~25–30, Raphinha ~18–24 (theo tỉ lệ bàn thật của đội).
- Đội anh và đối thủ luôn phong độ cao nhất (A); độ khó mặc định LEGEND (vẫn đổi được trong Settings).
- Chuyển nhượng máy hiếm và hợp lý: tối đa 1 vụ mỗi CLB mỗi kỳ, không bán trụ cột giá trị lớn cho CLB lớn khác.
- UCL: Galatasaray, Fenerbahçe, Benfica, Sporting luôn dự; bảng vua phá lưới / kiến tạo cúp (nút mới ở thanh bên trang Europe).
- Quả bóng vàng + Chiếc giày vàng: công bố 30 ứng viên 8/8, lễ trao giải 22/9 mùa sau (tab Season → Awards).
- Chỉ tiếng Anh; dịch thêm ~920 cụm còn tiếng Trung. Stat leaders hiện tên; bấm trận giải khác xem báo cáo; tab giải không tràn chữ.
- Một đội không thể có cầu thủ ghi nhiều bàn hơn số bàn đội đó ghi trong trận.
Cần **bắt đầu sự nghiệp Master League mới** để áp dụng đầy đủ (sự nghiệp cũ vẫn chạy được).

## RC29.2: sửa treo ở "Starting local services…"
Java V32 chèn 2 bước chặn trước khi vào game (hộp thoại "Join our Telegram group / I have joined" và trang chống lừa đảo cho máy tiếng Trung).
Với launcher RC26 các bước này bị che hoặc bấm "Later" là không bao giờ chạy lệnh vào game → đứng ở "Starting local services…" (gateway Python đã chạy xong).
`GatewayBootActivity.requestGameLaunch` giờ chạy thẳng lệnh vào game như RC26.

## RC29.1: Master League tách khỏi My League
RC26 dùng lại mã giải của game cho My League (122 = UCL, 128 = World Nation League, 518 = Y17, 473 = Y08, 549, 566...).
Master League V32 dùng đúng các mã đó cho giải thật (122 = Ligue 1; 125/128/476/518/566/473/549 lấy suất dự cúp châu Âu).
`ml_isolation.pyc` (trong `app.imy`): khi đang ở Master League (hồ sơ ML đang bật, hoặc lệnh đến từ module Master League),
13 hàm RC26 thay thế (`my_league` x7, `ml_super_league.start_season`, `opponent_squad` x2, `GateLogic` x3) và bảng giải/đội/lịch
trả về **bản gốc V32**; ngoài Master League mọi thứ vẫn là RC26 như cũ. Không đổi file nào của My League, không ghi save.
Tên đội: giữ tên thật RC26 đã sửa (Real Madrid, Man City...), không lấy các tên RC26 dùng cho đội trẻ/đội khác.

## Gồm
- Master League V32 (`assets/ml-league`, runtime Python V32 trong `assets/chaquopy/app.imy`, Java Master League trong `classes5.dex` gồm cả `MlSaveTransfer` mới của V32).
- Giữ nguyên các phần của RC26: Transfer 122/128, My League, UCL/WC + giải thưởng, Event Edit, Match Settings, Single Player, face 88044950524330 = NR17.

Runtime Python của Master League V32 nằm chung với dữ liệu thẻ của V30/V32 nên không tách riêng được.

Kiểm tra trên máy chủ: 31/31 PASS - gateway, hook RC26, My League, Transfer 122/128, UCL/WC + giải thưởng, tạo mùa Master League (82 CLB, 2399 cầu thủ), mô phỏng 6 vòng, bảng xếp hạng; My League vẫn thấy 122 = UCL sau khi chơi Master League. Chưa thử trên điện thoại.
