from pathlib import Path
import shutil
P=Path('/workspace/73-ui712/build');d=P/'smali/org/efootballrevival/runtimeprobe';h=P/'helper-smali/org/efootballrevival/runtimeprobe';names={f.stem for f in(P/'java/org/efootballrevival/runtimeprobe').glob('*.java')}
for f in d.glob('*.smali'):
 if f.stem.split('$')[0]in names:f.unlink()
for f in h.glob('*.smali'):shutil.copy2(f,d/f.name)
for f in d.glob('*.smali'):
 s=f.read_text().replace('UI7.11','UI7.12').replace('ui7.11','ui7.12');f.write_text(s)
assert 'DEFAULT_LEVEL_CAP:I = 0x64'in(d/'EditorForm.smali').read_text()
assert 'ProfileEditor;->attachTraits'in(d/'PlayerEditorPanel.smali').read_text()
print('UI711_PRIOR_CLASSES_AND_TRAITS_PRESERVED')

p=d/'CardDesignerPanel.smali';s=p.read_text();needle='    const-string v1, "https://card-designer.local/index.html?workspace=phone&ui=UI5-E169-mobile-10"';assert needle in s
s=s.replace(needle,'''    iget-object v2, p0, Lorg/efootballrevival/runtimeprobe/CardDesignerPanel;->activity:Landroid/app/Activity;
    invoke-static {v0, v2}, Lorg/efootballrevival/runtimeprobe/PortraitEditor;->mount(Landroid/webkit/WebView;Landroid/app/Activity;)V
'''+needle+'''
    invoke-static {v1}, Lorg/efootballrevival/runtimeprobe/PortraitEditor;->url(Ljava/lang/String;)Ljava/lang/String;
    move-result-object v1
''');p.write_text(s)
