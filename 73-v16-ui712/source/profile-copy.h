/* Immutable per-card body/motion donor profiles. No ID/face/ability substitution. */
static struct {uptr target,donor;} copy_rows[1024];static u32 copy_n;static volatile u32 copy_ready,copy_applies,copy_failures;
__attribute__((visibility("default")))u32 editor_copy_add(uptr target,uptr donor){if(copy_ready||!target||!donor||target==donor||copy_n>=1024)return 0;for(u32 i=0;i<copy_n;i++)if(copy_rows[i].target==target)return 0;copy_rows[copy_n].target=target;copy_rows[copy_n++].donor=donor;return 1;}
__attribute__((visibility("default")))void editor_copy_commit(void){__atomic_store_n(&copy_ready,1,__ATOMIC_RELEASE);}
__attribute__((visibility("default")))uptr editor_copy_status(u32 i){return i==0?copy_ready:i==1?copy_n:i==2?copy_applies:copy_failures;}
static void editor_copy_apply(void*p,uptr id){
 if(!p||!copy_ready||!get_context||!original_player||!get_parameter||!set_parameter)return;
 for(u32 i=0;i<copy_n;i++)if(copy_rows[i].target==id){
  unsigned char*ctx=get_context();void*db=ctx?*(void**)(ctx+0x40):0;if(!db){copy_failures++;return;}
  uptr chain[16];u32 depth=1;chain[0]=copy_rows[i].donor;for(;;){uptr next=0;for(u32 z=0;z<copy_n;z++)if(copy_rows[z].target==chain[depth-1])next=copy_rows[z].donor;if(!next)break;if(depth>=16){copy_failures++;return;}for(u32 z=0;z<depth;z++)if(chain[z]==next){copy_failures++;return;}chain[depth++]=next;}PlayerKey key={0,chain[depth-1]};void*source=original_player(db,key);if(!valid_player(source,key.id)){copy_failures++;return;}
  /* Existing native getter supplies the donor's actual parameters; no guessed presets. */
  static const u32 fields[]={43,47,48,50,51,52,53,54,55,56,57,58,59,60,63,64,65,66,67,68,69};u32 values[21];
  for(u32 k=0;k<21;k++)if(!get_parameter(source,fields[k],&values[k])){copy_failures++;return;}
  u32 cid=__atomic_load_n(&active_competition,__ATOMIC_ACQUIRE);for(u32 z=depth;z>0;z--)for(u32 pass=0;pass<2;pass++)for(u32 j=0;j<editor_np;j++){EditorPlayer*r=&editor_players[j];if(r->id==chain[z-1]&&editor_player_scope(r,cid)&&((!pass&&!r->cid)||(pass&&cid&&r->cid==cid)))for(u32 k=0;k<21;k++)if(r->present[fields[k]])values[k]=r->value[fields[k]];}
  for(u32 k=0;k<21;k++)if(!set_parameter(p,fields[k],values[k])){copy_failures++;return;}
  copy_applies++;return;
 }
}
