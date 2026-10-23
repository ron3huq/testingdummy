"""Compare real private MIC payloads after normalizing only private object names."""
from pathlib import Path
import hashlib,json
from iostore import Toc
from zen_clone import rename
out=Path(__file__).resolve().parent.parent;base='/Game/Assets/character/RealFace/';t=Toc(str(out/'container/pc9298_mobile_and.utoc'));rows=[]
for quality in ['HQ','MQ']:
 canonical=None
 for profile in ['ND06','ND13','NF01','NF27','NFJR','NDHD','NDXS','NDDB','ND08']:
  name='MI_'+profile+'ep00v0313_Head_FaceLegacy_'+quality;dest='MI_COMMONep00v0313_Head_FaceLegacy_'+quality
  imports={base+'T_'+profile+'ep00v0313_Face_'+c:base+'T_COMMONep00v0313_Face_'+c for c in ['D','N','SRO']};repl={base+name:base+dest,name:dest}
  for a,b in imports.items():repl[a]=b;repl[a.rsplit('/',1)[-1]]=b.rsplit('/',1)[-1]
  raw=rename(t.read(t.files['character/RealFace/'+name+'.uasset']),repl,base+name,base+dest,imports=imports)
  if canonical is None:canonical=raw
  assert raw==canonical,(profile,quality)
  rows.append({'profile':profile,'quality':quality,'normalized_sha256':hashlib.sha256(raw).hexdigest()})
(out/'material-equivalence-validation.json').write_text(json.dumps({'status':'WORKING_AND_REPORTED_BLACK_PRIVATE_STATIC_MICS_EQUIVALENT_EXCEPT_NAMES_PASS','rows':rows,'runtime_binding_proven':False,'phone_tested':False},indent=2));print('STATIC_MIC_EQUIVALENCE_PASS',len(rows))
