# FULL-8 RC3 · APK73 · nền FULL-7

Gói FULL tích lũy tiếp nối HF1 a7ad1171, resource revision19009. Giữ sửa manifest thiếu cache của HF1. **RC3 chưa được kiểm chứng trên điện thoại.**

## Single Player và nút xanh

Đã xem video: chọn Ronaldo89138556572074 đang trên sân, nút1P ON nhưng cursor vẫn chuyển giữa Nuno Mendes, Dembélé, Stam. Nguyên nhân mã tái hiện được: RC2 chỉ bỏ gate AI tại tick0x112d4; hàm nhận điều khiển vẫn trả về ở gate0x120e8 khi AI tắt. RC3 bỏ thêm gate thứ hai, giữ kiểm tra ownership/pause/replay và restore. Không bắt buộc bật AI xanh.

Trong trận chạm1P bật/tắt, nhấn giữ chọn cầu thủ đội hình hiện tại. Nút **xanh / 1P ON** khi native báo đã áp dụng; **vàng / 1P WAIT** khi đã yêu cầu nhưng native chưa áp dụng; **xám / 1P OFF** khi tắt. Không còn dùng thông báo lưu thành công làm bằng chứng đã điều khiển được. Trạng thái đọc lại mỗi giây khi cửa sổ game có focus.

Đã đối chiếu picker/control code PES2021: key/slot live theo side, loại cầu thủ ngoài sân. Không sao chép engine/thư viện PES cũ sang73. Kiểm tra mới chạy xuyên toàn bộ enter, fixed và restore ARM64, không dừng trước hàm enter như RC2; setter/getter engine73 gốc chạy trên cấu trúc tổng hợp. Đã kiểm tra ghi controller và khóa lại cùng người sau11 thay đổi con trỏ, rồi phục hồi trạng thái trước đó khi AI gốc tắt. Các trạng thái trận thật trên điện thoại vẫn cần kiểm chứng.

## Transfer · Foot & Positions

Giữ đội hình và vai trò mà người dùng đã xác nhận hoạt động. Menu cầu thủ Transfer có thêm **Foot & Positions** cạnh Abilities/Accessories/Celebration/Skills & Boosters: chân thuận, mức dùng chân yếu, độ chính xác chân yếu, vị trí chính và13 ô thông thạo vị trí. Mức thông thạo0=None,1=Partial,2=Full. Lưu trước Enter Game, áp dụng ở lần vào game sau.

Hồ sơ lưu theo full ID/giải như Transfer. Chân thuận/yếu qua native parameters43/42/45; vị trí chính/thông thạo qua native0..13 bằng helper riêng vì editor_parameter cũ từ chối0..13. Helper giữ ánh xạ cache/identity và đường GamePlan cũ. Kiểm tra lưu/mở lại và các trường thực trong native record đã qua; cầu thủ khác giữ nguyên, ra khỏi scope giải phục hồi vị trí gốc. Booster global/cid merge theo từng field. Không sửa mặc định toàn đội hay sửa save cá nhân trong gói.

## Ronaldo2027 →89138556572074

Namespace mới RV8C/HV8C, containerspc9336..9339. Giữ V8 skin/hair. Chuyển kênh alpha diffuse PC sang alpha native255; không dùng PC gloss alpha như mask da UE. Texture nén đọc lại đã có alpha255 ở cả4biến thể. Đây là sửa định dạng material, không tô màu để che rig/cổ.

Thay cụm mắt/răng donor đã dịch vị trí bằng135vertex ocular/oral lấy trực tiếp native4522, giữ nguyên tọa độ/UV/tangent. Khớp vùng da quanh mắt với bề mặt4522; giữ bone mắt/hàm/mí riêng, không gom về head. Native material4522 riêng cho mắt/răng; tóc V8 giữ nguyên. Body hierarchy/bind pose nguyên native4522; lowLOD/UV native, MinLOD0, haiLOD thật; UEViewer đọc lại4biến thể và kiểm tra material/weights đã qua.

Chưa có xác nhận điện thoại rằng mặt hết đen, mắt tự nhiên hoặc không xuyên ở mọi animation. Sửa alpha/geometry là thay đổi thực tế; kiểm tra offline không chứng minh renderer cuối trên máy.

## Nghiên cứu độ khó AI

Engine có7mức EMenuCpuLevel: VERYEASY, EASY, NORMAL, HARD, VERYHARD, HARDEST, LEGEND. Gateway ai_division.prepare gửi cpu_level theo hạng10→VERYEASY,9/8→EASY,7→NORMAL,6→HARD,5/4/3→VERYHARD,2→HARDEST,1→LEGEND. Công tắc AI điều khiển và phong độ cầu thủ là các trường khác. Đã chạy my_league.prepare với7mức và setter/getter ARM64 native0..6; thêm observer chỉ đọc mức GetCpuLevel do engine tự tính theo chế độ/sự kiện vào diagnostics. Có nhánh engine áp mức tối thiểu; cần khớp đúng trận để kết luận. Mô phỏng tỉ số nền chỉ dùng level trong seed, không chứng minh AI trên sân khó hơn. Chưa đo hành vi mỗi mức trên máy; bản này không ép/đổi độ khó. Chi tiết trong source/repair-full8-rc3/AI-LEVELS-VI.md.

## Cài gói và giới hạn

Đây là payload FULL để ghép toàn bộ assets/ và classes5.dex vào APK73 đúng nền, ký bằng khóa đang dùng; không phải APK đã ký. Giữ dữ liệu ứng dụng/save. Không gỡ app hoặc xóa data để xử lý lỗi. Giữ CPK đăng nhập, kiểm tra integrity, accessories/bandage đã được xác nhận hoạt động, Spider V1 và Miles. Không thêm Ronaldo Vol9 đã hủy, DB/save người dùng, log/video riêng, RAR/APK nghiên cứu vào gói.

Giới hạn còn mở từ bản trước: Transfer thêm ID hoàn toàn chưa có trong native roster pool còn có thể bị từ chối; mọi state Single Player/animation/renderer thực chưa được xác nhận trên điện thoại. Báo cáo cũ là lịch sử; validation lần này có tiền tố full8-rc3.
