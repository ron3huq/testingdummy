# Ronaldo noodle v2 — màu tóc nguồn PC, atlas chi tiết và chỉnh nhẹ má/cằm

Chỉ Card ID **88044950524330**. Người dùng đã xác nhận v1b vào game và thấy tóc, gửi log HOOK_ACTIVE, redirects=1, nonnull_callbacks=1, null_callbacks=0, restore_requests=0, biến thể 4522ep00v0313. Đó là bằng chứng trên thiết bị cho **v1b**; **v2 chưa được thử trên điện thoại**.

## Cài bằng MT Manager

1. Buộc dừng game. Sao lưu `work/tools/noodle_hair.py`, `noodle_bundle.json` và ba tệp `livedata/pc9298_mobile_and.*` hiện có nếu muốn giữ bản đang dùng.
2. Giải nén `Ronaldo-noodle-v2-color-face-88044950524330.zip`.
3. Gộp **cả hai thư mục `work/` và `livedata/`** vào **`files/embedded-gateway/`**, đồng ý ghi đè. Không dán riêng mỗi file Python, không chép vào assets APK.
4. Mở game, nếu được hỏi tải Latest Data thì tải dữ liệu mới. Vào sân bằng đúng thẻ 88044950524330.
5. Kiểm tra `files/embedded-gateway/work/tools/noodle-hair-status.json`: version mới phải là **`ronaldo-noodle-v2-color-face`**, state HOOK_ACTIVE, payload_verified true, error null. Sau khi vào sân, redirects và nonnull_callbacks cần tăng. Log chỉ xác nhận đường tải đầu; cần ảnh trong game để đánh giá màu tóc và khuôn mặt.

## Thay đổi

- V1b chỉ dùng lớp alpha tóc trên nền màu tối. V2 lấy **màu nguyên bản từ hair_parts_bsm_alp** theo UV thứ hai và độ trong/cắt sợi từ **hair_alpha8** theo UV thứ nhất, rồi bake vào một atlas riêng cho shader Android. Các lọn vàng có dữ liệu màu thực từ mod PC; không nhuộm vàng đồng loạt cả đầu.
- Atlas ETC2 RGBA **2048×2048, 12 mip**, thay ảnh 256×256 cũ. Có 299 mảng tóc được xếp UV riêng, giữ 5005 đỉnh và 5179 tam giác tóc đã chạy được trên máy người dùng. Diện tích atlas chia cho nhiều mảng nên 2048 không có nghĩa chi tiết sợi tăng tám lần; nguồn alpha vẫn là 512 và ảnh màu nguồn 1024. Chi tiết cuối cùng còn phụ thuộc thiết lập chất lượng/LOD và ánh sáng của game.
- Chỉnh nhẹ phần mềm hai má và dưới hàm/cằm, tối đa khoảng **2,7 mm**, trên mesh Android. Tính lại normal/tangent tương ứng; giữ UV mặt, trọng số da, chỉ số tam giác, bind pose và skeleton. Vùng mắt/trán phía trên được kiểm tra giữ nguyên tới độ chính xác lưu trữ. Đây là sculpt nhẹ theo ảnh tham khảo, **không phải bản scan mặt 2017 hoặc cam kết giống hệt ảnh**. Không tạo texture da/nhãn cầu mới.
- Giữ nguyên binary hook v1b và gateway v1a 2441 byte. Không sửa save, đội hình, chỉ số, dt200 hoặc dt870. Nâng revision manifest thử từ offset +19 lên +20 để game nhận container đã đổi; giữ nguyên tất cả dữ liệu chính thức khác.

## Quay lại

Buộc dừng game, giải nén `Quay-lai-Ronaldo-v1b.zip`, gộp `work/` và `livedata/` vào `files/embedded-gateway/`, rồi mở lại. Đây là cùng bộ tóc tối và mặt Android gốc của bản v1b đã được người dùng xác nhận tải thành công. Nếu chỉ muốn tắt đầu thử, dùng `Tat-dau-thu-Ronaldo.zip` rồi buộc dừng/mở lại; gói tắt chỉ đổi enabled=false, giữ manifest ổn định.

## Kiểm tra và giới hạn

Đã kiểm tra độc lập bằng UEViewer đọc lại bốn mesh, hai material và texture 2048 từ container, mọi mip được parse, bulk/hash round-trip, giữ cấu trúc skeleton/skin/UV mặt, kiểm tra mức sculpt, UV tóc và hình học tóc. Kiểm tra pixel ETC2 thật cho sai số alpha trung bình 0,843/255 và màu vùng nhìn thấy 2,378/255. Kiểm tra gateway hash, idempotence, nhánh tắt và response gốc; bảo đảm ZIP chỉ có whitelist tám tệp cài. Native binary giữ byte-identical bản v1b.

Shader vẫn là shader tóc MQ có sẵn của Android, chưa tái tạo toàn bộ hiệu ứng FOX PC như specular/two-layer shader riêng. Atlas gộp hai lớp màu/alpha để chạy trên shader đó. Chưa xác nhận v2 bằng renderer Android; không thể gọi kết quả là photorealistic hoặc hoàn thiện khuôn mặt chỉ từ kiểm tra trên máy phân tích.

Nguồn tóc PC NEUBE do người dùng cung cấp. Các script bake/build/kiểm tra và report nằm cùng nhánh tải.
