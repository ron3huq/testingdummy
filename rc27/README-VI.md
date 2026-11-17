# FULL8 RC27 · V30 + RC26 (Master League) trên nền V19.1

Gói này đưa **toàn bộ những gì V30 thêm/sửa** so với V19.1 (Master League mới `ml-league` + các module `iml_*`, UCL/WC gốc của V30, face-conversion, card-art, anti-scam, thẻ mới tháng 11, đa ngôn ngữ…) vào V19.1, và **giữ lại các tính năng RC26** (Transfer Edit My League 122/128, Event Edit UCL/WC 901/902, Match Settings, Single Player, Diagnostics, mặt/face Ronaldo, áo đấu mới, bảng vua phá lưới Cup).

## Gói gồm 2 artifact ZIP — cần chép cả hai

Tải từ GitHub Actions (đăng nhập GitHub, artifact lưu 30 ngày). Actions dựng từ V30 + RC26 gốc trong release + `RC27-DELTA.zip`, kiểm tra SHA256 từng file.

| File | Nội dung |
|---|---|
| artifact `FULL8-RC27-V30-MERGE-part1-core` | `AndroidManifest.xml`, `resources.arsc`, `classes.dex`…`classes5.dex`, phần lớn `assets/` |
| artifact `FULL8-RC27-V30-MERGE-part2-data` | 5 file dữ liệu lớn trong `assets/` (pc0010, dt500, card-art, legends pc3700) |

## Áp bằng MT Manager

1. Sao lưu APK và save.
2. Mở bản sao **APK V19.1 gốc** (không cần áp RC26 trước — RC27 đã chứa sẵn RC26).
3. Chép đè **toàn bộ nội dung gốc** của part1 rồi part2 vào APK: `assets/`, `classes*.dex`, `AndroidManifest.xml`, `resources.arsc`.
4. Lưu, ký bằng **khóa cũ**, cập nhật đè. **Không xóa data, không gỡ game.**
5. Đóng hẳn game rồi mở lại. Lần đầu sẽ giải nén lại Python runtime và tài nguyên (lâu hơn bình thường).

> AndroidManifest của V30 có `versionCode` cao hơn V19.1, minSdk 28. Nếu MT Manager báo lỗi khi thay manifest, có thể giữ manifest cũ của V19.1 — các phần còn lại vẫn dùng được.

## Đã làm gì

- **Python gateway**: giữ **nguyên** runtime V30 (`_protected_runtime.pyc`, 268 module). Thêm module nhỏ `rc26_hook.pyc` vào `app.imy`; Java (`EmbeddedGateway.startPython`) nạp nó ngay sau `install_root`, nó gắn đúng hook `bridge_73` của RC26 → 121 file RC26 `work/tools` được nạp sau khi gateway V30 khởi tạo.
  - Cup/UCL: V30 đã có sẵn đúng bộ cup V25 (mới hơn) nên adapter `rc22_v25_events` được viết lại để **dùng module gốc của V30**, không thay `cup_entry` nữa; vẫn giữ bảng giải thưởng RC24, đội hình Event Transfer, AI LEGEND, mô hình mô phỏng UCL.
  - Thẻ Ronaldo 2017 (89136418985332): V30 đã có sẵn trong gói era-six → lớp thêm thẻ của RC26 tự tắt trên V30 (tránh lỗi trùng ID).
- **classes5.dex**: trộn 3 chiều V19.1/RC26/V30 theo từng method (V30 làm nền; thêm 313 class RC26; vá tay EmbeddedGateway, LauncherWeb, GatewayBootActivity…). Kiểm tra tham chiếu: 0 lỗi thiếu class/method.
- **dt870 (database)**: V30 sửa Player/Coach/Appearance…, RC26 thêm 41 file áo đấu → dựng lại CPK chứa cả hai (công cụ CPK đã kiểm chứng dựng lại đúng từng byte file RC26). Checksum kits/noodle/manifest được cập nhật dây chuyền.
- **Launcher**: dùng launcher V30 (đa ngôn ngữ, giới thiệu, lọc quốc tịch/đội…) + thêm các nút RC26: Single Player, Transfer, UCL Event Edit, World Cup Event Edit, Match Settings, Diagnostics; công cụ riêng trong Player Editor.
- **Face**: **88044950524330 dùng đúng bộ mặt NR17 của 88042803047215** (Ronaldo 2017 tóc noodle). Vá `libnoodle_hair.so`: mọi nhánh native theo card 88044950524330 đi đúng nhánh của 88042803047215; 42 card face khác giữ nguyên (đã chạy giả lập hàm chọn profile cho toàn bộ danh sách).

## Kiểm tra (trên máy chủ, chưa thử trên điện thoại)

Khởi động gateway V30 + RC26: PASS · My League adapter: INSTALLED · Transfer 122 (40/40 đội) & 128 (32/35) mở được, Barcelona OK · UCL & WC Event: 3 trận/giải, bảng ghi bàn, CPU LEGEND: PASS · Login livedata dt870 mới: PASS · Login guard checksum lồng nhau (cố tình làm hỏng bị chặn): PASS · Master League: tạo hồ sơ ML OK, hành vi giống hệt V30 gốc (mùa đấu đầy đủ cần dữ liệu thế giới chỉ có trên máy).

**phone_verified: false** — hãy thử trên máy và báo lỗi (kèm Diagnostics) nếu có.
