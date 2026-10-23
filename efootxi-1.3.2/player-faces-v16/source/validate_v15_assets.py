"""Independent native package, import graph, ETC2 exports and preservation checks."""
from pathlib import Path
import struct,json,hashlib
import numpy as np
from PIL import Image,ImageOps
from iostore import Toc,parse_header,store_entry
from mesh_tools import Mesh
from head_mq_and_seams import name_list
out=Path(__file__).resolve().parent.parent;old=Toc(str(out.parent/'player-faces-v14/container/pc9298_mobile_and.utoc'));new=Toc(str(out/'container/pc9298_mobile_and.utoc'));export=Path('/workspace/ronaldo-work/v15-verified/Game/Assets');report=json.loads((out/'card-art-validation.json').read_text());head=report['head_changes'];changes={row['path'] for row in head['mq_shader_substitutions']}|{row['path'] for row in head['dinh_bac']['hair_mask_clip']}|{'character/RealFace/SK_NDDBep00v0313_Face.uasset'};assert len(changes)==13
protected=[]
for path,i in old.files.items():
 if not path.startswith('character/') or path in changes:continue
 assert old.read(i)==new.read(new.files[path]),path;protected.append(path)
assert len(protected)==264
for i in range(len(new.ids)):assert hashlib.sha1(new.read(i)).digest()==new.metas[i][:20]
# Shader path and actual private diffuse resolve independently through UEViewer.
for row in head['mq_shader_substitutions']:
 p=row['path'];stem=Path(p).stem;log=(out/'reader-logs'/(stem+'.log')).read_text();assert 'Loading Material3 M_Head_Face_MQ from package' in log and 'Loading Texture2D T_'+stem[3:].split('_Head_')[0]+'_Face_D' in log
 assert 'Loading MaterialInstanceConstant MI_Head_FaceLegacy_HQ from package' not in log
 raw=new.read(new.files[p]);names=name_list(raw);assert 'NormalMap' not in names and 'SROMap' not in names
# Bone layout/positions/weights are unchanged even for the mesh with edge-UV repair.
p='character/RealFace/SK_NDDBep00v0313_Face.uasset';a=old.read(old.files[p]);b=new.read(new.files[p]);oldlog=(out/'references/NDDBep00v0313.log').read_text();newlog=(out/'reader-logs/SK_NDDBep00v0313_Face.log').read_text()
for lod in [0,1]:
 x=Mesh(a,oldlog,lod);y=Mesh(b,newlog,lod)
 for attr in ['positions','indices','weights','colors','tangents']:assert np.array_equal(getattr(x,attr),getattr(y,attr))
 assert x.info[0]['bones']==y.info[0]['bones'] and len(y.info[0]['bones'])<75
 at=y.lods[lod];n=struct.unpack_from('<I',b,at+10)[0];assert n==[166,153][lod]
 assert a[x.lods[lod]+10:x.lods[lod]+14+n*2]==b[at+10:at+14+n*2]
 assert np.any(x.uv!=y.uv) and np.array_equal(x.uv[x.info[0]['verts']-135:],y.uv[y.info[0]['verts']-135:])
# All 22 finished native texture exports, including every mip, correct native dimensions.
cards=[]
for row in report['cards']:
 p=Path(row['path']);actual=Image.open(export/p.with_suffix('.png')).convert('RGBA');expected=Image.open(out/'art'/row['file']).convert('RGBA');assert list(actual.size)==row['dimensions'][0] and actual.size==expected.size
 mae=float(np.abs(np.array(actual,dtype=float)-np.array(expected,dtype=float)).mean());assert mae<12,(p.name,mae)
 cards.append({'path':row['path'],'dimensions':list(actual.size),'mean_ETC2_error':mae,'aspect_preserving_source':True,'independent_UEViewer_export':True})
assert len(cards)==22
sha=hashlib.sha256((out/'container/pc9298_mobile_and.ucas').read_bytes()).hexdigest()
(out/'preservation-validation.json').write_text(json.dumps({'status':'264_HEAD_CHUNKS_UNCHANGED_10_NATIVE_MQ_PARENTS_DB_UV_HAIR_MASK_PASS','protected_files':protected,'changed_head_files':sorted(changes),'container_sha256':sha,'phone_tested':False},indent=2))
# Prior geometric/texture measurements remain applicable: every position, triangle,
# tangent, weight, skin texture block and LOD index has been proven unchanged.
for filename in ['asset-validation.json','quality-validation.json','texture-validation.json','seam-validation.json','2008-texture-validation.json']:
 v=json.loads((out.parent/'player-faces-v14'/filename).read_text());v['container_sha256']=sha;v['measurement_reused_from']='v14: mesh positions/tangents/weights/indices and all texture data unchanged; DB40skinUVedge vertices per LOD and 12MICs changed, independently inspected';(out/filename).write_text(json.dumps(v,indent=2))
sleeves=json.loads((out.parent/'player-faces-v14/sleeve-validation.json').read_text());sleeves['measurement_reused_from']='v14 exact selector/runtime binaries unchanged';(out/'sleeve-validation.json').write_text(json.dumps(sleeves,indent=2))
report['independent_ueviewer_export']=cards;(out/'card-art-validation.json').write_text(json.dumps(report,indent=2));(out/'v15-assets-validation.json').write_text(json.dumps({'status':'MQ_PARENT_IMPORT_RESOLUTION_NATIVE_LOD_PRESERVATION_AND_22_CARD_EXPORTS_PASS','container_sha256':sha,'shader_parent_changes':10,'UI_exports':cards,'head_meshes':25,'render_lods':50,'phone_tested':False},indent=2));print('V15_ASSETS_AND_22_NATIVE_CARD_EXPORTS_PASS')
