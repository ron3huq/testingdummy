"""Publish the complete pinned build before V19 compatibility checks.
All original SHA/size/path validation remains enabled; cache metadata supplies
only a monotonic version counter, never replacement content for this build.
"""
import json
from pathlib import Path
ROOT=None

def install(root):
 global ROOT
 ROOT=Path(root).resolve()
 import live_manifest_upgrade as upgrade
 if getattr(upgrade._path,'_private_v191',False):return
 original=upgrade._path
 def path(files_root,name):
  result=original(files_root,name)
  if name=='embedded-gateway/livedata/dt870_mobile_and.cpk':
   result=ROOT/'livedata/dt870_ui74_mobile_and.cpk'
  elif name.startswith('embedded-gateway/livedata/pc9311_mobile_and.'):
   import photo_editor
   if photo_editor.STATE.is_file():
    state=json.loads(photo_editor.STATE.read_text());row=state.get('files',{}).get(Path(name).name)
    if row:result=(photo_editor.LIVE.parent/row['relative']).resolve()
  if not result.resolve().is_relative_to(Path(files_root).resolve()):raise ValueError('Private resource escaped files root')
  return result
 path._private_v191=True;upgrade._path=path

def identities(ver):
 return (ver.get('targetAppVersion'),ver.get('dt870Hash'),ver.get('dt870FileSize'),sorted((r['name'],r.get('hash'),r.get('hashFileSize'),r.get('utoc'),r.get('utocFileSize'),r.get('ucas'),r.get('ucasFileSize'))for r in ver.get('dt880',[])))

def apply(original,value,port):
 if not isinstance(value,dict)or not isinstance(value.get('version_file'),str)or not isinstance(value.get('livedata_list'),list):return original(value)
 import noodle_hair,extras_runtime,manager_runtime,kits_runtime,private_bundles,photo_editor,live_manifest_upgrade as upgrade
 prepared=photo_editor.advertise(private_bundles.advertise(kits_runtime.advertise(manager_runtime.advertise(extras_runtime.advertise(noodle_hair.advertise(value,port),port),port),port),port),port)
 ver=json.loads(prepared['version_file']);base=int(ver['version'])+500000;cache=ROOT.parent/'Download/version.bin'
 if cache.is_file():
  try:
   cached=upgrade.decode_native_version(cache.read_bytes());old=upgrade._revision(cached)
   if cached.get('targetAppVersion')==ver.get('targetAppVersion'):
    base=max(base,old if identities(cached)==identities(ver)else old+1)
  except (ValueError,TypeError,KeyError,UnicodeError):pass
 if not 0<base<2**31:raise ValueError('Private live version is outside the native range')
 ver['version']=base;prepared=dict(prepared,version_file=json.dumps(ver,separators=(',',':')))
 return original(prepared)


def pin_rebased_kits(namespace):
 """Retain exact original validation for all files; update only the rebased CPK identity."""
 from pathlib import Path
 import json
 meta=json.loads(Path(__file__).with_name('kits_bundle.json').read_text())['files']['dt870_mobile_and.cpk']
 for key in ('_SOURCE_CHECKS','_ACTIVE_CHECKS'):
  rows=namespace.get(key)
  if not isinstance(rows,(list,tuple)):continue
  rebuilt=[]
  for item in rows:
   if item.get('name',item.get('source'))=='dt870_mobile_and.cpk':item=dict(item,bytes=meta['size'],sha256=meta['sha256'])
   rebuilt.append(item)
  namespace[key]=tuple(rebuilt)if isinstance(rows,tuple)else rebuilt
 namespace['_active_fingerprint']=None
