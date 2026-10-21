# File trao đổi cùng Codex

Nhánh `chat-downloads` lưu file từ cuộc trò chuyện, độc lập với nhánh mã nguồn.

## Dừng dùng cả hai bản thử dt200

Người dùng xác nhận bản đầu và CRCFIX đều gây màn hình đen. Sửa checksum chỉ khắc phục một lỗi cấu trúc đã tìm được; chưa giải quyết lỗi khởi động. **Không cài lại hai bản dt200 thử.** Khôi phục dt200 gốc để dùng game đang hoạt động.

- [dt200 gốc để khôi phục](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/restore/dt200_mobile_all.cpk)
- [Hướng dẫn khôi phục](efootxi-1.3.2/KHOI_PHUC.md)

## Native hotfix v6 — Super League thực tế, Scottish cổ điển, luật cầu thủ

**V6 đã kiểm tra thành phần ARM64/gateway, chưa thử trên điện thoại.** Có12 đội Scottish cổ điển,175 vị trí dùng172 ID thật,47 chỗ thay tạm theo lựa chọn của người dùng. Không đổi tên/face người thay để giả thành người còn thiếu.

- [Tải ZIP v6](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/hotfix-v6/efootxi-1.3.2-native-hotfix-v6.zip)
- [Hướng dẫn MT Manager và giới hạn](efootxi-1.3.2/hotfix-v6/HUONG_DAN.md)
- [Toàn bộ đội hình, số áo, ID và người thay](efootxi-1.3.2/hotfix-v6/DOI_HINH_CO_DIEN.md) · [47 chỗ thay JSON](efootxi-1.3.2/hotfix-v6/classic-replacements.json)
- [Cấu hình](efootxi-1.3.2/hotfix-v6/myleague_custom.json) · [Trạng thái](efootxi-1.3.2/hotfix-v6/RELEASE_STATUS.json)
- [Native18 roster/formation/OVR](efootxi-1.3.2/hotfix-v6/native-validation.json) · [Gateway12 CLB](efootxi-1.3.2/hotfix-v6/classic-gateway-validation.json) · [80.000 trận CPU](efootxi-1.3.2/hotfix-v6/club-policy-validation.json)

Nhóm1 thắng nhóm2 khoảng70%, riêng El Clasico cân bằng; nhóm1 gặp nhóm cuối90%. Tỷ số bóng đá được giới hạn hợp lý, không còn7–4/4–2 trong mô phỏng giải122. Giữ85% trước nhóm3 và95% cho nhóm2 trước nhóm4 từ cấu hình cũ. Roma/Dortmund và Gala/Napoli có khác biệt sân nhà/khách. Không sửa kết quả đã chốt hay trận người dùng đá; giao thức chưa có phút ghi bàn CPU, không giả sự kiện MU thủng lưới phút cuối.

Sửa Fabián Ruiz105820209653455: Acceleration88, Speed88, Tackling90, Defensive Awareness90. Kicking Power>84 được+7 (trần packed127), không cộng lặp; tiền vệ/tiền đạo thiếu cả Low Screamer lẫn Blitz Curler được Dipping Shot. Bayern127: Kane9, Díaz14, Olise17, Musiala10.

Scottish518 dùng12 CLB cổ điển, giữ lịch22 vòng của gói. Hồ sơ NPC cổ điển bỏ Marseille Turn, cân bằng **OVR nền≤89** ở13 vị trí; giữ dữ liệu/serial thẻ sở hữu. Messi chỉ định có Blitz Curler/Momentum; thêm kỹ năng theo vai và đã xác minh Attack Trigger128. PSG/City/Liverpool cổ điển alias logo/kit gốc. Boost HLV và render/trận thực vẫn cần xác nhận trên thiết bị. Không thay dt200/CPK/APK/save.

Cài đủ sáu file vào `files/embedded-gateway/work/tools`, buộc dừng mở lại. Kiểm tra `native-hotfix-v6`, `presentation_error:null`, rồi thử trận Bayern127 và Scottish. `native_last_player_full_id` mới giúp báo đúng lỗi thẻ64 bit. Giữ Asia-Pacific8 đội ở Danish549; Eredivisie125 là giải Hà Lan gốc. Tóc/áo dài và Power Tackle từ yêu cầu cũ vẫn chưa áp dụng.

## Native hotfix v5 — bản trước

Gói trước có Asia-Pacific8 đội/Danish, tên/logo và cầu thủ, chưa có12 đội Scottish cổ điển hay logic mới của v6.

- [Tải lại ZIP v5](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/hotfix-v5/efootxi-1.3.2-native-hotfix-v5.zip)
- [Hướng dẫn lịch sử v5](efootxi-1.3.2/hotfix-v5/HUONG_DAN.md)

## Native hotfix v4.1 — nền đã được người dùng xác nhận Bayern hoạt động

Người dùng xác nhận mọi thứ ổn và Bayern Munich đã hoạt động sau v4.1. Gói này giữ làm bản khôi phục khi cần, với22 cầu thủ Bayern, Dembélé Tap Trick và tỷ lệ CPU85/95. Chưa có các yêu cầu mới của v5.

- [Tải lại ZIP v4.1](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/hotfix-v4.1/efootxi-1.3.2-native-hotfix-v4.1.zip)
- [Hướng dẫn lịch sử v4.1](efootxi-1.3.2/hotfix-v4.1/HUONG_DAN.md)

## Native hotfix v4 — đã xác nhận còn lỗi Bayern59835

Các roster khác đạt trong log người dùng; Bayern chưa đạt do ID59835. [Trạng thái cập nhật](efootxi-1.3.2/hotfix-v4/STATUS.json). Gói v4 giữ để đối chiếu; dùng bản thử v4.1 phía trên cho lỗi này.

## Native hotfix v3 — đã xác nhận lỗi kiểm tra roster, giữ để đối chiếu

Không cài lại v3 để thử sửa To Match Bayern. [Trạng thái v3](efootxi-1.3.2/hotfix-v3/STATUS.json). V4 thay thế đường tra cứu sai; v3 được giữ trong lịch sử và không được khuyến nghị.

## Hierarchy v2 — đã xác nhận crash Bayern, giữ để đối chiếu lịch sử

Không cài lại v2 để thử sửa crash Bayern. [Trạng thái v2](efootxi-1.3.2/hierarchy-v2/STATUS.json). Tham khảo bản v4.1 phía trên; không tự xóa save hoặc thay CPK.

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
