"""Run the experimental adapter ELF with genuine native team-identity getters.
Original rule builder is a boundary fixture. No installed hook/phone claim.
"""
import hashlib,json,struct,sys
from pathlib import Path
from elftools.elf.elffile import ELFFile
from unicorn import Uc,UC_ARCH_ARM64,UC_MODE_ARM
from unicorn.arm64_const import *
from test_native_aggregate import SHA

def run(library,engine_path):
    raw=Path(engine_path).read_bytes();assert hashlib.sha256(raw).hexdigest()==SHA
    u=Uc(UC_ARCH_ARM64,UC_MODE_ARM);base=0x10000000;engine=0x40000000;heap=0x20000000;stop=0x30000000
    with open(library,'rb')as f:
        elf=ELFFile(f);segments=[s for s in elf.iter_segments()if s['p_type']=='PT_LOAD'];size=max(s['p_vaddr']+s['p_memsz']for s in segments);u.mem_map(base,(size+4095)&~4095)
        for seg in segments:u.mem_write(base+seg['p_vaddr'],seg.data())
        syms={s.name:base+s['st_value']for s in elf.get_section_by_name('.symtab').iter_symbols()if s['st_value']}
        reloc=elf.get_section_by_name('.rela.dyn')
        if reloc:
            for r in reloc.iter_relocations():assert r['r_info_type']==1027;u.mem_write(base+r['r_offset'],struct.pack('<Q',base+r['r_addend']))
    u.mem_map(heap,0x200000);u.mem_map(stop,4096)
    # return0x1234 from the boundary original; no input changes are hidden here.
    original=stop+0x100;u.mem_write(original,struct.pack('<II',0xd2824680,0xd65f03c0))
    for rva,size in [(0x72ebecc,72),(0x6a64b84,4)]:
        addr=engine+rva;u.mem_map(addr&~4095,4096);u.mem_write(addr,raw[rva-0x4000:rva-0x4000+size])
    def w(addr,fmt,*values):u.mem_write(addr,struct.pack('<'+fmt,*values))
    def call(name,*args):
        for i in range(8):u.reg_write(UC_ARM64_REG_X0+i,args[i]if i<len(args)else 0)
        u.reg_write(UC_ARM64_REG_SP,heap+0x1f0000);u.reg_write(UC_ARM64_REG_LR,stop)
        u.emu_start(syms[name],stop,count=100000);assert u.reg_read(UC_ARM64_REG_PC)==stop,name
        return u.reg_read(UC_ARM64_REG_X0)
    source=heap+0x10000;out=heap+0x1000;baseline=bytes([0x5a])*0x200
    def team_ids(h,a,src=source):
        w(src+0xad38+0x10,'I',h);w(src+0xad38+0x13a0+0x10,'I',a)
    assert call('ucl_rules_bind',engine,original)==1
    # Disabled adapter preserves output and original return value.
    team_ids(4219,114);u.mem_write(out,baseline);assert call('ucl_rule_hook',out,source)==0x1234;assert bytes(u.mem_read(out,len(baseline)))==baseline
    assert call('ucl_rules_arm',123,4219,114,0,1,1)==1
    assert call('ucl_rules_arm',123,4219,114,0,1,1)==1
    assert call('ucl_rules_arm',123,4219,114,7,1,1)==0
    assert call('ucl_rules_arm',124,4219,114,0,1,1)==0
    team_ids(101,114);u.mem_write(out,baseline);call('ucl_rule_hook',out,source);assert bytes(u.mem_read(out,len(baseline)))==baseline
    team_ids(4219,114);u.mem_write(out,baseline);assert call('ucl_rule_hook',out,source)==0x1234
    actual=bytes(u.mem_read(out,len(baseline)));expected=bytearray(baseline);expected[0x12a]=1;struct.pack_into('<HH',expected,0x12c,0,1);expected[0x135:0x137]=b'\0\0';assert actual==expected
    # Different native source cannot receive the armed input, even same teams.
    other=source+0x20000;team_ids(4219,114,other);u.mem_write(out,baseline);call('ucl_rule_hook',out,other);assert bytes(u.mem_read(out,len(baseline)))==baseline
    assert call('ucl_rules_clear',124)==0;assert call('ucl_rules_clear',123)==1
    # Physical home/away may differ from the fixture: map carry by team identity.
    assert call('ucl_rules_arm',125,4219,114,2,3,1)==1;team_ids(114,4219);u.mem_write(out,baseline);call('ucl_rule_hook',out,source)
    assert struct.unpack('<HH',bytes(u.mem_read(out+0x12c,4)))==(3,2)
    assert call('ucl_rules_clear',125)==1
    assert call('ucl_rules_arm',126,4219,114,100,0,1)==0
    assert call('ucl_rules_arm',126,4219,4219,0,0,1)==0
    assert call('ucl_rules_arm',126,4219,114,1,0,0)==0
    print(json.dumps(dict(passed=True,actual_compiled_arm64_adapter=True,genuine_native_team_getters=True,unrelated_teams_unchanged=True,disabled_unchanged=True,output_only_verified_fields_changed=True,source_pointer_binding=True,carry_follows_physical_team_order=True,retry_and_clear_guards=True,original_rule_builder_mocked=True,native_hook_installed=False,phone_verified=False),indent=2))
if __name__=='__main__':run(*sys.argv[1:])
