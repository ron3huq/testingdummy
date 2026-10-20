# File trao đổi cùng Codex

Nhánh `chat-downloads` lưu file từ cuộc trò chuyện, độc lập với nhánh mã nguồn.

## Dừng dùng cả hai bản thử dt200

Người dùng xác nhận bản đầu và CRCFIX đều gây màn hình đen. Sửa checksum chỉ khắc phục một lỗi cấu trúc đã tìm được; chưa giải quyết lỗi khởi động. **Không cài lại hai bản dt200 thử.** Khôi phục dt200 gốc để dùng game đang hoạt động.

- [dt200 gốc để khôi phục](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/restore/dt200_mobile_all.cpk)
- [Hướng dẫn khôi phục](efootxi-1.3.2/KHOI_PHUC.md)

## My League Hierarchy v2 — phân cấp CLB, hai giải tuyển và Bayern127

**Bản mới chưa thử trên điện thoại.** Đã kiểm tra hàm ARM64/detour/destructor khi tăng 18→20 đội, gateway trên DB sao chép, giữ lịch/kết quả mùa cũ và 600 mùa mô phỏng (200 cho mỗi giải).

- [Tải ZIP Hierarchy v2](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/hierarchy-v2/efootxi-1.3.2-hierarchy-v2.zip)
- [Hướng dẫn cài, phân cấp, roster và khôi phục](efootxi-1.3.2/hierarchy-v2/HUONG_DAN.md)
- [Cách sửa skill/chỉ số CPU, tay áo và logo](efootxi-1.3.2/hierarchy-v2/EDIT_CAU_THU_VA_LOGO.md)
- [Cấu hình đội/tier/ưu tiên bàn thắng](efootxi-1.3.2/hierarchy-v2/myleague_custom.json)
- [Kiểm chứng gateway và mô phỏng](efootxi-1.3.2/hierarchy-v2/worlds-validation.json) · [ARM64](efootxi-1.3.2/hierarchy-v2/native-validation.json) · [Hồi quy save](efootxi-1.3.2/hierarchy-v2/regression-validation.json)

Cài cả 6 file vào vùng nội bộ `embedded-gateway/work/tools`. Ligue1: Bayern127 thay Monaco112; Belgian League: 18 tuyển châu Á; Liga Portugal: 20 tuyển thế giới, 38 vòng. Top5 CLB áp đảo nhóm dưới; MU rất hiếm thắng; Nhật ~90% thắng CPU. Tăng ưu tiên chân sút theo yêu cầu. Mùa hiện tại giữ snapshot; bắt đầu mùa mới để có thành phần mới.

**Bayern127 có roster inline thử 15 người; Brazil45 có roster inline 21 người để thêm Vinícius vốn vắng trong native selection.** Đã kiểm tra payload prepare/START; chưa chứng minh consumer My League trên điện thoại áp dụng và chơi được trận. Logo giải và công tắc áo dài chưa thay. Không ghi đè CPK/DB hoặc dùng Monaco giả làm Bayern. Chỉ số/skill CPU inline có tùy chọn override, mặc định rỗng.

## My League Realism v1 — nâng cấp lịch, CPU và vua phá lưới

Bản Select Team trước đã được người dùng xác nhận hoạt động. Bản nâng cấp này **giữ nguyên native Select Team**, chỉ cập nhật hai file Python trong vùng nội bộ `embedded-gateway/work/tools`.

- [Tải ZIP My League Realism v1](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/myleague-realism/efootxi-1.3.2-myleague-realism-v1.zip)
- [Hướng dẫn cài/gỡ và ảnh hưởng đến mùa hiện tại](efootxi-1.3.2/myleague-realism/HUONG_DAN.md)
- [Mã mô hình](efootxi-1.3.2/myleague-realism/myleague_realism.py)
- [Kiểm chứng save/receipt và 300 mùa mô phỏng](efootxi-1.3.2/myleague-realism/validation.json)

Lịch mùa mới ngẫu nhiên một lần rồi lưu; mùa hiện tại giữ lịch và kết quả đã đá. CPU xét sức mạnh công/thủ, sân nhà và phong độ; phân bổ bàn/kiến tạo theo roster thật trong game, vị trí, chất lượng base card và đội hình chính/dự bị. Không tự cộng bàn cho CLB người chơi. Đã kiểm tra phía gateway trên DB sao chép và mô phỏng; **bản Realism mới chưa xác nhận trên điện thoại**.

## Sửa trực tiếp menu Select Team, không root — người dùng đã xác nhận hoạt động

**Người dùng xác nhận menu Select Team hoạt động ngày 20/10/2026 trên máy không root.** Bản sửa nạp qua gateway Python sẵn có, sửa danh sách My League trong bộ nhớ; không thay CPK, DB/save hoặc ký lại APK. Đã kiểm tra mã C và hàm ARM64 gốc, cả nhánh gọi mới/trampoline, với vector tổng hợp. Phần kiểm tra tự động không bao gồm Android UI; chưa có xác nhận riêng về toàn bộ luồng vào trận.

- [Tải ZIP bản thử native](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/select-team-native/efootxi-1.3.2-select-team-native-experimental.zip)
- [Hướng dẫn MT Manager và cách gỡ](efootxi-1.3.2/select-team-native/HUONG_DAN.md)
- [Phạm vi/phiên bản hỗ trợ](efootxi-1.3.2/select-team-native/BASELINE.json)
- [Kiểm tra hàm ARM64](efootxi-1.3.2/select-team-native/native-validation.json)

Khôi phục dt200 gốc trước, chỉ chép ba file của gói vào vùng **nội bộ** `embedded-gateway/work/tools` qua DocumentsProvider `73efootball 资源`. Nếu vẫn không đổi đội, file `select-team-status.json` cho biết bước nào chưa chạy. Đọc hướng dẫn trước khi thử. Menu đã được người dùng xác nhận hoạt động; giữ nguyên hai file native khi cài Realism.

## Hướng khác: chọn đội qua máy chủ/save, không sửa CPK

Công cụ này gọi đúng logic My League Android để tạo **một bản sao save mới** đã chọn đội. Đã kiểm tra Arsenal trong Ligue 1: 18 đội, 34 vòng, mở lại save/đọc thông tin mùa giải/chuẩn bị đối thủ thành công; bảng cầu thủ và vật phẩm không đổi. Từ chối ghi đè file hoặc thay mùa đã có khi chưa được yêu cầu.

**Chỉ mới xác minh phía máy chủ. Chưa chứng minh game Android mở mùa giải hoặc chơi trận thành công. Công cụ không thay danh sách Select Team nguyên bản. Cần save thực tế đang chơi và gateway đúng phiên bản; không dùng save seed trong APK để ghi đè save của bạn.**

- [Tải công cụ và hướng dẫn](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/server-team-selector/efootxi-server-team-selector.zip)
- [Đọc hướng dẫn](efootxi-1.3.2/server-team-selector/HUONG_DAN.md)
- [Xem mã công cụ](efootxi-1.3.2/server-team-selector/select_myleague.py)
- [Kết quả kiểm tra phía máy chủ](efootxi-1.3.2/server-team-selector/validation.json)

## Face, chỉ số và ngoại hình

[Phân tích mã iOS và đối chiếu Android](research/player-face-stats.md), đã cập nhật hai nhánh iOS người dùng gửi tại commit be7b0aa và f8dc2a8: phân biệt preset tham số 49–60, mesh/texture RealFace, chỉ số thẻ đang sở hữu và ngoại hình như tay áo. Có liên kết tới các dòng mã thực tế và ví dụ đường dẫn asset.

[SHA-256 các file](SHA256SUMS). Các bản thử thất bại được giữ để đối chiếu lịch sử và đánh dấu ngừng dùng; chúng không phải bản sửa được khuyến nghị.
