import os,re,sys
roots=sys.argv[1:]
defs_cls=set();defs_m=set();defs_f=set();supers={}
refs=[]
mre=re.compile(r'(L[\w/$\-]+;)->([\w$<>\-]+)(\([^)]*\)[\w/$;\[]+)')
fre=re.compile(r'(L[\w/$\-]+;)->([\w$\-]+):([\w/$;\[]+)')
for r in roots:
  for d,_,fs in os.walk(r):
    for f in fs:
      if not f.endswith('.smali'):continue
      p=os.path.join(d,f);t=open(p).read()
      cls=re.search(r'^\.class.* (L\S+;)$',t,re.M).group(1);defs_cls.add(cls)
      sp=re.search(r'^\.super (L\S+;)',t,re.M);supers[cls]=sp.group(1) if sp else None
      for m in re.finditer(r'^\.method.* ([\w$<>\-]+\(.*)$',t,re.M):defs_m.add(cls+'->'+m.group(1))
      for m in re.finditer(r'^\.field.* ([\w$\-]+:[^\s=]+)',t,re.M):defs_f.add(cls+'->'+m.group(1))
      if '/classes5' in r or r.endswith('merged'):
        for m in mre.finditer(t):refs.append((p,m.group(1),m.group(1)+'->'+m.group(2)+m.group(3)))
        for m in fre.finditer(t):refs.append((p,m.group(1),m.group(1)+'->'+m.group(2)+':'+m.group(3)))
def found(cls,rest):
  c=cls
  while c in defs_cls:
    if c+rest in defs_m or c+rest in defs_f:return True
    c=supers.get(c)
  if c is None or c.startswith('Lorg/efootballrevival') or c.startswith('Lfi/iki'): return False
  ext.add((cls+rest, c)); return True
bad={};ext=set()
for p,cls,ref in refs:
  if not(cls.startswith('Lorg/efootballrevival') or cls.startswith('Lfi/iki')):continue
  rest=ref[len(cls):]
  if cls not in defs_cls: bad.setdefault(ref,set()).add(os.path.basename(p));continue
  if not found(cls,rest): bad.setdefault(ref,set()).add(os.path.basename(p))
for k,v in sorted(bad.items()):print(k,sorted(v)[:3])
print('missing',len(bad))
import collections
print('external-assumed',len(ext))
for (r,c) in sorted(ext):
  print('  EXT',r,'via',c)
