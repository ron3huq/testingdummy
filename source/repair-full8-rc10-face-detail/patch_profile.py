"""Add a card-specific startup palette selector. Never modifies a cached resource key.
Original exports, relocations, symbols, data RVAs, non-target profiles stay intact.
"""
from pathlib import Path
import struct,hashlib,io,json
from elftools.elf.elffile import ELFFile

def build(original,stub,out):
 b=bytearray(Path(original).read_bytes());assert hashlib.sha256(b).hexdigest()=='b53b1f9f53d6d73dd20fcfa1860efe6240282f59628320baee84a0b8070f3443';e=ELFFile(io.BytesIO(b));assert e.num_segments()==9
 symbols={s.name:s['st_value']for s in e.get_section_by_name('.symtab').iter_symbols()};a=symbols['profile_for'];assert a==0x1a5e8
 seg=next(s for s in e.iter_segments()if s['p_type']=='PT_LOAD'and s['p_vaddr']<=a<s['p_vaddr']+s['p_filesz']);off=seg['p_offset']+a-seg['p_vaddr'];assert b[off:off+4]==struct.pack('<I',0xd29f00c8)
 with Path(stub).open('rb')as f:
  se=ELFFile(f);t=se.get_section_by_name('.text');assert t['sh_addr']==0x101000;code=t.data();ss={s.name:s['st_value']for s in se.get_section_by_name('.symtab').iter_symbols()}
 at=(len(b)+65535)&~65535;rx=0x100000;rw=0x110000;assert max(s['p_vaddr']+s['p_memsz']for s in e.iter_segments()if s['p_type']=='PT_LOAD')<rx
 ph=e['e_phoff'];headers=[bytes(b[ph+i*56:ph+(i+1)*56])for i in range(9)];headers[0]=struct.pack('<II6Q',6,4,at,rx,rx,11*56,11*56,8)
 headers.extend([struct.pack('<II6Q',1,5,at,rx,rx,4096+len(code),4096+len(code),65536),struct.pack('<II6Q',1,6,at+65536,rw,rw,5,5,65536)])
 b.extend(bytes(at+65536+5-len(b)));b[at:at+11*56]=b''.join(headers);b[at+4096:at+4096+len(code)]=code;b[at+65536:at+65536+5]=b'R9B2\0'
 struct.pack_into('<Q',b,32,at);struct.pack_into('<H',b,56,11);delta=ss['rc8_profile']-a;assert delta%4==0;struct.pack_into('<I',b,off,0x14000000|((delta//4)&0x3ffffff))
 Path(out).write_bytes(b);return {'configure_rva':ss['rc8_configure'],'profile_export_rva':symbols['noodle_profile_char'],'sha256':hashlib.sha256(b).hexdigest()}
if __name__=='__main__':
 import sys
 print(json.dumps(build(*sys.argv[1:]),indent=2))
