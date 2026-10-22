/* Exact-card render request redirect. Engine callbacks run on original threads.
 * No player DB, shared mesh/material or other hotfix state is modified. */
typedef unsigned long uptr; typedef unsigned int u32; typedef unsigned short u16;
typedef struct {const u16 *data;int count,cap;} FString;
typedef void (*LoadFn)(void*,const FString*);
typedef void (*DoneFn)(void*,void*,void*);
static LoadFn load_original;static DoneFn done_original;
static volatile u32 enabled;static volatile uptr stats[16];static unsigned char lock;
#define TARGET 88044950524330UL

typedef struct {void *actor;u16 face[64];int length;u32 pending;} Slot;
static Slot slots[16];static u16 last_face[64];
static int take(void){return !__atomic_test_and_set(&lock,__ATOMIC_ACQUIRE);}
static void drop(void){__atomic_clear(&lock,__ATOMIC_RELEASE);}
static void inc(u32 n){__atomic_fetch_add(&stats[n],1,__ATOMIC_RELAXED);}
__attribute__((visibility("default"))) void configure_load(uptr base,uptr p){(void)base;load_original=(LoadFn)p;}
__attribute__((visibility("default"))) void configure_done(uptr base,uptr p){(void)base;done_original=(DoneFn)p;}
__attribute__((visibility("default"))) void noodle_enable(u32 v){__atomic_store_n(&enabled,v==1,__ATOMIC_RELEASE);}
__attribute__((visibility("default"))) uptr noodle_stat(u32 n){return n<16?__atomic_load_n(&stats[n],__ATOMIC_RELAXED):0;}
__attribute__((visibility("default"))) u32 noodle_face_char(u32 i){u32 v=0;if(i>=64||!take())return 0;v=last_face[i];drop();return v;}
__attribute__((visibility("default"))) void noodle_load_hook(void *actor,const FString *face){
 inc(0);if(!load_original)return;
 uptr id=actor?*(const uptr*)((const unsigned char*)actor+0x10b0):0;
 if(id!=TARGET){load_original(actor,face);return;}
 inc(1);__atomic_store_n(&stats[10],id,__ATOMIC_RELAXED);
 if(!__atomic_load_n(&enabled,__ATOMIC_ACQUIRE)){inc(7);load_original(actor,face);return;}
 if(!face||!face->data||face->count<5||face->count>64||face->cap<face->count||face->data[face->count-1]||face->data[0]!=52||face->data[1]!=53||face->data[2]!=50||face->data[3]!=50){inc(5);load_original(actor,face);return;}
 if(!take()){inc(6);load_original(actor,face);return;}
 Slot *slot=0;
 for(u32 i=0;i<16;i++)if(slots[i].actor==actor){slot=&slots[i];break;}
 if(!slot)for(u32 i=0;i<16;i++)if(!slots[i].pending){slot=&slots[i];break;}
 if(!slot){drop();inc(6);load_original(actor,face);return;}
 slot->actor=actor;slot->length=face->count;
 for(u32 i=0;i<64;i++){u16 c=i<(u32)face->count?face->data[i]:0;slot->face[i]=c;last_face[i]=c;}
 slot->pending=1;drop();inc(2);
 u16 replaced[64];for(int j=0;j<face->count;j++)replaced[j]=face->data[j];replaced[0]=78;replaced[1]=68;replaced[2]=48;replaced[3]=49;
 FString replacement={replaced,face->count,face->count};load_original(actor,&replacement);
}
__attribute__((visibility("default"))) void noodle_done_hook(void *closure,void *result,void *detail){
 if(!done_original)return;
 void *actor=closure?*(void**)closure:0;u16 restore[64];int length=0;int pending=0;
 if(actor&&*(const uptr*)((unsigned char*)actor+0x10b0)==TARGET&&take()){
  for(u32 i=0;i<16;i++)if(slots[i].actor==actor&&slots[i].pending){pending=1;length=slots[i].length;for(u32 j=0;j<64;j++)restore[j]=slots[i].face[j];slots[i].pending=0;break;}
  drop();
 }
 int nonnull=result&&*(void**)result;
 int fallback=pending&&(!nonnull||!__atomic_load_n(&enabled,__ATOMIC_ACQUIRE));
 if(pending){if(nonnull)inc(3);else inc(4);if(fallback)inc(8);}
 /* Always delegate first, including null-result cleanup and ownership of detail. */
 done_original(closure,result,detail);
 if(fallback&&load_original&&length>0){FString original={restore,length,length};load_original(actor,&original);}
}
__attribute__((visibility("default"))) void flush(void *start,uptr n){uptr ctr;__asm__ volatile("mrs %0, ctr_el0":"=r"(ctr));uptr ds=4ul<<((ctr>>16)&15),is=4ul<<(ctr&15),end=(uptr)start+n;for(uptr p=(uptr)start&~(ds-1);p<end;p+=ds)__asm__ volatile("dc cvau, %0"::"r"(p):"memory");__asm__ volatile("dsb ish":::"memory");for(uptr p=(uptr)start&~(is-1);p<end;p+=is)__asm__ volatile("ic ivau, %0"::"r"(p):"memory");__asm__ volatile("dsb ish; isb":::"memory");}
__attribute__((visibility("default"))) void store_instruction(void *p,u32 v){__atomic_store_n((u32*)p,v,__ATOMIC_RELEASE);}
