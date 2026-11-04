# UCL trong V23.1: đọc implementation, chưa tích hợp vào FULL-7

Nguồn: https://github.com/ron3huq/testingdummy/releases/tag/releasee — hai phần `73efootball-V23.1.part1.rar` và `.part2.rar`. Đã đọc central directory APK từ HTTP Range, lấy đúng Python bundle/UI DEX và bảng tên đội, kiểm tra kích thước/CRC ZIP. Không chép engine, APK, Python bundle hoặc DB nghiên cứu vào FULL.

## Cấu trúc giải

32 đội, 8 bảng ×4. Mỗi bảng đấu vòng tròn một lượt,3lượt,6trận/bảng. Đội người chơi ở index0/bảngA, mặc định thuộc pot2. Người chơi đá3trận vòng bảng và tối đa4trận knockout; tổng tối đa7trận trực tiếp. Các trận khác là mô phỏng offline theo sức mạnh đội/seed, không chạy engine cho từng trận AI.

Thắng3điểm, hòa1, thua0. Xếp thứ tự: điểm, hiệu số, bàn thắng, team ID tăng dần. Không thấy tiêu chí đối đầu trong `UclMode._table`.

Logic hiện tại `UclMode._qualify` yêu cầu đội đứng trong hai đội đầu bảng sau khi hoàn tất3trận. **Mô tả/docstring và `cup_entry._group_event` vẫn chứa "ít nhất5điểm", nhưng code xét vé hiện tại dùng top2.** Đây là bất nhất nội dung event, không nên hứa5điểm bảo đảm đi tiếp.

Knockout16đội: R16→QF→SF→FINAL, một trận mỗi vòng. Lượt16ghép nhất bảng với nhì bảng kế tiếp theo vòng A→B→…→H→A. Cặp có người chơi được đưa lên đầu danh sách để phục vụ nhánh native. Các vòng sau theo nhánh đã lập; không bốc lại mỗi vòng. Event bật hiệp phụ và penalty. Kết quả hòa ở knockout phải có kết quả luân lưu phân thắng bại; dữ liệu penalty không hợp lệ bị từ chối.

## Danh sách đội

`UclService._select_opponents` có pool ưu tiên41CLB; chọn31đội khác đội người chơi và có tên hợp lệ, cộng đội người chơi thành32. Danh sách còn qua bước remap đội châu Âu hợp lệ của native trong `_ensure_entered`; vì thế đây là pool ưu tiên, không phải luôn đủ41đội hay một danh sách32đội cố định.

Thứ tự ưu tiên (tên CLB thông dụng; một số tên game là tên không bản quyền):

1. Real Madrid109
2. Bayern127
3. Manchester City173
4. Liverpool103
5. Barcelona108
6. PSG114
7. Inter119
8. Arsenal101
9. Manchester United100
10. Chelsea102
11. Dortmund126
12. Leverkusen128
13. Atlético172
14. Juventus120
15. Milan121
16. Napoli327
17. Atalanta234
18. Tottenham179
19. Newcastle106
20. Aston Villa107
21. Roma125
22. Benfica191
23. Porto192
24. Sporting193
25. Monaco112
26. Marseille113
27. Ajax116
28. PSV118
29. Feyenoord117
30. Lazio122
31. Lyon181
32. Sevilla265
33. Villarreal267
34. Real Sociedad196
35. Galatasaray130
36. Fiorentina124
37. Stuttgart231
38. Lille213
39. Club Brugge269
40. Frankfurt226
41. Fenerbahçe197

Các preset đối thủ được đọc từ70preset Division và ghép bằng alias/tên đội. Sức mạnh dùng trung bình `_overall`11cầu thủ đầu; thiếu thông tin thì fallback80. Đội người chơi cũng tính trung bình11cầu thủ đầu, fallback80. Không lấy dữ liệu UCL ngoài đời hay kết quả Internet.

`_draw_groups` chia4pots, giữ chỗ người chơi ở pot2, thử tối đa400lần để giảm trùng quốc gia trong bảng. Tìm được0xung đột thì dừng; nếu không có thì lấy phương án ít xung đột nhất. Đây là ràng buộc mềm, không phải đầy đủ quy định UEFA. Không thấy ràng buộc quốc gia tương tự trong bước ghép R16.

Có thể đổi đội trong danh sách trước khi bắt đầu; code từ chối đổi danh sách đội khi đã chơi. Native plan cần11–40player IDs hợp lệ và gameplan, không chỉ đổi tên/crest.

## Đường event, UI và tiến trình

Event1120006 cho vòng bảng,1120007 cho knockout. Knockout chỉ hiện sau khi đủ điều kiện. Event cũ1120005 không còn được chiếu ra danh sách mới. Trạng thái có GROUP, QUALIFIED, ELIMINATED và CHAMPION.

Trang group native dạng UserCompe bị trống khi dùng EventCompe. V23.1 khắc phục bằng bridge mượn bảng/lịch MyLeague: sao lưu mùa thật, mở một mùa4đội/3lượt riêng, chuyển6kết quả bảng về UCL rồi khôi phục mùa thật. Có đường release/restore nếu thoát group. Việc port cần kiểm tra backup/restore, league scope và các thay đổi MyLeague sẵn có, không chép nguyên module sang nền này.

Vào lại event là resume, không tự reset giải. State/receipt trong SQLite; kết quả gửi trùng không được cộng hai lần. Trận bị gián đoạn chưa có kết quả hợp lệ giữ pending. Có lưu bản ghi chức vô địch trong `e112_cup16_trophies`; chưa thấy cơ sở để khẳng định có thưởngGP/coin riêng. Các reward list trong projection event đang rỗng.

Có7tùy chọn CPU: VERYEASY/EASY/NORMAL/HARD/VERYHARD/HARDEST/LEGEND, mặc địnhNORMAL. Việc có field/tùy chọn không chứng minh mức khó thực tế trên điện thoại; đặc biệt group dùng bridgeMyLeague phải đối chiếu đường mức khó của mùa mượn.

## Giới hạn xác minh

Đã đọc code và các điều kiện nhánh thực tế; chưa kiểm chứng hoàn chỉnh UCL trên điện thoại. FULL-8RC7 chỉ chứa báo cáo này, không tích hợp UCL hay đổi nền FULL-7. Các module nghiên cứu chính: cup_entry, ucl_mode, ucl_service, ucl_group_bridge, cup16_mode, cup16_service và e112_cup_runtime_compat.
