# Kiểm tra đồng bộ đội hình v18

Vấn đề người dùng xác nhận: dữ liệu đội hình trên web v17 khác game, không phải báo game mới lỗi toàn bộ đội. Nguyên nhân xác định được trong build_data.py v17: roster tĩnh, suy luận sơ đồ4-3-3 khi không có plan, tự cấp số áo còn trống, captain mặc định ô0 và các taker mặc định ô10. Các đội có plan tĩnh cũng không đồng nghĩa với dữ liệu hiện tại trên điện thoại.

v18 không dùng các suy luận này làm đội hình mở để sửa. Catalog offline chỉ cung cấp danh sách tên đội; roster trên màn hình phải đến từ snapshot native hoặc dự án người dùng đã lưu và chủ động nhập lại.

## Dữ liệu gốc đã truy

Native Team: danh sách key16 byte bắt đầu+0x110; count tại+0x40c bits9..15; số áo uint16 tại+0x3a2; bốn plan34 byte tại+0x478,+0x49a,+0x4d8,+0x4fa; mỗi plan gồm11 role,11 cặp tọa độ và byte cờ. Thứ tự người tại+0x538 không được giả định là0,1,2...; sáu người đá phạt tại+0x560; captain tại+0x569.255 là chưa gán.

Hàm ARM64 gốc0x68fc714 lấy player key và số áo theo member index.0x82bfb2c đọc order rồi ghép đúng vị trí/tọa độ qua0x68fe1cc/0x6a6238c. Để xuất ra web, phải đổi member index về đúng Card ID trước; người đá phạt/captain cũng đổi về ID. Khi ghi lại, index được dựng lại từ roster mới theo ID. Kiểm tra chỉ nhìn một mảng có thứ tự0..10 sẽ bỏ sót lỗi này.

## Bản đọc thụ động

Chỉ chèn lệnh copy ở các hook tra Team/cache đã có từ bản trước. Không có địa chỉ hook mới. Capture giới hạn76 đội và0x5d4 byte mỗi record. Python đọc bộ đệm riêng của thư viện bằng API copy có khóa; không dereference con trỏ engine, không gọi API engine trong đường xuất JSON. Bản cache được ưu tiên hơn record lookup; bản ghi trùng không sinh thêm file. Bận khóa thì thử lại lượt sau, không xuất thiếu rồi coi là hoàn tất.

Không chụp team bị thiếu rồi tự điền từ dữ liệu tĩnh. Không bảo đảm một đội chưa mở đã có trong file. Source=NATIVE_MATCH_CACHE hoặc NATIVE_TEAM_LOOKUP và capture_generation được giữ trong từng đội; đây vẫn là dữ liệu tại lần đọc, không phải cam kết mọi thay đổi UI sau đó đã được nhìn thấy.

## Vòng kiểm tra

Fixture thử có roster16 người và order không đồng nhất; bốn plan khác nhau; một taker255; captain nằm dự bị. Capture C → decoder Python → nhập web → lưu/xuất JSON → API C → bộ đọc sơ đồ ARM64 gốc. Đối chiếu ID, số áo, tọa độ, role, cờ riêng từng plan và captain/taker theo danh tính. Snapshot không thay byte nào của record lúc copy. Lỗi/giới hạn source được báo thay vì đổi sang một cầu thủ khác.

Các dữ liệu thử chỉ dùng kiểm tra, không đóng gói làm snapshot thật hoặc dự án mặc định. Bộ cập nhật đầu tiên bỏ riêng myleague_editor.json khỏi ZIP để giữ nguyên các sửa đội hình hiện có. Runtime chấp nhận dự án v17 trong bộ nhớ, không ghi đè file đó để nâng phiên bản.

Theo yêu cầu mới nhất, không phát hành thay đổi tóc, mặt hay hình thể trong bản này.
