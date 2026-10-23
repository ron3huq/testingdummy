# Faces v15 — efootxi Android 1.3.2 / hotfix v18

Bản đầy đủ: **Faces-v15-13-cards.zip**. Giữ đủ 13 Card ID từ v14, không sửa Face ID, chỉ số, save hoặc hệ thống nhận diện cầu thủ.

## Cài bằng MT Manager — không cần root

1. **Buộc dừng game** trong cài đặt Android.
2. Giải nén ZIP, gộp và chép đè **cả `work/` và `livedata/`** vào thư mục `files/embedded-gateway/` hiện tại. Hai thư mục phải nằm trực tiếp trong `embedded-gateway`, không lồng thêm `Faces-v15…`.
3. Mở game, để hoàn thành cập nhật dữ liệu. Gateway quảng bá revision manifest mới (offset phiên bản 33 thay vì 32 của v14) cùng checksum mới.
4. Xem `files/embedded-gateway/work/tools/player-faces-v15-status.json`. Dòng version phải là `player-faces-v15-native-face-mq`. File `noodle-hair-status.json` vẫn được ghi tương thích.

Không xóa dữ liệu ứng dụng/save. Không cần chép thư mục game lên. ZIP `Tat-thay-dau-v15.zip` chỉ tắt thay đầu nếu cần; không hạ phiên bản manifest.

## Những thay đổi thực tế

- **Bốn mặt đen**: Ronaldo 2017 `88044950524330`, Ronaldo 2027 `106734785925546`, Ronaldo Jr `105765448873424`, Hoàng Đức `105643042189511`: thay parent của 10 material HQ riêng bằng **shader mặt native có ánh sáng `M_Head_Face_MQ`**. Giữ tên/package ID mà mesh đang tham chiếu, cập nhật đúng dependency/import graph. Đây là thay shader thực tế, khác thử gán lại MIC/MID v13–v14. MQ dùng diffuse; không dùng normal/SRO riêng của đường HQ. Vì vậy chi tiết phản xạ da có thể khác HQ.
- Giữ nguyên hình dáng, tóc, xương, trọng số, mắt/miệng của bốn đầu trên. Những đầu khác giữ nguyên, ngoại trừ chỉnh UV và ngưỡng alpha riêng cho Đình Bắc.
- **Đình Bắc**: chặn 40 đỉnh mép UV mỗi LOD lấy mẫu ra vùng đen cạnh atlas; không dịch đỉnh hay đổi weight. Hạ ngưỡng cắt tóc từ khoảng 0,333 xuống 0,20 và bật cờ override rõ ràng, giữ nguyên texture alpha/sợi nguồn. Không vẽ mũ tóc kín. Chưa xác minh hình nhìn nghiêng trên điện thoại.
- **11 cặp ảnh** làm lại nền và bố cục, gồm Xuân Son, Đình Bắc, Hoàng Đức, Hoàng Hên, Pendant, IShowSpeed, Ronaldo Jr, Ronaldo 2006/2008/2013/2017. Ảnh lớn 184×256 và miniface 128×128 được chuẩn bị riêng. Chỉ co đồng đều/cắt khung, không kéo giãn khuôn mặt; không vẽ đè khung, điểm số, sao hay tên mà game đã hiển thị. Dùng ảnh `ronaldo 2008.png`, bỏ `plus` như bạn chọn.
- **Tên hiển thị và tên áo đấu**: tám ID trong bảng dưới. Thêm đường lấy tên native record mà `GetPlayerNameStr` gọi, giữ hook cũ để tương thích; tên áo dùng hàm `SetShirtName` của engine, không chỉ viết tên lên ảnh.
- Giữ nguyên binary áo dài tay/hotfix v18 từ v14: Ronaldo 2017/2006/2013/2008 và Messi `17592722922839` dài tay, 2027 ngắn tay. Màu thân Xuân Son/Pendant/Speed giữ index 6 của v14, màu đầu không đổi.

| Card ID | Tên hiển thị | Tên áo |
| --- | --- | --- |
| 88045755960841 | Nguyen Xuan Son | XUAN SON |
| 88038776539586 | Nguyen Dinh Bac | DINH BAC |
| 105643042189511 | Nguyen Hoang Duc | HOANG DUC |
| 106728863696709 | Do Hoang Hen | HOANG HEN |
| 105848932271764 | Cao Pendant Quang Vinh | QUANG VINH |
| 105874433662542 | Nguyen Tai Loc | TAI LOC |
| 88033139360669 | IShowSpeed | ISHOWSPEED |
| 105765448873424 | Ronaldo Jr | RONALDO JR |

Tên dùng chữ Latin không dấu để phù hợp font game. Các bản Ronaldo khác giữ tên cũ.

## Kết quả kiểm tra và giới hạn

- 607 kiểm tra native ARM64 trong Unicorn, 8 đường cài detour, checksum/manifest/idempotence và ZIP CRC. Engine/RHI/render và setter áo có phần được mô hình hóa tại biên; không tương đương chạy game Android.
- UEViewer độc lập đọc được 10 parent MQ mới và xuất 22 ảnh thẻ đúng kích thước. 264 chunk đầu/tóc không liên quan giống hệt v14; toàn bộ vị trí/triangle/weight và RequiredBones 166/153 của hai LOD được giữ nguyên, tránh quay lại lỗi compact pose gây kéo tay/chân.
- 1.296 trường hợp áo dài tay dùng lại kết quả vì binary selector/runtime giữ nguyên byte so với v14.
- **Chưa kiểm thử renderer điện thoại. Không coi HOOK_ACTIVE, texture_confirmed hay các bộ đếm MID là bằng chứng đã hết mặt đen.** V15 thay shader để tránh đường HQ đang lỗi; chưa chứng minh nguyên nhân cuối cùng trên GPU của máy bạn.
- Log mới: `mq_shader_parent_confirmed` phải tăng khi xem bốn thẻ lỗi; `mq_shader_parent_mismatch` cho biết asset đang tải vẫn có parent khác MQ. `native_ui_name_changes` và `shirt_name_changes` cho biết từng đường đổi tên có thực sự chạy. Không đánh đồng bộ đếm tăng với ảnh đã đúng.
- Sau cài cần xem bốn mặt từng lỗi, miniface/ảnh lớn, tên UI/tên áo, góc nghiêng Đình Bắc và replay/corner. Báo cáo `device_verified` vẫn false đến khi có xác nhận từ điện thoại.

Xem `card-layout-preview.png`, `RESEARCH.md`, mã nguồn và các JSON kiểm tra cùng thư mục.
