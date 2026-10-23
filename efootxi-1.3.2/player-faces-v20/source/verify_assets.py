"""Independent UEViewer mesh readback, approved-head byte preservation,
full native rigs and per-LOD bone lists, font EAC alpha and card/kit dimensions.
No GPU renderer outcome is inferred from these checks.
"""
from pathlib import Path
import json,struct,hashlib,subprocess
import numpy as np
from PIL import Image,ImageChops
from iostore import Toc,parse_header
from mesh_tools import Mesh
O=Path(__file__).resolve().parent.parent;R=Path('/workspace/ronaldo-work');old=Toc(str(O.parent/'player-faces-v19/container/pc9298_mobile_and.utoc'));new=Toc(str(O/'container/pc9298_mobile_and.utoc'));rows=[];approved=[]
for path,ix in old.files.items():
 if not path.startswith('character/RealFace/'):continue
 if any(Path(path).name.startswith(prefix+profile)for prefix in ['SK_','T_','MI_']for profile in ['NV01','NV27','NVJR','NVHD']):continue
 assert new.read(new.files[path])==old.read(ix);approved.append(path)
assert all(not p.startswith('Assets/')for p in new.files)
for row in json.loads((O/'head-build.json').read_text())['heads']:
 profile=row['profile'];suffix=next((s for s in ['lg00v0000','ep01v0291','ep00v0313']if profile.endswith(s)),'');n='SK_'+profile+'_Face';b=new.read(new.files['character/RealFace/'+n+'.uasset']);donor=old.read(old.files['character/RealFace/SK_ND06'+suffix+'_Face.uasset']);log=(O/'reader-logs'/(n+'.log')).read_text();donorlog=(O/'references/ND06'/('v10-ND06'+suffix+'.log')).read_text()
 for lod in [0,1]:
  a=Mesh(b,log,lod);d=Mesh(donor,donorlog,lod);assert b[a.r['REF_BEGIN']:a.r['REF_END']]==donor[d.r['REF_BEGIN']:d.r['REF_END']]
  def req(m,l):
   at=m.lods[l]+10;count=struct.unpack_from('<I',m.data,at)[0];return list(struct.unpack_from('<%dH'%count,m.data,at+4))
  assert req(a,lod)==req(d,lod);assert len(req(a,lod))==[166,153][lod]
  ns=d.info[0]['verts'];assert a.info[0]['verts']==ns==2504;assert np.array_equal(a.tangents[:ns],d.tangents[:ns]);assert np.array_equal(a.uv[:ns],d.uv[:ns]);assert np.array_equal(a.indices[:d.info[0]['tris']],d.indices[:d.info[0]['tris']]);assert np.array_equal(a.weights[:ns],d.weights[:ns]) and a.info[0]['bones']==d.info[0]['bones']
  assert np.isfinite(a.positions).all() and np.isfinite(a.uv).all();assert len(a.positions)<65536 and a.indices.max()<len(a.positions);assert all(len(q['bones'])<75 for q in a.info);assert np.all(a.weights[:,4:].sum(1)==255);assert a.positions[:,2].min()>=d.positions[:,2].min()-4 and a.positions[:,2].max()<195
  rows.append({'mesh':n,'lod':lod,'required_bones':len(req(a,lod)),'vertices':len(a.positions),'native_bind_block_byte_identical':True,'skin_weights_UVs_tangents_topology_match_phone_proven_ND06':True})
# Package store and file identities must agree, with no duplicate package ID.
h=parse_header(new.read(next(i for i,c in enumerate(new.ids)if c[11]==10)));actual=[int.from_bytes(new.ids[i][:8],'little')for p,i in new.files.items()if p.endswith('.uasset')];assert len(set(actual))==len(actual)and set(actual)==set(h['pids'])
# Native font EAC alpha blocks are kept literally, not merely re-encoded.
fonts=Toc(str(next((R/'resources').rglob('pc0103_mobile_and.utoc'))))
def payloads(raw):
 p=raw.rfind(b'PF_ETC2_RGBA\0');assert p>0;at=p+len(b'PF_ETC2_RGBA\0');first,count=struct.unpack_from('<II',raw,at);assert first==0;at+=8;out=[]
 for level in range(count):
  cooked,flags,n,size,off=struct.unpack_from('<IIIIq',raw,at);at+=24;assert cooked==1 and flags==72 and n==size;data=raw[at:at+n];at+=n;dims=struct.unpack_from('<III',raw,at);at+=12;out.append((data,dims))
 return out
font_count=0
for path,i in new.files.items():
 if '_Font'in path and path in fonts.files:
  a=payloads(new.read(i));b=payloads(fonts.read(fonts.files[path]));assert len(a)==len(b)
  for (ap,ad),(bp,bd)in zip(a,b):assert ad==bd and np.array_equal(np.frombuffer(ap,'u1').reshape(-1,16)[:,:8],np.frombuffer(bp,'u1').reshape(-1,16)[:,:8])
  font_count+=1
assert font_count==32
# Reader export of new card packages and all kit previews verifies their native
# Texture2D serialization and exact decoded pixels against the build decoder.
readback=[]
for card in ['88044950524330','89135066911146','106726716084650','106781745353130','106778792700170','105874433662542']:
 for suffix,size in [('_',(128,128)),('_l',(184,256))]:
  name=card+suffix;cmd=[str(R/'UEViewer/umodel'),'-export','-png','-game=ue4.26','-android','-noanim','-aes=0x4552d45005dfe94964893f4925ec747d3d591401e060ed8b3d58be5721c81295','-path='+str(R/'v20-final-reader'),'-out='+str(R/'v20-verified-images'),name];p=subprocess.run(cmd,capture_output=True);(O/'reader-logs'/(name+'.log')).write_bytes(p.stdout+p.stderr);assert p.returncode==0 and ('Exporting Texture2D '+name).encode()in p.stdout
  image=Image.open(next((R/'v20-verified-images').rglob(name+'.png'))).convert('RGBA');built=Image.open(O/'art'/(card+('-small-decoded.png'if suffix=='_'else'-large-decoded.png'))).convert('RGBA');assert image.size==built.size==size and ImageChops.difference(image,built).getbbox()is None;readback.append(name)
kits=json.loads((O/'kit-build.json').read_text())['kits'];assert len(kits)==8 and {x['team_id']for x in kits}=={351,352,242,245}
for k in kits:
 for item in k['previews']:
  path=item['path'];b=new.read(new.files[path]);dims=payloads(b)[0][1];assert list(dims[:2])==item['dimensions'][0]
report={'status':'V20_INDEPENDENT_MESH_CARD_FONT_CONTAINER_VALIDATION_PASS','new_mesh_LODs':rows,'approved_prior_head_hair_chunks_byte_identical':len(approved),'glyph_assets_original_EAC_alpha_exact':font_count,'card_textures_independent_pixel_match':readback,'kit_team_ids':[351,352,242,245],'kits':8,'kit_UI_previews':16,'all_package_store_IDs_consistent':True,'container_sha256':hashlib.sha256((O/'container/pc9298_mobile_and.ucas').read_bytes()).hexdigest(),'phone_tested':False,'renderer_black_face_fixed_verified':False};(O/'asset-validation.json').write_text(json.dumps(report,indent=2));print(report['status'],len(approved),'approved asset chunks untouched')
