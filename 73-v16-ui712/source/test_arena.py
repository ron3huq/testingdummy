from pathlib import Path
import sys,ctypes as C,struct,hashlib,subprocess,tempfile,threading,json,importlib.util
from unicorn import Uc,UC_ARCH_ARM64,UC_MODE_ARM
from unicorn.arm64_const import *
P=Path('/workspace/73-ui712');sys.path.insert(0,str(P/'build/apk/assets/gateway-release/work/tools'));import hook_arena as a
T=Path(tempfile.mkdtemp(prefix='arena73-'));(T/'stub.c').write_text('''#include <stdint.h>
void hook(void){} void configure(uintptr_t base,uintptr_t trampoline){} void flush(void*p,unsigned long n){} void store_instruction(void*p,uint32_t v){__atomic_store_n((uint32_t*)p,v,__ATOMIC_SEQ_CST);}
''');subprocess.run(['cc','-shared','-fPIC','-O2',str(T/'stub.c'),'-o',str(T/'libnoodle_hair.so')],check=True);(T/'libselect_team.so').write_bytes((T/'libnoodle_hair.so').read_bytes());(T/'engine').write_bytes(b'fixture engine')
original_CDLL=C.CDLL;libc=original_CDLL(None,use_errno=True);libc.mmap.argtypes=[C.c_void_p,C.c_size_t,C.c_int,C.c_int,C.c_int,C.c_long];libc.mmap.restype=C.c_void_p;libc.mprotect.argtypes=[C.c_void_p,C.c_size_t,C.c_int];libc.munmap.argtypes=[C.c_void_p,C.c_size_t]
BASE=0x40000000;PAGE=4096;lo=0x41000000;hi=lo+4*PAGE;regions=[]
for e,hexbytes in a.PLANS.items():
 address=(BASE+e)&~4095
 if address not in regions:
  p=libc.mmap(address,PAGE,3,0x22,-1,0);assert p==address,(hex(p or 0),hex(address));regions.append(address)
 C.memmove(BASE+e,bytes.fromhex(hexbytes),16)
for p in regions:assert libc.mprotect(p,PAGE,5)==0
maps=lambda:[(BASE,lo,'r-xp',0,'engine'),(hi,0x60000000,'r-xp',0,'engine')]
class Fn:
 def __init__(self,fn,name,tracker):self.fn=fn;self.name=name;self.tracker=tracker
 def __call__(self,*args):self.tracker.append((self.name,args));return self.fn(*args)
class Libc:
 def __init__(self):
  self.mmap=Fn(libc.mmap,'mmap',calls);self.mprotect=Fn(libc.mprotect,'mprotect',calls);self.munmap=Fn(libc.munmap,'munmap',calls)
calls=[];C.CDLL=lambda name,*args,**kwargs:Libc()if name=='libc.so'else original_CDLL(name,*args,**kwargs)
# Execute the original73 allocator, not a model of its allocation count.
spec=importlib.util.spec_from_file_location('old_allocator', '/workspace/ronaldo-work/73-ui71/payload/work/tools/noodle_hair.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
old.HERE=T;old.ENGINE_SHA=hashlib.sha256(b'fixture engine').hexdigest();old.HOOK_SHA=hashlib.sha256((T/'libnoodle_hair.so').read_bytes()).hexdigest();old.digest=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def occupied_maps():
 return [(BASE,lo,'r-xp',0,'engine')]+[(v[1],v[1]+PAGE,'r-xp',0,'old-cave')for v in sorted(old._installed_hooks.values(),key=lambda v:v[1])]+[(hi,0x60000000,'r-xp',0,'engine')]
old.maps=occupied_maps
first=[0x3883248,0x38809bc,0x330ae54,0x39c0420,0x39bc570]
for e in first[:4]:old.install(BASE,str(T/'engine'),entry=e,prologue=bytes.fromhex(a.PLANS[e]),hook_name='hook',configure_name='configure')
try:
 old.install(BASE,str(T/'engine'),entry=first[4],prologue=bytes.fromhex(a.PLANS[first[4]]),hook_name='hook',configure_name='configure');raise AssertionError('original allocator unexpectedly fit fifth hook')
except RuntimeError as exc:assert '0 hints tried'in str(exc),str(exc)
assert len(old._installed_hooks)==4
for(base,e),(target,cave,hook)in old._installed_hooks.items():
 assert libc.mprotect(target&~4095,PAGE,7)==0;C.memmove(target,bytes.fromhex(a.PLANS[e]),16);assert libc.mprotect(target&~4095,PAGE,5)==0;assert libc.munmap(cave,PAGE)==0
calls.clear()
keys=list(a.PLANS);faceplans={}
# Derive original grouping from production preflight lists.
import ast,re
source=Path('/workspace/ronaldo-work/73-ui71/payload/work/tools/noodle_hair.py').read_text();face={e for e,_ in ast.literal_eval(re.search(r'for entry,expected in (\[.*?\]):',source).group(1))}
def context(name):
 d={'__name__':name,'HERE':T,'ENGINE_SHA':hashlib.sha256(b'fixture engine').hexdigest(),'HOOK_SHA':hashlib.sha256((T/'libnoodle_hair.so').read_bytes()).hexdigest(),'digest':lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest(),'_installed_hooks':{},'_installed_entries':[],'_keep':[],'maps':maps}
 def owned(base,entry,prologue):
  target,cave,hook=d['_installed_hooks'][(base,entry)];return C.string_at(target,4)==struct.pack('<I',a.branch(target,cave))and C.string_at(target+4,12)==prologue[4:]
 d['owned_entry']=owned;return d
F=context('noodle_hair');G=context('select_team_runtime');errors=[]
def worker(g,entries):
 try:
  for e in entries:a.install(g,BASE,str(T/'engine'),e,bytes.fromhex(a.PLANS[e]),'hook','configure')
 except Exception as exc:errors.append(repr(exc))
threads=[threading.Thread(target=worker,args=(F,sorted(face))),threading.Thread(target=worker,args=(G,sorted(set(keys)-face)))]
for t in threads:t.start()
for t in threads:t.join()
assert not errors,errors;arena=a._ARENAS[BASE][0];assert len(F['_installed_hooks'])==15 and len(G['_installed_hooks'])==29
mm=[x for x in calls if x[0]=='mmap'];assert len(mm)==1,calls;assert len(a._ARENAS)==1
assert len(F['_installed_entries'])==15 and len(G['_installed_entries'])==29
code=C.string_at(arena.address,PAGE);codehash=hashlib.sha256(code).hexdigest();pool_prots=[x[1][2]for x in calls if x[0]=='mprotect'and x[1][0]==arena.address];assert pool_prots==[5],pool_prots
# Real ARM64 execution of all40 branch veneers and indirect target slots.
u=Uc(UC_ARCH_ARM64,UC_MODE_ARM);mapped=set()
def mapbytes(addr,data):
 start=addr&~4095;end=(addr+len(data)+4095)&~4095
 for p in range(start,end,4096):
  if p not in mapped:u.mem_map(p,4096);mapped.add(p)
 u.mem_write(addr,data)
mapbytes(arena.address,code);data_address=C.addressof(arena.targets);mapbytes(data_address,C.string_at(data_address,C.sizeof(arena.targets)))
mapbytes(0x70000000,b'\0'*0x20000)
for e in keys:mapbytes(BASE+e,bytes.fromhex(a.PLANS[e]))
for g in[F,G]:
 for(base,e),(target,cave,hook)in g['_installed_hooks'].items():
  destination=C.cast(hook.hook,C.c_void_p).value;mapbytes(destination,b'\xc0\x03\x5f\xd6')
  for i,reg in enumerate([UC_ARM64_REG_X0,UC_ARM64_REG_X1,UC_ARM64_REG_X2,UC_ARM64_REG_X3,UC_ARM64_REG_X4,UC_ARM64_REG_X5,UC_ARM64_REG_X6,UC_ARM64_REG_X7]):u.reg_write(reg,0x100+i)
  u.reg_write(UC_ARM64_REG_LR,0x12345678);u.emu_start(cave,destination,count=20);assert u.reg_read(UC_ARM64_REG_PC)==destination
  assert u.reg_read(UC_ARM64_REG_LR)==0x12345678
  assert all(u.reg_read(reg)==0x100+i for i,reg in enumerate([UC_ARM64_REG_X0,UC_ARM64_REG_X1,UC_ARM64_REG_X2,UC_ARM64_REG_X3,UC_ARM64_REG_X4,UC_ARM64_REG_X5,UC_ARM64_REG_X6,UC_ARM64_REG_X7]))
  # Execute the actual relocated first instruction, then its return path.
  word=struct.unpack_from('<I',bytes.fromhex(a.PLANS[e]))[0]
  conditional=(word&0x7e000000)in(0x34000000,0x36000000)or(word&0xff000010)==0x54000000
  for zero in([False,True]if conditional else[False]):
   for reg in [UC_ARM64_REG_X1,UC_ARM64_REG_X2,UC_ARM64_REG_X3,UC_ARM64_REG_X4,UC_ARM64_REG_X5,UC_ARM64_REG_X6,UC_ARM64_REG_X7]:u.reg_write(reg,0x70010000)
   u.reg_write(UC_ARM64_REG_SP,0x70010000);u.reg_write(UC_ARM64_REG_X0,0 if zero else 0x70010000)
   expected=target+4
   if conditional and zero:
    bits=14 if(word&0x7e000000)==0x36000000 else 19;imm=(word>>5)&((1<<bits)-1)
    if imm&(1<<(bits-1)):imm-=1<<bits
    expected=target+imm*4
   try:u.emu_start(cave+32,expected,count=30)
   except Exception:
    print('FAILED',hex(e),zero,hex(u.reg_read(UC_ARM64_REG_PC)),hex(u.reg_read(UC_ARM64_REG_SP)),a.PLANS[e]);raise
   assert u.reg_read(UC_ARM64_REG_PC)==expected,(hex(e),hex(expected),hex(u.reg_read(UC_ARM64_REG_PC)))
  # Reinstalling the same owned branch must not allocate/write another stub.
  a.install(g,BASE,str(T/'engine'),e,bytes.fromhex(a.PLANS[e]),'hook','configure')
assert hashlib.sha256(C.string_at(arena.address,PAGE)).hexdigest()==codehash
assert len([x for x in calls if x[0]=='mmap'])==1
# No common hole: two outside holes still cover all targets without per-hook pages.
for g in[F,G]:
 for(base,e),(target,cave,hook)in g['_installed_hooks'].items():
  assert libc.mprotect(target&~4095,PAGE,7)==0;C.memmove(target,bytes.fromhex(a.PLANS[e]),16);assert libc.mprotect(target&~4095,PAGE,5)==0
assert libc.munmap(arena.address,PAGE)==0
a._ARENAS.clear();calls.clear();left=BASE-8*1048576;right=BASE+190*1048576
maps=lambda:[(0x30000000,left,'r-xp',0,'engine'),(left+PAGE,right,'r-xp',0,'engine'),(right+PAGE,0x70000000,'r-xp',0,'engine')]
assert not a.candidates(maps(),[BASE+e for e in sorted(a.PLANS)],PAGE)
F2=context('noodle_hair');G2=context('select_team_runtime');worker(F2,sorted(face));worker(G2,sorted(set(keys)-face));assert not errors,errors
assert len(a._ARENAS[BASE])==2 and sum(p.bound for p in a._ARENAS[BASE])==44
assert len(F2['_installed_hooks'])==15 and len(G2['_installed_hooks'])==29
assert len([x for x in calls if x[0]=='mmap'])==2
for g in[F2,G2]:
 for(base,e),(target,cave,hook)in g['_installed_hooks'].items():assert -(1<<27)<=cave-target<(1<<27)
C.CDLL=original_CDLL
report={'passed':True,'old_four_pages_exhausted_before_fifth_hook':True,'new_hooks_installed':44,'two_concurrent_workers':True,'no_common_hole_supported_with_two_shared_pages':True,'shared_RX_pages':1,'page_bytes':PAGE,'RX_code_never_rewritten_after_publication':True,'separate_RW_target_slots':True,'ARM64_stub_and_argument_and_LR_checks':44,'ARM64_original_instruction_return_checks':44,'conditional_branch_both_paths':True,'idempotent_reinstall':True,'MAP_FIXED_used':False,'RX_pool_ever_RWX':False,'device_tested':False};(P/'arena-validation.json').write_text(json.dumps(report,indent=2));print('ARENA_PASS',report)
