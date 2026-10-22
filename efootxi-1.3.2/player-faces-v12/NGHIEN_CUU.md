# Chẩn đoán v12

Log điện thoại v11: mesh_texture_confirmed=3 nhưng face_texture_reapplied=0, guard_skips=34433. Dữ liệu chứng minh texture tìm được; chưa phân biệt owner bị thiếu và actor MID rỗng. V11 test đã đặt sẵn MID, thiếu kịch bản component hợp lệ nhưng MID rỗng. V12 thêm đường gán trực tiếp material slot0, không cần cache MID, cùng các counter phân biệt nguyên nhân.

Đối chiếu libUE4 SHA256 3da06a36fb5c434a75c5739af65f16664347477bd653659eb354376410d52f98:

- Native SetMesh 0x39c6b18 dùng *actor[0x1a70] hoặc actor[0x228]. SkeletalMesh của component tại +0x468. V12 chỉ chấp nhận nếu chính pointer mesh đã được callback xác minh.
- GetMaterial exec 0x62f86c4: virtual +0x588; SetMaterial exec 0x62f85c8: virtual +0x590. Dùng API để engine cập nhật render state, không viết thẳng OverrideMaterials.
- Material/texture riêng được xác minh theo class USkeletalMesh và FName native như v11. Gán nguyên MIC chứa BaseColorMap/NormalMap/SROMap, không chỉ sửa một texture trên actor MID có thể không tồn tại.
- UI GetPlayerName exec 0x3ce95b0 đọc ID64 rồi gọi 0x3a55674; hàm này chuyển X0 ID sang X1 cho 0x3a908a0(manager,ID64,FString*). Hook đúng ID Xuân Son; FString ResizeTo dùng hàm engine 0x286ff60. Đường khác/ID khác/disabled gọi nguyên bản. Không thay Player.bin vì tên ở đó có thể dùng chung nhiều thẻ.

Unicorn thực thi mã hook ARM64 và các getter texture native. GetMaterial/SetMaterial và ResizeTo được mô hình hóa tại biên, vì vậy đây không phải kiểm tra renderer/cấp phát thực trên Android. 432 kiểm tra bao gồm MID rỗng, hai đường component, trùng component, thay override sau bake, mesh sai, disabled, full64 ID và các face đã đẹp.

Card art: texture gốc pc1000 tại ui/Data/Thumbnail/Player/Variation2022/88045755960841_{,l}.uasset. Giữ nguyên package IDs, header, kích thước và mip descriptors; chỉ thay payload ETC2 RGBA. Khung/UI vẫn do game vẽ. Container mới 182 packages, 264 chunk đầu/tóc cũ byte-identical; 2 UI packages thêm. UEViewer đọc ngược được ảnh lớn 184x256, cần điện thoại xác minh mount/cache UI.
