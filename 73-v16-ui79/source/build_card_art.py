from pathlib import Path
import sys,struct,json,hashlib,inspect
from PIL import Image
import etcpak
sys.path.insert(0,'/workspace/testingdummy/efootxi-1.3.2/player-faces-v25/source')
from iostore import Toc,parse_header,store_entry
from bundle_tools import Bundle,replace_texture,decode_first_texture
from zen_clone import rename,pid
P=Path('/tmp/73-ui79');old=Toc('/workspace/ronaldo-work/73-ui7/carry/livedata/pc9298_mobile_and.utoc');b=Bundle(old);b.files={};b.entries={};folder='ui/Data/Thumbnail/Player/Variation2022/';BASE='/Game/Assets/'+folder;rows=[];cache={};originals=json.loads((P/'asset-matches.json').read_text())
def alpha_only(raw,bulk,image):
 data=bytearray(raw);bulk=bytearray(bulk);fmt=b'PF_ETC2_RGBA\0';at=data.rfind(fmt);assert at>0;at+=len(fmt);first,count=struct.unpack_from('<II',data,at);at+=8;assert first==0
 for level in range(count):
  cooked,flags,n,size,off=struct.unpack_from('<IIIIq',data,at);at+=24;external=bool(flags&256);w,h,d=struct.unpack_from('<III',data,at if external else at+n);im=image.resize((max(4,w),max(4,h)),Image.Resampling.LANCZOS).convert('RGBA');encoded=etcpak.compress_etc2_rgba(im.tobytes(),im.width,im.height);prior=bytes(bulk[off:off+n])if external else bytes(data[at:at+n]);assert len(encoded)==len(prior)==n
  edited=bytearray(encoded)
  for block in range(0,n,16):edited[block+8:block+16]=prior[block+8:block+16]
  assert all(edited[j+8:j+16]==prior[j+8:j+16]for j in range(0,n,16))
  if external:bulk[off:off+n]=edited
  else:data[at:at+n]=edited;at+=n
  at+=12
 return bytes(data),bytes(bulk)
def add(target,source,srcpath,image,alpha=False):
 oldname=Path(srcpath).stem;newname='U79_'+target+('_l'if oldname.endswith('_l')else'_');raw=source.read(source.files[srcpath]);bulkp=srcpath[:-7]+'.ubulk';bulk=source.read(source.files[bulkp])if bulkp in source.files else b''
 if alpha:data,bb=alpha_only(raw,bulk,image)
 else:data,bb,dims,decoded=replace_texture(raw,image,bulk)
 ownold=BASE+oldname;ownnew=BASE+newname;renamed=rename(data,{oldname:newname,ownold:ownnew},ownold,ownnew);h=parse_header(source.read(next(i for i,x in enumerate(source.ids)if x[11]==10)));original_pid=int.from_bytes(source.ids[source.files[srcpath]][:8],'little');entry=store_entry(h['store'],h['pids'].index(original_pid));ident=struct.pack('<Q',pid(ownnew));b.put(folder+newname+'.uasset',ident+b'\0\0\0\2',renamed,entry)
 if bulk:b.put(folder+newname+'.ubulk',ident+b'\0\0\0\3',bb)
 result=decode_first_texture(renamed,bb);result.save(P/'art'/(newname+'-encoded.png'));rows.append({'id':target,'key':newname,'size':list(result.size),'preserved_original_RGB_compressed_blocks':alpha,'image_pixels_not_regenerated':True})
# New supplied photographs: full source pose and a separately fitted miniface.
for target in ['89135066911146','89138556572074','88044950524330']:
 for suffix,kind in [('_l','large'),('_','small')]:
  row=next(x for x in originals if Path(x['path']).stem==target+suffix and x['path'].endswith('.uasset'));source=cache.setdefault(row['toc'],Toc(row['toc']));add(target,source,row['path'],Image.open(P/'art'/(target+'-'+kind+'.png')))
# Existing custom pictures retain every compressed RGB colour block. Only their background alpha changes.
for target in json.loads((P/'old-cutouts.json').read_text()):
 for suffix in ['_l','_']:
  src=folder+target+suffix+'.uasset';raw=old.read(old.files[src]);bulkp=src[:-7]+'.ubulk';bulk=old.read(old.files[bulkp])if bulkp in old.files else b''
  if suffix=='_l':image=Image.open(P/'art'/(target+'-background-cutout.png'))
  else:
   # The existing miniface keeps its exact framing; its alpha follows the original foreground crop.
   image=decode_first_texture(raw,bulk);from prepare_portraits import cutout
   # import side effects regenerate only the three supplied source portraits, no old card pixels.
   image=cutout(image)
  add(target,old,src,image,alpha=True)
# User authorized self-created hero card artwork: Blender portraits from the supplied meshes.
missing=[]
for target in ['106754901843130','105647605587130']:
 if not(P/'art'/(target+'-large.png')).exists():missing.append(target);continue
 for suffix,kind in [('_l','large'),('_','small')]:add(target,old,folder+'88044950524330'+suffix+'.uasset',Image.open(P/'art'/(target+'-'+kind+'.png')))
src=inspect.getsource(Bundle.write).replace("name='pc9298_mobile_and'","name='pc9306_mobile_and'");ns={};exec('class Writer:\n'+src,Bundle.write.__globals__,ns);ns['Writer'].write(b,P/'art-pack/livedata');(P/'art-validation.json').write_text(json.dumps({'native_private_photos':len(rows),'private_packages':len(b.entries),'old_RGB_blocks_byte_identical':True,'new_hero_photos_pending':missing,'publishable':not missing,'rows':rows,'phone_tested':False},indent=2));print('CARD_ART_BUILD',len(rows),'PENDING_HERO_PHOTOS',missing)
