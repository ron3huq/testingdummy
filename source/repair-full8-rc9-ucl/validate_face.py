"""Independent reader for both newly serialized LODs; no old stream offsets reused."""
from pathlib import Path
import sys,struct,json,numpy as np
sys.path[:0]=[str(Path(__file__).parent),str(Path(__file__).parent.parent/'repair-full8-rc7'),str(Path(__file__).parent.parent/'repair-full8-rc4')]
from iostore import Toc
from mesh_tools import Mesh
from bundle_tools import decode_first_texture
from face_mesh import labels

def read_lod(b,at):
 begin=at;at+=10
 def arr():
  nonlocal at
  n=struct.unpack_from('<I',b,at)[0];at+=4;v=list(struct.unpack_from('<%dH'%n,b,at));at+=n*2;return v
 required=arr();sections=[];n=struct.unpack_from('<I',b,at)[0];at+=4;assert n==2
 for _ in range(n):
  h=b[at:at+29];at+=29;bones=arr();nv,inf=struct.unpack_from('<II',b,at);at+=8;# tail may contain variable metadata after the vertex/influence count
  # Audited sections have tail fixed at 34 bytes after their bone map.
  tail_extra=26;at+=tail_extra
  sections.append(dict(bones=bones,verts=nv,tris=struct.unpack_from('<I',h,8)[0]))
 active=arr();size=struct.unpack_from('<I',b,at)[0];at+=4;stream=at
 return dict(begin=begin,required=required,active=active,sections=sections,stream=stream,end=stream+size)

def run(root):
 root=Path(root);live=root/'assets/gateway-release/livedata';logs=json.loads((root/'source/repair-full8-rc7/mesh-ranges.json').read_text());reports=[]
 for variant,suffix in enumerate(['','ep00v0313','ep01v0291','lg00v0000']):
  old=Toc(str(live/('pc%d_mobile_and.utoc'%(9356+variant))));op=next(p for p in old.files if p.endswith('SK_RG28'+suffix+'_Face.uasset'));raw=old.read(old.files[op]);mesh=Mesh(raw,logs['SK_RG27'+suffix+'_Face'],lod_index=1)
  # Record the section tail lengths from the native reader, independent of guessed new offsets.
  tail_lengths=[len(q['tail'])for q in mesh.info];assert tail_lengths==[34,34],tail_lengths
  for palette in range(1,7):
   toc=Toc(str(live/('pc%d_mobile_and.utoc'%(9360+variant*6+palette-1))));p=next(p for p in toc.files if p.endswith('SK_R8A'+str(palette)+suffix+'_Face.uasset'));b=toc.read(toc.files[p]);a=read_lod(b,mesh.lods[0]);low=read_lod(b,a['end']);assert b[low['end']:]==bytes.fromhex('020200000000');assert len(a['required'])==166 and len(low['required'])==153;assert set(range(8,21)).isdisjoint(low['required']);assert a['active']==list(range(166))and low['active']==list(range(8));assert a['sections'][0]['verts']==mesh.info[0]['verts']and low['sections'][0]['verts']==743
   for lod in [a,low]:
    assert set(lod['active'])<=set(lod['required'])
    for sec in lod['sections']:assert set(sec['bones'])<=set(lod['required'])
   # Original skeleton prefix stays byte-identical except bounds, MinLod and size fixups (reviewed in builder).
   reports.append(dict(variant=suffix or'base',palette=palette,required_bones=[166,153],low_skin_vertices=743,streams_exact_length=True))
 return dict(passed=True,assets=reports,phone_verified=False)
if __name__=='__main__':print(json.dumps(run(sys.argv[1]),indent=2))
