from pathlib import Path
import json,sys,struct,hashlib,zipfile
P=Path('/workspace/ronaldo-work/73-ui6');sys.path.insert(0,'/workspace/testingdummy/efootxi-1.3.2/player-faces-v25/source');from iostore import Toc
from bundle_tools import decode_first_texture
r=json.loads((P/'resources-build.json').read_text());new=Toc(str(P/'payload/livedata/pc9303_mobile_and.utoc'));memo={};checks=[]
for row in r['mirrored_kits']:
 srcpath='/workspace/ronaldo-work/73-v25-port/package/payload/livedata/'+row['source_container'] if row['source_container']=='pc9298_mobile_and.utoc'else None
 if row['source_container']=='pc9300_mobile_and.utoc':srcpath='/workspace/ronaldo-work/73-ui5/payload/livedata/'+row['source_container']
 if srcpath is None:srcpath=str(next(Path('/workspace/ronaldo-work/resources').rglob(row['source_container'])))
 src=memo.setdefault(srcpath,Toc(srcpath));relative=row['source'];source=next(k for k in src.files if (src.mount+k).split('/Content/Assets/')[-1]==relative);a=src.read(src.files[source]);b=new.read(new.files[row['destination']]);assert a!=b
 if relative.endswith('.uasset')and any(t in relative for t in['Uni_D','Thumbnail/Uniform']):
  assert decode_first_texture(a).tobytes()==decode_first_texture(b).tobytes(),relative
 checks.append(row['destination'])
assert len(checks)==170
# The historicalMU2008 diffuse is taken from our working face/kit container,
# never from the unmodified whiteTelstar resource.
mu=next(x for x in r['mirrored_kits']if x['destination'].endswith('T_u1706p1_Uni_D.uasset'));assert mu['source_container']=='pc9298_mobile_and.utoc'
old=Toc('/workspace/ronaldo-work/73-ui5/payload/livedata/pc9300_mobile_and.utoc');extras=Toc(str(P/'payload/livedata/pc9300_mobile_and.utoc'))
for path,i in old.files.items():
 if '/Coach/'not in path:assert old.read(i)==extras.read(extras.files[path])
original=Toc('/workspace/ronaldo-work/pc0000/PesMobile/Content/Paks/pakchunk0-Android_ETC2.utoc');manager=Toc(str(P/'payload/livedata/pc9302_mobile_and.utoc'))
for path in r['restored_original_manager_assets']:assert manager.read(manager.files[path])==original.read(original.files['PesMobile/Content/Assets/'+path])
# Exercise the real template through the production resource advertisement chain.
sys.path.insert(0,str(P/'payload/work/tools'));import noodle_hair,extras_runtime,manager_runtime,kits_runtime
z=zipfile.ZipFile('/workspace/ronaldo-work/73-v25-port/package/output/73-V16-V25-unsigned.apk');v=json.loads(z.read('assets/gateway-release/work/templates/CMD_LOGIN_LIVEDATA.json'));out=v
# The standalone test tools do not contain the90MB basefacecontainer: its real
# bytes are checked against their unchanged pinned source separately below.
for module in[extras_runtime,manager_runtime,kits_runtime]:out=module.advertise(out,8085);assert module.advertise(out,8085)==out
version=json.loads(out['version_file']);cpk=P/'payload/livedata/dt870_mobile_and.cpk';assert version['dt870Hash']==hashlib.sha256(cpk.read_bytes()).hexdigest()and version['dt870FileSize']==cpk.stat().st_size
rows=out['livedata_list'];assert len([x for x in rows if x['name']=='dt870_mobile_and.cpk'])==1
assert not any(x['name']in['pc9301','pc9299']for x in version['dt880']);assert not any('pc9301'in x['name']for x in rows)
meta=json.loads((P/'payload/work/tools/noodle_bundle.json').read_text());assert len(meta['target_card_ids'])==19
for name,row in meta['files'].items():
 f=Path('/workspace/ronaldo-work/73-v25-port/package/payload/livedata')/name;assert f.stat().st_size==row['size']and hashlib.sha256(f.read_bytes()).hexdigest()==row['sha256']
(P/'resources-validation.json').write_text(json.dumps({'passed':True,'mirrored_assets':len(checks),'mirrored_diffuse_thumbnails_decode_equal_to_source':True,'MU2008_uses_working_custom_pack':True,'approved_Y17_glyph_assets_unchanged':True,'native_manager_assets_restored_exactly':len(r['restored_original_manager_assets']),'dt870_protocol_hash_and_size_correct':True,'resource_advertisement_idempotent':True,'old_cuff_containers_not_advertised':True,'base_face_container_bytes_unchanged':True,'phone_tested':False},indent=2));print('RESOURCES_PASS',len(checks))
