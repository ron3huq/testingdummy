/* APK73 native PlayerKey bridge. No SQL, Python or file access in game hooks.
 * Offsets come from the pinned original ARM64 823c8d4/823c9a8/823be04.
 * A mode-2 key has a pool index in word zero; canonical editor IDs do not.
 */
typedef unsigned long uptr;
typedef unsigned int u32;
typedef struct {uptr kind,id;} Key;
typedef void *(*Lookup)(void *,Key);
typedef Key (*GetKey)(void *);
static uptr engine;
static Lookup original_lookup,mod_player;
static GetKey get_key;
static volatile u32 cache_lock;
typedef struct {void *db;uptr id;u32 index,count;} Item;
static Item cache[4096];
static uptr hits,searches,canonicalized,rejected;
#define MAX_INDEX 0x12f34u
#define STRIDE 0x1d0u
#define MODE_OFFSET 0x3194a10u
#define COUNT_OFFSET 0x2686098u
static void lock(void){while(__atomic_exchange_n(&cache_lock,1,__ATOMIC_ACQUIRE)){} }
static void unlock(void){__atomic_store_n(&cache_lock,0,__ATOMIC_RELEASE);}
static int mode2(void *db){return db&&*(u32*)((char*)db+MODE_OFFSET)==2;}
static int same(void *p,uptr id){if(!p)return 0;Key k=get_key(p);return (u32)k.kind==0&&k.id==id;}
static void *find(void *db,uptr id){
 u32 n=*(u32*)((char*)db+COUNT_OFFSET);if(!n||n>MAX_INDEX+1){__atomic_fetch_add(&rejected,1,__ATOMIC_RELAXED);return 0;}
 unsigned slot=(unsigned)((id^(id>>32)^((uptr)db>>8))&4095);Item item;
 lock();item=cache[slot];unlock();
 if(item.db==db&&item.id==id&&item.count==n&&item.index<=MAX_INDEX){void*p=(char*)db+(uptr)item.index*STRIDE;if(same(p,id)){__atomic_fetch_add(&hits,1,__ATOMIC_RELAXED);return p;}}
 /* The ordinary ID search is separate from the mode-2 index getter. It
    already bounds the main pool using COUNT_OFFSET and the 80 reserve rows. */
 __atomic_fetch_add(&searches,1,__ATOMIC_RELAXED);void*p=((Lookup)(engine+0x823be04))(db,(Key){0,id});
 if(!same(p,id)){
  p=0;
  for(u32 i=0;i<n;i++){void*q=(char*)db+(uptr)i*STRIDE;if(same(q,id)){p=q;break;}}
 }
 if(!p){__atomic_fetch_add(&rejected,1,__ATOMIC_RELAXED);return 0;}
 uptr delta=(uptr)p-(uptr)db;
 if(delta%STRIDE==0&&delta/STRIDE<=MAX_INDEX){lock();cache[slot]=(Item){db,id,(u32)(delta/STRIDE),n};unlock();}
 return p;
}
__attribute__((visibility("default"))) void *cached_lookup_original(void *db,Key key){
 void*p=original_lookup(db,key);
 if(!mode2(db)||!key.id||(u32)key.kind>MAX_INDEX||same(p,key.id))return p;
 void*q=find(db,key.id);return q?q:p;
}
__attribute__((visibility("default"))) void *cached_lookup_player(void *db,Key key){
 if(mode2(db)&&key.id&&(u32)key.kind<=MAX_INDEX){
  void*p=cached_lookup_original(db,key);
  if(same(p,key.id)){key.kind=0;__atomic_fetch_add(&canonicalized,1,__ATOMIC_RELAXED);}
 }
 return mod_player(db,key);
}
__attribute__((visibility("default"))) u32 cached_lookup_configure(uptr base,uptr original,uptr mod){
 if(original_lookup||!original||!mod)return 0;
 engine=base;original_lookup=(Lookup)original;mod_player=(Lookup)mod;get_key=(GetKey)(base+0x68fe720);return 1;
}
__attribute__((visibility("default"))) uptr cached_lookup_status(u32 i){if(i==0)return __atomic_load_n(&hits,__ATOMIC_RELAXED);if(i==1)return __atomic_load_n(&searches,__ATOMIC_RELAXED);if(i==2)return __atomic_load_n(&canonicalized,__ATOMIC_RELAXED);if(i==3)return __atomic_load_n(&rejected,__ATOMIC_RELAXED);return 0;}

/* Single Player selects by card ID; live GamePlayerKeys also contain serial.
   Preserve the verified module's AI lifecycle. Only its roster lookup gets
   the exact live key; all other callers retain native serial-sensitive lookup. */
static uptr single_engine,caller_low,caller_high,single_hits;
static u32 (*single_original)(void*,Key);
__attribute__((visibility("default"))) void configure_single_lookup(uptr base,uptr trampoline){single_engine=base;single_original=(void*)trampoline;}
__attribute__((visibility("default"))) void single_lookup_caller(uptr low,uptr high){caller_low=low;caller_high=high;}
__attribute__((visibility("default"))) u32 single_lookup_hook(void *team,Key wanted){
 uptr caller=(uptr)__builtin_return_address(0);
 if(!team||wanted.kind||!wanted.id||caller<caller_low||caller>=caller_high)return single_original(team,wanted);
 /* Iterate the eleven actual starting slots, not the storage pool order.
    Do not select an opponent, substitute or another card with matching low32. */
 for(u32 slot=0;slot<11;slot++){
  u32 pool=((u32(*)(void*,u32))(single_engine+0x72f29c4))(team,slot);
  if(pool>=40)continue;
  void*entry=((void*(*)(void*,u32))(single_engine+0x72f2ca8))(team,pool);
  if(!entry)continue;
  Key actual=((Key(*)(void*))(single_engine+0x72f29e0))(entry);
  if(actual.id!=wanted.id)continue;
  u32 result=single_original(team,actual);
  if(result<22){__atomic_fetch_add(&single_hits,1,__ATOMIC_RELAXED);return result;}
 }
 return single_original(team,wanted);
}
__attribute__((visibility("default"))) uptr single_lookup_status(void){return __atomic_load_n(&single_hits,__ATOMIC_RELAXED);}
__attribute__((visibility("default"))) void flush(void *start,uptr n){uptr ctr;__asm__ volatile("mrs %0, ctr_el0":"=r"(ctr));uptr ds=4ul<<((ctr>>16)&15),is=4ul<<(ctr&15),end=(uptr)start+n;for(uptr p=(uptr)start&~(ds-1);p<end;p+=ds)__asm__ volatile("dc cvau, %0"::"r"(p):"memory");__asm__ volatile("dsb ish":::"memory");for(uptr p=(uptr)start&~(is-1);p<end;p+=is)__asm__ volatile("ic ivau, %0"::"r"(p):"memory");__asm__ volatile("dsb ish; isb":::"memory");}
__attribute__((visibility("default"))) void store_instruction(void *p,u32 v){__atomic_store_n((u32*)p,v,__ATOMIC_RELEASE);}
