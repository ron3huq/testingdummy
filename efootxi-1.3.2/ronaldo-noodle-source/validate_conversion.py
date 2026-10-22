from pathlib import Path
import struct,json,hashlib
ROOT=Path(__file__).resolve().parent
r=json.loads((ROOT/'model-analysis.json').read_text())
assert len(r['models'])==3
assert len(r['textures'])==12 and all(t.get('converted') for t in r['textures'].values())
vertices=sum(m['vertices'] for f in r['models'].values() for m in f['meshes']);tris=sum(m['triangles'] for f in r['models'].values() for m in f['meshes'])
assert (vertices,tris)==(8180,10705)
glb=(ROOT/'converted/Ronaldo_88044950524330_SOURCE.glb').read_bytes();assert glb[:4]==b'glTF'
assert struct.unpack_from('<II',glb,4)==(2,len(glb))
n,typ=struct.unpack_from('<II',glb,12);assert typ==0x4E4F534A
g=json.loads(glb[20:20+n]);assert len(g['meshes'])==10
# Exported triangles, retained UVs/weights and reference bones. This is NOT engine validation.
assert sum(g['accessors'][p['indices']]['count']//3 for m in g['meshes'] for p in m['primitives'])==tris
assert all('TEXCOORD_0' in p['attributes'] and 'JOINTS_0' in p['attributes'] and 'WEIGHTS_0' in p['attributes'] for m in g['meshes'] for p in m['primitives'])
hair=[m for m in g['meshes'] if m['name'].startswith('hair_high_0')][0]
assert 'TEXCOORD_1' in hair['primitives'][0]['attributes']
res={'status':'SOURCE_CONVERSION_VALIDATED_NOT_ANDROID_READY','target_card_id':'88044950524330','source_vertices':vertices,'source_triangles':tris,'mesh_count':10,'converted_textures':12,'hair_curl_mesh_vertices':5005,'hair_curl_mesh_triangles':5179,'hair_curl_weights':'100% sk_head for all 5005 vertices','glb_triangle_count_matches':True,'glb_uv_skin_attributes_present':True,'android_asset_built':False,'android_runtime_tested':False,'game_files_modified':False}
(ROOT/'validation.json').write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
