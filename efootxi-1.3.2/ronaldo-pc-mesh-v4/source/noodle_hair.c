/* Exact-card asset-path replacement. Original player/face IDs are never changed. */
typedef unsigned long uptr;typedef unsigned int u32;typedef unsigned short u16;
typedef struct{const u16*data;int count,cap;} FString;
typedef void(*LoadFn)(void*,const FString*);typedef void(*DoneFn)(void*,void*,void*);
#define TARGET 88044950524330UL
static LoadFn outer_original,mesh_original;static DoneFn done_original,texture_original;
__attribute__((visibility("hidden"))) uptr printf_original,texture_format;
static volatile u32 enabled;static volatile uptr stats[24];static unsigned char lock;
static int take(void){return !__atomic_test_and_set(&lock,__ATOMIC_ACQUIRE);}static void drop(void){__atomic_clear(&lock,__ATOMIC_RELEASE);}static void inc(u32 i){__atomic_fetch_add(&stats[i],1,__ATOMIC_RELAXED);}
static uptr tid(void){uptr p;__asm__ volatile("mrs %0,tpidr_el0":"=r"(p));return p;}
typedef struct Scope{int target;struct Scope*prev;}Scope;
static struct{uptr tid;Scope*top;} scopes[16];
static int enter(Scope*s,int target){if(!take())return -1;uptr t=tid();int free=-1,slot=-1;for(int i=0;i<16;i++){if(scopes[i].tid==t){slot=i;break;}if(!scopes[i].tid)free=i;}if(slot<0)slot=free;if(slot>=0){s->target=target;s->prev=scopes[slot].top;scopes[slot].tid=t;scopes[slot].top=s;}drop();return slot;}
static void leave(Scope*s,int slot){if(slot<0)return;while(!take()){}if(scopes[slot].top==s){scopes[slot].top=s->prev;if(!s->prev)scopes[slot].tid=0;}drop();}
static int active(void){if(!__atomic_load_n(&enabled,__ATOMIC_ACQUIRE)||!take())return 0;uptr t=tid();int yes=0;for(int i=0;i<16;i++)if(scopes[i].tid==t&&scopes[i].top){yes=scopes[i].top->target;break;}drop();return yes;}
static int eq(const u16*a,const char*b){if(!a)return 0;for(int i=0;i<160;i++){if(a[i]!=(unsigned char)b[i])return 0;if(!b[i])return 1;}return 0;}
static const char*variants[]={"4522","4522lg00v0000","4522ep01v0291","4522ep00v0313"};
static int face_variant(const u16*a){for(int i=0;i<4;i++)if(eq(a,variants[i]))return i;return -1;}
static int put(u16*out,int at,const char*s){while(*s)out[at++]=(unsigned char)*s++;return at;}
typedef struct{void*actor;u16 face[64];u32 pending,redirected;}Slot;static Slot slots[16];static u16 last_face[64],last_profile[64];
__attribute__((visibility("default"))) void configure_outer(uptr base,uptr p){(void)base;outer_original=(LoadFn)p;}
__attribute__((visibility("default"))) void configure_load(uptr base,uptr p){(void)base;mesh_original=(LoadFn)p;}
__attribute__((visibility("default"))) void configure_done(uptr base,uptr p){(void)base;done_original=(DoneFn)p;}
__attribute__((visibility("default"))) void configure_texture_done(uptr base,uptr p){(void)base;texture_original=(DoneFn)p;}
__attribute__((visibility("default"))) void configure_printf(uptr base,uptr p){printf_original=p;texture_format=base+0x85575c;}
__attribute__((visibility("default"))) void noodle_enable(u32 v){__atomic_store_n(&enabled,v==1,__ATOMIC_RELEASE);}
__attribute__((visibility("default"))) uptr noodle_stat(u32 i){return i<24?__atomic_load_n(&stats[i],__ATOMIC_RELAXED):0;}
__attribute__((visibility("default"))) u32 noodle_face_char(u32 i){u32 v=0;if(i<64&&take()){v=last_face[i];drop();}return v;}
__attribute__((visibility("default"))) u32 noodle_profile_char(u32 i){u32 v=0;if(i<64&&take()){v=last_profile[i];drop();}return v;}
__attribute__((visibility("default"))) void noodle_outer_hook(void*actor,const FString*face){if(!outer_original)return;inc(16);int target=actor&&*(const uptr*)((char*)actor+0x10b0)==TARGET;Scope scope;int at=enter(&scope,target);outer_original(actor,face);leave(&scope,at);}
__attribute__((visibility("hidden"))) uptr texture_id(u16*out,const u16*a,const u16*b){if(!active())return 0;int v=face_variant(a);if(v<0||!eq(b,variants[v]))return 0;int n=put(out,0,variants[v]);out[n]=0;out[0]=78;out[1]=68;out[2]=48;out[3]=49;inc(17);return (uptr)out;}
/* Only the exact Face_D format is intercepted; unrelated varargs calls tail-call unchanged.
 * x8 is the non-trivial FString result address and is preserved across the helper. */
__attribute__((naked,visibility("default"))) void noodle_printf_hook(void){__asm__ volatile(
 "adrp x16,texture_format\nldr x16,[x16,:lo12:texture_format]\ncmp x0,x16\nb.ne 3f\n"
 "stp x29,x30,[sp,#-256]!\nstp x0,x1,[sp,#16]\nstp x2,x3,[sp,#32]\nstp x4,x5,[sp,#48]\nstp x6,x7,[sp,#64]\nstr x8,[sp,#80]\n"
 "add x0,sp,#96\nbl texture_id\nmov x16,x0\nldp x0,x1,[sp,#16]\nldp x2,x3,[sp,#32]\nldp x4,x5,[sp,#48]\nldp x6,x7,[sp,#64]\nldr x8,[sp,#80]\ncbz x16,1f\nmov x1,x16\nmov x2,x16\n1:\n"
 "adrp x17,printf_original\nldr x17,[x17,:lo12:printf_original]\nblr x17\nldp x29,x30,[sp],#256\nret\n"
 "3:\nadrp x16,printf_original\nldr x16,[x16,:lo12:printf_original]\nbr x16\n");}
static void restore(void*actor,const u16*face){if(!outer_original)return;int n=0;while(n<63&&face[n])n++;if(!n)return;FString f={face,n+1,n+1};Scope scope;int at=enter(&scope,0);if(at<0){inc(6);return;}inc(8);outer_original(actor,&f);leave(&scope,at);}
__attribute__((visibility("default"))) void noodle_load_hook(void*actor,const FString*path){
 inc(0);if(!mesh_original)return;uptr id=actor?*(const uptr*)((char*)actor+0x10b0):0;if(id!=TARGET){mesh_original(actor,path);return;}inc(1);__atomic_store_n(&stats[10],id,__ATOMIC_RELAXED);
 if(!active()){inc(7);mesh_original(actor,path);return;}
 if(!path||!path->data||path->count<1||path->count>160||path->cap<path->count||path->data[path->count-1]){inc(5);mesh_original(actor,path);return;}
 u16 expected[160];int variant=-1;
 for(int v=0;v<4;v++){int n=put(expected,0,"SkeletalMesh'/Game/Assets/character/RealFace/SK_");n=put(expected,n,variants[v]);n=put(expected,n,"_Face.SK_");n=put(expected,n,variants[v]);n=put(expected,n,"_Face'");expected[n]=0;if(n+1==path->count){int yes=1;for(int j=0;j<=n;j++)if(expected[j]!=path->data[j]){yes=0;break;}if(yes){variant=v;break;}}}
 if(variant<0){inc(5);mesh_original(actor,path);return;}
 if(!take()){inc(6);mesh_original(actor,path);return;}Slot*slot=0;for(int i=0;i<16;i++)if(slots[i].actor==actor){slot=&slots[i];break;}if(!slot)for(int i=0;i<16;i++)if(!slots[i].pending){slot=&slots[i];break;}
 if(!slot){drop();inc(6);mesh_original(actor,path);return;}slot->actor=actor;slot->pending=1;slot->redirected=1;for(int i=0;i<64;i++)slot->face[i]=last_face[i]=0;put(slot->face,0,variants[variant]);put(last_face,0,variants[variant]);drop();
 u16 replaced[160];for(int i=0;i<path->count;i++)replaced[i]=path->data[i];for(int i=0;i+6<path->count;i++)if(replaced[i]==83&&replaced[i+1]==75&&replaced[i+2]==95&&replaced[i+3]==52&&replaced[i+4]==53&&replaced[i+5]==50&&replaced[i+6]==50){replaced[i+3]=78;replaced[i+4]=68;replaced[i+5]=48;replaced[i+6]=49;}
 inc(2);FString next={replaced,path->count,path->count};mesh_original(actor,&next);
}
__attribute__((visibility("default"))) void noodle_done_hook(void*closure,void*result,void*detail){
 if(!done_original)return;void*actor=closure?*(void**)closure:0;u16 face[64];int pending=0;
 if(actor&&*(const uptr*)((char*)actor+0x10b0)==TARGET&&take()){for(int i=0;i<16;i++)if(slots[i].actor==actor&&slots[i].pending){pending=1;for(int j=0;j<64;j++)face[j]=slots[i].face[j];slots[i].pending=0;break;}
  const FString*profile=(const FString*)((char*)actor+0x448);if(profile->data&&profile->count>=1&&profile->count<=64&&profile->cap>=profile->count&&profile->data[profile->count-1]==0){for(int j=0;j<64;j++)last_profile[j]=j<profile->count?profile->data[j]:0;inc(12);}drop();}
 int nonnull=result&&*(void**)result;int fallback=pending&&(!nonnull||!__atomic_load_n(&enabled,__ATOMIC_ACQUIRE));if(pending){if(nonnull)inc(3);else inc(4);}done_original(closure,result,detail);if(fallback)restore(actor,face);
}
__attribute__((visibility("default"))) void noodle_texture_done_hook(void*closure,void*result,void*detail){if(!texture_original)return;void*actor=closure?*(void**)closure:0;if(actor&&*(const uptr*)((char*)actor+0x10b0)==TARGET){inc(13);if(result&&*(void**)result)inc(14);else inc(15);}texture_original(closure,result,detail);}
__attribute__((visibility("default"))) void flush(void*start,uptr n){uptr ctr;__asm__ volatile("mrs %0,ctr_el0":"=r"(ctr));uptr ds=4ul<<((ctr>>16)&15),is=4ul<<(ctr&15),end=(uptr)start+n;for(uptr p=(uptr)start&~(ds-1);p<end;p+=ds)__asm__ volatile("dc cvau,%0"::"r"(p):"memory");__asm__ volatile("dsb ish":::"memory");for(uptr p=(uptr)start&~(is-1);p<end;p+=is)__asm__ volatile("ic ivau,%0"::"r"(p):"memory");__asm__ volatile("dsb ish;isb":::"memory");}
__attribute__((visibility("default"))) void store_instruction(void*p,u32 v){__atomic_store_n((u32*)p,v,__ATOMIC_RELEASE);}
