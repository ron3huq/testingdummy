from pathlib import Path
import sys,inspect,json
sys.path.insert(0,'/workspace/testingdummy/efootxi-1.3.2/player-faces-v25/source');from iostore import Toc;from bundle_tools import Bundle
P=Path('/tmp/73-ui79');t=Toc(str(P/'heads/livedata/pc9298_mobile_and.utoc'));b=Bundle(t);b.files={k:v for k,v in b.files.items()if any(token in k for token in ['NHUL','NH0001','NSPD','NS0001'])};pids={int.from_bytes(v[0][:8],'little')for k,v in b.files.items()if k.endswith('.uasset')};b.entries={k:v for k,v in b.entries.items()if k in pids}
src=inspect.getsource(Bundle.write).replace("name='pc9298_mobile_and'","name='pc9305_mobile_and'");ns={};exec('class Writer:\n'+src,Bundle.write.__globals__,ns);ns['Writer'].write(b,P/'hero-pack/livedata');print('HERO_PACK',len(b.files),len(pids))
