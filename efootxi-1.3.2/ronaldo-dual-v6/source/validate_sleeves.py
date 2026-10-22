from pathlib import Path
import importlib.util,copy,json,ctypes,sys
r=Path(__file__).parent;baseline=r.parents[1]/'hotfix-v18'
if not baseline.exists():baseline=r.parent/'references/v18'
spec=importlib.util.spec_from_file_location('sleeve_overlay',r/'myleague_editor_runtime.py');editor=importlib.util.module_from_spec(spec);spec.loader.exec_module(editor)
s=(baseline/'validate_native.py').read_text();s=s[:s.index('import sys,sqlite3')].replace('r=Path(__file__).parent','r=baseline').replace('/workspace/analysis/my-league/android/official-apk','/workspace/ronaldo-work/apk');exec(compile(s,'v18-elf-loader','exec'),globals())
# Real ARM64 editor methods; only the original UE shirt loader is stubbed.
data=copy.deepcopy(editor.DEFAULT);data['players']=[{'id':'89135066911146','competition':122,'sleeve':'short','parameters':{'17':90}},{'id':'52776558193083','competition':0,'sleeve':'short','parameters':{}}];before=copy.deepcopy(data);editor._config=data
class Function:
 def __init__(self,n):self.n=n
 def __call__(self,*a):return call(symbols[self.n],*a)
class Handle:
 def __getattr__(self,n):f=Function(n);setattr(self,n,f);return f
editor.install_native(Handle());assert data==before and call(symbols['editor_status'],0)==1
stub=0x33000080;u.mem_write(stub,bytes.fromhex('c0035fd6'));call(symbols['configure_appearance_shirt'],0,stub)
owner=0x30000000;actor=0x30010000;w(owner+0x4d8,'Q',actor)
checks=[]
for cid in [122,518,566,128,549]:
 call(symbols['activate_context'],cid)
 for pid,long in [(89135066911146,True),(17592722922839,True),(88044950524330,True),(52776558193083,False),(89135066911147,False),(17592722922839+(1<<32),False)]:
  u.mem_write(actor,b'\x55'*0x2000);w(actor+0x10b0,'Q',pid);w(actor+0x10f0,'I',0);old=bytes(u.mem_read(actor,0x2000));call(symbols['appearance_shirt_hook'],owner,0);new=bytes(u.mem_read(actor,0x2000));want=bytearray(old)
  if long:import struct;struct.pack_into('<I',want,0x10f0,1)
  assert new==bytes(want),(cid,pid);checks.append([cid,pid,long])
Path(__file__).resolve().parent.parent.joinpath('sleeve-validation.json').write_text(json.dumps({'status':'THIRTY_NATIVE_FULL_CARD_SLEEVE_CASES_PASS','checks':checks,'existing_editor_configuration_unchanged':True,'phone_tested':False,'original_shirt_loader_stubbed':True},indent=2));print('30 real ARM64 sleeve cases PASS; only requested field changes')
