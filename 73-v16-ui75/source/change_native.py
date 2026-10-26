from pathlib import Path
p=Path('/workspace/ronaldo-work/73-ui75/native/select_team.c');s=p.read_text()
# The native recipe path gate reads bit2 at Team+3fd; palettes alone cannot change it.
s=s.replace('for(unsigned i=0;i<80;i++)a[i]=b[i];}', '''for(unsigned i=0;i<80;i++)a[i]=b[i];
 if(tid==1706||tid==4937||tid==1957||tid==1956||tid==4962||tid==4964||tid==4938||tid==1950||tid==1228||tid==1955){unsigned char*t=p,*d=donor;t[0x3fd]=(t[0x3fd]&~4u)|(d[0x3fd]&4u);}
}''')
# Include original donors for retro palette resources, but leave approved Y17 behavior unchanged.
# Cached My League records must receive the same kit gate and palette fix as DB lookup.
s=s.replace('if(kit_visual_donor(tid)!=tid){unsigned char*ctx=get_context();', 'if(kit_visual_donor(tid)!=tid||((cid==473)&&(tid==1706||tid==4937||tid==1957||tid==1956||tid==4962||tid==4964||tid==4938||tid==1950||tid==1228||tid==1955))){unsigned char*ctx=get_context();')
anchor='static u32 (*original_appearance_serialize)'
at=s.index(anchor)
code='''/* Eleven verified body fields. Values0..14 map to native(-1..1),
   15 means inherit. Exact64 card scope, per-thread stack: no source record edits. */
#define MODEL_ROWS 1024
static struct {uptr id;unsigned char fields[11];} model_rows[MODEL_ROWS];
static u32 model_count;static volatile u32 model_ready,model_applies,model_scopes_failed;
static const unsigned char model_nibble[11]={7,3,0,4,1,2,10,8,5,6,9};
static volatile unsigned char model_lock;
static struct {uptr thread;u32 depth;uptr ids[8];} model_scopes[32];
static uptr model_tid(void){register uptr x8 __asm__("x8")=178;register uptr x0 __asm__("x0");__asm__ volatile("svc #0":"=r"(x0):"r"(x8):"memory");return x0;}
static void model_take(void){while(__atomic_test_and_set(&model_lock,__ATOMIC_ACQUIRE)){} }
static void model_drop(void){__atomic_clear(&model_lock,__ATOMIC_RELEASE);}
__attribute__((visibility("default"))) u32 model_add(uptr id,uptr packed){if(model_ready||!id||model_count>=MODEL_ROWS)return 0;for(u32 i=0;i<model_count;i++)if(model_rows[i].id==id)return 0;u32 at=model_count++;model_rows[at].id=id;for(u32 i=0;i<11;i++)model_rows[at].fields[i]=(packed>>(i*4))&15;return 1;}
__attribute__((visibility("default"))) void model_commit(void){__atomic_store_n(&model_ready,1,__ATOMIC_RELEASE);}
__attribute__((visibility("default"))) uptr model_status(u32 ix){return ix==0?model_ready:ix==1?model_count:ix==2?model_applies:model_scopes_failed;}
static u32 model_begin(uptr id){if(!model_ready||!model_count)return 0;uptr thread=model_tid();model_take();int n=-1;for(u32 i=0;i<32;i++)if(model_scopes[i].thread==thread){n=i;break;}if(n<0)for(u32 i=0;i<32;i++)if(!model_scopes[i].thread){n=i;break;}if(n<0||model_scopes[n].depth>=8){model_scopes_failed++;model_drop();return 0;}model_scopes[n].thread=thread;model_scopes[n].ids[model_scopes[n].depth++]=id;model_drop();return n+1;}
static void model_end(u32 token){if(!token)return;uptr thread=model_tid();model_take();u32 n=token-1;if(n<32&&model_scopes[n].thread==thread&&model_scopes[n].depth){if(!--model_scopes[n].depth)model_scopes[n].thread=0;}model_drop();}
static uptr model_card(void){uptr id=0,thread=model_tid();model_take();for(u32 i=0;i<32;i++)if(model_scopes[i].thread==thread&&model_scopes[i].depth){id=model_scopes[i].ids[model_scopes[i].depth-1];break;}model_drop();return id;}
__attribute__((visibility("default"))) u32 model_patch(void*out,uptr id){if(!out||!__atomic_load_n(&model_ready,__ATOMIC_ACQUIRE))return 0;for(u32 i=0;i<model_count;i++)if(model_rows[i].id==id){unsigned char*b=out;for(u32 k=0;k<11;k++){u32 v=model_rows[i].fields[k],n=model_nibble[k];if(v<15){u32 shift=(n&1)*4;b[n/2]=(b[n/2]&~(15u<<shift))|(v<<shift);}}__atomic_fetch_add(&model_applies,1,__ATOMIC_RELAXED);return 1;}return 0;}
'''
s=s[:at]+code+s[at:]
s=s.replace('u32 ok=original_appearance_serialize(record,out);','u32 ok=original_appearance_serialize(record,out);\n if(ok&&out&&model_count){uptr card=model_card();if(card)model_patch(out,card);}')
s=s.replace(' original_appearance_build(out,spec);',' u32 model_token=model_begin(id);\n original_appearance_build(out,spec);\n model_end(model_token);')
p.write_text(s)
