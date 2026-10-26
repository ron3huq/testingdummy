from pathlib import Path
import shutil,json,struct,zlib
P=Path('/workspace/ronaldo-work/73-ui76');O=P.with_name('73-ui75')
for n in ['smali','java','stubs-out','native','payload']:shutil.copytree(O/n,P/n,dirs_exist_ok=True)
p=P/'native/select_team.c';s=p.read_text().replace('(d[0x3fd]&4u)','(tid==4937?4u:(d[0x3fd]&4u))').replace('static u32 appearance_mode(unsigned long long id){','static u32 appearance_mode(unsigned long long id){\n if(id==89138556572074ULL)return 1;')
a=s.index('static u32 model_begin(')
s=s[:a]+'''static void model_floats(void*spec,uptr id){static const unsigned char offsets[11]={0x20,0x14,8,0x18,0xc,0x10,0x30,0x28,0x1c,0x24,0x2c};if(!spec||!model_ready)return;for(u32 i=0;i<model_count;i++)if(model_rows[i].id==id){for(u32 k=0;k<11;k++)if(model_rows[i].fields[k]<15)*(float*)((unsigned char*)spec+0x10+offsets[k])=(float)model_rows[i].fields[k]/7.0f-1.0f;return;}}\n'''+s[a:]
s=s.replace(' model_end(model_token);',' model_end(model_token);\n model_floats((void*)spec,id);');p.write_text(s)
# Latest source appearance table, including custom cards.
ns={};src=Path('/workspace/testingdummy/efootxi-1.3.2/player-faces-v18/source/prepare_country_sources.py').read_text();exec('import struct,zlib\n'+src[src.index('def unpack'):src.index('out=Path')],ns)
b=ns['unpack'](Path('/workspace/ronaldo-work/73-ui6/original-cpk/common/etc/appearance/PlayerAppearance.bin').read_bytes());assert len(b)%64==0
rows={str(struct.unpack_from('<Q',b,i)[0]):b[i+8:i+15].hex()for i in range(0,len(b),64)}
(P/'payload/work/tools/player_model_baselines.json.gz').write_bytes(zlib.compress(json.dumps(rows,separators=(',',':')).encode()))
p=P/'payload/work/tools/player_model.py';s=p.read_text().replace('import json,threading,functools,ctypes as C','import json,threading,functools,ctypes as C,zlib\nfrom pathlib import Path\n@functools.lru_cache(maxsize=1)\ndef baseline_rows():return json.loads(zlib.decompress(Path(__file__).with_name("player_model_baselines.json.gz").read_bytes()))\ndef baseline(pid):\n rows=baseline_rows();raw=rows.get(pid)or rows.get(str(int(pid)&262143))\n if raw is None:return {}\n b=bytes.fromhex(raw);nibbles=[7,3,0,4,1,2,10,8,5,6,9]\n return {key:((b[n//2]>>((n%2)*4))&15)for key,n in zip(FIELDS,nibbles)}')
s=s.replace("'values':profiles.get(pid,{}),'fields'", "'values':profiles.get(pid,{}),'baseline':baseline(pid),'fields'");p.write_text(s)
p=P/'java/org/efootballrevival/runtimeprobe/PlayerModelEditor.java';s=p.read_text().replace('form(a,player,data.optJSONObject("values"))','form(a,player,data)').replace('JSONObject values){ScrollView','JSONObject data){JSONObject values=data.optJSONObject("values"),base=data.optJSONObject("baseline");ScrollView').replace('int value=custom?values.optInt(KEYS[i],7):7;', 'final String original=base!=null&&base.has(KEYS[i])?(base.optInt(KEYS[i])==15?"default":String.valueOf(base.optInt(KEYS[i]))):"unavailable";int value=custom?values.optInt(KEYS[i],7):base==null?7:Math.min(14,base.optInt(KEYS[i],7));').replace('" · Original"','" · Original: "+original');p.write_text(s)
p=P/'smali/org/efootballrevival/runtimeprobe/UiStringsData.smali';p.write_text(p.read_text().replace('UI7.5','UI7.6'))
print('BASELINES',len(rows))
