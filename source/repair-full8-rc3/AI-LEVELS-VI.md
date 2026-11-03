# Độ khó AI trong APK73

Engine libUE4.so SHA256 efd257d9e41b622d6ecb8f51f7b0a8ee8820113fd427c5572025df1c8eecc7b8 có enum EMenuCpuLevel::CPU_LEVEL_*. Gateway ai_division trong app.imy có bảy tên: VERYEASY, EASY, NORMAL, HARD, VERYHARD, HARDEST, LEGEND.

Hàm ai_division.prepare ghi LEVELS[active['division']] vào saved['cpu_level'] và resp['cpu_level'] trước trận. Ánh xạ AI Division: hạng10 VERYEASY;9/8 EASY;7 NORMAL;6 HARD;5/4/3 VERYHARD;2 HARDEST;1 LEGEND. Đây là hạng Division được ánh xạ vào bảy mức AI, không phải mười thuật toán AI riêng.

Công tắc AI native (flag15 trong single_player) là trạng thái điều khiển, không phải trường cpu_level này. Các LEVELS Terrible/Bad/Normal/Good/Excellent trong myleague_condition là phong độ cầu thủ, không phải độ khó AI.

Đã kiểm tra enum trong binary và đường sinh dữ liệu trước trận trong bytecode gateway. Chưa đo hành vi/độ khó từng mức trên điện thoại, chưa xác nhận engine dùng cùng ánh xạ ở mọi chế độ. RC3 không thay độ khó hoặc thêm menu chỉnh độ khó.

## Kiểm tra sâu sau yêu cầu mới

Đã chạy hàm my_league.prepare thật với biên lưu mùa giải tổng hợp cho cả7mức: giá trị chọn đi vào response đối thủ và state.active.opponent.cpu_level; thiếu yêu cầu mới giữ mức cache, giá trị không hợp lệ bị từ chối. Giá trị dự phòng trong mã là NORMAL; không thể suy ra save hiện tại của người dùng đang dùng mức nào từ mặc định đó. Adapter myleague_73.prepare gọi hàm gốc, không ghi đè cpu_level.

Trong engine73, enum tương ứng0..6 (VERYEASY..LEGEND); normalizer0x389a154/0x389a16c loại giá trị ngoài dải về NORMAL2. Đã thực thi setter/getter native0x7b80140/0x7b7cc70 (global setting ở context+0x48→0x1cfd) và0x7b7f780/0x7b7cc90 (event setting ở+0x1d00), đọc lại đúng0..6. Đây là cấu hình native thực, chưa phải thước đo hành vi AI.

Đã lần từ UFunction SetCpuLevel/GetCpuLevel qua0x32a6ba0/0x32a6b7c tới engine getter0x73a9ba4. Getter chọn mức theo chế độ; có nhánh lấy mức tối thiểu bằng max(setting, level trong dữ liệu sự kiện) tại0x73a9cc4..0x73a9cdc. Binary cũng đọc boss_match_cpu_level và minimum_cpu_level. Không được mặc định mọi nhánh này đều áp cho mọi trận MyLeague: điều kiện sự kiện/boss cần runtime cụ thể.

RC3 thêm observer chỉ đọc cho getter0x73a9ba4: giữ nguyên kết quả trả về, ghi số lần gọi/mức cuối/competition đang active vào cached_gameplan diagnostics, cùng hai setting global/event. Không gọi getter nặng từ background thread và không ép mức. Các trường native_computed_cpu_* phản ánh lần engine tự gọi GetCpuLevel gần nhất; competition0 có thể là menu. Không được coi chúng là mức AI trên sân nếu chưa khớp trận/thời điểm.

Bài test observer chạy thân GetCpuLevel ARM64 gốc ở nhánh global, biên nhận diện mode được giả lập; cả7giá trị trả về giữ nguyên, dữ liệu setting không bị sửa. Nhánh minimum/boss chưa được thực thi trong fixture.

ml_career.simulate_score chỉ đưa level vào seed SHA256 rồi lấy hai byte modulo4 để mô phỏng tỉ số nền. Nó không có hệ số làm mức cao luôn thắng nhiều hơn. ml_event.level_reward có quà10..60điểm/100..600fans khi WIN theo7mức; đây là module sự kiện, không phải chứng minh AI trận thực khó hơn hoặc quà mọi chế độMyLeague đều giống nhau.

**Kết luận hiện có:** đã chứng minh7mức được truyền/lưu và có cấu hình/getter native riêng. Chưa chứng minh thay level làm AI quyết định/chạy/phòng ngự khác nhau trong trận MyLeague thật trên điện thoại. Không dùng tỉ số mô phỏng, tên enum, quà thưởng hoặc lưu thành công để khẳng định điều đó. Cần đối chiếu lần engine tính mức trong đúng trận và hành vi trận thực.
