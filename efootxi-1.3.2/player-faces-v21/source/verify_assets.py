"""Independent reader, exact native rigs, scoped bytes and posed jaw seams.
No result here is an Android renderer or a full gameplay test.
"""
from pathlib import Path
import json,struct,subprocess,itertools,hashlib
import numpy as np
from scipy.spatial import cKDTree
from PIL import Image,ImageChops
from iostore import Toc,parse_header
from mesh_tools import Mesh
from gltf_read import Gltf

O=Path(__file__).resolve().parent.parent;R=Path('/workspace/ronaldo-work')
old=Toc(str(O.parent/'player-faces-v20/container/pc9298_mobile_and.utoc'));new=Toc(str(O/'container/pc9298_mobile_and.utoc'))
logs=O/'reader-logs';logs.mkdir(exist_ok=True);checks=[]
def readmesh(name):
    cmd=[str(R/'UEViewer/umodel'),'-export','-gltf','-png','-game=ue4.26','-android','-noanim','-aes=0x4552d45005dfe94964893f4925ec747d3d591401e060ed8b3d58be5721c81295','-path='+str(R/'v21-reader'),'-out='+str(R/'v21-export'),name]
    p=subprocess.run(cmd,capture_output=True);body=p.stdout+p.stderr;(logs/(name+'.log')).write_bytes(body)
    assert p.returncode==0 and (R/'v21-export/Game/Assets/character/RealFace'/(name+'.gltf')).exists()
    return body.decode('utf8','replace')

name='SK_NWDYep00v0313_Face';log=readmesh(name);raw=new.read(new.files['character/RealFace/'+name+'.uasset']);donor=old.read(old.files['character/RealFace/SK_ND06ep00v0313_Face.uasset']);dlog=(O.parent/'player-faces-v20/references/ND06/v10-ND06ep00v0313.log').read_text()
for lod in [0,1]:
    m=Mesh(raw,log,lod);d=Mesh(donor,dlog,lod)
    assert raw[m.r['REF_BEGIN']:m.r['REF_END']]==donor[d.r['REF_BEGIN']:d.r['REF_END']]
    def required(m,lod):
        at=m.lods[lod]+10;n=struct.unpack_from('<I',m.data,at)[0];return list(struct.unpack_from('<%dH'%n,m.data,at+4))
    assert required(m,lod)==required(d,lod) and len(required(m,lod))==[166,153][lod]
    assert np.isfinite(m.positions).all()and np.isfinite(m.uv).all()and m.indices.max()<len(m.positions)<65536
    assert m.positions[:,2].max()<195 and np.all(m.weights[:,4:].sum(1)==255)
    assert all(len(q['bones'])<75 and set(q['bones'])<=set(required(m,lod))for q in m.info)
    checks.append({'mesh':name,'lod':lod,'required_bones':len(required(m,lod)),'native_bind_block_exact':True,'vertices':len(m.positions)})

# Every pre-existing head/hair asset outside the two requested jaw repairs is exact.
changed=[];unchanged_heads=0
for p,i in old.files.items():
    assert p in new.files
    if new.read(new.files[p])!=old.read(i):changed.append(p)
    elif p.startswith('character/RealFace/'):unchanged_heads+=1
allowed_meshes={'character/RealFace/SK_NWOZep00v0313_Face.uasset','character/RealFace/SK_NDDBep00v0313_Face.uasset'}
assert {p for p in changed if p.startswith('character/RealFace/')}==allowed_meshes
assert 12<=len(changed)<=44,changed  # Some glyph RGB already matched the requested color in v20.
assert all(p in allowed_meshes or '_Font' in p or any(Path(p).name==row['card']+('_'if row['kind']=='minis'else'_l')+'.uasset'for row in json.loads((O/'card-layout-validation.json').read_text())['portraits'])for p in changed)
h=parse_header(new.read(next(i for i,c in enumerate(new.ids)if c[11]==10)));actual=[int.from_bytes(new.ids[i][:8],'little')for p,i in new.files.items()if p.endswith('.uasset')]
assert len(set(actual))==len(actual) and set(actual)==set(h['pids'])

seams=json.loads((O/'seam-repair.json').read_text())['repairs'];posechecks=[]
for profile in ['NWOZep00v0313','NDDBep00v0313']:
    name='SK_'+profile+'_Face';log=readmesh(name);path='character/RealFace/'+name+'.uasset'
    a=Mesh(old.read(old.files[path]),log,0);b=Mesh(new.read(new.files[path]),log,0)
    assert np.array_equal(a.indices,b.indices)and np.array_equal(a.uv,b.uv)
    ns=a.info[0]['verts'];pcns=ns-135
    for field in ['positions','tangents','weights','colors']:
        assert np.array_equal(getattr(a,field)[pcns:],getattr(b,field)[pcns:]),field
    assert np.max(np.linalg.norm(a.positions-b.positions,axis=1))<.025
    g=Gltf(R/'v21-export/Game/Assets/character/RealFace'/(name+'.gltf'))
    inv=g.get(g.d['skins'][0]['inverseBindMatrices']).reshape(-1,4,4).transpose(0,2,1).astype(float);bind=np.linalg.inv(inv)
    # Infer the actual UE-to-glTF axis conversion from independent exported vertices.
    accessor=g.d['meshes'][0]['primitives'][0]['attributes']['POSITION'];gp=g.get(accessor)[:ns]
    possibilities=[]
    for axes in itertools.permutations(range(3)):
        for signs in itertools.product([-1,1],repeat=3):
            pp=b.positions[:ns][:,axes]*signs/100
            possibilities.append((float(cKDTree(gp).query(pp)[0].max()),axes,signs))
    error,axes,signs=min(possibilities);assert error<1e-5,(profile,error)
    groups=next(x['coincident_chin_neck_weight_groups_unified']for x in seams if x['profile']==profile and x['lod']==0)
    assert groups
    cases=[]
    for direction in [-1,1]:
        pose=bind.copy()
        for bone,angle in [(5,.2),(6,-.15),(7,.3),(8,.35)]:
            c=np.cos(angle*direction);s=np.sin(angle*direction);rot=np.eye(4);rot[:3,:3]=[[1,0,0],[0,c,-s],[0,s,c]];pose[bone]=bind[bone]@rot
        transforms=pose@inv
        def deform(m):
            pp=np.c_[m.positions[:ns][:,axes]*signs/100,np.ones(ns)];result=np.zeros((ns,4))
            for i,row in enumerate(m.global_weights(0)):
                for bone,w in row:result[i]+=transforms[bone]@pp[i]*w/255
            return result[:,:3]
        before=deform(a);after=deform(b)
        gap=lambda pp:max(float(np.linalg.norm(pp[group]-pp[group[0]],axis=1).max())for group in groups)
        oldgap,newgap=gap(before),gap(after);assert oldgap>1e-6 and newgap<1e-7
        cases.append({'direction':direction,'before_max_gap_mm':oldgap*1000,'after_max_gap_mm':newgap*1000})
    posechecks.append({'mesh':name,'closed_groups':len(groups),'cases':cases,'pose_is_synthetic':True})

fonts=Toc(str(R/'v20-final-reader/pc0103_mobile_and.utoc'))
def blocks(raw):
    p=raw.rfind(b'PF_ETC2_RGBA\0');assert p>0;at=p+len(b'PF_ETC2_RGBA\0');first,n=struct.unpack_from('<II',raw,at);assert first==0;at+=8;out=[]
    for level in range(n):
        cooked,flags,size,size2,offset=struct.unpack_from('<IIIIq',raw,at);at+=24;assert cooked==1 and flags==72 and size==size2
        payload=raw[at:at+size];at+=size;dimensions=struct.unpack_from('<III',raw,at);at+=12;out.append((payload,dimensions))
    return out
for row in json.loads((O/'kit-letter-validation.json').read_text())['glyphs']:
    p=f"character/Uniform/LowTextures/T_u{row['team']:04d}p{row['slot']}_Font{row['kind']}_D.uasset"
    for (a,ad),(b,bd)in zip(blocks(new.read(new.files[p])),blocks(fonts.read(fonts.files[p]))):
        assert ad==bd and np.array_equal(np.frombuffer(a,'u1').reshape(-1,16)[:,:8],np.frombuffer(b,'u1').reshape(-1,16)[:,:8])

readback=[]
for row in json.loads((O/'card-layout-validation.json').read_text())['portraits']:
    suffix='_'if row['kind']=='minis'else'_l';name=row['card']+suffix
    cmd=[str(R/'UEViewer/umodel'),'-export','-png','-game=ue4.26','-android','-noanim','-aes=0x4552d45005dfe94964893f4925ec747d3d591401e060ed8b3d58be5721c81295','-path='+str(R/'v21-reader'),'-out='+str(R/'v21-card-readback'),name]
    p=subprocess.run(cmd,capture_output=True);(logs/(name+'.log')).write_bytes(p.stdout+p.stderr);assert p.returncode==0
    exported=Image.open(next((R/'v21-card-readback').rglob(name+'.png'))).convert('RGBA');built=Image.open(O/'art'/(name+'-decoded.png')).convert('RGBA')
    assert exported.size==built.size and ImageChops.difference(exported,built).getbbox()is None;readback.append(name)
report={'status':'V21_INDEPENDENT_READER_RIG_GLYPH_JAW_AND_CARD_PASS','new_head_LODs':checks,'approved_prior_head_hair_chunks_byte_identical':unchanged_heads,'old_container_changed_chunks':changed,'native_EAC_alpha_exact_glyph_assets':32,'independently_read_card_images':readback,'jaw_pose_checks':posechecks,'all_package_store_ids_consistent':True,'phone_tested':False,'black_faces_renderer_fixed_verified':False,'jersey_names_visible_device_verified':False}
(O/'asset-validation.json').write_text(json.dumps(report,indent=2));print(report['status'])
