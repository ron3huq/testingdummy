/* Cache GamePlan consumers bypass the database getter used by FULL-7.
   Bridge only those two accessors through the existing scoped plan editor. */
typedef unsigned long uptr;
typedef unsigned int u32;
typedef struct{uptr kind,id;}Key;
static uptr engine;
static void*(*original_index)(void*,void*);
static void*(*original_find)(void*,void*);
static void*(*refresh_team)(void*,void*);
static void*(*edit_plan)(void*,Key);
static uptr index_calls,find_calls,edited,mismatch;
static void*(*previous_player)(void*,Key);
static u32(*scope_id)(u32);
static volatile u32 booster_lock;
typedef struct{uptr id;u32 cid,values[3];}Booster;
typedef struct{void*p;u32 values[3],saved,applied;}BoosterSnapshot;
static Booster boosters[1024];static BoosterSnapshot boost_old[1024];
static u32 booster_count,booster_ready;static uptr booster_applies;
__attribute__((visibility("default")))void tactics_player_bind(uptr base,uptr previous,uptr scope){engine=base;previous_player=(void*)previous;scope_id=(void*)scope;}
__attribute__((visibility("default")))u32 transfer_booster_add(uptr id,u32 cid,u32 a,u32 b,u32 c){if(booster_ready||!id||booster_count==1024||a>255||b>1023||c>1023)return 0;boosters[booster_count++]=(Booster){id,cid,{a,b,c}};return 1;}
__attribute__((visibility("default")))void transfer_booster_commit(void){__atomic_store_n(&booster_ready,1,__ATOMIC_RELEASE);}
__attribute__((visibility("default")))void*tactics_player_hook(void*db,Key key){
 void*p=previous_player(db,key);if(!p||!__atomic_load_n(&booster_ready,__ATOMIC_ACQUIRE))return p;
 Key actual=((Key(*)(void*))(engine+0x68fe720))(p);if(actual.id!=key.id)return p;
 u32 cid=scope_id?scope_id(0):0,first=1024,chosen=1024;
 for(u32 i=0;i<booster_count;i++)if(boosters[i].id==key.id){if(first==1024)first=i;if(boosters[i].cid==0&&chosen==1024)chosen=i;if(boosters[i].cid==cid)chosen=i;}
 if(first==1024)return p;
 while(__atomic_exchange_n(&booster_lock,1,__ATOMIC_ACQUIRE)){}
 u32(*get)(void*,u32,u32*)=(void*)(engine+0x82a84d4);u32(*set)(void*,u32,u32)=(void*)(engine+0x82a907c);
 BoosterSnapshot*s=&boost_old[first];
 if(s->p!=p){s->p=p;s->saved=0;s->applied=0;}
 if(s->applied){for(u32 i=0;i<3;i++)set(p,144+i,s->values[i]);s->applied=0;}
 if(chosen!=1024){
  if(!s->saved){u32 ok=1;for(u32 i=0;i<3;i++)ok&=get(p,144+i,&s->values[i]);s->saved=ok;}
  if(s->saved){for(u32 i=0;i<3;i++)set(p,144+i,boosters[chosen].values[i]);s->applied=1;__atomic_fetch_add(&booster_applies,1,__ATOMIC_RELAXED);}
 }
 __atomic_store_n(&booster_lock,0,__ATOMIC_RELEASE);return p;
}
typedef struct{uptr thread;u32 depth;}Guard;
static Guard guards[32];
static Guard *guard(void){uptr thread;__asm__ volatile("mrs %0,tpidr_el0":"=r"(thread));for(unsigned i=0;i<32;i++){uptr value=__atomic_load_n(&guards[i].thread,__ATOMIC_ACQUIRE);if(value==thread)return &guards[i];if(!value&&__atomic_compare_exchange_n(&guards[i].thread,&value,thread,0,__ATOMIC_ACQ_REL,__ATOMIC_ACQUIRE))return &guards[i];}return 0;}
__attribute__((visibility("default")))void configure_cached_plan_index(uptr base,uptr fn){engine=base;original_index=(void*)fn;}
__attribute__((visibility("default")))void configure_cached_plan_find(uptr base,uptr fn){engine=base;original_find=(void*)fn;}
__attribute__((visibility("default")))void cached_plan_bind(uptr editor,uptr team){edit_plan=(void*)editor;refresh_team=(void*)team;}
static void *apply(void*root,void*p){
 if(!p||!edit_plan||!refresh_team)return p;
 uptr delta=(uptr)p-(uptr)root-0x11d0;
 if(delta!=0&&delta!=0x188){__atomic_fetch_add(&mismatch,1,__ATOMIC_RELAXED);return p;}
 Guard*g=guard();if(!g||g->depth)return p;
 g->depth=1;u32 side=(u32)(delta/0x188);
 /* Prime the edited Team and the editor's per-thread pool/order mapping first. */
 void*t=refresh_team(root,&side);
 Key key=((Key(*)(void*))(engine+0x68f89ec))(p);
 void*context=((void*(*)(void))(engine+0x82468d4))();
 void*db=context?*(void**)((char*)context+0x40):0;
 void*out=p;
 if(t&&db){
  Key teamkey=*(Key*)((char*)t+0x390);
  /* Different record types can encode different words; require the native
     plan identity returned by the getter, then let its editor verify it. */
  if(key.id&&teamkey.id==key.id){void*q=edit_plan(db,key);if(q){out=q;if(q!=p)__atomic_fetch_add(&edited,1,__ATOMIC_RELAXED);}}
 }
 g->depth=0;return out;
}
__attribute__((visibility("default")))void *cached_plan_index(void*root,void*key){__atomic_fetch_add(&index_calls,1,__ATOMIC_RELAXED);return apply(root,original_index(root,key));}
__attribute__((visibility("default")))void *cached_plan_find(void*root,void*key){__atomic_fetch_add(&find_calls,1,__ATOMIC_RELAXED);return apply(root,original_find(root,key));}
__attribute__((visibility("default")))uptr cached_plan_status(u32 i){if(i==0)return index_calls;if(i==1)return find_calls;if(i==2)return edited;if(i==3)return mismatch;if(i==4)return booster_applies;return 0;}
__attribute__((visibility("default")))void flush(void *start,uptr n){uptr ctr;__asm__ volatile("mrs %0,ctr_el0":"=r"(ctr));uptr ds=4ul<<((ctr>>16)&15),is=4ul<<(ctr&15),end=(uptr)start+n;for(uptr p=(uptr)start&~(ds-1);p<end;p+=ds)__asm__ volatile("dc cvau,%0"::"r"(p):"memory");__asm__ volatile("dsb ish":::"memory");for(uptr p=(uptr)start&~(is-1);p<end;p+=is)__asm__ volatile("ic ivau,%0"::"r"(p):"memory");__asm__ volatile("dsb ish;isb":::"memory");}
__attribute__((visibility("default")))void store_instruction(void*p,u32 x){__atomic_store_n((u32*)p,x,__ATOMIC_RELEASE);}
