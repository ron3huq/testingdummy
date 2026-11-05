"""Run RC7 and candidate against actual engine cursor accessors and mode predicate.
This deliberately does not call a mocked engine an on-phone movement test.
"""
from pathlib import Path
import json,hashlib,subprocess,sys
R=Path(__file__).parent
fixture=(R/'test_live_roster.py').read_text()
extra='''
mode=call(0x7317168,pad+0x5c)
u.reg_write(UC_ARM64_REG_X0,mode)
u.emu_start(0x6fc563c,0x6fc5648,count=10)
fixed_family=u.reg_read(UC_ARM64_REG_X0)
assert fixed_family==EXPECTED_FAMILY,(mode,fixed_family)
print('NATIVE_MODE',mode,'NATIVE_FIXED_FAMILY',fixed_family)
'''
# Insert while live, before selecting a bench player deactivates interception.
where='# Bench selection must wait'
assert where in fixture
rows=[]
for old in [True,False]:
 s=fixture
 if old:
  s=s.replace("R=Path('/workspace/work/full8-rc8')","R=Path('/workspace/work/full8-rc7')")
  s=s.replace("assert call(0x7317168,pad+0x5c)==1","assert call(0x7317168,pad+0x5c)==3",1)
  s=s.replace("assert struct.unpack('<I',u.mem_read(match+0x1998+8,4))[0]==1","assert struct.unpack('<I',u.mem_read(match+0x1998+8,4))[0]==3",1)
  s=s.replace('assert st(25)>0 and st(26)==1 and st(27)==1','')
 s=s.replace(where,extra.replace('EXPECTED_FAMILY','1' if old else '0')+'\n'+where)
 p=R/('_baseline_mode.py' if old else '_candidate_mode.py');p.write_text(s)
 result=subprocess.run([sys.executable,str(p)],capture_output=True,text=True);assert result.returncode==0,result.stdout+result.stderr
 rows.append({'build':'RC7' if old else 'RC8-candidate','output':result.stdout.strip(),'sha256':hashlib.sha256((Path('/workspace/work/full8-rc7')if old else R).joinpath('libsingle_player_live.so').read_bytes()).hexdigest()})
report={'passed':True,'phone_verified':False,'test_scope':'real ARM64 cursor accessors and fixed-mode predicate on synthetic match context; no movement simulation','results':rows}
(R/'single-manual-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
