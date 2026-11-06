/* Experimental aggregate input adapter, NOT installed in any release.
 * Caller must verify engine identity and install the original trampoline.
 * This does NOT establish the extra-time/penalty end-of-match control path.
 */
typedef unsigned W;typedef unsigned long U;typedef unsigned short H;typedef unsigned char B;
#define EX __attribute__((visibility("default")))
static U engine,previous,game,bound_source;static W home,away,carry_home,carry_away,aggregate,armed,busy;static U applies,rejected;
static void lock(void){while(__atomic_exchange_n(&busy,1,__ATOMIC_ACQUIRE)){} }
static void unlock(void){__atomic_store_n(&busy,0,__ATOMIC_RELEASE);}
EX W ucl_rules_bind(U base,U trampoline){if(!base||!trampoline)return 0;lock();if(armed){unlock();return 0;}engine=base;__atomic_store_n(&previous,trampoline,__ATOMIC_RELEASE);unlock();return 1;}
EX W ucl_rules_arm(U key,W h,W a,W ch,W ca,W use_aggregate){
 if(!key||!h||!a||h==a||h>262143||a>262143||ch>99||ca>99||use_aggregate>1||(!use_aggregate&&(ch||ca)))return 0;
 lock();if(!engine||!previous||(armed&&game!=key)){unlock();return 0;}
 if(armed){W same=home==h&&away==a&&carry_home==ch&&carry_away==ca&&aggregate==use_aggregate;unlock();return same;}
 game=key;home=h;away=a;carry_home=ch;carry_away=ca;aggregate=use_aggregate;bound_source=0;armed=1;unlock();return 1;
}
EX W ucl_rules_clear(U key){lock();if(armed&&game!=key){unlock();return 0;}armed=0;game=0;bound_source=0;unlock();return 1;}
EX U ucl_rule_hook(void*out,void*source){
 U original=__atomic_load_n(&previous,__ATOMIC_ACQUIRE);if(!original)return 0;
 U result=((U(*)(void*,void*))original)(out,source);
 if(!out||!source)return result;
 lock();if(!armed){unlock();return result;}
 if(bound_source&&bound_source!=(U)source){rejected++;unlock();return result;}
 /* Team identity getter in the fingerprinted engine. It reads MatchData,
  * unlike the actor index or cache key. Accept either physical field order. */
 W h=((W(*)(void*,W))(engine+0x72ebecc))(source,0);
 W a=((W(*)(void*,W))(engine+0x72ebecc))(source,1);
 W ch,ca;
 if(h==home&&a==away){ch=carry_home;ca=carry_away;}
 else if(h==away&&a==home){ch=carry_away;ca=carry_home;}
 else{rejected++;unlock();return result;}
 bound_source=(U)source;B*b=out;b[0x12a]=(B)aggregate;*(H*)(b+0x12c)=(H)ch;*(H*)(b+0x12e)=(H)ca;
 b[0x135]=0;b[0x136]=0;applies++;unlock();return result;
}
EX U ucl_rules_status(W index){lock();U value=index==0?armed:index==1?game:index==2?applies:index==3?rejected:index==4?bound_source:0;unlock();return value;}
