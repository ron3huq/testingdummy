# Bàn giao: thêm UCL league phase vào My League của APK73

Ngày bàn giao: 05/11/2026, giờ Việt Nam.

Đây là hướng dẫn cho tài khoản/phiên ChatGPT tiếp quản. **UCL chưa được tích hợp trong FULL-8 RC8.** Không được hiểu báo cáo nghiên cứu hay tài liệu bàn giao là một tính năng đã chạy trên điện thoại.

## 1. Sứ mệnh và phạm vi

Người dùng muốn áp dụng ý tưởng/code UCL trong bản v23 vào **My League của dự án APK73 hiện tại**, nhưng chuyển sang **thể thức league phase mới**, sau đó vào knockout. Làm tính năng thật: vào được từ giao diện, đá được trận, nhận đúng kết quả, lưu/mở lại được và tiếp tục đúng vòng.

Giữ nguyên nền **FULL-7**. Các FULL-8 là bản tích lũy trên nền này. Người dùng đã hủy chuyển sang FULL-6/efootxi. Không đổi nền, không thay engine bằng thư viện PES2021/v23.

Làm trên nhánh và bản FULL mới; không sửa đè bản đã phát hành. Không thay tất cả các mùa My League đang tồn tại thành UCL, không tự chuyển lịch sử mùa đang chơi sang 36 đội.

Người dùng chưa chốt mùa điều lệ UEFA cụ thể, danh sách 36 đội hay cách lập pots. Các mặc định đề xuất bên dưới là lựa chọn kỹ thuật, **không phải những lựa chọn người dùng đã xác nhận riêng**. Có thể tiến hành với mặc định hợp lý và ghi rõ, không cần dừng xin phép từng bước thông thường.

## 2. Nền phải tiếp quản chính xác

Repo: https://github.com/ron3huq/testingdummy

**Bản mới nhất được bàn giao: FULL-8 RC8, resource_revision 19017.**

- Branch: 73-full8-rc8-manual-skin-lods-ui
- Commit cố định: 27cf2b7281f0f3651b30a1c1b3fd30835227b913
- Tree: fe04a6f2581dba52b95fdc7bd34e1c0db5449b0a
- Source ZIP: https://github.com/ron3huq/testingdummy/archive/27cf2b7281f0f3651b30a1c1b3fd30835227b913.zip
- Workflow: https://github.com/ron3huq/testingdummy/actions/runs/41960571794
- **FULL thực tế**: https://github.com/ron3huq/testingdummy/actions/runs/41960571794/artifacts/13384553393
- Artifact: FULL8-RC8-complete-APK73, 630.712.705 byte.
- SHA256 artifact: 973ecb6f873694aaf4b9b6f7abb0c533d5edfe611ce07587388739cd874241a7
- Link artifact cần đăng nhập GitHub; hết hạn 12/11/2026 lúc 10:19:24 giờ Việt Nam.
- Inventory SHA256: 6c2963941fc9a279c418dbcd1c2d9b4ebe018e5289f79e7166bef718b504355e
- classes5.dex SHA256: dba92ec98a87a88b034668b425f122f0cc29dd2bb84d1a8344ae8138f1685801
- 1.494 file trong FULL, 319 file runtime được kiểm tra.

**Source ZIP của GitHub khác gói FULL.** Source checkout chứa đầu vào và các bước dựng; phải chạy pipeline để tái tạo FULL. Không gửi source ZIP rồi gọi đó là FULL đã dựng. Artifact FULL gồm assets/ và classes5.dex; đây là payload cho APK73, không phải APK đã ký.

FULL-7 gốc, dùng đối chiếu khi cần:
https://github.com/ron3huq/testingdummy/archive/74a1cd8100c8ecd022af9f16ef1f9f98cffcfc96.zip

Tình trạng xác minh:

- Người dùng xác nhận RC7: Single Player, Transfer/vai trò/chỉ số và accessories đã hoạt động trên điện thoại.
- RC8 sửa thêm tự lùi khi nhả điều khiển và các vấn đề mặt/cổ/môi/LOD Ronaldo. RC8 đã dựng khớp checksum giữa workspace và GitHub, **chưa có xác nhận mới trên điện thoại**.
- Không nói mọi sửa của RC8 đã được kiểm chứng trên máy người dùng.
- Bản thử RC8 revision19016/run41959759477 đã được thay bằng revision19017 ở trên; không dùng nhầm artifact đầu.

## 3. Nếu không có workspace cũ

Tài khoản khác thường không có cùng máy, thư mục, file đính kèm, công cụ hay kết nối GitHub. Kiểm tra thực tế trước; không khẳng định đã thấy hoặc sửa các file chỉ vì tài liệu liệt kê đường dẫn.

Ưu tiên lấy commit cố định ở mục2 và nguồn release. Không bắt người dùng tải lại gói face/source cũ qua link workspace: người dùng không tải được kiểu link đó.

Nếu tài khoản Plus không có terminal/môi trường thực thi và công cụ cần thiết, phải nói rõ giới hạn và thiết lập môi trường làm việc thích hợp. Không giả vờ đã build/đẩy GitHub/kiểm thử. Không chia sẻ token, cookie hay thông tin đăng nhập giữa tài khoản.

Nếu workspace còn, các đường dẫn hữu ích:

~~~
/workspace/work/full8-rc8/payload
/workspace/work/full8-rc8/ci
/workspace/work/full8-rc8/progress.json
/workspace/work/full8-rc7/v23-research
/workspace/work/full8-rc7/remote_v23.py
/workspace/.setup-testingdummy/venv/bin/python
~~~

Trong FULL đã dựng, runtime chủ yếu ở:

~~~
assets/gateway-release/work/tools/
assets/gateway-release/livedata/
assets/gateway-release/ui6-runtime-manifest.json
assets/gateway-release/release-manifest.json
assets/launcher/
source/repair-full8-rc*/
validation/
payload-inventory.json
classes5.dex
~~~

## 4. Nghiên cứu UCL v23 đã làm được gì

Nguồn:
https://github.com/ron3huq/testingdummy/releases/tag/releasee

Hai phần đã nghiên cứu:

~~~
73efootball-V23.1.part1.rar
73efootball-V23.1.part2.rar
~~~

Báo cáo đầy đủ, có danh sách 41 đội ưu tiên và ID:
https://github.com/ron3huq/testingdummy/blob/27cf2b7281f0f3651b30a1c1b3fd30835227b913/source/repair-full8-rc7/RESEARCH-UCL-V23.1.md

Đã đọc implementation/nhánh điều kiện của các module:

~~~
cup_entry
ucl_mode
ucl_service
ucl_group_bridge
cup16_mode
cup16_service
e112_cup_runtime_compat
ml_event
ml_event_entry
ml_event_match
event_availability
~~~

Nếu workspace còn, có các file .decoded.dis và .decoded.pyc trong v23-research. **Đây là bytecode/disassembly, không phải bộ source .py hoàn chỉnh.** Không tự nhận đã có source gốc. Không thực thi mù quáng bundle nghiên cứu hoặc chép toàn bộ protected runtime sang game đích.

Cách lấy nguồn trước đây: đọc RAR header và central directory APK bằng HTTP Range, lấy đúng entry cần nghiên cứu, kiểm tra kích thước và CRC ZIP. remote_v23.py là công cụ địa phương đã dùng; nó có giả định về layout/method của hai volume này, không phải bộ giải nén RAR tổng quát. Nếu không có các file prefix/index cần thiết, phải dựng lại index hoặc dùng công cụ giải nén chuẩn. Không tái sử dụng offset cho một release khác.

### Những điểm đã thấy trong code v23.1

- **32 đội, 8 bảng x4, vòng bảng một lượt**; không phải league phase36đội.
- Người chơi ở bảngA/index0, mặc định pot2.
- Ba trận vòng bảng của người chơi; các trận khác mô phỏng offline.
- Xếp bảng: điểm, hiệu số, bàn thắng, teamID tăng dần; không thấy đối đầu.
- Code xét đi tiếp bằng top2. Nội dung event còn ghi “ít nhất5điểm”: **mô tả và code không nhất quán**.
- R16 → QF → SF → FINAL, **mỗi vòng một trận**, khác thể thức UCL mới.
- R16 ghép nhất bảng với nhì bảng kế tiếp theo vòng; các vòng sau theo nhánh.
- Event1120006 là group,1120007 là knockout;1120005 cũ không còn chiếu ra danh sách mới. Phải kiểm tra xung đột ID trên nền73 trước khi dùng.
- Pool ưu tiên41CLB, chọn31đối thủ hợp lệ cộng đội người chơi; có bước remap native châu Âu. Không có danh sách32đội cố định cho mọi lần vào.
- Lập pots/giảm trùng quốc gia bằng tối đa400lần thử, lấy phương án ít xung đột nhất. Đây là ràng buộc mềm, không phải đầy đủ luật UEFA.
- Rating mô phỏng lấy trung bình OVR11người đầu, fallback80; không phải hệ số CLB UEFA.
- Có lưu state/receipt trong SQLite, resume event, chống cộng kết quả trùng, giữ pending khi chưa có kết quả hợp lệ.
- Có bản ghi vô địch trong e112_cup16_trophies; reward lists đang rỗng. Không tự hứa có thưởng GP/coin.
- Có7tùy chọn CPU từ VERYEASY đến LEGEND, mặc định NORMAL. Field cấu hình không chứng minh độ khó thực tế đã đến engine.

### Bridge My League của v23 — điểm nguy hiểm nhất khi port

Trang group native UserCompe bị trống khi dùng EventCompe. v23 mượn bảng/lịch My League: sao lưu mùa thật, mở mùa4đội/3lượt, chuyển6kết quả bảng về UCL rồi khôi phục mùa thật; có release/restore.

**Không chép bridge4đội này rồi đổi số thành36.** Phải kiểm tra schema, giới hạn UI/native, transaction, crash recovery và những wrapper My League hiện có. Tuyệt đối không làm mất mùa thật hoặc ghi kết quả UCL vào lịch sử giải khác.

## 5. Thể thức mới cần triển khai

Mốc thiết kế đề xuất là UCL36đội từ2024/25 trở đi. Trước khi gọi là “đúng luật UEFA”, chọn và ghi rõ một mùa điều lệ cụ thể, đối chiếu tài liệu chính thức tại https://documents.uefa.com/ và https://www.uefa.com/uefachampionsleague/ .

Không dùng tóm tắt này thay cho phụ lục bốc thăm/knockout chính thức của mùa đã chọn; các quy định lợi thế sân nhà có thể thay đổi giữa các mùa.

### League phase

- 36đội, một bảng xếp hạng chung.
- 4pots,9đội/pot; mỗi đội gặp2đối thủ từ mỗi pot, gồm cả pot của chính mình.
- Với mỗi pot: một trận sân nhà, một trận sân khách. Tổng8đối thủ khác nhau,4nhà/4khách.
- Tám lượt, mỗi lượt18trận; tổng144trận.
- Không gặp đội cùng liên đoàn theo luật chuẩn; tối đa2đối thủ từ cùng một liên đoàn khác. Phải dùng liên đoàn CLB, không nhầm quốc tịch cầu thủ hoặc quốc gia đội tuyển.
- Thắng3, hòa1, thua0; league phase không có hiệp phụ/penalty.
- Top1–8 vào thẳng R16. Hạng9–24 đá playoff. Hạng25–36 bị loại; không chuyển sang Europa League theo thể thức mới này.

Không gọi lịch vòng tròn36đội rồi cắt8lượt. myleague_worlds.schedule hiện phục vụ lịch league thông thường; lịch8lượt có ràng buộc pots/home-away/quốc gia cần thuật toán riêng.

Nếu dùng OVR để lập pots vì chưa có dữ liệu hệ số UEFA, phải gọi đó là **pots theo sức mạnh trong game**, không giả là hệ số UEFA thật. Không tự giữ đội người chơi ở pot2 chỉ vì v23 làm vậy.

Khi pool không đủ hoặc không thỏa ràng buộc, trả lỗi/đổi pool hợp lệ có giải thích; không lặng lẽ cho trùng đối thủ hoặc phá luật quốc gia để solver “qua”.

### Xếp hạng

Ngoài điểm, bộ luật chuẩn cần kiểm tra các tiêu chí: hiệu số, bàn thắng, bàn thắng sân khách, số trận thắng, số trận thắng sân khách, tổng điểm/hiệu số/bàn thắng của các đối thủ đã gặp, kỷ luật và hệ số CLB theo đúng điều lệ mùa chọn.

Không dùng đối đầu làm tiêu chí mặc định của league phase. Không dùng teamID để vượt qua các tiêu chí chính thức. Phải giữ kết quả của toàn bộ144trận để tính lại các tiêu chí sức mạnh đối thủ khi kết thúc lượt8.

Phân biệt: bàn thắng sân khách có thể là tiêu chí xếp bảng, nhưng **không có luật bàn thắng sân khách để phân thắng bại cặp knockout**.

### Playoff và knockout

- Playoff: hạng9–16 được xếp hạt giống, gặp hạng17–24 theo nhóm thứ hạng và sơ đồ UEFA, hai lượt.
- Các nhóm playoff thường là9/10 với23/24,11/12 với21/22,13/14 với19/20,15/16 với17/18; phải kiểm tra phụ lục mùa chọn trước khi đóng cứng.
- R16 gồm top8 và8đội thắng playoff, không có đội trùng.
- R16/QF/SF hai lượt; FINAL một trận.
- Không tự bốc ngẫu nhiên hoàn toàn mỗi vòng. Phải duy trì nhánh đấu và seed path theo thể thức đã chọn.
- Ghi rõ luật đội nào đá lượt về sân nhà cho từng vòng theo điều lệ mùa chọn.
- Tổng tỷ số hòa sau lượt về mới có hiệp phụ rồi luân lưu. Không cộng một kết quả luân lưu giả khi native không trả dữ liệu hợp lệ.

Số trận để kiểm tra:

- Toàn giải:144 league phase +16 playoff +16 R16 +8 QF +4 SF +1 FINAL = **189trận**.
- CLB vào thẳng R16 rồi vô địch:15trận.
- CLB đi từ playoff rồi vô địch:17trận.

Không giữ mô tả “tối đa7trận” của v23 cho giải mới.

## 6. Đường tích hợp trên nền73 hiện tại

Đọc trước các file trong assets/gateway-release/work/tools:

~~~
myleague_73.py
myleague_worlds.py
myleague_realism.py
myleague_balance.py
myleague_editor_runtime.py
myleague_team_snapshot.py
myleague_condition.py
myleague_custom.json
select_team_runtime.py
transfer_final_runtime.py
cached_lookup_runtime.py
mod_startup.py
private_bundles.py
~~~

Các API mà myleague_73.install hiện yêu cầu ở module my_league:

~~~
fixtures, cpu_score, _cpu_round_stats,
prepare, start, info, _opponent_squad, current, state
~~~

Nó còn bọc ml_super_league.start_season, ziru_data registry/rosters và các đường gate opponent/start. Module my_league/ziru_data có thể nằm trong bundle Python của app, không nhất thiết là file .py cạnh tools. Đọc đúng module đang được import; không kết luận thiếu code chỉ vì rg không thấy file .py.

myleague_73.scoped kiểm tra competition_id, tập đội và schedule_v2. Nếu tự đưa36đội vào competition122 hiện có, wrapper có thể coi sai scope hoặc thay lịch giải khác. Phải thiết kế discriminator UCL rõ ràng và xem thứ tự cài wrapper; nhánh không thuộc UCL phải đi qua đúng handler cũ.

**Không nhầm namespace ID:** competition122 hiện dùng cho UEFA My League; team122 là Lazio trong danh mục nghiên cứu. Event1120006, competition122, team122 và full playerID là các loại khóa khác nhau.

Lần theo toàn tuyến:

~~~
Nút mở thực tế
→ tạo/chọn mùa UCL
→ state SQLite
→ league table / fixture projection
→ CMD_GET_VSCOM_OPPONENT
→ CMD_START_GAME và cấu hình trận
→ native team/gameplan/player records
→ trận đấu thật
→ handler kết quả thực tế của nền73
→ receipt chống gửi trùng
→ cập nhật vòng/bảng/nhánh
→ tắt/mở app rồi resume
~~~

Tên CMD kết thúc trận phải xác định từ dispatcher thực tế; không đoán một endpoint tên END_GAME rồi coi như đã tích hợp.

Đối thủ phải có roster/gameplan native hợp lệ:11–40full playerIDs phù hợp API, đội hình xuất phát, dự bị, vị trí, vai trò và kit có sẵn. Đổi tên/crest trong JSON không đủ để tạo một đội thật.

### Giao diện thực tế

Launcher hiện dùng WebView:

~~~
assets/launcher/index.html
assets/launcher/launcher.js
assets/launcher/editor-private.js
LauncherWeb → PrivateTools.open → màn hình công cụ
~~~

Trước đây thêm attach() vào lớp native không được gọi đã khiến tính năng không có nút mở. Phải nối từ launcher/My League đang dùng và kiểm tra đường mở thật. Không chỉ kiểm tra lớp có trong DEX.

Ưu tiên UCL như một lựa chọn mùa/chế độ trong luồng My League, giữ các mùa league thường. Nếu bảng native không hỗ trợ36đội/8lượt, phải chứng minh giới hạn rồi thiết kế projection/UI thích hợp; có thể dùng trang WebView cho bảng/nhánh, nhưng trận thật vẫn phải đi đúng đường native. Không làm một trang bảng giả tách rời tiến trình trận.

## 7. Kiến trúc và lưu dữ liệu đề xuất

Đây là đề xuất mới, chưa phải module tồn tại sẵn:

~~~
ucl_lp_rules.py          # cấu hình điều lệ theo mùa
ucl_lp_draw.py           # pots, đối thủ, home/away,8lượt
ucl_lp_mode.py           # state machine và tiến trình
ucl_lp_service.py        # gate/My League integration
ucl_lp_store.py          # transactions, migrations, receipts
ucl_lp_projection.py     # bảng, lịch, bracket, UI payload
~~~

Nên có các trạng thái rõ: DRAW_READY, LEAGUE_PHASE, PLAYOFFS, R16, QF, SF, FINAL, CHAMPION, ELIMINATED. Ghi rõ trạng thái nào cho phép đổi đội/reset/bắt đầu trận.

State tối thiểu:

- schema_version, season_uuid, ruleset_version, mode marker.
- 36participants; phân biệt participant ID, team native ID, alias/kit donor, association, pot, strength/coefficient.
- Seed bốc thăm, toàn bộ lịch144trận và home/away.
- Kết quả từng trận, tình trạng pending/completed; không tính trận vừa START là đã đá xong.
- Vòng hiện tại, tie ID, lượt1/lượt2, tổng tỷ số, ET/penalty hợp lệ.
- Nhánh cố định và seed mapping.
- Match receipt/idempotency key; liên kết request/native session với đúng fixture.
- Snapshot/restore journal nếu thật sự cần mượn state My League.

Full playerIDs dùng chuỗi trong JSON/JS để tránh rủi ro precision với64bit; không cắt thành baseID để đối chiếu danh tính.

Mô phỏng17trận CPU còn lại trong một lượt chỉ khi trận thật của người chơi có kết quả hợp lệ, trong transaction phù hợp. Seed và kết quả mô phỏng được lưu; mở lại màn hình hay gửi lại request không được tạo tỷ số mới.

Không reset giải khi vào lại event/màn hình. Kill app, lỗi mạng và request gửi lại phải resume được. Dùng unique constraints cho receipts/fixtures; không chỉ dựa vào biến RAM để chống cộng hai lần.

Không khôi phục nguyên DB cũ đè lên mọi thay đổi mới sau khi đá UCL. Nếu phải mượn mùa, sao lưu đúng các record bị thay, có owner/session/version, journal và phát hiện xung đột. Cần đường khôi phục sau crash, thoát giữa trận, kết thúc giải và nâng schema. Backup cá nhân ở máy người dùng; không đóng gói vào FULL.

## 8. Những phần tuyệt đối không làm hỏng

### Transfer và My League balance

Giữ đội hình, vai trò gắn cầu thủ, chỉ số, skills, boosters, weakfoot, position và accessories đã hoạt động. Đảm bảo context competition của UCL tới native đúng để profile Transfer áp dụng như chủ đích; không dùng eventID thay competitionID.

Quy tắc người dùng: chỉ đúng cầu thủ đã chỉnh chỉ số được miễn cân bằng trong giải tương ứng; các cầu thủ chưa chỉnh vẫn cân bằng. Không tắt cân bằng toàn giải để làm một cầu thủ thay đổi. Không ép OVR hiển thị để giả vờ đã sửa stat.

Hai bài học native:

- Key DB có kind32 + padding32 không khởi tạo, rồi fullID64. Không so kind như64bit.
- Cached team mode2 có word đầu là cache index; không áp cách hiểu PlayerKey.kind=0 cho mọi record. Xác minh đủ hai word, pool và danh tính.

### Single Player

RC7 đã dùng đúng roster native thay roster lưu sai:

- Global Scene team getter:72c19dc;72c404c thuộc context khác.
- Pool accessor72f29c4, entry72f2ca8, key72f29e0, order72f2de0.
- Không đổi lại thành danh sách toàn bộ40.000cầu thủ.
- Giữ full ID, đội đang trên sân, thay người/đổi phía/pause/replay/trận mới.
- RC8 giữ native human cursor/controller policy thay việc ép3; phần tự lùi chưa được xác nhận lại trên điện thoại.

AI đồng đội chưa xác định được cấp độ riêng từ log hiện có. Global/event0 VERYEASY và getter có0lần gọi không phải bằng chứng mức AI đồng đội. Với UCL, phải lần theo độ khó từ cấu hình đến native match, không chỉ lưu field CPU.

### Face, tài nguyên và đăng nhập

Không sửa face trong nhiệm vụ UCL trừ khi cần chữa regression do chính thay đổi mới gây ra. Giữ:

~~~
Ronaldo2027: 89138556572074
Spider-Man V1: 106782819217056
Miles Morales: 88035555413452
~~~

Ronaldo hiện dùng nguồn Android MessipradeepV2 của người dùng, không tự đổi về V8/FULL6. Hai Ronaldo Vol9 đã hủy, không thêm lại.

Giữ login/resource fixes và các integrity guards. Network Error C_NAJM_0009 từng xuất hiện do chuỗi khởi tạo/checksum bị sai. Không bỏ require_ready, giả READY hoặc trả response login giả để né lỗi.

Các SHA nền RC8 để đối chiếu:

~~~
libsingle_player_live.so
eb5dc425760a5cfa1694d7c859b418db8ee4b64b0378a6751838d09c15c53063

libnoodle_hair.so
b3cc3f656446c5de1d97d5c60c483d5f0d63b5f12c80d4803d6071bf5e9a4e31

libtransfer_final.so
0d0d588b4305536d3dd3db14edbeb1d6965f1957178b6a8eeedc24a33052d403

libselect_team.so
674fca3a1293aa06a572124cce8e67ef3251f3c84d70d059bcf29f756df92ab6

libUE4.so của APK73 đã nghiên cứu
efd257d9e41b622d6ecb8f51f7b0a8ee8820113fd427c5572025df1c8eecc7b8
~~~

## 9. Cách dựng FULL — phải đọc trước khi sửa pipeline

Workflow tham chiếu:
https://github.com/ron3huq/testingdummy/blob/27cf2b7281f0f3651b30a1c1b3fd30835227b913/.github/workflows/build-full8-rc8.yml

Nó dựng tích lũy theo thứ tự:

~~~
.ci-full8-rc4/assemble.py
.ci-full8-rc5/assemble.py
.ci-full8-rc5-hf1/assemble.py
.ci-full8-rc6/assemble.py
.ci-full8-rc7/assemble.py
.ci-full8-rc8/assemble.py
~~~

Chạy trong checkout sạch của commit nền, với Java, curl và Python phù hợp. Venv dùng .ci-full8-rc5/venv, vì bước RC4 có xóa thư mục stage của chính nó. Không đặt venv ở .ci-full8-rc4.

Các dependency đang được workflow pin:

~~~
ziglang==0.13.0
cityhash==0.4.10
pyelftools==0.32
numpy==2.5.4
scipy==1.18.1
Pillow==13.0.0
etcpak==0.9.15
texture2ddecoder==1.0.6
~~~

Pipeline GitHub đã chạy thành công cả trên Python runner khác phiên bản host và khớp inventory; không cần tùy tiện đổi toolchain. Không đưa SciPy/solver host vào runtime Android nếu Android không có dependency đó.

Các assembler có pin input/output và điều kiện revision. **Không chạy ngược các bước cũ lên gói FULL RC8 đã dựng.** Hai cách hợp lệ:

1. Checkout sạch → dựng toàn bộ chain đến RC8 → xác minh baseline → áp dụng bước UCL mới.
2. Dùng đúng FULL RC8 đã dựng làm input cho một bước mới có pin baseline RC8; lấy build tooling/source từ repo nếu cần.

Đề xuất nhánh mới và source/repair-full8-rc9-ucl/. Đặt bước dựng mới sau RC8, kiểm tra inventory SHA nền trước khi sửa. Revision mới phải lớn hơn19017;19018 chỉ là số kế tiếp đề xuất, phải kiểm tra repo không có bản khác đã dùng.

Không sửa các source RC4–RC8 đã công bố để làm lệch khả năng tái tạo bản nền. Thêm bước mới với manifest/validation riêng.

Nếu cần native mới: compile từ C/assembly minh bạch, không upload ELF mù. Toolchain đã dùng AArch64 freestanding, PIC, fixed x18, không stack protector, không outline atomics, -O2 -g0 và max-page-size16384. Tránh native hook mới nếu API Python/My League đã đủ.

Nếu cần DEX: dùng DexTool.java ở source/repair-full8-rc4, overlay đúng smali rồi assemble theo thứ tự ổn định. Không thay cả DEX bằng một bản cũ làm mất các tính năng.

### Thứ tự refresh integrity

1. Hoàn tất tất cả runtime/resource/UI edits.
2. Tính native HOOK_SHA và resource hashes mới.
3. Cập nhật private_bundles.json nếu có resource mới.
4. Refresh các pin lồng trong noodle_bundle.json.appearance_files **sau cùng các dependency nó pin**, cùng appearance_overlay_sha256 nếu liên quan.
5. Refresh ui6-runtime-manifest.json và release-manifest.json.
6. Chạy validator khởi tạo và LOGIN guard thật, với ARM workers được mock trên host khi cần.
7. Tạo payload-inventory.json cuối cùng từ allowlist.
8. Dựng lại từ source trên GitHub và đối chiếu inventory.
9. Đóng gói đúng allowlist rồi cung cấp artifact FULL thật.

Các công cụ tham chiếu:

~~~
source/repair-full8-rc2-hf1/build_runtime_manifests.py
source/repair-full8-rc5-hf1/check_startup_integrity.py
source/repair-full8-rc5-hf1/verify_login_gate.py
source/repair-full8-rc8/finalize.py
source/repair-full8-rc8/check_payload.py
source/repair-full8-rc8/ci_assemble.py
~~~

finalize RC8 yêu cầu input RC7, không dùng nguyên file đó như finalizer của RC9. Viết bước mới phù hợp baseline.

Không đóng gói save/DB cá nhân, diagnostics/log riêng, backup người dùng, ZIP/RAR nghiên cứu, APK/video nguồn, __pycache__ hoặc .pyc sinh ra trên máy build. **assets/chaquopy/app.imy là thành phần gốc cần thiết của APK, không được xóa chỉ vì nó cũng là bundle.** Phân biệt nó với app.imy trích từ v23 phục vụ nghiên cứu, không được chép bundle v23 vào payload.

## 10. Kiểm tra nghiệm thu cần thiết

### Thuật toán và state

- 36đội hợp lệ,8lượt,18trận/lượt,144trận, mỗi đội8đối thủ khác nhau.
- Mỗi đội4nhà/4khách; mỗi pot2đối thủ, một nhà/một khách; ràng buộc liên đoàn.
- Test độc lập nhiều seed và pool không khả thi; không chỉ test chính helper bằng chính nó.
- Xếp hạng đúng khi có hòa nhiều tiêu chí và khi tổng điểm đối thủ thay đổi ở lượt cuối.
- Biên hạng8/9,16/17,24/25; đủ16đội vào R16.
- Mỗi cặp hai lượt giữ đúng home/away/tổng tỷ số; ET/penalty chỉ đúng tình huống.
- Nhánh playoff/R16/QF/SF/FINAL đúng điều lệ và không có đội trùng.
- 15/17trận của đội vô địch và189trận toàn giải theo cấu hình chuẩn.
- Request kết quả gửi trùng, gửi lại sau timeout, pending, kill/restart và resume.
- Hoàn tất giải/reset mới không làm sai mùa thường, Transfer hay lịch sử cũ.

### Tích hợp thật

- Nút mở xuất hiện từ giao diện người dùng đang dùng.
- League table36đội/lịch/bracket hiển thị đúng và lưu/mở lại được.
- Trận thật nạp đúng đối thủ, XI, bench, vị trí, vai trò, kit và full playerIDs.
- Kết quả native cập nhật đúng fixture, không phải JSON tự sửa điểm.
- Theo dõi cả hai lượt của knockout, thắng/thua/hòa, ET và shootout hợp lệ.
- Single Player đọc roster thực trong trận UCL; đổi người và nhả điều khiển không gây regression.
- Chỉ số/skill/booster/weakfoot/position đã chỉnh qua Transfer còn được áp dụng; cầu thủ chưa chỉnh vẫn cân bằng theo policy.
- Accessories đúng cầu thủ/trái/phải; không ảnh hưởng face/rig.
- Độ khó đi hết đường native, không chỉ field đã lưu.
- LOGIN và tài nguyên vẫn qua kiểm tra; checksum bị cố ý làm sai vẫn phải bị chặn.

### Cách báo kết quả

Tách rõ: đọc code; unit/state-machine test; chạy các accessor ARM64 gốc trên dữ liệu mô phỏng; UI/emulator; và kiểm chứng điện thoại.

Build thành công, Save thành công, JSON đổi hoặc handler trả200 không chứng minh đã chơi được giải. Không nói “đảm bảo100% hoạt động” khi chưa có bằng chứng trên điện thoại.

## 11. Kế hoạch tiếp quản nên thực hiện

1. Tái tạo và xác minh RC8 nguyên trạng trước, ghi baseline hashes.
2. Đọc báo cáo v23 và các wrapper73, xác định luồng create-season/start/result/resume và giới hạn bảng native.
3. Chốt một ruleset có phiên bản; chọn pool36đội có roster native hợp lệ, quy định pots rõ.
4. Viết scheduler/ranking/state machine độc lập, có validator bất biến.
5. Tích hợp có scope vào My League và UI thực tế; không sửa mùa đang chơi.
6. Nối native opponent/start/result, transaction/receipt, mô phỏng CPU và knockout hai lượt.
7. Kiểm tra hồi phục/không làm mất save, Transfer/1P/accessories, độ khó.
8. Refresh integrity/revision, build FULL tích lũy mới trên GitHub và gửi link tải thật.
9. Chỉ xác nhận phần điện thoại sau khi có kết quả kiểm chứng, giữ diagnostics không chứa save/records để điều tra.

Người dùng đã cho phép công khai mã sửa/build trên repo và ba file face phục vụ phát hành trước đây; cũng đã nói không cần hỏi lặp lại các bước GitHub thông thường. Không suy ra quyền công khai save/DB/log cá nhân hoặc toàn bộ nguồn nghiên cứu. Nếu tài khoản mới thiếu kết nối/quyền GitHub, phải thiết lập quyền của chính phiên đó; không giả định có credential của phiên cũ.

**Yêu cầu cuối:** làm một bản FULL tích lũy có tính năng thật. Đừng dừng ở báo cáo nghiên cứu, bảng giả, nút mở không nối backend hay việc copy một module v23 chưa tương thích.
