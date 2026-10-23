"""Package the known jersey/country repair and a separately labelled phone comparison.
Never advertise the unresolved four-face defect as fixed.
"""
from pathlib import Path
import hashlib,json,zipfile,re,shutil,subprocess,sys
r=Path(__file__).resolve().parent;out=r.parent;deploy=r/'deploy';base=out.parent/'player-faces-v16/Faces-v16-13-cards.zip'
sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha(base.read_bytes())=='1bc1baaa90b4ac618c46c07651d5fb174c7cd8e1bd38ebd320e0437719ae2732'
files=['work/tools/'+n for n in ['gateway_runtime.py','noodle_hair.py','libnoodle_hair.so','noodle_hair.json','noodle_bundle.json','myleague_editor_runtime.py','select_team_runtime.py','libselect_team.so']]+['livedata/pc9298_mobile_and.'+ext for ext in ['pak','utoc','ucas']]
with zipfile.ZipFile(base) as z:
 for n in files:
  if n.startswith('livedata/') or Path(n).name in ['gateway_runtime.py','myleague_editor_runtime.py','select_team_runtime.py','libselect_team.so']:assert z.read(n)==(deploy/n).read_bytes(),n
for n in ['native-validation.json','hook-install-validation.json','runtime-validation.json']:(out/n).write_bytes((r/n).read_bytes())
native=json.loads((out/'native-validation.json').read_text());assert len(native['checks'])==692
assert native['jersey_texture_config_bytes_preserved'] and native['native_nationality_setter_body_executed']
assert native['hook_sha256']==sha((deploy/'work/tools/libnoodle_hair.so').read_bytes())
assert json.loads((out/'comparison-native-validation.json').read_text())['diagnostic_only']
comparison=r/'comparison';overlay=comparison/'deploy';shutil.copytree(deploy,overlay,dirs_exist_ok=True)
nat=(comparison/'libnoodle_hair.so').read_bytes();csha=sha(nat);assert csha!=native['hook_sha256']
code=(r/'noodle_hair.py').read_text().replace('player-faces-v17-jersey-nationality','player-faces-v17-compare-working-2006');code=re.sub(r"HOOK_SHA='[0-9a-f]{64}'",'HOOK_SHA='+repr(csha),code)
(comparison/'noodle_hair.py').write_text(code);(overlay/'work/tools/noodle_hair.py').write_text(code);(overlay/'work/tools/libnoodle_hair.so').write_bytes(nat)
meta=json.loads((deploy/'work/tools/noodle_bundle.json').read_text());meta.update(version='player-faces-v17-compare-working-2006',native_sha256=csha,asset_revision='v17-diagnostic-only-four-failing-cards-use-known-working-ND06',diagnostic_only=True,comparison_ids=['88044950524330','106734785925546','105765448873424','105643042189511'])
(overlay/'work/tools/noodle_bundle.json').write_text(json.dumps(meta,indent=2))
install=(r/'validate_install.py').read_text().replace('player-faces-v17-jersey-nationality','player-faces-v17-compare-working-2006');(comparison/'validate_install.py').write_text(install);shutil.copyfile(r/'validate_runtime.py',comparison/'validate_runtime.py')
for test in ['validate_install.py','validate_runtime.py']:subprocess.run([sys.executable,test],cwd=comparison,check=True)
for n in ['hook-install-validation.json','runtime-validation.json']:(out/('comparison-'+n)).write_bytes((comparison/n).read_bytes())
notes=(out/'HUONG_DAN.md').read_text()
def package(name,root,selected,note):
 with zipfile.ZipFile(out/name,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for n in selected:z.write(root/n,n)
  z.writestr('HUONG_DAN.md',note)
 with zipfile.ZipFile(out/name) as z:
  assert z.testzip() is None and set(z.namelist())==set(selected+['HUONG_DAN.md'])
  m=json.loads(z.read('work/tools/noodle_bundle.json'));native=z.read('work/tools/libnoodle_hair.so');assert sha(native)==m['native_sha256'] and m['native_sha256'] in z.read('work/tools/noodle_hair.py').decode()
  for n in selected:
   if n.startswith('livedata/'):
    assert sha(z.read(n))==m['files'][Path(n).name]['sha256']
  if 'work/tools/gateway_runtime.py' in selected:assert len(z.read('work/tools/gateway_runtime.py'))==2441
 return {'bytes':(out/name).stat().st_size,'sha256':sha((out/name).read_bytes())}
artifacts={}
artifacts['Faces-v17-jersey-nationality.zip']=package('Faces-v17-jersey-nationality.zip',deploy,files,notes)
small=['work/tools/'+n for n in ['noodle_hair.py','libnoodle_hair.so','noodle_bundle.json']]
artifacts['Faces-v17-compare-four-with-2006.zip']=package('Faces-v17-compare-four-with-2006.zip',overlay,small,'# CHỈ ĐỐI CHIẾU — tạm thay đúng bốn đầu lỗi bằng đầu 2006\n\n'+notes)
artifacts['Faces-v17-restore-own-heads.zip']=package('Faces-v17-restore-own-heads.zip',deploy,small,'# KHÔI PHỤC ĐẦU RIÊNG — vẫn giữ phần sửa áo và quốc tịch\n\nBuộc dừng game, gộp work/ vào files/embedded-gateway/, mở lại.\n\n'+notes)
report={'status':'V17_JERSEY_RESOURCE_PRESERVATION_COUNTRY_AND_COMPARISON_PACKAGES_PASS','native_cases_per_mode':692,'twelve_detour_install_paths_per_mode':True,'original_v16_container_byte_identical':True,'gateway_bytes':2441,'source_native_sha256':native['hook_sha256'],'comparison_native_sha256':csha,'four_black_faces_fixed':False,'requires_phone_comparison_result':True,'device_verified':False,'black_face_root_cause_proven':False,'jersey_render_and_flags_phone_verified':False,'artifacts':artifacts}
(out/'package-validation.json').write_text(json.dumps(report,indent=2))
sourcefiles=[p for p in r.iterdir() if p.suffix in ['.py','.c','.sh']]+list(out.glob('*.json'))+list(out.glob('*.md'))+list((out/'references').glob('*'))
with zipfile.ZipFile(out/'Faces-v17-source-and-research.zip','w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in sorted(sourcefiles):
  if p.suffix=='.py':compile(p.read_bytes(),str(p),'exec')
  z.write(p,p.relative_to(out))
with zipfile.ZipFile(out/'Faces-v17-source-and-research.zip') as z:assert z.testzip() is None
names=list(artifacts)+['Faces-v17-source-and-research.zip'];(out/'SHA256SUMS').write_text(''.join(sha((out/n).read_bytes())+'  '+n+'\n' for n in names))
print(json.dumps(report,indent=2))
