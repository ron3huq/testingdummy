/* Exact Transfer overrides run after classic/world/rating and the existing bridge.
 * No SQL, allocation, IO or key coercion inside native callbacks.
 */
typedef unsigned long U;typedef unsigned int W;typedef unsigned short H;typedef unsigned char B;typedef struct{U kind,id;}Key;
#define EX __attribute__((visibility("default")))
#define CAP 1024
static U engine;static void*(*previous)(void*,Key);static W(*scope)(W);static W ready,lock;
typedef struct{U id;W cid;H value[147];B present[147];}Profile;
typedef struct{void*p;H old[147];B present[147];W applied;}Snapshot;
static Profile profiles[CAP];static Snapshot snapshots[CAP];static W count;
static U calls,applies,restores,rejected,last_id;static W last_cid;
static W league(W c){return c==122||c==128||c==473||c==518||c==566||c==549||c==125;}
static W valid(void*p,U id){if(!p)return 0;Key k=((Key(*)(void*))(engine+0x68fe720))(p);return k.kind==0&&k.id==id;}
static W allowed(W ix,W v){return(ix<14&&v<=(ix?2:12))||(ix>=14&&ix<=40&&ix!=33&&v<=127)||((ix==42||ix==45)&&v<=3)||(ix==43&&v<=1)||(ix==59&&v<=511)||(ix==60&&v<=127)||(ix>=70&&ix<=143&&v<=1)||(ix==144&&v<=255)||(ix>144&&ix<=146&&v<=1023);}

typedef struct{U id;W cid,stamp;H values[147];H pad;}Observed;
static Observed observed[512];static W observed_count,observed_lock;static U observed_generation;
static void observe(void*p,U id,W cid){
 if(!league(cid)||!valid(p,id))return;
 while(__atomic_exchange_n(&observed_lock,1,__ATOMIC_ACQUIRE)){}
 for(W i=0;i<observed_count;i++)if(observed[i].id==id&&observed[i].cid==cid){__atomic_store_n(&observed_lock,0,__ATOMIC_RELEASE);return;}
 W at=observed_count<512?observed_count++:(W)(observed_generation%512);Observed*o=&observed[at];o->id=id;o->cid=cid;o->stamp=(W)++observed_generation;
 for(W k=0;k<147;k++){W v=0;((W(*)(void*,W,W*))(engine+0x82a84d4))(p,k,&v);o->values[k]=(H)v;}
 __atomic_store_n(&observed_lock,0,__ATOMIC_RELEASE);
}
EX W final_copy_observed(void*out,W bytes){if(!out||bytes<sizeof(observed))return 0;while(__atomic_exchange_n(&observed_lock,1,__ATOMIC_ACQUIRE)){}for(W i=0;i<observed_count*sizeof(Observed);i++)((volatile B*)out)[i]=((volatile B*)observed)[i];W n=observed_count;__atomic_store_n(&observed_lock,0,__ATOMIC_RELEASE);return n;}

EX W final_bind(U base,U prev,U context){if(engine||!prev||!context)return 0;engine=base;previous=(void*)prev;scope=(void*)context;return 1;}
EX W final_add(U id,W cid){if(ready||!id||id>>63||(!league(cid)&&cid)||count==CAP)return 0;for(W i=0;i<count;i++)if(profiles[i].id==id&&profiles[i].cid==cid)return i+1;profiles[count].id=id;profiles[count].cid=cid;return ++count;}
EX W final_parameter(W row,W ix,W v){if(ready||!row||row>count||ix>=147||!allowed(ix,v))return 0;profiles[row-1].present[ix]=1;profiles[row-1].value[ix]=(H)v;return 1;}
EX void final_commit(void){__atomic_store_n(&ready,1,__ATOMIC_RELEASE);}
static U owner;static U balance_skips;
static U thread_id(void){U t;__asm__ volatile("mrs %0,tpidr_el0":"=r"(t));return t;}
static W relevant(U id){for(W i=0;i<count;i++)if(profiles[i].id==id)return 1;return 0;}
static W acquire(void){U t=thread_id();if(__atomic_load_n(&owner,__ATOMIC_ACQUIRE)==t)return 0;while(__atomic_exchange_n(&lock,1,__ATOMIC_ACQUIRE)){}__atomic_store_n(&owner,t,__ATOMIC_RELEASE);return 1;}
static void release(W token){if(token){__atomic_store_n(&owner,0,__ATOMIC_RELEASE);__atomic_store_n(&lock,0,__ATOMIC_RELEASE);}}
EX W final_before_record(void*p,U id){
 if(!__atomic_load_n(&ready,__ATOMIC_ACQUIRE)||!relevant(id)||!valid(p,id))return 0;W token=acquire();
 W(*set)(void*,W,W)=(void*)(engine+0x82a907c);
 for(W i=count;i>0;i--){Profile*r=&profiles[i-1];Snapshot*s=&snapshots[i-1];if(r->id==id&&s->applied){if(s->p==p){for(W k=0;k<147;k++)if(s->present[k])set(p,k,s->old[k]);restores++;}s->applied=0;}}
 return token;
}
EX W final_skip_balance(void*p,U id){
 if(!__atomic_load_n(&ready,__ATOMIC_ACQUIRE)||!valid(p,id))return 0;W cid=scope(0);if(!league(cid))return 0;
 for(W i=0;i<count;i++){Profile*r=&profiles[i];if(r->id!=id||(r->cid&&r->cid!=cid))continue;for(W k=14;k<=40;k++)if(k!=33&&r->present[k]){__atomic_fetch_add(&balance_skips,1,__ATOMIC_RELAXED);return 1;}}
 return 0;
}
EX void final_after_record(void*p,U id,W token){
 if(!__atomic_load_n(&ready,__ATOMIC_ACQUIRE)||!valid(p,id)){release(token);return;}W extra=0;W cid=scope(0);
 if(relevant(id)){
  if(!token)extra=acquire();W(*get)(void*,W,W*)=(void*)(engine+0x82a84d4);W(*set)(void*,W,W)=(void*)(engine+0x82a907c);
  if(league(cid))for(W pass=0;pass<2;pass++)for(W i=0;i<count;i++){
   Profile*r=&profiles[i];if(r->id!=id||!((pass==0&&r->cid==0)||(pass==1&&r->cid==cid)))continue;
   Snapshot*s=&snapshots[i];W capture=!s->applied||s->p!=p;s->p=p;
   for(W k=0;k<147;k++)if(r->present[k]){if(capture){W v=0;get(p,k,&v);s->old[k]=(H)v;s->present[k]=1;}if(!set(p,k,r->value[k]))rejected++;}
   s->applied=1;applies++;last_id=id;last_cid=cid;
  }
 }
 observe(p,id,cid);release(extra);release(token);
}
EX void*final_player(void*db,Key key){
 __atomic_fetch_add(&calls,1,__ATOMIC_RELAXED);void*p=previous(db,key);
 if(ready&&valid(p,key.id))final_after_record(p,key.id,0);else if(p)rejected++;
 return p;
}
EX U final_status(W i){if(i==0)return ready;if(i==1)return count;if(i==2)return calls;if(i==3)return applies;if(i==4)return restores;if(i==5)return rejected;if(i==6)return last_id;if(i==7)return last_cid;if(i==8)return observed_count;if(i==9)return observed_generation;if(i==10)return balance_skips;return 0;}
