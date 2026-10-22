"""Four-file native update for an already verified v10 installation."""
from pathlib import Path
import zipfile,json,hashlib
out=Path(__file__).resolve().parent.parent;full=out/'Faces-v11-12-cards.zip';name='Faces-v11-update-from-v10.zip';names=['work/tools/'+n for n in ['noodle_hair.py','libnoodle_hair.so','noodle_bundle.json','noodle_hair.json']]
notes='Bản này chỉ dành cho v10 đã cài đủ và hoạt động. Buộc dừng game, gộp work/ vào files/embedded-gateway/, ghi đè 4 tệp rồi mở lại. Container, gateway, áo và texture đầu giữ nguyên v10. Nếu thiếu tệp/checksum sai, dùng gói đầy đủ Faces-v11-12-cards.zip. Không xóa save. Phần artwork Xuân Son chưa hoàn thành, chưa được cài vào game.\n'
with zipfile.ZipFile(full) as src,zipfile.ZipFile(out/name,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for n in names:z.writestr(n,src.read(n))
 z.writestr('CAP_NHAT_TU_V10.txt',notes)
with zipfile.ZipFile(out/name) as z:
 assert z.testzip() is None
 meta=json.loads(z.read('work/tools/noodle_bundle.json'));assert hashlib.sha256(z.read('work/tools/libnoodle_hair.so')).hexdigest()==meta['native_sha256']
 with zipfile.ZipFile(out.parent/'player-faces-v10/Faces-v10-12-cards.zip') as baseline:
  for n,row in meta['files'].items():assert hashlib.sha256(baseline.read('livedata/'+n)).hexdigest()==row['sha256']
  for n,sha in meta['appearance_files'].items():assert hashlib.sha256(baseline.read('work/tools/'+n)).hexdigest()==sha
  assert hashlib.sha256(baseline.read('work/tools/myleague_editor_runtime.py')).hexdigest()==meta['appearance_overlay_sha256']
r={'status':'FOUR_FILE_V10_UPDATE_NATIVE_SHA_AND_BASELINE_DEPENDENCIES_PASS','files':names,'bytes':(out/name).stat().st_size,'sha256':hashlib.sha256((out/name).read_bytes()).hexdigest(),'requires_verified_original_v10':True,'phone_tested':False};(out/'v10-update-validation.json').write_text(json.dumps(r,indent=2));print(r['status'],r['bytes'])
