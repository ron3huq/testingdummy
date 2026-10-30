"""Shared immutable RX pages for44 hooks, with separate non-executable target slots.
Arena code is written once, then RX. No MAP_FIXED; entry patch permissions
use the existing atomic branch-install procedure.
"""
import ctypes as C,os,struct,threading,json
from pathlib import Path
_LOCK=threading.RLock();_ARENAS={}
PLANS={0x39ce7d8:'ffc306d1fd7b15a9fc6f16a9fa6717a9',0x39cefe4:'ffc301d1fd7b03a9f72300f9f65705a9',0x39ca65c:'e80f19fcfd7b01a9fc6f02a9fa6703a9',0x388180c:'fd7bbaa9fc6f01a9fa6702a9f85f03a9',59257416: 'ff0307d1fd7b16a9fc6f17a9fa6718a9', 59247036: 'fd7bbaa9fc6f01a9fa6702a9f85f03a9', 53522004: 'ff4307d1fd7b17a9fc6f18a9fa6719a9', 60556320: 'fd7bbba9f90b00f9f85f02a9f65703a9', 60540272: 'fd7bbea9f44f01a9fd030091f40300aa', 60540332: '08dc82522aa440a90000088b28004039', 136560132: 'ff8301d1fd7b03a9f52300f9f44f05a9', 136977992: 'fd7bbea9f30b00f9fd030091f30300aa', 61409440: 'ff4306d1fd7b14a9fcab00f9f85f16a9', 60602204: 'ffc306d1fd7b17a9fc5f18a9f65719a9', 73095344: 'ff8301d1fd7b03a9f52300f9f44f05a9', 60634628: 'ff0301d1fd7b01a9f65702a9f44f03a9', 60636700: 'ff4302d1fd7b03a9fc6f04a9fa6705a9', 60610332: 'ff0304d1fd7b0ca9f76b00f9f6570ea9', 60611344: 'ff4307d1fd7b17a9fcc300f9fa6719a9', 121102428: 'fd7bbaa9fb0b00f9fa6702a9f85f03a9', 136563156: 'ffc300d1fd7b01a9f44f02a9fd430091', 136562900: 'ff0301d1fd7b02a9f44f03a9fd830091', 136923344: '280040b909bb80520a8018910929a99b', 136923372: 'ff0301d1fd7b01a9f65702a9f44f03a9', 136595160: 'ff0301d1fd7b02a9f31b00f9fd830091', 54665332: 'ff4301d1fd7b02a9f51b00f9f44f04a9', 54664760: 'ff4301d1fd7b02a9f51b00f9f44f04a9', 59357124: 'ff4306d1fd7b14a9fc6715a9f85f16a9', 59358164: 'ff4306d1fd7b14a9fc6715a9f85f16a9', 59358684: 'ff4306d1fd7b14a9fc6715a9f85f16a9', 136564688: 'fd7bbea9f44f01a9fd030091f30300aa', 136564940: 'fd7bbea9f30b00f9fd030091f30300aa', 137038356: 'e8031f2a3f30007128050054e903012a', 109906024: 'fd7bbfa9fd03009102600091e00301aa', 109898564: 'fd7bbaa9fc6f01a9fa6702a9f85f03a9', 109949264: '800000b4080040f9032d40f960001fd6', 60863116: 'fd7bbaa9fc6f01a9fa6702a9f85f03a9', 61173224: 'ff0306d1fd7b12a9fc6f13a9fa6714a9', 137054844: '00280191c0035fd60850218b3f0c0071', 61167724: 'fd7bbca9f85f01a9f65702a9f44f03a9', 61167676: 'fd7bbea9f44f01a9fd030091f303002a', 61184292: 'ff4305d1fd7b10a9fc8b00f9f85f12a9', 49574744: 'ff8301d1fd7b03a9f52300f9f44f05a9', 49565260: 'fd7bbaa9fc6f01a9fa6702a9f85f03a9'}
SLOT=88;RETURN=32

def branch(source,target):
 delta=target-source
 if delta%4 or not -(1<<27)<=delta<(1<<27):raise ValueError('ARM64 branch out of range')
 return 0x14000000|((delta>>2)&0x3ffffff)

def jump(target):return struct.pack('<IIQ',0x58000050,0xd61f0200,target)

def relocated(prologue,target):
 word=struct.unpack_from('<I',prologue)[0]
 if(word&0x7e000000)in(0x34000000,0x36000000)or(word&0xff000010)==0x54000000:
  bits=14 if(word&0x7e000000)==0x36000000 else 19;mask=(1<<bits)-1;imm=(word>>5)&mask
  if imm&(1<<(bits-1)):imm-=1<<bits
  local=(word&~(mask<<5))|(5<<5)
  return struct.pack('<I',local)+jump(target+4)+jump(target+imm*4)
 return prologue[:4]+jump(target+4)

def candidates(entries,targets,page,preferred_index=None):
 offsets=[i*SLOT for i in range(len(targets))]
 def gaps(lo,hi):
  out=set()
  for left,right in zip(entries,entries[1:]):
   low=(max(left[1],lo)+page-1)&~(page-1);high=min(right[0]-page,hi)&~(page-1)
   if low<=high:out.update((low,high,min(max(targets[0]&~(page-1),low),high)))
  return out
 common=gaps(max(t-(1<<27)-o for t,o in zip(targets,offsets)),min(t+(1<<27)-4-o for t,o in zip(targets,offsets)))
 options=set(common)
 if preferred_index is not None:
  t=targets[preferred_index];o=offsets[preferred_index];options.update(gaps(t-(1<<27)-o,t+(1<<27)-4-o))
 def coverage(p):return sum(-(1<<27)<=p+o-t<(1<<27)for t,o in zip(targets,offsets))
 return sorted(options,key=lambda p:(-coverage(p),abs(p-targets[0]),p))

def report(base):
 try:
  pools=_ARENAS[base];bound=sum(p.bound for p in pools);p=Path(__file__).with_name('hook-arena-status.json');temp=p.with_suffix('.tmp');temp.write_text(json.dumps({'version':'73-ui7.16','state':'ALL_TARGETS_BOUND'if bound==len(PLANS)else'RX_ARENA_READY','arena_pages':len(pools),'system_page_bytes':pools[0].page,'planned_slots':len(PLANS),'bound_targets':bound,'arena_code_immutable_RX':True},indent=2));temp.replace(p)
 except (OSError,KeyError,IndexError):pass

class Arena:
 def __init__(self,base,maps,flush,preferred_entry):
  self.base=base;self.entries=sorted(PLANS);self.index={e:i for i,e in enumerate(self.entries)};self.page=os.sysconf('SC_PAGE_SIZE')
  if len(self.entries)*SLOT>self.page:raise RuntimeError('Hook arena exceeds one system page')
  self.targets=(C.c_uint64*len(self.entries))();self.libc=C.CDLL('libc.so',use_errno=True)
  self.libc.mmap.argtypes=[C.c_void_p,C.c_size_t,C.c_int,C.c_int,C.c_int,C.c_long];self.libc.mmap.restype=C.c_void_p
  self.libc.mprotect.argtypes=[C.c_void_p,C.c_size_t,C.c_int];self.libc.mprotect.restype=C.c_int
  self.libc.munmap.argtypes=[C.c_void_p,C.c_size_t];self.libc.munmap.restype=C.c_int
  targets=[base+e for e in self.entries];preferred_index=self.index[preferred_entry];hints=candidates(maps(),targets,self.page,preferred_index);address=None
  for hint in hints:
   found=self.libc.mmap(hint,self.page,3,0x22,-1,0)
   if found in(None,C.c_void_p(-1).value):continue
   try:
    branch(base+preferred_entry,found+preferred_index*SLOT)
   except ValueError:self.libc.munmap(found,self.page);continue
   address=found;break
  if address is None:raise RuntimeError('No shared hook page in branch range: '+str(len(hints))+' hints')
  try:
   code=bytearray(struct.pack('<I',0xd503201f)*(self.page//4))
   for i,entry in enumerate(self.entries):
    # Load the hook address indirectly from a separate ordinary RW array.
    prefix=struct.pack('<IIIIQQ',0x58000090,0xf9400210,0xd61f0200,0xd503201f,C.addressof(self.targets)+i*8,0)
    block=prefix+relocated(bytes.fromhex(PLANS[entry]),base+entry);assert len(block)<=SLOT;code[i*SLOT:i*SLOT+len(block)]=block
   C.memmove(address,bytes(code),len(code));flush(address,self.page)
   if self.libc.mprotect(address,self.page,5)!=0:raise OSError(C.get_errno(),'Cannot publish RX hook arena')
  except BaseException:self.libc.munmap(address,self.page);raise
  self.address=address;self.bound=0
 def slot(self,entry,prologue):
  if PLANS.get(entry)!=prologue.hex():raise RuntimeError('Unregistered hook prologue')
  address=self.address+self.index[entry]*SLOT;branch(self.base+entry,address);return address
 def reachable(self,entry):
  delta=self.address+self.index[entry]*SLOT-(self.base+entry)
  return -(1<<27)<=delta<(1<<27)
 def bind(self,entry,target):
  index=self.index[entry]
  if not self.targets[index]:self.bound+=1
  self.targets[index]=target
  if sum(p.bound for p in _ARENAS.get(self.base,[]))==len(PLANS):report(self.base)

def install(g,base,path,entry,prologue,hook_name,configure_name):
 if g['digest'](path)!=g['ENGINE_SHA']:raise RuntimeError('Unsupported73 engine; no patch installed')
 # Module filenames are fixed trusted startup code, not request input.
 libname='libnoodle_hair.so'if g['__name__']=='noodle_hair'else'libselect_team.so'
 libpath=g['HERE']/libname
 if g['digest'](libpath)!=g['HOOK_SHA']:raise RuntimeError('Hook binary checksum mismatch')
 key=(base,entry);registry=g['_installed_hooks']
 with _LOCK:
  if key in registry:
   if not g['owned_entry'](base,entry,prologue):raise RuntimeError('Installed mod hook changed; restart game')
   return registry[key][2]
  if PLANS.get(entry)!=prologue.hex():raise RuntimeError('Unregistered hook entry')
  target=base+entry;region=next((r for r in g['maps']()if r[0]<=target and target+16<=r[1]and'r'in r[2]and'x'in r[2]),None)
  if region is None or C.string_at(target,16)!=prologue:raise RuntimeError('Native prologue mismatch; no patch installed')
  hook=C.CDLL(str(libpath));configure=getattr(hook,configure_name);configure.argtypes=[C.c_size_t,C.c_size_t];configure.restype=None
  hook.flush.argtypes=[C.c_void_p,C.c_size_t];hook.flush.restype=None;hook.store_instruction.argtypes=[C.c_void_p,C.c_uint32];hook.store_instruction.restype=None
  pools=_ARENAS.setdefault(base,[])
  arena=next((p for p in pools if p.reachable(entry)),None)
  if arena is None:
   arena=Arena(base,g['maps'],hook.flush,entry);pools.append(arena);report(base)
  cave=arena.slot(entry,prologue);configure(base,cave+RETURN);arena.bind(entry,C.cast(getattr(hook,hook_name),C.c_void_p).value)
  page=arena.page;target_page=target&~(page-1);oldprot=(1 if'r'in region[2]else 0)|(2 if'w'in region[2]else 0)|(4 if'x'in region[2]else 0)
  if arena.libc.mprotect(target_page,page,oldprot|2)!=0:raise OSError(C.get_errno(),'Cannot change hook entry permissions')
  try:
   if C.string_at(target,16)!=prologue:raise RuntimeError('Native entry changed during installation')
   g['_keep'].extend([hook,arena]);hook.store_instruction(target,branch(target,cave));registry[key]=(target,cave,hook)
   if '_installed_entries'in g:g['_installed_entries'].append(hex(entry))
   hook.flush(target,4)
  finally:
   if arena.libc.mprotect(target_page,page,oldprot)!=0:raise OSError(C.get_errno(),'Cannot restore hook entry permissions; restart game')
  return hook
