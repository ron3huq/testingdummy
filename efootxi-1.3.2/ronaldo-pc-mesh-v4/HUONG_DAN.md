> V4 đã được báo mất tóc: đọc sai đối số FSoftObjectPath. Dùng [v4a](../ronaldo-pc-mesh-v4a/HUONG_DAN.md) thay thế.

# Ronaldo v4 — mesh mặt PC đầy đủ và giới hạn thay thế ở đường dẫn asset

Chỉ Card ID **88044950524330**. Bản thử cho efootxi Android 1.3.2, MT Manager, không cần root. **Chưa được thử trên điện thoại; chưa xác nhận hết lỗi tay/giày trong replay.**

## Kết quả báo từ điện thoại

Người dùng thấy má/cằm v3 còn đầy, và tay hoặc giày bị kéo dài trong cutscene/replay, hết cutscene thì bình thường. Người dùng xác nhận **chỉ Ronaldo** gặp lỗi. Ảnh cho thấy biến dạng. Video tải lên lớn hơn giới hạn chuyển 32 MiB nên chưa đọc được bằng công cụ; không tuyên bố đã xem video hoặc đã xác định duy nhất nguyên nhân GPU/animation của lỗi.

## Cài

1. **Buộc dừng** efootxi trước khi ghi đè; không chỉ chuyển ứng dụng xuống nền.
2. Giải nén `Ronaldo-PC-mesh-v4-cutscene-trial-88044950524330.zip`.
3. Gộp **cả `work/` và `livedata/`** vào **`files/embedded-gateway/`**, đồng ý ghi đè đủ tám tệp, bao gồm `libnoodle_hair.so` mới. Không chép CPK PC thẳng vào APK mobile.
4. Mở game và tải Latest Data nếu được hỏi. Vào sân bằng đúng thẻ 88044950524330; thử lại cả replay bàn thắng, bỏ lỡ và ăn mừng.

Không xóa dữ liệu ứng dụng, không sửa save, đội hình hoặc dt200/dt870. Gateway vẫn 2441 byte; v4 tăng revision gói thử để game nhận container mới.

## Mặt lần này lấy từ đâu

V1/v1b dùng mặt Android gốc 743 đỉnh. V2 sculpt nhẹ mặt đó. V3 chuyển bề mặt/màu PC lên cùng topology Android. **V4 dùng trực tiếp hình học da mặt/cổ/da đầu từ FMDL PC trong 4522.cpk**:

- face_high mesh 0: cổ, 237 đỉnh / 370 tam giác.
- face_high mesh 2: da mặt đầy đủ, 1788 đỉnh / 3478 tam giác.
- hair_high mesh 1: phần da đầu, 341 đỉnh / 572 tam giác.
- Tổng skin: **2366 đỉnh / 4420 tam giác**. Tóc giữ 5005 đỉnh / 5179 tam giác và atlas màu v2.

Vị trí và UV0 skin đối chiếu với nguồn PC; **không dùng 743 đỉnh mặt có sẵn và không nắn hình học đó để giả mặt PC**. Diffuse mặt dùng ảnh gốc PC 1024×1024, không dùng ảnh preview 512. CPK người dùng gửi và nguồn FPK ban đầu trùng byte về mô hình/texture; cùng nguồn được sử dụng.

Mã `4522...` vẫn xuất hiện trong log vì đó là **mã nhận diện/điều khiển gốc của Ronaldo**, không phải bằng chứng hình học mặt Android đang được dùng. Đường dẫn mesh/texture riêng mới dùng ND01. Gói giữ **khung xương, bind pose và shader/nhãn cầu/răng có sẵn của Android** để tương thích engine; không chuyển nguyên hệ thống FOX PC.

## Rig và biểu cảm

Bản gốc LOD đang có geometry bỏ 13 xương mặt khỏi RequiredBones, gồm jaw, eyelids và eyes. V4 đặt RequiredBones của cả hai LOD và ActiveBoneIndices thành đủ **166 xương native**, giữ nguyên toàn bộ inverse bind matrices, kể cả xương tay/chân. BoneMap mỗi draw chỉ có **11 xương**, không đưa 166 ma trận vào một draw mobile.

Trọng số PC được gán sang xương native có tên xác định: giữ head/jaw và bốn eyelid; cổ/clavicle có bảng alias rõ ràng. Môi dưới/cằm đi theo jaw, môi trên/mũi theo head; một số điều khiển má/môi trung gian được giản lược theo bảng trong source/report. Không đoán các xương native có tên số. Vì vậy **đây là retarget biểu cảm cơ bản**, không phải chuyển đầy đủ các control/clip biểu cảm PC. Cần thử mắt, miệng, răng và vị trí đồng tử trong game.

Đã thực thi phương trình skinning offline: 810 đỉnh chịu ảnh hưởng jaw; bốn nhóm mí mắt có trọng số thực. Điều đó chứng minh mesh có thể biến dạng theo các control này, **chưa chứng minh game đang phát đúng clip hoặc driver cho chúng**.

## Hướng xử lý tay/giày kéo dài

V3 đổi đối số Face ID của hàm tải tổng trước rồi sửa lại một setter. Việc đó vẫn cho phép các nhánh khác trong hàm tổng nhận tên ND01. V4 bỏ cách đó: đối số Face ID gốc đi nguyên vẹn qua hàm tổng; không hook/đổi setter nhận diện.

Thay thế chỉ còn ở hai điểm:
- Loader mesh, với đúng actor/full Card ID và đường dẫn mesh 4522 hợp lệ.
- Formatter của đúng chuỗi đường dẫn Texture2D Face_D, trong scope của cùng actor/thread khi đang dựng đầu đó.

Các format khác đi thẳng đến hàm gốc, không đổi varargs/hidden result pointer. Scope kết thúc khi hàm dựng đầu trả về; các lời gọi ngoài scope hoặc thread khác không thừa hưởng việc thay asset. Callback gốc giữ nguyên cleanup. Nếu mesh riêng trả null, nạp lại **cả đầu và texture gốc** trong scope bị chặn redirect để không lặp.

Điều này loại bỏ việc đổi Face ID khỏi toàn bộ luồng dựng hình, đồng thời bổ sung rig metadata phù hợp mesh PC. **Đó là thay đổi nhằm xử lý lỗi đã báo, chưa phải xác nhận thực nghiệm rằng nguyên nhân duy nhất đã được tìm thấy hoặc replay đã hết lỗi.**

## Log cần lấy sau khi thử

`files/embedded-gateway/work/tools/noodle-hair-status.json`

- `version`: `ronaldo-pc-face-v4-scoped-assets`.
- `state`: HOOK_ACTIVE, `error`: null, `payload_verified`: true.
- `redirects`, `texture_path_redirects`, `nonnull_callbacks`, `texture_nonnull_callbacks`: cần có lượt tương ứng khi đầu/texture được tải.
- `last_face_profile`: vẫn là mã gốc như `4522ep00v0313`.
- Nếu có lỗi: chép thêm `skipped_face_id`, `unscoped_or_disabled_calls`, `restore_requests`, `null_callbacks`, `texture_null_callbacks`, `outer_calls`, và ảnh/đoạn quay ngắn cutscene. Video dưới 32 MiB mới tải được bằng công cụ hiện tại.

## Tắt và so sánh với đầu gốc

Dùng `Tat-dau-thu-Ronaldo.zip`: buộc dừng game, giải nén, chép `work/` vào `files/embedded-gateway/`, ghi đè rồi mở lại. Gói chỉ đặt enabled=false, để manifest ổn định; mọi đường dẫn mặt/tóc trở lại nguyên bản khi chạy. Đây cũng là phép so sánh để biết lỗi kéo dài có đi cùng đầu thử không. Không cần xóa save. Để bật lại, cài đủ gói v4 như trên.

## Kiểm tra trên máy phân tích

- UEViewer đọc đủ 4 head + 4 texture mặt và atlas tóc từ container 11 package; kiểm tra checksum/bulk/mip.
- So hình học/UV skin PC, bind matrices native, bone lists, bone-map <=75, tổng weight mỗi đỉnh =255; kiểm tra deformation jaw cơ bản.
- Unicorn chạy code ARM64 và năm detour thực: 16 kiểm tra về full Card ID, bốn biến thể, giữ nguyên Face ID, formatter chỉ đổi texture, bảo toàn hidden FString result x8, scope đóng sau call, cách ly thread khác, full fallback và fallback inline không lặp. **Thân hàm engine được mô hình hóa tại biên, không phải chạy renderer Android.**
- Chạy năm đường Python installer và worker HOOK_ACTIVE ở biên ctypes/native mô hình hóa, kiểm tra SHA/prologue engine thật.
- Gateway delivery/hash/idempotence, kích thước gateway và CRC/whitelist ZIP. Native v4 khác v3, cần chép đủ .so và .py cùng gói.

Nguồn PC do người dùng cung cấp, tóc NEUBE. Chưa có xác nhận Android v4. Không dùng ảnh render Blender làm bằng chứng replay đã hết lỗi.
