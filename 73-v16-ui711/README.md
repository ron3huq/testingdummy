# 73 V16 · UI7.11 FULL

Bản áp tích lũy cho **73 V16 / com.efootball.revival.local**, giữ toàn bộ phần UI7.10. Không dùng cho efootxi. Đây là bộ file chép vào APK; vẫn cần APK và Resource73 gốc, không phải APK đã ký hay bộ resource gốc đầy đủ.

- [Part1 — Faces cũ, giữ nguyên](../73-v16-ui7/V25-73-UI7-FULL-Part1-Faces-MT.zip)
- [Part2 — Main UI7.11 FULL](V25-73-UI7.11-FULL-Part2-Main-MT.zip)
- [Part3 — Năm face Ronaldo mới](V25-73-UI7.11-FULL-Part3-Ronaldo-Faces-MT.zip)
- [Xem ảnh thẻ](previews/portrait-preview.jpg) · [SHA256](SHA256SUMS.txt)

## Cách áp

1. Xuất save qua Save Manager nếu cần sao lưu.
2. MT Manager: chép **nội dung cả ba ZIP vào cùng APK73 V16**, thay file trùng. Không chép nguyên ZIP vào APK. Nếu APK đã có đúng Part1 từ trước thì giữ Part1, cập nhật Part2 và thêm Part3. **Part3 là bắt buộc với Main7.11**, vì Main kiểm tra tài nguyên năm face mới.
3. Ký bằng đúng khóa đang dùng rồi **cài đè**. Không cần gỡ game hoặc xóa dữ liệu. Không áp Main cũ sau Main7.11. APK sạch vẫn cần Resource73 gốc.
4. Kiểm tra dòng **UI7.11 Earth**. Chỉnh các profile trước Enter Game; sau khi lưu hãy đóng hẳn và mở lại ứng dụng. Native profile được nạp một lần khi khởi động, không sửa bộ nhớ đang chạy giữa trận.

## Năm face và ảnh thẻ mới

Người dùng xác nhận ghép theo **ID trong tên file**; không dùng ID trial ghi bên trong archive. Không nạp thư viện hoặc mã trial đính kèm; chỉ lấy tài nguyên mesh/material/texture.

| Card ID | Face riêng | Club | Quốc gia |
|---|---|---|---|
| 105837926394281 | NCA1 | Real Madrid | Portugal |
| 88040387132864 | NCA2 | Real Madrid | Portugal |
| 106654775417922 | NCA3 | Real Madrid | Portugal |
| 105758469512061 | NCA4 | Manchester United | Portugal |
| 105563585358239 | NCA5 | Real Madrid | Portugal |

Cả năm tên **C.Ronaldo**, tên áo **Ronaldo** (native in hoa RONALDO theo kiểu chữ áo game). Đổi club/flag ở record và dữ liệu card lớn/icon; không đổi đội hình đang sở hữu của người chơi. Giữ ID thẻ và face riêng. Thân hình11 thông số, chiều cao/cân nặng, chân thuận, 21 trường body/motion/AI native lấy từ **89138556572074**. Không sao chép chỉ số kỹ năng thi đấu hoặc vị trí của source sang thẻ đích.

Ảnh lớn184×256 và miniface128×128 dùng ảnh gốc Image.rar tương ứng, nền mặc định Maldini88045755960770 như ba Ronaldo trước; tùy chọn đổi nền của người dùng vẫn ưu tiên. Đã sửa ảnh **88044950524330**: đầu lớn hơn trong miniface, ảnh lớn ưu tiên đầu/thân trên. Scale hai trục bằng nhau, không kéo nén mặt. Ảnh gốc giữ khuôn mặt, không tạo lại bằng AI; cúp trong ảnh được giữ. Có giải mã lại texture ETC2 để kiểm tra kích thước, alpha và sai số màu.

Tài nguyên mới ở **pc9308**, không chồng các gói face/hero cũ. Cả20 biến thể có166 xương native73, đúng thứ tự/parent; giữ bind/reference transforms nguồn đã đối chiếu, BoneMap và skin weights. LOD0/1 đều có render stream thật, Active/Required đầy đủ. Không scale tay/chân để che lỗi.

## Editor mới

- **Appearance & Motion → Copy Body & Motion**: chọn tên Dembélé, Ronaldinho, Cristiano Ronaldo, Vieira, Haaland, Messi, Lukaku. Sao chép11 thông số PlayerModel và chiều cao/cân nặng/chân thuận; native đọc chính record source để lấy kiểu chạy, tư thế/tay rê bóng, dáng đá phạt/penalty/corner, main/memorial celebration và bảy cờ AI playing style. Không lấy các motion mặc định0 từ dữ liệu web làm preset. Giữ face/ID/abilities/positions của đích. Lệnh copy thay các body edits cũ của thẻ đó; sau đó vẫn có thể chỉnh riêng.
- **Name · Shirt Name · Age**: tên cầu thủ UTF-8 (tối đa60 byte), tên áo và tuổi15–63, theo đúng full cardID. Native record names và UI string được sửa; riêng tên áo chuẩn hóa chữ hoa theo font áo. Không tạo cầu thủ giả hoặc đổi playerID để đổi tên.
- **Sleeves · Undershirt · Socks**: áo ngắn, áo dài nguyên bản, áo lót cổ thường hoặc cổ cao; tất Normal/Long/Short. Có Original để giữ/phục hồi lựa chọn gốc. Người dùng chọn riêng được ưu tiên hơn mặc định Ronaldo cũ ở mọi giải.
- **Accessories**: tám loại có cờ native đã xác định: short tights, long tights, băng cổ tay trái/phải, băng cổ chân, găng cầu thủ sân, áo lót cổ thường/cổ cao. Original/Off/On; không bật đồng thời hai kiểu quần bó hoặc hai cổ áo. Loại2/3 chưa rõ không đưa lên UI. Không đưa găng thủ môn vào danh sách. Native flags và đường socks tới material đã được kiểm tra; hiển thị từng mẫu áo lót/accessory trong Android vẫn chưa thử trực tiếp.
- **Card Background**: bảy nền hiện tên donor thay vì chỉ ID. Thêm **Club & Nationality**,441 club và214 quốc gia từ dữ liệu native; đổi logo/flag trên card, không chuyển squad đang chơi. Portugal dùng native Country228/flag49/national team6, không nhầm mã ISO.
- **Positions & Playing Style → Preferred Foot · Weak Foot · Injury Resistance**: Right/Left; Weak Foot Usage, Weak Foot Accuracy, Injury Resistance nhận đúng giá trị raw native0–3. Các giá trị này đã roundtrip bằng getter/setter thật của engine.

UI chỉ tải dữ liệu khi mở mục, xử lý lưu ở worker thread, chống bấm lặp lúc đang tải/lưu. Profile native bất biến trong RAM; không thêm SQL, xử lý ảnh hoặc đọc file vào từng khung hình. Mã tìm kiếm/index/filter giữ nguyên từng byte; chỉ vô hiệu cache tên khi người dùng thực sự đổi tên. Chưa đo độ trễ trên điện thoại nên không cam kết tuyệt đối không lag trên mọi máy.

## Tích lũy

Giữ toàn bộ UI7.10: kitsY08/Y17/Real và luật licensing, các giải/đội hình/phân cấp AI, đội người chơi không bị áp trần AI, HLV gốc, face alias Ronaldo2027/2017, áo ngắn89138556572074/áo dài các Ronaldo khác trừ lựa chọn riêng, giỏ Catalogue, nhiều thẻ cùng cầu thủ, search không dấu, PlayerModel thực tế,64 tên innate skill/Additional skills, Main/Memorial celebrations, Earth UI, sửa tải resource/đăng nhập, Level100. Giữ Hulk/Spider/Naruto/Orc và sửa skeleton166/both LOD trước đó. Không có Physics hoặc custom RGB; sáu palette da gốc; height140–220cm, weight40–130kg.

[Danh sách ăn mừng HTML](celebration-ids.html) · [CSV](celebration-ids.csv) giữ318 nhóm/1544 dòng, tới6 thẻ có tên khi dữ liệu đủ. Không đoán các tên hoặc biến542/571/595 thành parameter IDs khi chưa có bằng chứng.

## Đã kiểm chứng và giới hạn

- [Đóng gói](package-validation.json): ba phần không trùng đường dẫn, manifest cài mới/repair khớp, SHA native/tài nguyên đúng,371 lớp DEX và267 lớp gốc giữ đủ, không chứa save cá nhân.
- [Login](login-validation.json): gateway73 thật initialize/CMD_LOGIN trả NOERR; privatepc9308 được quảng bá và xác thực; CPK gốc tách CPK mod; bước Android được mô phỏng.
- [Native copy](copy-native-validation.json), [lưu profile](profile-storage-validation.json), [native identity](identity-native-validation.json), [quần áo](clothing-native-validation.json), [lưu equipment](equipment-validation.json), [xương/LOD](skeleton-deep-validation.json), [UEViewer độc lập](independent-mesh-validation.json), [phụ thuộc](dependency-validation.json), [ảnh ETC2](art-decode-validation.json), [kits/rosters](retained-native-validation.json), [PlayerModel→bone consumer](bone-consumer-validation.json).

**Không có thử nghiệm trực tiếp trên Android/GPU/cutscene trong đợt này.** Native tests chạy ARM64 qua Unicorn với DB/allocator/renderer boundary được mô phỏng khi cần. Chưa thể xác nhận100% mọi signature animation gắn riêng với playerID đã được copy:21 trường motion/AI và11 body fields đã xác minh; không giả ID để ép những animation chưa biết.

Yêu cầu cũ trích chính đầu modder của89136418985302 vẫn chưa hoàn thành: không thay bằng đầu4522 gốc. Bộ ghi đường dẫn thụ động từ7.10 được giữ để lấy asset thực khi card được mở3D/trong trận; bản này không sửa face của ID đó.
