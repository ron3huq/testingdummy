# Face, chỉ số và ngoại hình: mã iOS thực sự làm gì?

Nguồn đối chiếu: ron3huq/testingdummy commit 1f84f36e67b4ad1f12e46310ef48a19123c7aff0; gateway Python efootxi 1.3.2 từ các file Android người dùng gửi. Không coi hai layout là giống nhau.

## 1. Preset ngoại hình do máy chủ gửi

Hàm [z27ApplyAppearanceAndClub](https://github.com/ron3huq/testingdummy/blob/1f84f36e67b4ad1f12e46310ef48a19123c7aff0/core/srv_part5.inc#L66) đọc `gameplayer_id.id`, lấy `base_id = id & 0xFFFFFF`, rồi tra `kAppearancePresets` trong [appearance_presets_gen.inc](https://github.com/ron3huq/testingdummy/blob/1f84f36e67b4ad1f12e46310ef48a19123c7aff0/core/appearance_presets_gen.inc).

Khi ngoại hình bị thiếu/hỏng, nó chép 12 giá trị đầu của preset vào `parameters[49..60]`. Chỉ số 49 được chú thích là màu da. Mã có giá trị mặc định và giữ ngoại hình tùy chỉnh sẵn có khi dữ liệu hợp lệ. Struct preset chứa 16 phần tử nhưng hàm này chỉ sao chép 12, không đủ cơ sở tự gán ý nghĩa sleeve/boots cho các phần tử còn lại.

Mã có nhánh riêng cho base ID 133543, 133580, 40352: giữ `49..60` bằng 0 để mô hình 3D có sẵn nạp đúng, theo chú thích Neymar/Haaland. Đây là điều kiện của các ID cụ thể, không phải công thức bảo đảm bật real face cho mọi cầu thủ.

Phần này sửa tham số ngoại hình hoặc cách dùng tài nguyên sẵn có, không tạo mesh khuôn mặt mới từ một ảnh.

## 2. Face/hair 3D thật

Đã đọc chỉ mục IoStore trong các container `ziru-extra/livedata/*_mobile_and.utoc` của chính kho tham khảo, tìm được 206 đường dẫn có face/hair/head/appearance. Ví dụ trong `pc9242_mobile_and.utoc`:

- `character/RealFace/SK_134589ep00v0310_Face.uasset`
- `character/RealFace/T_134589ep00v0310_Face_D.uasset` và `.ubulk`
- `character/RealFace/T_134589ep00v0310_Face_N.uasset` và `.ubulk`
- `character/RealFace/T_134589ep00v0310_Hair_D.uasset` và `.ubulk`
- các material instance `MI_..._Head_Face...` / `MI_..._Head_Hair...`

Đây là đầu mối mesh, texture và material; không phải ảnh thẻ cầu thủ. `.utoc` chứa chỉ mục, dữ liệu tương ứng nằm trong `.ucas`. Một face thường cần nhiều asset đồng bộ; thay mỗi tên file hoặc một ảnh PNG không chuyển cả khuôn mặt.

Quy trình mod thông thường là xác định đúng base/variant và tài nguyên đang nạp, trích xuất bằng công cụ tương thích Unreal, sửa mesh/tóc hoặc texture/material, rồi cook/đóng gói lại phù hợp engine và nền tảng. Kho này không cung cấp một editor tạo face hoàn chỉnh hay bằng chứng rằng mọi face Android có thể chép nguyên sang iOS. `tools/make_extra_pak.py` chủ yếu sao chép ảnh thẻ, logo và thumbnail áo; nó không phải công cụ dựng khuôn mặt 3D.

## 3. Chỉ số, kỹ năng và tiến trình

Ở kho iOS, chỉ số được xử lý qua `parameters` / `original_parameters`, dữ liệu cầu thủ đang sở hữu trong store và phản hồi giao thức. [z27ApplyProgressionPoints](https://github.com/ron3huq/testingdummy/blob/1f84f36e67b4ad1f12e46310ef48a19123c7aff0/core/srv_part5.inc#L160) cộng tiến trình từ dữ liệu nền.

Ví dụ các chỉ số mảng được dùng trong hàm này (đếm từ 0, không phải byte offset của Player.bin):

| Mục | Index trong mã iOS tham khảo |
|---|---:|
| Dứt điểm | 20 |
| Chuyền thấp / bổng | 21 / 22 |
| Đá phạt / Curl | 27 / 28 |
| Tốc độ / tăng tốc | 34 / 35 |
| Thể lực | 40 |

Ví dụ Curl nằm ở `parameters[28]` trong layout này. Chỉ sửa JSON nguồn không bảo đảm thẻ đang sở hữu đổi theo, vì save, `original_parameters`, tiến trình và lớp chuẩn hóa phản hồi có thể vẫn cung cấp giá trị khác. Cần kiểm tra cả phản hồi chi tiết lẫn payload vào trận sau khi đóng/mở lại game.

Android efootxi có `gameplayers` và `player_pool` trong SQLite, cùng `player_parameters.py`, `player_operations.py`, `player_migration.py` và dữ liệu policy/catalog. Mã phân biệt mảng 145/147/149 phần tử; booster và các skill mới có vị trí khác. [ios_compat.hpp](https://github.com/ron3huq/testingdummy/blob/1f84f36e67b4ad1f12e46310ef48a19123c7aff0/core/ios_compat.hpp#L41) chuyển layout Android/save sang iOS 147 phần tử. Không dùng index hoặc byte offset của một phiên bản để sửa mù phiên bản khác.

Kỹ năng cần đồng bộ cờ trong parameters, skill-ID list và kỹ năng học thêm theo layout. Panel Android đã có đường `set_skill` gọi đúng giao dịch `player_operations`, thay vì sửa trực tiếp một mảng không rõ ý nghĩa.

`initial_base_team_id` là thông tin CLB/áo, không phải face ID. `serial` phân biệt bản cầu thủ đang sở hữu, không phải ID mesh mặt.

## 4. Tay áo dài, tóc, thể hình

Chưa có trường sleeve/tay áo dài được xác minh trong hàm preset nói trên. Trong Android, `dt200` có `common/etc/appearance/PlayerAppearance.bin`, nhưng sự có mặt của file không chứng minh byte nào điều khiển tay áo. Không suy ra sleeve từ một slot Curl/skill hay sao chép toàn bộ ngoại hình từ cầu thủ khác vì có thể thay cả mặt và thể hình.

Muốn xác định một trường ngoại hình chính xác, cần so sánh hai bản dữ liệu của **cùng cầu thủ/cùng build**, chỉ khác đúng tùy chọn đó, hoặc xác định native getter/setter và bitfield tương ứng. Không thể bảo đảm long sleeves chỉ bằng các ID hai cầu thủ khác nhau.
