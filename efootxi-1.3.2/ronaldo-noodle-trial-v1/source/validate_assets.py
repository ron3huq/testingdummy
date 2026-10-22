from pathlib import Path
import json,struct,hashlib,sys,math
sys.path.insert(0,'/workspace/testingdummy/tools');from make_extra_pak import Toc
r=Path(__file__).parent;t=Toc(str(r/'container/pc9298_mobile_and.utoc'))
def get(d,b,idx):
 a=d['accessors'][idx];v=d['bufferViews'][a['bufferView']];offset=v.get('byteOffset',0)+a.get('byteOffset',0);sizes={5120:1,5121:1,5122:2,5123:2,5125:4,5126:4};width={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}[a['type']];size=sizes[a['componentType']]*width;stride=v.get('byteStride',size);return b''.join(b[offset+i*stride:offset+i*stride+size] for i in range(a['count']))
def read(path):
 d=json.loads(path.read_text());return d,(path.parent/d['buffers'][0]['uri']).read_bytes()
results=[]
for variant in ['4522','4522lg00v0000','4522ep01v0291','4522ep00v0313']:
 old,ob=read(r/('original-export/Game/Assets/character/RealFace/SK_'+variant+'_Face.gltf'))
 name='SK_'+variant.replace('4522','ND01',1)+'_Face';new,nb=read(r/('full-export/Game/Assets/character/RealFace/'+name+'.gltf'));p0=old['meshes'][0]['primitives'][0];p1=new['meshes'][0]['primitives'][0];hair=new['meshes'][0]['primitives'][1]
 assert set(p0['attributes'])==set(p1['attributes'])
 for attr in p0['attributes']:assert get(old,ob,p0['attributes'][attr])==get(new,nb,p1['attributes'][attr]),(variant,attr)
 assert get(old,ob,p0['indices'])==get(new,nb,p1['indices'])
 assert get(old,ob,old['skins'][0]['inverseBindMatrices'])==get(new,nb,new['skins'][0]['inverseBindMatrices'])
 assert new['accessors'][hair['attributes']['POSITION']]['count']==5005 and new['accessors'][hair['indices']]['count']==5179*3
 assert new['materials'][hair['material']]['name']=='MI_ND0001_Head_Hair_MQ'
 # Every hair vertex has native bone index 7 with weight 255/255.
 joints=get(new,nb,hair['attributes']['JOINTS_0']);weights=get(new,nb,hair['attributes']['WEIGHTS_0'])
 assert all(struct.unpack_from('<H',joints,i*8)[0]==7 for i in range(5005))
 assert all(weights[i*4:i*4+4]==b'\xff\0\0\0' for i in range(5005))
 raw=(r/'asset'/(name+'.uasset')).read_bytes();assert t.read(t.files['RealFace/'+name+'.uasset'])==raw
 results.append({'source_variant':variant,'new_asset':name,'all_exported_face_attributes_and_indices_identical':True,'native_bind_matrices_identical':True,'hair_vertex_count':5005,'hair_triangles':5179,'hair_bone':7,'private_material_resolved':True})
assert len([x for x in t.files if x.endswith('.uasset')])==7
log=(r/'full-asset-reader.log').read_text();assert 'Exported 4/4 objects' in log and 'Loading Texture2D T_ND0001_Hair_D' in log and 'PF_ETC2_RGBA' in log
report={'status':'INDEPENDENT_UNREAL_READER_AND_FOUR_VARIANT_ROUNDTRIP_PASS','assets':results,'private_packages':7,'texture_format':'PF_ETC2_RGBA','alpha_mae':json.loads((r/'material-build.json').read_text())['alpha_mae'],'android_engine_loader_tested':False,'phone_tested':False};(r/'asset-validation.json').write_text(json.dumps(report,indent=2));print(report['status'])
