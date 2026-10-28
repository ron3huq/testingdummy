/* New cut-long mode only; the original long mesh and selection remain untouched. */
#include "cut-models.h"
static uptr cut_cards[1024];static u32 cut_count;static volatile u32 cut_ready,cut_applies,cut_unsupported;static volatile uptr cut_last_id;
static void(*cut_detail_original)(void*,u32,u32,u32,u32,u32),(*cut_common_original)(void*,u32,u32,u32,u32,u32);
static u32(*cut_begin)(void*);static void(*cut_end)(u32);
__attribute__((visibility("default")))u32 editor_cut_add(uptr id){if(cut_ready||!id||cut_count>=1024)return 0;for(u32 i=0;i<cut_count;i++)if(cut_cards[i]==id)return 0;cut_cards[cut_count++]=id;return 1;}
__attribute__((visibility("default")))void editor_cut_commit(void){__atomic_store_n(&cut_ready,1,__ATOMIC_RELEASE);}
__attribute__((visibility("default")))uptr editor_cut_status(u32 i){return i==0?cut_ready:i==1?cut_count:i==2?cut_applies:i==3?cut_unsupported:cut_last_id;}
__attribute__((visibility("default")))void configure_cut_scope(uptr begin,uptr end){cut_begin=(void*)begin;cut_end=(void*)end;}
__attribute__((visibility("default")))void configure_cut_detail(uptr base,uptr original){(void)base;cut_detail_original=(void*)original;}
__attribute__((visibility("default")))void configure_cut_common(uptr base,uptr original){(void)base;cut_common_original=(void*)original;}
static u32 cut_token(void*actor,u32 model,u32 variant,u32 mode){if(!actor||!cut_ready||!cut_begin||!cut_end)return 0;uptr id=*(uptr*)((char*)actor+0x10b0);int yes=0;for(u32 i=0;i<cut_count;i++)if(cut_cards[i]==id)yes=1;if(!yes)return 0;for(u32 i=0;i<sizeof(cut_models)/sizeof(*cut_models);i++)if(cut_models[i][0]==model&&cut_models[i][1]==variant){u32 token=cut_begin(actor);if(token){cut_applies++;cut_last_id=id;}return token;}cut_unsupported++;return 0;}
__attribute__((visibility("default")))void cut_detail_hook(void*actor,u32 model,u32 sleeve,u32 variant,u32 mode,u32 flag){u32 token=cut_token(actor,model,variant,mode);if(cut_detail_original)cut_detail_original(actor,model,token?1:sleeve,variant,mode,flag);if(token)cut_end(token);}
__attribute__((visibility("default")))void cut_common_hook(void*actor,u32 model,u32 sleeve,u32 variant,u32 mode,u32 flag){u32 token=cut_token(actor,model,variant,mode);if(cut_common_original)cut_common_original(actor,model,token?1:sleeve,variant,mode,flag);if(token)cut_end(token);}
