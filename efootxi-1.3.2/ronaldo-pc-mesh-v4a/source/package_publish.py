from pathlib import Path
import json,hashlib,zipfile,subprocess,tempfile,os,urllib.request
r=Path(__file__).parent;repo=Path('/workspace/testingdummy');prefix='efootxi-1.3.2/ronaldo-pc-mesh-v4a/';base='https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/'+prefix
readme='''# Ronaldo v4a — sửa đường dẫn làm mất tóc ở v4

Chỉ Card ID **88044950524330**, Android efootxi 1.3.2, MT Manager không root.

## Cài

1. Buộc dừng game.
2. Giải nén `Ronaldo-PC-mesh-v4a-88044950524330.zip`.
3. Gộp cả **work/** và **livedata/** vào **files/embedded-gateway/**, ghi đè đủ 8 tệp. Không dán bên trong work/tools và không cài chồng bản v4 cũ sau đó.
4. Mở game, tải dữ liệu nếu có yêu cầu, vào sân bằng đúng thẻ 88044950524330.
5. Kiểm tra tóc và cả cảnh replay/ăn mừng. Chưa có xác nhận hết lỗi tay/giày kéo dài trên điện thoại.

Không xóa dữ liệu/save. Gateway giữ nguyên bản tương thích 2441 byte; không thay dt200, đội hình hay cấu hình My League. Container/mesh/texture giống v4, chỉ sửa runtime/native và checksum liên quan. Không cần sửa APK.

## Vì sao tóc biến mất

Log điện thoại v4: HOOK_ACTIVE, target_calls=1, skipped_face_id=1, redirects=0. Đã gặp đúng thẻ nhưng không thay asset.

Đối chiếu mã engine thật cho thấy hàm mesh 0x39cd71c nhận FSoftObjectPath 24 byte (FName + subpath FString), không phải FString 16 byte như v4 đọc. V4 vì vậy không nhận diện đường dẫn và chuyển thẳng đầu gốc. Kiểm tra v4 trước đây mô hình hóa sai kiểu đối số này nên không phát hiện lỗi.

V4a giữ đối số loader như một cấu trúc opaque, không đọc hay tự tạo FName. Việc thay đường dẫn được chuyển sang FSoftObjectPath::SetPath tại 0x45b58b0: game nhận chuỗi UTF-16 có độ dài xác định rồi tự tạo đối tượng native. Hỗ trợ cả đường dẫn object trần và class reference, chỉ đúng bốn biến thể 4522 ở RealFace, trong scope của đúng actor/thẻ/thread. Giữ nguyên Face ID và callback gốc. Nếu private mesh trả null, nạp lại đầu gốc trong scope chặn redirect để tránh vòng lặp.

Đây là bản sửa lỗi nhận diện đường dẫn. Không tuyên bố đã xác nhận tóc, màu da/biểu cảm hoặc biến dạng replay trên thiết bị. Giữ nguyên mesh PC và bảng retarget của v4; xem hướng dẫn v4 để biết giới hạn chuyển rig PC sang Android.

## Log sau khi vào sân

`files/embedded-gateway/work/tools/noodle-hair-status.json`

- version: **ronaldo-pc-face-v4a-softpath**.
- Cần quan sát `mesh_path_redirects`, `redirects`, `nonnull_callbacks` tăng khi đầu mới tải.
- `last_face_profile` vẫn là 4522... là đúng: không thay nhận diện cầu thủ.
- `last_asset_path`, `last_actor_type`, `scoped_path_calls` bổ sung chẩn đoán.
- Với actor dùng vật liệu gắn sẵn, không nhất thiết có callback texture riêng; chỉ số texture=0 không tự kết luận mesh thất bại.
- Nếu tóc vẫn không xuất hiện hoặc replay lỗi, gửi toàn bộ log và ảnh.

## Tắt đầu thử

Buộc dừng game, dán work/ từ `Tat-dau-thu-Ronaldo.zip` vào files/embedded-gateway/, mở lại. Chỉ đặt enabled=false, không xóa save. Bật lại bằng gói đầy đủ v4a.

## Kiểm tra

30 trường hợp thực thi native ARM64 trong Unicorn: plain/class path, cả bốn biến thể, length có/không NUL, đúng full Card ID, thẻ khác, opaque FSoftObjectPath 24 byte có FName không thể dùng như con trỏ, giữ nguyên nhận diện, cách ly scope/thread, disabled, callback và fallback cả inline/async. Các thân hàm engine vẫn mô hình hóa tại biên; không chạy renderer Android.

Năm đường cài detour Python, SHA/prologue engine thật, worker HOOK_ACTIVE, manifest/hash/idempotence và gateway được kiểm tra. Asset không đổi so với v4 và được đối chiếu byte trước đóng gói. ZIP kiểm tra CRC và checksum đủ 8 tệp.

Nguồn PC người dùng cung cấp (NEUBE), chưa xác minh trên điện thoại.
'''
(r/'HUONG_DAN.md').write_text(readme)
files=['work/tools/gateway_runtime.py','work/tools/noodle_hair.py','work/tools/libnoodle_hair.so','work/tools/noodle_hair.json','work/tools/noodle_bundle.json']+['livedata/pc9298_mobile_and.'+x for x in ['pak','utoc','ucas']]
z=r/'Ronaldo-PC-mesh-v4a-88044950524330.zip';off=r/'Tat-dau-thu-Ronaldo.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as f:
 for name in files:f.write(r/'deploy'/name,name)
 f.writestr('HUONG_DAN.md',readme)
with zipfile.ZipFile(off,'w',zipfile.ZIP_DEFLATED) as f:f.writestr('work/tools/noodle_hair.json','{"enabled":false}\n')
with zipfile.ZipFile(z) as f:
 assert f.testzip() is None and set(f.namelist())==set(files+['HUONG_DAN.md']);assert len(f.read('work/tools/gateway_runtime.py'))==2441
 meta=json.loads(f.read('work/tools/noodle_bundle.json'))
 for name,row in meta['files'].items():
  b=f.read('livedata/'+name);assert len(b)==row['size'] and hashlib.sha256(b).hexdigest()==row['sha256'];assert b==(r.parent/'android-face-v4/container'/name).read_bytes()
 native=hashlib.sha256(f.read('work/tools/libnoodle_hair.so')).hexdigest();assert native==meta['native_sha256'] and native in f.read('work/tools/noodle_hair.py').decode();compile(f.read('work/tools/noodle_hair.py'),'noodle_hair.py','exec')
report={'status':'EIGHT_FILE_BUNDLE_HASHES_BOOTSTRAP_SIZE_AND_ZIP_CRC_PASS','assets_byte_identical_v4':True,'phone_tested':False,'replay_stretch_verified_fixed':False,'artifacts':{p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [z,off]}};(r/'package-validation.json').write_text(json.dumps(report,indent=2))
def git(*args,**kw):return subprocess.run(['git','-C',str(repo),*args],check=True,capture_output=True,**kw).stdout
old=git('rev-parse','chat-downloads').decode().strip();assert git('ls-remote','--heads','origin','chat-downloads').decode().split()[0]==old;assert git('status','--porcelain')==b''
blobs={prefix+p.name:p.read_bytes() for p in [z,off,r/'HUONG_DAN.md',r/'package-validation.json',r/'native-validation.json',r/'hook-install-validation.json',r/'runtime-validation.json']}
for name in ['noodle_hair.c','build_native.sh','noodle_hair.py','prepare_deploy.py','validate_install.py','validate_runtime.py','validate_native.py','package_publish.py']:
 blobs[prefix+'source/'+name]=(r/name).read_bytes()
blobs['README.md']=('> **Ronaldo v4a — sửa lỗi v4 mất tóc:** [Tải gói đầy đủ]('+base+z.name+') · [Hướng dẫn]('+prefix+'HUONG_DAN.md). Log điện thoại xác nhận v4 không redirect; sửa kiểu đối số FSoftObjectPath. V4a chưa thử trên điện thoại.\n\n').encode()+git('show',old+':README.md')
pv='efootxi-1.3.2/ronaldo-pc-mesh-v4/HUONG_DAN.md';blobs[pv]=('> V4 đã được báo mất tóc: đọc sai đối số FSoftObjectPath. Dùng [v4a](../ronaldo-pc-mesh-v4a/HUONG_DAN.md) thay thế.\n\n').encode()+git('show',old+':'+pv)
with tempfile.TemporaryDirectory() as d:
 env=os.environ.copy();env['GIT_INDEX_FILE']=str(Path(d)/'index');git('read-tree',old,env=env);sums={}
 for line in git('show',old+':SHA256SUMS').decode().splitlines():sha,name=line.split('  ',1);sums[name]=sha
 for name,data in blobs.items():
  blob=git('hash-object','-w','--stdin',input=data).decode().strip();git('update-index','--add','--cacheinfo',f'100644,{blob},{name}',env=env);sums[name]=hashlib.sha256(data).hexdigest()
 data=''.join(sums[n]+'  '+n+'\n' for n in sorted(sums)).encode();blob=git('hash-object','-w','--stdin',input=data).decode().strip();git('update-index','--add','--cacheinfo',f'100644,{blob},SHA256SUMS',env=env)
 tree=git('write-tree',env=env).decode().strip();commit=git('commit-tree',tree,'-p',old,input=b'Fix v4 lost hair: use scoped native SetPath ABI; preserve opaque mesh FSoftObjectPath and original identity\n').decode().strip();git('update-ref','refs/heads/chat-downloads',commit,old);git('push','origin','refs/heads/chat-downloads:refs/heads/chat-downloads');assert git('status','--porcelain')==b''
for p in [z,off]:
 raw='https://raw.githubusercontent.com/ron3huq/testingdummy/refs/heads/chat-downloads/'+prefix+p.name;data=urllib.request.urlopen(raw,timeout=45).read();assert data==p.read_bytes();report['artifacts'][p.name].update(url=base+p.name,public_download_verified=True)
report['commit']=commit;(r/'published.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
