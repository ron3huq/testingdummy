# V17 — sửa lỗi tài nguyên chữ/số áo và quốc tịch; mặt đen CHƯA xác minh sửa được

Gói chính `Faces-v17-jersey-nationality.zip` giữ nguyên toàn bộ asset đầu/tóc/ảnh thẻ của v16. Không đổi Face ID, skeleton, inverse bind, BoneMap hay LOD. Không sửa các mặt đã được người dùng xác nhận tốt.

Các thay đổi trong mã:
- Bỏ việc thay FString đầu tiên của cấu hình texture áo thành tên người. Hàm native dùng chuỗi này làm đường dẫn tải font atlas; thay bằng tên sẽ dẫn tới tài nguyên không tồn tại. V17 giữ nguyên từng byte cấu hình và khóa cache do game tính. Đây là sửa nguyên nhân cụ thể có thể gây mất cả chữ và số; hình ảnh trên điện thoại vẫn cần xác nhận.
- Chuỗi tên áo Việt Nam: Xuan Son, Dinh Bac, Hoang Duc, Hoang Hen, Quang Vinh, Tai Loc. Các chuỗi khác: IShowSpeed, Ronaldo Jr. Không viết hoa toàn bộ. Không đổi số áo.
- Giữ cách đổi tên UI đã được người dùng xác nhận hoạt động ở v16.
- Quốc tịch đúng 8 Card ID được đổi tên: sáu cầu thủ Việt Nam dùng Việt Nam; IShowSpeed và Ronaldo Jr dùng Bồ Đào Nha. Đọc Country.bin và theo đúng hàm nhập/setter native, không dùng nhầm mã ảnh cờ hoặc ISO. Không đổi quốc tịch các thẻ Ronaldo gốc.

Cài gói chính: buộc dừng game, giải nén ZIP, gộp/chép đè CẢ `work/` và `livedata/` vào `files/embedded-gateway/`, rồi mở lại. Không xóa save hay dữ liệu ứng dụng. Gateway giữ nguyên 2441 byte.

Log: `files/embedded-gateway/work/tools/noodle-hair-status.json`. Gói chính phải ghi `player-faces-v17-jersey-nationality`; có thêm `nationality_changes`, `nationality_last_card`, `nationality_internal_code`, `four_face_comparison_mode` (gói chính = 0).

## Đối chiếu bốn mặt đen — chỉ để kiểm tra

V16 đã được người dùng xác nhận vẫn đen. Các bộ đếm gắn material/MID thành công không chứng minh renderer hoạt động đúng. Phiên này không có renderer Android; không tuyên bố đã sửa hết mặt đen.

Sau khi cài gói chính, có thể dùng `Faces-v17-compare-four-with-2006.zip`: buộc dừng game, chép đè `work/` của gói này vào cùng `embedded-gateway/`, mở lại. Gói đối chiếu tạm dùng CHÍNH đầu/tóc/material/texture ND06 của bản 2006 đang chạy tốt cho đúng bốn thẻ:
- 88044950524330 (2017)
- 106734785925546 (2027)
- 105765448873424 (Jr)
- 105643042189511 (Hoang Duc)

Chín thẻ còn lại, thân, tên, số áo và Face ID không bị chuyển. Đây KHÔNG phải diện mạo hoàn thiện của bốn cầu thủ. Không coi gói này là bản sửa xong. Phiên bản log phải là `player-faces-v17-compare-working-2006`, `four_face_comparison_mode = 1`.

Kiểm tra một thẻ bị đen trong cùng cảnh trước đây: đầu 2006 có còn đen không? Một ảnh kèm log chế độ đối chiếu đủ để quyết định bước tiếp; không cần gửi thư mục game.

Khôi phục đúng các đầu riêng bằng `Faces-v17-restore-own-heads.zip`: buộc dừng game, gộp `work/`, mở lại. Hoặc chép lại gói chính. Khôi phục vẫn giữ phần sửa chữ/số áo và quốc tịch.

Kiểm tra máy chủ: mỗi chế độ chạy 692 kiểm tra ARM64, 12 đường cài detour, manifest/checksum/idempotence; setter quốc tịch chạy thân hàm native và giữ nguyên byte lân cận, getter chạy với bản ghi nguồn thật. GPU/renderer, chữ số áo, cờ UI, mặt và replay trên Android của v17 chưa được người dùng xác nhận.
