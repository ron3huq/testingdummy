from pathlib import Path
import json,shutil,re,subprocess,os
R=Path(__file__).parent;P=Path('/workspace/analysis/my-league/ronaldo-pc-conversion');N=P/'android-five-combined';N.mkdir(exist_ok=True);S=P/'android-orc-v1';targets=json.loads((R/'targets.json').read_text());mapping={k:v['card_id']for k,v in targets.items()};version='five-faces-neck2006-v1'
for name in ['zen_clone.py','build_native.sh','noodle_hair.py','noodle_hair.c','validate_native.py','validate_install.py','validate_runtime.py']:
 s=(S/name).read_text()
 if name=='noodle_hair.py':
  s=s.replace("{'orc':'53878485695166'}",repr(mapping)).replace("['53878485695166']",repr(list(mapping.values()))).replace('orc-supplied-sculpt-v1',version).replace("version['version']+=35","version['version']+=36")
 if name=='noodle_hair.c':
  a=s.index('static int target_kind(');b=s.index('\n',a);s=s[:a]+'static int target_kind(uptr id){return '+''.join('id=='+v['card_id']+'UL?'+str(i+1)+':'for i,v in enumerate(targets.values()))+'0;}'+s[b:]
  s=re.sub(r'const char\*priv=variant==1\?"ND01"[^;]*;', 'const char*priv='+''.join('variant=='+str(i+1)+'?"'+v['prefix']+'":'for i,v in enumerate(targets.values()))+'"ND01";',s)
 if name in ['validate_install.py','validate_runtime.py']:s=s.replace('orc-supplied-sculpt-v1',version).replace('+35','+36')
 if name=='validate_native.py':
  a=s.index("report={'status':")
  s=s[:a]+'''# Exact-card dispatch and original fallback for all five requested IDs.
'''+''.join("es=request("+v['card_id']+",'"+str(20000+i)+"ep01v0999');assert es[1][1].count('SK_"+v['prefix']+"_Face')==2;checks.append('card_"+k+"');u.mem_write(closure,struct.pack('<Q',actor));u.mem_write(result,b'\\0'*8);at=len(events);call(done,closure,result,detail);assert 'ND0'not in events[-1][1]and'"+str(20000+i)+"ep01v0999'in events[-1][1];checks.append('fallback_"+k+"')\n"for i,(k,v)in enumerate(targets.items()))+'''# Interleave actor requests, then verify each cache restores its own original key.
primary_actor=actor
for off,card,key in [(0,53878485695166,'21001'),(0x20000,70379213169392,'21002'),(0x40000,106783356083208,'21005')]:
 actor=primary_actor+off;request(card,key)
for off,key in [(0x20000,'21002'),(0,'21001'),(0x40000,'21005')]:
 actor=primary_actor+off;u.mem_write(closure,struct.pack('<Q',actor));u.mem_write(result,b'\\0'*8);call(done,closure,result,detail);assert key in events[-1][1]and'ND0'not in events[-1][1];checks.append('interleaved_'+key)
actor=primary_actor
'''+s[a:]
 (N/name).write_text(s)
env=os.environ.copy();env.update(ZIG_GLOBAL_CACHE_DIR='/workspace/.cache/zig-global',ZIG_LOCAL_CACHE_DIR='/workspace/.cache/zig-local');env['PATH']='/workspace/.venvs/testingdummy/bin:'+env['PATH'];subprocess.run(['sh',str(N/'build_native.sh')],env=env,check=True);subprocess.run(['/workspace/.venvs/testingdummy/bin/python',str(N/'validate_native.py')],check=True);print('FIVE_CARD_NATIVE_DISPATCH_TESTED')
