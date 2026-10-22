> Cập nhật: đã lấy được đầu Android từ pc3700 và ghép tóc trong Blender. Xem [bản ghép Android mới](../ronaldo-android-fit/README.md). Chưa có bản cài trong game. Các ghi chú thiếu mesh dưới đây mô tả thời điểm của bản nguồn PC trước đó.

# Ronaldo tóc mì tôm — bộ nguồn đã chuyển đổi

**Trạng thái: chưa cài được vào eFootball Android. Không chép đè bộ này vào game.**

Mục tiêu duy nhất: Card ID **88044950524330**. Không sửa các thẻ Ronaldo khác. Bộ này không chứa hook đang bật, file dt200, APK sửa đổi hoặc asset Unreal Android đã cook.

## Đã làm được

Đọc được face.fpk, face.fpkd và f.rar người dùng gửi. Gói NEUBE chứa 3 FMDL: mặt, tóc và miệng; tổng cộng 10 mesh, 8.180 đỉnh và 10.705 tam giác. Chuyển đủ 12 FTEX sang DDS/PNG. Dựng lại hình học, UV, normals và các trọng số xương trong Blender 4.3, xuất FBX và GLB.

Riêng lớp tóc xoăn: 5.005 đỉnh, 5.179 tam giác; toàn bộ trọng số là 100% sk_head. Mesh phụ của hair_high.fmdl có thêm 572 tam giác vùng đầu/cổ. Hướng chuyển riêng lớp tóc khả thi hơn về skinning so với mang cả mặt PC sang.

## Các file chính

- `converted/Ronaldo_88044950524330_SOURCE.blend`: cảnh nguồn có texture đóng gói, mở bằng Blender 4.3.2.
- `converted/Ronaldo_88044950524330_SOURCE.fbx`: mặt/tóc/miệng, UV và rig tham khảo PES.
- `converted/Ronaldo_88044950524330_SOURCE.glb`: mô hình trung gian; vật liệu tóc hai lớp FOX chưa được chuyển tương đương hoàn toàn.
- `converted/Ronaldo_NOODLE_HAIR_ONLY_REFERENCE.fbx`: chỉ lớp tóc xoăn và rig tham khảo đi kèm; không phải asset Unreal.
- `converted/*.png`, `converted/*.dds`: texture nguồn đã giải mã/chuyển định dạng.
- `Ronaldo_source_preview.png`: ảnh render từ mô hình nguồn, **không phải ảnh trong game**. Mắt/common overlays thiếu texture; vật liệu tóc chỉ là bản xem trước gần đúng, chưa phải chất lượng hoàn thiện.
- `source-extracted/`: dữ liệu PES nguồn giữ để làm tiếp.
- `model-analysis.json`, `bone-name-comparison.json`, `conversion-notes.json`, `validation.json`: kết quả đo/kiểm tra.

## Vì sao chưa áp dụng được vào Android

1. PES 2021 PC dùng FPK/FMDL/FTEX; Android đang xét tải SkeletalMesh Unreal từ đường dẫn dạng `/Game/Assets/character/RealFace/SK_<variant>_Face`. Đổi đuôi FPK/FBX thành uasset hoặc bỏ FBX vào pak không tạo ra SkeletalMesh hợp lệ.
2. Mẫu Android đọc được (`SK_133157_Face`) phụ thuộc `SKEL_Body`, các material head/hair và dữ liệu `PesFaceAssetDataMobile`. Bảng tên của mẫu có 6/38 tên xương PC. Đây chỉ là đối chiếu tên trong package, không phải chứng minh bind pose hoặc các index trùng nhau. Riêng tóc xoăn chỉ cần liên kết sk_head nhưng vẫn phải khớp transform, vị trí đầu và phân chia phần tóc cũ.
3. Chưa tìm thấy mesh đầu Ronaldo 4522/biến thể tương ứng trong các container đã đọc được. Thumbnail và bảng redirect không thay thế được head mesh. Cần mesh Ronaldo Android thật cùng skeleton/material/texture liên quan để kiểm tra đường nối, phần tóc cũ và vị trí đeo tóc mới.
4. Chưa có quy trình cook Android đúng phiên bản/định dạng tùy biến của game được xác minh trong môi trường này. Chưa tạo hoặc nạp thử uasset mới trên thiết bị. Vật liệu FOX hai UV/alpha phải chuyển lại thành vật liệu Android tương ứng.
5. Thay toàn cục head asset 4522 sẽ ảnh hưởng những thẻ Ronaldo khác. Khi có asset hợp lệ, cần asset riêng và định tuyến theo **full 64-bit ID 88044950524330** tại khâu tạo nhân vật. Chưa bật định tuyến này vì asset đích chưa tồn tại.

Không có kết luận rằng chuyển đổi là bất khả thi. Kết luận hiện tại là **đọc và chuyển nguồn 3D thành công, cài vào Android chưa hoàn thành**. Không phát hành bản dán đè giả để thử vận may.

## Hướng làm tiếp cụ thể

Lấy đầu Ronaldo Android thật và skeleton bind pose; chọn ghép riêng tóc, giữ mặt/biểu cảm Android; căn chỉnh tóc vào đầu, xử lý mesh tóc cũ; chuyển alpha/material/normal; cook skeletal mesh Android có tên riêng; mount container; sau đó mới thêm hook nhận full ID. Kiểm tra mục tiêu, các thẻ Ronaldo khác, cảnh cận mặt, vào trận và chuyển màn hình. Chỉ khi kiểm tra được các bước này mới đóng gói bản cài.

## Tái tạo và ghi nguồn

Nguồn hình học/texture: mod người dùng cung cấp, tác giả **NEUBE**, tên gói Cristiano_Ronaldo_Nodle_Hair_Pes_2021_From_FIFA_-_NEUBE. Không phải tác phẩm tạo mới của người chuyển đổi. Không thực hiện các yêu cầu subscribe/donate hoặc cài Sider trong ảnh hướng dẫn PC.

Parser tham khảo: https://github.com/the4chancup/pes-fmdl-blender commit `231093d3a056176b8d6e33e79d13f5563b27b985` (addon foreground). Không phân phối lại mã thư viện trong ZIP; để chạy script, clone đúng commit vào thư mục `pes-fmdl-blender`, giữ các thông báo/điều khoản của nguồn đó. `inspect_models.py` cần Pillow; `build_blender.py` chạy bằng Blender 4.3.2. Rig trong cảnh dùng vị trí tham khảo PES của addon, chưa được retarget sang Android.

`validation.json` xác nhận số mesh/tam giác, các thuộc tính UV/skinning trong GLB và việc chuyển 12 texture. Đây không phải kiểm thử engine hoặc điện thoại. Game và bộ đội hình v18 giữ nguyên.
