from pathlib import Path
import importlib.util,types,json,struct,sys
from elftools.elf.elffile import ELFFile
from unicorn import Uc,UC_ARCH_ARM64,UC_MODE_ARM,UC_HOOK_CODE
from unicorn.arm64_const import *
b=Path('/workspace/ronaldo-work/73-v25-full');p=b/'payload/work/tools/select_team_runtime.py';spec=importlib.util.spec_from_file_location('select73_test',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
f=open('/workspace/ronaldo-work/73-inspect/v16-meta/lib/arm64-v8a/libUE4.so','rb');elf=ELFFile(f);segs=list(elf.iter_segments())
def at(addr,n):
 for s in segs:
  if s['p_type']=='PT_LOAD' and s['p_vaddr']<=addr<s['p_vaddr']+s['p_filesz']:
   f.seek(s['p_offset']+addr-s['p_vaddr']);return f.read(n)
 raise AssertionError(hex(addr))
m.C=types.SimpleNamespace(string_at=at);path='/workspace/ronaldo-work/73-inspect/v16-meta/lib/arm64-v8a/libUE4.so';m.preflight(0,path)
entries=json.loads((b/'hook-entries.json').read_text());assert len(entries)==23
m.C.string_at=lambda addr,n: b'\0'*n if addr==entries[-1][0] else at(addr,n)
try:m.preflight(0,path);raise AssertionError('late conflict accepted')
except RuntimeError:pass
# Execute the actual relocated entity-hook first instruction, both branch paths.
target=0x68db150;cave=0x0b100000;code=m.relocated_first(at(target,16),target);outcomes=[]
for value,dest in [(0,target+16),(123,target+4)]:
 u=Uc(UC_ARCH_ARM64,UC_MODE_ARM);u.mem_map(cave,4096);u.mem_write(cave+32,code);u.mem_map(target&~4095,4096);u.reg_write(UC_ARM64_REG_X0,value)
 def stop(uc,addr,size,data):
  if addr in [target+4,target+16]:outcomes.append(addr);uc.emu_stop()
 u.hook_add(UC_HOOK_CODE,stop);u.emu_start(cave+32,cave+4096,count=20);assert outcomes[-1]==dest
checks=['all_23_native_hook_prologues_match_real_73_engine','late_hook_conflict_detected_before_any_patch','CBZ_zero_path_reaches_original_target','CBZ_nonzero_path_reaches_original_fallthrough']
# No new My League inline hook may collide with the already working face hooks.
face=json.loads(Path('/workspace/ronaldo-work/73-inspect/engine-offset-comparison.json').read_text());face_hooks={0x3883248,0x38809bc,0x330ae54,0x39c0420,0x39bc570,0x39bc5ac,0x823be04,0x82a1e48,0x3a908a0,0x39cb75c,0x45b58b0,0x39d3604,0x39d3e1c,0x39cd71c,0x39cdb10};assert not face_hooks&{row[0] for row in entries};checks.append('no_overlap_with_15_working_face_hook_entries')
# Independently check the retained eight kits, font maps and UI thumbnails.
sys.path.insert(0,'/workspace/testingdummy/efootxi-1.3.2/player-faces-v25/source');from iostore import Toc
t=Toc('/workspace/ronaldo-work/73-v25-port/package/payload/livedata/pc9298_mobile_and.utoc');paths=set(t.files)
for tid in [351,352,242,245]:
 for slot in [1,2]:
  for kind in ['Uni','FontName','FontBack','FontChest','FontLeg']:assert f'character/Uniform/LowTextures/T_u{tid:04d}p{slot}_{kind}_D.uasset' in paths
  for suffix in ['_r','_full_r']:assert f'ui/Data/Thumbnail/Uniform/uni{tid*16384+slot-1}{suffix}.uasset' in paths
checks.append('eight_kit_textures_32_font_textures_16_thumbnails_present')
(b/'runtime-validation.json').write_text(json.dumps({'passed':True,'checks':checks,'phone_tested':False},indent=2));print('RUNTIME_PASS',len(checks))
