# V15 — thay đường shader, không lặp lại kết luận sai từ kiểm tra CPU

## Bằng chứng v14 do người dùng gửi

Runtime v14/hook hash hợp lệ. Có 3 mesh texture confirmed, 2378 head-material checks/confirmed, 3 rebinds, 3 MID created, 2378 MID channels confirmed và 0 failures; mặt trên ảnh điện thoại vẫn đen. Vì vậy kết quả đó chỉ chứng minh con trỏ, tên texture và tham số CPU, không chứng minh shader/RHI ánh sáng đúng. Chưa có bằng chứng nguồn diffuse đen hoặc người dùng cài thiếu.

## Thay đổi khác biệt có thể kiểm chứng

10 MIC HQ riêng của NF01/NF27/NFJR/NDHD được dựng từ payload MQ tương ứng: đổi own object/package name về tên HQ cũ bằng Zen FName/hash/object-ID hợp lệ, giữ package ID HQ, dùng package-store/import dependencies của MQ. Các shader native được cook sẵn trong game; không giả tạo shader bytecode. UEViewer từ container cuối đọc rõ `Loading Material3 M_Head_Face_MQ` và diffuse riêng đúng variant. Parent HQ FaceLegacy dùng D/N/SRO; parent MQ chỉ cần D. MID độc lập chỉ override BaseColorMap, có guard parent FName native MQ. Đây là phương án tránh đường shading HQ; chưa chứng minh vấn đề chính xác nằm ở lightmap/shadow/normal/material-quality GPU nào.

Không sửa skeleton/RequiredBones/active arrays/global Face IDs. Actor fields được đối chiếu UHT: +0x1aa0 là material BODY, +0x1ab8 là FACE; không gán MID đầu vào cache body. Chỉ bind component có SkeletalMesh chính xác vừa callback trả về.

## Tên UI và áo đấu

UHT `GetPlayerNameStr` exec 0x3f7a528 gọi 0x2f39c04; hàm này lookup native player bằng typed full ID (0x823c8d4), rồi lấy UTF-8 qua 0x82a1e48. V15 hook getter 0x82a1e48, dùng getter identity XOR 0x68fe720 trả typed key 16 byte, so sánh nguyên ID64/kind0. Không quét/ghi struct record hoặc sửa Player.bin dùng chung.

UHT `SetShirtName` exec 0x3d10f34 dựng FString copy sở hữu riêng, gọi virtual slot 0x838. V15 cấp FString bằng ResizeTo của engine 0x286ff60, cho phép callee move buffer, sau gọi chỉ free phần còn sở hữu qua FMemory 0x42cc968. Không đưa buffer stack/static cho một API có thể nhận FString theo giá trị. Chạy một lần cho actor/fullID/name-render-resource +0x18d0; resource đổi thì áp dụng lại. Getter/virtual setter GPU đều cần xác nhận trên máy.

## Đình Bắc

Không thấy khe mở do vị trí ở nhóm seam trùng tọa độ đã kiểm tra; các normal ngoài mặt đã trùng nhau. V15 không nhận vơ đã hàn một khe geometry chưa tìm được. UV nguồn sát biên atlas (nhỏ nhất khoảng 0,00005) có thể lấy mẫu ngoài quadrant khi lọc; chặn 40 UV mép da mỗi LOD vào vùng an toàn 2 pixel atlas. Các đỉnh hình học, rig, normal/tangent và phụ kiện mắt/miệng giữ nguyên. Hair BasePropertyOverrides ghi clip0,20 đồng thời thêm BoolProperty `bOverride_OpacityMaskClipValue=true`; chỉ đổi float mà thiếu cờ sẽ không đủ để override parent. Texture nguồn và UV tóc giữ nguyên.

## Tái dựng

Dùng venv dependency trong `source/requirements-build.txt`, Zig0.13, UEViewer patch, bản libUE4 đúng SHA và các container native đã mô tả ở v14. Đây không phải bộ công cụ độc lập tự chạy trên mọi máy. Cần khôi phục workspace đầu vào và dependency trước; không có renderer Android trong workspace này.

Các entrypoint v15: `prepare_v14_baseline.py`, `prepare_v15_art.py`, `build_v15_assets.py`, `build_native.sh`, `export_v15_assets.py`, `validate_v15_assets.py`, `validate_native.py`, `validate_install.py`, `prepare_deploy.py`, `validate_runtime.py`, `package_release.py`, `package_sources.py`. Những script v4–v14 còn kèm là lịch sử/công cụ nghiên cứu, không chạy toàn bộ theo tên file. Ảnh sheet đã tạo được kèm trong source ZIP để không phụ thuộc phiên imagegen hay đường /workspace/generated_images cũ. `references/NDDBep00v0313.log` kèm offset mesh đã đọc từ UEViewer.
