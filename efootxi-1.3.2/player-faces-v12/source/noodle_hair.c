/* Exact-card asset-path replacement. Original player/face IDs are never changed. */
typedef unsigned long uptr;typedef unsigned int u32;typedef unsigned short u16;
typedef struct{const u16*data;int count,cap;} FString;
typedef void(*LoadFn)(void*,const void*);typedef uptr(*PathFn)(void*,const u16*,int);typedef void(*DoneFn)(void*,void*,void*);
#define TARGET 88044950524330UL
#define TARGET_2006 89135066911146UL
static int target_card(uptr id){return id==TARGET || id==TARGET_2006 || id==106781745353130UL || id==106734785925546UL || id==105765448873424UL || id==88045755960841UL || id==88038776539586UL || id==105643042189511UL || id==106728863696709UL || id==105848932271764UL || id==105874433662542UL || id==88033139360669UL || id==88045755960841UL || id==105848932271764UL;}
static LoadFn outer_original,mesh_original;static DoneFn done_original,texture_original;
static PathFn path_original;
static volatile u32 enabled;static volatile uptr stats[48];static unsigned char lock;
static int take(void){return !__atomic_test_and_set(&lock,__ATOMIC_ACQUIRE);}static void drop(void){__atomic_clear(&lock,__ATOMIC_RELEASE);}static void inc(u32 i){__atomic_fetch_add(&stats[i],1,__ATOMIC_RELAXED);}
static uptr tid(void){uptr p;__asm__ volatile("mrs %0,tpidr_el0":"=r"(p));return p;}
typedef struct Scope{int target;void*actor;u16 face[64];struct Scope*prev;}Scope;
static struct{uptr tid;Scope*top;} scopes[16];
static int enter(Scope*s,int target){if(!take())return -1;uptr t=tid();int free=-1,slot=-1;for(int i=0;i<16;i++){if(scopes[i].tid==t){slot=i;break;}if(!scopes[i].tid)free=i;}if(slot<0)slot=free;if(slot>=0){s->target=target;s->actor=0;s->face[0]=0;s->prev=scopes[slot].top;scopes[slot].tid=t;scopes[slot].top=s;}drop();return slot;}
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
__attribute__((visibility("default"))) uptr noodle_stat(u32 i){return i<48?__atomic_load_n(&stats[i],__ATOMIC_RELAXED):0;}
__attribute__((visibility("default"))) u32 noodle_face_char(u32 i){u32 v=0;if(i<64&&take()){v=last_face[i];drop();}return v;}
__attribute__((visibility("default"))) u32 noodle_profile_char(u32 i){u32 v=0;if(i<64&&take()){v=last_profile[i];drop();}return v;}
__attribute__((visibility("default"))) u32 noodle_path_char(u32 i){u32 v=0;if(i<160&&take()){v=last_path[i];drop();}return v;}

typedef void(*BakeFn)(void*);typedef void(*FaceSetFn)(void*,void*);
static BakeFn bake_original;static FaceSetFn face_set;static uptr engine_base;
typedef void(*NameFn)(uptr*,const char*,u32);typedef void*(*GetTexFn)(void*,uptr);
static const char*profile_for(uptr id);
static int protected_card(uptr id){return id==TARGET || id==106734785925546UL || id==105765448873424UL || id==105643042189511UL;}
typedef struct{void*actor;uptr id;void*texture;void*mesh;void*material;int expected;}TexOwner;
static TexOwner texowners[32];static u32 tex_cursor;
static TexOwner*owner(void*actor,uptr id,int create){TexOwner*empty=0;for(int i=0;i<32;i++){if(texowners[i].actor==actor){if(texowners[i].id!=id){texowners[i].id=id;texowners[i].texture=0;texowners[i].mesh=0;texowners[i].expected=0;}return &texowners[i];}if(!texowners[i].actor&&!empty)empty=&texowners[i];}if(create){if(!empty)empty=&texowners[(tex_cursor++)%32];empty->texture=0;empty->mesh=0;empty->expected=0;empty->actor=actor;empty->id=id;return empty;}return 0;}
static void expect_texture(void*actor,int reset){uptr id=*(uptr*)((char*)actor+0x10b0);if(!protected_card(id)||!take())return;TexOwner*t=owner(actor,id,1);if(t){t->expected=!reset;if(reset){t->texture=0;t->mesh=0;}}drop();}
static void observe_texture(void*actor,void*result){if(!actor)return;uptr id=*(uptr*)((char*)actor+0x10b0);if(!protected_card(id)||!take())return;TexOwner*t=owner(actor,id,0);void*p=result?*(void**)result:0;if(t&&t->expected){t->expected=0;t->mesh=0;t->texture=p&&*(void**)((char*)actor+0x1a40)==p?p:0;if(t->texture)inc(25);}drop();}
__attribute__((visibility("default"))) void configure_bake(uptr base,uptr p){engine_base=base;bake_original=(BakeFn)p;face_set=(FaceSetFn)(base+0x39c728c);}
static void apply_body_skin(void*actor){if(!actor||!__atomic_load_n(&enabled,__ATOMIC_ACQUIRE))return;uptr id=*(uptr*)((char*)actor+0x10b0);if(id!=88045755960841UL&&id!=105848932271764UL&&id!=88033139360669UL)return;u32*skin=(u32*)((char*)actor+0x42c);if(*skin!=6){*skin=6;*(unsigned char*)((char*)actor+0x1a6b)=1;inc(33);}stats[34]=id;stats[35]=*skin;}
/* USkeletalMesh.Materials offset 0xd8 and FSkeletalMaterial stride 0x28
 * verified from UHT property/struct metadata, not guessed scanning. */
static void capture_mesh_texture(void*actor,void*mesh){
 if(!actor||!mesh||!bake_original)return;uptr id=*(uptr*)((char*)actor+0x10b0);if(!protected_card(id))return;inc(28);
 void*cls=*(void**)((char*)mesh+0x10);if(!cls){inc(36);return;}typedef void*(*ClassFn)(void);void*type=((ClassFn)(engine_base+0x63233e8))();int ix=*(int*)((char*)type+0x38),max=*(int*)((char*)cls+0x38);void**supers=*(void***)((char*)cls+0x30);if(ix<0||ix>max||!supers||supers[ix]!=(char*)type+0x30){inc(36);return;}
 void**materials=*(void***)((char*)mesh+0xd8);int n=*(int*)((char*)mesh+0xe0),cap=*(int*)((char*)mesh+0xe4);if(!materials||n<1||n>32||cap<n){inc(31);return;}
 void*material=materials[0];if(!material){inc(31);return;}
 NameFn intern=(NameFn)(engine_base+0x4414bec);GetTexFn get=(GetTexFn)(engine_base+0x59b8a2c);uptr key=0;intern(&key,"faceBaseColor",1);void*texture=get(material,key);
 if(!texture){intern(&key,"BaseColorMap",1);texture=get(material,key);}if(!texture){inc(30);return;}
 const char*profile=profile_for(id);char name[96];int at=0;name[at++]='T';name[at++]='_';for(const char*p=profile;*p;p++)name[at++]=*p;
 const char*suffixes[]={"","lg00v0000","ep01v0291","ep00v0313"};int count=(id==TARGET||id==106734785925546UL)?4:1;int match=0;
 for(int i=0;i<count;i++){int pos=at;const char*suf=count==1?"ep00v0313":suffixes[i];for(;*suf;suf++)name[pos++]=*suf;const char*end="_Face_D";for(;*end;end++)name[pos++]=*end;name[pos]=0;uptr expected=0;intern(&expected,name,1);if(*(uptr*)((char*)texture+0x18)==expected){match=1;break;}}
 if(!match){inc(29);return;}if(!take()){inc(6);return;}TexOwner*t=owner(actor,id,1);if(t){t->texture=texture;t->mesh=mesh;t->material=material;t->expected=0;inc(32);}drop();
}
/* Native mesh setter 0x39c6b18 uses *actor[0x1a70], or actor[0x228]
 * in the alternate path. Accept ONLY a component holding our confirmed mesh.
 * GetMaterial/SetMaterial vtable slots 0x588/0x590 are proven by UE exec
 * 0x62f86c4 / 0x62f85c8. SetMaterial performs normal render-state updates;
 * never mutate a shared MIC or raw OverrideMaterials array. */
static int bind_head_material(void*actor,void*mesh,void*material){
 if(!mesh||!material)return 0;
 void**ref=*(void***)((char*)actor+0x1a70);
 void*components[2]={ref?*ref:0,*(void**)((char*)actor+0x228)};int matched=0;
 for(int i=0;i<2;i++){
  void*c=components[i];if(!c||(i&&c==components[0]))continue;
  if(*(void**)((char*)c+0x468)!=mesh)continue;
  void**v=*(void***)c;if(!v||!v[0x588/8]||!v[0x590/8])continue;
  typedef void*(*GetMatFn)(void*,int);typedef void(*SetMatFn)(void*,int,void*);
  GetMatFn get=(GetMatFn)v[0x588/8];SetMatFn set=(SetMatFn)v[0x590/8];matched=1;
  inc(37);
  if(get(c,0)!=material){set(c,0,material);inc(38);}
  if(get(c,0)==material)inc(39);else inc(40);
 }
 if(!matched)inc(41);return matched;
}
__attribute__((visibility("default"))) void noodle_bake_hook(void*actor){if(!bake_original)return;apply_body_skin(actor);bake_original(actor);inc(24);if(!actor||!__atomic_load_n(&enabled,__ATOMIC_ACQUIRE))return;uptr id=*(uptr*)((char*)actor+0x10b0);if(!protected_card(id)||!take())return;TexOwner*t=owner(actor,id,0);void*p=t?t->texture:0;void*mesh=t?t->mesh:0;void*material=t?t->material:0;int yes=p&&(t->mesh||p==*(void**)((char*)actor+0x1a40))&&*(void**)((char*)actor+(*(unsigned char*)((char*)actor+0x1a5d)?0x1ab8:0x1aa0));drop();if(bind_head_material(actor,mesh,material))return;if(!t)inc(42);else if(!p)inc(43);else if(!yes)inc(44);if(yes&&face_set){face_set(actor,p);inc(26);}else inc(27);}
__attribute__((visibility("default"))) void noodle_outer_hook(void*actor,const FString*face){if(!outer_original)return;inc(16);int target=actor&&target_card(*(const uptr*)((char*)actor+0x10b0));if(target)expect_texture(actor,1);Scope scope;int at=enter(&scope,target);if(at>=0){scope.actor=actor;if(face&&face->data&&face->count>0&&face->count<=64&&face->cap>=face->count&&face->data[face->count-1]==0)for(int j=0;j<face->count;j++)scope.face[j]=face->data[j];}outer_original(actor,face);apply_body_skin(actor);leave(&scope,at);}
/* FSoftObjectPath::SetPath receives UTF-16 + length. The lower mesh loader
 * receives FName + subpath FString (24 bytes), NEVER an FString (16 bytes).
 * Let Unreal intern and own the new path; never fabricate or read an FName. */
static const char*profile_for(uptr id){switch(id){case TARGET:return "NF01";case TARGET_2006:return "ND06";case 106781745353130UL:return "ND13";case 106734785925546UL:return "NF27";case 105765448873424UL:return "NFJR";case 88045755960841UL:return "NDXS";case 88038776539586UL:return "NDDB";case 105643042189511UL:return "NDHD";case 106728863696709UL:return "NDHH";case 105848932271764UL:return "NDPQ";case 105874433662542UL:return "NDTL";case 88033139360669UL:return "NDSP";}return 0;}
static int original_face(void*actor,u16*out){if(!take())return 0;uptr t=tid();int yes=0;for(int i=0;i<16;i++)if(scopes[i].tid==t&&scopes[i].top&&scopes[i].top->actor==actor){Scope*s=scopes[i].top;int j=0;for(;j<63&&s->face[j];j++)out[j]=s->face[j];out[j]=0;yes=j>0;break;}drop();return yes;}
__attribute__((visibility("default"))) uptr noodle_path_hook(void*out,const u16*path,int length){
 if(!path_original)return 0;void*actor=active_actor();if(!actor)return path_original(out,path,length);inc(18);
 if(!path||length<1||length>=160)return path_original(out,path,length);
 if(take()){for(int i=0;i<160;i++)last_path[i]=i<length?path[i]:0;stats[21]=*(const u32*)((char*)actor+0x10a8);drop();}
 uptr id=*(const uptr*)((char*)actor+0x10b0);const char*profile=profile_for(id);if(!profile)return path_original(out,path,length);
 u16 face[64],pathface[64];int fn=0,kind=-1;char ascii[64];u16 expected[160];
 /* Preserve v7 behavior: the outer argument may be a base Face ID while the
  * engine formats an ep/lg profile internally. Parse the actual path, not an
  * assumed equality between those two identities. */
 for(int k=0;k<4;k++){
  int n=0;if(k==0)n=put(expected,n,"SkeletalMesh'");if(k==2)n=put(expected,n,"Texture2D'");
  n=put(expected,n,"/Game/Assets/character/RealFace/");n=put(expected,n,k<2?"SK_":"T_");
  int yes=length>n;for(int j=0;j<n&&yes;j++)if(path[j]!=expected[j])yes=0;if(!yes)continue;
  fn=0;while(n+fn<length&&fn<32){u16 c=path[n+fn];if(!((c>='0'&&c<='9')||(c>='a'&&c<='z')))break;ascii[fn]=(char)c;pathface[fn]=c;fn++;}
  ascii[fn]=0;pathface[fn]=0;if(!fn||ascii[0]<'0'||ascii[0]>'9'||fn==32)continue;
  n=put(expected,n,ascii);n=put(expected,n,k<2?"_Face.SK_":"_Face_D.T_");n=put(expected,n,ascii);n=put(expected,n,k<2?"_Face":"_Face_D");if(k==0||k==2)n=put(expected,n,"'");expected[n]=0;
  if(length!=n&&!(length==n+1&&path[n]==0))continue;yes=1;for(int j=0;j<n;j++)if(expected[j]!=path[j]){yes=0;break;}if(yes){kind=k;break;}
 }
 if(kind<0){inc(5);return path_original(out,path,length);}
 int foreign=id==105765448873424UL||id==88045755960841UL||id==88038776539586UL || id==105643042189511UL || id==106728863696709UL || id==105848932271764UL || id==105874433662542UL || id==88033139360669UL;int variant=kind>=0?face_variant(pathface):-1;
 if(!foreign&&variant<0){inc(5);return path_original(out,path,length);}
 if(foreign&&original_face(actor,face)){fn=0;while(fn<63&&face[fn])fn++;}
 else{for(int i=0;i<=fn;i++)face[i]=pathface[i];}
 if(kind<2){
  if(!take()){inc(6);return path_original(out,path,length);}Slot*slot=0;for(int i=0;i<16;i++)if(slots[i].actor==actor){slot=&slots[i];break;}if(!slot)for(int i=0;i<16;i++)if(!slots[i].pending){slot=&slots[i];break;}
  if(!slot){drop();inc(6);return path_original(out,path,length);}slot->actor=actor;slot->pending=1;slot->redirected=1;
  for(int i=0;i<64;i++)slot->face[i]=last_face[i]=i<=fn?face[i]:0;drop();inc(2);inc(19);
 }else{expect_texture(actor,0);inc(17);inc(20);}
 const char*suffix=foreign?"ep00v0313":variants[variant]+4;u16 replaced[160];int n=0;if(kind==0)n=put(replaced,n,"SkeletalMesh'");if(kind==2)n=put(replaced,n,"Texture2D'");
 n=put(replaced,n,"/Game/Assets/character/RealFace/");n=put(replaced,n,kind<2?"SK_":"T_");n=put(replaced,n,profile);n=put(replaced,n,suffix);n=put(replaced,n,kind<2?"_Face.SK_":"_Face_D.T_");n=put(replaced,n,profile);n=put(replaced,n,suffix);n=put(replaced,n,kind<2?"_Face":"_Face_D");if(kind==0||kind==2)n=put(replaced,n,"'");replaced[n]=0;
 return path_original(out,replaced,n+(length>0&&path[length-1]==0));
}

static void restore(void*actor,const u16*face){if(!outer_original)return;int n=0;while(n<63&&face[n])n++;if(!n)return;FString f={face,n+1,n+1};Scope scope;int at=enter(&scope,0);if(at<0){inc(6);return;}inc(8);outer_original(actor,&f);leave(&scope,at);}
/* Observe only. Its second argument is an opaque native FSoftObjectPath. */
__attribute__((visibility("default"))) void noodle_load_hook(void*actor,const void*path){inc(0);if(!mesh_original)return;uptr id=actor?*(const uptr*)((char*)actor+0x10b0):0;if(target_card(id)){inc(1);__atomic_store_n(&stats[10],id,__ATOMIC_RELAXED);}mesh_original(actor,path);}
__attribute__((visibility("default"))) void noodle_done_hook(void*closure,void*result,void*detail){
 if(!done_original)return;void*actor=closure?*(void**)closure:0;u16 face[64];int pending=0;
 if(actor&&target_card(*(const uptr*)((char*)actor+0x10b0))&&take()){for(int i=0;i<16;i++)if(slots[i].actor==actor&&slots[i].pending){pending=1;for(int j=0;j<64;j++)face[j]=slots[i].face[j];slots[i].pending=0;break;}
  const FString*profile=(const FString*)((char*)actor+0x448);if(profile->data&&profile->count>=1&&profile->count<=64&&profile->cap>=profile->count&&profile->data[profile->count-1]==0){for(int j=0;j<64;j++)last_profile[j]=j<profile->count?profile->data[j]:0;inc(12);}drop();}
 int nonnull=result&&*(void**)result;int fallback=pending&&(!nonnull||!__atomic_load_n(&enabled,__ATOMIC_ACQUIRE));if(pending){if(nonnull)inc(3);else inc(4);}done_original(closure,result,detail);apply_body_skin(actor);if(pending&&nonnull&&!fallback)capture_mesh_texture(actor,*(void**)result);if(fallback)restore(actor,face);
}
__attribute__((visibility("default"))) void noodle_texture_done_hook(void*closure,void*result,void*detail){if(!texture_original)return;void*actor=closure?*(void**)closure:0;if(actor&&target_card(*(const uptr*)((char*)actor+0x10b0))){inc(13);if(result&&*(void**)result)inc(14);else inc(15);}texture_original(closure,result,detail);observe_texture(actor,result);}
__attribute__((visibility("default"))) void flush(void*start,uptr n){uptr ctr;__asm__ volatile("mrs %0,ctr_el0":"=r"(ctr));uptr ds=4ul<<((ctr>>16)&15),is=4ul<<(ctr&15),end=(uptr)start+n;for(uptr p=(uptr)start&~(ds-1);p<end;p+=ds)__asm__ volatile("dc cvau,%0"::"r"(p):"memory");__asm__ volatile("dsb ish":::"memory");for(uptr p=(uptr)start&~(is-1);p<end;p+=is)__asm__ volatile("ic ivau,%0"::"r"(p):"memory");__asm__ volatile("dsb ish;isb":::"memory");}
__attribute__((visibility("default"))) void store_instruction(void*p,u32 v){__atomic_store_n((u32*)p,v,__ATOMIC_RELEASE);}

/* UFootballFunctionLibrary.GetPlayerName int64 -> 0x3a55674 ->
 * 0x3a908a0(manager, full ID, FString*). Only this exact card is renamed.
 * Native FString ResizeTo keeps Unreal allocator ownership; no static buffer. */
typedef struct{u16*data;int count,cap;} WritableString;
typedef void(*PlayerNameFn)(void*,uptr,WritableString*);
static PlayerNameFn name_original;
__attribute__((visibility("default"))) void configure_player_name(uptr base,uptr p){engine_base=base;name_original=(PlayerNameFn)p;}
__attribute__((visibility("default"))) void noodle_player_name_hook(void*manager,uptr id,WritableString*out){
 if(!name_original)return;
 if(!__atomic_load_n(&enabled,__ATOMIC_ACQUIRE)||id!=88045755960841UL||!out){name_original(manager,id,out);return;}
 const char*name="Nguyen Xuan Son";int n=15;
 typedef void(*ResizeFn)(WritableString*,int);
 out->count=0;((ResizeFn)(engine_base+0x286ff60))(out,n);
 if(!out->data||out->cap<n){name_original(manager,id,out);return;}
 for(int i=0;i<n;i++)out->data[i]=(unsigned char)name[i];out->count=n;inc(45);
}
