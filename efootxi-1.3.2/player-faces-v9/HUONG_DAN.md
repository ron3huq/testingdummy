# Faces v9 — 11 thẻ, bản cần xác nhận hiển thị trên Android

Dành cho efootxi Android 1.3.2 ARM64, đã cài hotfix v18; không cần root.

## Phạm vi

| ID đầy đủ | Mặt |
|---|---|
|88044950524330|Ronaldo 2017 — thử sửa mặt đen|
|89135066911146|Ronaldo 2006 — giữ nguyên v8|
|106781745353130|Ronaldo 2013 — giữ nguyên v8|
|106734785925546|Ronaldo 2027 — thử sửa mặt đen|
|105765448873424|Ronaldo Jr — thử sửa mặt đen|
|88045755960841|Nguyễn Xuân Son — chỉ chỉnh màu da sẫm hơn|
|88038776539586|Nguyễn Đình Bắc — giữ nguyên v8|
|105643042189511|Nguyễn Hoàng Đức — ID mới theo yêu cầu mới nhất|
|106728863696709|Đỗ Hoàng Hên|
|105848932271764|Pendant Quang Vinh|
|105874433662542|Nguyễn Tài Lộc|

Không tác động ID Hoàng Đức cũ 105850542916637. Không đổi Face ID gốc, tên, chỉ số hay thiết kế thẻ.

## Cài đặt bằng MT Manager

1. Buộc dừng game.
2. Giải nén Faces-v9-11-cards.zip. Gộp hai thư mục work/ và livedata/ vào files/embedded-gateway/ của game, đồng ý ghi đè đủ 11 tệp.
3. Không xóa dữ liệu ứng dụng hoặc save. Không chỉ chép một mình container hay thư viện; checksum của gói phải đồng bộ.
4. Mở lại game và kiểm tra mặt ở cả trận đấu và replay/cutscene. Bản này giữ nguyên bộ xương 166 xương và danh sách RequiredBones từng LOD đã hết lỗi biến dạng theo xác nhận v8 của người dùng.

Áo: giữ nguyên chính sách v8/v18, 2017/2006/2013 và Messi 17592722922839 dài tay, 2027 ngắn tay. Các thẻ mới giữ cấu hình tay áo hiện có.

## Những gì đã làm và giới hạn

Các asset đã được người dùng xác nhận tốt được bảo vệ bằng đối chiếu SHA-256 từng tệp; riêng Xuân Son chỉ thay Face_D, không sửa mesh, mắt/miệng, tóc hay rig. Màu da khuôn mặt được điều chỉnh, không đồng nghĩa thay màu da toàn thân.

Ba mặt đen dùng tên package mới để tách khỏi các asset cũ và dựng lại tiếp tuyến theo vị trí/UV thực. Đây là hướng sửa tiếp theo sau khi làm phẳng normal ở v8 không giải quyết lỗi trên điện thoại. Chưa chứng minh nguyên nhân gốc của lỗi mặt đen bằng renderer Android; không được coi việc giải mã texture hay kiểm tra Unicorn là bằng chứng đã hết mặt đen.

Bốn mặt mới được kiểm tra mesh, vật liệu, texture và các trọng số điều khiển mắt/miệng. Không chuyển được toàn bộ biểu cảm PC. Hoàng Hên có mask tóc riêng; Hoàng Đức có phần da đầu riêng. Chất lượng khớp mặt và màu da cần người dùng xác nhận trong game.

Nếu ba mặt vẫn đen, cần log files/embedded-gateway/work/tools/noodle-hair-status.json sau khi mở các thẻ và ảnh cùng góc nhìn. Không cần chép toàn bộ thư mục game. Để tắt thay đầu, chép Tat-thay-dau-v9.zip theo cùng cách; để quay lại v8, chép lại nguyên gói v8.

## Tên và thiết kế thẻ

Nguồn nghiên cứu trong repo xác định Player.bin chứa tên ở byte 332..399 của record 400 byte, ID64 ở +8. Chưa có hook tên được kiểm chứng cho tất cả màn hình và cache của bản này. Vì vậy có cơ sở để nghiên cứu đổi tên, nhưng v9 không tuyên bố đã đổi tên trong game.

Có thể thiết kế ảnh thẻ theo ảnh người dùng cung cấp. Việc tích hợp riêng từng ID cần xác định texture/ảnh tải ngoài, atlas, kích thước và cache mà giao diện thẻ sử dụng. Mặt 3D và ảnh thẻ là hai nguồn tài nguyên khác nhau. Pipeline này chưa kiểm chứng chức năng thay artwork thẻ trong game.
