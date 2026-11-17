"""Update kits_bundle dt870 identity and propagate sha256 pins through gateway-release text files."""
import hashlib,json,sys,re
from pathlib import Path
G=Path(sys.argv[1])  # assets/gateway-release
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
texts=[p for p in G.rglob('*') if p.is_file() and p.suffix in ('.json','.py') and p.stat().st_size<20_000_000 and 'outputs' not in p.parts]
ORIG=Path(sys.argv[2]) if len(sys.argv)>2 else None
def orig_sha(p):
    if ORIG is not None:
        o=ORIG/p.relative_to(G)
        if o.is_file():return sha(o)
    return sha(p)
before={p:orig_sha(p) for p in texts}
kb=G/'work/tools/kits_bundle.json';d=json.loads(kb.read_text())
cpk=G/'livedata/dt870_ui74_mobile_and.cpk'
old=dict(d['files']['dt870_mobile_and.cpk'])
d['files']['dt870_mobile_and.cpk'].update(size=cpk.stat().st_size,sha256=sha(cpk))
kb.write_text(json.dumps(d,separators=(',',':')) if '\n' not in kb.read_text().strip() else json.dumps(d,indent=1))
# raw replacement of the CPK identity everywhere (size+sha)
repl={old['sha256']:sha(cpk)}
changed={kb}
for it in range(20):
    now={p:sha(p) for p in texts}
    for p in texts:
        if now[p]!=before[p]:repl[before[p]]=now[p]
    for p in (G/'work/tools').iterdir():
        if p.suffix in ('.so','.pyc','.zlib','.gz','.marshal') and ORIG is not None and (ORIG/p.relative_to(G)).is_file():
            o=sha(ORIG/p.relative_to(G)); c=sha(p)
            if o!=c: repl[o]=c
    n=0
    for p in texts:
        s=p.read_text(errors='surrogateescape');t=s
        for a,b in repl.items():
            if a in t:t=t.replace(a,b)
        if t!=s:p.write_text(t,errors='surrogateescape');n+=1;changed.add(p)
    if n==0:break
print('iterations',it,'changed files',sorted(str(p.relative_to(G)) for p in changed))
print('replacements',len(repl))
