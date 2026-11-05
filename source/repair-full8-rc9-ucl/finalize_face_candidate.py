"""RC7-based face-only candidate. UCL core is SOURCE ONLY, never advertised as integrated."""
from pathlib import Path
import sys,json,hashlib,re,ast,shutil
VERSION='V19.1-FULL8-RC7-BASE-FACEFIX-19018-CANDIDATE'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def finalize(root):
 root=Path(root);g=root/'assets/gateway-release';t=g/'work/tools';src=root/'source/repair-full8-rc9-ucl';v=root/'validation';prior=json.loads((root/'payload-inventory.json').read_text());assert sha(root/'payload-inventory.json')=='4acc1d023a92a7e75874aa7684e97e21e49193f3cd166911fc04eacd78e95ff8';assert sha(root/'classes5.dex')=='687f574b70c37888c274bd8d9b1cf193dc3eff33d4556eb8db34d8b124a53c51'
 # Only the reviewed face palette chain changes; leave RC7 1P/Transfer controls and DEX exact.
 shutil.copyfile(src/'face-overlays/appearance_choices.py',t/'appearance_choices.py');shutil.copyfile(root/'.ci-face-candidate/libnoodle_hair.so',t/'libnoodle_hair.so')
 p=t/'noodle_hair.py';text,n=re.subn(r"HOOK_SHA='[^']+'","HOOK_SHA='"+sha(t/'libnoodle_hair.so')+"'",p.read_text());assert n==1;p.write_text(text)
 p=t/'private_bundles.py';text=p.read_text();assert "'pc9359']"in text or "'pc9383']"in text;p.write_text(text.replace("'pc9359']","'pc9359', "+', '.join(repr('pc%d'%n)for n in range(9360,9384))+']'))
 p=t/'private_bundles.json';d=json.loads(p.read_text());d['resource_revision']=19018
 for n in range(9360,9384):
  for ext in ['pak','utoc','ucas']:
   q=g/'livedata'/('pc%d_mobile_and.%s'%(n,ext));d['files'][q.name]={'size':q.stat().st_size,'sha256':sha(q)}
 p.write_text(json.dumps(d,indent=2))
 p=t/'noodle_bundle.json';d=json.loads(p.read_text());d['version']=VERSION;d['asset_revision']=19018;d['native_sha256']=sha(t/'libnoodle_hair.so');d['new_three_faces']['89138556572074']='R8A2';d['ronaldo2027_profile'].update(profile='R8A1..R8A6',final_face_containers='pc9360..9383',native_body_palette=2,selectable_head_and_body_palettes=list(range(1,7)),geometry_texture_weights_bind_pose_LODs='RC7 base. Measured head/neck diffuse calibration to native palette; closed rest lips; black matte oral parts; high166 and native compact153 LODs. Phone pending.',phone_verified=False);d['appearance_files']={n:sha(t/n)for n in d['appearance_files']};d['appearance_overlay_sha256']=sha(t/'myleague_editor_runtime.py');p.write_text(json.dumps(d,indent=2))
 for name,key in [('release-manifest.json','release_id'),('ui6-runtime-manifest.json','version')]:
  p=g/name;d=json.loads(p.read_text());d[key]=VERSION;p.write_text(json.dumps(d,indent=2))
 (root/'README-VI.md').write_text('''# RC7 BASE — Ronaldo 2027 face correction candidate

Nền FULL8 RC7 trên v19.1; revision19018. Payload assets/ và classes5.dex, không phải APK đã ký. Giữ DEX, Single Player và Transfer RC7 nguyên byte. Không áp dụng bộ điều khiển RC8.

Ronaldo2027 ID89138556572074: giữ đầu/tóc MessipradeepV2, chỉnh môi nghỉ cục bộ; các phần trong miệng chuyển đen và không phản sáng theo yêu cầu hiện tại. Da đầu và cổ được chuẩn màu từ UV của asset RC7 về cùng palette thân native; lựa chọn1–6 áp dụng cả đầu và thân trước khi engine tải. Có LOD0 đủ166bone và LOD1 độc lập153bone với trọng số native. Không scale tay hay thay mesh cơ thể.

Đây là bản ứng viên cần kiểm tra trực tiếp trên điện thoại: SIUU, nghỉ/há miệng, ánh sáng cổ và chuyển LOD. Host kiểm tra không chứng minh hết lỗi tay dài hoặc crash trên thiết bị.

UCL: chỉ có thuật toán/state source trong source/repair-full8-rc9-ucl/runtime để tiếp tục phát triển. Chưa có nút mở, native match adapter, thống kê cầu thủ, World Cup adapter hay bộ lọc EventAI2mục trong bản ứng viên này. Không gọi đây là bản FULL đã tích hợp UCL. Nút thắt là engine phải xử lý hòa tổng tỷ số sau lượt về, không chỉ hòa tỷ số riêng của trận. Không gửi giải chưa nối trận thật dưới tên bản hoàn thiện.

Không xóa data hoặc save. Không có DB, save hay log cá nhân trong payload. Chưa kiểm thử điện thoại.
''')
 helper=root/'source/repair-full8-rc2-hf1/build_runtime_manifests.py';ns={};exec(compile(helper.read_text(),str(helper),'exec'),ns);ns['update'](g);ns['check'](g)
 sys.path.insert(0,str(root/'source/repair-full8-rc5-hf1'));from check_startup_integrity import verify;from verify_login_gate import run
 report=verify(root);report.update(run(root));report.update(revision=19018,ucl_integrated=False,phone_verified=False);(v/'full8-rc9-face-startup-integrity.json').write_text(json.dumps(report,indent=2))
 for p in t.glob('*.py'):ast.parse(p.read_text())
 names={r['path']for r in prior['files']}|{p.relative_to(root).as_posix()for p in src.rglob('*')if p.is_file()}|{p.relative_to(root).as_posix()for p in(g/'livedata').glob('pc93*_mobile_and.*')if 9360<=int(p.name[2:6])<=9383}|{p.relative_to(root).as_posix()for p in v.glob('full8-rc9-*.json')}
 rows=[]
 for name in sorted(names):
  p=root/name;assert p.is_file()and '__pycache__'not in p.parts and p.suffix not in{'.db','.sqlite','.sqlite3','.log','.zip','.rar','.apk','.mp4'},name;rows.append(dict(path=name,bytes=p.stat().st_size,sha256=sha(p)))
 (root/'payload-inventory.json').write_text(json.dumps(dict(version=VERSION,resource_revision=19018,phone_verified=False,ucl_integrated=False,files=rows),indent=2));print(json.dumps(report,indent=2))
if __name__=='__main__':finalize(sys.argv[1])
