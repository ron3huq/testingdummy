# Ngoại hình v16

Giữ tay dài v14 và các nhóm theo giải v15. Thử nghiệm packed-mode3/config2 của Gullit đã bị loại khỏi đường appearance_mode; set_appearance_trial luôn tắt. Editor cho ghi đè riêng theo exact64 ID và phạm vi: original, short hoặc long. Short ghi packed-mode1/config0; long ghi packed-mode2/config1. Không ghi đè nghĩa là giữ chính sách nền; original bỏ chính sách nền để dùng dữ liệu áo gốc của thẻ.

Chiều cao/cân nặng dùng tham số native47/48, đã đọc/ghi và thử biên bằng accessor gốc. Không sửa packed face/hair. Overlay được hoàn nguyên trước lượt tính buff tiếp theo rồi áp dụng sau cùng; có khóa serialize các giao dịch snapshot nội bộ và publish cấu hình trước khi hook có thể đọc. Chỉ game thread gọi các accessor context; Python loader chỉ cấu hình các bảng riêng của thư viện.

Ảnh trên Android vẫn cần xác nhận. Không có slider cơ bắp, mesh mặt/tóc hoặc tuyên bố tạo được tay xắn. Xem HUONG_DAN.md và editor-validation.json để biết phạm vi kiểm chứng.
