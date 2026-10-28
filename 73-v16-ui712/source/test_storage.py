exec(open('/workspace/ronaldo-work/73-ui75/inspect_wire.py').read().split('import my_league')[0])
from pathlib import Path
import sys,sqlite3,json,tempfile,copy,time,base64,io
P=Path('/workspace/73-ui712');T=P/'build/apk/assets/gateway-release/work/tools';sys.path.insert(0,str(T))
import body_dimensions as body,myleague_editor_runtime as editor,stat_editor as stats,motion_editor as motion,transfer_editor as tr,photo_editor as photo,world_skills as world
root=Path(tempfile.mkdtemp(prefix='ui712-storage-',dir='/tmp'));tools=root/'work/tools';tools.mkdir(parents=True);editor.PATH=tools/'myleague_editor.json';editor.PATH.write_text(json.dumps(editor.DEFAULT));body.ROOT=root
c=sqlite3.connect(root/'test.sqlite3');c.executescript('CREATE TABLE meta(key TEXT PRIMARY KEY,value TEXT);CREATE TABLE gameplayers(id TEXT,serial INTEGER,json TEXT);')
pid='88044950524330';req={'id':pid,'serial':1};params=[0]*147;params[47]=185;params[48]=80;params[70]=1;player={'parameters':params,'_careerplan_base_parameters':list(params),'additional_skill_id':[3,74,74,74,74],'gameplayer_id':{'id':int(pid),'serial':1},'level_info':{'level':100}}
for serial in [1,2]:c.execute('INSERT INTO gameplayers VALUES(?,?,?)',(pid,serial,json.dumps(player)))
c.commit();stats.manage(c,'ui712_stats_apply',dict(req,values={'14':127,'20':0,'34':103}));p=json.loads(c.execute('SELECT json FROM gameplayers WHERE serial=2').fetchone()[0]);assert p['parameters'][14]==127 and p['parameters'][20]==0 and p['parameters'][34]==103;assert p['additional_skill_id']==player['additional_skill_id']and p['level_info']==player['level_info']
for x in [-1,128,True,'99']:
 try:stats.validate({'14':x});raise AssertionError('bad stat accepted')
 except ValueError:pass
assert stats.inject(copy.deepcopy(editor.DEFAULT))['players'][0]['ui712_stats']
motion.manage(c,'ui712_motion_apply',dict(req,source='89138556572074'));assert motion.profiles[pid]=='89138556572074';assert motion.manage(c,'ui712_motion_search',{'query':'kaka'})['total']>0
try:motion.check_graph({'1':'2','2':'1'});raise AssertionError('cycle accepted')
except ValueError:pass
import appearance_gear as gear
colors={'4':'#fa1734','5':'#2093fe','7':'#31cc91'}
ge=gear.manage(c,'ui710_equipment_apply',dict(req,section='accessories',values={'accessories':{'4':2,'5':2,'7':2},'accessory_colors':colors,'sleeve':'cutlong'}));assert ge['saved'];assert gear.manage(c,'ui710_equipment_get',req)['values']['accessory_colors']==colors
assert any(r['accessory_colors']==colors and r['sleeve']=='cutlong'for r in json.loads(editor.PATH.read_text())['players']if r['id']==pid)
for bad in ['#00000000','#xyz000','#12345','red']:
 try:gear.validate({'accessory_colors':{'4':bad}});raise AssertionError('Invalid accessory color accepted')
 except ValueError:pass
# The exact22 classic plans, without guessed formations or duplicate shirts.
import myleague_worlds
classic=myleague_worlds.config()['classic_teams'];count=0
for tid,d in classic.items():
 row=tr.classic(int(tid),d.get('competition',518));assert row and row['verified_formation'];count+=1
assert count==22
row=tr.classic(4937,473);request={'team_id':4937,'competition':473};reply=tr.manage(c,'ui712_transfer_get',request);assert reply['ready'];team=reply['team'];team['roster'][1]['shirt']=98
tr.manage(c,'ui712_transfer_save',dict(request,revision=team['revision'],team=team));assert tr.source(4937,473)['roster'][1]['shirt']==98
try:tr.manage(c,'ui712_transfer_save',dict(request,revision='stale',team=team));raise AssertionError('stale edit accepted')
except ValueError:pass
bad=copy.deepcopy(team);bad['roster'][1]['shirt']=bad['roster'][0]['shirt']
try:tr.validate_team(bad);raise AssertionError('duplicate shirt accepted')
except ValueError:pass
# Every role adds flags without clearing originals or Additional Skills.
for role in range(13):
 p=copy.deepcopy(player);p['parameters'][0]=role;p['parameters'][143]=1;out=world.project(p,128);assert all(out['parameters'][f]for f in world.flags(role));assert out['parameters'][143]==1 and out['additional_skill_id']==player['additional_skill_id'];assert world.project(p,518)is p
trace=[];c.set_trace_callback(trace.append);trace.clear();t=time.perf_counter()
for _ in range(1000):stats.project(player);editor.project(player,128)
ms=(time.perf_counter()-t)*1000;assert not trace;projection_queries=len(trace)
# Full browser-shaped512RGBA PNG -> native BGRA payload; atomic manifest advertisement.
from PIL import Image
photo.LIVE=root/'livedata/ui712-photos';photo.STATE=tools/'ui712-photo-state.json'
def png(w,h):
 im=Image.new('RGBA',(512,512));im.paste((170,80,30,255),(0,0,w,h));out=io.BytesIO();im.save(out,format='PNG');return'data:image/png;base64,'+base64.b64encode(out.getvalue()).decode()
out=photo.manage(c,'ui712_photo_apply',dict(req,mini=png(128,128),large=png(184,256)));assert out['saved']and photo.STATE.is_file();meta=json.loads(photo.STATE.read_text());assert meta['count']==1;v=photo.advertise({'livedata_list':[],'version_file':json.dumps({'version':1,'dt880':[]})},8085);assert len(v['livedata_list'])==3 and all('/ui712-photos/g_'in x['url']for x in v['livedata_list']);assert json.loads(v['version_file'])['dt880'][0]['name']=='pc9311'
# Stale generated resources are bounded; unrelated directories are preserved.
old=photo.LIVE/('g_'+'0'*24);old.mkdir();(old/'dummy').write_text('old');unrelated=photo.LIVE/'keep-user-folder';unrelated.mkdir();photo.prune_generations(meta['generation'],'1'*24);assert not old.exists()and unrelated.exists()
# Reject edits after engine launch, without touching data or current resources.
before=photo.STATE.read_bytes();body.engine_loaded=lambda:True
try:photo.manage(c,'ui712_photo_apply',dict(req,mini=png(128,128),large=png(184,256)));raise AssertionError('live edit accepted')
except ValueError:pass
assert photo.STATE.read_bytes()==before
(P/'storage-validation.json').write_text(json.dumps({'passed':True,'accessory_color_storage_and_opaque_hex_validation':True,'cut_sleeve_is_separate_from_original_long':True,'stats_minmax_and_all_owned_instances':True,'native_motion_donor_and_cycle_rejection':True,'classic_plans_validated':count,'team_revision_and_duplicate_validation':True,'all13_world_roles_preserve_existing_skills':True,'projection_calls':2000,'projection_elapsed_ms':round(ms,2),'projection_SQL_queries':projection_queries,'custom_photo_full_native_generation':True,'old_photo_generations_pruned_safely':True,'immutable_nested_resource_urls':True,'live_edit_rejected':True,'Android_tested':False},indent=2));print('STORAGE_PASS',round(ms,2),'ms per2000 projection calls')
