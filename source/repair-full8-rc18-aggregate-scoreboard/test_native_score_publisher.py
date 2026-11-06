"""Execute the native score-publication block, not a synthetic scoreboard.
Entry is an inner block with explicitly supplied valid-display context registers.
Only the current-goal lookup is mocked. No UI rendering/phone claim.
"""
import hashlib,json,struct,sys
from pathlib import Path
from unicorn import Uc,UC_ARCH_ARM64,UC_MODE_ARM,UC_HOOK_CODE
from unicorn.arm64_const import *
SHA='efd257d9e41b622d6ecb8f51f7b0a8ee8820113fd427c5572025df1c8eecc7b8'

def run(engine_path):
    raw=Path(engine_path).read_bytes();assert hashlib.sha256(raw).hexdigest()==SHA
    u=Uc(UC_ARCH_ARM64,UC_MODE_ARM);heap=0x20000000;u.mem_map(heap,0x200000);pages=set()
    for rva,size in [(0x6ba04ac,0x114),(0x73044a0,12),(0x68fb58c,20),(0x72ead9c,36)]:
        for page in range(rva&~4095,(rva+size+4095)&~4095,4096):
            if page not in pages:u.mem_map(page,4096);pages.add(page)
        u.mem_write(rva,raw[rva-0x4000:rva-0x4000+size])
    getter=0x6991db8;u.mem_map(getter&~4095,4096);u.mem_write(getter,bytes.fromhex('c0035fd6'))
    output=heap;rules=heap+0x10000;match_state=heap+0x20000;frame=heap+0x1f0000;goals=(0,0)
    def w(address,fmt,*values):u.mem_write(address,struct.pack('<'+fmt,*values))
    def boundary(uc,address,size,data):
        if address!=getter:return
        assert uc.reg_read(UC_ARM64_REG_X0)==match_state+0x78118
        assert uc.reg_read(UC_ARM64_REG_X2)==5
        side=uc.reg_read(UC_ARM64_REG_X1);assert side in(0,1)
        uc.reg_write(UC_ARM64_REG_X0,goals[side]);uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
    u.hook_add(UC_HOOK_CODE,boundary)
    def publish(carry,current,enabled):
        nonlocal goals
        goals=current;w(rules+0x12a,'B',enabled);w(rules+0x12c,'HH',*carry)
        for reg,value in [(UC_ARM64_REG_X19,output),(UC_ARM64_REG_X20,output+0x61bc),(UC_ARM64_REG_X25,rules),(UC_ARM64_REG_X26,match_state),(UC_ARM64_REG_X29,frame),(UC_ARM64_REG_SP,frame-0x40)]:u.reg_write(reg,value)
        u.emu_start(0x6ba04ac,0x6ba05bc,count=10000);assert u.reg_read(UC_ARM64_REG_PC)==0x6ba05bc
        regular=struct.unpack('<II',bytes(u.mem_read(output+0x61dc,8)))
        aggregate=struct.unpack('<II',bytes(u.mem_read(output+0x61f0,8)))
        visible=bytes(u.mem_read(output+0x61ec,1))[0]
        return dict(match=list(regular),aggregate=list(aggregate),aggregate_visible=visible)
    example=publish((1,0),(0,0),1);assert example==dict(match=[0,0],aggregate=[1,0],aggregate_visible=1)
    update=publish((1,0),(2,1),1);assert update==dict(match=[2,1],aggregate=[3,1],aggregate_visible=1)
    for carry in[(0,1),(2,0),(1,2),(0,0),(3,3)]:
        for current in[(0,0),(1,0),(0,1),(2,2),(3,1)]:
            result=publish(carry,current,1)
            assert result['match']==list(current)and result['aggregate']==[a+b for a,b in zip(carry,current)]and result['aggregate_visible']==1
    hidden=publish((1,0),(2,1),0);assert hidden['match']==[2,1]and hidden['aggregate_visible']==0
    report=dict(passed=True,engine_sha256=SHA,native_publication_block=['0x6ba04ac','0x6ba05bc'],example_matching_reference=example,after_goals=update,comparison_cases=25,aggregate_off_hides_panel_flag=True,current_goals_lookup_mocked=True,valid_display_context_registers_supplied=True,outer_display_gate_executed=False,pixel_layout_verified=False,live_game_hud_binding_verified=False,phone_verified=False)
    print(json.dumps(report,indent=2))
if __name__=='__main__':run(sys.argv[1])
