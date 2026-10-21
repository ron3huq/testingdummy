# V11 — bản thử áo tay dài Ronaldo89138556572074

Bản này chỉ thêm đường sửa tay áo; giữ nguyên đội hình/chỉ số/skills và mô phỏngv10. TócPato→Ronaldo88044950524330 **chưa áp dụng**, xem `NGOAI_HINH.md` để biết bằng chứng và tài nguyên còn thiếu.

1. Buộc dừng efootxi. Sao lưu đủ7 file đang dùng.
2. Giải nénZIP. Chép **đủ7 file** trong`install/work/tools/` vào`files/embedded-gateway/work/tools/` của game, ghi đè cùng tên. Không tạo thêm thư mục lồng. Không thaydt200/CPK/APK/DB, không xóa save.
3. Mở game, dùng đúng thẻ`89138556572074` vào trận. Kiểm tra lúc trận đã tải xong; ảnh card không phản ánh mesh tay áo3D.
4. Mở`work/tools/select-team-status.json`: cần`version: native-hotfix-v11`, `state: HOOK_ACTIVE`, `appearance_error: null`. Sau khi dựng đúng thẻ,`appearance_sleeve_applies` cần lớn hơn0. Bộ đếm xác nhận đường sửa dữ liệu đã chạy, không tự chứng minh hình ảnh render đúng.
5. Nếu bộ đếm0: buộc dừng rồi mở lại, đưa đúngCardID vào đội hình và vào trận mới. Nếu đã>0 nhưng tay áo vẫn ngắn, chụp hình cầu thủ trong trận và gửi đoạnstatus trên để phân biệt kit/đườngrender khác.

Ronaldo88044950524330 và các thẻ khác không được đổi tay áo bởi bản thử này. Face, tóc và thống kê của các thẻ giữ nguyên.

Nếu có lỗi, buộc dừng và phục hồi đủ7 filev10 đã sao lưu. Các kiểm tra native/gateway đã qua trên môi trường phân tích; **chưa chạy trên điện thoại**.

`myleague-realism-status.json` vẫn có thể ghi model`native-hotfix-v10`: chủ ý giữ mã và hạt ngẫu nhiên của mô phỏngv10. Phiên bản gói mới nằm ở`select-team-status.json`.
