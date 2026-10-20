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

## 5. Hai nhánh iOS người dùng vừa gửi, chụp tại thời điểm kiểm tra

- `community-mod-engine`: commit [`be7b0aae386bc92b568d1195ba4fbf1e400f96c3`](https://github.com/iOSVNNews/pes2027-mod/tree/be7b0aae386bc92b568d1195ba4fbf1e400f96c3).
- `codex/repair-data-loss-20261020`: commit [`f8dc2a85f75557d5903f3b877b66f5042852729c`](https://github.com/iOSVNNews/pes2027-mod/tree/f8dc2a85f75557d5903f3b877b66f5042852729c).

Nhánh là địa chỉ thay đổi theo thời gian; các nhận xét dưới đây bám vào hai commit này. Không suy ra thời điểm phát hành hay việc đã chạy thành công từ lời mô tả commit.

### Cách đổi face cụ thể

[ZiruPlayerIdentity.hpp](https://github.com/iOSVNNews/pes2027-mod/blob/f8dc2a85f75557d5903f3b877b66f5042852729c/ios/ZiruPlayerIdentity.hpp#L6) lấy `base = pid & 0xFFFFFF`. Chỉ ID `9901397` được gán face Zidane `9901397`; ID `37576` được gán face R9 `37576`. Nhánh sửa lỗi bỏ cách suy ra mặt từ tên trên áo: Cristiano `4522` và R9 `37576` cùng có thể mang tên **RONALDO**, nên tra tên sẽ gán nhầm mặt.

[applyLegendRealFace trong ZiruJersey.inc](https://github.com/iOSVNNews/pes2027-mod/blob/f8dc2a85f75557d5903f3b877b66f5042852729c/ios/ZiruJersey.inc#L208) gán chuỗi face vào trường `actor + 0x468`, thông qua phép gán FString gốc tại `0x102e14b64 + gSlide`. Điểm sửa đáng chú ý là để engine quản lý bản sao chuỗi; trỏ thẳng vào bộ đệm tĩnh có thể gây giải phóng bộ nhớ sai khi `ReloadFace` chạy. Hook `SetupFromPlayerId` ghi nhớ đúng player ID; đối số thứ tư là số áo, không phải cờ sân nhà/sân khách.

**Các offset/địa chỉ trên chỉ thuộc build iOS đó. Không chép vào libUE4 Android.** Đây là chuyển sang tài nguyên face tồn tại, không phải sinh một khuôn mặt 3D mới từ ảnh. Chưa đủ bằng chứng rằng chỉ thêm hai ID là mọi asset của Zidane/R9 sẽ tải và hiển thị được.

### Vì sao hai nhánh xử lý tài nguyên khác nhau?

Commit đầu nhánh community khôi phục dt870 stock và loại pc3611 Android. Nhánh repair lại giữ tài nguyên pc3611, ghép dữ liệu nền với Legends, bảo toàn kit/stadium, và xử lý biến thể layout package-store 16/32 byte thay vì ghi lại nội dung bằng một layout duy nhất. Chỉ mục pc3611 có hàng chục nghìn đường dẫn character/texture; xóa gói mù có thể làm mất tài nguyên liên quan. Đổi tên/alias package cũng không tự chứng minh package ID và liên kết phụ thuộc tương thích.

Tài liệu [repair-20261020.md](https://github.com/iOSVNNews/pes2027-mod/blob/f8dc2a85f75557d5903f3b877b66f5042852729c/docs/repair-20261020.md) tự đánh dấu bản sửa **chưa xác minh trên iPhone**. Vì vậy chưa thể kết luận nhánh mới hơn đã sửa face thành công trên máy thật.

### Stats và ngoại hình

Các thay đổi mới còn sửa khâu truyền/lưu skill và booster. [ios_compat.hpp](https://github.com/iOSVNNews/pes2027-mod/blob/f8dc2a85f75557d5903f3b877b66f5042852729c/core/ios_compat.hpp#L29) chuẩn hóa mảng gửi ra thành 147 phần tử: skill bits 142/143 và booster 144–146; đầu vào save Android có thể dùng layout khác. Đây là lý do chỉnh một slot trực tiếp có thể làm hỏng skill/booster hay bị ghi đè khi phản hồi được chuẩn hóa.

Muốn sửa chỉ số thật: nhận diện đúng bản thẻ đang sở hữu, sửa dữ liệu nền/tiến trình theo layout của build, đồng bộ dữ liệu được trả về rồi kiểm tra lại sau khi mở save và vào trận. Ngoại hình preset vẫn đi qua vùng `parameters[49..60]`; face 3D còn phụ thuộc hook nhận diện và tài nguyên mesh/texture. Hai phần này có liên quan nhưng không thay thế nhau.

Trong hai nhánh vừa đọc, tôi không tìm được bản sửa menu Select Team dành cho Android có thể lấy chép sang. Phần face iOS cho thấy hướng can thiệp native là khả thi về thiết kế, nhưng phải xác định lại hàm và cấu trúc Android. Bản thử Select Team lần này được xây từ libUE4 Android 1.3.2, không dùng offset iOS.
