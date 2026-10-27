"""Verified private hero meshes and player photographs, without replacing the existing face pack."""
from pathlib import Path
import functools,json
from mod_integrity import digest
HERE=Path(__file__).resolve().parent
@functools.lru_cache(maxsize=1)
def verified():
 doc=json.loads((HERE/'private_bundles.json').read_text());live=HERE.parents[1]/'livedata'
 for name,row in doc['files'].items():
  p=live/name
  if p.stat().st_size!=row['size']or digest(p)!=row['sha256']:raise ValueError('Private hero/art payload mismatch: '+name)
 return doc

def advertise(value,port):
 if not isinstance(value,dict)or not isinstance(value.get('livedata_list'),list)or not isinstance(value.get('version_file'),str):return value
 doc=verified();version=json.loads(value['version_file']);names=set(doc['files']);out=dict(value);out['livedata_list']=[x for x in value['livedata_list']if not isinstance(x,dict)or x.get('name')not in names]
 for container in ['pc9305','pc9306','pc9307']:
  stem=container+'_mobile_and';r={ext:doc['files'][stem+'.'+ext]for ext in ['pak','utoc','ucas']};item={'name':container,'hash':r['pak']['sha256'],'hashFileSize':r['pak']['size'],'ucas':r['ucas']['sha256'],'ucasFileSize':r['ucas']['size'],'utoc':r['utoc']['sha256'],'utocFileSize':r['utoc']['size']};prior=next((x for x in version['dt880']if isinstance(x,dict)and x.get('name')==container),None)
  if prior!=item:version['version']+=710
  version['dt880']=[x for x in version['dt880']if not isinstance(x,dict)or x.get('name')!=container]+[item]
  out['livedata_list'] +=[{'name':stem+'.'+ext,'size':r[ext]['size'],'url':'http://127.0.0.1:'+str(port)+'/livedata/'+stem+'.'+ext}for ext in ['pak','utoc','ucas']]
 if version['version']>=2**31:raise ValueError('Resource version overflow')
 out['version_file']=json.dumps(version,separators=(',',':'));return out
