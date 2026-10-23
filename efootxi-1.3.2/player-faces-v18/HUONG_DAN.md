# V18 — bốn đầu riêng dựng lại, tên áo đầy đủ, sáu thẻ Việt Nam không CLB

Chỉ cài một gói: `Faces-v18-13-cards.zip`. Gói này thay thế cả chế độ đối chiếu v17. Không cần cài lại ba gói v17.

1. Buộc dừng game.
2. Giải nén ZIP, gộp/chép đè CẢ `work/` và `livedata/` vào `files/embedded-gateway/` bằng MT Manager.
3. Mở lại game. Không xóa save hoặc dữ liệu ứng dụng.

## Bốn đầu bị đen

Người dùng đã xác nhận: CHÍNH bốn thẻ 2017/2027/Jr/Hoàng Đức hiển thị đầu 2006 bình thường khi dùng gói đối chiếu. V18 dùng phần cấu trúc asset và material tĩnh từ bộ ND06 đã được kiểm tra trên điện thoại để dựng lại bốn bộ đầu riêng:

- 88044950524330: Ronaldo 2017, không phải đầu 2006.
- 106734785925546: Ronaldo 2027, không phải đầu 2006.
- 105765448873424: Ronaldo Jr, không phải đầu 2006.
- 105643042189511: Nguyen Hoang Duc, không phải đầu 2006.

Giữ nguyên toàn bộ byte hai LOD, hình dáng mặt, tóc, vertex weight/BoneMap, Active/RequiredBones, skeleton và bind pose của bốn đầu; giữ nguyên payload texture của từng người. Bộ material được dựng lại từ ND06 và dùng MIC tĩnh như bộ đã chạy tốt, bỏ thử nghiệm tạo MID riêng ở bốn đầu. Các đường dẫn private mới NV01/NV27/NVJR/NVHD chỉ chọn theo đúng full Card ID; không đổi Face ID hay hệ thống nhận diện cầu thủ.

Đây là bản sửa cần kiểm tra trên điện thoại. Việc đầu 2006 hết đen đã xác nhận phạm vi điều tra, nhưng chưa chứng minh renderer của bốn đầu riêng v18 hoạt động đúng. Không hứa đã hết đen 100% khi chưa có xác nhận mới.

## Tên áo và CLB

Theo lựa chọn mới nhất của người dùng, tên áo dùng đầy đủ chữ HOA để font gốc vẽ được mọi ký tự. Không thêm/thay font, texture font, cỡ chữ hoặc cấu hình bố trí chữ của bất kỳ áo nào. Chuỗi đường dẫn tài nguyên font giữ nguyên, không ghi tên người vào đường dẫn như lỗi v16.

| Card ID | Tên giao diện | Tên trên áo | Quốc tịch | CLB trong bản ghi thẻ |
|---|---|---|---|---|
| 88045755960841 | Nguyen Xuan Son | XUAN SON | Việt Nam | Không CLB |
| 88038776539586 | Nguyen Dinh Bac | DINH BAC | Việt Nam | Không CLB |
| 105643042189511 | Nguyen Hoang Duc | HOANG DUC | Việt Nam | Không CLB |
| 106728863696709 | Do Hoang Hen | HOANG HEN | Việt Nam | Không CLB |
| 105848932271764 | Cao Pendant Quang Vinh | QUANG VINH | Việt Nam | Không CLB |
| 105874433662542 | Nguyen Tai Loc | TAI LOC | Việt Nam | Không CLB |
| 88033139360669 | IShowSpeed | ISHOWSPEED | Bồ Đào Nha | Giữ nguyên |
| 105765448873424 | Ronaldo Jr | RONALDO JR | Bồ Đào Nha | Giữ nguyên |

Không sửa số áo; không sửa danh sách thành viên đội hoặc đội hình sở hữu. Giữ nguyên tất cả ảnh thẻ, chín bộ đầu còn lại, màu da thân đang có và quy tắc áo dài/ngắn tay hiện tại. Thông tin/biểu tượng CLB hiển thị và chữ/số áo của v18 vẫn cần xác nhận trong game; mã đã gọi đúng setter native cho trạng thái không CLB của sáu bản ghi.

## Kiểm tra

680 kiểm tra ARM64 chạy mã hook và các getter/setter native; có kiểm tra glyph gốc xác nhận toàn bộ ký tự của tám tên áo đều có hình vẽ, và cấu hình font/size/path giữ nguyên từng byte. Đã chạy 12 đường cài hook, manifest/checksum/idempotence.

UEViewer đọc lại 10 mesh/20 LOD của bốn bộ; vị trí, UV, tangent, màu đỉnh, index, weight và BoneMap, skeleton/bind pose, ActiveBones, RequiredBones166/153 và toàn bộ vùng LOD giống nguồn từng byte. Texture diffuse xuất lại giống pixel nguồn, toàn bộ dữ liệu mip/bulk giống nguồn. 209 chunk khác, gồm toàn bộ ảnh thẻ và các đầu/tóc giữ lại, không thay đổi.

Sau cài kiểm tra mặt 2017, 2027, Jr, Hoàng Đức, tên/số áo và một replay/cutscene. Log:
`files/embedded-gateway/work/tools/noodle-hair-status.json`

Phiên bản cần thấy: `player-faces-v18-working-template-club-shirts`; `four_face_comparison_mode` phải bằng0. Có thêm `vietnam_club_removed` và `vietnam_club_last_card`. `face_mid_created` bằng0 là bình thường vì v18 dùng material tĩnh. `device_verified` vẫn false cho đến khi có kiểm chứng renderer; số đếm HOOK_ACTIVE/material không chứng minh hình ảnh đúng.
