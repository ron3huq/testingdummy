# Nâng cấp My League: lịch ngẫu nhiên, kết quả CPU và vua phá lưới

Dành cho **Android efootxi 1.3.2**, trên bản Select Team native bạn đã xác nhận chạy tốt. Không thay `dt200`, `dt870`, registry, cầu thủ, save hoặc hai file native Select Team. Bản Select Team giữ nguyên; **phần nâng cấp Python này đã kiểm tra phía gateway, chưa xác nhận trên điện thoại**.

## Ba thay đổi

1. **Lịch mùa mới được bốc ngẫu nhiên một lần rồi lưu.** Thay đối thủ theo từng vòng bằng hoán vị đội trên lịch vòng tròn gốc đã kiểm chứng; giữ đủ lượt đi/lượt về, sân nhà/sân khách, số vòng, vòng nghỉ và chất lượng chuỗi sân của lịch gốc. Cùng một mùa không đổi lịch khi thoát/mở game hay xem lại menu. Mùa hiện tại đã có lịch lưu sẽ giữ nguyên; muốn có lịch mới thì bắt đầu mùa mới bằng chức năng có sẵn trong game.
2. **Trận CPU xét sức mạnh đội hình.** Ước tính công/thủ từ đội hình chính, chỉ số base card trong dữ liệu đi kèm game, lợi thế sân nhà, phong độ mùa và biến động từng trận; lấy số bàn bằng phân phối Poisson. Không dùng phép `%4` theo ID đội nữa. Đội mạnh có lợi thế nhưng vẫn có thể hòa/thua; không ép Barcelona/PSG/City/Arsenal thắng hoặc đứng đầu. Super League có nhiều đội mạnh nên vị trí thay đổi giữa các mùa.
3. **Bàn thắng/kiến tạo CPU xét chất lượng cầu thủ và thời lượng thi đấu ước tính.** Đội hình chính, vai trò CF/cánh/hộ công, chỉ số dứt điểm/tấn công/chuyền và chất lượng base card quyết định trọng số. Dự bị vẫn có cơ hội nhỏ; thủ môn không được phân bàn thắng giả. Dùng đúng ID và danh sách cầu thủ native của từng CLB, không gán người từ CLB khác chỉ để đưa tên nổi tiếng lên bảng.

Đây là mô hình offline theo dữ liệu bản mod, không phải dự báo được hiệu chỉnh bằng thống kê bóng đá ngoài đời. Khi không có hồ sơ base card, dùng ước tính trung tính; dữ liệu CLB/cầu thủ trong bản mod có thể khác đội hình bóng đá thực tế. Không truy cập mạng khi mô phỏng.

## Mùa bạn đang chơi dở

**Giữ nguyên lịch, tỷ số, điểm, số bàn/kiến tạo đã được ghi nhận, đội hình và trận đang chuẩn bị.** Các trận CPU chưa hoàn tất sử dụng mô hình mới; một tỷ số CPU đang xem trước nhưng chưa chốt có thể thay đổi khi cài bản nâng cấp. Kết quả mới sẽ ổn định sau đó qua các lần xem/khởi động lại.

Bảng vua phá lưới sẽ cải thiện dần từ các vòng tiếp theo. Không tự viết lại 10 vòng cũ để đẩy các ngôi sao lên top. Sửa lịch chỉ áp dụng khi tạo mùa mới. Bắt đầu mùa mới cũng cho bảng xếp hạng cầu thủ của mùa mới.

**CLB bạn điều khiển dùng cầu thủ Dream Team thực tế bạn đưa vào sân.** Bàn của đội bạn và đối thủ khi bạn đá trực tiếp vẫn lấy từ sự kiện trận thật. Ví dụ chọn Barcelona không làm Yamal/Raphinha tự có bàn nếu bạn không dùng và ghi bàn với họ trong đội hình của mình. Phần mô phỏng chỉ áp dụng các trận CPU khác, đúng điều bạn yêu cầu.

## Cài bằng MT Manager — chỉ cập nhật hai file

1. Buộc dừng game, hoàn tất trận đang đá trước khi cập nhật. Không xóa dữ liệu hay cài lại game.
2. Vào đúng vùng nội bộ đã cài Select Team thành công: `73efootball 资源` → `files/embedded-gateway/work/tools` qua trình chọn tệp/provider của ứng dụng. Không dùng `Android/data` thay thế đường dẫn này.
3. Sao lưu riêng `gateway_runtime.py` đang hoạt động. Để nguyên `select_team_runtime.py` và `libselect_team.so`.
4. Chép **hai file** từ `install/work/tools/` vào tools: `gateway_runtime.py` và `myleague_realism.py`. Không chép toàn bộ thư mục gateway. Không thay DB, CPK, `installed-release.txt` hoặc release ID.
5. Mở game, kiểm tra `myleague-realism-status.json` trong cùng thư mục: `state: INSTALLED` xác nhận đã nạp mô hình Python, chưa tự chứng minh toàn bộ màn hình Android hoạt động. Nếu có `myleague-realism-error.txt`, gửi nội dung lỗi. Tệp lỗi cũ có thể còn sau một lần thử trước; hãy xem thời gian cập nhật.
6. Tiếp tục mùa hiện tại để có CPU và phân bổ bàn mới. Khi bắt đầu mùa mới bằng game, lịch sẽ bốc lại và giữ ổn định trong mùa đó.

`gateway_runtime.py` giữ nguyên lời gọi bản sửa Select Team và các hàm URL, thêm lời gọi module mới. File vẫn **2441 byte**, phù hợp kiểm tra kích thước file hỗ trợ của GatewayGuard 1.3.2. Các module My League gốc được kiểm tra SHA-256 trước khi gắn mô hình, nên bản nguồn khác sẽ bị từ chối thay vì áp dụng nhầm. Không sửa manifest/hash CPK.

## Gỡ riêng bản nâng cấp này

Buộc dừng game, khôi phục `gateway_runtime.py` đã sao lưu. Gói có `restore/gateway_runtime.py` là bản trước nâng cấp, **vẫn gọi bản sửa Select Team**; chỉ dùng nếu đó là bản bạn đã cài trước đây. Xóa `myleague_realism.py` và hai file chẩn đoán. Để nguyên hai file native Select Team. Mở lại game.

Kết quả trận đã chốt khi dùng mô hình mới được giữ, không hoàn tác. Lịch đã tạo cho mùa mới vẫn là lịch của mùa đó dù gỡ module; không có thay đổi dữ liệu không thể đọc bằng gateway gốc. Không cần khôi phục DB để gỡ.

## Kiểm chứng

Xem `validation.json`: kiểm tra mọi giải trong registry giữ đủ cặp đấu/hai lượt, lịch lưu/đọc lại ổn định, 100 seed khác nhau cho 100 lịch khác nhau, giữ 10 vòng đã chơi và active match. Dùng bản sao DB để chạy select/resume, mở lại save, chuẩn bị đối thủ, chốt thống kê CPU và thử lại receipt; bàn cầu thủ cộng đúng bằng tỷ số CLB, không ghi lặp, không thay bảng cầu thủ/vật phẩm hay file nguồn. Các sự kiện trận thật vẫn được giữ nguyên.

Đã chạy thêm 300 mùa Super League **toàn CPU** để khảo sát lợi thế sân nhà, tỷ lệ hòa, biến động điểm và sự tham gia ghi bàn của sáu cầu thủ bạn nêu. Đây không phải 300 mùa chạy trên điện thoại và không mô phỏng bàn của CLB người dùng. Không bảo đảm tất cả ngôi sao luôn vào top hoặc không có mùa phong độ kém.

Chạy lại: `python validate_realism.py --gateway /duong/dan/gateway-release --seasons 300`. Chỉ dùng gateway đúng 1.3.2 cùng dữ liệu đã gửi; kiểm tra tạo DB tạm, không ghi vào save nguồn. Đặt `myleague_realism.py` cạnh script kiểm tra. Phần nâng cấp chỉ dùng Python standard library và các module sẵn trong gateway.
