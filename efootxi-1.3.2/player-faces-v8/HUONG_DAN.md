# Faces v8 — sửa vật liệu, nối cổ và thêm ba mặt từ nguồn mới

**Người dùng đã xác nhận v7 hết biến dạng thân trong cutscene. V8 giữ nguyên mã dựng LOD của v7, skeleton/bind và danh sách xương từng LOD; không quay lại cách cắt RequiredBones của v6. V8 chưa được thử trên điện thoại.**

## Các ID trong gói

| Mặt | Full Card ID | Ghi chú |
|---|---|---|
| Ronaldo 2017 mì tôm | 88044950524330 | Sửa shading mặt đen; giữ hình dáng |
| Ronaldo 2006 | 89135066911146 | Nối mép cổ; tóc; tay dài |
| Ronaldo 2013 | 106781745353130 | Nối mép cổ; tóc; **tay dài** |
| Ronaldo 2027 | 106734785925546 | Sửa shading mặt đen; tóc; **tay ngắn** |
| Ronaldo Junior | 105765448873424 | Nguồn Ronaldo Junior.rar |
| Nguyễn Xuân Son | 88045755960841 | Thay mặt Adriano trên đúng thẻ; nguồn Nguyen Xuan Son.rar |
| Nguyễn Đình Bắc | 88038776539586 | Thay mặt Pato trên đúng thẻ; nguồn Nguyen Dinh Bac.rar |

**Chưa có mặt Nguyễn Hoàng Đức cho 105850542916637.** Đã tìm trong repo, các tệp cũ và ba RAR mới nhưng không có nguồn tương ứng. ID này được giữ nguyên; không dùng nhầm mặt khác để lấp chỗ. Cần đúng tệp nguồn Hoàng Đức hoặc đường dẫn tải để làm tiếp. Gói này không đổi tên/thông số/DB cầu thủ hoặc Face ID; các ghi chú Adriano/Pato chỉ xác định thẻ cần thay mặt.

## Cài bằng MT Manager

1. **Buộc dừng game.**
2. Giải nén **Faces-v8-7-cards.zip**.
3. Gộp **work/** và **livedata/** vào **files/embedded-gateway/**, cho phép ghi đè **11 tệp**. Không chép thành `work/work/` hoặc `livedata/livedata/`.
4. Mở lại game và để hoàn tất cập nhật dữ liệu.

Không xóa save/dữ liệu ứng dụng. Gói dựa trên hotfix v18 người dùng đã cài; không yêu cầu root hay sửa APK. Với repo riêng tư, đăng nhập GitHub có quyền truy cập trước khi tải ZIP.

## Sửa gì

- **Mặt đen 2017/2027:** dùng normal trung tính hợp lệ trên vùng da của hai đầu này, thay vì để quy ước normal PC lọt vào đường shading. Nguồn 2027 thực tế có hai kênh XY, kênh B=0; không thể dùng nguyên như XYZ Android. SRO da của hai đầu được lấy màu phản hồi từ vùng da native theo **UV native**, không áp hoa văn UV native lên UV PC. Không coi đây là bằng chứng đã tìm hết nguyên nhân mặt đen 2017 trong renderer.
- **Khe cổ 2006/2013:** phát hiện các đỉnh trùng vị trí nhưng khác weights. V8 đồng bộ vị trí/weights tại các mép nối cần kín, làm mượt normal và sửa tangent frame. Không hàn dính các điểm tiếp xúc môi trên/môi dưới cần tách khi mở miệng.
- **Tangent/shading:** kiểm tra hai vector tangent và normal có độ dài hợp lệ và vuông góc. Nguồn Đình Bắc có nhiều tangent gần song song normal; dựng lại từ geometry/UV cho mặt và tóc, tránh đưa basis không hợp lệ vào shader Android. Các đầu khác được trực chuẩn hóa basis, không đổi hình dáng.
- **Tóc 2006/2013/2027:** giữ 2048×512 thật của nguồn, tăng chi tiết RGB bằng lọc có xét alpha để hạn chế viền sáng từ vùng trong suốt. Dùng HQ như v7; không quảng cáo tạo thêm sợi thật bằng phóng ảnh.
- **Mắt/miệng mới:** chọn geometry da/tóc theo material thực tế của từng FMDL. Nguồn Xuân Son/Đình Bắc có mặt chia ba mesh, khác bộ Ronaldo. Giữ native eyes/teeth/cavity, điều chỉnh vị trí/kích thước theo mí/môi nguồn; giữ jaw, eye, eyelid controls. Xuân Son giữ phụ kiện/băng trán theo nguồn, texture tóc/phụ kiện đóng atlas riêng; hair-transfer dùng thêm màu từ nguồn thứ hai. Đây là chuyển vật liệu sang shader native, không sao chép toàn bộ shader FOX.
- **Áo:** 2013 dài tay; giữ 2006, 2017 và Messi 17592722922839 dài tay; 2027 ngắn tay. Quy tắc exact64 trong library v18, không phụ thuộc editor Python đã khởi tạo. Không thay JSON cấu hình người dùng.
- **Hook:** bốn Ronaldo giữ cách nhận đường dẫn profile của v7, kể cả khi engine định dạng ep/lg từ đối số Face ID gốc. Ba ID mới có thể nhận profile RealFace khác Ronaldo nhưng chỉ trong scope đúng actor/thread/Card ID; đường dẫn private chọn một head canonical. Không thay nhận diện cầu thủ toàn cục.

## Kiểm tra và giới hạn

Các báo cáo nằm cạnh gói trên GitHub:

- **188** ca hook đầu ARM64 Unicorn: exact64, namespace, FSoftObjectPath ABI, actor/thread, fallback, profile đã định dạng khác đối số ngoài; thân engine tại các biên hook được mô hình hóa.
- **1.008** ca chạy mã chọn áo UE ARM64 đến ngay trước LoadUniShirt. Kit availability/resources/callback dùng mô hình/sentinel; không phải render áo trên máy.
- UEViewer đọc **19 mesh / 38 LOD**, material và texture của bảy đầu gần. Skeleton/bind nguyên byte, RequiredBones nguyên thứ tự native, writer LOD có SHA giống v7. Draw BoneMap ≤75, tổng weight byte=255.
- Kiểm tra jaw/eyes/eyelids, basis shading và mép nối. `seam-validation.json` tái hiện khe ở v7 trong hai **pose cổ tổng hợp**; các nhóm nối đã sửa có sai lệch vị trí bằng 0 trong phép thử v8. Không gọi con số này là đo từ replay điện thoại.
- Đối chiếu texture bằng hai decoder; normal 2006/2013 giữ đúng dữ liệu của v7, ảnh tóc/alpha giữ kích thước nguồn. ZIP CRC, checksum native/container và manifest/idempotence/disable/corrupt-file paths được kiểm tra.

**Không thể bảo đảm “không còn lỗi gì” trước khi chạy renderer trên điện thoại.** V7 đã được bạn xác nhận về cutscene; v8 còn cần kiểm tra mặt đen, vết nối, blink/jaw/eyes, bảy thẻ đúng ID và áo 2013/2027 trong game. Ảnh CPU diagnostic chỉ hỗ trợ kiểm tra geometry/texture, không chứng minh shader Android đã đúng. LOD xa giữ cơ chế native, không có đầy đủ biểu cảm như LOD gần; không hứa mọi biểu cảm PC.

Nguồn Xuân Son/Đình Bắc có một số texture 1254×1254 với payload nén không đủ block ở hàng cuối. Bộ dựng chỉ bổ sung hàng biên thiếu bằng block hoàn chỉnh cuối cùng, ghi rõ trong `new-input-analysis.json`, rồi chuyển về texture mobile. Một số FTEX không được converter hỗ trợ dùng DDS có sẵn trong chính RAR. Không yêu cầu lấy lại thư mục game từ điện thoại.

## Tắt hoặc quay lại

Nếu cần ngừng thay đầu: buộc dừng game, giải nén **Tat-thay-dau-v8.zip**, gộp `work/` vào `files/embedded-gateway/`. Gói này tắt cả bảy đầu tùy chỉnh; không xóa save và vẫn giữ các quy tắc áo của v18/v8.

Muốn quay lại đủ v7: chép lại [gói v7](../ronaldo-four-v7/Ronaldo-v7-4-faces-native-lod.zip) theo hướng dẫn v7, ghi đè cả work/ và livedata/. V7 vẫn có mặt đen/vết nối người dùng đã báo. Không quay về v6.

Log nếu cần đối chiếu cài đặt:

- `work/tools/noodle-hair-status.json`: version `player-faces-v8-material-seams`, HOOK_ACTIVE, payload_verified=true.
- `work/tools/select-team-status.json`: version `native-hotfix-v18-faces-v8-sleeves`; appearance_hooks.shirt phải INSTALLED.
