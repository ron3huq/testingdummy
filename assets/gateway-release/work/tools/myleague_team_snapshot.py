"""Decode bounded passive native Team captures. Never call an engine method."""
import ctypes as C,json,struct,hashlib,os
from pathlib import Path
ENGINE_SHA='efd257d9e41b622d6ecb8f51f7b0a8ee8820113fd427c5572025df1c8eecc7b8'
SIZE=16+0x5d4

def decode(blob):
 if len(blob)!=SIZE:raise ValueError('invalid capture length')
 tid,cid,origin,generation=struct.unpack_from('<4I',blob);b=blob[16:]
 if struct.unpack_from('<I',b)[0]>>14!=tid or origin not in (1,2)or cid not in (0,122,125,473,566,128,549,518):raise ValueError('capture identity mismatch')
 n=(struct.unpack_from('<I',b,0x40c)[0]>>9)&127
 if not 11<=n<=40:raise ValueError('native roster count outside editor range')
 ids=[];shirts=[]
 for i in range(n):
  kind,pid=struct.unpack_from('<QQ',b,0x110+16*i)
  if kind!=0 or not 0<pid<2**63:raise ValueError('non-base/native player key; cannot safely edit this roster')
  ids.append(str(pid));shirts.append(struct.unpack_from('<H',b,0x3a2+2*i)[0])
 if len(set(ids))!=n:raise ValueError('duplicate native player keys')
 order=list(b[0x538:0x538+n]);first=order[:11]
 if any(i>=n for i in first)or len(set(first))!=11:raise ValueError('invalid native starting order')
 used=set(first);ordered=first+[]
 for i in order[11:]:
  if i<n and i not in used:ordered.append(i);used.add(i)
 ordered.extend(i for i in range(n)if i not in used)
 plans=[]
 for off in (0x478,0x49a,0x4d8,0x4fa):
  slots=[dict(role=b[off+i],x=b[off+11+2*i],y=b[off+12+2*i])for i in range(11)]
  if any(p['role']>12 or p['x']>52 or p['y']>104 for p in slots):raise ValueError('native formation values outside verified range')
  plans.append(dict(slots=slots,flags=b[off+33]))
 def taker(index):
  if index==255:return None
  if index>=n:raise ValueError('invalid native role reference')
  return ids[index]
 roster=[dict(id=ids[old],shirt=shirts[old],**(plans[0]['slots'][new]if new<11 else dict(role=0,x=0,y=0)))for new,old in enumerate(ordered)]
 return dict(team_id=tid,competition=cid,name=b[4:74].split(b'\0')[0].decode('utf8','replace'),roster=roster,plans=plans,captain=taker(b[0x569]),kickers=[taker(v)for v in b[0x560:0x566]],source='NATIVE_MATCH_CACHE'if origin==2 else'NATIVE_TEAM_LOOKUP',capture_generation=generation,capture_sha256=hashlib.sha256(blob).hexdigest(),native_roster_order=ids,native_match_order=order,verified_formation=True)

_last=None

def export(hook,path=None):
 global _last
 path=path or Path(__file__).with_name('myleague-live-teams.json')
 hook.team_capture_generation.argtypes=[];hook.team_capture_generation.restype=C.c_uint
 hook.team_capture_copy.argtypes=[C.c_uint,C.c_void_p,C.c_uint];hook.team_capture_copy.restype=C.c_uint
 generation=hook.team_capture_generation()
 if generation==_last:return False
 rows=[];errors=[]
 for i in range(1024):
  out=C.create_string_buffer(SIZE);size=hook.team_capture_copy(i,out,SIZE)
  if size==0xffffffff:return False
  if not size:continue
  try:rows.append(decode(out.raw[:size]))
  except ValueError as exc:
   tid,cid,origin,g=struct.unpack_from('<4I',out.raw);errors.append(dict(team_id=tid,competition=cid,error=str(exc),capture_generation=g))
 doc=dict(schema=1,kind='myleague-runtime-teams',version='native-hotfix-v18',engine_sha256=ENGINE_SHA,device_verified=False,capture_generation=generation,teams=rows,errors=errors,note='Passive records observed by existing lookups; no guessed formation. Re-import after changing lineups in game.')
 tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(doc,ensure_ascii=False,indent=2));os.replace(tmp,path);_last=generation;return True
