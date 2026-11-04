"""Finalize RC6 checksums from reviewed payload files; retain LOGIN integrity gates."""
from pathlib import Path
import json,hashlib,sys,re,ast
VERSION='V19.1-FULL8-RC6-live-control-scoped-transfer'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def finalize(root):
 root=Path(root);g=root/'assets/gateway-release';t=g/'work/tools';s=root/'source/repair-full8-rc6';v=root/'validation'
 baseline=json.loads((root/'payload-inventory.json').read_text());assert baseline['resource_revision']==19013
 # Change only the profile literal, leaving the known working body lifecycle intact.
 p=t/'libnoodle_hair.so';raw=p.read_bytes();assert sha(p)=='71508da5f16cec8c234a61062e1ab7dc6fd5d441db8f31073ee25f7df3673989';assert raw.count(b'RV8F\0')==1;p.unlink();p.write_bytes(raw.replace(b'RV8F\0',b'RG27\0'))
 for source,lib in [('noodle_hair.py','libnoodle_hair.so'),('select_team_runtime.py','libselect_team.so'),('transfer_final_runtime.py','libtransfer_final.so'),('single_player_live_runtime.py','libsingle_player_live.so')]:
  p=t/source;code=p.read_text();code,n=re.subn(r"HOOK_SHA='[^']+'","HOOK_SHA='"+sha(t/lib)+"'",code);assert n==1;p.write_text(code)
 p=t/'private_bundles.py';code=p.read_text();assert "'pc9351']"in code;p.write_text(code.replace("'pc9351']","'pc9351', 'pc9352', 'pc9353', 'pc9354', 'pc9355']"))
 p=t/'private_bundles.json';doc=json.loads(p.read_text());doc['resource_revision']=19014
 for n in range(9352,9356):
  for ext in ['pak','utoc','ucas']:
   q=g/'livedata'/('pc%d_mobile_and.%s'%(n,ext));doc['files'][q.name]={'size':q.stat().st_size,'sha256':sha(q)}
 p.write_text(json.dumps(doc,indent=2))
 p=t/'noodle_bundle.json';doc=json.loads(p.read_text());doc['version']=VERSION;doc['native_sha256']=sha(t/'libnoodle_hair.so');doc['asset_revision']=19014;doc['new_three_faces']['89138556572074']='RG27'
 doc['ronaldo2027_profile']={'target':'89138556572074','profile':'RG27','source':'User supplied RONALDO-MESSIPRADEEP-V2-106654775417922-ANDROID (1).zip','source_zip_sha256':'5336edc370f5eba5b511902e75d8311cec2974b39fcd713d2c508ca644b0c643','final_face_containers':'pc9352..9355','geometry_texture_weights_bind_pose_LODs':'All34 authored export payloads byte-exact; package namespace only changed','source_scripts_copied':False,'source_archive_copied':False,'phone_verified':False}
 names=set(doc['appearance_files'])|{'transfer_final_runtime.py','libtransfer_final.so','transfer_classic_native_baselines.json','transfer_booster_choices.py'}
 doc['appearance_files']={n:sha(t/n)for n in sorted(names)};doc['appearance_overlay_sha256']=sha(t/'myleague_editor_runtime.py');p.write_text(json.dumps(doc,indent=2))
 for name,key in [('release-manifest.json','release_id'),('ui6-runtime-manifest.json','version')]:
  p=g/name;d=json.loads(p.read_text());d[key]=VERSION;p.write_text(json.dumps(d,indent=2))
 (root/'README-VI.md').write_text('''# FULL-8 RC6 · APK73 · tiếp tục FULL-7

Resource revision **19014**. Gói FULL tích lũy, không phải APK đã ký. Ghép toàn bộ assets/ và classes5.dex vào APK73 đúng nền và ký bằng khóa đang dùng. Giữ dữ liệu ứng dụng; không gỡ app/xóa data. Không có save/DB cá nhân, diagnostics riêng, video, ZIP/RAR nguồn hoặc APK nghiên cứu trong payload.

Single Player: sửa lỗi nhầm tham số Update với pad manager (nguyên nhân roster không bao giờ thu được trên RC5). Lấy pad manager thực từ scene, giữ kiểm tra đúng bên/người điều khiển/đủ hai word key. Tap 1P mở danh sách cầu thủ đang trên sân của đội mình; chọn full ID để bật, tap lần nữa để tắt. Giữ 1P để đổi cầu thủ. Không cần bật AI. Danh sách rỗng có thời hạn3giây và trạng thái native thay vì WAIT vô hạn. Ô1P nền sáng, vuông gọn, bên phải AI; xanh chỉ khi native active. Dùng kích thước/vị trí AI đo được khi Android cung cấp view; với AI vẽ trên surface engine dùng tỉ lệ HUD theo chiều cao viewport. Vị trí chính xác trên các điện thoại chưa được xác nhận.

Transfer My League: áp dụng stat/skill/booster/foot/position sau lớp classic/world/tactics. Chỉ full ID đã sửa stat trong đúng giải đó được miễn cân bằng stat;26stat khác giữ giá trị hiển thị tại lúc sửa. Những cầu thủ chưa sửa vẫn cân bằng; mở/lưu không đổi số không tạo miễn trừ. Quan sát record native giữ riêng trên máy để đọc chỉ số thực, không xuất records vào diagnostics. Trước khi record được quan sát, giao diện ghi rõ nguồn owned/base hoặc baseline classic được kiểm tra. Booster bằng tiếng Anh, +4 trở lên, sắp theo mức và nhóm. Giữ vai trò/đội hình và accessories đã được người dùng xác nhận hoạt động.

Ronaldo2027 full ID89138556572074: thay bằng gói Android MessipradeepV2 do người dùng gửi gần nhất, profile RG27, containers9352..9355. Giữ nguyên toàn bộ34export payload: geometry, UV, texture, rig, bind pose, bone map/weights, RequiredBones và LOD gốc. Chỉ đổi namespace/tên package để không lan sang face khác. Không ghép mặt4522, không tự nặn đầu/mắt, không thêm vạch tóc hoặc sửa texture. Không chép scripts hay thư viện trong ZIP nguồn. Giữ Spider106782819217056, Miles88035555413452 và toàn bộ bản sửa login/integrity. Không thêm lại Vol9.

Kiểm tra tự động gồm native73 mode2 key/cache, MessiY17 bị lớp rating ghi đè rồi được khôi phục đúng stat/skill, cầu thủ chưa sửa vẫn cân bằng, scope không lan giải, lưu/mở lại, native roster/cursor lifecycle với Update-context độc lập, toàn bộ34export face không đổi và gọi trực tiếp validator/LOGIN guard (checksum sai vẫn bị chặn). Native workers của bài kiểm tra LOGIN được giả lập. **Chưa kiểm chứng bản RC6 trên điện thoại; build/test host không chứng minh Single Player và face đã hết lỗi thực tế.**

Nghiên cứu AI giữ observer chỉ đọc: có7mức CPU native và đường mức của MyLeague; chưa có đo đối chứng hành vi trên điện thoại. Không ép hoặc tuyên bố mức khó đã được kiểm chứng tác động thực tế.

Báo cáo source/validation cũ là lịch sử. Kết quả RC6 mới nhất có tiền tố full8-rc6.
''')
 helper=root/'source/repair-full8-rc2-hf1/build_runtime_manifests.py';ns={};exec(compile(helper.read_text(),str(helper),'exec'),ns);ns['update'](g);runtime=ns['check'](g)
 sys.path.insert(0,str(root/'source/repair-full8-rc5-hf1'));from check_startup_integrity import verify;report=verify(root);from verify_login_gate import run;report.update(run(root));report['revision']=19014
 # Also validate owners added in RC6, without starting ARM64 workers on host.
 for name,lib in [('select_team_runtime.py','libselect_team.so'),('transfer_final_runtime.py','libtransfer_final.so')]:
  code=(t/name).read_text();assert "HOOK_SHA='"+sha(t/lib)+"'"in code
 (v/'full8-rc6-startup-integrity.json').write_text(json.dumps(report,indent=2))
 for p in t.glob('*.py'):ast.parse(p.read_text())
 # Only previous FULL inventory plus reviewed new source/assets/reports.
 allowed={x['path']for x in baseline['files']}
 allowed|={p.relative_to(root).as_posix()for p in s.rglob('*')if p.is_file()}
 allowed|={p.relative_to(root).as_posix()for p in(g/'livedata').glob('pc935[2-5]_mobile_and.*')}
 allowed|={p.relative_to(root).as_posix()for p in t.iterdir()if p.is_file()and not p.name.endswith('.private.json')and p.name in ['transfer_final_runtime.py','libtransfer_final.so','transfer_classic_native_baselines.json','transfer_booster_choices.py']}
 allowed|={p.relative_to(root).as_posix()for p in v.glob('full8-rc6-*.json')}
 files=[]
 for name in sorted(allowed):
  p=root/name;assert p.is_file(),name;assert '__pycache__'not in p.parts and not p.name.endswith('.private.json')and p.suffix.lower()not in{'.db','.sqlite','.sqlite3','.log','.rar','.zip','.apk','.mp4'},name
  files.append({'path':name,'bytes':p.stat().st_size,'sha256':sha(p)})
 (root/'payload-inventory.json').write_text(json.dumps({'version':VERSION,'resource_revision':19014,'phone_verified':False,'files':files},indent=2));print(json.dumps({'files':len(files)+1,'runtime_assets':runtime,'login_checks':report},indent=2))
if __name__=='__main__':finalize(sys.argv[1])
