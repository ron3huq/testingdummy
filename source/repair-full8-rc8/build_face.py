from pathlib import Path
import sys,json,struct,hashlib,re
sys.path[:0]=[str(Path(__file__).parent),str(Path(__file__).parent.parent/'repair-full8-rc7'),str(Path(__file__).parent.parent/'repair-full8-rc4'),'/workspace/work/full8/recovered-tools']
from iostore import Toc
from ci_bundle import Bundle
from zen_clone import rename,pid
from mesh_tools import Mesh
from face_mesh import build_mesh,labels
from face_texture import masks,build_texture
BASE='/Game/Assets/character/RealFace/'

def build(root,logfile,lowlogfile):
 root=Path(root);live=root/'assets/gateway-release/livedata';logs=json.loads(Path(logfile).read_text());lowlogs=json.loads(Path(lowlogfile).read_text());reports=[]
 for variant,suffix in enumerate(['','ep00v0313','ep01v0291','lg00v0000']):
  t=Toc(str(live/('pc%d_mobile_and.utoc'%(9356+variant))));source=Bundle(t);old='SK_RG28'+suffix+'_Face';meshpath='character/RealFace/'+old+'.uasset';raw=source.files[meshpath][1];log=logs[old.replace('RG28','RG27')];mesh=Mesh(raw,log,lod_index=1)
  low=Toc(str(live/('pc%d_mobile_and.utoc'%(9340+variant))));nativepath=next(p for p in low.files if p.endswith('SK_RV8D'+suffix+'_Face.uasset'));native=low.read(low.files[nativepath]);patched,lab,check=build_mesh(raw,log,native,lowlogs['SK_RV8D'+suffix+'_Face']);source.files[meshpath]=(source.files[meshpath][0],patched)
  prefix='character/RealFace/T_RG28'+suffix+'_Face_';dpath=prefix+'D.uasset';assert dpath in source.files
  from bundle_tools import decode_first_texture
  im=decode_first_texture(source.files[dpath][1],source.files[prefix+'D.ubulk'][1]);skin,neck,oral=masks(mesh,lab,im.size)
  for palette in range(1,7):
   profile='R8A'+str(palette);change=lambda s:s.replace('RG2801',profile+'01').replace('RG28',profile)
   mapping={}
   for p in source.files:
    if not p.endswith('.uasset'):continue
    name=Path(p).stem
    if name.startswith('SK_')or(name.startswith('MI_')and '_Head_Face' in name)or(name.startswith('T_')and name.endswith('_Face_D')):mapping[BASE+name]=BASE+change(name)
    elif name.startswith('T_')and name.endswith('_Face_SRO'):mapping[BASE+name]=BASE+name.replace('RG28','R8A2')
   remap={pid(a):pid(b)for a,b in mapping.items()};out=Bundle(t);out.files={};out.entries={};data=dict(source.files);texture_checks={}
   for ch in ['D','SRO']:
    p=prefix+ch;ra,bu,info=build_texture(data[p+'.uasset'][1],data[p+'.ubulk'][1],ch,palette,skin,neck,oral);data[p+'.uasset']=(data[p+'.uasset'][0],ra);data[p+'.ubulk']=(data[p+'.ubulk'][0],bu);texture_checks[ch]=info
   for path,(idb,b)in data.items():
    name=Path(path).stem;ext=Path(path).suffix;entry=None
    if BASE+name not in mapping:continue
    if name.endswith('_Face_SRO')and palette!=2:continue
    new=Path(mapping[BASE+name]).name
    if ext=='.uasset':
     fixed,deps=source.entries[int.from_bytes(idb[:8],'little')];entry=(fixed,[remap.get(v,v)for v in deps]);repl={}
     for a,z in mapping.items():repl[a]=z;repl[Path(a).name]=Path(z).name
     b=rename(b,repl,BASE+name,BASE+new,imports=mapping)
    out.put('character/RealFace/'+new+ext,struct.pack('<Q',pid(BASE+new))+b'\0\0\0'+(b'\2'if ext=='.uasset'else b'\3'),b,entry)
   out.output_name='pc%d_mobile_and'%(9360+variant*6+palette-1);out.write(live);reports.append({'profile':profile,'variant':suffix or'base','container':out.output_name,'texture':texture_checks,**check})
 return reports
if __name__=='__main__':
 result=build(*sys.argv[1:4]);Path(sys.argv[4]).write_text(json.dumps(result,indent=2));print('Built',len(result),'face palette/LOD variants; phone verification pending.')
