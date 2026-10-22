from pathlib import Path
import json,re,hashlib
from skills_verified import SKILLS,MOTIONS
r=Path(__file__).parent;d=json.loads((r/'catalog.json').read_text());apk=r.parent/'reference-editor-apk/assets/ext.js';s=apk.read_text();skills=s[s.index('const PLAYER_SKILLS = ['):s.index('const playStyleLabel')]
lookup={int(ix):name for ix,name in re.findall(r'parameter: (\d+), en: "([^"]+)"',skills)}
alias={'Long Throws':'Long Throw','Long-Reach Tackle':'Long Reach Tackle','GK Directing Defense':'GK Directing Defence'}
assert len(SKILLS)==64 and len({i for i,n in SKILLS})==64
for ix,name in SKILLS:assert lookup[ix]==alias.get(name,name),(ix,name,lookup.get(ix))
assert dict(SKILLS)[131]=='Attack Trigger' and 140 not in dict(SKILLS)
assert d['skills']==[list(x)for x in SKILLS]and d['motions']==[list(x)for x in MOTIONS]
assert not d['default']['players']and not d['default']['teams']and not d['default']['packs']
assert len(d['players'])==len({p[0]for p in d['players']})==46610
for ix,name,maxv in MOTIONS:
 assert all(0<=p[3][ix]<=maxv for p in d['players']if p[3])
report=dict(status='VERIFIED_LABELS_AND_CATALOG_PASS',skill_labels=64,unresolved=['Defensive Fortress'],reference_apk_sha256=hashlib.sha256(Path('/workspace/attachments/b1d9c43e-0dab-42a2-8db2-4ef7c737573d/eFootbase_Ziru_Editor_sign.apk').read_bytes()).hexdigest(),attack_trigger_parameter=131,hidden_placeholders=True,motion_enum_registration_log='motion-string-xrefs.txt',motion_widths=[2,3,4,3,4],catalog_players=len(d['players']),pack_registry_players=len(d['packPlayerIds']),empty_default_project=True)
(r/'catalog-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(report['status'])
