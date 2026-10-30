# UI7.17 FULL · Sửa tương thích Live Update sau UI7.16

Gói đầy đủ, giữ các tính năng/face UI7.16, không Part3. Chép assets/ và classes5.dex vào gốc APK73V16 versionCode311010108, thay thế rồi ký một lần. Dùng cùng khóa ký để cài cập nhật; không gỡ game/xóa dữ liệu. extras/ là file Blender, không chép vào APK.

## Hotfix

Log mới cho thấy CMD_LOGIN thành công, hooks hoạt động, lỗi xảy ra ở phía client áp tài nguyên. Lỗi checksum UI7.12 và noodle-advertise-error.txt trong log là lịch sử cũ, không được coi là nguyên nhân hiện tại. Chưa có thông báo native xác định chính xác file bị từ chối.

UI7.16 đã chèn40byte marker vào PAK phụ để phân biệt ảnh/gói thay đổi. UI7.17 bỏ cách này: giữ đúng bố cục PAK native version11 gồm144byte index mã hóa và221byte footer (365byte), thay PathHashSeed của index rỗng rồi tính lại SHA1 và mã hóa. Cả hai secondary-index giữ nguyên. PAK vẫn có hash khác theo nội dung, không dùng hash cố định khiến cache giữ ảnh cũ. Đây là hotfix tương thích; đọc UEViewer hoặc SHA đúng không chứng minh Android đã mount thành công.

Trước khi vào engine, chỉ PAK cache trong Download có đúng tên, kích thước405 và hash của5file UI7.16 đã biết mới được thay bằng PAK chuẩn365 sau khi payload được xác minh. Có backup trong embedded-gateway/ui716-pak-backup. Không sửa file không nhận diện, save, Transfer, UCAS hoặc UTOC. Ảnh custom đã lưu được dựng lại theo schema17, giữ crop trongSQLite. Không bỏ kiểm tra integrity.

RuntimeDiagnostics thêm manifest tài nguyên thực sự đã quảng bá và đối chiếu SHA/kích thước file Download, chạy khi bấm Diagnostics trên luồng nền. Thiếu file trong Download chưa đủ chứng minh lỗi (có thể game dùng nguồn khác). Không chạy scan/hash này trong search hoặc trận đấu.

## Kiểm chứng và giới hạn

Kiểm thử host gồm bố cục/indexSHA1, mã hóa AES theo Java platform, file cache đã biết/unknown/backup, gateway và hai lần import ảnh→login, GET/HEAD/range/SHA. Chưa thử Android/GPU: cần vào game sau cập nhật để xác nhận lỗi Live Update đã hết; không tuyên bố100%. Nếu còn lỗi, gửi log RuntimeDiagnostics mới, đặc biệt ui717-client-resource-probe và ui717-live-update-status.json. Giữ giới hạn UI7.16: băng cổ tay/face render cần thử thiết bị; SOUND riêng từng thẻ chưa triển khai.

# 73 V16 UI7.16 · Full một ZIP · Không Part 3

Dành riêng 73 V16 versionCode311010108; không dùng cho efootxi.
Mở thư mục bọc testingdummy-<commit> nếu tải qua GitHub. Chép **assets/** và **classes5.dex** vào gốc APK bằng MT Manager, thay thế, ký một lần. Không áp chồng thêm UI/Part cũ. Cài cập nhật cùng khóa ký để giữ save, không cần gỡ game/xóa dữ liệu. **extras/** chứa file Blender để mở trên máy tính; không chép extras vào APK.

## Thay đổi UI7.16

- Yan Diomande của Real Madrid My League: bản ghi native176104 dùng đầu procedural nên bỏ qua đường thay face cũ. Chuyển đúng chế độ named face và tên NDI2ep00v0313 bằng hàm string engine gốc, trước lúc dựng nhân vật. Áp dụng sáu bản ghi Yan đã xác minh:176104,84062184,105863243280360,105877118037992,52904065150952,56164297650152. Dùng face Diomande đã gửi, không đổi cơ thể/motion. Tài nguyên thật được đọc lại độc lập trong pc9310; diagnostics mới phân biệt số lần cấu hình và callback mesh thực tế.
- Mullet V13 thay V12 **chỉ89138288266704**. Giữ Ronaldo2014 V18 tại106654775417922. Henry105625593957752 dùng gói mới PES_Thierry_Henry_by_Gabri_Facemaker.rar thực tế đã nhận (không phải file tên henry2.zip). Bốn biến thể đầu mỗi face giữ đủ166xương, cả haiLOD, weights và bind pose.
- Viền áo xắn: bỏ vòng viền dịch/chỉnh chu vi dễ biến dạng. Giữ bề mặt áo native đã cắt và trọng số xương nội suy, lấy UV viền áo gốc để giữ màu/trim. Dựng đủ123mẫu;246LOD và các đường nối được kiểm tra. Áo dài nguyên bản vẫn tách riêng.
- Copy Background Style dựng thẻ được chọn trước, chỉ thay layer nền/khung. Không sao chép header, danh tính, ảnh người, huy hiệu hoặc mask của thẻ nguồn. Sửa nhận dạng nhầm tile nền0000_b01_128_ là ảnh cầu thủ; đây cũng là nguyên nhân có thể gây preview lặp ảnh donor.
- Import Photo giữ ưu tiên độc lập với nền. Mỗi generation ảnh đổi cả hashPAK/UTOC/UCAS; phục hồi từ crop trongSQLite khi file/state thiếu hoặc không khớp dữ liệu đã lưu. Giữ HTTP tên phẳng, URLgeneration, HEAD, resume-range và kiểm traSHA; không tắt integrity để né lỗi Live Update. Đã chạy nhập ảnh→đăng nhập gateway được bảo vệ hai lần liên tiếp, khởi động lại trạng thái, GET đủ ba file và đối chiếuSHA trên máy build.
- 11ảnh mini/lớn được căn lại từ ảnh đã gửi, resize đồng tỉ lệ128×128 và184×256: Mullet/R2008,Henry,Joker,R2017,R2014,Zidane,Wukong,Spider-Man,R9,Robben,Raiden. Không vẽ lại mặt. **Một lần nâng cấp**, crop custom cũ của đúng11thẻ này được sao lưu trongSQLite meta ui716_previous_custom_portraits rồi nhường cho ảnh mới theo yêu cầu. Ảnh custom các thẻ khác giữ nguyên; ảnh tự nhập sau nâng cấp vẫn ưu tiên bình thường.
- Tự tách nền mặc định khi chọn ảnh còn nền: U2NetP chạy offline trong WebWorker, một luồngWASM, chỉ tải khi nhập ảnh. Có preview, khôi phục ảnh gốc, hủy. Ảnh đã trong suốt giữ nguyên. Ảnh xử lý tối đa1536px, inference320px; đóng/hủy/xong thì dừng worker, không chạy trong tìm cầu thủ hay trận đấu. Máy build xử lý thử khoảng6,5giây; đây không phải benchmark điện thoại. Tách nền tự động có thể cần chỉnh lại với ảnh khó.
- Transfer chỉ bốn giải UEFA122,WorldNation128,Y08473,Y17518. Giữ thứ tự pool native ổn định và ánh xạ slot đội hình vào pool; đội trưởng/sáu vai trò đá phạt/số áo theo đúngID, không trôi theo người đượcSWAP. Kiểm thử đã dùng hàm consumerARM64 gốc để đọc lại Güler/Valverde, thêm/bỏ dự bị, áp dụng lại, phục hồi ngoài giải được chọn.
- Accessories: chuẩn hóa vector đang rỗng/thiếu/đảo thứ tự về vị trí native type0–17 vì renderer truy cập trực tiếp chỉ số. Giữ màu, găng thủ môn và mục không chỉnh. Giữ tùy chọn màu accessories hiện có. Băng trái/phải có counters để kiểm tra thiết bị.
- extras/Ronaldo2027-89138556572074-MERGED.blend là mesh NQ27 đã ghép đang dùng, **không phải đầu gốc4522**. Bốn biến thể,166xương,UV/weights và texture đóng gói; đã mở lại file và đối chiếu điểm với mesh runtime.

Giữ các thay đổi tích lũy UI7.15 và trước đó ngoài Part3/pc9308: WukongV9,Ghost,Raiden,Joker,Robben,R2017, editor,cart,Transfer, sửa bootstrap/repair, tóc matte chỉ89138556572074… Không nhập Python/SO thử từ ZIPface người dùng; chỉ dùng tài nguyên mesh/material/texture.

## Giới hạn kiểm chứng

Các báo cáo validation/ là kiểm thử trên máy build: gateway/codec, JavaHTTP, giả lậpARM64 bằng hàm engine gốc, đọc tài nguyên bằngUEViewer và browserworker. **Chưa kiểm chứng Android/GPU, replay/cutscene, preview đối thủ và độ mượt trên điện thoại.** Yan đã đổi đúng config native và asset có thật, nhưng callback xác nhận mesh trên thiết bị cần log mới. Băng cổ tay: hai thẻ Suárez88039044974657 và89134261635137 trong tài nguyên gốc đang có không bật cờ4/5; chưa đủ bằng chứng để khẳng định band của họ do cờ nào. Việc vector canonical đúng chưa chứng minh band đã hiển thị. Không tuyên bố các phần này đạt100% khi chưa thử máy.

**SOUND đổi riêng một thẻ vẫn chưa triển khai**; không thêm nút giả hoặc thay cue chung làm ảnh hưởng thẻ khác.

Sau cập nhật đóng hẳn rồi mở lại. Chỉnh ảnh/appearance/Transfer trước EnterGame; nếu giao diện yêu cầu mở lại thì làm trước khi thử. Nếu lỗi, gửi RuntimeDiagnostics sau đúng lần lỗi; bản này thêm ui716-photo-status.json, actual_photo_override và yan_actual_mesh để phân biệt lưu cấu hình với tài nguyên được engine dùng thật.
