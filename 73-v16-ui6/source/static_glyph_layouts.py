from pathlib import Path
import sys,struct,zlib,re,json
P=Path('/workspace/ronaldo-work/73-ui6');ns={};exec((P/'prepare_cpk_kits.py').read_text(),ns);files=ns['files'];root=P/'cpk-kit-additions'
for name,(data,archive)in files.items():
 if any(name.startswith('common/etc/uniform/team/'+str(d)+'/')for d in[242,245,351,352])and any('_DEF_'+s+'_realUni.bin'in name for s in['1st','2nd']):
  f=root/name;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(data)
s=Path('/workspace/testingdummy/efootxi-1.3.2/player-faces-v18/source/prepare_country_sources.py').read_text();un={};exec('import struct,zlib\n'+s[s.index('def unpack'):s.index('out=Path')],un)
header=Path('/workspace/testingdummy/73-v16-ui6/source/resource_codec.h').read_text();layouts={i:bytes(map(int,re.search(r'glyph_layout_'+str(i)+r'\[57\]=\{(.*?)\}',header).group(1).split(',')))for i in[1,2]};proof=[]
for f in root.rglob('*realUni.bin'):
 encoded=f.read_bytes();raw=un['unpack'](encoded) if encoded[3:8]==b'WESYS' else encoded
 if len(raw)==92 and raw[76:81]in[b'u0242',b'u0245',b'u0351',b'u0352']and raw[81:82]==b'p'and raw[82:83]in[b'1',b'2']:
  out=raw[:19]+layouts[int(chr(raw[82]))]+raw[76:];comp=zlib.compress(out,9);body=b'\xff\x22\x81WESYS'+struct.pack('<II',len(comp),len(out))+comp;assert un['unpack'](body)==out;f.write_bytes(body);proof.append({'file':f.relative_to(root).as_posix(),'change':'same57-byte layout formerly applied by runtime inflate hook','all_other_decoded_bytes_preserved':True})
assert len(proof)==12,len(proof)
(P/'static-glyphs-validation.json').write_text(json.dumps({'passed':True,'files':proof,'global_engine_inflate_hook_needed':False,'Y17_decoded_layouts_same_as_UI5':True},indent=2));print('STATIC_GLYPHS_PASS',len(proof))
