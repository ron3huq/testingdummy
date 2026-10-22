from pathlib import Path
import sys,json,sqlite3,tempfile,copy,hashlib
r=Path(__file__).parent;sys.path[:0]=[str(r),str(r.parent/'android/user-gateway/work/tools')]
import myleague_packs as packs,club_store as store,managed_card_pool as managed,gate_logic
source=r.parent/'android/user-gateway/outputs/efootball/local-club.sqlite3';before=hashlib.sha256(source.read_bytes()).hexdigest()
with tempfile.TemporaryDirectory()as d:
 db=Path(d)/'test.sqlite';src=sqlite3.connect('file:'+str(source)+'?mode=ro',uri=True);conn=sqlite3.connect(db);src.backup(conn);src.close()
 raw=json.loads((r.parent/'editor-v18/browser-project.json').read_text());rows=raw['packs'];assert len(rows)==1
 aid=rows[0]['agent_id'];original_players=conn.execute('SELECT count(*) FROM gameplayers').fetchone()[0];original_agents=conn.execute('SELECT count(*) FROM agents').fetchone()[0]
 assert packs.apply(conn,rows)['changed']
 assert conn.execute('SELECT count(*) FROM gameplayers').fetchone()[0]==original_players
 assert conn.execute('SELECT count(*) FROM agents').fetchone()[0]==original_agents+1
 assert sum(managed.counts(conn,aid))==len(rows[0]['player_ids'])
 assert packs.apply(conn,rows)['changed']is False
 # Real gateway list/preview, finite draw, receipt retry and reset paths.
 gate=gate_logic.GateLogic({},conn=conn)
 listing=gate.handle('CMD_GET_MYCLUB_AGENTLIST',{})
 agent=next(p for p in listing['agent_list']if p['agent_id']==aid);assert agent['title']=='My stars'and agent['player_list_total']==2
 assert {str(p['gameplayer_id']['id'])for p in agent['pickup_list']}==set(rows[0]['player_ids'])
 store.set_meta(conn,'coin','10000');conn.commit()
 req={'agent_id':aid,'count':1,'buy_type':'BUY_BY_COIN','user_id':123,'rqid':'studio-test-draw'}
 out=gate.handle('CMD_USE_MYCLUB_AGENT',req)
 assert out.get('result')=='NOERR',out.get('result')
 assert len(out['gameplayer_list'])==1 and str(out['gameplayer_list'][0]['gameplayer']['gameplayer_id']['id'])in rows[0]['player_ids']
 assert sum(managed.counts(conn,aid))==1 and int(store.get_meta(conn,'coin','0'))==99999
 count_after=conn.execute('SELECT count(*) FROM gameplayers').fetchone()[0]
 again=gate.handle('CMD_USE_MYCLUB_AGENT',req)
 assert again['gameplayer_list'][0]['gameplayer']['gameplayer_id']==out['gameplayer_list'][0]['gameplayer']['gameplayer_id']
 assert conn.execute('SELECT count(*) FROM gameplayers').fetchone()[0]==count_after and int(store.get_meta(conn,'coin','0'))==99999
 # Reinstall/rename must preserve remaining pool and owned instances.
 renamed=copy.deepcopy(rows);renamed[0]['title']='My renamed stars';packs.apply(conn,renamed)
 assert sum(managed.counts(conn,aid))==1 and conn.execute('SELECT count(*) FROM gameplayers').fetchone()[0]==count_after
 changed=copy.deepcopy(renamed);changed[0]['player_ids']=changed[0]['player_ids'][:1]
 snapshot=list(conn.iterdump())
 try:packs.apply(conn,changed)
 except ValueError as e:assert 'immutable'in str(e)
 else:raise AssertionError('used pool membership was overwritten')
 assert list(conn.iterdump())==snapshot
 # Whole plan preflight: valid addition + invalid card must not install either.
 bad=copy.deepcopy(rows);bad[0]['agent_id']+=2;bad.append({'agent_id':aid+3,'title':'missing','player_ids':['999999999999']})
 try:packs.apply(conn,bad)
 except ValueError:pass
 else:raise AssertionError('missing registry card accepted')
 assert list(conn.iterdump())==snapshot
 packs.apply(conn,[]);assert aid not in json.loads(store.get_meta(conn,'league_position_agent_ids','[]'))
 assert conn.execute('SELECT enabled FROM managed_agents WHERE agent_id=?',(aid,)).fetchone()[0]==0
 assert conn.execute('SELECT count(*) FROM gameplayers').fetchone()[0]==count_after and sum(managed.counts(conn,aid))==1
 packs.apply(conn,renamed);managed.reset_agent(conn,aid,request={'rqid':'studio-reset'});assert sum(managed.counts(conn,aid))==2
 # The shipped account policy refills coins to99999 after gateway replies.
 # Verify price and retry at the actual transaction boundary independently.
 store.set_meta(conn,'account_resource_fixed','');store.set_meta(conn,'coin','1000');conn.commit()
 rawreq={'user_id':123,'rqid':'raw-cost','buy_type':'BUY_BY_COIN'}
 first=managed.draw_and_grant(conn,aid,1,request=rawreq);assert int(store.get_meta(conn,'coin','0'))==900
 second=managed.draw_and_grant(conn,aid,1,request=rawreq);assert int(store.get_meta(conn,'coin','0'))==900 and first[0]['gameplayer_id']==second[0]['gameplayer_id']
 import myleague_editor_runtime as editor
 editor._config=raw
 assert packs.install()is True and packs.install()is False
 gate.handle('CMD_GET_MYCLUB_AGENTLIST',{})
 assert json.loads((r/'myleague-packs-status.json').read_text())['state']=='READY'
 conn.close()
assert hashlib.sha256(source.read_bytes()).hexdigest()==before
report=dict(status='PACK_NATIVE_GATEWAY_LIST_DRAW_RETRY_RESET_PRESERVATION_PASS',actual_shipped_gateway=True,source_save_unchanged=True,install_does_not_grant_players=True,missing_card_atomic_rollback=True,immutable_published_membership=True,retry_no_duplicate_grant_or_charge=True,rename_preserves_consumed=True,hide_preserves_owned_and_receipts=True,device_tested=False)
(r/'packs-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(report['status'])
