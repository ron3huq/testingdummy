# V19.1 FULL-3 · Earth

Gói **tích lũy đầy đủ**, dùng cho APK 73efootball V19.1 gốc, SHA-256 `9c0b249557eeab1543ce143af4d08269b6e9a5a965472242815dba5712c76469`. Không áp vào V16/V20.2. Không cần áp FULL-1 hoặc BOOT-FIX trước.

## Cài bằng MT Manager

1. Export Save để có bản sao lưu. Giữ nguyên dữ liệu và tài nguyên game hiện có.
2. Mở APK V19.1. Mở thư mục bọc ngoài của ZIP GitHub, chép **assets/** và **classes5.dex** vào gốc APK, thay file trùng.
3. Ký bằng cùng khóa đang dùng và cài cập nhật. Không gỡ ứng dụng, không xóa dữ liệu, không áp chồng các Part/UI V16 cũ.
4. README, validation và inventory không chép vào APK. Lưu chỉnh sửa trước Enter Game; đóng/mở lại ứng dụng khi trình chỉnh ảnh yêu cầu.

Đây là gói thay file APK, không phải APK 2,5 GB đã ký sẵn. Không chứa save cá nhân.

## Sửa mới FULL-3

- Sửa hồi quy bộ đóng CPK: rebase V19 trước đã dùng bộ đóng UI6, đổi storage flags/NULL và mã hóa UTF. FULL-3 dùng cách đóng UI7.4 của V16, giữ schema native, NULL, mã hóa và thứ tự101 hàng gốc, kiểm tra toàn bộ142 payload/ID. CPK mới SHA-256 `6fa4b9050f0a125e9ee295a7260ca3f1b5f718cdca6d5af94e2cc697d215fc4a`. Đồng bộ cả ba đường cung cấp và manifest.
- Thay cache chỉ khi khớp chính xác CPK stock hoặc bản rebase lỗi đã biết, lưu bản phục hồi có kiểm tra hash. Không xóa save, cache lạ hoặc version.bin. Bản sửa cache nhỏ trước đó còn dùng CPK sai cấu trúc; không cần áp lại.
- Đồng nhất lối vào Player Editor, tạo tab khi mở, thêm Back/Refresh; giữ công cụ native bên dưới. Home tự Enter sau10 giây không thao tác, chỉ khi Home hiện và Activity có focus; không tự Enter trong trang chỉnh sửa/hộp native.
- Catalogue: mở Cart → Choose players, bấm Select multiple nếu cần. Bấm lần lượt các thẻ; ô chọn chuyển xanh và có số thứ tự. Tìm kiếm giữ lựa chọn. Cart liệt kê đúng thứ tự bấm, cho bỏ chọn/clear và thêm tuần tự vào kho; tối đa50 thẻ/lượt.
- Wukong native được đọc lại bằng bộ đọc độc lập trên cả bốn biến thể, giữ166 xương/weights. Blender và tám góc render gửi ZIP riêng.

Kiểm tra mới mang tiền tố `full3-`: CPK native format, gateway/relogin, cache repair,512 lớp DEX, layout sáu kích thước, giỏ hàng/thứ tự thêm và idle-focus guard, cùng mesh Wukong. Đây là kiểm tra trên máy build; chưa xác nhận lần Enter Game với CPK mới trên điện thoại.

64 ID yêu cầu vẫn được giữ trong Favorites. Đối chiếu catalogue thực có57 bản ghi; bảy ID `16957006,16906937,16940451,16912943,16912948,16900351,16918387` có bản ghi native nhưng chưa có mẫu thẻ catalogue để thêm vào kho. Không tạo thẻ hoặc chỉ số giả cho bảy ID này.

## Các sửa đổi tích lũy

- Giữ bản sửa lỗi DEX gây văng ngay khi mở ứng dụng. Sửa nguồn HTTP `dt870_mobile_and.cpk`: manifest, đường tải và nguồn phục hồi cùng dùng CPK đã ghép kits 7.680.000 byte. Giữ nguyên kiểm tra hash/kích thước, không tắt Live Update integrity.
- Giao diện Earth xanh biển, tĩnh, bố cục theo chiều rộng màn hình; bỏ Recently Viewed, khóa zoom trang launcher. Giữ thao tác căn ảnh trong studio. Rút gọn nhãn tab, bố trí lại bảng chỉ số, dành chỗ cho thanh điều hướng và system bars. Dịch nhãn launcher và hộp công cụ sang tiếng Anh; tên/dữ liệu do người dùng nhập không bị tự sửa.
- Giữ 64 ID Favorites mặc định đã yêu cầu, không ghi đè lựa chọn bỏ thích về sau. Portrait queue giới hạn bốn tác vụ, gộp yêu cầu trùng, bỏ tác vụ của hàng đã rời trang; thumbnail launcher thu nhỏ riêng, không giảm chất lượng ảnh xuất vào game.
- Booster picker chỉ hiện +4 trở lên, tăng dần, không có Total Package. Giá trị cũ đang lưu không bị tự thay khi chỉ mở giao diện.
- Transfer Add Player ưu tiên Standard/Base. Tìm kiếm có cache giới hạn và không ghi SQL đội hình. Transfer vẫn chỉ dành UEFA Champion League122, World Nation League128, Y08473, Y17518. Giữ captain và các vai trò theo ID cầu thủ khi swap; giữ đường dữ liệu native và tránh con trỏ GamePlan clone không an toàn. Chưa có snapshot thì yêu cầu đọc đội trong game, không tự đoán XI.
- Studio dùng renderer/layer của DIY Card gốc. Sửa mã phiên bản CSS/JS lệch, nạp lại dependency editor-fields và tương thích phương thức date tùy chọn. Mục **Apply portraits to an owned card** chọn đúng thẻ đang sở hữu, xuất riêng hai bố cục subject trong suốt, giữ background/frame/badges/stats native. Thay background không lấy ảnh cầu thủ của thẻ donor. Đường tạo thẻ DIY mới vẫn là Generate gốc, tách khỏi sửa ảnh thẻ đang sở hữu.
- Preview cũ bị chặn lưu khi đổi project. Lưu ảnh đi qua pipeline xác thực sở hữu và tài nguyên hiện có, rồi báo Player Editor tải ảnh mới. Không ghép nền/frame của preview vào portrait.

## Sao chép nguyên ba thẻ

| Nguồn | Đích | Face native mod | Portrait |
|---|---|---:|---:|
|89136418985332|89138288266704|56334|9500031|
|89136418985303|88044145348047|56323|56323|
|89136418985320|106782013894690|56331|9500027|

Sao chép toàn bộ payload147 parameters và metadata, suite/design/ảnh/face tham chiếu nguồn; giữ ID đích, serial owned và lịch sử cá nhân. Nguồn320 trong dữ liệu thực là P. E. Aubameyang; gói theo đúng ID đã yêu cầu, không tự đổi nguồn. Không dùng đầu4522 thay các face mod này.

Migration một lần chỉ xóa cấu hình ngoại hình/phân bổ cũ của đúng ba đích có thể ghi đè bản sao mới, lưu recovery tại `outputs/efootball/full2-card-copy-recovery.json` trong runtime. Không sửa squad/captain khi copy thẻ. Sau migration, các chỉnh sửa mới của người dùng không bị reset mỗi lần mở.

## Nội dung tích lũy và Wukong

Giữ tài nguyên và công cụ FULL-1 đã ghép từ V16/UI7.19 trên runtime V19.1: face/kits, skill/editor/progression, model/motion đã kiểm chứng, phụ kiện/màu native, crop, save manager, catalogue và Transfer. Giữ các loại trừ đã yêu cầu: Part3, physics và custom skin colours; chỉ dùng palette da native. Không thay runtime protected V19 bằng V16.

Wukong dùng atlas râu trên cả bốn biến thể; làm dày chân các mảng lông bên trong tối đa3,5mm, khóa đỉnh đường bao và ngọn lông để giữ khung và chiều dài. Giữ nguyên bộ râu, topology, skinweights và skeleton/bind166 xương. Blender và tám ảnh góc xem trước được gửi trong ZIP Wukong riêng, không nằm trong gói full. Đây là render Blender, không phải ảnh chụp Android; shader game cần xác nhận trên máy.

## Saudi trong dữ liệu

Có sáu CLB và đầy đủ bản ghi cầu thủ đã gán: Al Ahli Saudi FC36, Al Ittihad30, Al Hilal34, Al Nassr32, Al Taawoun34, Al Qadsiah31. Không tìm thấy registry giải Saudi1/2 đầy đủ hoặc CLB Saudi2 trong bộ dữ liệu đã kiểm tra. Xem `validation/full2-saudi-data-report.json`. Danh sách cầu thủ không đồng nghĩa đã xác minh XI/roles đang dùng trong một save My League.

## Kiểm chứng và giới hạn

Báo cáo mới có tiền tố `full2-` trong validation: gateway/Live Update đăng nhập lại sau thay ảnh, copy ba thẻ, Chromium6 kích thước ×5 tab, DIY startup và hai ảnh/crop/alpha, tìm kiếm500 truy vấn, liên kết508 lớp DEX, ARM64 Transfer consumer. Các báo cáo không có tiền tố là kiểm tra nền FULL-1 được giữ để đối chiếu, không phải kiểm tra lại trên điện thoại.

**Chưa chạy gói này trực tiếp trên Android/GPU.** Không thể cam kết 100% không crash/lag hoặc tất cả phụ kiện hiện đúng chỉ bằng host test. Cần xác nhận Enter Game, đội hình đối thủ, captain sau swap, ảnh thẻ và replay trên thiết bị. Host fixture thiếu container pc3700 gốc V19, nên không xác nhận ảnh nguồn303/320 từ host; chúng tham chiếu tài nguyên có trong game gốc. Wrist tape vẫn cần kiểm tra hiển thị thực tế. SOUND theo từng thẻ chưa triển khai; copy motion chỉ gồm trường đã kiểm chứng, không cam kết mọi signature animation khóa theo danh tính. Cap lưu chỉ số127 không bảo đảm gameplay vượt cap native.
