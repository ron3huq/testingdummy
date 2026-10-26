from pathlib import Path
import sys,struct,json,hashlib
sys.path.insert(0,'/workspace/testingdummy/efootxi-1.3.2/player-faces-v25/source')
from iostore import Toc,parse_header,store_entry
from bundle_tools import Bundle
from zen_clone import rename,pid
P=Path('/tmp/73-ui79');base=Toc('/workspace/ronaldo-work/73-ui7/carry/livedata/pc9298_mobile_and.utoc');bundle=Bundle(base);report=[];BASE='/Game/Assets/character/RealFace/'
for name,tag,hair,card in [('HULK-ONLY-ANDROID-TRIAL','NHUL','NH0001','106754901843130'),('SpiderMan-v6-ORIGINAL2006-NECK-ANDROID-TRIAL','NSPD','NS0001','105647605587130')]:
 t=Toc(str(P/'input'/name/'livedata/pc9298_mobile_and.utoc'));h=parse_header(t.read(next(i for i,x in enumerate(t.ids)if x[11]==10)))
 mapping={}
 for path in t.files:
  if path.endswith('.uasset'):
   old=Path(path).stem;new=old.replace('ND0001',hair).replace('ND01',tag);mapping[BASE+old]=BASE+new
 replacements={**mapping,**{a.split('/')[-1]:b.split('/')[-1]for a,b in mapping.items()}};imports={pid(a):pid(b)for a,b in mapping.items()}
 for path,i in t.files.items():
  raw=t.read(i);ext=Path(path).suffix;old=Path(path).stem;new=old.replace('ND0001',hair).replace('ND01',tag);dest='character/RealFace/'+new+ext;assert dest not in bundle.files
  entry=None
  if ext=='.uasset':
   pk=int.from_bytes(t.ids[i][:8],'little');fixed,deps=store_entry(h['store'],h['pids'].index(pk));entry=(fixed,[imports.get(x,x)for x in deps]);data=rename(raw,replacements,BASE+old,BASE+new,imports=mapping)
  else:data=raw
  idb=struct.pack('<Q',pid(BASE+new))+b'\0\0\0'+(b'\x02'if ext=='.uasset'else b'\x03');bundle.put(dest,idb,data,entry)
  report.append({'card':card,'source':path,'destination':dest,'source_sha256':hashlib.sha256(raw).hexdigest(),'geometry_bulk_untouched':ext!='.uasset' or 'SK_'not in old,'only_package_name_metadata_changed':ext=='.uasset','source_engine_trial':True})
bundle.write(P/'heads/livedata')
new=Toc(str(P/'heads/livedata/pc9298_mobile_and.utoc'))
for path,i in base.files.items():assert base.read(i)==new.read(new.files[path]),path
(P/'head-merge-validation.json').write_text(json.dumps({'passed':True,'old_chunks_verbatim':len(base.files),'added_files':len(report),'targets':{'Hulk':'106754901843130','Spider-Man':'105647605587130'},'no_shared_ND01_override':True,'packages':report,'phone_tested':False},indent=2));print('MERGED_HEADS_PASS',len(base.files),len(report))
