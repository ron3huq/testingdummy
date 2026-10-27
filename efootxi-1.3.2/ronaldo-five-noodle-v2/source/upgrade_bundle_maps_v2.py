from pathlib import Path
import sys,subprocess,os,json,re,hashlib,shutil
R=Path(__file__).parent;V=R/'v2';P=Path('/workspace/analysis/my-league/ronaldo-pc-conversion');N=P/sys.argv[1];targets=json.loads((V/'targets.json').read_text());m=json.loads((N/'deploy/work/tools/noodle_bundle.json').read_text());targets={k:v for k,v in targets.items()if k in m['target_card_ids']}
s=(N/'noodle_hair.c').read_text()
if 'texsuffix'not in s:
 insert='''const char*texsuffix="_Face_D";const char*texmiddle="_Face_D.T_";
 if(kind>=2){const char*candidates[2]={"_Face_N.T_","_Face_SRO.T_"};for(int ci=0;ci<2;ci++){int ok=1;for(int j=0;candidates[ci][j];j++){if(at+j>=n||path[at+j]!=(unsigned char)candidates[ci][j]){ok=0;break;}}if(ok){texsuffix=ci==0?"_Face_N":"_Face_SRO";texmiddle=candidates[ci];break;}}}
 '''
 s=s.replace('u16 expected[160];int e=0;',insert+'u16 expected[160];int e=0;').replace('kind<2?"_Face.SK_":"_Face_D.T_"','kind<2?"_Face.SK_":texmiddle').replace('kind<2?"_Face":"_Face_D"','kind<2?"_Face":texsuffix');(N/'noodle_hair.c').write_text(s)
# Keep texture requests scoped to their owner even when issued by async callbacks.
s=(N/'noodle_hair.c').read_text()
if 'completion_scope' not in s:
 s=s.replace('done_original(closure,result,detail);if(fallback)', 'Scope completion_scope;int completion_at=enter(&completion_scope,actor&&target_kind(*(const uptr*)((char*)actor+0x10b0)));if(completion_at>=0)completion_scope.actor=actor;done_original(closure,result,detail);leave(&completion_scope,completion_at);if(fallback)')
 s=s.replace('texture_original(closure,result,detail);}', 'Scope texture_scope;int texture_at=enter(&texture_scope,actor&&target_kind(*(const uptr*)((char*)actor+0x10b0)));if(texture_at>=0)texture_scope.actor=actor;texture_original(closure,result,detail);leave(&texture_scope,texture_at);}')
 (N/'noodle_hair.c').write_text(s)
env=os.environ.copy();env.update(ZIG_GLOBAL_CACHE_DIR='/workspace/.cache/zig-global',ZIG_LOCAL_CACHE_DIR='/workspace/.cache/zig-local');env['PATH']='/workspace/.venvs/testingdummy/bin:'+env['PATH']
def run(*a):subprocess.run(list(map(str,a)),env=env,check=True)
run('sh',N/'build_native.sh');run(sys.executable,N/'validate_native.py')
# Repeat the real ARM64 scope tests for both additional native face texture types.
s=(N/'validate_native.py').read_text();a=s.index('target=')if 'target='in s else s.index('def request(pid,name):');s=s[:a];s=s.replace('names={};plain=True;',"texture_suffix='D';names={};plain=True;")
s=s.replace('texture="Texture2D\'/Game/Assets/character/RealFace/T_"+name+\'_Face_D.T_\'+name+"_Face_D\'"', 'texture="Texture2D\'/Game/Assets/character/RealFace/T_"+name+\'_Face_\'+texture_suffix+\'.T_\'+name+"_Face_"+texture_suffix+"\'"')
s+='''def request(pid,name):
 u.mem_write(actor+0x10b0,struct.pack('<Q',pid));fstring(face,name,chars);call(syms['noodle_enable'],1);at=len(events);call(outer,actor,face);return events[at:]
with_texture=True
'''
s+='targets='+repr(targets)+'\n'
s+='''for suffix in ['D','N','SRO']:
 texture_suffix=suffix
 for card,row in targets.items():
  for key in ['4522','4522lg00v0000','4522ep01v0291','4522ep00v0313']:
   es=request(int(card),key);paths=[e[1]for e in es if e[0]=='path'];assert any('T_'+row['prefix']+'_Face_'+suffix in p for p in paths),(card,suffix,paths)
 for card in [4522,53878485695166,70379213169392,89135066911146,88044950524330]:
  es=request(card,'4522');assert all('ND0'not in e[1]for e in es if e[0]=='path')
print('THREE_FACE_TEXTURE_TYPES_EXACT_SCOPE_AND_FOUR_VARIANTS_PASS')
''';(N/'validate_texture_types.py').write_text(s);run(sys.executable,N/'validate_texture_types.py')
for card in targets:
 for f in (P/('android-r5-v2-'+card)/'asset').glob('*'):
  if '_Face_N.'in f.name or'_Face_SRO.'in f.name:shutil.copyfile(f,N/'asset'/f.name)
s=(N/'build_full_container.py').read_text()
if "for suffix in ['N','SRO']"not in s:
 a=s.index('chunks=[];');s=s[:a]+'''for kind,row in targets.items():
 prefix=row['prefix']
 for suffix in ['N','SRO']:
  recipes += [('T_'+v.replace('4522',prefix,1)+'_Face_'+suffix,mats,'character/RealFace/T_133157_Face_'+suffix+'.uasset',{})for v in ['4522','4522lg00v0000','4522ep01v0291','4522ep00v0313']]
'''+s[a:];(N/'build_full_container.py').write_text(s)
run(sys.executable,N/'build_full_container.py');t=N/'deploy/work/tools';l=N/'deploy/livedata';shutil.copyfile(N/'libnoodle_hair.so',t/'libnoodle_hair.so');sha=hashlib.sha256((t/'libnoodle_hair.so').read_bytes()).hexdigest();m['native_sha256']=sha
for p in [N/'noodle_hair.py',t/'noodle_hair.py']:
 s=p.read_text();s=re.sub("HOOK_SHA='[0-9a-f]{64}'","HOOK_SHA="+repr(sha),s);p.write_text(s)
for ext in ['pak','utoc','ucas']:
 name='pc9298_mobile_and.'+ext;data=(N/'container'/name).read_bytes();(l/name).write_bytes(data);m['files'][name]={'size':len(data),'sha256':hashlib.sha256(data).hexdigest()}
(t/'noodle_bundle.json').write_text(json.dumps(m,indent=2))
for name in ['validate_install.py','validate_runtime.py','read_assets.py']:run(sys.executable,N/name)
print('ALL_MAPS_AND_SCOPED_RUNTIME_UPGRADED',N.name,flush=True)
