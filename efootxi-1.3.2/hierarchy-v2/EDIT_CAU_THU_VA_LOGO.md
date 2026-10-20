> **DỪNG DÙNG BẢN V2 NÀY:** người dùng xác nhận văng ngay sau Bắt đầu khi gặp Bayern127. Các kiểm tra payload dưới đây không chứng minh consumer Android chơi được trận. Xem [bản thử sửa v3](../hotfix-v3/HUONG_DAN.md), chưa xác nhận trên điện thoại.

# Skill, chỉ số, tay áo và logo trên Android 1.3.2

## 1. Sửa skill/chỉ số cầu thủ

Có hai nguồn dữ liệu cần xử lý đúng:

- Thẻ đang sở hữu: có `id` **và serial**. Gateway có `efootxi_panel.handle(conn, 'set_skill', req)` gọi giao dịch `player_operations.skill`, đồng bộ `additional_skill_id`, cờ skill, receipt và phản hồi. Trường `slot` của panel từ 1 đến 5; skill ID khác index của `parameters`. Ví dụ `DOUBLE_TOUCH` là skill ID 1, `BLITZ_CURLER` là 18. Phải chọn skill được build hỗ trợ qua `player_skills.SELECTABLE_SKILL_IDS`.
- Cầu thủ CPU: My League mặc định gửi `player_list = null`, `squad_data = null`, để engine dùng base roster native. Chỉnh một hàng thẻ trong SQLite không bảo đảm thay đổi cầu thủ native đó. Có thể dùng hook dữ liệu native hoặc phục vụ một đội hình inline hoàn chỉnh. V2 đã có đường inline cho Bayern127 và Brazil45.

Với mảng 147 phần tử của gateway này, các index đã đối chiếu gồm: tấn công 14, dứt điểm 20, chuyền thấp/bổng 21/22, Curl 28, tốc độ 34, tăng tốc 35, thể lực 40. Không dùng `_overall` làm chỉ số gameplay: đó là metadata tổng quát. Không sao chép offset iOS vào Android hoặc áp dụng nguyên layout 145/147/149 cho nhau.

## 2. V2 có thể chỉnh base của CLB tôi không chọn không?

**Có, với đội dùng đường inline.** Không cần bạn sở hữu thẻ đó hoặc điều khiển CLB đó. Cấu hình `player_overrides` được áp dụng lên bản sao cầu thủ CPU khi dựng đội hình, không ghi thẻ sở hữu hay thư viện vào DB.

Ví dụ: sửa Kane của **Bayern127**, ngay cả khi bạn chọn Arsenal. Trong `myleague_custom.json`, thay đối tượng `player_overrides` rỗng bằng:

```json
"player_overrides": {
  "47287": {
    "stats": {"finishing": 99, "speed": 90},
    "skills_add": [18]
  }
}
```

`47287` là base ID Kane đã kiểm tra trong dữ liệu gửi. Ví dụ này tăng dứt điểm/tốc độ và bật cờ innate Blitz Curler của **bản sao CPU inline**, không cấp thẻ hoặc huấn luyện thẻ trong đội bạn. Mặc định gói **không bật ví dụ này**.

Các tên stat được hỗ trợ: `offensive_awareness`, `finishing`, `low_pass`, `lofted_pass`, `curl`, `speed`, `acceleration`, `stamina`; giá trị nguyên 40–99. `skills_add` chỉ nhận skill ID có trong danh sách hỗ trợ, rồi ánh xạ bằng `PARAMETER_BY_SKILL`, không lấy ID làm index.

Chỉ cần buộc dừng và mở lại game, rồi chuẩn bị trận mới để nhận payload mới. Trận đã khởi động giữ đội hình đóng băng. Hệ số `scorer_boosts` là trọng số mô phỏng bàn thắng; nó không tự sửa chỉ số thẻ trong trận.

**CLB khác hiện vẫn dùng native roster**, trừ những đội có mục trong `custom_rosters`. Muốn chỉnh cầu thủ của Arsenal/Real/City... theo cách inline này, phải thêm **roster của đúng ID CLB đó** vào `custom_rosters`, đủ 11–40 cầu thủ, và mọi base card phải có payload trong thư viện. Bộ dựng từ chối thẻ thiếu; không mượn danh tính của Monaco hoặc tự thay cầu thủ lạ. Không chỉ thêm một cầu thủ đơn lẻ vào danh sách đội. Đường chung đã có trong mã; v2 mới kiểm tra payload/trận phía máy chủ cho Bayern và Brazil, chưa kiểm chứng thiết bị cho mọi CLB.

Ví dụ cấu hình ở trên đã được thử trên DB sao chép: wire payload Kane có `parameters[20] = 99` và cờ skill đúng; hàng thư viện gốc không đổi. Điều này xác minh nội dung phản hồi, chưa chứng minh mọi hiệu ứng skill được render/thực thi trên điện thoại.

## 3. Áo ngắn thành áo dài

Chưa xác minh đúng field/bit tay áo trên **libUE4 Android build này**. Có `PlayerAppearance.bin` và vùng tham số ngoại hình, nhưng chưa có phép so sánh một biến hoặc getter native chứng minh trường nào là sleeve. Các slot `parameters[49..60]` từng được dùng cho preset ngoại hình không đủ để kết luận tay áo nằm ở đâu.

Cách làm cần thiết: lấy hai trạng thái của cùng một cầu thủ/cùng build, chỉ khác tay áo; so sánh payload/dữ liệu appearance, hoặc theo native getter/setter đến trường lưu trữ. Sau đó mới thêm override có kiểm tra. Gói v2 chưa có công tắc áo dài; không ghi một offset phỏng đoán vì có thể sửa cả mặt hoặc thể hình.

## 4. Logo đội và giải

Có thể sửa tài nguyên logo, nhưng cần xác định đúng texture/asset và nơi nó đang được nạp. Có thể phải thay nhiều biến thể icon/menu/trong trận. Trong các gói Unreal, `.utoc` là chỉ mục, nội dung tương ứng ở `.ucas`; cần giữ package ID/dependency và cook đúng engine/nền tảng Android. Đổi một file ảnh ngoài không tự cập nhật texture đã cook.

Kho iOS tham khảo có công cụ `tools/make_extra_pak.py` nhắm các đường `/ui/data/symbol/emblem/` và `/ui/data/symbol/emblemlc/`. Đây là dấu vết để tra tài nguyên; không chứng minh gói iOS có thể chép nguyên sang Android. Chỉ mục Android đã đọc có các asset placeholder/render-target emblem, nhưng chưa trích xuất và xác minh đúng texture logo cần thay cho từng đội/giải.

V2 sử dụng ID đội tuyển/CLB thật để game lấy tài nguyên sẵn có. **Tên/logo vỏ Belgian League và Liga Portugal vẫn là tài nguyên gốc; chưa thay logo giải.** Bayern127 vẫn dùng tài nguyên áo/logo của ID München RW đang có trong game; gói chưa thêm bộ logo/áo Bayern chính thức. Thay đổi roster hay xếp hạng sức mạnh không tự tạo logo mới.
