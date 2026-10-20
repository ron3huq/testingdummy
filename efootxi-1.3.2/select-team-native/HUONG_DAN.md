# Bản thử sửa trực tiếp Select Team — Android efootxi 1.3.2 ARM64

**CẬP NHẬT 20/10/2026: người dùng đã xác nhận Select Team hoạt động trên Android không root.** Kiểm tra ARM64 tự động chỉ xác minh thành phần; xác nhận màn hình là báo cáo từ người dùng, chưa có xác nhận riêng về mọi luồng vào trận. ZIP native ban đầu giữ nguyên để truy vết, nên tài liệu trong ZIP vẫn có nhãn thử nghiệm tại thời điểm đóng gói.

## Nó thay gì?

Khi mở danh sách đội của My League, sửa đúng danh sách Pháp 18 đội trong bộ nhớ sang 18 đội Super League đã có trong registry người dùng gửi. Giữ nguyên packed word của mỗi đội để không chỉ đổi chữ hiện trên màn hình. Hàm gốc tiếp tục lấy danh sách từ chính bộ nhớ đã sửa. Không thay CPK, SQLite, save, lịch đấu, APK hay file libUE4 trên ổ đĩa. Chỉ kiểm tra thành công việc trả về danh sách đội; logic xác nhận lựa chọn/vào trận trên máy thật vẫn cần kiểm chứng.

Đội đích theo đúng thứ tự registry: Arsenal, Chelsea, Liverpool, PSG, Manchester United, Manchester City, Tottenham, Barcelona, Real Madrid, Atlético, Milan, Inter, Juventus, Lyon, Monaco, Roma, Napoli, Galatasaray.

Chỉ tác động lớp native My League và danh sách có đầy đủ 18 ID Pháp gốc. Nếu sai hash libUE4, sai mã hàm, thiếu đội, có packed ID mâu thuẫn hoặc không cấp được bộ nhớ thực thi thì từ chối cài/sửa tương ứng. Android vẫn có thể từ chối nạp `.so` hoặc chặn sửa bộ nhớ; đây chưa phải điều đã thử trên máy của bạn.

## Cách thử bằng MT Manager, không root

1. **Khôi phục dt200 gốc và xác nhận game mở được trước.** Buộc dừng game. Không dùng hai bản dt200 thử trước đây.
2. Giải nén ZIP. Mở **bộ nhớ nội bộ mà DocumentsProvider của efootxi cung cấp**, tên `73efootball 资源` trong trình chọn tệp hệ thống. Tìm `files/embedded-gateway/work/tools`. Đường dẫn vật lý là `/data/user/0/com.efootxi.game/files/embedded-gateway/work/tools`; đường dẫn này cần mở qua provider của ứng dụng trên máy không root. **Không chép vào `Android/data/.../files`**: đó là vị trí khác. Nếu MT Manager không mở được provider này, dừng tại đây; chưa có cách cài đã kiểm chứng qua đường dẫn ngoài.
3. Sao lưu riêng `gateway_runtime.py` đang có. Chỉ dùng gói này nếu file đó là bản 1.3.2 gốc: 2441 byte, SHA-256 xem `BASELINE.json`. Không ghi đè nếu bạn đã tự sửa file này.
4. Chép đúng **ba file trong `install/work/tools/`** vào thư mục tools vừa tìm: `gateway_runtime.py`, `select_team_runtime.py`, `libselect_team.so`. Không chép cả gateway, không thay DB, không thay `installed-release.txt` hoặc release ID.
5. Mở game mới, vào My League → Select Team → giải Pháp. Nếu nạp thành công và dữ liệu đúng, danh sách này phải là 18 đội Super League. Cần giữ registry/lịch Super League bạn đã sửa; gói này chỉ sửa menu, không tự cài registry/lịch.
6. Sau khi mở menu, đọc `select-team-status.json` trong cùng thư mục tools. File này phân biệt lỗi nạp với lỗi nhận diện menu. Nếu vẫn còn đội cũ, hãy gửi nội dung file này. Nếu không có file, kiểm tra lại vị trí cài và xem `gateway_runtime.py` có bị khôi phục không.

`gateway_runtime.py` giữ nguyên hàm xử lý URL gốc, chỉ thêm khởi động module thử. Chú thích/docstring được rút gọn và giữ nguyên kích thước file vì GatewayGuard 1.3.2 kiểm tra kích thước các file hỗ trợ trước khi tự phục hồi. Hash file thử khác bản gốc; không coi đây là xác minh checksum manifest. Cơ chế phục hồi/cập nhật có thể vẫn đưa file gốc trở lại. Không đổi release ID để ép cài lại vì có thể chép lại dữ liệu gói.

## Đọc chẩn đoán

- `WAITING_FOR_LIBUE4`: đang chờ thư viện game trong cùng tiến trình.
- `INSTALL_FAILED`: xem `error`; thiếu quyền nạp `.so`, quyền sửa code hoặc sai hash sẽ dừng trước khi cài hook trong các trường hợp đó. Nếu lỗi nêu rõ đã cài hook nhưng không khôi phục được quyền trang, buộc dừng game và gỡ bản thử.
- `HOOK_ACTIVE`, `menu_calls = 0`: hook đã cài nhưng chưa quan sát được lời gọi đúng lớp My League; chưa chứng minh danh sách đã đổi.
- `result = 1`, `patched_contexts >= 1`: đã sửa một danh sách trong bộ nhớ. Vẫn phải kiểm tra màn hình và đội thực sự được chọn.
- `result = 2`: thấy danh sách đích ở lần gọi tiếp theo; không ghi lại.
- `result = 3`: thiếu đội đích; `4`: cùng ID có packed word mâu thuẫn; `5`: không thấy đủ danh sách Pháp gốc; `7`: chế độ danh sách đặc biệt; `8`: vector không đúng giới hạn; `9`: nhiều danh sách Pháp trùng khớp. Các trường hợp này không ghi danh sách.

Cờ `device_verified` luôn là false: bộ cài không tự tuyên bố đã kiểm chứng điện thoại chỉ vì cài được hook.

## Gỡ bản thử

Buộc dừng game. Khôi phục `gateway_runtime.py` đã sao lưu; bản gốc kèm trong `restore/gateway_runtime.py` chỉ dùng nếu trước đó bạn dùng đúng bản gốc 1.3.2. Xóa `select_team_runtime.py`, `libselect_team.so` và `select-team-status.json`. Mở lại game; mọi thay đổi bộ nhớ mất khi tiến trình kết thúc. Không gỡ cài đặt ứng dụng và không xóa dữ liệu.

Nếu bị đen màn hình sau khi cài gói này, gỡ ba file như trên trước khi thử bất kỳ thay đổi nào khác. Gói không sửa file dữ liệu game trên ổ đĩa nhưng vẫn là native hook chưa qua thử nghiệm thiết bị, nên có thể gây crash/treo do tích hợp hoặc layout thực tế khác mô phỏng.

## Kiểm tra đã thực hiện

`native-validation.json`: thực thi getter ARM64 gốc, mã C đã biên dịch và toàn bộ đường gọi detour/trampoline với vector tổng hợp. Kiểm tra danh sách gốc/đích, hai bộ chỉ số home/away, không đổi giải khác, gọi lại không sửa lặp, và từ chối các dữ liệu thiếu/mâu thuẫn/sai lớp/vector lỗi. Không có Android UI, thiết bị, API xác nhận đội hay trận đấu trong kiểm tra này.

`package-validation.json`: kiểm tra hash, mã nhánh và giới hạn khoảng cách, AST hàm gateway không đổi, kích thước file và cú pháp Python.

Để chạy lại kiểm tra native: Python có `unicorn`, `pyelftools`; giải nén libUE4 ARM64 của APK 1.3.2, chạy `python check_menu_native.py --libue4 /duong/dan/libUE4.so` trong thư mục source. Biên dịch lại bằng Python package `ziglang==0.13.0`, chạy `sh build.sh`; nếu binary thay đổi phải cập nhật `HOOK_SHA` trong loader và chạy kiểm tra lại. Thư viện không phụ thuộc libc, không có undefined symbols/relocations và dùng segment alignment 64 KiB.
