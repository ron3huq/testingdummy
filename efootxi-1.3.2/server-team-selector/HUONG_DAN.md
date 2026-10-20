# Chọn đội My League qua logic máy chủ — efootxi 1.3.2

**Đây là phương án khác, không sửa dt200/dt870 và không thay danh sách Select Team nguyên bản.** Công cụ chọn đội trong một bản sao save bằng đúng hàm `my_league.select` của gateway Android. Mục tiêu là để game đọc một mùa giải đã chọn đúng đội, thay vì tiếp tục vá bảng nhị phân khiến game đen màn hình.

Đã kiểm tra phía máy chủ: Arsenal (101) vào Ligue 1 (122), 18 đội, 34 vòng; mở lại save, đọc thông tin mùa giải và chuẩn bị đối thủ thành công. Các bảng cầu thủ/vật phẩm không đổi. **Chưa kiểm chứng giao diện Android nhận save này hoặc chơi được trận thật.**

## Chuẩn bị

- Khôi phục dt200 gốc; game phải vào bình thường trước khi thử hướng này.
- Dùng Python 3.10 trở lên trên máy tính, cùng thư mục `gateway-release` đã giải nén từ đúng bản Android, chứa `work/tools/my_league.py` và `outputs/reference/ziru-data/`.
- Dùng **save đang chơi của chính bạn**, xuất sau khi đóng hẳn game. Không dùng save seed trong APK hoặc save mẫu trong `outputs.rar` thay cho save hiện tại: nó có thể không chứa cầu thủ/tiến độ của bạn.
- Sao lưu save gốc. Công cụ chỉ đọc đầu vào và tạo đường dẫn đầu ra mới; nó từ chối ghi đè file có sẵn, sai phiên bản mã hoặc dữ liệu WAL/journal còn treo.

Không cần sửa hoặc ký lại APK cho hướng save. Không xóa dữ liệu ứng dụng. Nếu chưa lấy được save đang chơi, chưa thực hiện bước ghi/copy bên dưới.

## Chạy trên máy tính

Cài thư viện trong môi trường Python của bạn:

```
python -m pip install msgpack cryptography
```

Liệt kê đội của Ligue 1 trong registry bạn đang dùng:

```
python select_myleague.py --gateway "D:/efootxi/gateway-release" --list --competition 122
```

Tạo bản sao save có Arsenal được chọn:

```
python select_myleague.py --gateway "D:/efootxi/gateway-release" --input-save "D:/backup/local-club.sqlite3" --output-save "D:/backup/arsenal-new.sqlite3" --team 101 --competition 122
```

Đổi đường dẫn theo máy bạn. Nếu bản sao đầu vào đã có mùa My League, công cụ sẽ từ chối. Chỉ thêm `--restart-season` nếu bạn muốn bắt đầu mùa My League mới trong **bản sao đầu ra**; cầu thủ/vật phẩm vẫn được kiểm tra không đổi. Không hỗ trợ đổi giữa một trận My League đã bắt đầu và chưa kết thúc.

Công cụ kiểm tra hash của `my_league.py` để tránh chạy trên một phiên bản logic chưa được đối chiếu. Nếu báo không tương thích, giữ nguyên file và gửi lại phần work thực tế; không bỏ kiểm tra.

## Vị trí save và kiểm tra trên máy

Trong DEX của bản này, gateway dùng `Context.getFilesDir()/embedded-gateway/outputs/efootball/local-club.sqlite3`. Đây là dữ liệu nội bộ ứng dụng; không tự coi một đường dẫn `Android/data/...` cùng tên là bản đang được sử dụng. Ứng dụng có DocumentsProvider với tên gốc `73efootball 资源`, có thể cho trình quản lý tệp hỗ trợ SAF truy cập dữ liệu ứng dụng. Khả năng trình quản lý tệp của bạn truy cập được thư mục này cần xác minh trên điện thoại.

Sau khi đã có bản sao lưu và xác định đúng file đang dùng, đóng hẳn game rồi thay save bằng bản đầu ra mới theo quy trình nhập/khôi phục save đang hoạt động trên máy bạn. Không chép đè khi còn SQLite WAL/journal chưa được hợp nhất.

Mở game -> My League. Kỳ vọng máy chủ trả về đội Arsenal trong Ligue 1 và mùa đã chọn. Nếu client vẫn bắt mở menu chọn đội cũ hoặc từ chối mùa, ghi nhận đúng biểu hiện; đó là bước chưa được kiểm chứng, không khẳng định công cụ đã sửa UI.

Nếu cần quay lại, đóng game và khôi phục save gốc. Công cụ không thay CPK, APK, DEX, native library hoặc tài nguyên face.
