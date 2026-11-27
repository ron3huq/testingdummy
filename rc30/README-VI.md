# FULL8 RC30 (RC26 gốc + face Ronaldo 2017, không có Master League / V32)

Áp y hệt RC26: chép đè `assets/` + `classes5.dex` vào APK V19.1, ký khóa cũ, cập nhật đè (không xóa data).

## RC30.1
- Nền: FULL8 RC26 TRANSFER RESTORE + face Ronaldo 2017 (NR17) cho 88044950524330. Không có quỹ đạo bóng, không có Master League.
- My League Y17 Champion League: 3 lượt, 33 vòng (mùa mới; mùa đang đá giữ lịch cũ).
- Sức mạnh 2016/17: Real Madrid, Barcelona đỉnh cao; Bayern, Juventus, Liverpool bám sát; PSG, Chelsea, Man City, Atlético; Spurs, Roma, Man United.
- Ghi bàn / kiến tạo đội máy theo mùa 2016/17: Messi, Ronaldo thời đỉnh cao: số bàn xấp xỉ hoặc hơn số trận (thường 33-43 bàn / 33 trận), kiến tạo Messi nhiều hơn Ronaldo; Suárez, Neymar, Lewandowski, Kane, Cavani, Salah, Agüero, Griezmann, Džeko, Dybala, Costa...; kiến tạo De Bruyne, Eriksen, Messi, Neymar, Di María, Müller, Kroos, Modrić...
- Tỉ số Y17 giữa các đội lớn: ít 0-0, nhiều trận mở.
- Tên CLB đầy đủ cho UCL và Y17 (Paris Saint-Germain, FC Bayern München, Atlético de Madrid, Tottenham Hotspur, Inter, AC Milan, Napoli...).
- Ảnh thẻ Ronaldo 2017: thẻ 88042803047215 (thẻ Honda đã áp Ronaldo) và 88044950524330 luôn hiện ảnh Ronaldo, cả ảnh mini 128x128 lẫn ảnh thẻ lớn 184x256 (nền xám), qua cơ chế ảnh tùy chỉnh của game. Ảnh bạn tự nhập sau đó vẫn thay được.

## RC30.2 - đội hình Y17 chuẩn 2016/17 - 2017/18 (sửa trong thư viện game libselect_team.so)
- Mỗi cầu thủ chỉ ở một CLB, số áo đúng mùa đó, đội hình chính 11 người hợp lý:
  - Real Madrid: Hazard số 7 thay Ronaldo; thêm Lucas Vázquez (17); bỏ Pepe.
  - Barcelona (11 -> 16): thêm Cillessen (13), Nélson Semedo (2), Digne (19), André Gomes (21), Denis Suárez (6).
  - Chelsea 2016/17: bỏ Hazard, Lampard, Mata, Čech, Oscar; thêm Begović (1), Chalobah (14), Aké (16), Christensen (27); Costa ở lại Chelsea.
  - Juventus: bỏ Alves, Pirlo, Pogba, Vidal, Thuram; thêm Szczęsny (23), Douglas Costa (11), Lemina (18), Rincón (28), Pjaca (20), Rugani (24), Kean (34); Benatia ở Juve.
  - Bayern: bỏ Benatia, Bernat, Ulreich; thêm Javi Martínez (8).
  - Liverpool 2017/18: bỏ Alisson, Fabinho, Shaqiri, Origi, thêm Emre Can (23), Alberto Moreno (18).
  - PSG: bỏ Zlatan, Sirigu; thêm Mbappé (29), Lo Celso (18); Alves, Lucas Moura ở PSG.
  - Man City: thêm Bernardo Silva (20).
  - Atlético: bỏ Diego Costa, Forlán, Trippier; thêm Santiago Arias (4), Thomas Partey (5), Vietto (20).
  - Tottenham: Trippier (2) về Spurs; bỏ Bale, Lucas Moura, Ndombélé, Lo Celso, Reguilón; thêm Gazzaniga (22), Davinson Sánchez (6), Walker-Peters (37), Janssen (9).
  - Roma: Alisson ở Roma; bỏ Benatia, Candela, Aldair, Candreva, Paredes; thêm Juan Jesus (5), Vermaelen (15), Gerson (30), Schick (14).
  - Man United: bỏ Rooney, Fletcher, Evans, Blind; thêm Lukaku (9), Lindelöf (2), Luke Shaw (23).
- Dữ liệu game không có nhiều cầu thủ thời đó (Pjanić, Khedira, Matuidi, Higuaín, Mandžukić, Boateng, Robben, Dele Alli, Dembélé (Spurs), Fàbregas, Nainggolan, Manolas, Juanfran, Filipe Luís...) nên chỉ dùng người có thẻ trong game.
- Messi và Ronaldo (đội máy): 33-37 bàn mỗi mùa 33 trận, theo nhịp từng mùa; vẫn có trận tịt ngòi khi gặp đội khó.

## RC30.4
- Bỏ trang League ngoài launcher (RC30.3). Mọi thứ nằm trong **My League trong game**: tỉ số, bảng xếp hạng, tab Score/Assist.
- Người ghi bàn/kiến tạo của máy trong Y17 theo đúng tỉ lệ đóng góp thực tế mùa 2016/17–2017/18 của từng cầu thủ (Lewandowski, Kane, Salah, Cavani, Džeko, Dybala, Costa, Griezmann, Agüero... là chân sút chính; Eriksen, De Bruyne, Koke, Müller, Di María, Pogba... là người kiến tạo chính).
- Messi: luôn 33–37 bàn mỗi mùa 33 trận, khoảng 5–13 kiến tạo; đạt mốc rồi thì không ghi thêm.
- Barça và Real chênh rõ hơn với phần còn lại; Liverpool/Juve/Bayern bám sau.
- Trận bạn đá: Score/Assist lấy đúng người ghi bàn/kiến tạo thật trong trận.

## RC30.5
- **Sửa lỗi không vào được game** (RC30.1–30.4): `noodle_hair.py` lệch checksum với `noodle_bundle.json` → mod dừng ở BLOCKED_MOD_NOT_READY. Từ bản này mỗi build đều được kiểm tra lại toàn bộ checksum trước khi đẩy.
- Y17: nhóm mạnh nhất Barcelona, Bayern, Juventus, Liverpool; Real (mất Ronaldo) xuống nhóm 2 cùng PSG, City, Atlético, Chelsea; Spurs, Roma, United nhóm 3.
- Không có tab/trang thống kê riêng nào; chỉ luật giải, tỉ số và người ghi bàn/kiến tạo trong My League của game.

## RC30.6
- **Áo Juventus My League (Y17)**: sân nhà = template trắng-đen bạn gửi (Jeep, Cygames sau lưng, scudetto, logo Serie A), sân khách = áo xanh camo bạn gửi dựng lại theo layout áo của game. Font số Adidas (như áo Real 2017), số đen trên áo nhà, trắng trên áo khách; có cả ảnh áo trong menu chọn áo.
- Kỹ thuật: giống cách áo Real 2017 (đội 351) — texture trong gói áo pc9303 + file đồng phục trong dt870, gắn vào đội ảo "eFootball FC KIT1" (5063) nên không đè áo của câu lạc bộ thật nào; Juventus Y17 trỏ áo sang đó.

## RC30.7
- **Sửa áo Juventus không đổi**: bảng "đội → áo" của My League được biên dịch cứng trong `libselect_team.so`, RC30.6 chỉ đổi file JSON nên game vẫn dùng áo cũ. Giờ vá cả trong `.so`.
- Font số áo Juve: đen trên áo nhà, trắng trên áo khách (RC30.6 lỡ dùng font xanh của Real).
- **Áo PSG Y17**: sân nhà = template bạn gửi (Fly Emirates, sọc đỏ giữa, Nike), số trắng; sân khách = bản trắng cùng logo, số navy. Gắn vào đội ảo "eFootball FC KIT2" (5064).
- **Neymar sang PSG** số 10 (cánh trái, PSG 2017/18), Mbappé cánh phải, Di María lùi giữa, Draxler dự bị, Lucas Moura rời đội. Neymar ~20% bàn và ~17% kiến tạo của PSG (mô phỏng: 13–15 bàn, 9–12 kiến tạo/mùa).
- **Barça kiểu 2018/19**: Ousmane Dembélé số 11 thay Neymar ở cánh trái.

## RC30.8
- **5 mặt GLB của bạn** chuyển bằng chính bộ chuyển GLB→mặt của V32 (chạy trên máy build), đóng thành mặt riêng như cách RC24 thêm Ronaldo 2007/2020, gắn vào 5 thẻ Cristiano Ronaldo chưa có mặt riêng:
  - Cris05 → thẻ 52784879636906 (profile RQ05, pc9504)
  - Criswc06 → thẻ 52847425098154 (RQ06, pc9505)
  - cris20 → thẻ 105802492809642 (RQ20, pc9506)
  - Cris21 → thẻ 106723780071850 (RQ21, pc9507)
  - Ronaldo_JR → thẻ 105773233344938 (RQJR, pc9508)
- 5 thẻ này được gắn sao sẵn trong Favorites của launcher (một lần; bỏ sao thì không tự thêm lại).
- Lưu ý: bộ chuyển V32 tự ghi chú mặt là "gameReady: false" (pháp tuyến/SRO tạm, khớp miệng chờ engine) — cần thử trên máy.

## RC30.9
- **Sửa lỗi không vào được game ở RC30.8**: 5 container mặt mới (pc9504–pc9508) chỉ được ghi vào release-manifest, thiếu trong ui6-runtime-manifest (danh sách file game giải nén ra máy) → lúc đăng nhập mod tìm không thấy pc9504 và dừng. Giờ ghi vào cả hai; bước kiểm tra trước khi đẩy cũng kiểm luôn điều này.

## RC30.10
**Launcher (thiết kế lại giao diện, không đổi tính năng)**
- Tông xanh biển mới cho mọi trang và mục con: Home, Players (danh sách, chi tiết, 5 tab Abilities/Positions/Skills/Boosters/Appearance), Player Catalogue, bộ lọc, các bảng chọn, Cards, Saves, Storage.
- Thanh trạng thái tài nguyên chỉ ở Home; trang con có tiêu đề gọn một dòng. Bỏ các lối tắt trùng với thanh dưới; mỗi lối tắt có icon riêng (UCL cúp, World Cup quả địa cầu, Match Settings thanh trượt).
- Tab không còn xuống 2 dòng; thanh "Select multiple / sắp xếp / lưới" gọn một hàng; giỏ hàng chỉ hiện khi đang chọn.
- Dọn chữ Trung/Việt lẫn trong Saves, Storage, Help.
- **Chống lag/chậm**: bỏ nền cố định khi cuộn, bỏ blur và đổ bóng nặng (nguyên nhân giật khi cuộn trong WebView); ảnh thẻ tải song song 8 ảnh, tải trước khi sắp cuộn tới; ảnh thẻ lấy từ mạng được **lưu lại trong máy** — lần sau hiện ngay, không chờ mạng.

**Mặt / ảnh thẻ**
- Thẻ **89138556572074**: mặt Ronaldo 2017 (profile NR17, cùng mặt của thẻ ảnh Honda 88042803047215) và ảnh thẻ của 89138288266704 (mini + ảnh lớn).
- 5 mặt GLB: sửa lỗi không hiện — material tóc HQ của bộ chuyển V32 cần texture `T_4522_Hair_High_SRO` (dữ liệu CR7 của V32) mà RC26 không có; giờ dùng material tóc như mặt Ronaldo 2007 của RC26 (không phụ thuộc gì thêm). Tất cả tài nguyên ngoài mà 5 mặt cần đều là tài nguyên mặt Ronaldo 2007 cũng dùng.
- Log chẩn đoán (`noodle-hair-status.json`) có thêm bộ đếm của hook mặt và profile/đường dẫn mặt gần nhất, để soi nếu còn lỗi.

**Nhập GLB trong Card studio (như V32)**
- Card studio có nút **◉ GLB Face**: nhập ID thẻ, chọn file .glb (≤32MB) → máy tự chuyển (bộ chuyển GLB của V32, chạy trên máy) → đóng và mở lại app là thẻ mang mặt mới. Tối đa 8 thẻ, có nút xoá.
- Kỹ thuật: thêm lớp mã hoá texture `FaceTextureCodec` của V32 vào `classes5.dex`; thư viện numpy/Pillow (gói requirements của V32, giữ nguyên các thư viện cũ); 20 module chuyển mặt của V32 đổi tên `v32_*` để không đụng module RC26; `libnoodle_hair.so` có 8 khe mặt động (RU01–RU08) mà Python điền ID thẻ lúc chạy.
- **Bản này có `classes5.dex` mới — nhớ chép cả `classes5.dex`.**

## RC30.11
- **Sửa lỗi màu ảnh Ronaldo đè ảnh Honda** (thẻ 88042803047215 và 88044950524330): ảnh bị lưu sai thứ tự kênh màu (đỏ/xanh đảo) nên da xanh, áo đỏ. Đã sửa, và tự thay trên máy đã lưu bản lỗi (ảnh bạn tự nhập cho 2 thẻ này thì giữ nguyên).
- **Chép ảnh thẻ** (Card studio → ◉ GLB Face → Copy card pictures): nhập ID thẻ nguồn và thẻ đích → chép cả ảnh mini lẫn ảnh thẻ lớn, lấy đúng ảnh gốc trong dữ liệu game (không có thì tải từ efootballhub). Thẻ 89138556572074 tự nhận ảnh gốc của 89138288266704 ngay lần mở đầu tiên.
- **Saudi Pro League** thay Eredivisie trong My League (giải 125), 34 vòng:
  - CLB thật trong game (đội hình, áo, logo gốc): Al Nassr, Al Hilal, Al Ahli, Al Ittihad.
  - 14 CLB đè lên đội Hà Lan (đổi tên trong game): Al Qadsiah (Feyenoord), Al Shabab (PSV), Al Ettifaq, Al Taawoun, Al Fateh, Al Khaleej, Al Fayha, Al Riyadh, Al Okhdood, Al Kholood, Damac, Al Najma, Neom, Al Hazem.
  - Ivan Toney (Al Ahli) và Julián Quiñones (Al Qadsiah) mỗi mùa 26–30 bàn; Al Nassr/Al Hilal mạnh nhất.
  - Logo 14 CLB đè: chưa có (game không có dữ liệu logo các CLB này; tải logo từ Wikipedia bị chặn).

## RC30.12
- **Kit Studio** (launcher → Shortcuts → Kit Studio): chọn giải (UCL, Saudi Pro League, World Nation League, Y17, Y08) → đội → Home/Away → chọn ảnh → Preview → Save kit. Đóng và mở lại app để thấy áo trong game.
  - "Shirt photo": ảnh áo thật (mặt trước, nền trơn; ảnh mặt sau tuỳ chọn). Thân trước lấy từ ảnh, thân sau lấy hoạ tiết áo, tay/quần/tất/cổ áo/số áo chỉnh màu được.
  - "Kit template": texture áo PES/eFootball (ảnh vuông) dùng nguyên.
  - Tối đa 80 áo tự tạo; nút Remove để trả lại áo gốc.
- **Real Madrid 2017 (Y17)**: áo sân khách tím 2016/17; áo sân nhà giữ nguyên.
- **Saudi Pro League**: Al Hilal mạnh nhất; top 5 luôn là Al Hilal, Al Nassr, Al Ittihad, Al Ahli, Al Qadsiah; khoảng 3 bàn/trận, hoà ~25%. Logo 14 CLB thay trong game. Al Okhdood → Abha, Damac → Al Faisaly, Al Najma → Diriyah (theo logo bạn gửi).
- **Transfer**: có thêm giải Saudi Pro League.
- **Thẻ 88044950524330**: ảnh thẻ Ronaldo Juventus 2020 (Big Time) và face GLB Ronaldo Juve 2020 (tự gắn ở lần mở app đầu tiên, hiện từ lần mở sau).

## RC30.13
- **Sửa lỗi không vào được game** (RC30.12: "Newer local live resource is missing or changed: pc9521"): bước kiểm tra tài nguyên lúc đăng nhập giờ tìm đúng container face GLB (pc9521–pc9528) và áo Kit Studio (pc9540) trong thư mục con của chúng.
- **Al Qadsiah**: tiền đạo cắm đá chính được thay bằng Julián Quiñones (ID 105624788652267) trong đội hình thật. App tự lưu thành một chỉnh sửa Transfer của giải 125 khi đã có ảnh chụp đội hình (vào game 1 lần → mở lại app → vào game).
- **Y17 – thẻ không có mặt**: Harry Kane dùng thẻ thường 47287 (thẻ cũ cần mẫu mặt không có trong dữ liệu). Cầu thủ không có mặt trong dữ liệu game được thay bằng cầu thủ cùng CLB có mặt: Chalobah → Loftus-Cheek, Begović → Zappacosta, Zouma → Tammy Abraham, Denis Suárez → Paulinho, Pjaca → Bernardeschi, Javi Martínez → Juan Bernat, Draxler → Paredes, Gaitán → Rodri, Mata → Daley Blind.
- **Giao diện**: toàn bộ hộp thoại Java của launcher (Transfer, chỉnh đội, Equipment, Single Player, Diagnostics…) có nền xanh biển bo góc, nút bo góc viền xanh, nút chính gradient, ô nhập bo góc. Catalogue gọn lại: nút ←, tiêu đề và số thẻ trên một dòng.
- **Bấm nhanh hơn**: thao tác người dùng (mở thẻ, danh sách, catalogue) luôn chạy trước. Ảnh thẻ chỉ tải khi rảnh, tối đa 2 cái một lúc, nên không còn xếp hàng sau ảnh.

## RC30.14
- **Sửa lỗi kẹt khi vào game sau đăng nhập**: game luôn tải container theo tên phẳng `/livedata/<tên file>`, nên container face GLB (pc9521…) và áo Kit Studio (pc9540) nằm trong thư mục con bị 404. Giờ chúng luôn có bản phẳng trong `livedata/` (file cũ trên máy được tự chuyển ở lần mở app tới), và khi xoá face/áo thì bản phẳng cũng xoá theo.

## RC30.15
- **Kit Studio và GLB Face nằm trong Card studio** (web view của launcher không có bộ chọn file, nên không chọn được ảnh). Nút "Kit Studio" và "GLB Face" ở launcher mở Card studio và tự mở đúng bảng. Trong Card studio còn có nút nổi "👕 Kit Studio" phía trên "◉ GLB Face".
- **Transfer · Edit Member → "Name & Shirt Name"**: đổi tên cầu thủ và tên in trên áo cho bất kỳ thẻ nào (không cần sở hữu). Lưu chung vào hồ sơ tên theo ID thẻ mà game áp dụng native; có hiệu lực từ lần vào game tiếp theo.
- **Ảnh thẻ tải nhanh hơn**: gom một lần gọi cho cả màn hình thẻ (tối đa 24) thay vì mỗi thẻ một lần. Ảnh lưu trong máy được thu nhỏ đúng cỡ hiển thị (nhỏ hơn khoảng 10 lần). Ảnh chưa có thì trình duyệt tải song song, không đi qua cầu nối.

## RC30.16
- **Sửa face GLB không hiện**: đầu chuyển từ V32 tham chiếu vật liệu lông mi `MI_Head_Eyelash04Occlusion00`, vật liệu này chỉ có ở V32, V19 không có. Thiếu gói này nên game bỏ qua cả cái đầu. Giờ mọi đầu GLB trỏ tới `MI_Head_Eyelash01Occlusion00` của V19 (giống đầu R7A2 vẫn chạy được):
  - 5 face Ronaldo tĩnh (pc9504–pc9508) đã build lại;
  - face nhập trong Card studio được sửa ngay lúc chuyển đổi;
  - face đã nhập sẵn trên máy (ví dụ Ronaldo Juve 2020, pc9521) tự được sửa ở lần mở app đầu tiên.
- Diagnostics giữ lại bộ đếm hook face (`rc30_stats`, `last_face_profile`, `last_asset_path`…) sau khi thoát game, để còn kiểm tra nếu face vẫn chưa hiện.

## RC30.17 (chẩn đoán face)
- Thư viện face (libnoodle_hair.so) ghi lại 32 ID thẻ gần nhất mà game đưa vào hook nạp đầu. Diagnostics hiển thị chúng ở `rc30_face_cards`, kèm bảng slot GLB (`rc30_glb_table`) và trạng thái ghi bảng (`rc30_glb_status`), giữ lại cả sau khi thoát game. Mục đích: biết chính xác ID mà game dùng khi nạp đầu cho các thẻ Ronaldo GLB.

## RC30.18
- Thẻ **88044145348047** dùng face **CR JR** (profile RQJR, container pc9508, dùng chung với thẻ 105773233344938).
- Vẫn giữ bộ ghi ID thẻ của hook face (RC30.17) để kiểm tra.

## RC30.19 (chẩn đoán face)
- Bản chụp hook face không còn bị phiên mở game không đá trận ghi đè. Danh sách `rc30_face_cards` ghi đủ 32 ô, kể cả ID 0.
