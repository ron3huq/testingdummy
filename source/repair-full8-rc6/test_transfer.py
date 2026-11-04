from pathlib import Path
import sys,json,sqlite3,tempfile,copy
R=Path('/workspace/work/full8-rc6');T=R/'payload/assets/gateway-release/work/tools';sys.path[:0]=[str(T),'/workspace/73-v191-migration/decoded']
import transfer_native_data as native,transfer_player_editor as players,transfer_traits as traits,transfer_editor as transfer,myleague_editor_runtime as editor,body_dimensions as body
c=sqlite3.connect(':memory:');c.executescript('CREATE TABLE meta(key TEXT PRIMARY KEY,value TEXT);CREATE TABLE gameplayers(id INTEGER,serial INTEGER,json TEXT);CREATE TABLE player_pool(id INTEGER,serial INTEGER,json TEXT)')
transfer.identity=lambda req:(109,518);transfer.source=lambda tid,cid:{'roster':[{'id':'113911'}]};body.engine_loaded=lambda:False
with tempfile.TemporaryDirectory(dir=R)as d:
 editor.PATH=Path(d)/'config.json';editor.PATH.write_text(json.dumps(editor.DEFAULT));editor._config=None;players._profiles={}
 req={'player_id':'113911'}
 p,source=native.read(c,'113911',518);assert source=='game73_native_base'and len(p)==147 and p[14]==72 and p[43]==0
 got=players.manage(c,'ui712_transfer_player_get',dict(req,section='celebrations'));assert got['values']['parameters']['14']==72
 rows=got['celebration_choices']['59'];assert len(rows)>100 and all('label'in r for r in rows);assert any('Ronaldo'in r['label']for r in rows)
 original=traits.manage(c,'ui712_transfer_traits_get',req);assert original['foot']=={str(i):p[i]for i in(42,43,45)}
 # Merely opening and saving unchanged values must not exempt a player.
 players.manage(c,'ui712_transfer_player_apply',dict(req,values={'parameters':copy.deepcopy(got['values']['parameters'])}))
 assert players.read(c)['518:113911']['parameters']=={}
 assert not any(14<=int(k)<=40 and int(k)!=33 for k in players.runtime_fields('113911',518,players.read(c)['518:113911']))
 # Saving the prefilled panel must only store changed abilities.
 values=copy.deepcopy(got['values']['parameters']);values['14']=81
 assert players.manage(c,'ui712_transfer_player_apply',dict(req,values={'parameters':values}))['saved']
 saved=players.read(c)['518:113911'];assert saved['parameters']['14']==81 and len(saved['parameters'])==26,saved
 assert all(v==p[int(k)] for k,v in saved['parameters'].items()if k!='14')
 editor._config=None;players.restore_config(c)
 assert players.manage(c,'ui712_transfer_player_get',req)['values']['parameters']['14']==81
 assert native.read(c,'113911',122)[0][14]==72
 traits.manage(c,'ui712_transfer_traits_apply',dict(req,skills=[0,5,73],boosters=[31,511,418],foot={'43':1,'42':3,'45':3},positions={'0':12,'1':2}))
 editor._config=None;players.restore_config(c);got=traits.manage(c,'ui712_transfer_traits_get',req)
 assert got['skills']==[0,5,73] and got['boosters']==[31,511,418] and got['foot']=={'43':1,'42':3,'45':3}and got['positions']['0']==12
 traits.manage(c,'ui712_transfer_traits_apply',dict(req,skills=[],boosters=[0,0,0]));assert traits.manage(c,'ui712_transfer_traits_get',req)['skills']==[]
 # Exact IDs: a different card with the same low bits cannot inherit Valverde.
 try:native.read(c,str(113911+2**32),518);raise AssertionError('ID alias accepted')
 except ValueError:pass
 # Owned native parameters take precedence; duplicate serials cannot be guessed.
 import player_editor
 owned=[0]*147;owned[14]=95
 c.execute('INSERT INTO gameplayers VALUES(?,?,?)',(113911,1,json.dumps({'parameters':owned})));c.commit()
 # player_editor.native_parameters decodes wire arrays; compare using same real conversion.
 assert native.read(c,'113911',122)[0]==player_editor.native_parameters(owned)
 c.execute('INSERT INTO gameplayers VALUES(?,?,?)',(113911,2,json.dumps({'parameters':owned})));c.commit();assert native.read(c,'113911',122)[1]=='game73_native_base'
print('PASS NPC actual parameters, named celebrations, freeze all stats only on a changed stat, scoped save/reopen, skills add/remove, boosters, foot/positions, exact IDs, duplicate serial handling. Phone not verified.')
