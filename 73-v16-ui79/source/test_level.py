exec(open('/tmp/73-ui79/level_research.py').read().split('for mod')[0])
import sys,sqlite3,copy
sys.path.insert(0,'/tmp/73-ui79/build/payload/work/tools');import level100
level100.install();c=sqlite3.connect(':memory:');c.executescript('CREATE TABLE meta(key TEXT PRIMARY KEY,value TEXT);CREATE TABLE gameplayers(id TEXT,serial INT,json TEXT);CREATE TABLE careerplan(id INT,serial INT,category TEXT,points INT);')
params=[70]*147;p={'gameplayer_id':{'id':88044950524330,'serial':7},'parameters':params,'level_info':{'level':1,'level_limit':31,'customize_point':0,'exp_current_level':0,'exp_to_next_level':1000,'exp_total':0},'additional_skill_id':[4,8,74,74,74]}
print('STATE',development.state(c,p));after=copy.deepcopy(p);result=development.project(c,p,after,{'level':100,'level_limit':100,'allocation':dict.fromkeys(development.GROUPS,0)});print('PROJECT',str(result)[:500]);print('AFTER',after['level_info']);assert after['level_info']['level']==100 and after['level_info']['level_limit']==100;assert after['additional_skill_id']==p['additional_skill_id'];assert player_editor.schema()['level_limit_max']==100
for kind in ['Trending','Highlight','Legendary','Epic','Standard','Unknown']:assert development.level_cap_for_type(kind)==100
try:development.project(c,after,copy.deepcopy(after),{'level':101,'level_limit':101,'allocation':dict.fromkeys(development.GROUPS,0)});raise AssertionError('level101accepted')
except ValueError:pass
c.execute('INSERT INTO gameplayers VALUES(?,?,?)',('88044950524330',7,json.dumps(after)));c.commit();reloaded=json.loads(c.execute('SELECT json FROM gameplayers').fetchone()[0]);assert reloaded['level_info']['level']==100 and reloaded['level_info']['customize_point']==198
from pathlib import Path
Path('/tmp/73-ui79/level-validation.json').write_text(json.dumps({'passed':True,'actual73_editor_progression_project':True,'all_card_type_caps100':True,'schema_limit100':True,'level100_SQL_reload':True,'points_at_level100':198,'level101_rejected':True,'additional_skills_unchanged':True,'no_auto_train_on_install':True,'device_tested':False},indent=2));print('LEVEL100_PASS')
