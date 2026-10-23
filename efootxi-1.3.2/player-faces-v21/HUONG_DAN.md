# V21 — đường render đầu native, cằm, Diomande, miniface và chữ áo

Cài **một gói**: `Faces-v21-native-heads-cards-kits.zip`. Đây là gói đầy đủ, đã gồm sửa crash Đội hình của v20a; không cần cài v20/v20a tiếp sau nó.

1. **Buộc dừng game** trong Cài đặt Android.
2. Giải nén ZIP. Dùng MT Manager gộp cả `work/` và `livedata/` vào `files/embedded-gateway/`, chép đè các tệp trùng tên.
3. Mở lại game. Log `work/tools/noodle-hair-status.json` phải ghi `version: player-faces-v21-native-head-path`, `state: HOOK_ACTIVE`, `error: null`.

Không xóa save, dữ liệu ứng dụng hoặc toàn bộ thư mục game. Gói không chứa tệp cấu hình đội hình/chỉ số My League cá nhân. `gateway_runtime.py` vẫn đúng 2441 byte.

## Bốn đầu bị đen — thay đổi lần này

Đúng bốn ID đang xử lý:

- Ronaldo 2017: `88044950524330` → NW01.
- Ronaldo 2027: `106734785925546` → NW27.
- Ronaldo Jr: `105765448873424` → NWJR.
- Nguyen Hoang Duc: `105643042189511` → NWHD.

V21 **bỏ ép lại material sau bake và bỏ can thiệp bóng riêng trên bốn đầu này**. Chúng đi qua vòng đời material/bake gốc của engine như đầu 2006 đang hoạt động tốt. Geometry, tóc và texture của bốn đầu giữ nguyên v20. Không đổi Face ID của cầu thủ.

Theo yêu cầu, sao chép đầu 2017 sang **ID thử `105807861630781`**, dùng chính asset `SK_NW01ep00v0313_Face`; không đổi tên, chỉ số hay vị trí của thẻ thử này. Đầu 2017 trên ID cũ vẫn được giữ.

**Chưa xác nhận hết đen trên renderer Android.** Đây là thay đổi đường xử lý có kiểm tra phạm vi và gọi hàm gốc; chưa có bằng chứng kết luận nguyên nhân gốc đã được loại bỏ trên điện thoại. Không coi các bộ đếm `confirmed` hay `HOOK_ACTIVE` là chứng minh hình ảnh đúng.

Sau khi xem đầu 2017 và ID thử, log mới có `standard_head_mesh_callbacks`, `standard_head_bake_calls` và `last_redirected_asset_path`. Đường dẫn phải chứa `NW01`, không phải log v20 cũ với mọi bộ đếm tải đầu bằng 0. Nếu vẫn đen, gửi **log mới của v21** cùng kết quả thẻ gốc/thẻ thử; không cần gửi toàn bộ thư mục game.

## Cằm và Diomande

Özil/Đình Bắc: thống nhất trọng số các đỉnh sát nhau ở đường nối cằm/cổ, chỉnh normal vùng cằm. Không đổi tóc hoặc skeleton của hai đầu; dịch chuyển bind pose tối đa dưới 0,25 mm. Giữ độc lập môi, mắt và 135 đỉnh phụ kiện native. Kiểm tra há hàm/quay đầu tổng hợp khép các đường nối đã sửa; chưa tương đương replay trên máy.

Yan Diomande base trong My League: nguồn từ `Diomande.rar`, giữ geometry/UV mặt gốc, atlas tóc riêng và retarget theo tên xương Android. Phạm vi đúng hai ID base đã tìm được trong catalog: `176104` và `84062184`; không thay các thẻ đặc biệt khác của Diomande. Có xử lý đúng asset đầu generic `SK_Base_Face` khi được gọi trong scope của hai ID base này; không thay mesh thân người. Có mắt và trong miệng native; không hứa chuyển đủ biểu cảm PC.

Skeleton/inverse bind native 166 xương và RequiredBones của LOD0/LOD1 166/153 được giữ; tối đa 4 trọng số/đỉnh, tổng byte 255, BoneMap dưới 75. Các đầu khác giữ nguyên dữ liệu mặt/tóc v20.

## Áo và ảnh thẻ

Giữ tám bộ áo trên bốn đội: Sparta Rotterdam → Real Madrid 2017; Telstar → Manchester United 2007; AZ → Real Madrid 2011; Heerenveen → Barcelona 2017.

Màu tên/số: Real 2017 home xanh cyan, away trắng; MU 2007 cả hai bộ trắng; Real 2011 home vàng đồng, away vàng champagne; Barca 2017 home vàng, away navy đậm. Giữ nguyên hình dạng font, kích thước, layout và **từng block alpha EAC** gốc. Không sửa chuỗi resource thành tên cầu thủ. V21 giữ chi tiết đổ viền RGB của font Sparta, thay vì san phẳng toàn bộ như v20.

**Việc tên áo hiện lại chưa được xác nhận trên máy.** Log có thêm `last_font_name_resource_path` và `font_name_resource_paths` để xác định chính xác atlas engine gọi nếu còn mất chữ. Màu đã được dựng lại ở asset; không tuyên bố đã kiểm tra GPU/bake tên áo Android.

Sáu miniface được bố trí độc lập, cùng cỡ đầu/đường chân vai, nền alpha: Đình Bắc, Özil, Ronaldo 2013, 2008, 2006, 2017. Thẻ đang có ID `106726716084650` vẫn là bản 2008 đã gán trước đây. Không nén ảnh thẻ dọc thành hình vuông. Giữ texture mini native 128×128 và ảnh lớn 184×256.

Bốn ảnh lớn Ronaldo dùng bố cục tham khảo riêng: 2017 xanh sân vận động, 2006/2008 vàng đồng, 2013 vàng/đen. Đây là thiết kế tùy chỉnh dựa ảnh tham khảo, không tuyên bố là background Big Time chính thức. Không in đè rating/tên/khung lên ảnh: game tự vẽ các phần đó.

## Kiểm tra và giới hạn

Đã đọc lại bằng UEViewer: đầu mới, mesh cằm và mười texture ảnh thẻ; kiểm tra package ID, hash, shader/material import và alpha font. Kiểm tra native gồm scope ID/thread, fallback, hàm bake gốc không bị ép material trên bốn đầu, tên áo/UI và glyph native; hồi quy crash thực thi prologue, 15 lần đọc stack argument và lần đọc con trỏ thật của engine với đủ 23 đối số.

Chưa chạy trực tiếp trên điện thoại. Cần kiểm tra Đội hình, mặt bốn thẻ lỗi, thẻ thử, tên/số áo và replay/cutscene sau khi cài. Các render Blender chỉ dùng rà geometry/UV, không chứng minh shader UE4 Android đúng.
