# Kết quả nghiên cứu Android: tay áo và ghép tóc

Ngày21/10/2026. Nguồn là libUE4.so của efootxi1.3.2 Android ARM64, không dùng offset iOS.

## Áo tay dài: đã có bản thử cho đúng thẻ Ronaldo

Mục tiêu `89138556572074`. Nguồn tham chiếu tay dài `88041729329832` (Bale).

`PlayerAppearance.bin` có bản ghi64 byte: ID64bit ở đầu,52 byte dữ liệu ngoại hình bắt đầu từ+8. Trong bản dt870 hiện có, Ronaldo có chế độ tay áo0, Bale có chế độ2. Hai bit62–63 của u64 đầu trong52 byte dữ liệu là thiết lập mà native chuyển thành `sleeveType2`:

| Chế độ lưu | Mùa hè | Mùa đông |
|---|---|---|
|0: tự động|ngắn|dài|
|1: buộc ngắn|ngắn|ngắn|
|2: buộc dài|dài|dài|

Bản thử đặt2 cho Ronaldo89138556572074. Không sửa file bảng gốc: hook hàm serialize`0x68d0868` kiểm tra full64 ID rồi chỉ đổi2 bit trên **bản sao52 byte** mà game đang dùng dựng nhân vật. Cách này bao phủ dữ liệu tra từ DB và bản ghi cache của đường dựng nhân vật đã lần được.

Đường native đã đối chiếu:

- Đọc bảng: `0x6abcb9c`, stride64; copy52 byte từ raw+8 vào record runtime+0x18, stride80.
- Serialize: `0x68d0868(this80,out52)`, copyrecord+0x18 ra52 byte.
- Hàm dựng đầu/thân `0x68ceb44` gọi serialize tại`0x68cf258`, sau nhánh cache hoặc DB; không gọi thêm accessor engine từ Python.
- Chuyển ngoại hình `0x68d1fbc`: đọc hai bit nói trên,0 dùng mùa hiện tại,1/2 đổi thành0/1; ghi trường cấu hình+0x50.
- Cấu hình nhân vật trong actor ở+0x10a0; trường tay áo tại+0x10f0. Đường gọi áo tại`0x3a0b538` đọc trường này,`0x3a0b5e0` chuyển sangW3,`0x3a0b5f8` gọi virtual`LoadUniShirt`.
- Reflection`0x916aab8` gọi tham số thứ ba là`sleeveType2`; wrapper`0x3d11a3c` nạp đúngW3 trước virtualslot0x6a8.

Kiểm tra thực thi ARM64 gốc bằng Unicorn:107 trường hợp serialize,6 trường hợp chế độ/mùa; toàn bộ converter gốc và đoạn chuẩn bị tham số gọi áo chạy thực. Hàm copy libc, cấp phát và std::string được mô hình hóa. Khi đổi Ronaldo mùa hè, vùng cấu hình nhân vật trước vector phụ kiện chỉ khác byte+0x50; mùa đông không khác vì trước đó đã dài. ID trùng phần thấp nhưng khác64bit không được áp dụng; dữ liệu nguồn và vùng nhớ liền kề giữ nguyên.

**Chưa xác nhận hình ảnh trên Android.** Đây là bản thử đã kiểm tra logic native, cần vào trận để xác nhận mesh áo của bộ kit đang dùng có hiển thị tay dài đúng không.

## Tóc Pato → Ronaldo: chưa áp dụng, đã xác định điểm vướng

Nguồn `88038776539586` là Alexandre Pato, base35266. Đích `88044950524330` là Cristiano Ronaldo, base4522. Đây là yêu cầu mới, khác ID đích17592186048938 ở lần trước.

Đã xác nhận:

- Có bản ghi ngoại hình riêng của cả nguồn và đích trongdt870; không có trường trong147 tham số kỹ năng/chỉ số nào đã được chứng minh cho phép sao chép nguyên tóc real-face giữa hai thẻ.
- Android có hệ tóc chỉnh sửa`HairNo`, tóc real-face,`HairAssetData`,`m_indecies_hair`, vật liệu/texture tóc. Điều đó cho thấy có phần xử lý tóc riêng, nhưng không chứng minh chỉ đổi một số là ghép đúng tócPato.
- `LoadRealFace`native`0x39cdb10` tạo đường **SK_<mẫu>_Face**, không có bước chọn mộtHairCardID độc lập trong đường này. Mesh này đi qua callback`0x39d3e1c` và dữ liệu phần mặt/tóc. Chuyển hướng nguyên mẫu đầu sẽ đổi cả mặt.
- Đã đọc được cookedDataTable`DT_RealFaceMapping`: trongpc9261/9262,`35266ep00v0318` chuyển về`35266ep00v0290`. Một số thẻ Ronaldo có chuyển hướng`4522ep01v0278`→`4522lg00v0000`; **không kết luận đây là mẫu cuối cùng của thẻ đích0313**, vì chưa quan sát resolver trên điện thoại.
- Đã rà các chỉ mục IoStore đọc được trong tệp hiện có và48 CPK: không tìm thấy mesh/texture3D của Pato35266 và Ronaldo4522 theo đường tên có thể xác minh. Ảnh thumbnail/card và bảng mapping có tồn tại nhưng không thay thế được mesh3D. Một số tên hash CPK vô tình chứa4522 không được coi là tài nguyên Ronaldo.

Hướng cần làm tiếp: lấy đúng mesh đầu nguồn và đích; tách phần vertex/index/material tóc của Pato, đối chiếu skeleton/bone weights, vị trí chân tóc, LOD và texture; dựng mesh kết hợp giữ phần mặt Ronaldo. Nếu runtime cho phép nạp phần tóc từ một asset đầu khác một cách độc lập thì có thể dùng đường đó, nhưng hiện chưa có callback đã kiểm chứng để phát hành an toàn.

**Không có sửa tóc trong ZIP.** Không đổi toàn bộ mặt thành Pato, không chọn tóc generic gần giống rồi gọi là tóc Pato.

Dữ liệu cần bổ sung để tiến tiếp: các gói Android`.utoc`/`.ucas` cùng tên chứa **SK_35266…_Face**, **SK_4522…_Face** và các texture/material`…Hair…`, hoặc các asset này đã xuất nguyên gốc bằng FModel. Giữ cả`.pak` cùng tên nếu có. Chúng có thể ở các gói tài nguyên tải thêm/assetpacks, không nằm trong APK cơ sở và gateway đã gửi. Chưa biết chính xác sốpc của các gói thiếu nên không đoán tên để bạn thay nhầm.
