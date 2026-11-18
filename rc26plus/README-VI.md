# FULL8 RC26 PLUS (không có V30)

Nền là **FULL8 RC26 nguyên bản**. Chỉ thêm hai thứ:

1. **Face:** card 88044950524330 dùng đúng bộ mặt **NR17** (Ronaldo 2017 tóc noodle) của 88042803047215. Đã vá `libnoodle_hair.so` và cập nhật các checksum liên quan (`noodle_hair.py`, `noodle_bundle.json`, manifest). Kiểm tra cổng đăng nhập: PASS.
2. **Quỹ đạo sút kiểu Ronaldo:** `assets/dt270_mobile_all.cpk` (bảng `ball.o`):
   - knuckle lắc 1.0 → 1.6, dải tốc độ 45–105 → 38–125 km/h
   - knuckle bay cao hơn (rise 1.0 → 0.75), cắm mạnh (down 1.0 → 5.0)
   - dipping: rise 1.0 → 0.8, down 10 → 13
   - Magnus giữ nguyên

## Áp dụng (giống RC26)
Chép đè `assets/` và `classes5.dex` vào APK V19.1, ký khóa cũ, cập nhật đè. Không xóa data.
Muốn bỏ quỹ đạo mới: chép lại `assets/dt270_mobile_all.cpk` từ APK V19.1 gốc.

Chưa thử trên điện thoại.
