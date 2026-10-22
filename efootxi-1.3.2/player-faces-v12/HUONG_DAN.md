# Faces v12 — material component, ảnh thẻ và tên Xuân Son

Gói cho efootxi Android 1.3.2 ARM64, hotfix v18. **Chưa kiểm chứng renderer trên điện thoại.**

## Cài

Buộc dừng game. Nếu đã cài đầy đủ v10/v11, dùng `Faces-v12-update-from-v11.zip`: gộp `work/` và `livedata/` vào `files/embedded-gateway/`, ghi đè đủ 7 tệp. Nếu chưa chắc bản cũ đầy đủ, dùng `Faces-v12-12-cards.zip` và gộp cả hai thư mục (11 tệp). Không cài đồng thời hai ZIP; không xóa save hay dữ liệu ứng dụng. Mở lại game.

Gói update lớn hơn v11 vì có container chứa ảnh thẻ Xuân Son mới. `gateway_runtime.py` vẫn 2441 byte; các tệp áo/v18 giữ nguyên.

## Thay đổi

- Chỉ 4 thẻ lỗi mặt đen: Ronaldo 2017 `88044950524330`, 2027 `106734785925546`, Jr `105765448873424`, Hoàng Đức `105643042189511`. Gán material Face riêng vào slot0 của component đang giữ đúng mesh riêng, qua API SetMaterial của UE; kiểm tra lại kết quả. Không sửa material dùng chung, slot tóc, Face ID, skeleton, inverse binds hoặc LOD.
- Giữ nguyên từng byte của toàn bộ 264 chunk đầu/tóc đã cài. Hai texture ảnh thẻ Adriano/Xuân Son được thêm riêng.
- Thẻ `88045755960841`: hai ảnh mới theo bố cục Epic xanh lục/xanh lam từ ảnh Xuân Son đã gửi. Giữ các lớp khung, OVR, sao và vị trí do game vẽ.
- Đổi riêng ID trên thành `Nguyen Xuan Son` trong đường UI `GetPlayerName`. Chưa xác minh mọi màn hình/cache trên điện thoại đều đi qua hàm này; không sửa toàn bộ tên Adriano trong database.
- Màu da toàn thân Xuân Son/Pendant/Speed giữ cơ chế native index6 của v11. Không sửa thêm các mặt đã được xác nhận đẹp.

## Đọc log

`files/embedded-gateway/work/tools/noodle-hair-status.json`, version `player-faces-v12-material-seams`.

`head_material_rebinds`: số lần SetMaterial; `head_material_confirmed`: slot0 đọc lại đúng material riêng; `head_component_mismatch`: chưa tìm thấy component giữ đúng mesh; `head_material_rebind_failed`: engine không giữ kết quả. `bake_owner_missing`, `bake_texture_missing`, `bake_material_missing` phân biệt nguyên nhân v11 bỏ qua. `xuan_son_name_changes` đếm lần đổi tên qua UI.

Kiểm tra bốn đầu lỗi trong gameplay/replay/cutscene, thẻ Xuân Son trong đội hình và màn chi tiết. Nếu còn đen, gửi log v12 cùng ảnh mới để phân biệt lỗi binding và shader. Không coi HOOK_ACTIVE hoặc các kiểm tra Unicorn là bằng chứng renderer đã hết lỗi.

432 kiểm tra ARM64 đã qua; 7 đường cài detour, checksum/manifest/idempotence đã qua. UEViewer đã đọc ngược ảnh thẻ từ container mới. Các API material, cấp phát FString và thân engine bake được mô hình hóa tại biên; chưa chạy renderer Android.

Tắt thay đầu bằng `Tat-thay-dau-v12.zip` (ghi đè cấu hình work/tools). Muốn quay lại v11, buộc dừng rồi cài lại gói v11 đầy đủ.
