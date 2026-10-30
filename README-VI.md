# Mặt gốc bản 73 — thẻ 89136418985302

**Đây là mặt mod gốc dùng đầu `56322`, không phải mesh Ronaldo mặc định `4522`.**

Đã tìm thấy lớp chuyển hướng trong module đóng gói `legends_v10` của bản 73 V16. Chạy lại chính đoạn mã ARM64 đó bằng Unicorn cho kết quả:

| ID thẻ | Nhãn thẻ trong dữ liệu 73 | Đầu được mã gốc trả về |
| --- | --- | --- |
| 89136418985302 | Cristiano Ronaldo 2008 | **56322** |
| 89136418985303 | Cristiano Ronaldo 2012 | 56323 |

Gói này chỉ trích đầu **56322** của thẻ được yêu cầu. Không lấy mesh 56323 hoặc mesh 4522 để thay thế.

## Các file

- `73-ORIGINAL-89136418985302-FACE56322.blend`: đầu gốc đã đưa vào Blender, texture đóng gói trong file, đủ 166 xương.
- `PSK/SK_56322_Face.psk`: mesh LOD0 xuất trực tiếp từ asset gốc, 9.836 đỉnh và 15.708 tam giác.
- `Textures/`: Face D/N/SRO và Hair D được giải mã trực tiếp từ dữ liệu ETC2 gốc. Không chỉnh màu, vẽ lại, fit đầu hoặc thay cấu trúc.
- `Original-IoStore-Chunks/`: byte của mesh, material HQ/MQ và texture lấy nguyên từ gói gốc `custom-resources/legends-v10/pc3700_mobile_and`. Đây là các chunk cooked IoStore/Zen; không phải asset nguồn chưa cook để nhập thẳng vào Unreal Editor.
- `Renders/`: tám góc xem trong Blender. `CONTACT-SHEET.jpg` gom đủ tám góc.
- Các JSON ghi lại kiểm tra đường chuyển hướng, hash asset và kết quả nhập Blender.

Mesh gốc trong IoStore giữ nguyên các LOD của tác giả. File Blender/PSK sử dụng LOD0 để chỉnh sửa. Không sửa ActiveBoneIndices, RequiredBones, BoneMap hoặc trọng số xương của asset gốc.

## Phạm vi kiểm tra

Đã đọc toàn bộ 16.091 mục ZIP trong hai APK hiện có tại workspace, đối chiếu bảng Player/Appearance/Variation và phân tích cả các lớp bytecode lồng nhau trong module gốc. Việc quét ID dạng chữ đơn thuần không tìm được chuyển hướng này vì đoạn xử lý nằm trong payload ARM64 mã hóa dạng chuỗi hex.

Đã kiểm chứng chuyển hướng bằng cách thực thi đoạn mã gốc; không chỉ suy luận từ tên file. Đầu 56322 là asset thêm của gói 73 và không có trong danh sách đầu của container nền dùng để đối chiếu. Hash từng chunk nguyên bản được ghi trong `Original-source-asset-hashes.json`.

Tóc phải được đọc theo platform mip **ETC2 RGBA**, giữ alpha. Bản xuất RGB thông thường của trình đọc cho kết quả sai màu; PNG trong gói được giải mã trực tiếp theo mip RGBA thực tế, không phải ảnh sửa đẹp lại.

Material trong Blender chỉ dựng lại để xem, không mô phỏng đầy đủ shader/ánh sáng eFootball. Material cooked gốc vẫn được giữ riêng. Gói này là dữ liệu trích xuất, **không phải bản vá Android để dán vào APK**.

Các chỉnh sửa Mullet A, Wukong và Joker ở yêu cầu trước đang tạm dừng theo ưu tiên trích mặt này trước.
