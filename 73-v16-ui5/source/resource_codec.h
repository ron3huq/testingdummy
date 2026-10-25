/* Pinned73 resource records. No account or save data. */
typedef struct{uptr id;u32 offset;const char*name;unsigned char original[176],replacement[176];}RawCoach;
static const RawCoach raw_coaches[]={{17606144688129,289872,"Zinedine Zidane",{1,0,0,64,3,16,0,0,0,0,0,0,0,0,0,0,3,0,16,192,7,176,91,58,186,172,14,152,218,146,113,7,227,131,173,227,131,153,227,131,171,227,131,136,32,227,131,158,227,131,171,227,131,134,227,130,163,227,131,141,227,130,185,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,82,46,32,77,97,114,116,195,173,110,101,122,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,231,189,151,228,188,175,230,137,152,194,183,233,169,172,228,184,129,229,134,133,230,150,175,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},{1,0,0,64,3,16,0,0,0,0,0,0,0,0,0,0,3,0,16,192,7,64,91,58,186,172,14,152,90,143,113,7,90,105,110,101,100,105,110,101,32,90,105,100,97,110,101,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,90,105,110,101,100,105,110,101,32,90,105,100,97,110,101,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,90,105,110,101,100,105,110,101,32,90,105,100,97,110,101,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}},{17604802510874,288992,"Sir Alex Ferguson",{26,0,0,240,2,16,0,0,0,0,0,0,0,0,0,0,4,0,96,192,12,92,107,34,181,99,45,123,65,80,206,6,227,130,184,227,130,167,227,131,179,227,131,138,227,131,188,227,131,173,32,227,130,172,227,131,131,227,131,136,227,130,165,227,131,188,227,130,190,0,0,0,0,0,0,0,0,0,71,101,110,110,97,114,111,32,71,97,116,116,117,115,111,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,232,169,185,231,186,179,231,189,151,194,183,229,138,160,229,155,190,231,180,162,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},{26,0,0,240,2,16,0,0,0,0,0,0,0,0,0,0,4,0,96,192,12,160,107,34,181,99,45,123,193,89,206,6,83,105,114,32,65,108,101,120,32,70,101,114,103,117,115,111,110,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,83,105,114,32,65,108,101,120,32,70,101,114,103,117,115,111,110,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,83,105,114,32,65,108,101,120,32,70,101,114,103,117,115,111,110,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}}};
static const unsigned char glyph_layout_1[57]={9,142,142,69,26,112,238,123,14,32,15,222,123,239,189,247,30,37,34,34,34,34,34,34,34,34,34,242,234,206,0,0,0,0,0,36,65,154,153,125,65,0,0,170,65,102,102,108,66,205,204,176,66,0,0,196,65};
static const unsigned char glyph_layout_2[57]={10,2,2,8,26,112,238,123,14,32,15,222,123,239,189,247,30,39,34,34,34,34,34,34,34,34,34,242,234,206,0,0,0,215,163,56,65,154,153,125,65,0,0,170,65,0,0,122,66,205,204,176,66,0,0,196,65};

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
