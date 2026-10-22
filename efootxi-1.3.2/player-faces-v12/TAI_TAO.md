# Rebuild v12

Cần môi trường/dependency từ source v10, libUE4 Android đúng SHA trong NGHIEN_CUU.md, và ZIP v10 gốc SHA256 8f0e38a49cf14f66d6123224f03be1225158709d2a704612033d2f8753a34286. Các đường /workspace/ronaldo-work không tự tồn tại ở phiên mới. V12 không dựng lại mesh; khôi phục baseline và kiểm tra từng chunk.

Lấy v10 asset/container từ ZIP qua source/prepare_v10_baseline.py; source/build_native.sh cũng cần ZIP v10 tại ../player-faces-v10/. Nguồn texture thẻ lấy từ pc1000_mobile_and đã giải nén resources-03 công khai. Đặt ảnh PNG đính kèm source kit đúng đường card-art-research/xuan-son/.

Thứ tự: build_card_art.py; build_native.sh; validate_native.py; validate_preservation.py; prepare_deploy.py; validate_install.py; validate_runtime.py; package_release.py; package_v10_update.py; package_sources.py. Dùng Python với ziglang0.13, unicorn, pyelftools, numpy, Pillow, cityhash, etcpak và các dependency v10. UEViewer export độc lập để đối chiếu texture; build từ patch đã cung cấp, không chuẩn hóa line endings của patch.

Các báo cáo hình học/rig/texture/seam v10 được tái sử dụng sau khi validate_preservation chứng minh 264 chunk đầu/tóc không đổi. SHA container được cập nhật vì hai UI packages mới. Shader/render/cutscene chưa được thử trên điện thoại; các biên engine được mô hình hóa ghi rõ trong native-validation.json.
