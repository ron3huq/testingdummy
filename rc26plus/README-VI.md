# FULL8 RC26 PLUS (không có V30)

## Gói 1: FULL8-RC26-PLUS-FACE (áp như RC26)
RC26 nguyên bản + face NR17 cho 88044950524330. Chỉ đổi file trong `assets/gateway-release` (Java tự giải nén) nên áp y hệt RC26: chép đè `assets/` + `classes5.dex`, ký khóa cũ, cập nhật đè.

## Gói 2: quỹ đạo sút (`assets/dt270_mobile_all.cpk`) — PHẢI CHÉP KHÔNG NÉN
`dt270` là file engine đọc thẳng từ APK. Trong APK gốc nó được lưu **không nén (Store)**. Nếu MT Manager nén lại khi thay file → **vào game màn hình đen**.
Trong MT Manager khi thay/thêm file này: chọn **mức nén = Không nén / Store (0)**, rồi ký. Kiểm tra lại trong thuộc tính file trong APK: phương thức nén phải là Stored.
Muốn bỏ: chép lại `dt270_mobile_all.cpk` từ APK V19.1 gốc (cũng Store).

Thông số: knuckle lắc 1.0→1.6, dải 45–105→38–125 km/h, bay cao hơn (0.75), cắm mạnh (5.0); dipping rise 0.8, down 13; Magnus giữ nguyên. Chưa thử trên điện thoại.
