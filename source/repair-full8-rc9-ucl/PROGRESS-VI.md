# Tiến độ — chưa hoàn tất UCL

Đã xác minh nền FULL8 RC7/v19.1: inventory4acc1d023a92a7e75874aa7684e97e21e49193f3cd166911fc04eacd78e95ff8,1397tệp. Không chạy assembler RC8. Giữ nguyên DEX và control/Transfer RC7.

Face ID89138556572074: có24asset theo4biến thể và6palette, bộ chọn AArch64 được chạy với Unicorn; bảy fullID đối chứng không đổi. Reader độc lập kiểm tra24asset, LOD0/1 có RequiredBones166/153 và low skin743vertex; các bone thân ngoài8..20 có bind pose trùng donor native. Diffuse đầu/cổ được cân từ UV thực tế về cùng palette thân; khoang miệng và toàn bộ phần oral đen mờ. Preview4góc dựng từ readback asset đã đóng container. Chưa thử trực tiếp điện thoại, chưa chứng minh hết lỗi tay dài trong SIUU hay chuyển LOD.

UCL: source thuần Python +8lịch hợp lệ;144trận league phase,189toàn giải; tuyến vô địch15/17trận; test cộng tổng tỷ số, không luật bàn sân khách, từ chối penalty sai, lưu/mở lại SQLite và receipt gửi trùng. Pots là tier sức mạnh cân bằng trong game; chưa có hệ số UEFA thật. Pool36đội cố định cần kiểm tra đủ roster native trước khi nối trận.

CHƯA CÓ: native match adapter, nút mở thực tế, bảng cầu thủ xuyên giải, WorldCup adapter và lọc EventAI chỉ2mục. Không copy protected bundle v25 vào runtime. Thư việnUE4 v19.1 đã lấy đúng từ RAR và xác minh SHA efd257d9e41b622d6ecb8f51f7b0a8ee8820113fd427c5572025df1c8eecc7b8. Parser match_env tại0x7578bc8 đọc exTime/pk nhưng chưa tìm được đường truyền tổng tỷ số lượt đi vào điều kiện hiệp phụ/luân lưu của engine. Chỉ đổi exTime/pk ở lượt về sẽ sai khi thắng lượt về nhưng hòa tổng tỷ số. Không đoán offset để hook, không giả kết quả penalty hay quảng cáo đã đá được giải.

Ứng viên face revision19018 ghi ucl_integrated=false; không phải bản FULL hoàn thành yêu cầu UCL. Source tiếp tục tại runtime/ucl_lp_mode.py; code nghiên cứu/binary engine và bytecode v25 ở ngoài payload.

Mốc thể thức:2024/25, không áp quy định lợi thế sân nhà QF/SF mới hơn. Đối chiếu nguồn UEFA:
- https://www.uefa.com/uefachampionsleague/news/0287-1964b9b0f4ce-e069b2345f39-1000/
- https://www.uefa.com/uefachampionsleague/news/0296-1d0c26a3003a-1f9eb25a0553-1000--uefa-champions-league-round-of-16-quarter-final-and-semi/
- https://fr.uefa.com/news-media/news/0294-1c7efa2c4f6a-88043c185004-1000--en-cas-d-egalite-de-points/
