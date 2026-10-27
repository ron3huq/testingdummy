# eFootball73 V16 · UI7.10 FULL

Bản áp tích lũy dành cho **73 V16**, gồm Main mới và Part1 Faces giữ nguyên. Không áp cho efootxi. APK73 V16 và bộ Resource73 gốc vẫn cần có riêng; đây là bản áp vào APK, không phải APK đã ký.

- [Part2 Main UI7.10 FULL](V25-73-UI7.10-FULL-Part2-Main-MT.zip)
- [Part1 Faces FULL — giữ nguyên](../73-v16-ui7/V25-73-UI7-FULL-Part1-Faces-MT.zip)
- [Ảnh thẻ mới](previews/cards-preview.jpg) · [SHA256](SHA256SUMS.txt)

## Cách áp

1. Nếu có save cần giữ, xuất bằng Save Manager trước.
2. Trong MT Manager, chép **nội dung cả Part1 và Part2 vào cùng APK73 V16**, thay thế file trùng. Không chép nguyên ZIP vào APK. Nếu đã áp đúng Part1 thì chỉ cập nhật Part2. Không chồng Main cũ lên Main7.10.
3. Ký bằng đúng khóa đã dùng để cài bản hiện tại, rồi cài đè. **Không cần gỡ game/xóa dữ liệu.** Với APK sạch vẫn cần đủ Resource73 gốc.
4. Kiểm tra dòng **UI7.10 Earth**. Chỉnh Appearance & Motion trước Enter Game; sau khi lưu, đóng hẳn và mở lại ứng dụng để nạp native profile mới.

## Thay đổi mới

- **Spider-Man105647605587130:** sửa dữ liệu mesh/skeleton theo hướng dẫn người dùng. Giữ đủ166 xương native73, đúng tên/thứ tự/parent và reference transforms; engine suy ra inverse bind matrices từ reference pose. Giữ BoneMap/skin weights; không scale tay/chân hoặc sửa PlayerModel để che lỗi. Bản trial có LOD0 cooked-out; bản mới có dữ liệu render thật ở cả LOD0/LOD1, ActiveBoneIndices và RequiredBones đều0..165. Áp dụng đủ bốn biến thể, không chỉ bản chính. [Kiểm tra sâu](skeleton-deep-validation.json), [đọc độc lập12mesh](independent-mesh-validation.json). **Chưa chạy replay/ăn mừng trên Android nên cần xác minh thực tế trước khi kết luận hết lỗi cutscene.**
- **Naruto105804908868664**, **Orc105873896755947:** nhập đúng face từ ORC-NARUTO-V2-GAME.zip; chuyển sang namespace riêng NNAR/NORC, containerpc9307, không chồng pc9298 cũ. Cùng chuẩn native166 và hai LOD như trên. Đổi tên trong game/editor, cập nhật ảnh lớn/miniface. Không đổi các thẻ mang ID trial cũ hoặc những thẻ khác cùng cầu thủ gốc.
- **Bỏ custom RGB da**: chỉ giữ Original + sáu palette gốc có mẫu màu. Cấu hình RGB cũ được bỏ khỏi profile sau khi sao lưu SQLite nguyên trạng trong backups/ui710-before-remove-rgb.sqlite3. Không quảng bá container RGBpc9304, không cài hook RGB. Màu texture face gốc của nhân vật vẫn giữ theo file nguồn, không tô lại mặt.
- **Sleeves:** Original / Short / Long theo full cardID, ưu tiên lựa chọn của người dùng hơn mặc định Ronaldo ở mọi giải. Không dùng kiểu xắn tay lỗi cũ. Không chọn thì giữ quy tắc áo trước đây.
- **Accessories:** sáu loại đã xác định từ native registry: quần bó ngắn, quần bó dài, băng cổ tay trái/phải, băng cổ chân, găng tay cầu thủ sân. Mỗi loại Original/Off/On; hai loại quần bó không bật đồng thời. Không đưa găng thủ môn hay loại chưa xác định vào danh sách. Băng trắng Ronaldo cũ được giữ làm mặc định; lựa chọn riêng có thể bật/tắt theo thẻ.
- **Card Background:** bảy nền theo donorID88039313485858,88045755960770,89138019805599,89138288266704,89133456301399,89133724764840,88037702764935. Đổi style qua native TextureInfo; giữ ảnh của thẻ đích. Hero dùng thêm ảnh foreground trong suốt để nền mới không bị ảnh thiết kế cũ che kín. Default phục hồi nền mặc định của bản mod này.
- UI chỉ tải lựa chọn khi mở, lưu ở luồng nền; không thêm SQL/xử lý ảnh vào tìm kiếm hoặc từng khung hình. Mã search/index giữ nguyên từng byte. Native profile đọc trong bộ nhớ, có giới hạn1024 thẻ. Không hứa độ trễ thực tế trên mọi máy khi chưa đo Android.

## Ảnh thẻ và phần chưa hoàn thành

**Công cụ tạo ảnh AI từ chối yêu cầu, không tạo ra ảnh.** Ảnh thay thế hiện được render offline từ đúng mô hình3D người dùng gửi rồi ghép nền thiết kế riêng; không gọi chúng là ảnh AI. Xem [nguồn ảnh](hero-art-provenance.json), [kích thước và căn khung](card-art-layouts.json). Ảnh lớn184×256, miniface128×128, scale đồng đều không nén mặt. Spider-Man được thiết kế lại cùng đợt.

**Chưa trích được đầu modder thực sự của89136418985302.** Không gửi đầu4522 gốc giả làm đầu yêu cầu. Các biến thể mesh4522 trong pc3700 modder đã kiểm tra giống bản gốc; PlayerAppearance của full cardID có payload giống4522, nhưng điều đó không chứng minh đường dẫn đầu sau runtime binding. Bản này thêm bộ ghi đường dẫn thụ động cho đúng thẻ, không thay face của thẻ đó. Để lấy bằng chứng tiếp: mở3D/cảnh trận có89136418985302, rồi Runtime Diagnostics → Copy; trường noodle-hair-status.json → ronaldo_89136418985302_original_head có path/calls/redirected:false. Đường dẫn đó cho phép trích đúng asset thay vì đoán.

## Tích lũy các bản trước

Giữ kits và luật licensing Real Y08/Y17; đội hình/phân cấp My League, chỉ giới hạn chỉ số đội AI; HLV gốc phục hồi; face alias Ronaldo2027/2017; áo ngắn riêng89138556572074 và áo dài các Ronaldo đã yêu cầu (trừ khi người dùng tự đổi ở mục mới); giỏ Catalogue, nhiều thẻ cùng cầu thủ, search không dấu, PlayerModel,64 tên innate skills + Additional, chọn Main/Memorial celebration, Earth UI, sửa tải tài nguyên và đăng nhập, Level100. Physics vẫn bỏ; chiều cao140–220cm/cân nặng40–130kg. Mã các tính năng không liên quan được đối chiếu giữ nguyên từ7.9.

[Danh sách ăn mừng HTML](celebration-ids.html) · [CSV](celebration-ids.csv):318 nhóm/1544 dòng, tối đa6 thẻ/tên mỗi nhóm khi dữ liệu có đủ; giữ kết quả đã đối chiếu, không tự gán542/571/595 thành parameter ID khi thiếu bằng chứng.

## Xác minh

[Package](package-validation.json): ZIP CRC, hai manifest, SHA native/tài nguyên,267 lớp DEX gốc giữ đủ/362 lớp sau bổ sung, không save cá nhân, hai ZIP không trùng đường dẫn. [Login](login-validation.json): gateway73 thật initialize và CMD_LOGIN trả NOERR, URL lặp idempotent, CPK gốc tách CPK mod; bước Android được mô phỏng. [Native face](face-native-validation.json), [background](background-native-validation.json), [gear](gear-native-mode2-validation.json): chạy ARM64 qua Unicorn, kiểm tra đúng fullID và phạm vi; renderer/allocator được mô phỏng khi cần. [Giữ roster/kits/OVR](retained-native-validation.json): chạy kiểm tra hồi quy ARM64 các luật cũ. [Phụ thuộc](dependency-validation.json): không thiếu dependency hoặc trùng packageID mới với gói face cũ. [Bỏ RGB](rgb-removal-validation.json): backup/migrate/giữ palette và celebration.

Không có kiểm thử trực tiếp trên điện thoại; không tuyên bố mọi thay đổi đã hoạt động100% trên Android.
