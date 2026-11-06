"""Execute actual RC7 ARM64 editor ABI under Unicorn; engine boundaries mocked.
No Android execution is claimed. Native code and original team layout are used.
"""
import hashlib,json,struct,sys
from pathlib import Path
from elftools.elf.elffile import ELFFile
from unicorn import Uc,UC_ARCH_ARM64,UC_MODE_ARM,UC_HOOK_CODE
from unicorn.arm64_const import *
sys.path.insert(0,str(Path(__file__).parents[1]/'repair-full8-rc9-ucl/runtime'))
from ucl_lp_roster import dortmund_row,inject
EXPECTED='674fca3a1293aa06a572124cce8e67ef3251f3c84d70d059bcf29f756df92ab6'

def run(path):
    path=Path(path);raw=path.read_bytes();assert hashlib.sha256(raw).hexdigest()==EXPECTED
    u=Uc(UC_ARCH_ARM64,UC_MODE_ARM);base=0x10000000;engine=0x40000000;heap=0x20000000;stop=0x30000000
    with path.open('rb')as f:
        elf=ELFFile(f);syms={s.name:base+s['st_value']for s in elf.get_section_by_name('.symtab').iter_symbols()if s['st_value']}
        segments=[s for s in elf.iter_segments()if s['p_type']=='PT_LOAD']
        size=max(s['p_vaddr']+s['p_memsz']for s in segments);u.mem_map(base,(size+4095)&~4095)
        for seg in segments:u.mem_write(base+seg['p_vaddr'],seg.data())
        for rel in elf.get_section_by_name('.rela.dyn').iter_relocations():
            assert rel['r_info_type']==1027
            u.mem_write(base+rel['r_offset'],struct.pack('<Q',base+rel['r_addend']))
    u.mem_map(heap,0x200000);u.mem_map(stop,4096);u.mem_write(stop,struct.pack('<I',0xd65f03c0))
    def w(addr,fmt,*value):u.mem_write(addr,struct.pack('<'+fmt,*value))
    def call(name,*args):
        for i in range(8):u.reg_write(UC_ARM64_REG_X0+i,args[i]if i<len(args)else 0)
        u.reg_write(UC_ARM64_REG_SP,heap+0x1f0000);u.reg_write(UC_ARM64_REG_LR,stop)
        
        try:u.emu_start(syms[name],stop,count=10000000)
        except Exception as e:raise RuntimeError((name,hex(u.reg_read(UC_ARM64_REG_PC)),hex(u.reg_read(UC_ARM64_REG_LR))))from e
        assert u.reg_read(UC_ARM64_REG_PC)==stop,(name,hex(u.reg_read(UC_ARM64_REG_PC)))
        return u.reg_read(UC_ARM64_REG_X0)
    row=dortmund_row();ids=[int(p['id'])for p in row['roster']]
    assert inject({'teams':[]})['teams']==[row]
    n=call('editor_add_team',126,122,len(ids),ids.index(int(row['captain'])));assert n==1
    for i,p in enumerate(row['roster']):assert call('editor_team_slot',n,i,int(p['id']),p['shirt'],p['role'],p['x'],p['y'])==1
    for v,plan in enumerate(row['plans']):
        for i,p in enumerate(plan['slots']):assert call('editor_team_plan',n,v,i,p['role'],p['x'],p['y'],plan['flags'])==1
    for i,p in enumerate(row['kickers']):assert call('editor_team_taker',n,i,ids.index(int(p)))==1
    assert call('editor_commit')==1
    # Raw team and player boundaries use the verified RC7 capture layout.
    team=heap+0x1000;players=heap+0x10000;db=heap+0x500;context=heap+0x600
    w(team,'I',126<<14);w(team+0x40c,'I',11<<9)
    for i in range(11):w(team+0x110+16*i,'QQ',0,900000+i)
    w(context+0x40,'Q',db)
    original_team=stop+0x100;original_player=stop+0x200
    addresses={original_team:'team',original_player:'player',engine+0x82a84d4:'parameter',engine+0x82a907c:'setparameter',engine+0x82468d4:'context',engine+0x68fe720:'playerkey'}
    for addr in addresses:
        if addr>=engine:u.mem_map(addr&~4095,4096)
        u.mem_write(addr,struct.pack('<I',0xd65f03c0))
    engine_bytes=Path(sys.argv[2]).read_bytes()
    assert hashlib.sha256(engine_bytes).hexdigest()=='efd257d9e41b622d6ecb8f51f7b0a8ee8820113fd427c5572025df1c8eecc7b8'
    for rva,size in [(0x82b5edc,24),(0x8251cd8,32),(0x70b2fe0,12)]:
        addr=engine+rva;u.mem_map(addr&~4095,4096);u.mem_write(addr,engine_bytes[rva-0x4000:rva-0x4000+size])
    missing=set()
    def boundary(uc,addr,size,data):
        kind=addresses.get(addr)
        if kind is None:return
        x=[uc.reg_read(UC_ARM64_REG_X0+i)for i in range(4)];ret=0
        if kind=='team':ret=team if x[1]>>14==126 else 0
        elif kind=='player':
            pid=x[2]
            if pid in ids and pid not in missing:ret=players+ids.index(pid)*0x100;w(ret,'Q',pid)
        elif kind=='context':ret=context
        elif kind=='parameter':
            w(x[2],'I',0 if x[1]==0 else 185);ret=1
        elif kind=='setparameter':ret=1
        elif kind=='playerkey':
            uc.reg_write(UC_ARM64_REG_X1,struct.unpack('<Q',bytes(uc.mem_read(x[0],8)))[0]);ret=0
        uc.reg_write(UC_ARM64_REG_X0,ret);uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
    u.hook_add(UC_HOOK_CODE,boundary)
    call('configure_team',engine,original_team);call('configure_player',engine,original_player)
    before=bytes(u.mem_read(team,0x5d4));call('activate_context',125)
    # Compare with the same RC7 hook with editor disabled: RC7 itself renames BVB.
    w(syms['editor_ready'],'I',0);call('team_hook',db,126<<14);baseline=bytes(u.mem_read(team,0x5d4))
    u.mem_write(team,before);w(syms['editor_ready'],'I',1);call('team_hook',db,126<<14)
    assert bytes(u.mem_read(team,0x5d4))==baseline,'overlay affected unrelated league'
    call('activate_context',122);call('team_hook',db,126<<14)
    actual=[struct.unpack('<QQ',bytes(u.mem_read(team+0x110+16*i,16)))for i in range(22)]
    assert actual==[(0,pid)for pid in ids],(actual,[call('editor_status',i)for i in range(6)])
    assert(struct.unpack('<I',bytes(u.mem_read(team+0x40c,4)))[0]>>9)&127==22
    assert call('editor_team_status',126)==1,'native editor did not report successful roster'
    assert list(bytes(u.mem_read(team+0x538,11)))==list(range(11))
    assert [struct.unpack('<H',bytes(u.mem_read(team+0x3a2+2*i,2)))[0]for i in range(22)]==[p['shirt']for p in row['roster']]
    call('activate_context',125);call('team_hook',db,126<<14)
    assert bytes(u.mem_read(team,0x5d4))==baseline,'UEFA roster leaked after leaving scope'
    missing.add(ids[0]);call('activate_context',122);call('team_hook',db,126<<14)
    assert bytes(u.mem_read(team,0x5d4))==baseline,'missing native player partially modified roster'
    assert call('editor_status',3)>0,'missing player was not rejected'
    assert call('editor_team_status',126)!=1,'failed native roster reported success'
    assert call('ensure_team',126)!=1,'RC7 editor failure was ignored'
    missing.clear();call('team_hook',db,126<<14)
    assert [struct.unpack('<QQ',bytes(u.mem_read(team+0x110+16*i,16)))for i in range(22)]==[(0,pid)for pid in ids]
    assert call('ensure_team',126)==1,'valid editor roster was not ready'
    report=dict(passed=True,actual_rc7_arm64_editor_executed=True,roster22=True,scope122=True,native_ensure_team_propagates_editor_failure=True,other_scope125_unchanged=True,scope_exit_restores_baseline=True,missing_player_rejected_without_partial_write=True,engine_boundaries_mocked=True,phone_verified=False)
    print(json.dumps(report,indent=2))
if __name__=='__main__':run(sys.argv[1])
