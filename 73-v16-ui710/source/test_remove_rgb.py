from pathlib import Path
import sys,sqlite3,json,tempfile
T=Path('/tmp/73-ui710/build/payload/work/tools');sys.path.insert(0,str(T));import appearance_choices as a,body_dimensions as body
root=Path(tempfile.mkdtemp(prefix='ui710-rgb-retirement-',dir='/tmp'));body.ROOT=root;c=sqlite3.connect(':memory:');c.execute('CREATE TABLE meta(key TEXT PRIMARY KEY,value TEXT)');old={'106754901843130':{'rgb':'4e5b37','59':0,'60':0},'88044950524330':{'skin':6,'59':42,'60':2}};c.execute('INSERT INTO meta VALUES(?,?)',(a.KEY,json.dumps(old)));c.commit();assert a.retire_custom_rgb(c);a.load(c);assert a.profiles['106754901843130']=={'59':0,'60':0};assert a.profiles['88044950524330']==old['88044950524330'];assert not a.retire_custom_rgb(c)
backup=sqlite3.connect(root/'backups/ui710-before-remove-rgb.sqlite3');assert json.loads(backup.execute('SELECT value FROM meta WHERE key=?',(a.KEY,)).fetchone()[0])==old
try:a.validate({'rgb':'abcdef'});raise AssertionError('RGB still accepted')
except ValueError:pass
for i in range(1,7):a.validate({'skin':i})
assert 'custom_skin'not in (T/'bridge_73.py').read_text();assert 'configure_native(_handle,appearance_choices.profiles)'not in(T/'noodle_hair.py').read_text();assert 'entry=0x39ca65c'not in(T/'noodle_hair.py').read_text()
Path('/tmp/73-ui710/rgb-removal-validation.json').write_text(json.dumps({'passed':True,'six_native_palettes_retained':True,'custom_RGB_rejected':True,'SQL_original_backup_verified':True,'celebrations_and_native_palette_preserved':True,'migration_idempotent':True,'RGB_asset_advertiser_and_native_profile_registration_removed':True,'device_tested':False},indent=2));print('RGB_REMOVAL_PASS')
