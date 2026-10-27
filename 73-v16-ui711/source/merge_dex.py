from pathlib import Path
import shutil
P=Path('/tmp/73-ui711/build');d=P/'smali/org/efootballrevival/runtimeprobe';h=P/'helper-smali/org/efootballrevival/runtimeprobe';names={p.stem for p in(P/'java/org/efootballrevival/runtimeprobe').glob('*.java')}
for p in list(d.glob('*.smali')):
 if p.stem.split('$')[0]in names:p.unlink()
for p in h.glob('*.smali'):shutil.copy2(p,d/p.name)
for p in d.glob('*.smali'):
 s=p.read_text();s=s.replace('UI7.10','UI7.11').replace('ui7.10','ui7.11');p.write_text(s)
assert 'DEFAULT_LEVEL_CAP:I = 0x64'in(d/'EditorForm.smali').read_text()
print('SMALI_MERGE_PRESERVED_LEVEL100')

f=d/'PlayerEditorPanel.smali';s=f.read_text();needle='    invoke-virtual {v0, v1}, Landroid/widget/LinearLayout;->addView(Landroid/view/View;)V\n\n    .line 641';assert needle in s;s=s.replace(needle,needle.replace('\n\n    .line 641','\n\n    invoke-static {v15, v0, v11}, Lorg/efootballrevival/runtimeprobe/ProfileEditor;->attachTraits(Landroid/app/Activity;Landroid/widget/LinearLayout;Lorg/json/JSONObject;)V\n\n    .line 641'),1);f.write_text(s);print('TRAITS_UNDER_POSITIONS_ATTACHED')
