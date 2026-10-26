from pathlib import Path
import shutil
P=Path('/workspace/ronaldo-work/73-ui77');O=P.with_name('73-ui76')
for n in ['java','smali','stubs-out','payload','native']:shutil.copytree(O/n,P/n,dirs_exist_ok=True)
# Reproducible research extracts, not user inputs; their generator remains available.
for f in Path('/workspace/ronaldo-work/73-ui73/celebration-research').glob('*.bin'):f.unlink()
for name in ['body_dimensions.py','myleague_editor_runtime.py']:
 f=P/'payload/work/tools'/name;s=f.read_text().replace('140<=h<=220','140<=h<=255').replace('40<=w<=130','40<=w<=250').replace('140–220cm; weight40–130kg','140–255cm; weight40–250kg').replace('integer(value,140,220)','integer(value,140,255)').replace('integer(value,40,130)','integer(value,40,250)');f.write_text(s)
f=P/'java/org/efootballrevival/runtimeprobe/BodyEditor.java';s=f.read_text().replace('140–220','140–255').replace('40–130','40–250').replace('h>220','h>255').replace('w>130','w>250');f.write_text(s)
f=P/'native/select_team.c';s=f.read_text().replace('value<=220','value<=255').replace('value<=130','value<=250')
s=s.replace('static int editor_player_scope(EditorPlayer*p,u32 cid){','static int editor_has_skill_override(EditorPlayer*p){for(u32 i=70;i<=143;i++)if(p->present[i])return 1;return 0;}\nstatic int editor_player_scope(EditorPlayer*p,u32 cid){').replace('if(!p->cid&&(p->id==','if(!p->cid&&(editor_has_skill_override(p)||p->id==')
s=s.replace('model_applies,model_scopes_failed','model_applies,model_scopes_failed,model_final_applies;static volatile uptr model_last_id;static volatile u32 model_arm_before,model_arm_after')
s=s.replace('ix==2?model_applies:model_scopes_failed;', 'ix==2?model_applies:ix==3?model_scopes_failed:ix==4?model_final_applies:ix==5?model_last_id:ix==6?model_arm_before:model_arm_after;')
s=s.replace('if(model_rows[i].id==id){for(u32 k=0;k<11;k++)','if(model_rows[i].id==id){model_last_id=id;model_arm_before=*(u32*)((unsigned char*)spec+0x30);for(u32 k=0;k<11;k++)').replace('(float)model_rows[i].fields[k]/7.0f-1.0f;return;','(float)model_rows[i].fields[k]/7.0f-1.0f;model_arm_after=*(u32*)((unsigned char*)spec+0x30);model_final_applies++;return;');f.write_text(s)
f=P/'payload/work/tools/select_team_runtime.py';s=f.read_text().replace("['ready','profiles','applies','scope_failures']","['ready','profiles','applies','scope_failures','final_float_applies','last_card_id','arm_before_float_bits','arm_after_float_bits']");f.write_text(s)
f=P/'smali/org/efootballrevival/runtimeprobe/UiStringsData.smali';f.write_text(f.read_text().replace('UI7.6','UI7.7'))
shutil.copy2('/workspace/ronaldo-work/73-v25-full/test-gateway/work/tools/editor_skill_labels.json',P/'payload/work/tools/innate_skill_labels.json')
