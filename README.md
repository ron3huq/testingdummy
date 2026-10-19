# File trao đổi cùng Codex

Nhánh `chat-downloads` lưu các file trong cuộc trò chuyện, độc lập với nhánh mã nguồn.

## Mới: dt200 CRCFIX — bản thử chưa kiểm chứng trên điện thoại

Đã sửa lỗi checksum cụ thể trong bản thử đầu tiên: cập nhật CRC của hai thành viên CPK và TocCrc tương ứng. Toàn bộ 3.110 checksum file, TOC và GTOC đều đạt; bộ kiểm tra TOC của Android cũng chấp nhận trong giả lập CPU. Đây chưa phải kiểm thử chạy toàn bộ game.

- [Tải ZIP CRCFIX có file khôi phục](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/crcfix/select-team-dt200-crcfix-probe.zip)
- [Tải riêng dt200 CRCFIX](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/crcfix/test/dt200_mobile_all.cpk)
- [Hướng dẫn CRCFIX](efootxi-1.3.2/crcfix/HUONG_DAN.txt)
- [Trạng thái CRCFIX](efootxi-1.3.2/crcfix/STATUS.json)
- [Đối chiếu checksum](efootxi-1.3.2/crcfix/checksums.json)
- [Phân tích lỗi bản cũ](efootxi-1.3.2/crcfix/investigation.md)

Mục đích vẫn chỉ kiểm tra Arsenal ↔ Lille trong menu. Không xác nhận chọn đội hoặc tạo mùa giải bằng bản thử. Chưa có bản Super League đầy đủ được xác nhận hoạt động trên thiết bị.

## Bản thử đầu tiên: ngừng sử dụng

Bản thử cũ gây màn hình đen; người dùng đã xác nhận khôi phục dt200 gốc giúp vào game lại. Nó còn trong lịch sử để đối chiếu, không dùng lại.

- [Tải dt200 gốc để khôi phục](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/restore/dt200_mobile_all.cpk)
- [Hướng dẫn khôi phục](efootxi-1.3.2/KHOI_PHUC.md)
- [SHA-256 tất cả file](SHA256SUMS)

Ưu tiên bản sao APK của chính bạn. Kiểm tra SHA-256 đầu vào và chữ ký tương thích trước khi áp dụng file. Không gỡ ứng dụng hoặc xóa dữ liệu để ép cài.
