"""Exact source-card copies scoped to three target IDs, with preserved owned serials."""
from pathlib import Path
import json,copy,hashlib,functools,struct,types
HERE=Path(__file__).resolve().parent
ROWS=json.loads((HERE/'full2-card-copies.json').read_text());TARGETS=set(ROWS)
REV='full2_exact_card_copy_v1'
META_KEYS=['ui7_body_dimensions_v1','ui75_player_model_v1','ui77_innate_skills','ui78_appearance_choices','ui710_equipment','ui711_profiles','ui712_motion','ui718_motion_fields','ui712_photos','ui712_stats']

def clone(target,serial=0):
 p=copy.deepcopy(ROWS[str(target)]['payload']);p['gameplayer_id']={'id':int(target),'serial':int(serial)};return p

def migrate(conn):
 if conn.execute('SELECT 1 FROM meta WHERE key=?',(REV,)).fetchone():return False
 # A scoped recovery record is written before modifications; squad membership and roles are untouched.
 backup={'revision':REV,'rows':{},'meta':{}}
 for table in ['gameplayers','player_pool']:
  backup['rows'][table]=[list(r)for pid in TARGETS for r in conn.execute('SELECT id,serial,json FROM '+table+' WHERE id=?',(int(pid),))]
 backup['careerplan']=[list(r)for pid in TARGETS for r in conn.execute('SELECT id,serial,category,points,at FROM careerplan WHERE id=?',(int(pid),))]
 for key in META_KEYS:
  r=conn.execute('SELECT value FROM meta WHERE key=?',(key,)).fetchone()
  if r:backup['meta'][key]=r[0]
 backup_path=HERE.parents[1]/'outputs/efootball/full2-card-copy-recovery.json';backup_path.parent.mkdir(parents=True,exist_ok=True)
 if not backup_path.exists():
  tmp=backup_path.with_suffix('.tmp');tmp.write_text(json.dumps(backup,ensure_ascii=False));tmp.replace(backup_path)
 with conn:
  for table in ['gameplayers','player_pool']:
   for pid in TARGETS:
    for serial,raw in conn.execute('SELECT serial,json FROM '+table+' WHERE id=?',(int(pid),)).fetchall():
     current=json.loads(raw);p=clone(pid,serial)
     if table=='gameplayers':
      for key in ['games','goal','assist','red_card','is_lock','acquisition_date']:
       if key in current:p[key]=current[key]
     conn.execute('UPDATE '+table+' SET json=? WHERE id=? AND serial=?',(json.dumps(p,ensure_ascii=False),int(pid),serial))
    if table=='player_pool' and not conn.execute('SELECT 1 FROM player_pool WHERE id=?',(int(pid),)).fetchone():
     p=clone(pid);conn.execute('INSERT INTO player_pool(id,serial,rarity,json,source) VALUES(?,?,?,?,?)',(int(pid),0,p.get('default_rarity',4),json.dumps(p),REV))
  for pid in TARGETS:conn.execute('DELETE FROM careerplan WHERE id=?',(int(pid),))
  for pid,row in ROWS.items():
   p=clone(pid);conn.execute('UPDATE managed_cards SET payload=?,fingerprint=?,card_type=?,subtype=?,evidence=? WHERE card_id=?',(json.dumps(p),hashlib.sha256(json.dumps(p,sort_keys=True).encode()).hexdigest(),row['metadata'].get('card_type','LEGENDARY'),row['metadata'].get('subtype',''),json.dumps({'copy_source':row['source']}),pid))
  for key,raw in backup['meta'].items():
   d=json.loads(raw)
   if isinstance(d,dict):
    for pid in TARGETS:d.pop(pid,None)
    conn.execute('UPDATE meta SET value=? WHERE key=?',(json.dumps(d),key))
  conn.execute('INSERT INTO meta(key,value) VALUES(?,?)',(REV,json.dumps({'sources':{k:v['source']for k,v in ROWS.items()}})))
 return True

def install_projection():
 """No recurring whole-card rewrites: normal edits stay editable after the one-time copy."""
 import editor_names,photo_editor
 for pid,row in ROWS.items():editor_names.NAMES[pid]=row['payload'].get('name','')
 photo_editor.SUPPLIED_ART_IDS=set(photo_editor.SUPPLIED_ART_IDS)-TARGETS
 import motion_editor
 donors=motion_editor.donors()
 for pid,row in ROWS.items():
  p=row['payload'];name=p.get('name','')
  donors[pid]={'id':pid,'name':name,'role':p['parameters'][0],'fold':motion_editor.fold(name)}
 import editor_portraits
 source_list=editor_portraits.sources
 if not getattr(source_list,'_full2_original_sources',False):
  @functools.wraps(source_list)
  def sources(root):
   rows=list(source_list(root));toc=Path(root)/'livedata/pc9324_mobile_and.utoc';ucas=toc.with_suffix('.ucas')
   if toc.is_file()and ucas.is_file():rows.append((toc,(toc.stat().st_size,toc.stat().st_mtime_ns,ucas.stat().st_size,ucas.stat().st_mtime_ns)))
   return rows
  sources._full2_original_sources=True;editor_portraits.sources=sources
 original=editor_portraits.portrait
 if not getattr(original,'_full2_original_copies',False):
  mapping={'89138288266704':'9500031','88044145348047':'56323','106782013894690':'9500027'}
  @functools.wraps(original)
  def portrait(root,identity):return original(root,mapping.get(str(identity),identity))
  portrait._full2_original_copies=True;editor_portraits.portrait=portrait


def routes():
 return [
  {'cardId':89138288266704,'suiteDonorId':89133724764840,'portraitKey':'9500031','modelNativeId':56334},
  {'cardId':88044145348047,'suiteDonorId':89136418985303,'portraitKey':'9500090','modelNativeId':56323},
  {'cardId':106782013894690,'suiteDonorId':89139630444046,'portraitKey':'9500027','modelNativeId':56331}]

def bind(original):
 import diy_runtime as diy
 # Reuse the source portrait chunks. No re-encoding, scaling, or extra Live Update container.
 f=diy.prepare_binding(original,routes())[0]
 payload=diy.capture(f)
 # Original 56323 uses the older five-digit key. Preserve the fixed native route layout
 # while substituting its exact SSO/UTF-16 name and integer draw key in the newly added row.
 old=payload['blob_hex'];b=bytes.fromhex(old)
 def sso(text):return bytes([len(text)*2])+text.encode()+bytes(23-len(text))
 for suffix in ['_','f']:
  a=sso('9500090'+suffix);v=sso('56323'+suffix);assert len(a)==len(v)==24
  assert b.count(a)==1,(suffix,b.count(a));b=b.replace(a,v)
  a=('9500090'+suffix+'\0').encode('utf-16le');v=('56323'+suffix+'\0').encode('utf-16le');assert b.count(a)==1;b=b.replace(a,v+bytes(len(a)-len(v)))
 a=struct.pack('<Q',9500090);assert b.count(a)==1;b=b.replace(a,struct.pack('<Q',56323))
 new=b.hex();assert len(new)==len(old)
 space=dict(f.__globals__)
 space['__DIY_PAYLOAD__']=dict(payload,blob_hex=new)
 f=types.FunctionType(f.__code__,space,f.__name__,f.__defaults__,f.__closure__)
 assert diy.capture(f)['blob_hex']==new,'Source portrait alias did not survive binding generation'
 return f
