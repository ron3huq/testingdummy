# Phân tích v14

## Kết luận từ log thiết bị

Trong v13, appearance_build_ids chứa22 ID khác nhau, trong đó có88044950524330. Không có89138556572074,4522 hay16781738. Vì vậy điều kiện so khớp v13 không bao phủ Ronaldo đang được dựng trong lần chơi đó. appearance_shirt_calls0 cho biết điểm nạp áo bổ sung chưa được gọi trong lần ghi nhận, không phải cài hook thất bại. Log không chứng minh89138556572074 bị game đổi thành88044950524330.

## Thay đổi

Một hàm kiểm tra chung chỉ chấp nhận hai full64 ID89138556572074 và88044950524330. Serializer sửa hai bit sleeve trong bản sao52 byte; builder gọi hàm gốc rồi đặt config+0x50=1 (native long sleeve). Các đường entity/shirt cũ dùng cùng danh sách ID nếu được gọi. Không thêm điểm hook mới. Bỏ hai alias base4522/16781738. Không thay đầu/mặt/tóc.

Builder ghi riêng bộ đếm cho từng thẻ, ID vừa áp dụng và giá trị sau ghi. Cấu hình so khớp được kiểm tra với đúng chuỗi ID người dùng đã gửi, không dựa vào một ID cuối cùng.

## Kiểm tra và giới hạn

- Chạy toàn bộ builder gốc0x68ceb44 qua detour thật, converter0x68d1fbc và serializer0x68d0868; DB/context/resource boundary được mô hình hóa.
- Phát lại22 ID từ log người dùng: chỉ88044950524330 trong danh sách được cấu hình tay dài; hai bộ đếm theo thẻ và giá trị sau ghi bằng1 được kiểm tra.
- 107 ca serializer,16 ca builder,13 ca dispatch,67 ca chọn tài nguyên áo ở các bộ kiểm tra liên quan. Các ID khác và cùng lowbits khác full64 không bị sửa. Các ID base4522/16781738 không còn nhận thay đổi.
- Mã mô phỏng v10, đội hình và chỉ số không đổi; nguồn bảng/save không bị sửa. Native/cache/crash-entry/gateway regression được chạy lại.
- Đây là kiểm tra ARM64/Unicorn với một số boundary mô hình, **không phải kiểm chứng renderer/mesh/texture hoặc Android**. Cần kiểm tra tay áo trong trận trên thiết bị.

## Đội hình

Mã14 là nhánh trong apply_roster: nếu low32 của PlayerKey.kind của slot cũ khác0, bỏ qua ghi roster và lưu last_team_error. Log có14 cho1220/1221 nhưng không chứa các khóa slot, nên chưa đủ dữ liệu để bỏ kiểm tra này an toàn. Bản v14 không thay đổi nhánh đó.
