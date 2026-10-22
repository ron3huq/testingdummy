> Cập nhật tiếp: đã có [bộ thử Android v1](../ronaldo-noodle-trial-v1/HUONG_DAN.md) với asset/container/runtime riêng. Chưa chạy trên điện thoại. Tài liệu dưới đây mô tả giai đoạn nguồn/tham khảo trước đó.

# Ronaldo Android + tóc NEUBE: bản ghép tham khảo, chưa phải bản cài

**Mục tiêu: riêng thẻ 88044950524330. Chưa phát hành asset hoặc hook tóc chạy trong game. Không chép ZIP này đè vào game.**

## Kết quả mới từ 8 phần RAR

Giải nén đủ 8 volume bằng libarchive: `pc3700_mobile_and.ucas`, 193.341.792 byte, SHA256 `c3608ab0243bb83955efb028d043b886d693599544f8e5f021d97862f5b6d1dd`.

Trích xuất thành công bốn asset Android, cả bốn khớp SHA1 được lưu trong TOC:

- SK_4522_Face
- SK_4522lg00v0000_Face
- SK_4522ep01v0291_Face
- SK_4522ep00v0313_Face

Mỗi mesh xuất được có hai section: mặt (743 đỉnh, 1.222 tam giác) và tóc (601 đỉnh, 453 tam giác), cùng 166 xương tham khảo. Bộ đọc báo LOD 0 không có chỉ mục; kiểm tra sâu xác nhận **cooked_out=true** ở LOD 0, LOD tiếp theo **cooked_out=false, inlined=true**. Đây là dữ liệu LOD bị loại khi cook trong asset này, không tự kết luận UCAS hỏng hoặc thiếu phần RAR.

Đã tìm thấy chuỗi UTF16 `++UE4+Release-4.26` trong libUE4.so Android. Điều này xác định nhánh engine, không chứng minh mọi serializer/shader của bản Epic UE4.26 chuẩn tương thích với bản game tùy biến.

## Bản ghép Blender

Giữ phần mặt Android xuất được, tách và ẩn tóc Android cũ trong cảnh tham khảo. Đưa 5.005 đỉnh / 5.179 tam giác tóc xoăn từ mod PES PC NEUBE vào hệ tọa độ cùng đơn vị mét, gắn 100% vào xương **sk_head của rig Android**.

Thử xoay xương đầu 0,08 rad: cả 5.005 đỉnh tóc di chuyển theo xương. Tọa độ các đỉnh mặt gốc không thay đổi. Sau thử nghiệm trả rig về pose nghỉ.

Bản ghép xuất 6.401 tam giác và có UV/JOINTS/WEIGHTS. Không bao gồm tóc Android cũ trong FBX/GLB mới; tóc cũ giữ ẩn trong .blend để đối chiếu. Chưa chỉnh vị trí bằng các offset thủ công, chưa kiểm chứng tất cả góc nhìn, hoạt ảnh, giao cắt hoặc chất lượng cận cảnh.

**Ảnh preview là render Blender từ mặt Android và tóc PC, không phải ảnh game.** Mặt dùng vật liệu clay vì chưa có các material/texture gốc của đầu. Tóc dùng vật liệu cutout tham khảo, chưa port shader FOX sang shader game; màu, ánh sáng và alpha chưa phải thành phẩm.

Các file trong `fit/`:

- `Ronaldo_ANDROID_REFERENCE_NOODLE_NOT_COOKED.blend`: mở Blender 4.3.2; có rig và ảnh texture đóng gói.
- `.fbx`, `.glb`: dữ liệu trung gian để làm tiếp; không phải uasset.
- `Android-head-PC-hair-reference.png`: ảnh kiểm tra hình học.
- `fit-validation.json`: kết quả kiểm tra bước ghép.

`export/` chứa glTF/bin đầu Android đã đọc. `extracted/` chứa bốn asset nguồn Android chưa sửa. Các asset nguồn này **không phải bản cài tóc mới**. Không đưa toàn bộ UCAS 193 MB hay tám volume lên nhánh tải.

## Phần chưa hoàn thành để dùng trong game

1. Chưa xác minh biến thể FaceId mà thẻ 88044950524330 thực sự chọn khi vào trận. Bản fit hiện dùng SK_4522_Face làm đầu tham khảo. Không suy biến thể từ tên/thời kỳ thẻ.
2. Các head tham chiếu material `MI_4522..._Head_FaceLegacy/FaceUpcon_HQ/MQ`, `MI_4522..._Head_Hair_HQ/MQ` và common eyelash. Chưa tìm được các material này trong chín TOC mới hoặc các container đã đọc trước đó. SKEL_Body có trong pakchunk0 gốc nhưng chưa dùng bộ material gốc để duyệt hình ảnh.
3. Chưa tạo asset SkeletalMesh/Material/Texture Android hợp lệ cho tóc mới. FBX/GLB không thể đổi đuôi thành uasset. Chưa có quy trình cook tương thích game được kiểm chứng.
4. Chưa thêm định tuyến runtime theo full Card ID; thay chung SK_4522 sẽ ảnh hưởng nhiều thẻ. Cần asset đích riêng và logic giới hạn đúng 88044950524330.
5. Chưa kiểm thử trong efootxi trên điện thoại. Không có thay đổi APK, dt200, gateway hoặc đội hình v18.

Đã kiểm tra thêm khả năng ProceduralMesh ở runtime: thư viện có các đăng ký tên CreateMeshSection / CreateMeshSection_LinearColor / SetMeshSectionVisible. Đây chỉ là dấu vết tĩnh; chưa chứng minh có thể tạo/gắn mesh, nhận material, quản lý GC hoặc ẩn tóc gốc an toàn. Không phát hành hook phỏng đoán và không coi đây là đường bỏ qua cook đã hoạt động.

## Công cụ và tái tạo

- PC mod: NEUBE, nguồn người dùng cung cấp; parser FMDL/FTEX và bản nguồn chuyển đổi ở thư mục `ronaldo-noodle-source` đã công bố trước đó.
- Export Android: UEViewer https://github.com/gildor2/UEViewer commit `a0bfb468d42be831b126632fd8a0ae6b3614f981`. Dùng global.utoc/ucas từ APK Android trước đó làm bảng tên script; log ghi rõ các imports material chưa resolve. Không sử dụng global đó để đóng gói asset thay thế.
- Build UEViewer cục bộ: tắt RENDERING và THREADING, dùng libpng/zlib kèm nguồn, bỏ SDL/GL link. Sửa lỗi seek vị trí file ở bản Linux (`fseeko64(f, 0, FilePos)` thành `fseeko64(f, FilePos, SEEK_SET)`). Bản patch và thông tin giấy phép UEViewer kèm để tái tạo; không kèm binary công cụ.
- Chọn `-game=ue4.26 -android -notex -noanim -gltf`. Dùng PAK rỗng đã có chỉ để bộ đọc phát hiện container trong thư mục phân tích, không phát hành PAK đó cho người dùng và không sửa file game.
- `fit_android_head.py` cần bản .blend nguồn NEUBE chuyển đổi trước đó ở thư mục cha; chạy Blender 4.3.2. `validate_head.py` cần dữ liệu nguồn cục bộ và thư viện Toc của repo.

`validation.json` là kiểm tra tính toàn vẹn dữ liệu và bước ghép trong Blender. **Không phải chứng nhận asset load được trong engine, phạm vi theo thẻ đã hoạt động hoặc điện thoại đã chạy thành công.**
