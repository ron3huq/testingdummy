from pathlib import Path
import struct,hashlib,re
from elftools.elf.elffile import ELFFile
T=Path('/workspace/work/full8-rc3/payload/assets/gateway-release/work/tools');p=T/'libsingle_player.so';b=bytearray(p.read_bytes())
with p.open('rb')as f:
 e=ELFFile(f);site=0x120e8;s=next(s for s in e.iter_segments()if s['p_type']=='PT_LOAD'and s['p_vaddr']<=site<s['p_vaddr']+s['p_filesz']);off=s['p_offset']+site-s['p_vaddr'];word=struct.unpack_from('<I',b,off)[0];assert word&0x7f00001f==0x34000009;struct.pack_into('<I',b,off,0xd503201f)
p.write_bytes(b);p=T/'single_player_runtime.py';s=p.read_text();s=re.sub("HOOK_SHA='[a-f0-9]+'","HOOK_SHA='"+hashlib.sha256(b).hexdigest()+"'",s);p.write_text(s)
print('Removed second AI gate in actual control-entry function')
