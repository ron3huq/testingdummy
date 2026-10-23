# Dựng lại và kiểm tra

Source ZIP chứa mã, sáu RAR mới, model tham chiếu Jr/Hoàng Đức đã trích từ nguồn cũ, model/offset ND06, hai FTEX Sparta, ảnh thiết kế đã hoàn thành và runtime nền được ghim SHA. Đây **không phải bộ chạy độc lập trên một tài khoản trống**: cần dựng lại dependency và tải những dữ liệu nền dưới đây. Không cần root hoặc lấy cả thư mục game từ điện thoại.

## Dữ liệu/dependency

- Checkout repository `ron3huq/testingdummy`, nhánh `chat-downloads`, để có corpus `editor-v16/source/catalog.json`, CPK `crcfix/test/dt200_mobile_all.cpk` và lịch sử công cụ.
- Gói v19 đã đăng: `player-faces-v19/Faces-v19-13-cards-Sparta-kits.zip`; SHA-256 `40ffebb97edd616138150c7967675b9f03dab12698b7642d9c5fd42197c4375d`. Script chuẩn bị trích riêng ba tệp container vào `player-faces-v19/container`.
- APK efootxi 1.3.2 và hai `resources-02.zip`/`resources-03.zip` từ bản phát hành public của `maxlzyver/efootxi`. Engine SHA-256 `3da06a36fb5c434a75c5739af65f16664347477bd653659eb354376410d52f98`.
- Python 3.12, dependency trong `source/requirements.txt`; libarchive hệ thống.
- PES FMDL tools: `https://github.com/the4chancup/pes-fmdl-blender`, commit `231093d3a056176b8d6e33e79d13f5563b27b985`, đặt tại `/workspace/ronaldo-work/pes-fmdl-blender`.
- UEViewer có patch `references/ueviewer-v5.patch`, nằm tại `/workspace/ronaldo-work/UEViewer/umodel`. Patch cung cấp log RANGE để đọc đúng dữ liệu UE4.26 Android. Các hướng dẫn dựng nền chi tiết vẫn ở source v16/v19.
- Zig 0.13.0 qua `ziglang`; Blender 4.3.2 chỉ cần cho `render_portraits.py`, không cần để chép gói hoặc tái sử dụng PNG đã thiết kế.

Workspace mặc định: `/workspace/ronaldo-work`. Các script còn tham chiếu workspace này. Khi chuyển tài khoản/máy cần tạo lại cấu trúc đó hoặc chỉnh các biến đường dẫn ở đầu script; đường dẫn phiên trước không tự tồn tại.

Các reader cần `global.*`, native container `pc0010`, `pc0101`, `pc0103`, `pc1000`, `pc1001`, `pc3611`, `pc3700`, container native phụ và `pc9261` khi cần. `.utoc` phải đi cùng `.ucas` và `.pak`; không dùng riêng index để tuyên bố đã đọc được texture. Tệp `pc9261` có sẵn trong APK hoặc resources-03, không cần xin lại từ điện thoại.

`v19-reader` là thư mục symlink các native container kể trên cùng global; `v20-final-reader` có cùng dữ liệu native và trỏ `pc9298*` sang **container v20 cuối cùng**. Không để cả container v19 và v20 cùng tên trong reader.

## Thứ tự chạy trong môi trường đã chuẩn bị

```sh
python source/prepare_v20_inputs.py
python source/prepare_country_sources.py
python source/build_heads.py
python source/build_kits.py
python source/build_cards.py
bash source/build_native.sh
python source/validate_v20.py
python source/prepare_deploy.py
python source/validate_install.py
python source/validate_runtime.py
python source/verify_assets.py
python source/package_release.py
```

`verify_assets.py` cần các log mesh hiện hành ở `reader-logs/`; có thể xuất lại từng `SK_NW*_Face` bằng UEViewer với `-export -gltf -notex -game=ue4.26 -android -noanim`, AES được cấu hình trong scripts. Log đã xuất khi dựng bản phát hành được kèm để đối chiếu. Khi thay đổi cấu trúc binary phải xuất lại, không lấy offset cũ cho một layout mới.

Các ảnh `art/*-sheet.png` là đầu vào đã thiết kế. Script chỉ tách/crop/resample đúng kích thước native, không cần gọi lại công cụ tạo ảnh. Nền được ghi rõ là mẫu tự thiết kế, không xác nhận là nền Konami mới nhất.

Các bước kiểm tra ARM64 chạy mã hook thật trong Unicorn, nhưng nhiều ranh giới engine/API/allocator/RHI được mô hình hóa. Mở được mesh/texture bằng UEViewer hoặc render được trong Blender **không tương đương renderer Android**. Cần người dùng xác nhận mặt đen, biểu cảm, tên/số áo và replay trên điện thoại.
