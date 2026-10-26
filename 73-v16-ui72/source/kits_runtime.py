"""Advertise and verify the isolated shirt glyphs and coach portraits."""
from pathlib import Path
import functools,json,hashlib
HERE=Path(__file__).resolve().parent
CPK_SOURCE='dt870_ui72_mobile_and.cpk'
@functools.lru_cache(maxsize=1)
def verified():
 meta=json.loads((HERE/'kits_bundle.json').read_text());live=HERE.parents[1]/'livedata'
 for name,row in meta['files'].items():
  p=live/(CPK_SOURCE if name=='dt870_mobile_and.cpk'else name)
  if p.stat().st_size!=row['size']or hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']:raise ValueError('Shirt/coach payload does not match manifest: '+name)
 return meta

def advertise(value,port):
 if not isinstance(value,dict)or not isinstance(value.get('livedata_list'),list)or not isinstance(value.get('version_file'),str):return value
 meta=verified();version=json.loads(value['version_file']);stem='pc9303_mobile_and';rows=meta['files'];r={ext:rows[stem+'.'+ext]for ext in ['pak','utoc','ucas']}
 item={'name':'pc9303','hash':r['pak']['sha256'],'hashFileSize':r['pak']['size'],'ucas':r['ucas']['sha256'],'ucasFileSize':r['ucas']['size'],'utoc':r['utoc']['sha256'],'utocFileSize':r['utoc']['size']}
 previous=next((x for x in version['dt880']if isinstance(x,dict)and x.get('name')=='pc9303'),None)
 if previous!=item or version.get('dt870Hash')!=rows['dt870_mobile_and.cpk']['sha256']:
  version['version']+=61
  if version['version']>=2**31:raise ValueError('Live-data version overflow')
 version['dt870Hash']=rows['dt870_mobile_and.cpk']['sha256'];version['dt870FileSize']=rows['dt870_mobile_and.cpk']['size']
 version['dt880']=[x for x in version['dt880']if not isinstance(x,dict)or x.get('name')not in('pc9303','pc9301','pc9299')]+[item]
 out=dict(value);out['version_file']=json.dumps(version,separators=(',',':'));names=set(rows)|{'pc9301_mobile_and.'+e for e in['pak','utoc','ucas']}|{'pc9299_mobile_and.'+e for e in['pak','utoc','ucas']}
 out['livedata_list']=[x for x in value['livedata_list']if not isinstance(x,dict)or x.get('name')not in names]
 out['livedata_list'] += [{'name':stem+'.'+ext,'size':r[ext]['size'],'url':'http://127.0.0.1:'+str(port)+'/livedata/'+stem+'.'+ext}for ext in ['pak','utoc','ucas']]
 out['livedata_list'].append({'name':'dt870_mobile_and.cpk','size':rows['dt870_mobile_and.cpk']['size'],'url':'http://127.0.0.1:'+str(port)+'/livedata/'+CPK_SOURCE})
 return out
