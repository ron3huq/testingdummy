# Phạm vi kỹ thuật và bằng chứng của bản thử v1

Không còn là chỉ FBX/Blender: bộ này có bảy package Unreal cooked được dựng từ template Android, một bulk texture ETC2 và container IoStore mới pc9298. Chưa chạy engine trên thiết bị; không gọi là đã xác nhận hoạt động trong efootxi.

## Asset

Giữ hệ xương 166 bone, metadata kiểu PesFaceAssetDataMobile và LOD layout gốc. LOD0 cooked_out được giữ; thay section tóc của LOD inline. Mỗi đầu có743 đỉnh mặt gốc và5005 đỉnh tóc, tổng5748 đỉnh/6401 tam giác. BoneMap tóc [7] ứng với sk_head, mỗi đỉnh tóc trọng số255/255. Các buffer mặt positions/indices/tangents/UV/weights/colors được chép nguyên byte; bộ đọc độc lập xuất lại các thuộc tính mặt và inverse bind matrices khớp nguồn.

Bốn asset có tên riêng SK_ND01[_suffix]_Face, giữ suffix lg00v0000 / ep01v0291 / ep00v0313. Face material gốc theo từng biến thể được giữ. Hai material tóc riêng dùng template MQ của Android, masked/two-sided và BaseColorMap. Texture riêng T_ND0001_Hair_D dùng PF_ETC2_RGBA, 256x256,9 mip, hai mip đầu ở bulk, các mip sau inline theo template. ETC2 được giải mã kiểm tra alpha so với PNG: MAE0.6707/255. Đây là bản màu tối một lớp; chưa mô phỏng shader FOX hai UV/lớp màu.

Rebuild buffer size, số tam giác/đỉnh section, bounds, cooked export size. Cập nhật batch tên/hashes, tên object export, global import index, package ID, graph và container-store dependencies. Name hash là CityHash64 của tên ASCII lowercase; package ID dùng lowercase UTF16LE; global object index dùng đường dẫn package/object lowercase UTF16LE và type bits. Có kiểm tra các công thức với asset gốc trước khi dùng. Giữ virtual cooked serial offsets; dịch các offset bảng trong header theo thay đổi kích thước name batch. Không đổi đuôi FBX thành uasset.

## Runtime

Thư viện nhỏ độc lập libnoodle_hair.so, không thay libselect_team.so. Chỉ hỗ trợ SHA256 libUE4.so `3da06a36fb5c434a75c5739af65f16664347477bd653659eb354376410d52f98` và hai prologue đã kiểm tra.

Hook LoadRealFace 0x39cdb10, đọc full64 ID actor+0x10b0; chỉ88044950524330 và FaceId bắt đầu4522 mới đổi prefix sang ND01, giữ suffix. Không sửa FString caller hoặc bản ghi PlayerAppearance. Callback0x39d3e1c có closure[0]=actor, result[0]=object. Khi có request đang chờ và kết quả null, luôn gọi callback gốc để xử lý ownership/cleanup rồi gọi trực tiếp trampoline LoadRealFace gốc với tên cũ, tránh vòng chuyển hướng lại. Null result cũ được engine xử lý qua nhánh null sẵn có; nhánh này đã đọc disassembly nhưng chưa thử trên điện thoại.

Không gọi engine từ Python worker. Worker chỉ cài hook, ghi flag/bộ đếm của thư viện riêng. Trampoline gần dùng mmap không MAP_FIXED, kiểm tra B range ±128MiB; trang RW chuyển RX; entry chỉ sửa một lệnh4 byte atomic. Giữ nguyên code/data của bộ v18 ngoài entry cần cho tóc. Sau khi cài hook không giải phóng trang code đang dùng.

## Gateway

Thêm ba file mới vào CMD_LOGIN_LIVEDATA-shaped object qua wrapper gateway, cập nhật dt880 hashes/kích thước và version+19 theo base response. Không sửa response nguồn hoặc các dt880 entry cũ. Idempotent khi gọi lại trên response đã chỉnh. Checksum sai thì trả response cũ. Các file đặt tại embedded-gateway/livedata; mã DEX server Android đã đọc xác nhận GET /livedata/ nhận file dưới thư mục đó theo canonical path, không dùng danh sách tên pc9257 cố định.

Tắt visual bằng enabled=false vẫn giữ manifest riêng ổn định; Native hook chuyển tiếp yêu cầu gốc. Gateway startup không nạp được bộ tóc không được phép chặn startup phần khác.

## Đã kiểm tra

- UEViewer độc lập mở container, cả4 SkeletalMesh mới, hai MaterialInstanceConstant và Texture2D mới; texture/bulk/package imports nội bộ resolve. Các import game gốc không có trên host vẫn được giữ và còn phụ thuộc dữ liệu có trên điện thoại.
- Bảy package có ID/tên riêng, không override package gốc. Chép/read-back IoStore ra đúng bytes.
- So sánh output decoder: mặt, indices và bind pose khớp nguồn cho cả4 biến thể, tóc đúng5005 đỉnh/5179 tam giác/bone7.
- Unicorn thực thi thư viện ARM64 và entry detours với lệnh đầu gốc. Kiểm tra target, bốn biến thể, các thẻ khác/alias64-bit, disabled, kết quả async null, cleanup trước restore và không lặp fallback. Thân loader/callback engine sau lệnh đầu được mô hình hóa; renderer, async I/O, GC và thread thực của Android không được mô phỏng.
- Gateway: response không bị mutate, giữ entry cũ, append3 file đúng hash/size/URL, rewrite lặp không nhân đôi/tăng version tiếp, checksum hỏng trả response cũ, tắt visual giữ manifest ổn định.

## Còn phải kiểm tra trên thiết bị

Client thật nhận/mount pc9298; asset load không gặp phần serializer tùy biến ngoài những gì UEViewer đọc; shader hiển thị alpha/màu và lighting đúng; xương hoạt động qua hoạt ảnh; bản fallback đúng khi I/O/GC thực; full Card ID tại actor và suffix như dự đoán; camera/LOD/giao cắt tóc; các thẻ khác vẫn giữ mặt cũ. Không có tuyên bố đã qua các kiểm tra này.
