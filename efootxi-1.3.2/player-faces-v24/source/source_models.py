from pathlib import Path
from types import SimpleNamespace as N
import sys,zlib,xml.etree.ElementTree as ET
from PIL import Image
R=Path('/workspace/ronaldo-work')
sys.path.insert(0,str(R/'pes-fmdl-blender/pes-fmdl'));from FmdlFile import FmdlFile
sys.path.insert(0,str(R/'pes-model-blender/pes-model'));from ModelFile import readModelFile,ParserSettings

def load(label):
 root=R/'v24-input'/label;converted=root/'converted';converted.mkdir(exist_ok=True)
 if label=='fifa':
  models=[]
  for fn in ['face_high.fmdl','hair_high.fmdl']:
   m=FmdlFile();m.readFile(str(root/'fpk'/fn));models.append(m)
  for m in models:
   for mm in m.meshes:
    for v in mm.vertices:v.boneMapping={b.name:w for b,w in v.boneMapping.items()}
  return root,*models
 src=root/'extracted-0';models=[]
 hairfile={'rp':'hair_style_win32.model','prince':'hair_2_win32.model','2027':'hair_high_win32.model'}[label]
 for fn,mtl in [('face_high_win32.model','face.mtl'),(hairfile,'hair_style.mtl'if label=='rp'else'hair.mtl')]:
  model,w=readModelFile(str(next(src.rglob(fn))),ParserSettings());assert not w
  b=next(src.rglob(mtl)).read_bytes();b=zlib.decompress(b[16:])if b[1:8]==b'\x10\x01WESYS'else b;materials={m.attrib['name']:{s.attrib['name']:Path(s.attrib['path']).name for s in m.findall('sampler')}for m in ET.fromstring(b).findall('material')}
  for mm in model.meshes:
   old=mm.material;tx=materials[old];name='fox_skin_mat'if old in ['face_phong','head_phong','hairTubeShader']else'fox_eyeOcclusion_mat'if'eyeocclusion'in old else'fox_eyelash_mat'if'eyelash'in old else'fox_hair_mat'
   mm.base_is_hair=False
   height=max(v.position.y for v in mm.vertices)-min(v.position.y for v in mm.vertices)
   mm.skip_native=(old=='hairTubeShader'and height<.001)or(old=='head_phong'and len(mm.vertices)<=3)
   mm.materialInstance=N(name=name,textures=[('Base_Tex_SRGB'if role=='DiffuseMap'else role,N(filename=file))for role,file in tx.items()])
   for v in mm.vertices:
    v.boneMapping={mm.boneGroup.bones[k].name:weight for k,weight in v.boneMapping.items()}
    if v.tangent is None:v.tangent=N(x=1.,y=0.,z=0.)
    v.tangent.w=1.
  models.append(model)
 # Prince's custom hair_2 contains a three-vertex placeholder head and
 # flattened base geometry. Recover its supplied hair_high opaque head cap;
 # keep the declared hair_2 strand geometry, not the high model's other hair.
 if label=='prince':
  capmodel,w=readModelFile(str(next(src.rglob('hair_high_win32.model'))),ParserSettings());assert not w
  for mm in capmodel.meshes:
   if mm.material!='head_phong':continue
   mm.materialInstance=N(name='fox_skin_mat',textures=[('Base_Tex_SRGB',N(filename='face.dds'))]);mm.base_is_hair=False
   for v in mm.vertices:
    v.boneMapping={mm.boneGroup.bones[k].name:weight for k,weight in v.boneMapping.items()}
    if v.tangent is None:v.tangent=N(x=1.,y=0.,z=0.)
    v.tangent.w=1.
   models[1].meshes.append(mm)
 for p in src.rglob('*.dds'):
  b=p.read_bytes();b=zlib.decompress(b[16:])if b[1:8]==b'\x10\x01WESYS'else b
  import io
  Image.open(io.BytesIO(b)).save(converted/(p.stem+'.png'))
 return root,*models
