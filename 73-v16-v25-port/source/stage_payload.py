from pathlib import Path
import zipfile,json,hashlib,ast,marshal,importlib.util,shutil
repo=Path('/workspace/testingdummy');base=Path('/workspace/ronaldo-work/73-v25-port');out=base/'package';out.mkdir(exist_ok=True)
src=repo/'73-v16-v25-port/source';original=repo/'efootxi-1.3.2/player-faces-v25/Faces-v25-Ronaldo2017-BlenderV3-test.zip'
with zipfile.ZipFile(original) as z:
 for n in z.namelist():
  if n=='HUONG_DAN.md' or n.endswith('gateway_runtime.py'):continue
  p=out/'payload'/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(n))
p=out/'payload/work/tools/noodle_hair.py';s=p.read_text();s=s.replace('3da06a36fb5c434a75c5739af65f16664347477bd653659eb354376410d52f98','efd257d9e41b622d6ecb8f51f7b0a8ee8820113fd427c5572025df1c8eecc7b8').replace('player-faces-v25-2017-blender-v3-test','player-faces-v25-73-v16-port-test')
# Validate every target entry before installing even the first hook.
t=ast.parse(s);entries=[]
for n in ast.walk(t):
 if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='install':
  kw={k.arg:k.value for k in n.keywords}
  if 'entry' in kw:entries.append((ast.literal_eval(kw['entry']),ast.literal_eval(kw['prologue'].args[0])))
assert len(entries)==15
helper='\ndef preflight(base,path):\n    if digest(path)!=ENGINE_SHA:raise RuntimeError("unsupported 73 V16 engine; no patch installed")\n    for entry,expected in '+repr(entries)+':\n        prologue=bytes.fromhex(expected)\n        if C.string_at(base+entry,len(prologue))!=prologue:\n            raise RuntimeError("73 native hook conflict at "+hex(entry)+"; no V25 patch installed")\n\n'
s=s.replace('def worker():',helper+'def worker():').replace('base=matches[0][0];path=matches[0][4]','base=matches[0][0];path=matches[0][4]\n                preflight(base,path)');p.write_text(s);compile(s,str(p),'exec')
meta=out/'payload/work/tools/noodle_bundle.json';j=json.loads(meta.read_text());j['version']='player-faces-v25-73-v16-port-test';j['base_package']='com.efootball.revival.local';j['engine_sha256']='efd257d9e41b622d6ecb8f51f7b0a8ee8820113fd427c5572025df1c8eecc7b8';j['phone_tested']=False;meta.write_text(json.dumps(j,indent=2))
shutil.copy2(p,src/'noodle_hair_73.py');shutil.copy2(src/'bridge_73.py',out/'payload/work/tools/bridge_73.py')
wrapper=(src/'embedded_gateway_wrapper.py').read_text();compiled=importlib.util.MAGIC_NUMBER+b'\0'*12+marshal.dumps(compile(wrapper,'embedded_gateway.py','exec'))
# Only this wrapper changes in the original Python archive. Encrypted modules stay exact.
app=base/'app-v25.imy'
with zipfile.ZipFile('/workspace/ronaldo-work/73-inspect/v16-meta/assets/chaquopy/app.imy') as z,zipfile.ZipFile(app,'w',compression=zipfile.ZIP_DEFLATED) as w:
 for i in z.infolist():w.writestr(i,compiled if i.filename=='embedded_gateway.pyc' else z.read(i.filename))
shutil.copy2(app,out/'app-v25.imy')
manifest=json.load(open('/workspace/ronaldo-work/73-inspect/v16-meta/assets/gateway-release/release-manifest.json'));manifest['release_id']+='-v25-73-test1';paths={x['path'] for x in manifest['files']}
for p in sorted((out/'payload').rglob('*')):
 if not p.is_file():continue
 n=p.relative_to(out/'payload').as_posix();assert n not in paths,n
 manifest['files'].append({'path':n,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(out/'release-manifest-v25.json').write_text(json.dumps(manifest,indent=2));print('payload files',len([p for p in (out/'payload').rglob('*') if p.is_file()]),'preflight entries',len(entries))
