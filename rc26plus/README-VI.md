# FULL8 RC26 PLUS (không có V30)

Áp y hệt RC26: chép đè `assets/` + `classes5.dex`, ký khóa cũ, cập nhật đè.
**KHÔNG** thay `dt270_mobile_all.cpk` nữa — giữ nguyên file gốc của V19.1.

Gồm:
- Face NR17 (Ronaldo 2017 noodle hair) cho 88044950524330.
- Quỹ đạo sút kiểu Ronaldo, chỉnh **lúc game chạy** (trong `noodle_hair.py`): tìm bảng vật lý bóng trong bộ nhớ, ghi đè thông số, tự ghi lại nếu game nạp lại bảng.
  - Dipping (xoáy lên): bay cao hơn (topSpinRiseDecRate 1.0→0.7), cắm xuống gắt hơn (topSpinDownDecRate 10→15).
  - Knuckle (không xoáy): lắc 1.0→1.6, dải tốc độ 45–105→38–125 km/h, bay cao (0.75), cắm (5.0).
  - Magnus (độ cong) giữ nguyên.

Kiểm tra: trong Diagnostics, mục `noodle-hair-status.json` → `ball_trajectory.state` = `APPLIED` là đã chạy.
Chưa thử trên điện thoại.
