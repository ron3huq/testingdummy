# FULL8 RC28 LITE · V30 (Master League) + RC26 cho V19.1

Áp giống hệt FULL8 RC26: **chỉ chép đè `assets/` và `classes5.dex`** vào APK V19.1, ký khóa cũ, cập nhật đè. Không xóa data.

Hai artifact, chép cả hai (cùng gốc `assets/`):
- `FULL8-RC28-LITE-part1-core`: `classes5.dex` + phần lớn `assets/`
- `FULL8-RC28-LITE-part2-data`: các file dữ liệu lớn của V30 (`pc0010`, `dt500`, `legends pc3700`)

## Sửa so với RC27
- Không còn thay `AndroidManifest.xml`, `resources.arsc`, `classes1–4.dex` (nguyên nhân "ứng dụng chưa được cài đặt"). V30 không cần chúng: ID tài nguyên và code giống hệt V19.1.
- Gọn nhẹ hơn: bỏ gói ảnh thẻ `card-art` 312MB (dùng ảnh trong game), bỏ dữ liệu ngôn ngữ khác (chỉ English, ~10MB), bỏ file thừa của RC26 (cup V25 cũ, english-words).
- Launcher: ẩn ô chọn 10/20/30 lượt quay thẻ, tắt hiệu ứng/blur/bóng đổ để nhẹ máy.
- My League: dữ liệu 4 giải UCL, World Nation, Y17, Y08 giữ nguyên. Ba giải khác vẫn nằm trong cấu hình native đã biên dịch của RC26 (bỏ sẽ làm hỏng Transfer), nhưng không tốn gì nếu không chơi.

Giữ nguyên: Master League V30, UCL/WC V30 + giải thưởng RC26, Transfer 122/128, Event Edit 901/902, Match Settings, Single Player, face 88044950524330 = NR17 của 88042803047215.

Kiểm tra trên máy chủ: 16/16 PASS. Chưa thử trên điện thoại.
