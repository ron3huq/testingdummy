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
