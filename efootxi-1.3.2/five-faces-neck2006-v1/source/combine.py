from pathlib import Path
import json,shutil,subprocess,sys,re,hashlib
R=Path(__file__).parent;P=Path('/workspace/analysis/my-league/ronaldo-pc-conversion');N=P/'android-five-combined';targets=json.loads((R/'targets.json').read_text());(N/'asset').mkdir(exist_ok=True)
for kind in targets:
 for f in (P/('android-five-'+kind)/'asset').iterdir():shutil.copyfile(f,N/'asset'/f.name)
s=(P/'android-hulk-only/build_full_container.py').read_text();a=s.index('recipes=[]');b=s.index('chunks=[];',a)
s=s[:a]+'''recipes=[]
targets='''+repr(targets)+'''
for kind,row in targets.items():
 prefix=row['prefix'];mi=row['material_prefix']
 for variant in ['4522','4522lg00v0000','4522ep01v0291','4522ep00v0313']:
  parts=['Hair']if kind=='ronaldo'else['Hair','FaceLegacy','FaceUpcon']
  remap={pid(base+'MI_'+variant+'_Head_'+part+'_'+q):pid(base+'MI_'+mi+'_Head_Hair_'+q)for part in parts for q in ['HQ','MQ']}
  recipes.append(('SK_'+variant.replace('4522',prefix,1)+'_Face',heads,'RealFace/SK_'+variant+'_Face.uasset',remap))
 matimport={pid(base+'T_133157_Hair_D'):pid(base+'T_'+mi+'_Hair_D')}
 recipes +=[(f'MI_{mi}_Head_Hair_{q}',mats,'character/RealFace/MI_133157_Head_Hair_MQ.uasset',matimport)for q in ['HQ','MQ']]
 recipes +=[('T_'+mi+'_Hair_D',mats,'character/RealFace/T_133157_Hair_High_D.uasset',{})]
 recipes +=[('T_'+v.replace('4522',prefix,1)+'_Face_D',mats,'character/RealFace/T_133157_Face_D.uasset',{})for v in ['4522','4522lg00v0000','4522ep01v0291','4522ep00v0313']]
''' +s[b:]
s=s.replace("for mi in ['ND0001']for q", "for mi in [r['material_prefix']for r in targets.values()]for q");(N/'build_full_container.py').write_text(s);subprocess.run([sys.executable,str(N/'build_full_container.py')],check=True)
for ext in ['utoc','ucas']:shutil.copyfile(P/'android-hulk-venom-combined/container'/('global.'+ext),N/'container'/('global.'+ext))
t=N/'deploy/work/tools';l=N/'deploy/livedata';t.mkdir(parents=True,exist_ok=True);l.mkdir(parents=True,exist_ok=True);code=(N/'noodle_hair.py').read_text();code=re.sub("HOOK_SHA='[0-9a-f]{64}'",'HOOK_SHA='+repr(hashlib.sha256((N/'libnoodle_hair.so').read_bytes()).hexdigest()),code);(N/'noodle_hair.py').write_text(code);(t/'noodle_hair.py').write_text(code);shutil.copyfile(N/'libnoodle_hair.so',t/'libnoodle_hair.so');shutil.copyfile(P/'startup-fix/gateway_runtime_fixed.py',t/'gateway_runtime.py');assert len((t/'gateway_runtime.py').read_bytes())==2441;(t/'noodle_hair.json').write_text('{"enabled":true}\n')
meta={'version':'five-faces-neck2006-v1','container':'pc9298_mobile_and','target_card_ids':{k:v['card_id']for k,v in targets.items()},'native_sha256':hashlib.sha256((t/'libnoodle_hair.so').read_bytes()).hexdigest(),'files':{},'phone_tested':False,'fixed_facial_expression_heads':['hulk','orc','joker','naruto'],'ronaldo':'native face vertex order, weights and common eyes preserved; supplied 2009 diffuse on 2006 surface'}
for ext in ['pak','utoc','ucas']:
 name='pc9298_mobile_and.'+ext;b=(N/'container'/name).read_bytes();(l/name).write_bytes(b);meta['files'][name]={'size':len(b),'sha256':hashlib.sha256(b).hexdigest()}
(t/'noodle_bundle.json').write_text(json.dumps(meta,indent=2))
for f in ['validate_install.py','validate_runtime.py']:subprocess.run([sys.executable,str(N/f)],check=True)
print('FIVE_FACE_CONTAINER_AND_RUNTIME_STAGED',flush=True)
