# Hotfix v15 — thêm tay dài theo giải, thử kiểu tay áo riêng Gullit

Tay dài v14 đã được người dùng xác nhận hoạt động. V15 giữ nguyên hai thẻ Ronaldo89138556572074 và88044950524330 đã cấu hình, bổ sung:

- Y17 Champion League (518): Cristiano Ronaldo, Lionel Messi.
- Uefa Champion League / Ligue1 My League (122): K. Kvaratskhelia, Ousmane Dembélé, Jude Bellingham, Kylian Mbappé, Erling Haaland.

Nhận diện qua đúng tên/ID trong Player.bin:79 bản ghi Ronaldo/Messi ở518 và170 bản ghi của năm cầu thủ ở122. Chỉ kích hoạt nhóm mới trong đúng giải tương ứng. Danh sách đầy đủ trong sleeve-targets.json. Không nhầm Kvaratskhelia128720 với Pedri133157, hoặc Vitinha135067; không nhầm Jude/Jobe Bellingham hay Kylian/Ethan Mbappé.

## Hai ZIP, chọn một

1. **efootxi-1.3.2-native-hotfix-v15-long-sleeve.zip**: tay dài thông thường cho các nhóm trên; không bật thử nghiệm Gullit.
2. **efootxi-1.3.2-native-hotfix-v15-gullit-sleeve-trial.zip**: có đầy đủ thay đổi trên và bật giá trị tay áo thử nghiệm riêng ID88045755960810. Bảng Android xác nhận ID này là **Ruud Gullit**, không phải Cristiano Ronaldo. Chưa xác nhận giá trị này tạo kiểu xắn tay như ảnh; xem NGOAI_HINH.md.

Không cần cài bản1 trước bản2. Mỗi ZIP chứa đủ7 file. Hai bản dùng cùng thư viện native; chỉ khác cờ bật thử nghiệm trong myleague_custom.json.

## Cài bằng MT Manager

1. Buộc dừng hoàn toàn game, sao lưu đủ7 file hiện tại trong files/embedded-gateway/work/tools/.
2. Chọn một ZIP, giải nén rồi chép đủ **7 file trong install/work/tools/** đè vào thư mục trên.
3. Mở game, vào trận mới ở đúng giải để nhân vật được dựng lại.
4. Đọc files/embedded-gateway/work/tools/select-team-status.json.

## Kiểm tra trạng thái

- version: native-hotfix-v15.
- appearance_policy_matches.Y17 / UEFA: số lượt builder áp dụng theo nhóm giải; tăng khi cầu thủ phù hợp được dựng trong đúng giải.
- appearance_sleeve_applies: tổng lượt ghi tay áo, gồm cả serializer/builder nên không phải số cầu thủ duy nhất.
- appearance_last_applied_id: ID vừa được builder ghi gần nhất.
- appearance_build_after:1 cho tay dài;2 cho giá trị thử nghiệm Gullit.
- appearance_trial_enabled:false ở bản thường, true ở bản thử.
- appearance_policy_matches.rolled_trial: tăng khi bản thử dựng đúng Gullit88045755960810.
- appearance_build_ids: các ID trong tối đa64 lượt dựng gần nhất; gửi cùng trạng thái nếu có cầu thủ vẫn không nhận tay dài.

Shirt_calls hoặc entity_calls có thể0 trên đường game hiện dùng; v14 đã xác nhận builder vẫn đủ để đổi tay dài. Cần xem tay áo trong trận, bộ đếm chỉ xác nhận thao tác ghi cấu hình.

## Quay lại

Nếu không thích kết quả thử Gullit, buộc dừng rồi cài đủ7 file từ ZIP tay dài thông thường v15. Như vậy tắt thử nghiệm nhưng vẫn giữ phần mở rộng cầu thủ. Hoặc phục hồi đủ7 file sao lưu v14.

Không sửa save, lịch, chỉ số, đội hình, tóc/mặt, dt200, APK hay CPK. Mã mô phỏng giữ nguyên v10. Mã roster14 đã ghi nhận ở Real/Liverpool trong lượt trước vẫn chưa sửa trong bản này.
