from pathlib import Path
import shutil
P=Path('/workspace/ronaldo-work/73-ui78');O=P.with_name('73-ui77')
for name in ['java','smali','stubs-out','payload','native']:shutil.copytree(O/name,P/name,dirs_exist_ok=True)
for name in ['body_dimensions.py','myleague_editor_runtime.py']:
 f=P/'payload/work/tools'/name;s=f.read_text().replace('140<=h<=255','140<=h<=220').replace('40<=w<=250','40<=w<=130').replace('140–255cm; weight40–250kg','140–220cm; weight40–130kg').replace('integer(value,140,255)','integer(value,140,220)').replace('integer(value,40,250)','integer(value,40,130)');f.write_text(s)
f=P/'java/org/efootballrevival/runtimeprobe/BodyEditor.java';f.write_text(f.read_text().replace('140–255','140–220').replace('40–250','40–130').replace('h>255','h>220').replace('w>250','w>130'))
f=P/'native/select_team.c';s=f.read_text().replace('value<=255','value<=220').replace('value<=250','value<=130').replace('(index==60&&value<=127)','(index==59&&value<=511)||(index==60&&value<=127)').replace('p->present[60]','p->present[59]||p->present[60]');f.write_text(s)
f=P/'payload/work/tools/myleague_editor_runtime.py';s=f.read_text().replace('elif ix==60:', 'elif ix==59:integer(value,0,511)\n   elif ix==60:');f.write_text(s)
f=P/'smali/org/efootballrevival/runtimeprobe/PlayerEditorPanel.smali';s=f.read_text().replace('TuningEditor;->attachPhysics','AppearanceChoices;->attach');f.write_text(s)
for f in [P/'smali/org/efootballrevival/runtimeprobe/UiStringsData.smali',P/'java/org/efootballrevival/runtimeprobe/RuntimeDiagnostics.java']:f.write_text(f.read_text().replace('UI7.7','UI7.8'))
