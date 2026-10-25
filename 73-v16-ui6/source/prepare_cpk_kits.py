from pathlib import Path
import struct,sys,json
sys.path.insert(0,'/workspace/testingdummy/efootxi-1.3.2/player-faces-v24/source');from cpk_extract import utf,decompress
P=Path('/workspace/ronaldo-work/73-ui6');alias={1706:352,4937:242,1957:108,1956:121,4962:120,4964:102,4938:103,1950:119,1228:101,1955:127};files={}
for path in[P/'base-dt200.cpk',P/'original-dt870.cpk']:
 data=path.read_bytes();h=utf(data[16:2048])[0];off=h['TocOffset'];sz=struct.unpack_from('<Q',data,off+8)[0];rows=utf(data[off+16:off+16+sz]);base=min(h['ContentOffset'],off)
 for r in rows:
  name=(r.get('DirName')or'')+'/'+r['FileName'];name=name.lstrip('/')
  if any(name.startswith('common/etc/uniform/team/'+str(tid)+'/')for tid in set(alias.values())|{351,245}):
   at=base+r['FileOffset'];body=decompress(data[at:at+r['FileSize']]);files[name]=(body,path.name)
proof=[];root=P/'cpk-kit-additions'
for target,donor in alias.items():
 source={n:r for n,r in files.items()if n.startswith('common/etc/uniform/team/'+str(donor)+'/')}
 for name,(data,archive)in source.items():
  dest=name.replace('/'+str(donor)+'/', '/'+str(target)+'/').replace('/'+str(donor)+'_','/'+str(target)+'_');p=root/dest;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data);proof.append({'team':target,'donor':donor,'source':name,'destination':dest,'archive':archive,'bytes':len(data)})
 assert any('_DEF_1st' in n for n in source),(target,donor)
(P/'cpk-kits-build.json').write_text(json.dumps(proof,indent=2));print('EXACT_KIT_RECIPES',len(proof),{k:sum(r['team']==k for r in proof)for k in alias})
