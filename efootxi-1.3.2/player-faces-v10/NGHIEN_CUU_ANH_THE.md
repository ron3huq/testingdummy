# Ảnh thẻ Nguyễn Đình Bắc — ID 88038776539586

Đã tìm trong dữ liệu công khai của chính game, không yêu cầu lấy dữ liệu điện thoại. Container pc1000_mobile_and nằm trong resources-03.zip của bản resources-311010101-v1; đã trích xuất UTOC/UCAS/PAK và đọc bằng UEViewer.

Hai package đúng ID:

- /Game/Assets/ui/Data/Thumbnail/Player/Variation2022/88038776539586_
- /Game/Assets/ui/Data/Thumbnail/Player/Variation2022/88038776539586_l

Đã xuất PNG: ảnh nhỏ 128×128 RGBA, ảnh lớn 184×256 RGBA. Ảnh nhỏ là chân dung Pato tách nền; ảnh lớn gồm chân dung Pato cùng lớp ảnh phụ, có vùng trong suốt. Không phải ảnh thẻ hoàn chỉnh có rating/vị trí/tên/khung/sao như ảnh người dùng gửi.

Dữ liệu pc0102_mobile_and có M_UI_PlayerCardFront, MI_UI_PlayerCardFront, M_UI_MobileIconFront, MF_PlayerImageCropping và MF_PlayerCardFrameColorChange. Đây là bằng chứng giao diện ghép nhiều lớp. Việc thay chân dung đúng ID có cơ sở kỹ thuật rõ ràng; thay toàn bộ khung dùng chung sẽ tác động thẻ khác nên không làm như vậy.

Để có thiết kế Đình Bắc xanh neon theo mẫu, cần tách phần ảnh/hiệu ứng khỏi các thông tin 90, LWF, S+, tên, sao và ký hiệu B mà UI đang vẽ. Chép nguyên poster mẫu vào chân dung sẽ có nguy cơ trùng chữ, lệch crop và chồng khung. Rating/vị trí trên ảnh không đồng nghĩa thay rating/vị trí thật của cầu thủ.

V10 chưa thay artwork của thẻ. Nghiên cứu đã xác định chính xác hai asset đích, kích thước và alpha, kèm ảnh gốc trong card-art-research/. Bước tiếp theo là tạo hai texture chân dung/nền phù hợp crop và thử thay riêng hai package, rồi kiểm tra UI trên điện thoại; chưa tuyên bố thẻ trong game đã giống mẫu.
