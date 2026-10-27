from pathlib import Path
import shutil
P=Path('/tmp/73-ui710/build');d=P/'smali/org/efootballrevival/runtimeprobe';h=P/'helper-smali/org/efootballrevival/runtimeprobe';names={p.stem for p in(P/'java/org/efootballrevival/runtimeprobe').glob('*.java')}
for p in list(d.glob('*.smali')):
 if p.stem.split('$')[0]in names:p.unlink()
for p in h.glob('*.smali'):shutil.copy2(p,d/p.name)
for p in d.glob('*.smali'):
 s=p.read_text();s=s.replace('UI7.9','UI7.10').replace('ui7.9','ui7.10');p.write_text(s)
assert 'DEFAULT_LEVEL_CAP:I = 0x64'in(d/'EditorForm.smali').read_text()
print('SMALI_MERGE_PRESERVED_LEVEL100')
