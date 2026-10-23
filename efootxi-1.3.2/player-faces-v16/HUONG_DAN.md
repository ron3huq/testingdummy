# Faces v16 — đầu/bóng, tên native và ảnh thẻ

Gói đầy đủ cho efootxi Android1.3.2 ARM64, hotfix v18. Không root, cài bằng MT Manager.

## Cài

1. Buộc dừng game.
2. Giải nén **Faces-v16-13-cards.zip**, chép đè/gộp cả `work/` và `livedata/` vào `files/embedded-gateway/`. Không lồng thêm thư mục ZIP, không xóa save/dữ liệu ứng dụng.
3. Mở lại game, hoàn tất cập nhật dữ liệu. Manifest v16 dùng offset34 (v15 là33), checksum mới, giữ idempotence.
4. Đọc `work/tools/player-faces-v16-status.json`, version phải là `player-faces-v16-head-shadow-names`. `noodle-hair-status.json` vẫn ghi tương thích.

## Mặt đen: điều đã biết và thay đổi v16

Video người dùng gửi cho thấy đầu Ronaldo2017 có vùng đen/đốm đỏ, các mảng tam giác da bình thường xen kẽ, tóc/tay vẫn có màu. Log v15 xác nhận MQ parent7680 lần, mismatch0; vậy v15 đã tải shader mới nhưng **vẫn thất bại trên điện thoại**, không thể quy lỗi cài thiếu hoặc tiếp tục gọi các bộ đếm đó là bằng chứng đã hết đen.

V16 giữ nguyên toàn bộ277 chunk đầu/tóc từ v15, gồm shader MQ, geometry, UV, texture, skeleton, inverse bind và weight. Thay đổi xử lý render riêng bốn ID:

- `88044950524330` Ronaldo2017
- `106734785925546` Ronaldo2027
- `105765448873424` RonaldoJr
- `105643042189511` HoàngĐức

Trên component đang giữ đúng mesh riêng đã được callback xác nhận, tắt nhận bóng MobileCSM rồi báo render-state-dirty qua hàm engine. Nếu các array face/stencil của actor còn một component khác giữ **cùng nguyên mesh đầu riêng** và đang vẽ trong main pass, dùng `SetRenderInMainPass(false)` để nó không vẽ chồng lần nữa; giữ chức năng cast shadow của nó. Không ẩn body/đổi material body/đổi ID cầu thủ. Các component giữ mesh khác được bỏ qua.

Đây là hướng kiểm tra bóng và bề mặt vẽ chồng theo video. **Chưa chứng minh đó là nguyên nhân duy nhất và chưa kiểm chứng đã hết đen trên renderer Android.** Tắt nhận CSM có thể làm bóng đổ lên đầu nhẹ hơn so với native; mesh vẫn dùng vật liệu có ánh sáng. Không hứa100% trước khi có hình từ máy.

Log bổ sung: `head_csm_receive_disabled`, `head_shadow_checks`, `duplicate_private_head_candidates`, `duplicate_private_head_mainpass_disabled`, `head_shadow_last_card`. Bộ đếm tăng chỉ chứng minh nhánh xử lý đã chạy.

## Tên trên thẻ, trong trận và áo đấu

V15 gọi getter tên và setter áo nhưng chưa đủ: setter áo chỉ lưu chuỗi actor, không tự dựng lại texture chữ đã tạo. V16 cập nhật đúng bốn trường tên61byte trong **record native có typed full CardID trùng khớp** ngay trước khi lookup trả về. Không sửa Player.bin hay record dùng chung baseID; không đổi chỉ số. Các widget/copy tên lấy từ record sẽ nhận tên mới.

Tên áo được thay trong text config **trước bước hash/cache và vẽ glyph**, không chỉ ghi chuỗi sau khi texture áo đã có. Giữ các tham số font/màu/số áo khác. Có thêm chặn hai setter char/std::string để các lần nạp sau không ghi lại tên gốc.

| Card ID | Tên hiển thị | Tên áo |
| --- | --- | --- |
|88045755960841|Nguyen Xuan Son|XUAN SON|
|88038776539586|Nguyen Dinh Bac|DINH BAC|
|105643042189511|Nguyen Hoang Duc|HOANG DUC|
|106728863696709|Do Hoang Hen|HOANG HEN|
|105848932271764|Cao Pendant Quang Vinh|QUANG VINH|
|105874433662542|Nguyen Tai Loc|TAI LOC|
|88033139360669|IShowSpeed|ISHOWSPEED|
|105765448873424|Ronaldo Jr|RONALDO JR|

Các Ronaldo khác giữ tên gốc. Tên Latin không dấu phù hợp font game. Ảnh không vẽ sẵn tên, tên trên thẻ do UI game lấy từ record. Chưa xác nhận mọi cache/widget đặc biệt trên điện thoại đã đổi; cần mở lại thẻ và xem trận sau khi khởi động đầy đủ.

Log: `record_name_fields_updated` (thực sự ghi record tên), `record_name_field_rejections` (ID/schema không hợp lệ nên bỏ qua), `native_shirt_setter_intercepts`, `shirt_render_text_replaced` (thay text trước tạo texture). Không lấy `shirt_name_changes` đơn lẻ làm bằng chứng chữ đã xuất hiện.

## Ảnh thẻ

Làm lại11 cặp, nền sân vận động có chiều sâu nhẹ, bỏ nền neon/mảnh pha lê, dùng ảnh gốc làm tham chiếu, giữ trang phục và nhận dạng. Vẫn có công cụ tạo/chỉnh ảnh; không tuyên bố chân dung giữ từng pixel nguyên bản.

- Hoán đổi **cả ảnh lớn và miniface**: ID2006 `89135066911146` dùng ảnh tham chiếu `ronaldo 2008.png`; ID2008 `106726716084650` dùng `ronaldo 2006.png`, đúng yêu cầu hoán đổi. **Không hoán đổi face3D**, tên, chỉ số hay ID.
- Ảnh lớn184×256, miniface128×128; bố cục riêng, co đồng đều/cắt khung, không kéo giãn. Đã đối chiếu thumbnail native Adriano/Pato. Chừa vùng góc trái cho điểm/vị trí/emblem; không vẽ thêm lớp UI.
- Có ảnh Hoàng Hên, Xuân Son, Đình Bắc, Hoàng Đức, Pendant, Speed, Junior và bốn Ronaldo2006/2008/2013/2017.

Xem `card-layout-preview.png`. Các thẻ không có ảnh mod từ v15 không được tự thay ảnh mới.

## Giữ nguyên và kiểm tra

Giữ đủ13 ID của v15. Skeleton166, RequiredBones166/153 và toàn bộ mesh/texture đầu giống hệt v15; không dựng lại compact pose đã từng làm kéo tay/chân. Binary áo/hotfix v18 và màu thân giữ nguyên. 686 kiểm tra native ARM64,12 đường cài hook,22 ảnh xuất độc lập bằng UEViewer, checksum manifest/ZIP. 1296 trường hợp selector áo dùng lại vì binary/runtime giống byte v15.

**Giới hạn:** engine/RHI/render/glyph có phần được mô hình hóa; chưa chạy renderer Android. `device_verified` vẫn false. Sau cài cần kiểm tra bốn mặt lỗi, tên UI/trận/tên áo, miniface/ảnh lớn và cutscene/replay. Nếu còn lỗi chỉ cần logv16 và hình/video; không yêu cầu toàn bộ thư mục game.

`Tat-thay-dau-v16.zip` tắt redirection; khởi động lại game để bỏ trạng thái render/tên đã thay trong bộ nhớ. Để quay về v15 phải chép lại gói v15 đầy đủ.
