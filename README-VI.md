# 73 V16 · UI7.18 FULL · Một ZIP, không Part3

Dành riêng APK 73 V16 versionCode 311010108. Không dùng cho efootxi.

Mở thư mục bọc `testingdummy-<commit>/` nếu tải qua GitHub. Chép **assets/** và **classes5.dex** vào gốc APK, thay thế rồi ký một lần. Dùng cùng khóa ký để cài cập nhật và giữ save. Không áp chồng thêm Part/UI cũ. Không cần gỡ game hay xóa dữ liệu. **extras/** chứa file Blender cho máy tính, không chép vào APK.

## Sửa trong UI7.18

- **Ảnh cầu thủ:** sửa đường thay ảnh khi engine dùng tên tài nguyên ngắn hoặc đường dẫn tương đối; giữ đúng dạng tên mà engine đang dùng. Ảnh mặt trước thẻ dùng bản lớn, miniface dùng bản nhỏ. Tạo đủ alias ở hai thư mục native Player và Player/Variation2022. Copy Background tiếp tục chỉ thay nền/khung, giữ ảnh và danh tính thẻ đích. Ảnh nhập sau có ưu tiên hơn ảnh đi kèm.
- **Đồng bộ Player Editor:** danh sách, chi tiết và ảnh nhỏ dùng cùng crop đã lưu; cache ảnh có revision riêng cho từng thẻ và được làm mới sau import. Chuyển PNG chỉ khi hàng ảnh hiện ra cần tải, không xử lý ảnh toàn bộ catalogue khi tìm kiếm.
- **Live Update:** giữ bố cục PAK chuẩn version11, 365 byte, hai secondary index và SHA1 được kiểm tra. Hash PAK phụ thuộc cả UTOC/UCAS thực tế, để thay alias hoặc ảnh đều tạo cập nhật mới. Ảnh custom dùng schema18, dựng lại từ crop SQLite đã lưu, giữ đường generation cũ bất biến. Giữ GET/HEAD/range và SHA; không tắt integrity. Chỉ sửa bốn PAK cache UI7.16 đã biết khi companions giữ nguyên; pc9323 đã đổi companions nên để game tải đủ bộ, không đánh dấu cập nhật bằng cách chỉ sửa PAK.
- **Transfer:** giữ phạm vi bốn giải UEFA122, World Nation128, Y08473, Y17518. Sửa GamePlan runtime riêng mà màn hình đội hình dùng, thay vì chỉ sửa bản Team. Giữ pool ID ổn định; đội trưởng, sáu vai trò đá phạt và số áo theo cầu thủ. Mỗi bản Team cache có GamePlan riêng, tách theo luồng khi engine đang dùng nhiều bản pool. Không ghi đè GamePlan dùng chung.
- **Animation:** trong Copy native motion thêm **Edit individual animations**: Dribble Type, Dribbling Posture, Dribbling Arm, Running Posture, Running Arm, Free Kick Type, Penalty Kick Type, Corner Kick Pattern. Hiện giá trị hiện tại và biến thể tìm thấy trong dữ liệu native. Hai trường Arm chỉ có giá trị0 trong dữ liệu đã đối chiếu, nên không bịa thêm tên/hiệu ứng. Chỉnh riêng có ưu tiên hơn donor; copy donor mới bỏ override của tám trường này. Không thay face, skills hay animation ăn mừng khi copy motion.
- **Runtime Diagnostics:** lấy counters mới ngay lúc bấm, trên luồng nền. Dòng `ui718-live-runtime-status.json` phân biệt cấu hình đã lưu với loader phụ kiện/GamePlan/đường ảnh thực sự được gọi. Không chạy scan/hash chẩn đoán trong search hay trận đấu.

## Accessories: đủ10 loại trong registry native0–9

| Type | Phụ kiện |
|---|---|
| 0 | Quần bó ngắn — Short tights |
| 1 | Quần bó dài — full set |
| 2 | Quần bó dài — native variant2 |
| 3 | Quần bó dài — native variant3 |
| 4 | Băng cổ tay trái |
| 5 | Băng cổ tay phải |
| 6 | Băng cổ chân |
| 7 | Găng cầu thủ |
| 8 | Áo lót cổ thường |
| 9 | Áo lót cổ cao |

Mỗi loại có Original / Off / On và màu có sẵn hoặc #RRGGBB, kèm ô minh họa màu. Ba biến thể quần bó dài dùng asset native chung; không đặt tên trái/phải khi chưa có bằng chứng. Short và long tights không bật cùng lúc. High-neck bật cùng lớp áo lót cơ sở. Băng đội trưởng theo vai trò đội trưởng; tất có tab riêng. Găng thủ môn được loại trừ theo yêu cầu trước. Không thêm nút giả cho hình xăm/kính/trang sức gắn cứng trong mesh.

Sửa tại **đầu vào bộ nạp phụ kiện thật39b84bc**, bổ sung mục On bị thiếu hoặc bỏ mục Off trước khi game nạp asset native. Giữ row không chỉnh và cấu hình các thẻ khác. Sửa màu ARGB giao diện sang RRGGBBAA của loader, tránh alpha khiến màu/phụ kiện trong suốt. Áo xắn và băng cổ tay dùng hai phần native riêng, không scale tay hay thay skeleton để chữa băng.

## Giữ phần tích lũy

Giữ UI Earth, tìm tên không dấu, editor/cart/skills/level100, giới hạn cơ thể gốc, skin palettes native, copy model, tên/áo/tuổi/quốc tịch, sleeve/socks, Transfer và các face/ảnh từ gói trước ngoài Part3/pc9308. Giữ MulletV13 chỉ89138288266704; Ronaldo2014V18 tại106654775417922; Henry dùng gói Gabri đã nhận; WukongV9, Ghost, Raiden, Joker, Robben, R2017 và các face cũ. Giữ Yan named-face routes và asset Diomande; giữ123mẫu áo xắn/246LOD, matte tóc chỉ89138556572074. Không nhập Python/SO thử trong ZIP face của người dùng.

Giữ tự tách nền offline khi import: chỉ tải worker lúc cần, một luồng WASM, preview/hủy/khôi phục ảnh gốc; dừng khi đóng hoặc hoàn tất. Không chạy trong search hay trận. Với ảnh khó, cần xem preview trước khi lưu.

`extras/Ronaldo2027-89138556572074-MERGED.blend` là đầu NQ27 đã ghép đang dùng, bốn biến thể/166xương/textures đóng gói; giữ nguyên file đã kiểm chứng, không thay bằng đầu4522.

## Kiểm chứng và giới hạn

Validation gồm kiểm thử trên máy build: gateway được bảo vệ, import→login, alias/pixel đọc độc lập, đồng bộ Editor, tám trường motion SQL/native config/wire, cả10type ở đầu vào loader với màu, decoder màu engine gốc, consumer đội hình/captain engine gốc, hai luồng/hai pool, HTTP GET/HEAD/range/SHA, PAK/AES, integrity và cài cập nhật giữ save. Báo cáo cũ giữ nguyên được ghi rõ baseline.

**Chưa thử trên Android/GPU.** Các kiểm tra này chưa chứng minh phụ kiện đã hiện, preview đối thủ hoặc mọi cutscene/replay đã đúng trên máy bạn; không cam kết100% hoặc không lag tuyệt đối. Sau cập nhật, đóng hẳn rồi mở lại; chỉnh trước Enter Game. Nếu cần kiểm tra tiếp, mở đúng thẻ/trận đã chỉnh rồi lấy Runtime Diagnostics mới.

**SOUND đổi riêng từng thẻ chưa triển khai.** Không có nút giả cho tính năng này; animation độc nhất khóa theo danh tính như kiểu chuyền Beckham chưa được chứng minh chuyển riêng bằng tám trường motion.
