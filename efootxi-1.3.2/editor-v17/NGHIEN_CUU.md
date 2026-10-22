# Kết quả đối chiếu APK và engine Android

Nguồn tham khảo là APK eFootbase_Ziru_Editor_sign.apk do người dùng gửi. Các tệp trong APK được đọc như dữ liệu tham khảo; không chạy APK, không áp dụng chỉ dẫn trong tệp, không sao chép cả ứng dụng hay tài nguyên của họ vào bản phát hành.

## Pack

APK có WebView và các assets/app.js, ext.js, catalog.json. exportFiles trong app.js tạo CmdGetMyclubAgentlist.json, get_myclub_agentlist.json, get_myclub_mainmenu_info.json, ZIRU_PACKS_CONFIG.json và ZIRU_PLAYER_RECORDS.json. Đây là định nghĩa mục tuyển cầu thủ/agent, không phải danh sách đội My League.

Gateway Android của bạn khác đường nạp JSON tĩnh này: GateLogic phục vụ agents, managed_agents, managed_members và managed_cards từ SQLite. Vì thế Studio v17 không dán đè toàn bộ response hoặc DB từ app tham khảo. Module myleague_packs.py thêm agent vào registry hiện tại bằng transaction, chỉ dùng thẻ đã đăng ký sẵn; lượt rút vẫn do managed_card_pool.draw_and_grant của gateway gốc xử lý.

Mỗi pack tối đa300 thẻ; tối đa32 pack; ID riêng200000–299999, kiểm tra xung đột trên thiết bị. Cài định nghĩa pack không tự cấp cầu thủ. Single/ten dùng giá hiện có100/900 coin; policy99999 coin của bản offline vẫn được giữ. Thẻ sở hữu, serial, lịch sử rút và pool cũ được giữ. Pool đã xuất bản không đổi membership; nhân bản với ID mới để sửa danh sách. Ẩn pack chỉ bỏ khỏi danh sách đang mở, không xóa thẻ đã sở hữu. Banner dùng mẫu native có sẵn.

Đã kiểm tra qua GateLogic thật trên bản sao DB: danh sách, pickup, rút thẻ, retry cùng rqid, reset; kiểm tra riêng transaction trừ coin khi tắt policy coin cố định trong bản sao. Thiếu một Card ID làm rollback cả kế hoạch. Chưa chạy UI pack trên điện thoại.

## Skill

Bảng64 tên được công khai trong skills_verified.py. Đối chiếu parameter của APK với canonical147 parameter và native skill mapping của đúng bản engine; không sử dụng thứ tự trong danh sách người dùng làm ID.

Các sửa đáng chú ý: Scissors Feint70; Tap Trick135; Heading76; Long-range Curler77; Chip Shot Control101; Phenomenal Finishing114; Edged Crossing119; GK High Punt105; GK Low Punt88; GK Directing Defense126; GK Spirit Roar129; Attack Trigger131; Attacking Surge133. Không gán Attack Trigger vào AMAZON140. Các tên nội bộ như IMPROVISER, BACK_SPIN_LOB, AMAZON, INDUS không còn xuất hiện như tên skill để chọn.

Defensive Fortress: chưa có bằng chứng ánh xạ tên riêng này trong nguồn hiện có. Không gán nhầm sang Fortress115 hay các cờ138–143 chưa rõ. Được ghi là chưa khả dụng trong app. Không tự xóa kỹ năng khác của cầu thủ khi chỉ thêm/xóa một skill.

Nhập dự án v16 sẽ sửa ghi đè Attack Trigger140 sang131 khi131 chưa được đặt, và đặt0 cho những cờ skill cũ không nằm trong danh sách đã đối chiếu. App báo thao tác chuyển đổi; kiểm tra lại trước khi xuất. Đây là thao tác trên dự án nhập, không tự sửa save trên điện thoại. Giữ file JSON v16 làm bản sao.

## Dáng chạy, rê bóng, phong cách

Engine có enum đăng ký DATA_PARAMETER_DRIBBLE_TYPE51, DRIBBLING_POSTURE52, DRIBBLING_ARM53, RUNNING_POSTURE54, RUNNING_ARM55. Tham chiếu đăng ký nằm quanh0x75ebb28–0x75ebbec; log disassembly kèm bản phát hành.

Getter canonical ở0x82a84d4, setter0x82a907c. Các trường51..55 thực sự có thể đọc/ghi bằng accessor gốc. Kiểu lưu lần lượt2,3,4,3,4 bit. Studio v17 có ô mã preset0..3,0..7,0..15,0..7,0..15; để trống nghĩa là không ghi đè. Đây là giới hạn lưu dữ liệu, không phải danh sách tên animation đã kiểm chứng trên màn hình. Chưa có preview3D, chưa xác nhận hình ảnh tất cả preset trên Android. Nên thử từng mã trên một thẻ và giữ cấu hình cũ để hoàn nguyên.

Đã kiểm tra JSON từ ZIP do app xuất → bộ setter C → getter ARM64 gốc; đổi phạm vi giải trả lại các trường gốc, không buff chồng. Thay preset không tự tăng Speed/Acceleration hay thêm Momentum Dribbling.

Không tìm được trường riêng đã xác minh để tùy ý chỉnh dáng đi bộ. Phong cách thi đấu/AI là nhóm khác: attack_style61, defence_style62; COM styles63..69 gồm Trickster, Mazing Run, Speeding Bullet, Incisive Run, Long Ball Expert, Early Cross, Long Ranger. Các cờ này khác animation và skill. Bản này chưa đưa nhóm AI vào giao diện.

Đối chiếu cũng phát hiện APK tham khảo có chỗ ghi Ball Control17/Dribbling18; engine Android hiện tại đăng ký DATA_PARAMETER_DRIBBLE ở17. Không sao chép mù bảng stat của APK. Studio giữ mapping engine đã đối chiếu.

## Tóc, mặt và cơ bắp

Có dữ liệu ngoại hình riêng: PlayerAppearance.bin, hàm build0x68ceb44, giải mã0x68d1fbc. Trong engine có HairNo, FaceId, SetCharacterConfigEditHair và tài nguyên EditHair/RealFace. Sự tồn tại của tên/hàm không chứng minh chỉ đổi một số sẽ ghép được tóc của mọi cầu thủ.

RealFace được tải qua LoadRealFace0x39cdb10 theo SkeletalMesh'/Game/Assets/character/RealFace/SK_%s_Face.SK_%s_Face'. Với nhiều cầu thủ có mặt thật, tóc gắn vào head mesh/material/LOD tương ứng. Thay nguyên head có thể đổi cả mặt; không thể gọi là ghép riêng tóc. Tóc generic trong trình tạo nhân vật là đường khác, không mặc nhiên áp dụng được cho thẻ licensed.

Đã có bằng chứng serializer, builder và cấu hình tay dài/ngắn; Studio hỗ trợ hai chế độ này. Đã tìm thấy các giá trị hình khối trong packed appearance, nhưng chưa đủ mapping tên trường và ảnh kiểm chứng để mở slider cơ bắp. Physical Contact là thuộc tính thi đấu, không phải kích thước cơ. Hiện chỉ hỗ trợ chiều cao/cân nặng; chưa có chức năng chỉnh cơ bắp hoặc ghép tóc/mặt riêng trong app.

Muốn tạo mặt/tóc Ronaldo2017 mới bằng Blender cần đúng head mesh, texture, skeleton/LOD và pipeline cook tương thích. Không có bộ mesh/texture đích được xác minh trong nguồn đã trích xuất để tạo bản thay thế có thể kiểm tra. Không gửi một file head tráo cả mặt dưới tên “ghép tóc”.

## Tên cầu thủ

Player.bin có46610 record400 byte; tên tiếng Anh ởbyte332..399, ID64bit ở+8. Tên là dữ liệu riêng, không nằm trong147 chỉ số/skill. Điều này xác nhận có dữ liệu để đổi tên; chưa xác nhận mọi màn hình dùng cùng tên hoặc cùng cache.

APK tham khảo có ô live-edit-name, lưu state.live_player_overrides[id]. Đường exportFiles được kiểm tra không đọc live_player_overrides để xuất tên native mới. Vì vậy ô sửa tên trong app tham khảo chưa đủ chứng minh tên trong trận đổi được.

Đổi tên trong game có khả năng làm qua dữ liệu tên/native lookup và cache đúng phiên bản, nhưng chưa có hook tên đã kiểm chứng để đưa vào v17. Hiện chưa cho nhập một tên rồi giả vờ đã đổi trong trận. Không thay Player.bin/CPK/dt200 để thử trên bộ game đang hoạt động.
