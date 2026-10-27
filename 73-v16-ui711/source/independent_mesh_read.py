from pathlib import Path
import subprocess,sys,json
P=Path('/tmp/73-ui711');R=P/'native-reader';O=P/'independent-fixed-export';L=P/'independent-fixed-logs';L.mkdir(exist_ok=True)
for f in(P/'fixed-faces/livedata').glob('*'):
 dest=R/f.name
 if dest.is_symlink():dest.unlink()
 dest.symlink_to(f)
rows=[]
for tag in ['NCA1','NCA2','NCA3','NCA4','NCA5']:
 for suffix in ['','ep00v0313','ep01v0291','lg00v0000']:
  name='SK_'+tag+suffix+'_Face';r=subprocess.run(['/workspace/ronaldo-work/UEViewer/umodel','-export','-game=ue4.26','-android','-noanim','-aes=0x4552d45005dfe94964893f4925ec747d3d591401e060ed8b3d58be5721c81295','-path='+str(R),'-out='+str(O),name],stdout=subprocess.PIPE,stderr=subprocess.STDOUT);log=r.stdout.decode(errors='replace');(L/(name+'.log')).write_text(log);assert r.returncode==0,(name,log[-2000:]);assert log.count('cooked_out=0 inlined=1')==2,(name,log[-2000:]);rows.append(name)
(P/'independent-mesh-validation.json').write_text(json.dumps({'passed':True,'reader':'independent UEViewer4.26 Android','variants':rows,'each_has_two_real_inline_LODs':True,'device_replay_tested':False},indent=2));print('INDEPENDENT_20_MESHES_PASS')
