# Nguồn và tái tạo trên Linux

Đây là tài liệu cho người tiếp tục chỉnh mã; người cài bằng MT Manager chỉ cần ZIP cài và HUONG_DAN.md.

Đã dùng checkout hiện có, không tạo Git worktree. Không cần dữ liệu từ điện thoại: đầu/texture/engine Android được lấy từ APK và resource công khai đúng 1.3.2, kiểm tra SHA-256; mesh/texture PC lấy từ nguồn đã đăng và ZIP 2006 người dùng gửi. `input-inventory.json` ghi hash và commit công cụ thực tế.

## Tệp đã mở và kết luận

- ZIP v4a: gateway, runtime Python, native .so, config, manifest và đủ ba phần container. CRC/checksum đều được kiểm tra.
- HUONG_DAN.md v4/v4a; source/build_pc_head.py, build_face_textures.py, build_full_container.py, zen_clone.py, prepare_deploy.py, runtime Python, native C, script build và các bộ kiểm tra. `previous-source-audit.json` ghi inventory/hash các source và báo cáo trước đó. Đã đối chiếu thay đổi ABI v4 sang v4a.
- Nguồn cũ `Ronaldo-noodle-88044950524330-SOURCE-NOT-INSTALLABLE.zip`: toàn bộ face_high, hair_high, oral, texture và báo cáo; bốn đầu native cùng glTF trong gói Android reference cũ.
- Hai ZIP mới: FPK/FMDL và DDS/FTEX 2006; .blend/.glb kèm FMDL gốc. FMDL trong ZIP Blender trùng FMDL của ZIP gốc 2006. Không dùng ảnh xem trước 512 làm diffuse mặt.
- APK công khai 1.3.2 và resources-02/03: pc3700, pc3611 và optional mip, shader/common assets, libUE4 đúng SHA của v4a, mẫu CMD_LOGIN_LIVEDATA.

Nguyên nhân dữ liệu: section native 743 đỉnh có nhiều cụm hình học rời, trong đó mắt và trong miệng. V4 viết lại section bằng face_high:0/:2 và hair_high:1 nên những cụm đó bị bỏ. Các mesh eyeline/eyelash/occlusion PC không phải nhãn cầu. oral.fmdl là mesh riêng; texture chung FOX của nó không được giao cùng nguồn. V5 dùng lại 135 đỉnh native với texture Android phù hợp, không giả định oral đã có trong da mặt.

## Chuẩn bị nguồn

Cần Linux x86_64, Python 3.12 có venv, g++/make, mạng tới GitHub/Debian và registry Python. Không cần Unreal Editor hay Android SDK cho cách sửa cooked asset này. Các file game chỉ được đọc làm template; gói cài chứa asset riêng.

Giải nén ZIP nguồn vào thư mục riêng, giữ bố cục `source/`, báo cáo và `inputs/`. Hoặc dùng thư mục này trên nhánh chat-downloads. Chạy:

```bash
python3 -m venv /workspace/ronaldo-build-venv
/workspace/ronaldo-build-venv/bin/python -m pip install -r source/requirements-build.txt
/workspace/ronaldo-build-venv/bin/python source/prepare_inputs.py \
  --input-2006 inputs/CRISTIANO-RONALDO-2006.zip
```

Nếu dùng checkout Git thay ZIP nguồn, truyền đường dẫn tới ZIP 2006 đã tải lên thay cho `inputs/...`. Script cần khoảng 4 GB tải về khi cache trống; không kèm các archive Android lớn trong ZIP nguồn. Nó kiểm tra hash, giải nén phần cần thiết, lấy parser FMDL/UEViewer tại commit đã ghi, áp patch headless/seek/instrumentation/texture-export, biên dịch reader và tạo native/v4a reference export. Đường dẫn mặc định `/workspace/ronaldo-work` được các bộ kiểm tra native/runtime sử dụng. Đã thực thi script với cache xác minh ở phiên này; chưa chứng minh một máy trống hoàn toàn tự phục hồi xong.

## Dựng và kiểm tra

Từ thư mục chứa source/:

```bash
export PATH=/workspace/ronaldo-build-venv/bin:$PATH
python source/build_assets.py /workspace/ronaldo-work
bash source/build_native.sh
python source/prepare_deploy.py
python source/validate_native.py
python source/validate_install.py
python source/validate_runtime.py
```

Để đọc container mới, tạo ba symlink từ `container/pc9298_mobile_and.*` vào `/workspace/ronaldo-work/reader-input/`. Giữ các symlink nguồn native/material/global mà prepare_inputs đã tạo. Xuất glTF cả bốn suffix cho cả ND01 và ND06:

```bash
/workspace/ronaldo-work/UEViewer/umodel -export -gltf \
  -game=ue4.26 -android -notex -noanim \
  -aes=0x4552d45005dfe94964893f4925ec747d3d591401e060ed8b3d58be5721c81295 \
  -path=/workspace/ronaldo-work/reader-input \
  -out=/workspace/ronaldo-work/v5-export SK_ND01ep00v0313_Face \
  > /workspace/ronaldo-work/v5-ND01ep00v0313.log
```

Các suffix là chuỗi trống, lg00v0000, ep01v0291, ep00v0313; đặt tên log `v5-<profile><suffix>.log`. Khóa asset nêu trên đã có trong công cụ đọc công khai của repository, không phải credential đăng nhập.

```bash
python source/validate_assets.py /workspace/ronaldo-work
```

Kiểm tra texture bổ sung: xuất T_ND01ep00v0313_Face_D từ `v4a-reader` vào `v4a-texture-export` và từ `reader-input` vào `v5-export`, dùng `-export -png -game=ue4.26 -android` và cùng AES key, giữ log. Sau đó:

```bash
python source/validate_textures.py /workspace/ronaldo-work
python source/preview_mesh.py /workspace/ronaldo-work
python source/package_release.py
```

preview_mesh cần PNG tóc ND0001 xuất từ mesh v5 bằng reader `-png` như đã làm ở phiên này. Ảnh CPU chỉ kiểm tra geometry/UV, không mô phỏng shader, driver, animation clips hoặc renderer Android.

## Bất biến đã kiểm tra

- Hai full Card ID tách ND01/ND06; không thay Face ID; scope actor/thread và fallback gốc.
- Tám mesh đọc được; đầy đủ 166 active/required bones, ref skeleton/bind matrices nguyên byte; mỗi draw <=75 xương; weights tổng 255.
- ND01 giữ positions/triangles/tangents/weights mặt và positions/tangents/UV tóc v4a. Diffuse mặt mip0 khớp pixel v4a trong cả hai decoder; các block mip cũ được chép vào atlas, không nén lại phần mặt đó.
- Native N/SRO metadata/sRGB giữ đúng loại texture. Mọi import có trong container riêng hoặc dữ liệu công khai của phiên bản game.
- 58 kiểm tra ARM64, năm đường cài detour, worker, manifest/idempotence/checksum lỗi và gateway 2441 byte.
- Gói đúng tám tệp, ZIP CRC và checksum runtime/manifest/container khớp. Không sửa APK/save/dt200.

Chưa kiểm tra trên điện thoại, chưa xác nhận hết replay kéo dài; không có bộ test nào ở đây chứng minh mọi biểu cảm PC hay lưỡi độc lập hoạt động. Nguồn mod cũ: NEUBE; nguồn 2006 do người dùng cung cấp, tác giả chưa xác định. Parser: the4chancup/pes-fmdl-blender; reader: gildor2/UEViewer (MIT, license đi cùng bản patch/reference đã đăng).
