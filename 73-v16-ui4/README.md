# 73 V16 — UI4

[Tải gói cập nhật MT Manager, 71,6 MB](https://raw.githubusercontent.com/ron3huq/testingdummy/chat-downloads/73-v16-ui4/V25-73-UI4-Cuffs-Kits-Editor-Coaches-MT.zip) · [Tải file Blender, 25,4 MB](https://raw.githubusercontent.com/ron3huq/testingdummy/chat-downloads/73-v16-ui4/Ronaldo-Coaches-Blender-UI4.zip)

Áp lên APK **73 V16 đang có V25/UI1/UI2/UI3**. Giữ các sửa đổi trước: face, My League, đội hình Y08, kits, giao diện tiếng Anh, nút Enter lớn, tự vào sau 10 giây không chạm, cache đọc save/catalogue và Card Designer nhẹ. Gói không chứa save cá nhân.

## Cài bằng MT Manager

1. Xuất save dự phòng và giữ APK đang hoạt động.
2. Mở APK đang dùng; từ ZIP cập nhật, chép `classes5.dex` và **gộp toàn bộ thư mục `assets`** vào gốc APK. Thêm tệp mới, ghi đè tệp trùng, giữ những assets còn lại.
3. Ký bằng **đúng khóa MT đã dùng cho app đang cài**, rồi cài đè. Không gỡ game, không xóa dữ liệu, không gỡ resource app. Nếu xung đột chữ ký, chọn lại đúng khóa.
4. Đóng hẳn app và mở lại. Gói áo/font/ảnh HLV được nhập từ chính APK; không cần tải lại resource APK lớn qua mạng.
5. Vào Player Editor, chọn thẻ rồi chọn **Height / skills** để sửa chiều cao, cân nặng hoặc bỏ/chọn kỹ năng có sẵn. Lưu trước khi Enter Game. Phần Additional Skills năm ô vẫn dùng menu cũ.
6. File Blender dùng trên Windows với Blender 4.3 trở lên; không chép ZIP Blender vào APK.

Mùa Y08 mới vẫn có 10 đội/18 vòng. Lịch và kết quả mùa Swiss cũ đã lưu được giữ; muốn nhận lịch 10 đội thì bắt đầu mùa Y08 mới, không xóa save toàn game.

## Những thay đổi của UI4

- **Tay áo:** dựng từ mesh tay dài native liền mạch, giữ nguyên bảng bone, chỉ số bone và trọng số của mẫu tay dài. Không ghép chỉ số bone từ mẫu tay ngắn vào section khác như trước. Hạ ranh giới tay áo thêm 1,5 cm theo trục cẳng tay so với UI3, xử lý phần da/UV ở đoạn lộ ra. Chỉ bốn thẻ Ronaldo `88044950524330`, `89135066911146`, `89136418985303`, `89136418985302`, với Sparta351/Telstar352 slot0/1, được chọn mesh riêng. Giữ băng trắng cổ tay trái, tắt bên phải cho đúng bốn thẻ; không đổi phụ kiện cầu thủ khác.
- **Kits:** Y08 MU1706 → Telstar352/MU2008; Real4937 → AZ242/bwin. Y17 Real1220 → Sparta351/RM2017; Barca1222 → Heerenveen245/Barca2017. Các đội Y08 khác lấy áo CLB gốc. Bộ giải mã khóa áo hiện xử lý đủ phần loại áo ở bốn bit cao; lỗi cũ đọc thiếu phần này có thể chọn sai tài nguyên.
- **Tên/số áo:** AZ dùng màu đen. Bốn kits dùng bộ glyph native đồng bộ gồm Name, Name_Ex, Back, Chest, Leg và bố trí tên trên số từ mẫu áo được cấp phép của MU. Chỉ thay bố trí ở đúng tám cấu hình sân nhà/sân khách; giữ namespace và texture thân áo của từng bộ.
- **Y17/Y08:** 286 thẻ trong đội hình của hai giải có đủ 13 độ thông thạo vị trí, OVR mục tiêu 92–100 và thêm kỹ năng theo vai trò. Vị trí chính, đội hình, số áo và vai trò đá phạt giữ theo dữ liệu đã thiết lập. Phạm vi kiểm tra bằng mã giải518/473 và đúng ID thẻ; khôi phục dữ liệu khi ra ngoài. Bộ nạp face không còn ghi đè độ thông thạo của Ronaldo khi đang trong hai giải.
- **Editor:** chiều cao140–220 cm, cân nặng40–130 kg; bỏ/chọn kỹ năng có sẵn, gồm Chop Turn và Long-reach Tackle đúng cờ native. Không thêm Body & motion. Chỉ nạp giao diện này khi chọn thẻ; không quét cả catalogue hoặc thêm SQL cho từng cầu thủ. Ghi save trong transaction; cấu hình lỗi thì hoàn tác.
- **HLV:** Martínez`17606144688129` → Zinedine Zidane/Pháp/45 tuổi; Gattuso`17604802510874` → Sir Alex Ferguson/Scotland/66 tuổi. Tuổi theo giai đoạn2017/2008. Đổi ba trường tên, quốc tịch và tuổi trong bản ghi tài nguyên được đối chiếu byte trước khi sửa; giữ ID, chiến thuật và booster của thẻ. Ảnh thẻ dựng từ các gói PC bạn gửi, đã giải quyết namespace vật liệu và lớp mask tóc/da. Đây là ảnh thẻ HLV; **chưa có bản port mô hình HLV3D ở đường biên**.
- **Blender:** hai file Ronaldo là mẫu native thực tế được hai thẻ trỏ tới, có UV/rig/trọng số và texture đóng gói. Hai thẻ có cùng payload ngoại hình nên khuôn mặt giống nhau. Kèm hai bản dựng nguồn HLV để xem; mắt preview được bổ sung do gói PC phụ thuộc tài nguyên mắt chung của game.

## Kiểm tra và giới hạn

- DEX037 giữ toàn bộ267 lớp gốc; kiểm tra chữ ký/checksum, phương thức, thanh ghi, móc idle/English; không có lớp Body & motion.
- Thực thi ARM64 với accessor gốc: 28 đội hình, 22 đội cổ điển, 286 profile; vị trí/số áo/vai trò, OVR, kits, băng cổ tay, phạm vi thẻ và khôi phục ngoài giải.
- Chạy inflateInit2/inflate/inflateEnd **của chính engine73** qua hook đã biên dịch: tám cấu hình áo và hai bản ghi HLV sửa đúng vùng; dữ liệu khác giữ nguyên.
- Đọc mesh bằng UModel; đối chiếu bone/weight/index/bind với mẫu tay dài gốc; thử skinning CPU ở khuỷu tay0/30/60/90/120°. Kiểm tra này không chứng minh mọi bề mặt luôn không xuyên nhau trong mọi animation.
- Thử sửa chiều cao/cân nặng/skill trên bản sao save, đọc lại, từ chối giá trị sai, kiểm tra rollback và giữ progression/booster/Additional Skills.10.000 lần chiếu dữ liệu thẻ không truy vấn SQL mất khoảng0,10 giây trên máy kiểm tra; đây không phải số đo điện thoại.
- Card Designer chạy kiểm tra Chromium với/không bridge giả lập: tải/lưu/chuyển tab qua, không repaint liên tục khi đứng yên. Bốn file `.blend` mở lại bằng Blender4.3.2 với ảnh đã đóng gói.
- Đối chiếu7373 mục manifest với APK nền + overlay; không đóng gói save/DB cá nhân; container face`pc9298` và ánh xạ17 thẻ giữ nguyên.

**Chưa chạy trên Android/GPU điện thoại thực tế.** Đây là bản đã qua các kiểm tra thành phần và cần bạn kiểm tra trong trận; không thể cam kết hết100% lỗi hiển thị hoặc hiệu năng trên máy bạn. Các báo cáo cụ thể nằm trong `validation/`.
