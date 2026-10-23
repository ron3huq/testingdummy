# Faces v14 — material động cho bốn đầu đen và ảnh thẻ

**Chưa xác minh renderer trên Android.** Log v13 người dùng gửi đã xác nhận static material đúng6648lần nhưng vẫn đen; không coi các bộ đếm binding là bằng chứng hết lỗi.

## Cài đầy đủ

Tải `Faces-v14-13-cards.zip`. Buộc dừng game. Gộp **cả work/ và livedata/** vào `files/embedded-gateway/`, ghi đè đủ11tệp. Không xóa save/dữ liệu, không chép source/ vào game. Mở lại rồi kiểm tra bốn thẻ từng đen trong gameplay và replay/cutscene.

Log riêng: **work/tools/player-faces-v14-status.json**. Kiểm tra version là player-faces-v14-material-seams, state, error, runtime_path và session/timestamp mới. V14 không đổ lỗi cho cài đặt v13; log cũ đã xác nhận v13 hoạt động thật.

## Thay đổi mặt đen

Chỉ bốn ID: 88044950524330(Ronaldo2017),106734785925546(Ronaldo2027),105765448873424(Jr),105643042189511(Hoàng Đức).

V14 tạo một **UMaterialInstanceDynamic riêng theo actor** bằng factory native UE, kế thừa Face MIC riêng đã xác minh. Gán tường minh BaseColorMap/NormalMap/SROMap từ ba texture riêng cùng biến thể, rồi gắn MID vào slot0 của đúng component mang private mesh. Không ghi vào source MIC dùng chung hoặc cache bake của actor. Sau bake, kiểm tra/khôi phục tham số nếu engine đổi; không tạo lại hay gửi lại tham số khi MID vẫn đúng. Nếu MID đã bị gỡ khỏi component, không dereference con trỏ cache cũ; tạo lại để tránh dùng UObject sau GC. Chỉ cache material đang có component giữ tham chiếu; kiểm tra parent và outer.

Đây là thay đổi đường cấp tham số/uniform riêng cho shader. **Chưa có bằng chứng renderer trên điện thoại rằng nó hết đen.** Không thay geometry, UV, tangent, vertex colors, rig, LOD, texture đầu hoặc Face ID. Toàn bộ277chunk đầu/tóc của13thẻ giống v13 từng byte. Áo và màu da giữ nguyên.

Bộ đếm mới: face_mid_created (tạo MID), face_mid_binding_checks (dùng MID cho component), face_mid_channels_confirmed (CPU getter đọc lại đủ3texture đúng), face_mid_source_channels_invalid, face_mid_failures, face_mid_cache_hits, face_mid_last_card_id. Getter thành công không phải xác minh GPU/ảnh điện thoại. Nếu còn đen, gửi log riêng v14 và ảnh mới.

## Ảnh thẻ

Chín cặp ảnh lớn/nhỏ từ Card.rar theo bảng CARD_MAPPING.md. Dùng ronaldo2008.png cho106726716084650; bỏ ảnhplus theo lựa chọn người dùng. Không đổi chỉ số/khung/huy hiệu/đội/quốc tịch hay tên trong các đường UI chưa xác minh.

Xuân Son88045755960841: chỉ đổi ảnh nhỏ128x128 thành cận mặt như icon Ronaldo; ảnh lớn184x256 giữ nguyên byte của v13. Tổng19UItextures cập nhật. Đã đọc ngược đủ19bằng UEViewer.

## Kiểm tra

502 kiểm tra ARM64, bao gồm thân factory UMID và getter native; model các biên UObject construction/parent-init/material parameter update/GPU. Kiểm tra cache, thay đổi tham số sau bake, GC/unbound, chính xác64bit và bảo vệ thẻ khác. Toàn bộ25headmesh/50LOD và các số đo cũ được giữ sau chứng minh277chunk không đổi. Binary/runtime áo v13 được sao chép nguyên byte; báo cáo1296selector cases được tái sử dụng đúng binary. Manifest/checksum/idempotence/gateway2441byte pass.

Không có thiết bị Android trong workspace. Tắt thay đầu bằng Tat-thay-dau-v14.zip sau khi buộc dừng/copy/mở lại; điều này không gỡ ảnh thẻ. Quay lại bằng v13đầy đủ nếu cần.
