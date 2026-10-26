static struct{uptr thread;u32 depth;}skill_pages[16];static volatile unsigned char skill_page_lock;static volatile u32 skill_page_active_count;
static uptr skill_thread(void){uptr value;__asm__ volatile("mrs %0,tpidr_el0":"=r"(value));return value;}
static int in_custom_skill_page(void){if(!__atomic_load_n(&skill_page_active_count,__ATOMIC_ACQUIRE))return 0;int yes=0;while(__atomic_test_and_set(&skill_page_lock,__ATOMIC_ACQUIRE)){}uptr thread=skill_thread();for(u32 i=0;i<16;i++)if(skill_pages[i].thread==thread&&skill_pages[i].depth)yes=1;__atomic_clear(&skill_page_lock,__ATOMIC_RELEASE);return yes;}
static void(*original_skill_page)(void*,uptr);
__attribute__((visibility("default"))) void configure_skill_page(uptr base,uptr fn){engine_base=base;original_skill_page=(void*)fn;}
__attribute__((visibility("default"))) void skill_page_hook(void*widget,uptr id){
 int slot=-1;if(id==89136418985303ULL||id==89136418985302ULL){
  while(__atomic_test_and_set(&skill_page_lock,__ATOMIC_ACQUIRE)){}uptr thread=skill_thread();
  for(u32 i=0;i<16;i++)if(skill_pages[i].thread==thread){slot=i;break;}
  if(slot<0)for(u32 i=0;i<16;i++)if(!skill_pages[i].thread){slot=i;break;}
  if(slot>=0){skill_pages[slot].thread=thread;skill_pages[slot].depth++;__atomic_fetch_add(&skill_page_active_count,1,__ATOMIC_RELEASE);}__atomic_clear(&skill_page_lock,__ATOMIC_RELEASE);
 }
 original_skill_page(widget,id);
 if(slot>=0){while(__atomic_test_and_set(&skill_page_lock,__ATOMIC_ACQUIRE)){}__atomic_fetch_sub(&skill_page_active_count,1,__ATOMIC_RELEASE);if(!--skill_pages[slot].depth)skill_pages[slot].thread=0;__atomic_clear(&skill_page_lock,__ATOMIC_RELEASE);}
}
/* Empty skill labels only.74 native IDs use the engine's parameter-to-message table. */
static const struct{u32 message;const char*label;} skill_messages[]={{23068750,"Scissors Feint"},{23068775,"Double Touch"},{23068716,"Flip Flap"},{23068751,"Marseille Turn"},{23068752,"Sombrero"},{23068776,"Chop Turn"},{23068766,"Cut Behind & Turn"},{23068767,"Scotch Move"},{23068816,"Tap Fake"},{23068817,"Spring Cut"},{23068777,"Sole Control"},{23068797,"Momentum Dribbling"},{23068804,"Accel Burst"},{23068810,"Magnetic Feet"},{23068769,"Heading"},{23068803,"Bullet Header"},{23068733,"Long-range Curler"},{23068801,"Blitz Curler"},{23068778,"Chip Shot Control"},{23068738,"Knuckle Shot"},{23068779,"Dipping Shot"},{23068780,"Rising Shot"},{23068786,"Long-range Shooting"},{23068808,"Low Screamer"},{23068813,"Snap Strike"},{23068754,"Acrobatic Finishing"},{23068770,"Heel Trick"},{23068755,"First-time Shot"},{23068792,"Improviser"},{23068809,"Willpower"},{23068756,"Direct Pass"},{23068787,"Through Pass"},{23068757,"Weighted Pass"},{23068758,"Pin Point Cross"},{23068800,"Blitz Crossing"},{23068759,"Out Side Long"},{23068771,"Rabona"},{23068781,"No Look Pass"},{23068798,"Game-changing Pass"},{23068799,"Visionary Pass"},{23068802,"Phenomenal Pass"},{23068772,"Low Lofted Pass"},{23068760,"GK Low Punt"},{23068782,"GK High Punt"},{2424859,"Longthrow"},{23068747,"Gk Long Throw"},{23068783,"Penalty Specialist"},{23068784,"Pk Stopper"},{23068807,"GK Directing Defence"},{74973340,"GK Spirit Roar"},{23068773,"Malicia"},{23068706,"Man Marking"},{23068735,"Chasing"},{23068785,"Intercept"},{23068789,"Blocker"},{2359430,"Aerial Superiority"},{23068790,"Sliding Tackle"},{23068806,"Long-reach Tackle"},{23068818,"Power Tackle"},{23068793,"Fortress"},{23068774,"Acrobatic Clearance"},{23068805,"Df Sky High"},{23068814,"Shadow Hunt"},{23068761,"Captaincy"},{23068812,"Attack Trigger"},{23068720,"Super Sub"},{23068768,"Fighting Spirit"},{23068815,"Attacking Surge"}};
static int(*original_skill_text)(void*,u32);static volatile u32 skill_text_fallbacks;
__attribute__((visibility("default"))) void configure_skill_text(uptr base,uptr fn){engine_base=base;original_skill_text=(void*)fn;}
__attribute__((visibility("default"))) int skill_text_hook(void*out,u32 msg){
 int result=original_skill_text(out,msg);if(!out)return result;unsigned char*b=out;
 uptr size=(b[0]&1)?*((uptr*)b+1):(b[0]>>1);if(size&&!in_custom_skill_page())return result;
 const char*label=0;for(u32 i=0;i<sizeof(skill_messages)/sizeof(*skill_messages);i++)if(skill_messages[i].message==msg){label=skill_messages[i].label;break;}
 if(!label)return result;u32 n=0;while(label[n]&&n<22)n++;if(label[n])return result;
 if(b[0]&1){void*ptr=*((void**)b+2);if(ptr)((void(*)(void*))(engine_base+0x2f376d4))(ptr);}
 for(u32 i=0;i<24;i++)b[i]=0;b[0]=(unsigned char)(n*2);for(u32 i=0;i<n;i++)b[i+1]=label[i];
 __atomic_fetch_add(&skill_text_fallbacks,1,__ATOMIC_RELAXED);return 1;
}
__attribute__((visibility("default"))) u32 skill_text_status(void){return skill_text_fallbacks;}
