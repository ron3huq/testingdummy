/* Exact-card asset-path replacement. Original player/face IDs are never changed. */
typedef unsigned long uptr;typedef unsigned int u32;typedef unsigned short u16;
typedef struct{const u16*data;int count,cap;} FString;
typedef void(*LoadFn)(void*,const void*);typedef uptr(*PathFn)(void*,const u16*,int);typedef void(*DoneFn)(void*,void*,void*);
#define TARGET 105572980600878UL
static int target_kind(uptr id){return id==105572980600878UL?1:id==105577812455608UL?2:id==105710151126263UL?3:id==105768133207973UL?4:id==105820478135535UL?5:0;}
static LoadFn outer_original,mesh_original;static DoneFn done_original,texture_original;
static PathFn path_original;
static volatile u32 enabled;static volatile uptr stats[24];static unsigned char lock;
static int take(void){return !__atomic_test_and_set(&lock,__ATOMIC_ACQUIRE);}static void drop(void){__atomic_clear(&lock,__ATOMIC_RELEASE);}static void inc(u32 i){__atomic_fetch_add(&stats[i],1,__ATOMIC_RELAXED);}
static uptr tid(void){uptr p;__asm__ volatile("mrs %0,tpidr_el0":"=r"(p));return p;}
typedef struct Scope{int target;void*actor;struct Scope*prev;}Scope;
static struct{uptr tid;Scope*top;} scopes[16];
static int enter(Scope*s,int target){if(!take())return -1;uptr t=tid();int free=-1,slot=-1;for(int i=0;i<16;i++){if(scopes[i].tid==t){slot=i;break;}if(!scopes[i].tid)free=i;}if(slot<0)slot=free;if(slot>=0){s->target=target;s->actor=0;s->prev=scopes[slot].top;scopes[slot].tid=t;scopes[slot].top=s;}drop();return slot;}
static void leave(Scope*s,int slot){if(slot<0)return;while(!take()){}if(scopes[slot].top==s){scopes[slot].top=s->prev;if(!s->prev)scopes[slot].tid=0;}drop();}
static void*active_actor(void){if(!__atomic_load_n(&enabled,__ATOMIC_ACQUIRE)||!take())return 0;uptr t=tid();void*actor=0;for(int i=0;i<16;i++)if(scopes[i].tid==t&&scopes[i].top){if(scopes[i].top->target)actor=scopes[i].top->actor;break;}drop();return actor;}
static int eq(const u16*a,const char*b){if(!a)return 0;for(int i=0;i<160;i++){if(a[i]!=(unsigned char)b[i])return 0;if(!b[i])return 1;}return 0;}
static const char*variants[]={"4522","4522lg00v0000","4522ep01v0291","4522ep00v0313"};
static int face_variant(const u16*a){for(int i=0;i<4;i++)if(eq(a,variants[i]))return i;return -1;}
static int put(u16*out,int at,const char*s){while(*s)out[at++]=(unsigned char)*s++;return at;}
typedef struct{void*actor;u16 face[64];u32 pending,redirected;}Slot;static Slot slots[16];static u16 last_face[64],last_profile[64],last_path[160];
__attribute__((visibility("default"))) void configure_outer(uptr base,uptr p){(void)base;outer_original=(LoadFn)p;}
__attribute__((visibility("default"))) void configure_load(uptr base,uptr p){(void)base;mesh_original=(LoadFn)p;}
__attribute__((visibility("default"))) void configure_done(uptr base,uptr p){(void)base;done_original=(DoneFn)p;}
__attribute__((visibility("default"))) void configure_texture_done(uptr base,uptr p){(void)base;texture_original=(DoneFn)p;}
__attribute__((visibility("default"))) void configure_path(uptr base,uptr p){(void)base;path_original=(PathFn)p;}
__attribute__((visibility("default"))) void noodle_enable(u32 v){__atomic_store_n(&enabled,v==1,__ATOMIC_RELEASE);}
__attribute__((visibility("default"))) uptr noodle_stat(u32 i){return i<24?__atomic_load_n(&stats[i],__ATOMIC_RELAXED):0;}
__attribute__((visibility("default"))) u32 noodle_face_char(u32 i){u32 v=0;if(i<64&&take()){v=last_face[i];drop();}return v;}
__attribute__((visibility("default"))) u32 noodle_profile_char(u32 i){u32 v=0;if(i<64&&take()){v=last_profile[i];drop();}return v;}
__attribute__((visibility("default"))) u32 noodle_path_char(u32 i){u32 v=0;if(i<160&&take()){v=last_path[i];drop();}return v;}
__attribute__((visibility("default"))) void noodle_outer_hook(void*actor,const FString*face){if(!outer_original)return;inc(16);int target=actor&&target_kind(*(const uptr*)((char*)actor+0x10b0));Scope scope;int at=enter(&scope,target);if(at>=0)scope.actor=actor;outer_original(actor,face);leave(&scope,at);}
/* FSoftObjectPath::SetPath receives UTF-16 + length. The lower mesh loader
 * receives FName + subpath FString (24 bytes), NEVER an FString (16 bytes).
 * Let Unreal intern and own the new path; never fabricate or read an FName. */
__attribute__((visibility("default"))) uptr noodle_path_hook(void*out,const u16*path,int length){
 if(!path_original)return 0;void*actor=active_actor();if(!actor)return path_original(out,path,length);inc(18);
 if(!path||length<1||length>=160)return path_original(out,path,length);
 if(take()){for(int i=0;i<160;i++)last_path[i]=i<length?path[i]:0;stats[21]=*(const u32*)((char*)actor+0x10a8);drop();}
 int kind=-1,quoted=0,at=0,n=length;
 if(path[n-1]==0)n--;
 const char*base="/Game/Assets/character/RealFace/";
 const char*meshclass="SkeletalMesh'";const char*texclass="Texture2D'";
 int z=0;while(meshclass[z]&&z<n&&path[z]==(unsigned char)meshclass[z])z++;
 if(!meshclass[z]){at=z;kind=0;quoted=1;}else{z=0;while(texclass[z]&&z<n&&path[z]==(unsigned char)texclass[z])z++;if(!texclass[z]){at=z;kind=2;quoted=1;}}
 for(z=0;base[z];z++)if(at+z>=n||path[at+z]!=(unsigned char)base[z])return path_original(out,path,length);at+=z;
 if(at+3>=n)return path_original(out,path,length);
 if(path[at]=='S'&&path[at+1]=='K'&&path[at+2]=='_'){if(kind==2)return path_original(out,path,length);kind=quoted?0:1;at+=3;}
 else if(path[at]=='T'&&path[at+1]=='_'){if(kind==0)return path_original(out,path,length);kind=quoted?2:3;at+=2;}
 else return path_original(out,path,length);
 u16 original[64];int keylen=0;
 if(path[at]<'0'||path[at]>'9')return path_original(out,path,length);
 while(at<n&&path[at]!='_'&&keylen<50){u16 ch=path[at++];if(!((ch>='0'&&ch<='9')||(ch>='a'&&ch<='z')||(ch>='A'&&ch<='Z')))return path_original(out,path,length);original[keylen++]=ch;}
 original[keylen]=0;if(!keylen||at>=n)return path_original(out,path,length);
 const char*texsuffix="_Face_D";const char*texmiddle="_Face_D.T_";
 if(kind>=2){const char*candidates[2]={"_Face_N.T_","_Face_SRO.T_"};for(int ci=0;ci<2;ci++){int ok=1;for(int j=0;candidates[ci][j];j++){if(at+j>=n||path[at+j]!=(unsigned char)candidates[ci][j]){ok=0;break;}}if(ok){texsuffix=ci==0?"_Face_N":"_Face_SRO";texmiddle=candidates[ci];break;}}}
 u16 expected[160];int e=0;
 if(kind==0)e=put(expected,e,"SkeletalMesh'");if(kind==2)e=put(expected,e,"Texture2D'");e=put(expected,e,base);e=put(expected,e,kind<2?"SK_":"T_");for(int j=0;j<keylen;j++)expected[e++]=original[j];e=put(expected,e,kind<2?"_Face.SK_":texmiddle);for(int j=0;j<keylen;j++)expected[e++]=original[j];e=put(expected,e,kind<2?"_Face":texsuffix);if(quoted)e=put(expected,e,"'");
 if(e!=n)return path_original(out,path,length);for(int j=0;j<n;j++)if(expected[j]!=path[j])return path_original(out,path,length);
 int variant=target_kind(*(const uptr*)((char*)actor+0x10b0));if(!variant)return path_original(out,path,length);

 if(kind<2){
  if(!take()){inc(6);return path_original(out,path,length);}Slot*slot=0;
  for(int i=0;i<16;i++)if(slots[i].actor==actor){slot=&slots[i];break;}
  if(!slot)for(int i=0;i<16;i++)if(!slots[i].pending){slot=&slots[i];break;}
  if(!slot){drop();inc(6);return path_original(out,path,length);}
  slot->actor=actor;slot->pending=1;slot->redirected=1;for(int i=0;i<64;i++)slot->face[i]=last_face[i]=0;for(int j=0;j<=keylen;j++){slot->face[j]=original[j];last_face[j]=original[j];}drop();inc(2);inc(19);
 }else{inc(17);inc(20);}
 u16 replaced[160];int rn=0;const char*priv=variant==1?"ND01":variant==2?"ND02":variant==3?"ND03":variant==4?"ND04":variant==5?"ND05":"ND01";
 if(kind==0)rn=put(replaced,rn,"SkeletalMesh'");if(kind==2)rn=put(replaced,rn,"Texture2D'");rn=put(replaced,rn,base);rn=put(replaced,rn,kind<2?"SK_":"T_");rn=put(replaced,rn,priv);rn=put(replaced,rn,kind<2?"_Face.SK_":texmiddle);rn=put(replaced,rn,priv);rn=put(replaced,rn,kind<2?"_Face":texsuffix);if(quoted)rn=put(replaced,rn,"'");replaced[rn]=0;
 return path_original(out,replaced,rn+(length>n));
}
static void restore(void*actor,const u16*face){if(!outer_original)return;int n=0;while(n<63&&face[n])n++;if(!n)return;FString f={face,n+1,n+1};Scope scope;int at=enter(&scope,0);if(at<0){inc(6);return;}inc(8);outer_original(actor,&f);leave(&scope,at);}
/* Observe only. Its second argument is an opaque native FSoftObjectPath. */
__attribute__((visibility("default"))) void noodle_load_hook(void*actor,const void*path){inc(0);if(!mesh_original)return;uptr id=actor?*(const uptr*)((char*)actor+0x10b0):0;if(target_kind(id)){inc(1);__atomic_store_n(&stats[10],id,__ATOMIC_RELAXED);}mesh_original(actor,path);}
__attribute__((visibility("default"))) void noodle_done_hook(void*closure,void*result,void*detail){
 if(!done_original)return;void*actor=closure?*(void**)closure:0;u16 face[64];int pending=0;
 if(actor&&target_kind(*(const uptr*)((char*)actor+0x10b0))&&take()){for(int i=0;i<16;i++)if(slots[i].actor==actor&&slots[i].pending){pending=1;for(int j=0;j<64;j++)face[j]=slots[i].face[j];slots[i].pending=0;break;}
  const FString*profile=(const FString*)((char*)actor+0x448);if(profile->data&&profile->count>=1&&profile->count<=64&&profile->cap>=profile->count&&profile->data[profile->count-1]==0){for(int j=0;j<64;j++)last_profile[j]=j<profile->count?profile->data[j]:0;inc(12);}drop();}
 int nonnull=result&&*(void**)result;int fallback=pending&&(!nonnull||!__atomic_load_n(&enabled,__ATOMIC_ACQUIRE));if(pending){if(nonnull)inc(3);else inc(4);}Scope completion_scope;int completion_at=enter(&completion_scope,actor&&target_kind(*(const uptr*)((char*)actor+0x10b0)));if(completion_at>=0)completion_scope.actor=actor;done_original(closure,result,detail);leave(&completion_scope,completion_at);if(fallback)restore(actor,face);
}
__attribute__((visibility("default"))) void noodle_texture_done_hook(void*closure,void*result,void*detail){if(!texture_original)return;void*actor=closure?*(void**)closure:0;if(actor&&target_kind(*(const uptr*)((char*)actor+0x10b0))){inc(13);if(result&&*(void**)result)inc(14);else inc(15);}Scope texture_scope;int texture_at=enter(&texture_scope,actor&&target_kind(*(const uptr*)((char*)actor+0x10b0)));if(texture_at>=0)texture_scope.actor=actor;texture_original(closure,result,detail);leave(&texture_scope,texture_at);}
__attribute__((visibility("default"))) void flush(void*start,uptr n){uptr ctr;__asm__ volatile("mrs %0,ctr_el0":"=r"(ctr));uptr ds=4ul<<((ctr>>16)&15),is=4ul<<(ctr&15),end=(uptr)start+n;for(uptr p=(uptr)start&~(ds-1);p<end;p+=ds)__asm__ volatile("dc cvau,%0"::"r"(p):"memory");__asm__ volatile("dsb ish":::"memory");for(uptr p=(uptr)start&~(is-1);p<end;p+=is)__asm__ volatile("ic ivau,%0"::"r"(p):"memory");__asm__ volatile("dsb ish;isb":::"memory");}
__attribute__((visibility("default"))) void store_instruction(void*p,u32 v){__atomic_store_n((u32*)p,v,__ATOMIC_RELEASE);}
