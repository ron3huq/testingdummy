from pathlib import Path
P=Path('/workspace/ronaldo-work/73-ui78');T=P/'payload/work/tools'
f=T/'player_tuning.py';s=f.read_text();s=s.replace('On-demand innate skills and verified physics inputs.', 'On-demand innate skills. Physics controls removed.')
s=s.replace("physics=read(PH)","physics={}")
a=s.index(' for pid,row in physics.items():',s.index('def write_config'));b=s.index(' editor.validate(cfg)',a);s=s[:a]+s[b:]
s=s.replace("'choices':[{'id':i,'label':labels.get(str(i),'Skill '+str(i))}for i in range(74)]", "'choices':[{'id':i,'label':labels.get(str(i),'Unmapped native skill '+str(i))}for i in range(74)if str(i)in labels or i in ids]")
s=s.replace("  else:\n   h,w=body.validate_values(req);jump=check_jump(req.get('jump'));physics=dict(physics);physics[pid]={'jump':jump};body.profiles=dict(body.profiles);body.profiles[pid]={'height':h,'weight':w};changes={47:h,48:w,39:jump}","  else:raise ValueError('Physics controls have been removed')")
s=s.replace("['ui77_skills_get','ui77_skills_apply','ui77_physics_get','ui77_physics_apply']","['ui77_skills_get','ui77_skills_apply']")
# Avoid retaining dormant physics API/body in this release.
s=s.replace("  dims=body.get(conn,req)\n  return dict(dims,jump=physics.get(pid,{}).get('jump',p[39]),metrics_are_derived=True)","  raise ValueError('Unknown tuning action')")
s=s.replace(" if pid in physics:p[39]=physics[pid]['jump']",'')
s=s.replace(" load(module._logic.conn)\n if skills", " load(module._logic.conn)\n import player_editor\n labels=json.loads(Path(__file__).with_name('innate_skill_labels.json').read_text())\n player_editor.SKILL_LABELS.update({int(k):v for k,v in labels.items()})\n if skills")
f.write_text(s)
f=T/'bridge_73.py';s=f.read_text().replace('    card_rules.install_native_config(root)','    import appearance_choices\n    appearance_choices.migrate(root,module._logic.conn)\n    card_rules.install_native_config(root)').replace('    player_tuning.install(module)','    player_tuning.install(module)\n    appearance_choices.install(module)');f.write_text(s)
f=T/'noodle_hair.py';s=f.read_text().replace('    return _handle\n\n\ndef configuration',"    if configure_name=='configure_bake':\n        import appearance_choices,hook_arena\n        appearance_choices.configure_skin_chain(_handle,base,_installed_hooks[(base,entry)][1]+hook_arena.RETURN)\n    return _handle\n\n\ndef configuration");assert 'configure_skin_chain'in s;f.write_text(s)
f=P/'native/select_team.c';s=f.read_text();s+='''
/* Native body palette selection. Reuse the existing noodle bake callback;
   no new inline patches and no frame-time Python/SQL.1..6 are stock palette IDs.
   Face textures are separate assets, not recolored by this field. */
static struct {uptr id;u32 palette;} skin_rows[1024];
static u32 skin_n;static volatile u32 skin_ready;static volatile uptr skin_applies,skin_last_id;static volatile u32 skin_last_palette;
static void(*skin_original)(void*);
__attribute__((visibility("default"))) u32 skin_add(uptr id,u32 palette){if(skin_ready||!id||palette<1||palette>6||skin_n>=1024)return 0;for(u32 i=0;i<skin_n;i++)if(skin_rows[i].id==id)return 0;skin_rows[skin_n].id=id;skin_rows[skin_n++].palette=palette;return 1;}
__attribute__((visibility("default"))) void skin_commit(void){__atomic_store_n(&skin_ready,1,__ATOMIC_RELEASE);}
__attribute__((visibility("default"))) void configure_skin_bake(uptr base,uptr original){(void)base;skin_original=(void*)original;}
__attribute__((visibility("default"))) uptr skin_status(u32 i){return i==0?skin_ready:i==1?skin_n:i==2?skin_applies:i==3?skin_last_id:skin_last_palette;}
__attribute__((visibility("default"))) void skin_bake_hook(void*actor){if(actor&&__atomic_load_n(&skin_ready,__ATOMIC_ACQUIRE)){uptr id=*(uptr*)((unsigned char*)actor+0x10b0);for(u32 i=0;i<skin_n;i++)if(skin_rows[i].id==id){u32*field=(u32*)((unsigned char*)actor+0x42c);if(*field!=skin_rows[i].palette){*field=skin_rows[i].palette;*((unsigned char*)actor+0x1a6b)=1;}skin_applies++;skin_last_id=id;skin_last_palette=*field;break;}}if(skin_original)skin_original(actor);}
''';f.write_text(s)
f=P/'java/org/efootballrevival/runtimeprobe/TuningEditor.java';s=f.read_text();a=s.index(' private static void attach(');b=s.index(' private static void save(',a);s=s[:a]+''' public static void attachSkills(Activity a,LinearLayout panel,JSONObject player){Button b=new Button(a);b.setText("Edit Innate Skills");b.setAllCaps(false);b.setOnClickListener(v->{b.setEnabled(false);new Thread(()->{try{JSONObject data=new JSONObject(manage(a,"ui77_skills_get",player));a.runOnUiThread(()->{b.setEnabled(true);if(!a.isFinishing())skills(a,player,data);});}catch(Exception e){a.runOnUiThread(()->{b.setEnabled(true);error(a,e);});}},"InnateSkillsLoad").start();});panel.addView(b,new LinearLayout.LayoutParams(-1,-2));}
'''+s[b:];a=s.index(' private static EditText field');s=s[:a]+'}\n';f.write_text(s)
