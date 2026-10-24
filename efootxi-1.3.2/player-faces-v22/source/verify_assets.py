from pathlib import Path
import json,struct,subprocess
import numpy as np
from PIL import Image,ImageChops,ImageDraw
from iostore import Toc,parse_header
from mesh_tools import Mesh
from bundle_tools import decode_first_texture
from gltf_read import Gltf
from zen_clone import pid

O=Path(__file__).resolve().parent.parent;R=Path('/workspace/ronaldo-work');base=O.parent/'player-faces-v21'
old=Toc(str(base/'container/pc9298_mobile_and.utoc'));new=Toc(str(O/'container/pc9298_mobile_and.utoc'));logs=O/'reader-logs';logs.mkdir(exist_ok=True)
changed=[p for p,i in old.files.items()if new.read(new.files[p])!=old.read(i)];added=set(new.files)-set(old.files)
allowed={'character/RealFace/SK_'+p+'_Face.uasset'for p in ['NWOZep00v0313','NDDBep00v0313']}
allowed|={next(p for p in old.files if Path(p).name==c+'_.uasset')for c in ['88044950524330','89135066911146','106726716084650','106781745353130']}
assert set(changed)==allowed and len(added)==9
large=[p for p in old.files if p.endswith('_l.uasset')and'/Player/'in p]
assert all(old.read(old.files[p])==new.read(new.files[p])for p in large)
h=parse_header(new.read(next(i for i,c in enumerate(new.ids)if c[11]==10)));ids=[int.from_bytes(new.ids[i][:8],'little')for p,i in new.files.items()if p.endswith('.uasset')];assert len(set(ids))==len(ids)and set(ids)==set(h['pids'])

def reader(name,mesh=False):
    cmd=[str(R/'UEViewer/umodel'),'-export','-png','-game=ue4.26','-android','-noanim','-aes=0x4552d45005dfe94964893f4925ec747d3d591401e060ed8b3d58be5721c81295','-path='+str(R/'v22-reader'),'-out='+str(R/'v22-export')]
    if mesh:cmd.append('-gltf')
    p=subprocess.run(cmd+[name],capture_output=True);(logs/(name+'.log')).write_bytes(p.stdout+p.stderr);assert p.returncode==0
    return (p.stdout+p.stderr).decode('utf8','replace')
log=reader('SK_NT01ep00v0313_Face',True);control=new.read(new.files['character/RealFace/SK_NT01ep00v0313_Face.uasset']);src=old.read(old.files['character/RealFace/SK_NW01ep00v0313_Face.uasset']);srclog=(base.parent/'player-faces-v20/reader-logs/SK_NW01ep00v0313_Face.log').read_text()
for lod in [0,1]:
    a=Mesh(src,srclog,lod);b=Mesh(control,log,lod)
    for field in ['positions','tangents','uv','weights','colors','indices']:assert np.array_equal(getattr(a,field),getattr(b,field))
    assert src[a.r['REF_BEGIN']:a.r['REF_END']]==control[b.r['REF_BEGIN']:b.r['REF_END']]
    assert a.info==b.info
assert 'MI_ND06ep00v0313_Head_FaceLegacy_HQ'in log and 'MI_ND06ep00v0313_Head_FaceLegacy_MQ'in log

g=Gltf(R/'v21-export/Game/Assets/character/RealFace/SK_NWOZep00v0313_Face.gltf');inv=g.get(g.d['skins'][0]['inverseBindMatrices']).reshape(-1,4,4).transpose(0,2,1);bind=np.linalg.inv(inv);jaw=[]
for profile in ['NWOZep00v0313','NDDBep00v0313']:
    name='SK_'+profile+'_Face';log=reader(name,True);p='character/RealFace/'+name+'.uasset';a=Mesh(old.read(old.files[p]),log,0);b=Mesh(new.read(new.files[p]),log,0);ns=a.info[0]['verts']-135
    for lod in [0,1]:
        aa=Mesh(old.read(old.files[p]),log,lod);bb=Mesh(new.read(new.files[p]),log,lod)
        for field in ['positions','tangents','uv','colors','indices']:assert np.array_equal(getattr(aa,field),getattr(bb,field))
        assert np.array_equal(aa.weights[ns:],bb.weights[ns:])and aa.info==bb.info
        assert aa.data[aa.r['REF_BEGIN']:aa.r['REF_END']]==bb.data[bb.r['REF_BEGIN']:bb.r['REF_END']]
        if lod==1:assert np.array_equal(aa.weights,bb.weights)
    pos=a.positions[:ns];tri=a.indices[:a.info[0]['tris']];tri=tri[(tri<ns).all(1)];centers=pos[tri].mean(1);tri=tri[(centers[:,2]<167)&(centers[:,1]>10)]
    ref=np.cross(pos[tri[:,1]]-pos[tri[:,0]],pos[tri[:,2]]-pos[tri[:,0]]);pp=np.c_[pos[:,[0,2,1]]/100,np.ones(ns)]
    wa=np.array([dict(row).get(8,0)/255 for row in a.global_weights(0)[:ns]]);wb=np.array([dict(row).get(8,0)/255 for row in b.global_weights(0)[:ns]])
    cases=[]
    for axis,angle in [(0,10),(0,25),(0,35),(1,15),(2,15),(0,-10)]:
        rad=np.deg2rad(angle);c,s=np.cos(rad),np.sin(rad);rot=np.eye(4);axes=[j for j in range(3)if j!=axis];rot[np.ix_(axes,axes)]=[[c,-s],[s,c]];mat=bind[8]@rot@inv[8];delta=((mat@pp.T).T[:,:3]-pp[:,:3])[:,[0,2,1]]*100
        def folds(weights):
            q=pos+delta*weights[:,None];normal=np.cross(q[tri[:,1]]-q[tri[:,0]],q[tri[:,2]]-q[tri[:,0]]);return int((np.sum(normal*ref,1)<0).sum())
        cases.append({'axis':axis,'degrees':angle,'before':folds(wa),'after':folds(wb)})
    assert sum(x['after']for x in cases)<sum(x['before']for x in cases)*.25
    chin=(pos[:,1]>16)&(pos[:,2]>161)&(pos[:,2]<164.5)&(abs(pos[:,0])<4);assert wb[chin].mean()>.65
    assert np.array_equal(a.weights[:ns][pos[:,2]>=166],b.weights[:ns][pos[:,2]>=166])
    jaw.append({'profile':profile,'synthetic_jaw_cases':cases,'chin_mean_jaw_weight_after':float(wb[chin].mean()),'upper_face_and_native_accessory_weights_preserved':True,'jaw_motion_not_frozen':True})

def alpha_blocks(raw):
    p=raw.rfind(b'PF_ETC2_RGBA\0');assert p>0;at=p+len(b'PF_ETC2_RGBA\0')+8;cooked,flags,size,size2,off=struct.unpack_from('<IIIIq',raw,at);assert flags==72;at+=24
    return b''.join(raw[j:j+8]for j in range(at,at+size,16))
build=json.loads((O/'build-report.json').read_text())
for font in build['extended_fonts']:
    dest='character/Uniform/LowTextures/'+font['target']+'.uasset';ref=(O/'references'/Path(font['native_source']).name).read_bytes();assert alpha_blocks(new.read(new.files[dest]))==alpha_blocks(ref)
    reader(font['target'])
for row in build['minis']:
    name=row['card']+'_';reader(name);im=Image.open(next((R/'v22-export').rglob(name+'.png'))).convert('RGBA');built=Image.open(O/'art'/(name+'-decoded.png')).convert('RGBA');assert im.size==built.size==(128,128)and ImageChops.difference(im,built).getbbox()is None
canvas=Image.new('RGB',(640,180),'#243545');draw=ImageDraw.Draw(canvas)
for i,row in enumerate(build['minis']):
    im=Image.open(O/'art'/(row['card']+'_.png')).convert('RGBA');canvas.paste(im,(i*160+16,30),im);draw.text((i*160+4,8),row['card'],fill='white')
canvas.save(O/'Mini-preview.png')
report={'status':'V22_NATIVE_ASSETS_JAW_POSES_EX_GLYPHS_AND_MINIS_PASS','changed_prior_chunks':changed,'new_chunks':sorted(added),'all_v21_large_portraits_backgrounds_byte_identical':True,'original_four_failing_head_assets_byte_identical':True,'control_only_skin_materials_differ_from_2017':True,'jaw':jaw,'eight_Ex_fonts_native_alpha_exact':True,'ordinary_ASCII_fonts_byte_unchanged':True,'extended_accent_fallback_family_not_exact_original':True,'phone_tested':False,'black_faces_fixed_verified':False,'jersey_names_visible_verified':False}
(O/'asset-validation.json').write_text(json.dumps(report,indent=2));print(report['status'])
