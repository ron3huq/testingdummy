"""Execute real v19.1 native aggregate comparator under Unicorn.
Only live statistic lookup and period lookup are controlled engine boundaries.
This is not a native end-of-match/extra-time or Android integration test.
"""
import hashlib,json,struct,sys
from pathlib import Path
from unicorn import Uc,UC_ARCH_ARM64,UC_MODE_ARM,UC_HOOK_CODE
from unicorn.arm64_const import *
SHA='efd257d9e41b622d6ecb8f51f7b0a8ee8820113fd427c5572025df1c8eecc7b8'

def run(path):
    raw=Path(path).read_bytes();assert hashlib.sha256(raw).hexdigest()==SHA
    u=Uc(UC_ARCH_ARM64,UC_MODE_ARM);heap=0x20000000;stop=0x30000000;u.mem_map(heap,0x200000);u.mem_map(stop,4096)
    ranges=[(0x6cacc80,132),(0x6cacb24,348),(0x72ead9c,52),(0x68fc3d8,16)]
    pages=set()
    for address,size in ranges:
        for page in range(address&~4095,(address+size+4095)&~4095,4096):
            if page not in pages:u.mem_map(page,4096);pages.add(page)
        u.mem_write(address,raw[address-0x4000:address-0x4000+size])
    getters={0x6991db8:'goals',0x72b6f60:'period'}
    for address in getters:
        page=address&~4095
        if page not in pages:u.mem_map(page,4096);pages.add(page)
        u.mem_write(address,bytes.fromhex('c0035fd6'))
    side=heap;stats=heap+0x1000;rules=heap+0x2000;goals=(0,0);period=1
    def w(address,fmt,*values):u.mem_write(address,struct.pack('<'+fmt,*values))
    def boundary(uc,address,size,data):
        kind=getters.get(address)
        if kind is None:return
        if kind=='goals':
            assert uc.reg_read(UC_ARM64_REG_X0)==stats and uc.reg_read(UC_ARM64_REG_X2)==5
            result=goals[uc.reg_read(UC_ARM64_REG_X1)]
        else:
            assert uc.reg_read(UC_ARM64_REG_X0)==stats;result=period
        uc.reg_write(UC_ARM64_REG_X0,result);uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
    u.hook_add(UC_HOOK_CODE,boundary)
    def compare(ours):
        w(side,'I',ours);u.reg_write(UC_ARM64_REG_X0,side);u.reg_write(UC_ARM64_REG_X1,stats);u.reg_write(UC_ARM64_REG_X2,rules)
        u.reg_write(UC_ARM64_REG_SP,heap+0x1f0000);u.reg_write(UC_ARM64_REG_LR,stop)
        u.emu_start(0x6cacc80,stop,count=10000);assert u.reg_read(UC_ARM64_REG_PC)==stop
        return struct.unpack('<i',struct.pack('<I',u.reg_read(UC_ARM64_REG_X0)&0xffffffff))[0]
    checked=0
    # Distinguish match and aggregate differences on both sides; away-goals off.
    for carry in[(0,1),(2,0),(1,2),(0,0),(3,3)]:
        w(rules+0x12a,'B',1);w(rules+0x12c,'HH',*carry);w(rules+0x135,'BB',0,0)
        for goals in[(1,0),(0,0),(1,1),(3,2),(2,3),(4,0)]:
            for ours in(0,1):
                expected=goals[ours]+carry[ours]-goals[1-ours]-carry[1-ours]
                assert compare(ours)==expected,(carry,goals,ours,compare(ours),expected);checked+=1
    # Turning carry off must restore the ordinary per-match comparison.
    w(rules+0x12a,'B',0);w(rules+0x12c,'HH',9,1);goals=(0,0)
    assert compare(0)==compare(1)==0
    # Critical native result: winning1-0 on the night with0-1 carry is tied.
    w(rules+0x12a,'B',1);w(rules+0x12c,'HH',0,1);goals=(1,0);assert compare(0)==0
    # Native flag135 really changes the tied outcome by away-goals comparison.
    w(rules+0x12c,'HH',1,2);goals=(3,2);w(rules+0x135,'B',0);assert compare(0)==0
    w(rules+0x135,'B',1);assert compare(0)<0
    w(rules+0x135,'B',0);assert compare(0)==0
    report=dict(passed=True,engine_sha256=SHA,actual_native_comparator='0x6cacc80 -> 0x6cacb24',aggregate_flag_offset='0x12a',carry_offsets=['0x12c','0x12e'],away_goals_disabled_offsets=['0x135','0x136'],comparison_cases=checked,native_away_goals_flag_independently_checked=True,disabled_flag_restores_normal_comparison=True,leg_win_aggregate_draw_native_result_zero=True,live_goal_and_period_boundaries_mocked=True,end_of_match_branch_verified=False,native_hook_installed=False,phone_verified=False)
    print(json.dumps(report,indent=2))
if __name__=='__main__':run(sys.argv[1])
