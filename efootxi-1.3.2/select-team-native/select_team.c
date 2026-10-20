/* efootxi 1.3.2 ARM64 ONLY. Memory patch; no CPK, DB, or save writes. */
typedef unsigned int u32;
typedef unsigned long uptr;
typedef struct { uptr begin,end,cap; } Vec;
static const u32 old_ids[18]={213,182,413,114,4211,4213,1329,420,218,212,180,414,403,181,112,217,221,113};
static const u32 new_ids[18]={101,102,103,114,100,173,179,108,109,172,121,119,120,181,112,125,327,130};
static int count(Vec *v,uptr stride,uptr max) {
 if(!v->begin && !v->end && !v->cap)return 0;
 if(v->begin<65536 || v->begin>v->end || v->end>v->cap || (v->end-v->begin)%stride || (v->cap-v->begin)>max*stride)return -1;
 return (int)((v->end-v->begin)/stride);
}
static int fix_impl(void *root,uptr base) {
 unsigned char *r=root;
 if(!root || *(uptr*)r!=base+0x98c3ff0)return 6;
 if(r[0xf0]&32)return 7;
 Vec *rv=(Vec*)(r+0x90);int nr=count(rv,32,16);
 if(nr<0)return 8;
 u32 found[18]={0},*candidate=0;int matches=0,already=0;
 for(int i=0;i<nr;i++) {
  Vec *lv=(Vec*)(rv->begin+i*32+8);int nl=count(lv,40,128);if(nl<0)return 8;
  for(int j=0;j<nl;j++) {
   Vec *tv=(Vec*)(lv->begin+j*40+16);int nt=count(tv,4,512);if(nt<0)return 8;
   u32 *p=(u32*)tv->begin;unsigned mask=0;int exactnew=nt==18;
   for(int k=0;k<nt;k++) {
    u32 word=p[k],id=word>>14;
    if(nt==18) {for(int z=0;z<18;z++)if(id==old_ids[z])mask|=1u<<z; if(id!=new_ids[k])exactnew=0;}
    for(int z=0;z<18;z++)if(id==new_ids[z]) {if(found[z] && found[z]!=word)return 4;found[z]=word;}
   }
   if(nt==18 && mask==((1u<<18)-1)){candidate=p;matches++;}
   if(exactnew)already++;
  }
 }
 if(matches==0)return already?2:5;
 if(matches!=1)return 9;
 for(int i=0;i<18;i++)if(!found[i])return 3;
 /* Full preflight succeeded. Reuse the existing allocation, keep packed low bits. */
 for(int i=0;i<18;i++)candidate[i]=found[i];
 return 1;
}
__attribute__((visibility("default"))) int fix(void *root,uptr base){return fix_impl(root,base);}
static uptr engine_base;
static void (*original)(void*,unsigned,void*);
static volatile unsigned last_result,applied,seen;
__attribute__((visibility("default"))) void configure(uptr base,uptr trampoline){engine_base=base;original=(void*)trampoline;}
__attribute__((visibility("default"))) void menu_hook(void *r,unsigned h,void *out){int result=fix_impl(r,engine_base);if(result!=6){last_result=result;seen++;if(result==1)applied++;}original(r,h,out);}
__attribute__((visibility("default"))) unsigned status(unsigned which){return which==0?last_result:which==1?applied:seen;}
__attribute__((visibility("default"))) void flush(void *start,uptr n){uptr ctr; __asm__ volatile("mrs %0, ctr_el0":"=r"(ctr)); uptr ds=4ul<<((ctr>>16)&15),is=4ul<<(ctr&15),end=(uptr)start+n; for(uptr p=(uptr)start&~(ds-1);p<end;p+=ds)__asm__ volatile("dc cvau, %0"::"r"(p):"memory"); __asm__ volatile("dsb ish":::"memory"); for(uptr p=(uptr)start&~(is-1);p<end;p+=is)__asm__ volatile("ic ivau, %0"::"r"(p):"memory"); __asm__ volatile("dsb ish; isb":::"memory");}
__attribute__((visibility("default"))) void store_instruction(void *p,u32 v){__atomic_store_n((u32*)p,v,__ATOMIC_RELEASE);}
