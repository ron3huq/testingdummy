from pathlib import Path
import zipfile,json,hashlib
from PIL import Image,ImageDraw
R=Path(__file__).parent;N=Path('/workspace/analysis/my-league/ronaldo-pc-conversion/android-orc-v1')
guide='''ORC — chuyển trực tiếp từ bộ orc_head.part01–12.rar đã gửi
Card ID của gói thử này: 53878485695166 (thẻ Hulk cũ, dùng tạm vì chưa nhận Card ID riêng cho Orc).
Gói riêng, cài sẽ thay bộ nạp face thử hiện tại. Muốn quay lại Hulk/Ronaldo/Spider-Man thì cài lại gói tương ứng.

CÀI GAME ANDROID
1. Buộc dừng game.
2. Giải nén ORC-ANDROID-TRIAL.zip.
3. Chép gộp CẢ work/ và livedata/ vào files/embedded-gateway/, ghi đè đủ 8 file. Không lồng thêm thư mục ZIP, không chép riêng work/tools.
4. Mở lại game; cho tải dữ liệu nếu được yêu cầu. Không xóa save/dữ liệu ứng dụng.
Chỉ dành cho đúng bản efootxi 1.3.2 Android ARM64/libUE4 đã hỗ trợ. Bộ nạp kiểm tra hash và dừng nếu sai bản.
Trạng thái: work/tools/noodle-hair-status.json, version orc-supplied-sculpt-v1.
Tắt: buộc dừng, chép work/ từ Tat-Orc.zip vào files/embedded-gateway/, mở lại.

FILE BLENDER
ORC_GAME_RIGGED.blend: bản game có rig 166 xương native; 90.000 tam giác, 57.839 đỉnh sau tách đường UV. Các ảnh đã pack trong file, có thể mở để kiểm tra và pose xương đầu/cổ.
ORC-FULL-SCULPT.7z.001, .002, .003: tải ĐỦ 3 phần vào cùng thư mục, giữ nguyên tên; dùng ZArchiver/7-Zip mở và giải nén .001 để lấy ORC_FULL_SCULPT.blend. Đây là sculpt đầy đủ 3.684.505 đỉnh, 3.682.944 polygon, giữ nguyên topology và hình học nguồn dưới phép đổi trục/tỉ lệ đồng đều/tịnh tiến. Sculpt đầy đủ là tài liệu đối chiếu; không phải asset chạy trực tiếp trên điện thoại.

HÌNH DÁNG VÀ MÀU
Dùng trực tiếp mô hình Orc được gửi, gồm cả mắt cầu và hai nanh nguyên bản; không tạo một đầu khác thay nguồn. Không thêm tóc hay đổi tỉ lệ riêng từng vùng mặt.
Bộ nguồn chỉ chứa OBJ, STL, ZTL, không có texture màu, UV hay rig game. Màu xanh ô-liu, nanh ngà và màu mắt là vật liệu được tạo thêm, không phải texture gốc. RGB da tham chiếu: 91,106,66 (#5B6A42); swatch riêng được kèm để tham khảo khi chỉnh thân. Gói này không tự đổi da toàn thân.
Mô hình game phải giảm lưới; đối chiếu 50.000 điểm nguồn cho sai số bề mặt lớn nhất khoảng 0,315 mm, p99 khoảng 0,142 mm ở kích thước dựng này. Đây là phép đo lấy mẫu, không phải bảo đảm mọi chi tiết không sai lệch tuyệt đối.
Texture atlas giữ cavity từ sculpt độ phân giải cao, được nén ETC2 và đọc ngược kiểm tra. File Blender còn có normal map bake; shader game dùng atlas màu và normal hình học, nên chất liệu/ánh sáng không giống hoàn toàn Blender.
Orc-comparison.jpg: hàng trên sculpt đầy đủ với vật liệu mới; hàng dưới mesh/texture đã đọc ngược từ gói game, render bằng ánh sáng trung tính trong Blender. Không phải ảnh chụp game.

CỬ ĐỘNG VÀ KIỂM TRA
Giữ biểu cảm sculpt nguồn để giữ hình dáng mặt và nanh. Có skinning đầu/cổ/ngực theo xương native; không có há miệng, chớp mắt hay liếc mắt độc lập. Nguồn không cung cấp rig biểu cảm.
Đã đối chiếu 4 biến thể cooked: hình học, UV, normal, trọng số, indices và 166 ma trận bind gốc; đã thử các pose xoay/nghiêng trên bản đọc ngược với trọng số 8-bit. Vùng cổ sau có hình học thật và atlas alpha đục hoàn toàn.
32 kiểm tra ARM64 trên host, manifest/khởi động/fallback/hashes đều pass; thân hàm engine được mô phỏng. Chưa thử trực tiếp renderer Android, ráp cổ/áo/thân, trận/replay/ăn mừng và hiệu năng trên máy bạn. Không thể bảo đảm tương thích thực tế hoặc giống tuyệt đối 100% trước khi kiểm tra trong game trên thiết bị.
'''
(R/'HUONG-DAN.txt').write_text(guide,encoding='utf8')
board=Image.new('RGB',(1800,1280),(23,25,24));draw=ImageDraw.Draw(board)
for row,prefix in enumerate(['source','cooked']):
 draw.text((16,640*row+8),'SUPPLIED FULL SCULPT - authored materials'if row==0 else'COOKED MOBILE ASSET - Blender neutral preview (not in-game)',fill='white')
 for col,angle in enumerate(['front','quarter','profile']):
  im=Image.open(R/(prefix+'_'+angle+'.png')).convert('RGB');im.thumbnail((600,600));board.paste(im,(col*600,row*640+32));draw.text((col*600+12,row*640+615),angle,fill='white')
board.save(R/'Orc-comparison.jpg',quality=93)
Image.new('RGB',(256,256),(91,106,66)).save(R/'Orc-skin-colour.png')
files=['work/tools/'+n for n in ['gateway_runtime.py','noodle_hair.py','libnoodle_hair.so','noodle_hair.json','noodle_bundle.json']]+['livedata/pc9298_mobile_and.'+e for e in ['pak','utoc','ucas']]
zp=R/'ORC-ANDROID-TRIAL.zip'
with zipfile.ZipFile(zp,'w',zipfile.ZIP_DEFLATED)as z:
 for name in files:z.write(N/'deploy'/name,name)
 z.write(R/'HUONG-DAN.txt','HUONG-DAN.txt');z.write(R/'Orc-skin-colour.png','Orc-skin-colour.png')
with zipfile.ZipFile(R/'Tat-Orc.zip','w',zipfile.ZIP_DEFLATED)as z:z.writestr('work/tools/noodle_hair.json','{"enabled":false}\n')
with zipfile.ZipFile(zp)as z:
 assert z.testzip()is None;assert len(z.read('work/tools/gateway_runtime.py'))==2441;meta=json.loads(z.read('work/tools/noodle_bundle.json'));assert meta['target_card_ids']=={'orc':'53878485695166'}
 for name,m in meta['files'].items():data=z.read('livedata/'+name);assert len(data)==m['size']and hashlib.sha256(data).hexdigest()==m['sha256']
 assert hashlib.sha256(z.read('work/tools/libnoodle_hair.so')).hexdigest()==meta['native_sha256'];assert set(z.namelist())==set(files+['HUONG-DAN.txt','Orc-skin-colour.png'])
assets=[zp,R/'ORC_GAME_RIGGED.blend',*sorted(R.glob('ORC-FULL-SCULPT.7z.*')),R/'Tat-Orc.zip',R/'Orc-comparison.jpg',R/'Orc-skin-colour.png']
report={'phone_tested':False,'target_card_id':'53878485695166','target_is_temporary_previous_hulk_card':True,'fixed_expression':True,'full_sculpt_original_geometry_retained':True,'native_game_vertices':57842,'native_visible_vertices':57839,'native_triangles':90001,'visible_triangles':90000,'artifacts':{p.name:{'size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in assets}};(R/'package-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
