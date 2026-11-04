"""Finalize RC7 after verified RC6, retaining all nested integrity/login gates."""
from pathlib import Path
import sys,json,hashlib,re,ast
VERSION='V19.1-FULL8-RC7-native-roster-key-padding-face'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def finalize(root):
 root=Path(root);g=root/'assets/gateway-release';t=g/'work/tools';s=root/'source/repair-full8-rc7';v=root/'validation';prior=json.loads((root/'payload-inventory.json').read_text());assert prior['resource_revision']==19014
 p=t/'libnoodle_hair.so';b=p.read_bytes();assert sha(p)=='4331b5ca5cbc0e3101913abb4b5367d971751f6e05425af71eb9c1d5d950b557';assert b.count(b'RG27\0')==1;p.unlink();p.write_bytes(b.replace(b'RG27\0',b'RG28\0'))
 for code,lib in [('noodle_hair.py','libnoodle_hair.so'),('single_player_live_runtime.py','libsingle_player_live.so'),('transfer_final_runtime.py','libtransfer_final.so')]:
  p=t/code;text,n=re.subn(r"HOOK_SHA='[^']+'","HOOK_SHA='"+sha(t/lib)+"'",p.read_text());assert n==1;p.write_text(text)
 for name in ['full4_trace.py']:
  p=t/name;p.write_text(p.read_text().replace('FULL8-RC6','FULL8-RC7'))
 p=t/'private_bundles.py';text=p.read_text();assert "'pc9355']"in text;p.write_text(text.replace("'pc9355']","'pc9355', 'pc9356', 'pc9357', 'pc9358', 'pc9359']"))
 p=t/'private_bundles.json';d=json.loads(p.read_text());d['resource_revision']=19015
 for n in range(9356,9360):
  for ext in ['pak','utoc','ucas']:
   q=g/'livedata'/('pc%d_mobile_and.%s'%(n,ext));d['files'][q.name]={'size':q.stat().st_size,'sha256':sha(q)}
 p.write_text(json.dumps(d,indent=2))
 p=t/'noodle_bundle.json';d=json.loads(p.read_text());d['version']=VERSION;d['asset_revision']=19015;d['native_sha256']=sha(t/'libnoodle_hair.so');d['new_three_faces']['89138556572074']='RG28';d['ronaldo2027_profile'].update(profile='RG28',final_face_containers='pc9356..9359',geometry_texture_weights_bind_pose_LODs='Local eyelid adjustment <=1.13mm; lower teeth/tongue rigid jaw binding. Topology, UVs, source textures, reference poses, LODs, hair and body geometry preserved.',native_body_palette=2,phone_verified=False);d['appearance_files']={n:sha(t/n)for n in d['appearance_files']};d['appearance_overlay_sha256']=sha(t/'myleague_editor_runtime.py');p.write_text(json.dumps(d,indent=2))
 for name,key in [('release-manifest.json','release_id'),('ui6-runtime-manifest.json','version')]:
  p=g/name;d=json.loads(p.read_text());d[key]=VERSION;p.write_text(json.dumps(d,indent=2))
 (root/'README-VI.md').write_text('''# FULL-8 RC7 · APK73 · nền FULL-7

FULL tích lũy tiếp nối RC6; resource_revision19015. Đây là payload assets/ và classes5.dex, không phải APK đã ký. Giữ save/data và khóa ký cũ; không gỡ app/xóa data.

RC6 trên điện thoại đã chứng minh: roster captures có nhưng chỉ4cầu thủ trên sân, ID sai; Transfer final applies0 dù được gọi hơn21nghìn lần. Bài kiểm tra RC6 mô phỏng sai vị trí team và padding bằng0, nên chưa bắt được hai lỗi này.

Single Player RC7 dùng getter72c19dc đúng cho global Scene (native72d8070 sử dụng), thay getter72c404c của cấu trúc khác. Test đặt đồng thời roster đúng11người và đối tượng giả ở chỗ RC6 đọc nhầm: RC6 tái hiện reason6/pitch4, RC7 đọc11và khóa được cầu thủ. Tap1P khi cấu hình đang bật nhưng chưa active sẽ mở danh sách ngay để thay ID cũ sai; khi đã active thì tap để tắt. Giữ để đổi cầu thủ. Không cần bật AI. Nút xanh chỉ khi native active. Kiểm tra host đã thử cả hai phía; chưa xác nhận trên điện thoại.

Transfer: native key có kind32 cộng padding32 không được khởi tạo. RC6 so cả64bit nên có thể bỏ qua record đúng. RC7 chỉ kiểm tra kind32 như native, vẫn xác minh đủ full ID. Test cố ý làm bẩn padding tái hiện lỗi cũ và xác nhận stat/skill/booster/foot/position áp dụng sau classic/world; chỉ full ID đã sửa stat trong đúng giải được miễn cân bằng. Cầu thủ chưa sửa vẫn cân bằng. Diagnostics có verified_fields, mismatched_fields và padded_keys để đối chiếu trực tiếp native getter sau khi ghi. Không ép số OVR trên thẻ để giả vờ đã sửa stat; OVR có thể giữ nguyên do làm tròn/giới hạn hoặc chỉ chỉnh ít thuộc tính. Cần đối chiếu chỉ số thực tế, không chỉ OVR100.

Ronaldo2027 ID89138556572074, vẫn nguồn Android MessipradeepV2 mà người dùng gửi. Giữ topology, hình dạng đầu tổng thể, tóc, UV, texture,166bone, bind pose và LOD gốc. Chỉ khép nhẹ vùng mí ở rest pose tối đa1.13mm; giữ nhãn cầu và bone mắt riêng. Răng dưới và lưỡi là các phần rời, sửa từ blend head/jaw làm giãn sang rigid jaw để theo hàm khi há miệng. Không thay hay scale mesh cơ thể, không dồn bone mặt về head. Cổ/thân dùng native palette2 riêng đúng full ID, gần màu albedo mép cổ nguồn; không dùng texture che lỗi rig. Kiểm tra invariants và mô phỏng há hàm không thay thế kiểm chứng SIUU/ánh sáng trên điện thoại; không bảo đảm giống ảnh ngoài đời tuyệt đối.

UCL v23.1 mới được nghiên cứu, chưa tích hợp. Xem RESEARCH-UCL-V23.1.md. Không đổi sang FULL6/efootxi, không chép engine v23 hoặc PES2021. Giữ Transfer đội hình/vai trò và accessories đã được người dùng xác nhận, giữ sửa login/integrity, Spider/Miles và không thêm Vol9.

Không có save/DB cá nhân, diagnostics người dùng, source ZIP/RAR, video, APK hoặc bundle v23 nghiên cứu trong FULL. Reports cũ là lịch sử; kết quả RC7 mới có tiền tố full8-rc7. Kiểm tra checksum toàn gói và LOGIN guard thực tế; checksum sai vẫn bị chặn. Chưa kiểm chứng RC7 trên điện thoại.
''')
 helper=root/'source/repair-full8-rc2-hf1/build_runtime_manifests.py';ns={};exec(compile(helper.read_text(),str(helper),'exec'),ns);ns['update'](g);n=ns['check'](g)
 sys.path.insert(0,str(root/'source/repair-full8-rc5-hf1'));from check_startup_integrity import verify;report=verify(root);from verify_login_gate import run;report.update(run(root));report['revision']=19015
 for name,lib in [('transfer_final_runtime.py','libtransfer_final.so'),('single_player_live_runtime.py','libsingle_player_live.so')]:assert "HOOK_SHA='"+sha(t/lib)+"'"in(t/name).read_text()
 (v/'full8-rc7-startup-integrity.json').write_text(json.dumps(report,indent=2))
 for p in t.glob('*.py'):ast.parse(p.read_text())
 names={x['path']for x in prior['files']}|{p.relative_to(root).as_posix()for p in s.rglob('*')if p.is_file()}|{p.relative_to(root).as_posix()for p in(g/'livedata').glob('pc935[6-9]_mobile_and.*')}|{p.relative_to(root).as_posix()for p in v.glob('full8-rc7-*.json')}|{'RESEARCH-UCL-V23.1.md'}
 rows=[]
 for name in sorted(names):
  p=root/name;assert p.is_file(),name;assert '__pycache__'not in p.parts and not p.name.endswith('.private.json')and p.suffix.lower()not in{'.log','.db','.sqlite','.sqlite3','.zip','.rar','.apk','.mp4'},name;rows.append({'path':name,'bytes':p.stat().st_size,'sha256':sha(p)})
 (root/'payload-inventory.json').write_text(json.dumps({'version':VERSION,'resource_revision':19015,'phone_verified':False,'files':rows},indent=2));print(json.dumps({'files':len(rows)+1,'runtime':n,'login':report},indent=2))
if __name__=='__main__':finalize(sys.argv[1])
