"""Advertise and verify the isolated cuff meshes; original face container stays exact."""
from pathlib import Path
import functools,json,hashlib
HERE=Path(__file__).resolve().parent
@functools.lru_cache(maxsize=1)
def verified():
 meta=json.loads((HERE/'rolled_bundle.json').read_text());live=HERE.parents[1]/'livedata'
 for name,row in meta['files'].items():
  p=live/name
  if p.stat().st_size!=row['size']or hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']:raise ValueError('Cuff mesh payload does not match manifest: '+name)
 return meta

def advertise(value,port):
 if not isinstance(value,dict)or not isinstance(value.get('livedata_list'),list)or not isinstance(value.get('version_file'),str):return value
 meta=verified();version=json.loads(value['version_file']);stem='pc9299_mobile_and';rows=meta['files'];r={ext:rows[stem+'.'+ext]for ext in ['pak','utoc','ucas']}
 item={'name':'pc9299','hash':r['pak']['sha256'],'hashFileSize':r['pak']['size'],'ucas':r['ucas']['sha256'],'ucasFileSize':r['ucas']['size'],'utoc':r['utoc']['sha256'],'utocFileSize':r['utoc']['size']}
 previous=next((x for x in version['dt880']if isinstance(x,dict)and x.get('name')=='pc9299'),None)
 if previous!=item:
  version['version']+=19
  if version['version']>=2**31:raise ValueError('Live-data version overflow')
 version['dt880']=[x for x in version['dt880']if not isinstance(x,dict)or x.get('name')!='pc9299']+[item]
 out=dict(value);out['version_file']=json.dumps(version,separators=(',',':'));names=set(rows)
 out['livedata_list']=[x for x in value['livedata_list']if not isinstance(x,dict)or x.get('name')not in names]
 out['livedata_list'] += [{'name':stem+'.'+ext,'size':r[ext]['size'],'url':'http://127.0.0.1:'+str(port)+'/livedata/'+stem+'.'+ext}for ext in ['pak','utoc','ucas']]
 return out
