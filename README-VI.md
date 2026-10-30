# Sáu bản đầu — Blender và ảnh kiểm tra

Đây là gói xem trước trong Blender. **Không phải gói Android, không dán vào APK.** Bản game UI7.19 không được thay đổi trong đợt này.

| Thư mục | Nội dung |
| --- | --- |
| Mullet-A-Ferran-Texture | Giữ hình học tóc Mullet V13, ghép lại atlas texture tóc Ferran vào UV tóc Mullet. Giảm độ bóng tóc. |
| Mullet-B-Ferran-Full-Hair | Giữ mặt Mullet, thay toàn bộ phần tóc bằng mesh tóc và scalp Ferran. Căn bằng phép biến đổi đồng dạng theo bề rộng, mép trước và đỉnh tóc Mullet. |
| Ronaldo-2017-Noodle-Honda | **Một bản duy nhất:** Ronaldo 2017 / Noodle Hair / face đang áp lên Honda Keisuke theo xác nhận của bạn. Nguồn Blender mới nhất là RONALDO-EYES-V9; căn phần đầu theo kích thước da đầu 4522 và chuyển tiếp mềm xuống chân cổ. |
| Wukong-Beard-Fur-Dense | Tăng mật độ alpha của atlas lông đang dùng chung cho râu và tóc; giữ nguyên hình học, độ dài và UV. |
| Joker-Head-Neck-Refined | Căn lại chiều rộng, chiều sâu đầu và đoạn chuyển tiếp cổ; giữ texture nhận diện, topology và skin weights. |
| Raiden-Silver-Mask-Bright-Hair | Làm sáng tóc; các đảo UV giáp/mặt nạ dùng vật liệu bạc kim loại phản chiếu và normal map nguồn. Không dùng vùng tọa độ rộng để tô bạc cả da mặt. |

Mỗi thư mục có file `.blend` đóng gói texture và tám ảnh PNG: trước, chéo trái, trái, chéo sau trái, sau, chéo sau phải, phải, chéo phải. `CONTACT-SHEET.jpg` gom tám góc. `SIX-FRONTS.jpg` so sánh mặt trước của sáu bản. Ảnh là render từ mesh Blender, không dùng ảnh AI để thay kết quả render.

## Mắt và miệng Ronaldo

**Mắt giữ nguyên từ file Blender nguồn.** Hai cách thử đưa texture mắt gốc 4522 lên mesh hiện tại tạo mắt thiếu rõ nét, nên đã bỏ các cách thử đó khỏi vật liệu đang dùng. Hình học và UV mắt nguồn được khôi phục; vật liệu mắt có độ nhám riêng.

**Yêu cầu thay nguyên mắt 4522 chưa hoàn tất:** nguồn hiện có chỉ xuất được LOD thấp, không có hình học mắt 4522 chất lượng cao cần thiết. Không coi phần này là đã đáp ứng yêu cầu “nguyên mắt gốc 4522”.

Vật liệu vùng trong miệng được giảm độ sáng và độ bão hòa; môi và da ngoài không được tô tối chung. Có thêm ảnh thử xoay xương hàm 20 độ trong Blender để xem phần trong miệng. Đây là tư thế kiểm tra tĩnh; kiểm tra hoạt ảnh mở miệng trong game vẫn cần bước Android sau khi duyệt hình.

## Những gì đã kiểm tra

- Mở lại đủ sáu file Blender; texture nằm trong file, không phụ thuộc đường dẫn máy làm việc.
- Mỗi file giữ đủ 166 xương và ma trận xương trùng nguồn tương ứng.
- Mullet A, Wukong, Raiden giữ tọa độ đỉnh trùng nguồn; thay đổi nằm ở texture/vật liệu.
- Mullet B có 3.691 đỉnh tóc và 341 đỉnh scalp Ferran, giữ topology của hai phần đó.
- Báo cáo máy đọc được: `build-validation.json`, `reopen-verification.json` và `render-times.json`.

Đây là kiểm tra Blender. Chưa xác minh hoạt động trong trận, cutscene, replay, LOD trên điện thoại; chưa thể cam kết không lỗi hoặc không lag trong game. Không scale tay/chân để sửa lỗi skeleton.

## Mở file

Dùng Blender 4.3.2 hoặc bản tương thích mới hơn. Mở `.blend`, xem bằng Material Preview hoặc Rendered. Nếu máy không hỗ trợ denoiser, gói đã tắt tính năng đó. Ảnh PNG dùng ánh sáng studio; độ sáng và độ phản chiếu trong game sẽ phụ thuộc shader và ánh sáng sân.

Transfer, vai trò đội trưởng, preview đội Real Madrid bị lặp David Raya và bộ lọc booster chưa được sửa trong gói này; các mục đó làm sau đợt duyệt sáu đầu theo ưu tiên của bạn.
