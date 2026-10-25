from pathlib import Path
import json,struct
P=Path('/workspace/ronaldo-work/73-ui4');S=Path('/workspace/testingdummy/73-v16-ui4/source');raw=(P/'Coach-decoded.bin').read_bytes();countries=json.loads((P/'coach-countries.json').read_text());rules=[]
for cid,name,country,age in [(17606144688129,'Zinedine Zidane','France',45),(17604802510874,'Sir Alex Ferguson','Scotland',66)]:
 at=raw.find(struct.pack('<Q',cid));assert at>=0 and at%176==0;old=raw[at:at+176];new=bytearray(old);meta=int.from_bytes(old[16:32],'little');nation=countries[country][0];meta=(meta&~(511<<42))|(nation<<42);meta=(meta&~(63<<103))|((age-15)<<103);new[16:32]=meta.to_bytes(16,'little')
 for off in[32,78,124]:new[off:off+46]=name.encode().ljust(46,b'\0')
 rules.append(dict(id=cid,name=name,age=age,country=country,country_internal=nation,country_flag=countries[country][1],offset=at,old=old.hex(),new=bytes(new).hex()))
(P/'coach-rules.json').write_text(json.dumps(rules,indent=2));parts=['/* Pinned73 resource records. No account or save data. */\n']
parts.append('typedef struct{uptr id;u32 offset;const char*name;unsigned char original[176],replacement[176];}RawCoach;\nstatic const RawCoach raw_coaches[]={'+','.join('{%d,%d,"%s",{%s},{%s}}'%(r['id'],r['offset'],r['name'],','.join(str(v)for v in bytes.fromhex(r['old'])),','.join(str(v)for v in bytes.fromhex(r['new'])))for r in rules)+'};\n')
# Coherent name/number layout from the native licensed MU template. Body textures
# and kit namespace remain those requested; glyph atlases are cloned separately.
s=Path('/workspace/testingdummy/efootxi-1.3.2/player-faces-v18/source/prepare_country_sources.py').read_text();ns={};exec('import struct,zlib\n'+s[s.index('def unpack'):s.index('out=Path')],ns)
for slot,part in [(1,'1st'),(2,'2nd')]:
 f=Path('/workspace/ronaldo-work/73-ui2/tables870/common/etc/uniform/team/100')/('100_DEF_'+part+'_realUni.bin');b=ns['unpack'](f.read_bytes());assert len(b)==92 and b[76:83]==('u0100p'+str(slot)).encode();parts.append('static const unsigned char glyph_layout_%d[57]={%s};\n'%(slot,','.join(str(v)for v in b[19:76])))
parts.append(r'''
static int byte_equal(const unsigned char*a,const unsigned char*b,u32 n){for(u32 i=0;i<n;i++)if(a[i]!=b[i])return 0;return 1;}
static void byte_copy(unsigned char*a,const unsigned char*b,u32 n){for(u32 i=0;i<n;i++)a[i]=b[i];}
static volatile u32 codec_uniform_patches,codec_coach_patches,codec_native_coaches;
__attribute__((visibility("default"))) u32 patch_decoded(void*data,uptr size){
 if(!data)return 0;unsigned char*b=data;u32 changed=0;
 if(size==92&&b[76]=='u'&&b[81]=='p'&&(b[82]=='1'||b[82]=='2')&&b[83]==0){
  u32 team=0;for(u32 i=77;i<81;i++){if(b[i]<'0'||b[i]>'9')return 0;team=team*10+b[i]-'0';}
  if(team==242||team==245||team==351||team==352){byte_copy(b+19,b[82]=='1'?glyph_layout_1:glyph_layout_2,57);codec_uniform_patches++;return 1;}
 }
 if(size==292336){
  for(u32 i=0;i<2;i++){const RawCoach*r=&raw_coaches[i];if(r->offset+176>size)continue;
   if(byte_equal(b+r->offset,r->original,176)){byte_copy(b+r->offset,r->replacement,176);changed++;codec_coach_patches++;}
  }
 }
 return changed;
}
/* z_stream64 field offsets are confirmed by original6917eb0 accesses.
   Track a complete contiguous destination before inspecting decompressed bytes;
   incremental PNG rows/other streaming buffers are never dereferenced backwards. */
typedef struct{uptr stream,start,capacity;}InflateDestination;
static InflateDestination inflate_dest[32];static volatile unsigned char inflate_lock;
static int(*original_raw_inflate)(void*,int);
__attribute__((visibility("default"))) void configure_raw_inflate(uptr base,uptr trampoline){engine_base=base;original_raw_inflate=(void*)trampoline;}
__attribute__((visibility("default"))) int raw_inflate_hook(void*stream,int flush){
 if(!stream)return original_raw_inflate(stream,flush);
 unsigned char*p=stream;uptr begin=*(uptr*)(p+24),total=*(uptr*)(p+40);u32 capacity=*(u32*)(p+32);int slot=-1;
 if(!total&&begin&&capacity){
  while(__atomic_test_and_set(&inflate_lock,__ATOMIC_ACQUIRE)){}
  for(unsigned i=0;i<32;i++)if(inflate_dest[i].stream==(uptr)stream){slot=i;break;}
  if(slot<0)for(unsigned i=0;i<32;i++)if(!inflate_dest[i].stream){slot=i;break;}
  if(slot>=0)inflate_dest[slot]=(InflateDestination){(uptr)stream,begin,capacity};
  __atomic_clear(&inflate_lock,__ATOMIC_RELEASE);
 }
 int result=original_raw_inflate(stream,flush);
 if(result!=0){
  InflateDestination d={0};while(__atomic_test_and_set(&inflate_lock,__ATOMIC_ACQUIRE)){}
  for(unsigned i=0;i<32;i++)if(inflate_dest[i].stream==(uptr)stream){d=inflate_dest[i];inflate_dest[i].stream=0;break;}
  __atomic_clear(&inflate_lock,__ATOMIC_RELEASE);
  total=*(uptr*)(p+40);
  if(result==1&&d.start&&total<=d.capacity&&*(uptr*)(p+24)==d.start+total)patch_decoded((void*)d.start,total);
 }
 return result;
}
/* Late-loaded Coach DB views: identity is decoded by the original getter.
   Raw metadata is replaced only after an exact source-byte match in this record. */
static void*(*original_coach_lookup)(void*,uptr,uptr);
static void*(*original_cached_coach)(void*,void*);
static void*patch_coach_record(void*record){
 if(!record||!engine_base)return record;
 PlayerKey(*key_fn)(void*)=(void*)(engine_base+0x68f89ec);PlayerKey key=key_fn(record);const RawCoach*r=0;
 for(unsigned i=0;i<2;i++)if(raw_coaches[i].id==key.id){r=&raw_coaches[i];break;}
 if(!r)return record;unsigned char*p=record;unsigned n=0;while(r->name[n]&&n<45){p[0x20+n]=r->name[n];n++;}for(;n<48;n++)p[0x20+n]=0;
 int match=-1;for(unsigned i=0;i+12<=0x170;i++)if(byte_equal(p+i,r->original+20,12)){if(match>=0)return record;match=i;}
 if(match>=0)byte_copy(p+match,r->replacement+20,12);
 codec_native_coaches++;return record;
}
__attribute__((visibility("default"))) void configure_coach_lookup(uptr base,uptr trampoline){engine_base=base;original_coach_lookup=(void*)trampoline;}
__attribute__((visibility("default"))) void*coach_lookup_hook(void*db,uptr kind,uptr id){return patch_coach_record(original_coach_lookup(db,kind,id));}
__attribute__((visibility("default"))) void configure_cached_coach(uptr base,uptr trampoline){engine_base=base;original_cached_coach=(void*)trampoline;}
__attribute__((visibility("default"))) void*cached_coach_hook(void*root,void*key){return patch_coach_record(original_cached_coach(root,key));}
__attribute__((visibility("default"))) u32 codec_status(u32 n){return n==0?codec_uniform_patches:n==1?codec_coach_patches:n==2?codec_native_coaches:0;}
''')
(S/'resource_codec.h').write_text(''.join(parts));print('CODEC_RULES_READY')
