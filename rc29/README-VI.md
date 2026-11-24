# FULL8 RC29 · Master League V32 + RC26 cho V19.1

Áp giống hệt FULL8 RC26: **chỉ chép đè `assets/` và `classes5.dex`** vào APK V19.1, ký khóa cũ, cập nhật đè. Không xóa data.
Hai artifact, chép cả hai (cùng gốc `assets/`):
- `FULL8-RC29-V32-ML-part1-core`: `classes5.dex` + phần lớn `assets/`
- `FULL8-RC29-V32-ML-part2-data`: các file model lớn trong `assets/gateway-release` (Java tự giải nén, nén hay không đều được)

## Chống màn hình đen
- **Không** thay bất kỳ file nào engine đọc thẳng từ APK: `dt270`, `dt500`, `pc0010` giữ nguyên bản V19.1.
  (V32 chỉ khác V19.1 ở 2 file âm thanh mở thẻ trong đó; bản V30 full và addon quỹ đạo trước đây đen màn hình vì thay đúng các file này.)
- Không thay `AndroidManifest.xml`, `resources.arsc`, `classes1–4.dex`.
- Không có quỹ đạo bóng / knuckle.

## Gồm
- Master League V32 (`assets/ml-league`, runtime Python V32 trong `assets/chaquopy/app.imy`, Java Master League trong `classes5.dex` gồm cả `MlSaveTransfer` mới của V32).
- Giữ nguyên các phần của RC26: Transfer 122/128, My League, UCL/WC + giải thưởng, Event Edit, Match Settings, Single Player, face 88044950524330 = NR17.

Runtime Python của Master League V32 nằm chung với dữ liệu thẻ của V30/V32 nên không tách riêng được.

Kiểm tra trên máy chủ: 16/16 PASS (gateway, hook RC26, My League, Transfer, UCL/WC, API Master League). Chưa thử trên điện thoại.
Phần tạo mùa Master League cần đội hình thật từ save trên máy, nên chưa kiểm tra được trên máy chủ.
