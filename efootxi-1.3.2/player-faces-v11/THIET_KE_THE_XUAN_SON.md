# Adriano -> Nguyễn Xuân Son, ID 88045755960841

Đã xuất thật hai texture của đúng thẻ từ pc1000_mobile_and trong dữ liệu công khai:

- 88045755960841_: RGBA 128×128, ảnh nhỏ.
- 88045755960841_l: RGBA 184×256, ảnh ghép chân dung lớn và nhân vật phụ của Adriano; khung Epic là lớp UI khác.

Ảnh gốc và log ở card-art-research/xuan-son/. Không yêu cầu lấy dữ liệu điện thoại.

Bố cục dự kiến bám thiết kế thẻ Adriano gốc: giữ khung Epic và dải xanh lam/xanh lục của game, thay chân dung lớn bằng ảnh Xuân Son nghiêng người hô lớn, đặt ảnh Xuân Son giơ tay ăn mừng phía trước. Giữ da, tóc, băng đầu, áo Việt Nam và số 12 theo hai ảnh người dùng cung cấp. Dành khoảng trống cho overlay tên/vị trí/rating/sao native, không in một bộ chữ/số trùng lên ảnh. Không đổi chỉ số thi đấu bằng artwork.

Đã gọi image_gen với hai ảnh tham chiếu. Dịch vụ trả HTTP 400: Unknown parameter: reasoning. Đây là lỗi công cụ, không phải đã tạo xong ảnh. Hiện chỉ có bản đặc tả và ảnh đích gốc; chưa có artwork Xuân Son, chưa thay thẻ trong game và chưa đổi tên Adriano trong dữ liệu cầu thủ. Không đưa bản giả/chưa hoàn thành vào ZIP cài game. Khi công cụ ảnh hoạt động lại, cần tạo artwork, xuất hai texture đúng alpha/crop, đóng gói riêng đúng ID và kiểm tra UI.
