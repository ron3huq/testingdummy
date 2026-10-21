# Native hotfix v5 — tên/logo, cầu thủ và Asia-Pacific League8 đội

Nền v4.1 đã được người dùng xác nhận vào được trận Bayern. **V5 mới kiểm tra trên máy chủ và giả lập thành phần ARM64; chưa thử trên điện thoại.** Kiểm tra native dùng DB tổng hợp và accessor/tra cứu gốc; bài gateway dùng bản sao seed DB và cầu nối native giả lập. Logo đã kiểm tra đường chọn biểu tượng gốc, chưa kiểm tra render/cache texture thực tế.

## Cài bằng MT Manager

1. Buộc dừng game, sao lưu bộ sáu file tools đang hoạt động và save/gateway.
2. Giải nén ZIP. Chép đè **đủ sáu file** trong `install/work/tools/` vào nơi bạn đã cài v4.1: `73efootball 资源` → `files/embedded-gateway/work/tools`. Không chép sang Android/data.
3. Sáu file: `gateway_runtime.py`, `select_team_runtime.py`, `libselect_team.so`, `myleague_realism.py`, `myleague_worlds.py`, `myleague_custom.json`. Hash bảo vệ cấu hình đã biên dịch, không thay JSON riêng.
4. Mở lại game. `select-team-status.json`: `version: native-hotfix-v5`, `state: HOOK_ACTIVE`. `myleague-realism-status.json`: `state: INSTALLED`, cùng version.
5. Kiểm tra `presentation_error: null` để biết cả hook logo Ajax và tên/logo giải đã cài được. Đây chưa phải bằng chứng logo hiển thị đúng. Bayern khi chuẩn bị trận cần `native_team_results["127"]: 1`.
6. Để dùng danh sách giải mới và lịch21 vòng: vào đổi/chọn đội, chọn **Asia-Pacific League ở vị trí Danish League cũ** rồi tạo mùa mới bằng thao tác xác nhận của game. Không xóa DB/save. Mùa đang chơi giữ snapshot cũ, không tự đổi Lyon hay12 đội giữa mùa.

Để kiểm tra nâng cấp, mở Select Team, chọn Asia-Pacific League: phải có đúng8 CLB bên dưới. Mở lịch mùa mới: vòng cuối là21. Thử trận Bayern, đối chiếu Musiala giữa/Olise phải/Díaz trái, sau đó mở chi tiết thẻ Akliouche và Doué. Nếu có lỗi, gửi `select-team-status.json`, `myleague-native-error.json` nếu xuất hiện và bước gặp lỗi.

## Giải đấu theo yêu cầu cuối cùng

| Vị trí gốc / ID | Tên mới | Logo từ engine |
|---|---|---|
| Ligue1 /122 | UEFA Champions League | UEFA / nationalEurope |
| Belgian League /566 | AFC Nation League | AFC / nationalAsia |
| Liga Portugal /128 | World Super League | CONMEBOL / nationalLatinAmerica |
| Danish League /549 | Asia-Pacific League | CONCACAF / nationalNorthAmerica |
| Eredivisie /125 | Eredivisie, khôi phục18 CLB Hà Lan | Giữ đường logo gốc |

**Bỏ cấu hình Asia-Pacific18 đội ở Eredivisie.** Asia-Pacific mới dùng Danish League549,8 CLB, vòng tròn3 lượt:21 vòng,84 trận,21 trận mỗi đội,10/11 trận sân nhà. Lịch bốc ngẫu nhiên một lần và lưu theo mùa. Không sửa kết quả đã chốt.

| CLB | Viết tắt | Nhóm |
|---|---|---|
| Al Nassr | NSR | Top1 |
| Al Hilal | HIL | Top1 |
| Inter Miami | MIA | Top2 |
| Santos | SAN | Top2 |
| Los Angeles FC | LAFC | Còn lại |
| Vissel Kobe | VIS | Còn lại |
| Gamba Osaka | GAM | Còn lại |
| Flamengo | FLA | Còn lại |

Giữ LAFC4 chữ theo xác nhận của bạn. Dùng roster thật có trong nguồn, không chuyển Lewandowski/Benzema/Mitrovic để tạo tên trên bảng ghi bàn. Ưu tiên ghi bàn cũ chỉ áp dụng khi cầu thủ thực sự thuộc roster. Chuyển nhượng Bento về AjaxE từ bản trước được giữ; yêu cầu mới không có chuyển nhượng cầu thủ khác.

## Tên CLB và Bayern

Chelsea/CHE, Arsenal/ARS, Manchester City/MCI, Tottenham/TOT, Real Madrid/RMA, Atletico Madrid/ATM, Juventus/JUV, Bayern Munich/BAY, Barcelona/BAR. Ligue1 dùng **Borussia Dortmund126/BVB thay Lyon181** ở mùa mới. AjaxE116 vẫn dùng logo Lyon như bản trước.

Bayern giữ22 ID base đã chạy được ở v4.1, cùng11 cầu thủ chính. Xoay ba ô tấn công thành **Olise ở ô7/cánh phải; Díaz ô8/cánh trái; Musiala ô9/giữa**, Kane đá cắm. Không đưa lại ID59835 gây lỗi, không dùng đội hình CPU inline. Đã kiểm tra getter roster gốc đọc đúng thứ tự mới; cần đối chiếu hình đội hình trên máy bạn.

Tỷ lệ CPU UEFA Champions League giữ85% thắng trước nhóm3 và95% trước nhóm4 cho nhóm1/2, cả sân nhà/khách. Dortmund thay Lyon trong nhóm4. Đây là xác suất cho nhiều trận mô phỏng; không điều khiển kết quả trận bạn đá trực tiếp.

## Chỉ số và kỹ năng

Đã cập nhật Akliouche106786040464076 và Doué106746580456800 theo các chỉ số mới; Doué bỏ Double Touch, thêm Scissor Feint. Giữ thay đổi Card ID cũ, gồm Dembélé88039313485858 bỏ Chop Turn/thêm Tap Trick. Áp dụng ở LOGIN/list/detail và tham số START sau lớp learned skills; ô learned bị bỏ được đặt marker74, không dịch các ô còn lại.

Các Base được cập nhật theo danh sách mới: Mbappé, Yamal, Nuno Mendes, Haaland, Bruno Fernandes, De Bruyne, Enzo, Bellingham, Güler, Messi, Kane, Raphinha, Olise, Vinicius, Rodri. Giữ kỹ năng cũ trừ khi có yêu cầu bỏ rõ ràng. Bổ sung Momentum Dribbling cho đủ19 tên đã yêu cầu, dùng ID base thực được đối chiếu đủ64 bit; João Félix có cả biến thể CLB và tuyển Bồ Đào Nha.

Hậu vệ là CB/LB/RB theo vị trí chính trong nguồn; không tính GK/DMF. Hậu vệ của18 CLB Ligue1 mới được +4 Defensive Awareness/Engagement/Tackling/Aggression. Hậu vệ6 CLB Arsenal/PSG/Barcelona/Real/City/Bayern được thêm Interception, Track Back. Tiền vệ DMF/CMF/LMF/RMF/AMF của6 CLB này: mỗi chỉ số Low/Lofted Pass <84 được +6; đúng84 thì không cộng. Giới hạn99; chỉ số riêng bạn yêu cầu có ưu tiên cuối (ví dụ Tackling Nuno92 và Rodri94).

**Không cộng dồn:** giữ mốc gốc riêng cho từng ID/thông số trong mỗi tiến trình, sau đó ghi cùng một giá trị đích. Không ghi các mốc/giá trị này vào save. Native dùng khóa đồng bộ cho lần lấy mốc đầu; Python dùng cùng nguyên tắc. Khởi động lại với dữ liệu gốc tính lại một lần. Đã kiểm tra220 cầu thủ/790 quy tắc, ngưỡng83/84 và trần99 qua nhiều lần tra cứu.

**Phần chưa áp dụng: Power Tackle.** Dữ liệu thẻ xác minh Track Back93, Interception106, Visionary118, Game Changing117, và Long-Reach Tackle125. Long Range Tackle trong yêu cầu được áp dụng cho Nuno qua Long-Reach Tackle125. Chưa xác minh được một flag riêng của Power Tackle; không dùng nhầm125 hay learned ID74 (marker rỗng) cho kỹ năng đó. Vì vậy phần Power Tackle của Nuno và hàng thủ lớn còn chờ mã đúng.

Tóc và áo dài từ yêu cầu cũ vẫn chưa áp dụng vì chưa xác minh trường riêng; bản này không tuyên bố đã sửa ngoại hình. Không thay dt200/CPK, APK, manifest hay toàn bộ PlayerAppearance.

## Kiểm tra đi kèm

- Native ARM64: resolver/XOR ID thật trên record tổng hợp, getter/setter147 tham số, preflight roster,22 cầu thủ Bayern,21 tên CLB/viết tắt,220 cầu thủ điều chỉnh, tính lặp ổn định; từ chối dữ liệu thiếu.
- Menu native:5 quy tắc, Danish12→8, Eredivisie trở lại18 đội Hà Lan; cấp phát/giải phóng engine và destructor; sửa kích thước mảng đếm theo đủ số quy tắc.
- Presentation: detour/trampoline thật, FString dùng allocator engine, giữ X8 và tham số style,4 tên giải và4 nhánh biểu tượng liên đoàn; Eredivisie125 đi đường gốc.
- Gateway:19 Card ID qua handler thật; cả8 đội Asia-Pacific chọn/tiếp tục/chuẩn bị vòng1/vòng21;84 trận và tính hợp lệ sự kiện bàn thắng/kiến tạo. Không có bài này chạy trên điện thoại.
- Hồi quy: giữ lịch/kết quả10 vòng cũ, active match, inventory và DB nguồn; ranking receipt idempotent.576 biên và40.000 trận mô phỏng giữ xác suất85/95.

Khôi phục bằng bộ sáu file v4.1 đã sao lưu, sau khi buộc dừng game. Khôi phục code không hoàn tác lịch mùa đã tạo; giữ save hiện có hoặc dùng backup cá nhân phù hợp.
