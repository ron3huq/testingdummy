"""Chain only the verified upstream V19 appearance entry. Reject every other foreign hook."""
import ctypes as C,struct,time
ENTRY=0x68ceb44
_known={}
def destination(source,word):
 if word&0xfc000000!=0x14000000:return None
 imm=word&0x3ffffff
 if imm&(1<<25):imm-=1<<26
 return source+imm*4
def wait(base):
 import editor_appearance_runtime as original
 for _ in range(150):
  state=original._state
  if state is not None:
   if state.get('base')!=base:raise RuntimeError('V19 appearance engine base differs')
   address=base+ENTRY;dest=state['page']+256
   if destination(address,C.c_uint32.from_address(address).value)!=dest:raise RuntimeError('V19 appearance hook ownership changed')
   _known[address]=dest
   return
  if str(original._status).startswith('error'):raise RuntimeError('V19 appearance runtime did not initialize: '+str(original._status))
  time.sleep(.1)
 raise RuntimeError('V19 appearance runtime was not ready; no overlapping mod hook installed')
def accepted(address,expected):
 dest=_known.get(address)
 if dest is None:return False
 raw=C.string_at(address,len(expected))
 return raw[4:]==expected[4:] and destination(address,struct.unpack_from('<I',raw)[0])==dest
def target(address):return _known.get(address)
