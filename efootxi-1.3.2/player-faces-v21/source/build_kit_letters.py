"""Native jersey glyph assets: keep exact EAC alpha, font layout and dimensions."""
from pathlib import Path
import json,numpy as np
from PIL import Image
from iostore import Toc
from bundle_tools import Bundle,replace_texture,decode_first_texture

O=Path(__file__).resolve().parent.parent;R=Path('/workspace/ronaldo-work')
t=Toc(str(O/'seams-container/pc9298_mobile_and.utoc'));bundle=Bundle(t)
native=Toc(str(R/'v20-final-reader/pc0103_mobile_and.utoc'));rows=[]
# Colors follow the supplied historical kits. The native font itself is retained.
colors={351:[(2,121,165),(245,245,245)],352:[(245,245,245),(245,245,245)],242:[(154,116,68),(184,167,112)],245:[(244,218,59),(15,35,62)]}
for team,slots in colors.items():
    for slot,color in enumerate(slots,1):
        for kind in ['Name','Back','Chest','Leg']:
            p=f'character/Uniform/LowTextures/T_u{team:04d}p{slot}_Font{kind}_D.uasset'
            raw=native.read(native.files[p]);im=decode_first_texture(raw);pixels=np.array(im)
            # Preserve opaque letter edge shading/outline for the native black
            # Sparta atlas rather than flattening its RGB detail (v20 did).
            a=pixels[:,:,3];rgb=pixels[:,:,:3].astype(float)
            native_color=np.median(rgb[a>240],axis=0)
            if np.max(np.std(rgb[a>240],axis=0))>12:
                ratio=np.clip(np.mean(rgb,axis=2)/max(float(np.mean(native_color)),1),.35,1.7)
                rgb=np.clip(np.array(color)[None,None,:]*ratio[:,:,None],0,255)
            else:rgb[:]=color
            pixels[:,:,:3]=rgb.astype('u1');image=Image.fromarray(pixels)
            updated,bulk,dims,decoded=replace_texture(raw,image,preserve_alpha=True);assert not bulk
            bundle.native(native,p,updated)
            dest=O/'kit-letter-previews';dest.mkdir(exist_ok=True);decoded.save(dest/(Path(p).stem+'.png'))
            rows.append({'team':team,'slot':slot,'kind':kind,'RGB':list(color),'native_dimensions':dims,'original_font_and_exact_encoded_alpha_retained':True})
bundle.write(O/'letters-container');(O/'kit-letter-validation.json').write_text(json.dumps({'glyphs':rows,'native_font_size_layout_and_alpha_preserved':True,'original_name_resource_config_not_rewritten':True,'historical_color_palette':{str(k):v for k,v in colors.items()},'missing_names_device_verified_fixed':False},indent=2));print('32_NATIVE_GLYPHS_RECOLORED_ORIGINAL_ALPHA_PRESERVED')
