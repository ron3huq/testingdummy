"""Add two declared ELF load segments; original FULL-7 code/data is preserved.
Only apply_base/apply_rating entry branches change; copied prologues are audited.
"""
from pathlib import Path
import struct,hashlib,io,json
from elftools.elf.elffile import ELFFile
def build(original,stub_elf,out):
 b=bytearray(Path(original).read_bytes());assert hashlib.sha256(b).hexdigest()=='53a7786d44f2fcd4f95724509f37a2a0c98f032eddf2fc2948704e4a0d696b94'
 old=ELFFile(io.BytesIO(b));phoff=old.header['e_phoff'];phsize=old.header['e_phentsize'];assert phsize==56 and old.num_segments()==9
 with Path(stub_elf).open('rb')as f:
  e=ELFFile(f);text=e.get_section_by_name('.text');assert text['sh_addr']==0x10c1000;code=text.data();syms={s.name:s['st_value']for s in e.get_section_by_name('.symtab').iter_symbols()}
 file_at=(len(b)+65535)&~65535;rx=0x10c0000;rw=0x10d0000;assert max(s['p_vaddr']+s['p_memsz']for s in old.iter_segments()if s['p_type']=='PT_LOAD')<=rx
 headers=[bytes(b[phoff+i*56:phoff+(i+1)*56])for i in range(9)];new_n=11;headers[0]=struct.pack('<II6Q',6,4,file_at,rx,rx,new_n*56,new_n*56,8)
 headers +=[struct.pack('<II6Q',1,5,file_at,rx,rx,0x1000+len(code),0x1000+len(code),65536),struct.pack('<II6Q',1,6,file_at+65536,rw,rw,24,24,65536)]
 b.extend(bytes(file_at+65536+24-len(b)));b[file_at:file_at+new_n*56]=b''.join(headers);b[file_at+0x1000:file_at+0x1000+len(code)]=code
 struct.pack_into('<Q',b,32,file_at);struct.pack_into('<H',b,56,new_n)
 for address,expected,target in [(0x2d010,'610b0035ff0302d1fd7b02a9fc6f03a9',syms['rc6_apply']),(0x37180,'ef3bb66ded33016deb2b026de923036d',syms['rc6_rating'])]:
  seg=next(s for s in old.iter_segments()if s['p_type']=='PT_LOAD'and s['p_vaddr']<=address<s['p_vaddr']+s['p_filesz']);off=seg['p_offset']+address-seg['p_vaddr'];assert b[off:off+16].hex()==expected;delta=target-address;assert delta%4==0 and -(1<<27)<=delta<1<<27;struct.pack_into('<I',b,off,0x14000000|((delta//4)&0x3ffffff))
 Path(out).write_bytes(b);return dict(configure_rva=syms['rc6_configure'],editor_apply_player_rva=0x33ca8,sha256=hashlib.sha256(b).hexdigest())
if __name__=='__main__':
 import sys
 print(json.dumps(build(*sys.argv[1:]),indent=2))
