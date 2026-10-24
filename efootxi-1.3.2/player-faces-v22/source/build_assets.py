"""V22: anatomical jaw weights, native extended glyphs, varied minis and a
single-variable material control. Keep every v21 LARGE portrait/background.
"""
from pathlib import Path
import json,struct,hashlib,shutil
import numpy as np
from PIL import Image
from iostore import Toc,parse_header,store_entry
from bundle_tools import Bundle,replace_texture,decode_first_texture
from mesh_tools import Mesh,quantize
from zen_clone import rename,pid

O=Path(__file__).resolve().parent.parent;R=Path('/workspace/ronaldo-work');old=O.parent/'player-faces-v21'
t=Toc(str(old/'container/pc9298_mobile_and.utoc'));bundle=Bundle(t);report={'phone_tested':False,'jaw':[],'extended_fonts':[],'minis':[]}
def smooth(a):a=np.clip(a,0,1);return a*a*(3-2*a)
for profile,parameters in [('NWOZep00v0313',(12,19,157,168)),('NDDBep00v0313',(10,19,159,170))]:
    path='character/RealFace/SK_'+profile+'_Face.uasset';original=t.read(t.files[path]);raw=bytearray(original);log=(old/'reader-logs'/('SK_'+profile+'_Face.log')).read_text()
    for lod in [0,1]:
        m=Mesh(original,log,lod);n=m.info[0]['verts']-135;p=m.positions[:n];rows=[dict(x)for x in m.global_weights(0)];ylo,yhi,zlo,zhi=parameters
        if 8 not in m.info[0]['bones']:
            report['jaw'].append({'profile':profile,'lod':lod,'unchanged_native_reduced_LOD':True});continue
        field=smooth((p[:,1]-ylo)/(yhi-ylo))*smooth((p[:,2]-zlo)/3)*smooth((zhi-p[:,2])/3);blend=smooth((166-p[:,2])/3)
        changed=[]
        for i in range(n):
            available=rows[i].get(7,0)+rows[i].get(8,0);jaw=rows[i].get(8,0)*(1-blend[i])+available*field[i]*blend[i]
            if abs(jaw-rows[i].get(8,0))<1e-6:continue
            rows[i][7]=max(0,float(available-jaw));rows[i][8]=max(0,float(jaw));rows[i]={k:v for k,v in rows[i].items()if v>1e-8};changed.append(i)
        w=m.weights.copy();packed=quantize(rows,m.info[0]['bones'])
        for i in changed:w[i]=packed[i]
        at=m.r['SKIN_WEIGHTS_BEGIN']+30;raw[at:at+w.nbytes]=w.tobytes()
        after=Mesh(bytes(raw),log,lod);assert np.array_equal(m.positions,after.positions)and np.array_equal(m.uv,after.uv)and np.array_equal(m.tangents,after.tangents)
        assert np.array_equal(m.weights[n:],after.weights[n:])  # native eyes/oral and all hair
        report['jaw'].append({'profile':profile,'lod':lod,'anatomical_field':parameters,'changed_skin_weight_vertices':len(changed),'geometry_UVs_normals_native_accessories_and_hair_exact':True})
    key,_=bundle.files[path];bundle.files[path]=(key,bytes(raw))

# Nicolás test card ONLY: same exact 2017 vertices/rig/hair, literal phone-proven
# ND06 skin MIC objects. Do not clone their textures/materials or alter 4 originals.
BASE='/Game/Assets/character/RealFace/';source='SK_NW01ep00v0313_Face';name='SK_NT01ep00v0313_Face';path='character/RealFace/'+source+'.uasset'
imports={BASE+'MI_NW01ep00v0313_Head_FaceLegacy_'+q:BASE+'MI_ND06ep00v0313_Head_FaceLegacy_'+q for q in ['HQ','MQ']};rep={BASE+source:BASE+name,source:name}
for a,b in imports.items():rep[a]=b;rep[a.split('/')[-1]]=b.split('/')[-1]
body=rename(t.read(t.files[path]),rep,BASE+source,BASE+name,imports=imports)
h=parse_header(t.read(next(i for i,c in enumerate(t.ids)if c[11]==10)));pk=int.from_bytes(t.ids[t.files[path]][:8],'little');fixed,im=store_entry(h['store'],h['pids'].index(pk));remap={pid(a):pid(b)for a,b in imports.items()}
bundle.put('character/RealFace/'+name+'.uasset',struct.pack('<Q',pid(BASE+name))+b'\0\0\0\2',body,(fixed,[remap.get(v,v)for v in im]))
report['material_control']={'card_id':'105807861630781','profile':'NT01ep00v0313','skin_materials':'literal ND06 assets','mesh_positions_UVs_weights_hair_source':'2017 NW01 byte-identical arrays','original_four_profiles_unchanged':True,'intended_as_diagnostic_not_proven_black_face_fix':True}

# Native Ex atlas is an extended Latin alphabet, not the ordinary A-Z image.
# Keep each kit's A-Z font untouched. Supplement missing Ex assets with native
# fallback glyphs; original matching Ex family is absent from available bundles.
fontrefs=json.loads((O/'references/font-entries.json').read_text())
palette={r['team']:{}for r in json.loads((old/'kit-letter-validation.json').read_text())['glyphs']}
for row in json.loads((old/'kit-letter-validation.json').read_text())['glyphs']:palette[row['team']][row['slot']]=row['RGB']
FBASE='/Game/Assets/character/Uniform/LowTextures/'
for team,slots in palette.items():
    for slot,color in slots.items():
        family=136 if team==242 else 14
        sp=f'character/Uniform/LowTextures/T_u{family:04d}p1_FontName_Ex_D.uasset';oldname=Path(sp).stem;newname=f'T_u{team:04d}p{slot}_FontName_Ex_D';raw=(O/'references'/Path(sp).name).read_bytes();im=decode_first_texture(raw);a=np.array(im);a[:,:,:3]=color
        raw,bulk,dims,_=replace_texture(raw,Image.fromarray(a),preserve_alpha=True);assert not bulk and dims[0]==[256,128]
        raw=rename(raw,{FBASE+oldname:FBASE+newname,oldname:newname},FBASE+oldname,FBASE+newname)
        ref=fontrefs[str(family)];entry=(bytes.fromhex(ref['fixed']),ref['imports'])
        bundle.put('character/Uniform/LowTextures/'+newname+'.uasset',struct.pack('<Q',pid(FBASE+newname))+b'\0\0\0\2',raw,entry)
        report['extended_fonts'].append({'team':team,'slot':slot,'native_source':sp,'target':newname,'dimensions':dims,'ordinary_AZ_font_unchanged':True,'extended_accent_font_is_native_fallback_not_exact_original_family':True,'RGB':color})

art=O/'art';art.mkdir(exist_ok=True);sheet_path=art/'ronaldo-mini-sheet.png';sheet=Image.open(sheet_path).convert('RGBA');w,h=sheet.size;assert w==h and w%2==0
for i,card in enumerate(['88044950524330','89135066911146','106726716084650','106781745353130']):
    x,y=i%2,i//2;image=sheet.crop((x*w//2+2,y*h//2+2,(x+1)*w//2-2,(y+1)*h//2-2)).resize((128,128),Image.Resampling.LANCZOS)
    image.save(art/(card+'_.png'));path=next(p for p in t.files if Path(p).name==card+'_.uasset');raw,bulk,dims,decoded=replace_texture(t.read(t.files[path]),image);assert not bulk and dims[0]==[128,128]
    key,_=bundle.files[path];bundle.files[path]=(key,raw);decoded.save(art/(card+'_-decoded.png'));report['minis'].append({'card':card,'square_native_dimensions':dims,'distinct_pose':i,'alpha_background':True,'large_card_background_byte_unchanged':True})
bundle.write(O/'container');(O/'build-report.json').write_text(json.dumps(report,indent=2));print('V22_JAW_EXTENDED_FONTS_MINIS_SINGLE_VARIABLE_MATERIAL_CONTROL_BUILT')
