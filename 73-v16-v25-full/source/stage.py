from pathlib import Path
import shutil,json,hashlib,ast
old=Path('/workspace/ronaldo-work/73-v25-port/package');base=Path('/workspace/ronaldo-work/73-v25-full');out=base/'payload/work/tools';out.mkdir(parents=True,exist_ok=True);repo=Path('/workspace/testingdummy');src=repo/'73-v16-v25-full/source';hot=repo/'efootxi-1.3.2/hotfix-v18';v25=repo/'efootxi-1.3.2/player-faces-v25/source/deploy/work/tools'
for name in ['myleague_realism.py','myleague_worlds.py','myleague_balance.py','myleague_custom.json','myleague_editor.json','myleague_packs.py','myleague_team_snapshot.py']:
 shutil.copy2(hot/name,out/name)
for name in ['native_overall.py','team_kits.py']:shutil.copy2(Path('/workspace/ronaldo-work/73-inspect/old-extra')/name,out/name)
shutil.copy2(src/'myleague_73.py',out/'myleague_73.py')
import gzip
canonical=json.loads(Path('/workspace/ronaldo-work/73-v25-full/android/user-gateway/outputs/reference/canonical_rosters.json').read_text())
(out/'myleague_base_rosters.json.gz').write_bytes(gzip.compress(json.dumps({k:canonical[k] for k in ['rosters','positions']},separators=(',',':')).encode(),mtime=0))
shutil.copy2(base/'native-build/libselect_team.so',out/'libselect_team.so')
new_native_sha=hashlib.sha256((out/'libselect_team.so').read_bytes()).hexdigest()
select=(v25/'select_team_runtime.py').read_text().replace('1f1ad4ffee08464c01fd31bafb05e73a39a2eab987b3c726c121f768aba92292',new_native_sha).replace('3da06a36fb5c434a75c5739af65f16664347477bd653659eb354376410d52f98','efd257d9e41b622d6ecb8f51f7b0a8ee8820113fd427c5572025df1c8eecc7b8').replace('native-hotfix-v18-faces-v10-sleeves','v25-73-full1')
# Audit direct and loop-based hook entries. Preflight all before the menu hook.
t=ast.parse(select);es=[(0x737e05c,'fd7bbaa9fb0b00f9fa6702a9f85f03a9')]
for n in ast.walk(t):
 if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='install':
  kw={x.arg:x.value for x in n.keywords}
  if isinstance(kw.get('entry'),ast.Constant):es.append((ast.literal_eval(kw['entry']),ast.literal_eval(kw['prologue'].args[0])))
for a in [0x82b4a7c,0x3a5586c,0x3a5583c,0x3a59924]:es.append((a,'fd7bbfa9fd030091'))
# The loop install uses an eight-byte default; fetch full expected 16-byte prologues from the original source engine, verified against 73 below.
from elftools.elf.elffile import ELFFile
f=open('/workspace/ronaldo-work/apk/lib/arm64-v8a/libUE4.so','rb');elf=ELFFile(f)
for i,(a,hexs) in enumerate(es):
 if len(hexs)==16:
  for seg in elf.iter_segments():
   if seg['p_type']=='PT_LOAD' and seg['p_vaddr']<=a<seg['p_vaddr']+seg['p_filesz']:
    f.seek(seg['p_offset']+a-seg['p_vaddr']);es[i]=(a,f.read(16).hex())
assert len(es)==23,len(es)
helper='\ndef preflight(base,path):\n    if digest(path)!=ENGINE_SHA:raise RuntimeError("unsupported 73 V16 engine")\n    for entry,expected in '+repr(es)+':\n        if C.string_at(base+entry,16)!=bytes.fromhex(expected):\n            raise RuntimeError("My League hook conflict at "+hex(entry)+"; no My League hook installed")\n\n'
select=select.replace('def worker():',helper+'def worker():').replace('base = matches[0][0]','base = matches[0][0]\n                preflight(base,matches[0][4])')
# Reuse the V25 face installer's already tested whole-gap hint selection.
start=select.index('    candidates = []');end=select.index('    cave = None',start)
select=select[:start]+"    from noodle_hair import trampoline_hints\n    candidates = trampoline_hints(entries,target,page)\n"+select[end:]
# Preserve the target of a conditional first instruction in the optional entity hook.
reloc="""
def relocated_first(prologue, target):
    word=struct.unpack('<I',prologue[:4])[0]
    if (word & 0x7e000000) in (0x34000000,0x36000000) or (word & 0xff000010)==0x54000000:
        bits,shift=(14,5) if (word & 0x7e000000)==0x36000000 else (19,5)
        mask=(1<<bits)-1;imm=(word>>shift)&mask
        if imm & (1<<(bits-1)):imm-=1<<bits
        destination=target+imm*4
        local=(word & ~(mask<<shift)) | (5<<shift)
        return struct.pack('<I',local)+jump(target+4)+jump(destination)
    return prologue[:4]+jump(target+4)

"""
select=select.replace('def install(base,',reloc+'def install(base,')
select=select.replace("code = jump(hookaddr) + b'\\0'*16 + prologue[:4] + jump(target+4)","code = jump(hookaddr) + b'\\0'*16 + relocated_first(prologue,target)")
assert 'prologue[:4] + jump(target+4)' not in select
(out/'select_team_runtime.py').write_text(select);(src/'select_team_runtime_73.py').write_text(select)
# Snapshot labels follow the 73 engine too.
p=out/'myleague_team_snapshot.py';p.write_text(p.read_text().replace('3da06a36fb5c434a75c5739af65f16664347477bd653659eb354376410d52f98','efd257d9e41b622d6ecb8f51f7b0a8ee8820113fd427c5572025df1c8eecc7b8'))
bridge=(repo/'73-v16-v25-port/source/bridge_73.py').read_text();bridge=bridge.replace('    existing.start()\n    return existing','''    existing.start()
    try:
        import select_team_runtime
        select_team_runtime.start()
        import myleague_73
        myleague_73.install()
    except Exception as exc:
        import json
        (tools / 'myleague-73-status.json').write_text(json.dumps({'state':'ERROR','error':str(exc),'version':'v25-73-full1'},indent=2))
    return existing''');(out/'bridge_73.py').write_text(bridge);(src/'bridge_73.py').write_text(bridge)
meta=json.loads((old/'payload/work/tools/noodle_bundle.json').read_text());meta['appearance_files']['libselect_team.so']=new_native_sha;meta['appearance_files']['select_team_runtime.py']=hashlib.sha256((out/'select_team_runtime.py').read_bytes()).hexdigest();meta['myleague_port']='v25-73-full1';(out/'noodle_bundle.json').write_text(json.dumps(meta,indent=2))
manifest=json.loads((old/'release-manifest-v25.json').read_text());manifest['release_id']+='-full1';rows={r['path']:r for r in manifest['files']}
for p in sorted((base/'payload').rglob('*')):
 if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc':
  n=p.relative_to(base/'payload').as_posix();row={'path':n,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()};rows[n]=row
manifest['files']=list(rows.values());(base/'release-manifest.json').write_text(json.dumps(manifest,indent=2));(base/'hook-entries.json').write_text(json.dumps(es,indent=2));print('ADDED_AND_UPDATED_FILES',len(list(out.iterdir())))
