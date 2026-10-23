"""Safely recover user-supplied models/textures. Do not execute archive files."""
from pathlib import Path
import sys,struct,hashlib,json
import libarchive
from PIL import Image

O=Path(__file__).resolve().parent.parent;R=Path('/workspace/ronaldo-work')
archive=O/'original-inputs/Diomande.rar';root=R/'v21-input/diomande';root.mkdir(parents=True,exist_ok=True)
entries=[]
with libarchive.file_reader(str(archive))as files:
    for item in files:
        dest=(root/item.pathname.replace('\\','/')).resolve();assert dest.is_relative_to(root.resolve())
        if item.isdir:continue
        assert item.isfile;dest.parent.mkdir(parents=True,exist_ok=True)
        with dest.open('wb')as f:
            for block in item.get_blocks():f.write(block)
        entries.append({'path':item.pathname,'bytes':dest.stat().st_size,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()})
fp=root/'fpk';fp.mkdir(exist_ok=True);raw=next(root.rglob('face.fpk')).read_bytes();assert raw[:6]==b'foxfpk'
for i in range(struct.unpack_from('<I',raw,36)[0]):
    offset,size,nameoff,namelen=struct.unpack_from('<4Q',raw,48+48*i);name=raw[nameoff:nameoff+namelen].decode();assert Path(name).name==name and offset+size<=len(raw)
    (fp/name).write_bytes(raw[offset:offset+size])
sys.path.insert(0,str(R/'pes-fmdl-blender/pes-fmdl'));from Ftex import ftexToDds
converted=root/'converted';converted.mkdir(exist_ok=True)
for p in root.rglob('*.ftex'):
    target=converted/(p.stem+'.dds');assert ftexToDds(str(p),str(target));Image.open(target).save(target.with_suffix('.png'))
report={'archive':'Diomande.rar','sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'files_opened':entries,'instructions_from_archives_executed':False,'base_player_ids':[176104,84062184]}
(O/'input-inventory.json').write_text(json.dumps(report,indent=2));print('DIOMANDE_FPK_FTEX_SOURCE_RECOVERY_PASS')
