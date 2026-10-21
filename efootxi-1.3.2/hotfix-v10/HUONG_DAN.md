# Native hotfix v10 — mô phỏng My League

Bản này cập nhật kết quả CPU và phân bổ ghi bàn/kiến tạo cho bốn giải. Kế thừa nguyên binary native v9; không thay đội hình, số áo, vị trí, thông thạo gốc, chỉ số, áo/logo, tên giải hoặc sân/thời tiết. Không thay dt200/CPK/APK/DB; không xóa save.

## Cài bằng MT Manager, không root

1. Buộc dừng efootxi. Sao lưu đủ 7 file hiện tại.
2. Giải nén ZIP. Chép **đủ 7 file trong `install/work/tools/`** vào thư mục `files/embedded-gateway/work/tools/` của bản efootxi đang dùng (đường dẫn cũ của bạn có tiền tố `73efootball 资源/`). Ghi đè file cùng tên, không lồng thêm thư mục.
3. Mở lại game. Trong `work/tools/select-team-status.json`, kiểm tra `version: native-hotfix-v10` và `state: HOOK_ACTIVE`.
4. Kết quả mới áp dụng cho vòng CPU chưa hoàn tất. Trận đã lưu, lịch mùa hiện tại, trận đã chuẩn bị và bảng ghi bàn đã chốt không được tính lại. Không cần bắt đầu mùa mới; muốn đánh giá toàn mùa thì dùng mùa mới khi thuận tiện.
5. Cứ sau 5 vòng hoàn tất, lần đọc My League tiếp theo cập nhật `work/tools/myleague-simulation-status.json`: tỷ lệ hòa, chủ nhà thắng, bàn/trận và các tỷ số đã xảy ra. Đây là thống kê các trận đã lưu, bao gồm trận bạn chơi, không phải báo cáo thẻ đỏ/phút ghi bàn.

Nếu phát sinh lỗi, buộc dừng rồi phục hồi **đủ 7 file** đã sao lưu. Giữ save hiện tại.

## Phân nhóm

**Ligue 1 / Uefa Champion League — 18 CLB:**

1. Arsenal, Barcelona, PSG.
2. Real Madrid, Manchester City, Bayern Munich.
3. Atletico Madrid, Chelsea, Liverpool, Inter.
4. Juventus, AC Milan, Borussia Dortmund.
5. Napoli, Galatasaray, AS Roma.
6. Tottenham.
7. Manchester United.

Mô hình mới thay quy tắc 70%/85%/95% trước đó. Nhóm1–2 có prior trung bình55%/28%/17%; nhóm1 sân nhà nhỉnh hơn, sân khách cân hơn. El Clasico giữ cân bằng trước lợi thế sân nhà/phong độ. Các cặp derby được thu hẹp chênh lệch. Arsenal/Atletico/Inter/Juve thiên về tỷ số chặt; Barca/PSG/Dortmund/Spurs thiên về trận mở. Liverpool, Bayern, Roma, Dortmund, Gala, Napoli có hệ số sân nhà riêng.

**Scottish / Y17 Champion League — giữ 12 đội, 22 vòng:**

1. Real Madrid, Barcelona, Juventus.
2. Bayern Munich, Manchester City, PSG.
3. Atletico Madrid, Chelsea, Liverpool.
4. AS Roma, Tottenham.
5. Manchester United.

Không thêm Dortmund/Napoli/Milan/Galatasaray vì không có các đội này trong 12 vị trí Scottish hiện tại. Ronaldo/Messi là ưu tiên ghi bàn hàng đầu; các chân sút retro khác bám đuổi. Không nhập cầu thủ hiện đại hoặc thay roster trong bản này.

**Giải tuyển châu Á / AFC Nation League — giữ 18 tuyển:**

1. Nhật Bản.
2. Uzbekistan, Hàn Quốc, Saudi Arabia, Qatar.
3. Iran, Australia, Iraq, UAE.
4. Indonesia, Thái Lan, Malaysia, Việt Nam, Trung Quốc, Jordan.
5. Singapore, Hong Kong, Triều Tiên.

Nhật gặp nhóm4 có prior85% thắng/15% hòa/0% thua; nhóm3 là70%/15%/15%; nhóm2 là65%/22%/13%. Việt Nam–Thái Lan–Indonesia cân bằng trước lợi thế sân nhà/phong độ. Oman/Syria/Bahrain không được tự thêm vào giải.

**Giải tuyển thế giới / World Nation League — giữ 20 tuyển:**

1. Tây Ban Nha.
2. Pháp, Anh, Argentina.
3. Bồ Đào Nha, Đức, Bỉ, Brazil.
4. Hà Lan, Ý, Croatia, Uruguay.
5. Colombia, Mexico, Maroc.
6. Senegal, Hoa Kỳ.
7. Na Uy, Thụy Điển, Georgia.

Theo lưu ý cuối tệp yêu cầu, giữ các đội đang có thay vì nhập Nhật/Thụy Sĩ/Iran. Ưu tiên Mbappe/Kane/Haaland, tiếp theo Messi và các ngôi sao đã nêu. Yamal/Olise được ưu tiên kiến tạo; có pha phong độ cầu thủ ổn định theo từng4 vòng. Haaland có tỷ trọng ghi bàn lớn cho Na Uy, nhưng không ghi nhiều hơn tổng bàn thật của đội.

Asia-Pacific549 và Eredivisie125 giữ mô hình trước đó.

## Cách sinh kết quả và giới hạn

- Dùng nhóm, lợi thế sân nhà, phong độ5 trận đã chơi, pha phong độ4 vòng và phong cách đội. Kết quả ổn định khi mở lại cùng trạng thái mùa; không quay số lại mỗi lần đọc màn hình.
- Bộ chọn cả vòng tìm phương án gần quota2–3 hòa/1 trận1-0/1 trận4+ bàn/1 khách thắng/1 trận cả hai ghi2+, hạn chế lặp tỷ số và cách biệt. Scottish chỉ6 trận/vòng nên quota hòa là1–2. Trận của bạn không bị giả lập hay sửa để đủ quota.
- Phản hồi5 vòng điều chỉnh phân bố gần22% hòa,45% chủ nhà thắng,33% khách thắng,2,8 bàn/trận. Các tỷ lệ là mục tiêu xấp xỉ; quota và phong độ có thể làm thay đổi prior đối đầu. Không ép bảng xếp hạng hay điểm vô địch.
- Cú sốc lớn được định nghĩa đội yếu hơn ít nhất3 nhóm thắng; giới hạn tối đa2 trận CPU trong cửa sổ10 vòng, tính cả lịch sử thật. Nếu lịch sử đã vượt ngưỡng, không sinh thêm cú sốc lớn cho đến khi ra khỏi cửa sổ. Trận bạn trực tiếp chơi luôn giữ nguyên.
- Ligue1 thường tối đa5 bàn/đội, đôi lúc6 khi chênh lệch lớn; 4-4/6-2/7-1 và chiều ngược là ngoại lệ hiếm, giới hạn2 trận CPU/mùa. Scottish, châu Á, thế giới tuyệt đối tối đa5 bàn/đội.
- Lượt về tránh lặp đúng tỷ số theo góc nhìn cùng đội; tránh3 trận liên tiếp cùng tỷ số. Cặp nhóm đầu có lượt đi chưa0-0 hoặc4+ bàn sẽ được ưu tiên một trong hai loại ở lượt về. Không sửa lượt đi đã lưu.
- Sự kiện ghi bàn/kiến tạo chỉ dùng đúng full64 ID có mặt trong roster, tổng bàn cầu thủ bằng bàn đội; thủ môn không tự trở thành chân sút. Biên nhận cũ và sự kiện trận bạn chơi giữ nguyên.
- Không tạo dữ liệu giả về chấn thương, sa thải HLV, thẻ đỏ, penalty, bàn phút90 hoặc phản lưới. Gateway hiện chưa có nguồn sự kiện tương ứng để hiển thị trung thực. Do đó không gắn lời giải thích bịa vào tỷ số.
- Không bảo đảm mọi mùa cùng đạt86–97 điểm vô địch, MU26–34 điểm, hoặc đúng số bàn/kiến tạo mục tiêu. Scottish22 vòng cũng khác độ dài mùa34 vòng. Các báo cáo công bố số thực đo, kể cả khi lệch mục tiêu.

## Kiểm tra

`validation/simulation-validation.json` ghi6 mùa mỗi giải, tổng6.744 trận; kiểm tra snapshot/save, cú sốc, thành viên roster và sự kiện bảng xếp hạng qua gateway thật trên bản DB sao chép. Native bridge được giả lập trong bài kiểm tra gateway; chưa chạy trên điện thoại.

Ligue1 trong mẫu: hòa22,22%; chủ nhà44,44%; khách33,33%; trung bình2,806 bàn/trận;204/204 vòng đạt quota. Vua phá lưới và điểm cuối mùa còn dao động; xem số thực trong báo cáo, không coi đây là cam kết mùa của bạn.

Các kiểm tra native v9 được giữ dưới nhãn `baseline-v9/` vì `libselect_team.so` và `select_team.c` byte-identical. Bản này không tuyên bố đã khắc phục texture áo còn thiếu hay xác nhận mưa/ánh sáng trên Android.
