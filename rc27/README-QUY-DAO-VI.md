# Add-on quỹ đạo sút "Ronaldo" (knuckle cao rồi cắm + lắc) · thử nghiệm

Engine đọc toàn bộ hằng số bay của bóng từ `ball.o` trong `assets/dt270_mobile_all.cpk` → `common/match/constant/constant_match.bin` (bản biên dịch của `DevelopData/.../match/ball.json`). Struct C++ mặc định là 0 nên bảng này quyết định mọi cú sút/chuyền.

| Tham số | Gốc | Add-on | Ý nghĩa |
|---|---|---|---|
| nonSpinRate | 1.0 | **1.6** | độ lắc của bóng không xoáy (knuckle) |
| nonSpinMin / nonSpinMax | 45 / 105 | **38 / 125** | dải tốc độ (km/h) có hiệu ứng lắc → sút mạnh vẫn lắc |
| nonSpinTopRiseDecRate | 1.0 | **0.75** | knuckle giảm tốc lên chậm hơn → bay **cao hơn** |
| nonSpinTopDownDecRate | 1.0 | **5.0** | sau đỉnh quỹ đạo **cắm xuống mạnh** |
| topSpinRiseDecRate | 1.0 | **0.8** | dipping (xoáy lên) bay cao hơn chút |
| topSpinDownDecRate | 10 | **13** | dipping cắm gắt hơn |
| magnusRate | 0.035 | 0.035 | giữ nguyên (không ảnh hưởng chuyền/cứa lòng) |

Hiệu ứng lắc chỉ có ở bóng **không xoáy** (Knuckle Shot / sút lòng bàn chân mạnh). Muốn "cao – cắm – lắc" kiểu Ronaldo: cầu thủ có skill **Knuckle Shot** (thêm trong Player Editor) và sút mu từ xa. Dipping Shot (xoáy lên) sẽ cao và cắm hơn nhưng engine không cho bóng xoáy lên lắc.

## Áp dụng
Chép đè `AP-DUNG/assets/dt270_mobile_all.cpk` vào APK (sau khi đã áp FULL RC27), ký khóa cũ, cài đè. Muốn bỏ: chép `KHOI-PHUC/assets/dt270_mobile_all.cpk` (bản gốc).

Chưa thử trên điện thoại. Đây là thay đổi vật lý toàn cục; nếu sút quá cao/vọt xà hoặc lắc quá, báo lại để chỉnh mức (công cụ `source/ball_tune.py` có sẵn preset).
