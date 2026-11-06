YÊU CẦU HIỆN HÀNH: người dùng chốt lại knockout MỘT TRẬN, có hiệp phụ và penalty, không lượt về hoặc ô tổng tỷ số. Store tạo mùa mới mặc định1; league phase36đội/8lượt.167trận toàn giải, đường vô địch12/13trận. Các nghiên cứu hai lượt và ô tổng bên dưới là lịch sử, không là yêu cầu hiện hành. Test toàn mùa và cấu hình một lượt v25 đã qua; native event entry vẫn chưa nối hoàn chỉnh, chưa có FULL bàn giao.

Cập nhật rc19: chạy hàm _knockout_event v25 xác nhận một lượt bật YES/YES, nhánh two_legs ở R16/QF/SF đặt NO/NO. EventRules mới phân biệt lượt đi/lượt về/chung kết; lượt về yêu cầu xác nhận provider tổng tỷ số trước khi xuất YES/YES. 42ca một lượt +28ca hai lượt qua; chưa nối entry và chưa FULL. Chi tiết source/repair-full8-rc19-event-extra-time.

Cập nhật rc18 theo ảnh tham khảo: cần tỷ số trận + ôtổnghai lượt cập nhật live. Đã chạy native publicationblock6ba04ac..6ba05bc với ngữcảnhregisterđược cấp: ghi riêng current tại61dc/61e0, total61f0/61f4 vàflag61ec.25tổ hợp qua; chưa chạyoutergates hoặcpixelHUD/điện thoại, chưaFULL. Xem source/repair-full8-rc18-aggregate-scoreboard.

Cập nhật rc17: Bridge trảcachedstartcũng kiểm tra lại frozenaggregateplan và gọi provider nạp nativeRAM; thêm cleanup đúngsession khi finish. Controller định tuyến categorytrống nhưgatewaygốc, và chặn matchstart/chuẩn bị modekhác khiUCLpending. TestactualPythonAPIcode/Controller qua; chưa cài nativehook, chưa chứng minh nhánh90/120phút và chưaFULL. Xem source/repair-full8-rc17-session-lifecycle.

Cập nhật rc16: tìm thấy và chạy thử nativeaggregatecomparator0x6cacc80→0x6cacb24: cộng RuleInputcarry12c/12e khi cờ12a bật;60ca qua. Thư viện ARM64prototype nạp config đã build và test với getterđội native thật; chưa cài vào runtime. Chưa xác minh nhánh hết giờ và canonicalgamebinding, do đó chưa bỏgate và chưa cóFULL. Xem source/repair-full8-rc16-native-aggregate/README-VI.md.

Cập nhật rc15, yêu cầu mới nhất: KHÔI PHỤC knockout hai lượt từ play-off đến bán kết, chung kết một trận.189trận toàn giải; đường vô địch15/17trận. Store tạo mùa mới mặc định2, không đổi format của save cũ. Bridge chuẩn bị trận lưu match_plan riêng trong pending session (carry đảo sân đúng), kiểm tra kế hoạch không đổi trước start; không cộng carry vào bàn của lượt về. Hàm at_whistle mô tả yêu cầu điều khiển engine, CHƯA là native hook. Provider engine vẫn chưa nối; không tuyên bố bản FULL chạy được.

Cập nhật rc14 theo yêu cầu mới: mùa mới qua Store/Controller dùng knockout một lượt, hòa thì hiệp phụ và luân lưu. League phase36đội/8lượt giữ nguyên.167trận toàn giải, đường vô địch12hoặc13trận. Mùa cũ có luật hai lượt được giữ riêng, không tự đổi save đang chơi. Đã kiểm tra toàn mùa trên8bộ lịch, decoder bàn hiệp phụ/luân lưu, và sửa lịch sử native ghi WIN/LOSE đúng theo penalty thay vì DRAW. Chưa nối cấu hình hiệp phụ/penalty native; không mặc nhiên coi việc bỏ lượt về là game đã bật luật mới.

Cập nhật rc13: stage entry mới đã nối roster Dortmund22 qua JSON editor/API ARM64 sẵn có, scope122. Host chạy thư viện RC7 thật với dịch vụ engine giả lập ở biên:22ID/số áo/đội hình đúng, scope125 không đổi so với baseline, rời122 khôi phục nền, thiếu cầu thủ từ chối không ghi dở. Scope122 cũng áp Dortmund trong My League UEFA thường. DEX588lớp và Chromium/Controller SQLite stage2 đã qua; chưa có provider tổng tỷ số native, chưa giao FULL. Chi tiết source/repair-full8-rc13-ucl-roster.

> Cập nhật pool/launcher06/11/2026: theo yêu cầu mới, Ajax116 đã được thay bởi Como1907 ID4219, roster30slot. Kiểm tra dữ liệu v19.1 có CRC gốc:126/128/226/231 thiếu roster;131/132 đang dùng cho Y17. Pool hiện tại loại tất cả các ID đó và không trùng classic_teams/Y08/Y17. Có8bộ lịch mới36đội, ITA7đội,8lượt144trận; test độc lập đã qua. Xem native_pool.json và test_ucl_pool.py.

Launcher/Dex/bootstrap đã có source và stage riêng ở source/repair-full8-rc11-ucl-entry. Kiểm tra DEX588lớp chỉ đổi LauncherWeb; Chromium dùng launcher script thật + hostAndroid giả lập + Controller SQLite: Como, bảng36dòng, đủ8lượt ×18trận và resume/leave đều qua. Chưa áp stage vào payload đang quảng bá; chưa có FULL hoàn thiện. Đọc README-VI ở source11 cho điểm chưa nối.

> Tiến độ adapter06/11/2026: đã viết ucl_lp_bridge/view/controller/install. Adapter dùng riêng globals của các hàm Python My League có sẵn, tách metadata/season/receipt UCL trong cùng transaction. Kiểm tra host thực thi mã hàm prepare/start/info/finish/get_schedule/enter_view từ my_league.pyc đúngSHA74711ac3d97a5b96cb07d2204336ca1b3c1f1626062eac57c356f2b6eeca60ca, với dịch vụ dữ liệu giả lập có kiểm soát (không thực thi module top-level, không chạy engine). Bộ test đi đủ8lượt dữ liệu thử tớiR16, bảng36dòng, không báo hết mùa sauLP, giữ nguyên save/special squad/points MyLeague thường, kiểm tra rollback và replay. Chi tiết host-native-bridge-report.json.

Gateway routing/controller có test host riêng; CHƯA cài vào bootstrap hoặc DEX/launcher của FULL đang phát hành. Chưa có provider điều khiển hiệp phụ theo tổng tỷ số, nối scorer/assist/CPU-roster, UI lựa chọn thật, WorldCup và lọc EventAI. Provider vắng mặt bị chặn trước lượt về/chung kết; controller không cho kích hoạt mùa mới khi chưa đủ provider. Không gửi bản này như FULL hoàn thiện. Không yêu cầu người dùng biết/càiADB để tiếp tục viết phần còn lại.

> Cập nhật kết quả native06/11/2026: thêm ucl_lp_result.py đọc trường score_1st/score_2nd/score_ex1st/score_ex2nd, score_pk và match_result.game_id/pk_flag theo v19.1. Store.finish_native dùng cùng transaction/receipt với finish. Từ chối hiệp phụ khi tổng tỷ số chưa hòa, các kết quả bỏ trận/bất thường chưa có policy, và ID session mâu thuẫn. Sửa bộ kiểm tra penalty để chấp nhận1-0/2-0 hợp lệ, từ chối5-2 vốn đã kết thúc sớm hơn. Test native packet, rollback và replay đều qua trên host. Chưa cài hook command hay cung cấp đường cho engine bật hiệp phụ theo tổng tỷ số.

> Cập nhật06/11/2026: mô tả face19018 bên dưới là lịch sử của ứng viên ĐÃ THU HỒI. Xem source/repair-full8-rc10-face-detail/README-VI.md cho WIP19019. Không cài19018.

UCL bổ sung ledger vua phá lưới/kiến tạo tách theo mùa: lưu cùng transaction với receipt, xác nhận roster gốc, xử lý phản lưới, ID lớn, rollback và chống cộng trùng sau restart. test_ucl_stats.py đã chạy host. Chưa có bộ giải mã packet native, UI, hay gán scorer CPU cho đủ toàn giải; leaderboard trả coverage rõ ràng khi thiếu. Đây vẫn chưa phải tính năng UCL đã tích hợp.

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
