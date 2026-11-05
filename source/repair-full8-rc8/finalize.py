"""Finalize a new cumulative payload; preserve all startup and nested integrity gates."""
from pathlib import Path
import sys,json,hashlib,re,ast
VERSION='V19.1-FULL8-RC8-manual-control-authored-head-native-lods'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def finalize(root):
 root=Path(root);g=root/'assets/gateway-release';t=g/'work/tools';s=root/'source/repair-full8-rc8';v=root/'validation';prior=json.loads((root/'payload-inventory.json').read_text());assert prior['resource_revision']==19015
 for code,lib in [('noodle_hair.py','libnoodle_hair.so'),('single_player_live_runtime.py','libsingle_player_live.so')]:
  p=t/code;text,n=re.subn(r"HOOK_SHA='[^']+'","HOOK_SHA='"+sha(t/lib)+"'",p.read_text());assert n==1;p.write_text(text)
 p=t/'full4_trace.py';p.write_text(p.read_text().replace('FULL8-RC7','FULL8-RC8'))
 p=t/'private_bundles.py';text=p.read_text();assert "'pc9359']"in text;p.write_text(text.replace("'pc9359']","'pc9359', "+', '.join(repr('pc%d'%n)for n in range(9360,9384))+']'))
 p=t/'private_bundles.json';d=json.loads(p.read_text());d['resource_revision']=19016
 for n in range(9360,9384):
  for ext in ['pak','utoc','ucas']:
   q=g/'livedata'/('pc%d_mobile_and.%s'%(n,ext));d['files'][q.name]={'size':q.stat().st_size,'sha256':sha(q)}
 p.write_text(json.dumps(d,indent=2))
 p=t/'noodle_bundle.json';d=json.loads(p.read_text());d['version']=VERSION;d['asset_revision']=19016;d['native_sha256']=sha(t/'libnoodle_hair.so');d['new_three_faces']['89138556572074']='R8A2';d['ronaldo2027_profile'].update(profile='R8A1..R8A6',final_face_containers='pc9360..9383',geometry_texture_weights_bind_pose_LODs='Authored HQ topology, eyes, oral geometry, facial weights, hair and bind pose retained. Local lip seal; native surface/weights below neck z156. Real full LOD0 and independent native compact LOD1 (166/153). Native skin choice also selects head atlas before cache creation; neck atlas tint corrected and oral cavity darkened.',native_body_palette=2,selectable_head_and_body_palettes=[1,2,3,4,5,6],phone_verified=False);d['appearance_files']={n:sha(t/n)for n in d['appearance_files']};d['appearance_overlay_sha256']=sha(t/'myleague_editor_runtime.py');p.write_text(json.dumps(d,indent=2))
 for name,key in [('release-manifest.json','release_id'),('ui6-runtime-manifest.json','version')]:
  p=g/name;d=json.loads(p.read_text());d[key]=VERSION;p.write_text(json.dumps(d,indent=2))
 (root/'README-VI.md').write_text('''# FULL-8 RC8 · APK73 · nền FULL-7

FULL tích lũy tiếp nối RC7; resource_revision19016. Payload assets/ và classes5.dex, không phải APK đã ký. Giữ save/data và khóa ký cũ; không gỡ app/xóa data.

Người dùng đã xác nhận Single Player, Transfer và accessories RC7 hoạt động trên điện thoại. RC8 giữ các sửa roster, full ID, vai trò và key padding đó. Không thay native Transfer library hoặc giảm kiểm tra toàn vẹn/đăng nhập.

Single Player: vẫn khóa đúng full ID trong đội hình thực, nút1P bên phải AI, xanh khi native active. Bỏ việc liên tục ép controller/cursor policy sang3. Dùng thiết lập điều khiển người sau khi tắt AI native, đồng thời giữ các hook khóa cursor. Khi tắt/pause/replay/đổi phía/ra trận vẫn trả snapshot native. Host đã so sánh nhánh ARM64 gốc: RC7 đi vào nhóm mode3/4, RC8 giữ mode1 ở fixture; khóa full ID và khôi phục vẫn qua. Điều này chưa chứng minh trên điện thoại rằng hiện tượng tự lùi đã hết. Không ép cấp độ AI đồng đội. Log global/event0 VERYEASY không đủ để kết luận cấp độ AI đồng đội.

Ronaldo2027 ID89138556572074: vẫn đầu/tóc Android MessipradeepV2 hiện tại. HQ60785vertex, topology/UV, mắt/răng/lưỡi, trọng số mặt và bind pose giữ lại. Chỉ chỉnh môi cục bộ, tối đa5.23mm, giữ các bản sao đường nối da trùng nhau ở rest; không scale đầu hay tay. Cổ dưới z156 được khớp bề mặt/trọng số cổ native, có vùng chuyển tiếp, để tiếp giáp cơ thể; không thay mesh thân. Nguồn cũ chỉ có LOD1, MinLOD1 và RequiredBones166 ở cả hai LOD. RC8 có LOD0 thật, MinLOD0 và LOD1 độc lập dùng compact bones153 như native. Không dồn trọng số mặt HQ về head để vượt kiểm tra.

Vùng texture cổ dưới nguồn thiên hồng được chỉnh về tông vùng tiếp giáp phía trên. Màu da native1..6 cũng chọn biến thể màu cho toàn bộ da đầu/cổ; mặc định2. Giữ màu mắt, răng và tóc. Khoang miệng/lưỡi được làm tối và giảm phản sáng. Chọn màu rồi lưu và khởi động lại game để dùng cả head và body mới; không đổi resource key khi cache đã tạo. Giữ sáu lựa chọn đồng bộ qua bộ chọn profile chỉ đúng full ID này. Ánh sáng trong game vẫn cần kiểm chứng: kiểm tra texture hay mesh không phải bằng chứng màu đầu/thân đã khớp trên điện thoại.

Đọc lại24mesh đã repack bằng UEViewer độc lập; kiểm tra HQ, ref pose, weights mắt/miệng/tóc, RequiredBones và đường nối rest. Kiểm tra shader, SIUU, môi khi nghỉ, cổ, tay qua khoảng cách/LOD và hiện tượng AI tự lùi phải được xác nhận trên điện thoại. Không tuyên bố RC8 đã hoạt động thực tế chỉ từ build hay mô phỏng. UCL vẫn là nghiên cứu, chưa tích hợp. Không thêm Vol9.

Không có save/DB cá nhân, diagnostics người dùng, ZIP/RAR nghiên cứu, video hay APK nghiên cứu trong gói. Reports cũ là lịch sử. Kiểm tra mới có tiền tố full8-rc8; checksum sai vẫn chặn LOGIN.
''')
 helper=root/'source/repair-full8-rc2-hf1/build_runtime_manifests.py';ns={};exec(compile(helper.read_text(),str(helper),'exec'),ns);ns['update'](g);n=ns['check'](g)
 sys.path.insert(0,str(root/'source/repair-full8-rc5-hf1'));from check_startup_integrity import verify;report=verify(root);from verify_login_gate import run;report.update(run(root));report['revision']=19016
 (v/'full8-rc8-startup-integrity.json').write_text(json.dumps(report,indent=2))
 for p in t.glob('*.py'):ast.parse(p.read_text())
 names={x['path']for x in prior['files']}|{p.relative_to(root).as_posix()for p in s.rglob('*')if p.is_file()}|{p.relative_to(root).as_posix()for p in(g/'livedata').glob('pc93*_mobile_and.*')if 9360<=int(p.name[2:6])<=9383}|{p.relative_to(root).as_posix()for p in v.glob('full8-rc8-*.json')}
 rows=[]
 for name in sorted(names):
  p=root/name;assert p.is_file(),name;assert '__pycache__'not in p.parts and not p.name.endswith('.private.json')and p.suffix.lower()not in{'.log','.db','.sqlite','.sqlite3','.zip','.rar','.apk','.mp4'},name;rows.append({'path':name,'bytes':p.stat().st_size,'sha256':sha(p)})
 (root/'payload-inventory.json').write_text(json.dumps({'version':VERSION,'resource_revision':19016,'phone_verified':False,'files':rows},indent=2));print(json.dumps({'files':len(rows)+1,'runtime':n,'login':report},indent=2))
if __name__=='__main__':finalize(sys.argv[1])
