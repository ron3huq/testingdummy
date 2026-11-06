# Native aggregate research and experimental input adapter

Nền đúng FULL8 RC7/APK73 v19.1; engineSHA efd257d9e41b622d6ecb8f51f7b0a8ee8820113fd427c5572025df1c8eecc7b8. Không chuyển nền sang v25. Yêu cầu hiện hành: knockout hai lượt, chung kết một trận, không luật bàn sân khách.

## Bằng chứng native mới

Bộ so sánh0x6cacc80 chọn0x6cacb24 khi cờ trong RuleInput+0x12a bật. Hàm này đọc hai bàn mang sang tại+0x12c/+0x12e qua0x72eada4, cộng vào thống kê bàn hiện tại rồi so sánh tổng. Cờ+0x135 bật nhánh xét bàn sân khách; +0x136 tham gia điều kiện áp dụng theo giai đoạn. Tắt cả hai cho thể thức yêu cầu. Native constructor0x6a6479c điền những trường này qua0x72ea698/0x72ea6a0. Không dùng các offsetUI13c/728 đã khảo sát trước đó.

`test_native_aggregate.py ENGINE` chạy chính bộ so sánh ARM64 và getters trong engine; chỉ giả lập truy vấn bàn hiện tại và giai đoạn tại biên.60tổ hợp gồm cả hai phía qua; thắng riêng lượt về nhưng tổng hòa cho native diff0. Tắt aggregate khôi phục so sánh riêng trận. Kiểm tra riêng cờ bàn sân khách: bật làm đổi kết quả tổng hòa, tắt trả lại hòa. Đây KHÔNG phải bằng chứng nhánh hết giờ đã được điều khiển.

## Prototype được biên dịch và kiểm tra

`ucl_rules.c` gọi original rule builder trước rồi nạp cờ/tổng bàn vào RuleInput. Chỉ áp dụng khi IDhaiđội từ getter native0x72ebecc khớp kế hoạch; nếu sân thực tế đảo thì đảo carry theoIDđội. Không sửa bàn live, không tạo penalty. Lần arm lại cùnggame phải giữ cùng tham số; game khác bị từ chối; clear phải đúnggame; sourceđầu tiên được ràng buộc; nguồn khác không nhận bản nạp. Không đổi output khi tắt hoặc đội không khớp.

`test_native_adapter.py LIB ENGINE` chạy thư viện ARM64 vừa biên dịch cùng getter đội thật của engine. Original builder là fixture ở biên. Kiểm tra returnvaluegiữ nguyên, chỉ các trường đã xác minh thay đổi, sân đảo, retry/clear, sourcekhác và đội khác không bị sửa. Thiếu prologue/canonical game binding và nhánh hết giờ chưa được kiểm chứng, nên **prototype chưa cài vào bootstrap/runtime và không phải gói FULL**.

Lệnh trong môi trường đã cóziglang0.13,Unicorn,pyelftools:
```
python build_native.py FRESH_STAGE
python test_native_aggregate.py ENGINE
python test_native_adapter.py FRESH_STAGE/libucl_rules.so ENGINE
```

Tiếp theo cần xác minh nhánh kết thúc90/120phút thực sự tiêu thụ RuleInput, các cờ hiệp phụ/penalty, nối canonical session của engine với kế hoạch đã lưu, xử lý restart/trampoline/lifecycle, rồi mới đưa provider thật vào Bridge. Chưa chạy điện thoại, chưa bảo đảm không crash, chưa có bản FULL để bàn giao. Không chép engine hoặc protected bundle vào repo.
