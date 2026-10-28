from cut_body import *
P=Path('/workspace/73-ui712');t=Toc(str(P/'cut-bodies/livedata/pc9312_mobile_and.utoc'));logs=P/'cut-reader-logs';logs.mkdir(exist_ok=True)
def verify(path):
 name=Path(path).stem;r=subprocess.run(['/workspace/ronaldo-work/UEViewer/umodel','-testexport','-game=ue4.26','-android','-noanim','-aes=0x4552d45005dfe94964893f4925ec747d3d591401e060ed8b3d58be5721c81295','-path='+str(root),'-out=/tmp/ui712-cut-export',name],stdout=subprocess.PIPE,stderr=subprocess.STDOUT);text=r.stdout.decode();(logs/(name+'.log')).write_text(text);assert r.returncode==0 and'Exported 1/1'in text and'*** ERROR'not in text,(name,text[-500:]);raw=t.read(t.files[path]);proof=[]
 for l in [0,1]:
  m=Body(raw,text,l);r=m.r;a=r['ACTIVE_BEGIN'];assert struct.unpack_from('<I',raw,a)[0]==166;assert list(struct.unpack_from('<166H',raw,a+4))==list(range(166));a=m.begin+10;assert struct.unpack_from('<I',raw,a)[0]==166;assert list(struct.unpack_from('<166H',raw,a+4))==list(range(166));assert all(sum(x.values())==255 for x in m.rows);proof.append({'LOD':l,'vertices':len(m.positions),'triangles':len(m.tri),'full_active_required':166})
 original='Body/SK_'+str(int(name[3:7])-6000).zfill(3)+name[7:]+'.uasset';source=base.read(base.files[original]);assert m.ref==Body(source,reader(Path(original).stem),1).ref
 return {'name':name,'LODs':proof,'native_reference_pose_exact':True}
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:rows=list(pool.map(verify,t.files))
(P/'cut-independent-validation.json').write_text(json.dumps({'passed':True,'models':len(rows),'LODs':len(rows)*2,'all_original_bind_poses_preserved':True,'variants':rows,'Android_tested':False},indent=2));print('CUT_INDEPENDENT_PASS',len(rows))
