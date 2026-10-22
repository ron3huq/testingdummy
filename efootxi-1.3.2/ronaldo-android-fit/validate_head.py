from pathlib import Path
import sys,json,hashlib,struct
sys.path.insert(0,'/workspace/testingdummy/tools');from make_extra_pak import Toc
r=Path(__file__).parent;t=Toc(str(r/'pc3700_mobile_and.utoc'));checks=[]
for p in sorted((r/'extracted').glob('*.uasset')):
 i=t.files['RealFace/'+p.name];b=p.read_bytes();assert len(b)==t.ol[i][1];assert hashlib.sha1(b).digest()==t.metas[i][:20]
 gpath=r/'export/Game/Assets/character/RealFace'/(p.stem+'.gltf');g=json.loads(gpath.read_text());prims=g['meshes'][0]['primitives'];assert len(prims)==2
 rows=[{'vertices':g['accessors'][p['attributes']['POSITION']]['count'],'triangles':g['accessors'][p['indices']]['count']//3} for p in prims]
 assert rows==[{'vertices':743,'triangles':1222},{'vertices':601,'triangles':453}];assert len(g['skins'][0]['joints'])==166
 checks.append({'asset':p.name,'toc_sha1_match':True,'exported_sections':rows,'reference_bones':166})
assert len(checks)==4
fit=json.loads((r/'fit/fit-validation.json').read_text());assert fit['native_face_vertex_coordinates_unchanged'] and fit['vertices_following_test_head_rotation']==5005
b=(r/'fit/Ronaldo_ANDROID_REFERENCE_NOODLE_NOT_COOKED.glb').read_bytes();assert b[:4]==b'glTF';n,typ=struct.unpack_from('<II',b,12);g=json.loads(b[20:20+n]);assert typ==0x4e4f534a
triangles=sum(g['accessors'][p['indices']]['count']//3 for m in g['meshes'] for p in m['primitives']);assert triangles==6401
for p in g['meshes']:
 assert all('JOINTS_0' in x['attributes'] and 'WEIGHTS_0' in x['attributes'] for x in p['primitives'])
log=(r/'umodel-lod-audit.log').read_text();assert 'cooked_out=1' in log and 'cooked_out=0' in log
ue=(Path('/workspace/analysis/my-league/android/official-apk/lib/arm64-v8a/libUE4.so')).read_bytes();assert '++UE4+Release-4.26'.encode('utf-16-le') in ue
result={'status':'NATIVE_REFERENCE_FIT_VALIDATED_NOT_INSTALLABLE','archive':json.loads((r/'unpack-validation.json').read_text()),'engine_branch_observed':'UE4 Release-4.26 (UTF16 string in libUE4.so; exact custom build compatibility unverified)','heads':checks,'lod0':'cooked_out=true in serialized Android asset; exported available inline LOD','fit':fit,'exported_combined_triangles':triangles,'new_android_asset_built':False,'device_tested':False}
(r/'validation.json').write_text(json.dumps(result,indent=2));print('PASS: archive, four native TOC hashes, four glTF geometries, fit binding, face preservation, GLB topology and weights; NOT game validation.')
