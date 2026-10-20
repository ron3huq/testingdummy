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
static const u32 old_3_0[]={244,338,245,242,256,352,116,346,250,251,243,344,351,117,247,255,118,345};
static const u32 target_3[]={18961,17873,5738,279,5741,4155,158,157,147,17733,1493,282,17734,22428,22498,5394,20478,16679};
#define RULE_COUNT 4
typedef struct {const u32 *old;int nold;const u32 *previous;int nprevious;const u32 *target;int n;} Rule;
static const Rule rules[]={{old_0_0,18,old_0_1,18,target_0,18},{old_1_0,18,0,0,target_1,18},{old_2_0,18,0,0,target_2,20},{old_3_0,18,0,0,target_3,18}};
static void *(*allocate)(uptr,unsigned);
static void (*release)(void*);
static volatile unsigned outcomes[RULE_COUNT],applied[RULE_COUNT],last_result,total,seen;
static uptr engine_base;
static void (*original)(void*,unsigned,void*);
static int count(Vec *v,uptr stride,uptr max){if(!v->begin&&!v->end&&!v->cap)return 0;if(v->begin<65536||v->begin>v->end||v->end>v->cap||(v->end-v->begin)%stride||(v->cap-v->begin)>max*stride)return -1;return (v->end-v->begin)/stride;}
static int same(Vec *v,const u32 *ids,int n,int ordered){if(!ids||count(v,4,512)!=n)return 0;u32 *p=(u32*)v->begin;unsigned long mask=0;for(int i=0;i<n;i++){u32 id=p[i]>>14;if(ordered){if(id!=ids[i])return 0;}else{int found=0;for(int j=0;j<n;j++)if(id==ids[j]){if(mask&(1ul<<j))return 0;mask|=1ul<<j;found=1;break;}if(!found)return 0;}}return 1;}
static int fix_impl(void *root,uptr base){
 unsigned char *r=root;if(!root||*(uptr*)r!=base+0x98c3ff0)return 6;if(r[0xf0]&32)return 7;
 Vec *regions=(Vec*)(r+0x90);int nr=count(regions,32,16);if(nr<0)return 8;
 Vec *candidate[RULE_COUNT]={0};int matches[3]={0,0,0},already[3]={0,0,0};u32 words[RULE_COUNT][20]={{0}};
 for(int i=0;i<nr;i++){
  Vec *leagues=(Vec*)(regions->begin+i*32+8);int nl=count(leagues,40,128);if(nl<0)return 8;
  for(int j=0;j<nl;j++){
   Vec *teams=(Vec*)(leagues->begin+j*40+16);int nt=count(teams,4,512);if(nt<0)return 8;
   for(int k=0;k<RULE_COUNT;k++){
    const Rule *rule=&rules[k];
    if(same(teams,rule->target,rule->n,1)){already[k]++;continue;}
    if(same(teams,rule->old,rule->nold,0)||same(teams,rule->previous,rule->nprevious,0)){candidate[k]=teams;matches[k]++;}
    for(int x=0;x<nt;x++)for(int y=0;y<rule->n;y++)if((((u32*)teams->begin)[x]>>14)==rule->target[y])words[k][y]=((u32*)teams->begin)[x];
   }
  }
 }
 u32 *buffers[RULE_COUNT]={0};int changed=0;
 for(int k=0;k<RULE_COUNT;k++){
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
 for(int k=0;k<RULE_COUNT;k++)if(candidate[k]&&!outcomes[k]){
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
__attribute__((visibility("default"))) unsigned status(unsigned which){return which==0?last_result:which==1?total:which==2?seen:which<3+RULE_COUNT?outcomes[which-3]:which<3+2*RULE_COUNT?applied[which-3-RULE_COUNT]:0;}
__attribute__((visibility("default"))) void flush(void *start,uptr n){uptr ctr; __asm__ volatile("mrs %0, ctr_el0":"=r"(ctr)); uptr ds=4ul<<((ctr>>16)&15),is=4ul<<(ctr&15),end=(uptr)start+n; for(uptr p=(uptr)start&~(ds-1);p<end;p+=ds)__asm__ volatile("dc cvau, %0"::"r"(p):"memory"); __asm__ volatile("dsb ish":::"memory"); for(uptr p=(uptr)start&~(is-1);p<end;p+=is)__asm__ volatile("ic ivau, %0"::"r"(p):"memory"); __asm__ volatile("dsb ish; isb":::"memory");}
__attribute__((visibility("default"))) void store_instruction(void *p,u32 v){__atomic_store_n((u32*)p,v,__ATOMIC_RELEASE);}

typedef struct {u32 pid,param,value;} Edit;
static const Edit base_edits[]={{110718,34,94},{110718,38,94},{110718,124,1},{110718,127,1},{110718,135,1},{110718,136,1},{132933,127,1},{47287,114,1},{47287,121,1},{47287,127,1},{162114,28,94},{162114,116,1},{162114,119,1},{162114,120,1},{162114,130,1},{110644,103,1},{110644,124,1},{133157,116,1},{133157,118,1},{133543,103,1},{133543,121,1},{133543,136,1},{4522,121,1},{4522,136,1},{129369,28,90},{129369,119,1},{129369,120,1},{7511,116,1},{7511,120,1},{128720,116,1},{110626,103,1},{110626,124,1},{132756,124,1},{132756,132,1},{119835,13,2}};
static const u32 roster_0[]={141038,165696,138183,110784,47787,110815,161548,133157,162114,110644,119835,40937,113596,126337,179719,147233,171610,147235,185601,110902,144438,108200,181382,179510,185595,103845,185594,108662,151604,164570};
static const u32 roster_1[]={122128,136098,104717,113960,132756,159320,135067,143844,152928,128720,110626,139898,170826,45993,152458,45089,108239,178137,157339,148172,159204,176673,116751,167737};
static const u32 roster_2[]={33185,116655,112376,129961,117766,109005,60380,138000,129369,119907,47287,122460,162163,60884,140870,144102,124107,176197,174911,173937,130207,175422};
static const u32 roster_3[]={63560,45993,111207,117991,43985,126517,117049,111804,40352,110644,121276,129510,43989,61214,151794,140200,106636,143567,127160,138488,132518,127787,130044,110394,135017,138662,117047};
static const u32 roster_4[]={61672,113284,146916,158649,114604,104745,168685,60928,106778,168892,142230,114672,147634,170548,170847,178136,112218,45393,174966,181500,143266,157353,139680,178410,38797,181419,146052,113969,182754,44849,113707,16906726};
static const u32 roster_5[]={16912943,16912944,16903935,16822506,16900351,16912601,16834520,16940451,16922498,16903552,16781738,16962472,16963981,16931595,16940446,16948403,16957006,16955430,16918387,16888946,16913997,16948402,16963980,16906937,16949891,16837662,16899797,16912948,16957007,16912950,16949892};
typedef struct {u32 team;const u32 *ids;u32 n;} NativeRoster;
static const NativeRoster native_rosters[]={{108,roster_0,30},{114,roster_1,24},{127,roster_2,22},{45,roster_3,27},{116,roster_4,32},{18961,roster_5,31}};
#define ROSTER_COUNT 6

/* Public player lookup takes a 16-byte typed key, NOT a coach uint16 ID.
 * 0x823c8d4 -> 0x823be04; 0x823cfd0 in v3 was a different record family.
 * Native player identity at +0x38 contains an XOR-protected raw ID. Decode
 * through the game's getter instead of comparing +0x40 with plaintext. */
typedef struct {uptr kind,id;} PlayerKey;
static void *(*original_team)(void*,u32);
static void *(*original_player)(void*,PlayerKey);
static PlayerKey (*player_key)(void*);
static int (*get_parameter)(void*,u32,u32*);
static int (*set_parameter)(void*,u32,u32);
static void *(*get_context)(void);
static volatile unsigned team_results[ROSTER_COUNT],player_applies,last_player_error,last_team_error,last_player_reason;
static int valid_player(void *p,u32 pid){
 if(!p){last_player_reason=1;return 0;}
 PlayerKey key=player_key(p);
 if((u32)key.kind!=0 || key.id!=pid){last_player_reason=2;return 0;}
 u32 pos=99,height=0;
 if(!get_parameter(p,0,&pos)||pos>12){last_player_reason=3;return 0;}
 if(!get_parameter(p,47,&height)||height<100||height>250){last_player_reason=4;return 0;}
 return 1;
}
static void apply_base(void *p,PlayerKey key){
 if((u32)key.kind!=0||key.id>0xfffffffful)return;u32 pid=key.id;
 int selected=0;for(unsigned i=0;i<sizeof(base_edits)/sizeof(Edit);i++)if(base_edits[i].pid==pid){selected=1;break;}if(!selected)return;
 if(!valid_player(p,pid)){last_player_error=pid;return;}
 for(unsigned i=0;i<sizeof(base_edits)/sizeof(Edit);i++)if(base_edits[i].pid==pid)set_parameter(p,base_edits[i].param,base_edits[i].value);
 player_applies++;
}
__attribute__((visibility("default"))) void *player_hook(void *db,PlayerKey key){void *p=original_player(db,key);apply_base(p,key);return p;}
static void apply_roster(void *db,void *p,u32 key){
 u32 tid=key>>14;int ix=-1;for(int i=0;i<ROSTER_COUNT;i++)if(native_rosters[i].team==tid){ix=i;break;}if(ix<0)return;
 if(!p||(*(u32*)p>>14)!=tid||!original_player){last_team_error=tid;team_results[ix]=11;return;}
 const NativeRoster *rule=&native_rosters[ix];unsigned char *b=p;u32 n=(*(u32*)(b+0x40c)>>9)&127;
 if(n>40 || (tid!=127&&n<11)){team_results[ix]=12;last_team_error=tid;return;}
 // Preflight ALL original player keys, including when a previously written roster matches.
 for(u32 i=0;i<rule->n;i++){PlayerKey k={0,rule->ids[i]};void *player=original_player(db,k);if(!valid_player(player,rule->ids[i])){team_results[ix]=13;last_player_error=rule->ids[i];last_team_error=tid;return;}}
 if(n==rule->n){int same=1;for(u32 i=0;i<n;i++)if(*(uptr*)(b+0x110+i*16)!=0||*(uptr*)(b+0x118+i*16)!=rule->ids[i]){same=0;break;}if(same){team_results[ix]=1;return;}}
 uptr old_keys[40][2];unsigned short old_numbers[40];
 for(u32 i=0;i<n;i++){old_keys[i][0]=*(uptr*)(b+0x110+i*16);old_keys[i][1]=*(uptr*)(b+0x118+i*16);old_numbers[i]=*(unsigned short*)(b+0x3a2+i*2);if((u32)old_keys[i][0]!=0){team_results[ix]=14;last_team_error=tid;return;}}
 for(u32 i=0;i<rule->n;i++){
  uptr kind=0;unsigned short number=i+1;
  for(u32 j=0;j<n;j++)if(old_keys[j][1]==rule->ids[i]){kind=old_keys[j][0];number=old_numbers[j];break;}
  *(uptr*)(b+0x110+i*16)=kind;*(uptr*)(b+0x118+i*16)=rule->ids[i];*(unsigned short*)(b+0x3a2+i*2)=number;
 }
 u32 flags=*(u32*)(b+0x40c);*(u32*)(b+0x40c)=(flags&~(127u<<9))|(rule->n<<9);
 team_results[ix]=1;
}
static void rename_ajax(void *p,u32 key){
 if(!p||(key>>14)!=116||(*(u32*)p>>14)!=116)return;
 unsigned char *b=p;
 if(b[4]=='A'&&b[5]=='j'&&b[6]=='a'&&b[7]=='x'&&(b[8]==0||(b[8]=='E'&&b[9]==0))){
  b[8]='E';b[9]=0;b[0x4a]='A';b[0x4b]='J';b[0x4c]='E';b[0x4d]=0;
 }
}
static void *team_impl(void *db,u32 key){void *p=original_team(db,key);apply_roster(db,p,key);rename_ajax(p,key);return p;}
__attribute__((visibility("default"))) void *team_hook(void *db,u32 key){return team_impl(db,key);}
__attribute__((visibility("default"))) void configure_team(uptr base,uptr trampoline){engine_base=base;original_team=(void*)trampoline;get_parameter=(void*)(base+0x82a84d4);set_parameter=(void*)(base+0x82a907c);get_context=(void*)(base+0x82468d4);player_key=(void*)(base+0x68fe720);}
__attribute__((visibility("default"))) void configure_player(uptr base,uptr trampoline){original_player=(void*)trampoline;}
__attribute__((visibility("default"))) unsigned ensure_team(u32 team){
 if(!original_team||!original_player)return 10;
 void *context=get_context();if(!context)return 10;void *db=*(void**)((char*)context+0x40);if(!db)return 10;
 team_impl(db,team<<14);
 for(int i=0;i<ROSTER_COUNT;i++)if(native_rosters[i].team==team)return team_results[i];return 1;
}
__attribute__((visibility("default"))) unsigned native_status(unsigned n){return n<ROSTER_COUNT?team_results[n]:n==ROSTER_COUNT?player_applies:n==ROSTER_COUNT+1?last_player_error:n==ROSTER_COUNT+2?last_team_error:n==ROSTER_COUNT+3?last_player_reason:0;}

/* C++ FString uses indirect result X8. A naked tail-call shim changes only
 * the plain emblem asset ID; it never creates or frees a C++ string. */
static uptr original_emblem __attribute__((used));
__attribute__((visibility("default"))) void configure_emblem(uptr base,uptr trampoline){(void)base;original_emblem=trampoline;}
__attribute__((naked,visibility("default"))) void emblem_hook(void){
 __asm__ volatile("cmp w0, #116\nmov w9, #181\ncsel w0, w9, w0, eq\nadrp x16, original_emblem\nldr x16, [x16, :lo12:original_emblem]\nbr x16");
}
