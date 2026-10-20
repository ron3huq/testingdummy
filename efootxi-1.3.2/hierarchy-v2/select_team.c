/* Runtime-only My League vectors, same Android 1.3.2 getter as successful v1. */
typedef unsigned int u32;
typedef unsigned long uptr;
typedef struct {uptr begin,end,cap;} Vec;
static const u32 old_0_0[]={213,182,413,114,4211,4213,1329,420,218,212,180,414,403,181,112,217,221,113};
static const u32 old_0_1[]={101,102,103,114,100,173,179,108,109,172,121,119,120,181,112,125,327,130};
static const u32 target_0[]={101,102,103,114,100,173,179,108,109,172,121,119,120,181,127,125,327,130};
static const u32 old_1_0[]={5422,5195,5191,269,2009,5221,1196,1200,1195,2019,5217,174,5220,2013,5194,1197,6067,2010};
static const u32 target_1[]={5763,5750,1031,5759,5752,54,52,53,1184,57,55,1010,1032,1026,56,5748,1011,1012};
static const u32 old_2_0[]={1974,2387,1804,5028,2388,1979,192,2380,4082,5845,5844,191,193,5633,2383,2391,1944,1976};
static const u32 target_2[]={7,50,8,5,45,6,10,9,14,12,24,49,44,40,32,39,16,17,38,1174};
typedef struct {const u32 *old;int nold;const u32 *previous;int nprevious;const u32 *target;int n;} Rule;
static const Rule rules[]={{old_0_0,18,old_0_1,18,target_0,18},{old_1_0,18,0,0,target_1,18},{old_2_0,18,0,0,target_2,20}};
static void *(*allocate)(uptr,unsigned);
static void (*release)(void*);
static volatile unsigned outcomes[3],applied[3],last_result,total,seen;
static uptr engine_base;
static void (*original)(void*,unsigned,void*);
static int count(Vec *v,uptr stride,uptr max){if(!v->begin&&!v->end&&!v->cap)return 0;if(v->begin<65536||v->begin>v->end||v->end>v->cap||(v->end-v->begin)%stride||(v->cap-v->begin)>max*stride)return -1;return (v->end-v->begin)/stride;}
static int same(Vec *v,const u32 *ids,int n,int ordered){if(!ids||count(v,4,512)!=n)return 0;u32 *p=(u32*)v->begin;unsigned long mask=0;for(int i=0;i<n;i++){u32 id=p[i]>>14;if(ordered){if(id!=ids[i])return 0;}else{int found=0;for(int j=0;j<n;j++)if(id==ids[j]){if(mask&(1ul<<j))return 0;mask|=1ul<<j;found=1;break;}if(!found)return 0;}}return 1;}
static int fix_impl(void *root,uptr base){
 unsigned char *r=root;if(!root||*(uptr*)r!=base+0x98c3ff0)return 6;if(r[0xf0]&32)return 7;
 Vec *regions=(Vec*)(r+0x90);int nr=count(regions,32,16);if(nr<0)return 8;
 Vec *candidate[3]={0,0,0};int matches[3]={0,0,0},already[3]={0,0,0};u32 words[3][20]={{0}};
 for(int i=0;i<nr;i++){
  Vec *leagues=(Vec*)(regions->begin+i*32+8);int nl=count(leagues,40,128);if(nl<0)return 8;
  for(int j=0;j<nl;j++){
   Vec *teams=(Vec*)(leagues->begin+j*40+16);int nt=count(teams,4,512);if(nt<0)return 8;
   for(int k=0;k<3;k++){
    const Rule *rule=&rules[k];
    if(same(teams,rule->target,rule->n,1)){already[k]++;continue;}
    if(same(teams,rule->old,rule->nold,0)||same(teams,rule->previous,rule->nprevious,0)){candidate[k]=teams;matches[k]++;}
    for(int x=0;x<nt;x++)for(int y=0;y<rule->n;y++)if((((u32*)teams->begin)[x]>>14)==rule->target[y])words[k][y]=((u32*)teams->begin)[x];
   }
  }
 }
 u32 *buffers[3]={0,0,0};int changed=0;
 for(int k=0;k<3;k++){
  if(matches[k]>1){outcomes[k]=9;continue;}
  if(!candidate[k]){outcomes[k]=already[k]?2:5;continue;}
  const Rule *rule=&rules[k];
  for(int y=0;y<rule->n;y++)if(!words[k][y])words[k][y]=rule->target[y]<<14;
  /* Native builder 0x73814d4..0x73814f8 constructs exactly ID << 14. */
  if(candidate[k]->cap-candidate[k]->begin<(uptr)rule->n*4){
   if(!allocate||!release){outcomes[k]=10;continue;}
   buffers[k]=allocate(rule->n*4,0);if(!buffers[k]){outcomes[k]=10;continue;}
  }
  outcomes[k]=0;
 }
 for(int k=0;k<3;k++)if(candidate[k]&&!outcomes[k]){
  const Rule *rule=&rules[k];Vec *v=candidate[k];u32 *p=buffers[k]?buffers[k]:(u32*)v->begin;
  for(int y=0;y<rule->n;y++)p[y]=words[k][y];
  if(buffers[k]){uptr old=v->begin;v->begin=(uptr)p;v->end=(uptr)(p+rule->n);v->cap=v->end;release((void*)old);}else v->end=v->begin+rule->n*4;
  outcomes[k]=1;applied[k]++;changed=1;
 }
 return changed?1:2;
}
__attribute__((visibility("default"))) int fix(void *root,uptr base){return fix_impl(root,base);}
__attribute__((visibility("default"))) void configure(uptr base,uptr trampoline){engine_base=base;original=(void*)trampoline;allocate=(void*)(base+0x2f37644);release=(void*)(base+0x2f376d4);}
__attribute__((visibility("default"))) void set_allocator(uptr a,uptr f){allocate=(void*)a;release=(void*)f;}
__attribute__((visibility("default"))) void menu_hook(void *r,unsigned h,void *out){int result=fix_impl(r,engine_base);if(result!=6){last_result=result;seen++;if(result==1)total++;}original(r,h,out);}
__attribute__((visibility("default"))) unsigned status(unsigned which){return which==0?last_result:which==1?total:which==2?seen:which<6?outcomes[which-3]:which<9?applied[which-6]:0;}
__attribute__((visibility("default"))) void flush(void *start,uptr n){uptr ctr; __asm__ volatile("mrs %0, ctr_el0":"=r"(ctr)); uptr ds=4ul<<((ctr>>16)&15),is=4ul<<(ctr&15),end=(uptr)start+n; for(uptr p=(uptr)start&~(ds-1);p<end;p+=ds)__asm__ volatile("dc cvau, %0"::"r"(p):"memory"); __asm__ volatile("dsb ish":::"memory"); for(uptr p=(uptr)start&~(is-1);p<end;p+=is)__asm__ volatile("ic ivau, %0"::"r"(p):"memory"); __asm__ volatile("dsb ish; isb":::"memory");}
__attribute__((visibility("default"))) void store_instruction(void *p,u32 v){__atomic_store_n((u32*)p,v,__ATOMIC_RELEASE);}
