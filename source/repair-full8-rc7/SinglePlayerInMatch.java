package org.efootballrevival.runtimeprobe;
import android.app.*;
import android.view.*;
import android.widget.*;
import android.graphics.Rect;
import android.graphics.drawable.GradientDrawable;
import android.graphics.drawable.Drawable;
import android.util.TypedValue;
import org.json.*;
import java.lang.ref.WeakReference;
import java.util.WeakHashMap;

/** Ordinary in-app view; no system-overlay permission and no game-frame IO. */
public final class SinglePlayerInMatch {
 private static final WeakHashMap<Activity,WeakReference<Button>> attached=new WeakHashMap<>();
 private static final WeakHashMap<Button,Boolean> waiting=new WeakHashMap<>();
 private static final WeakHashMap<Button,Long> waitingSince=new WeakHashMap<>();
 private static int dp(Activity a,int n){return Math.round(n*a.getResources().getDisplayMetrics().density);}
 public static void attach(Activity a){
  if(!a.getClass().getName().equals("com.epicgames.ue4.GameActivity")||a.isFinishing())return;
  WeakReference<Button> old=attached.get(a);if(old!=null&&old.get()!=null)return;
  View decor=a.getWindow().getDecorView();if(!(decor instanceof ViewGroup))return;
  Button b=new Button(a);b.setTag("revival_single_player");b.setText("1P");b.setContentDescription("Single Player off: tap to choose, hold to change player");b.setTextSize(12);b.setSingleLine(true);b.setPadding(0,0,0,0);b.setAllCaps(false);b.setMinHeight(0);b.setMinimumHeight(0);b.setMinWidth(0);b.setMinimumWidth(0);b.setIncludeFontPadding(false);try{b.getClass().getMethod("setElevation",float.class).invoke(b,0f);b.getClass().getMethod("setStateListAnimator",Class.forName("android.animation.StateListAnimator")).invoke(b,new Object[]{null});}catch(Exception ignored){}b.setGravity(Gravity.CENTER);
  FrameLayout.LayoutParams lp=new FrameLayout.LayoutParams(dp(a,40),dp(a,40),Gravity.TOP|Gravity.LEFT);
  ((ViewGroup)decor).addView(b,lp);attached.put(a,new WeakReference<>(b));paint(a,b,0);decor.post(()->position(a,b));decor.addOnLayoutChangeListener((v,l,t,r,bb,ol,ot,or,ob)->{if(l!=ol||t!=ot||r!=or||bb!=ob)position(a,b);});poll(a,b);
  b.setOnClickListener(v->request(a,b,false));b.setOnLongClickListener(v->{request(a,b,true);return true;});
 }
 private static void paint(Activity a,Button b,int state){
  b.setText("1P");b.setTextColor(state==0?0xff252a2c:0xffffffff);GradientDrawable bg=new GradientDrawable();bg.setColor(state==1?0xe52dcb76:state==2?0xe5a86800:0xdde6e8e9);bg.setCornerRadius(dp(a,3));b.setBackground(bg);b.setSelected(state==1);b.setContentDescription("Single Player "+(state==1?"on":state==2?"pending":"off")+": tap to toggle, hold to choose a player");
 }
 private static View findAi(View v,View self){
  if(v==self)return null;CharSequence d=v.getContentDescription();String label=d==null?"":d.toString().trim().toLowerCase(java.util.Locale.ROOT);if(v instanceof TextView){String t=((TextView)v).getText().toString().trim().toLowerCase(java.util.Locale.ROOT);if(t.equals("ai")||t.equals("ai on")||t.equals("ai off"))return v;}if(label.equals("ai")||label.equals("ai control")||label.equals("ai mode")||label.equals("ai toggle"))return v;
  if(v instanceof ViewGroup)for(int i=0;i<((ViewGroup)v).getChildCount();i++){View hit=findAi(((ViewGroup)v).getChildAt(i),self);if(hit!=null&&hit.getVisibility()==View.VISIBLE)return hit;}return null;
 }
 private static void position(Activity a,Button b){
  View decor=a.getWindow().getDecorView();int w=decor.getWidth(),h=decor.getHeight();if(w==0||h==0)return;FrameLayout.LayoutParams p=(FrameLayout.LayoutParams)b.getLayoutParams();View ai=findAi(decor,b);int gap=Math.max(2,Math.round(h*.006f));
  // Some engine builds draw AI on the native surface. Match its HUD square in
  // viewport units; use exact measured bounds whenever Android exposes the view.
  int size=Math.round(h*.075f);p.width=size;p.height=size;p.leftMargin=Math.round(w*.785f)+gap;p.topMargin=Math.round(h*.012f);
  if(ai!=null&&ai.getWidth()>0&&ai.getHeight()>0){int[] origin=new int[2],anchor=new int[2];decor.getLocationOnScreen(origin);ai.getLocationOnScreen(anchor);p.width=ai.getWidth();p.height=ai.getHeight();p.leftMargin=anchor[0]-origin[0]+p.width+gap;p.topMargin=anchor[1]-origin[1];}
  Rect visible=new Rect();decor.getWindowVisibleDisplayFrame(visible);int[] origin=new int[2];decor.getLocationOnScreen(origin);p.leftMargin=Math.max(0,Math.min(p.leftMargin,w-p.width));p.topMargin=Math.max(p.topMargin,visible.top-origin[1]);b.setTextSize(TypedValue.COMPLEX_UNIT_PX,Math.min(p.width,p.height)*.32f);b.setLayoutParams(p);
 }
 private static void poll(Activity a,Button b){
  b.postDelayed(()->{if(a.isFinishing()||b.getWindowToken()==null)return;if(!a.hasWindowFocus()||!b.isEnabled()){poll(a,b);return;}
   new Thread(()->{try{JSONObject s=manage(a,"ui7_single_player_get",new JSONObject());boolean enabled=s.optBoolean("enabled"),active=s.optJSONObject("runtime")!=null&&s.optJSONObject("runtime").optInt("active")!=0;
    a.runOnUiThread(()->{if(!a.isFinishing()&&b.isEnabled()){paint(a,b,!enabled?0:active?1:2);if(Boolean.TRUE.equals(waiting.get(b))&&android.os.SystemClock.elapsedRealtime()-waitingSince.getOrDefault(b,0L)>3000){waiting.remove(b);waitingSince.remove(b);Toast.makeText(a,"Active team could not be read. Native status: "+(s.optJSONObject("runtime")==null?"unavailable":s.optJSONObject("runtime").optInt("reason_code")),Toast.LENGTH_LONG).show();}if(Boolean.TRUE.equals(waiting.get(b))){paint(a,b,2);}if(Boolean.TRUE.equals(waiting.get(b))&&s.optJSONObject("runtime")!=null&&s.optJSONObject("runtime").optInt("roster_count")>0){waiting.remove(b);request(a,b,true);}}});
   }catch(Exception ignored){}finally{a.runOnUiThread(()->poll(a,b));}},"SinglePlayerStatus").start();},200);
 }
 private static JSONObject manage(Activity a,String action,JSONObject req)throws Exception{return new JSONObject(EmbeddedGateway.manage(a,action,req.toString()));}
 private static void fail(Activity a,Button b,Exception e){a.runOnUiThread(()->{b.setEnabled(true);if(!a.isFinishing())Toast.makeText(a,e.getMessage(),Toast.LENGTH_LONG).show();});}
 private static void request(Activity a,Button b,boolean picker){
  if(Boolean.TRUE.equals(waiting.get(b))){waiting.remove(b);paint(a,b,0);return;}
  b.setEnabled(false);new Thread(()->{try{
   JSONObject status=manage(a,"ui7_single_player_get",new JSONObject());
   String id=status.optString("player_id","");
   if(!picker&&status.optBoolean("enabled")&&status.optJSONObject("runtime")!=null&&status.optJSONObject("runtime").optInt("active")!=0){apply(a,b,id,false);return;}
    JSONObject rows=manage(a,"ui7_single_player_search",new JSONObject().put("query","").put("page",0));
    a.runOnUiThread(()->{b.setEnabled(true);choose(a,b,rows.optJSONArray("players"));});
  }catch(Exception e){fail(a,b,e);}},"SinglePlayerInMatch").start();
 }
 private static void choose(Activity a,Button b,JSONArray rows){
  if(a.isFinishing())return;
  if(rows==null||rows.length()==0){waiting.put(b,true);waitingSince.put(b,android.os.SystemClock.elapsedRealtime());paint(a,b,2);Toast.makeText(a,"Live team is not available yet. Resume the match; tap to cancel selection.",Toast.LENGTH_LONG).show();return;}
  JSONArray pitch=new JSONArray();for(int i=0;i<rows.length();i++){JSONObject r=rows.optJSONObject(i);if(r!=null&&r.optBoolean("on_pitch"))pitch.put(r);}rows=pitch;
  if(rows.length()==0){choose(a,b,null);return;}
  String[] labels=new String[rows.length()],ids=new String[rows.length()];
  for(int i=0;i<rows.length();i++){JSONObject row=rows.optJSONObject(i);ids[i]=row.optString("id");labels[i]=(row.optBoolean("on_pitch")?"[XI] ":"[Bench] ")+row.optString("name")+" · "+ids[i];}
  new AlertDialog.Builder(a).setTitle("Single Player · Live team").setItems(labels,(dialog,i)->{b.setEnabled(false);new Thread(()->{try{apply(a,b,ids[i],true);}catch(Exception e){fail(a,b,e);}},"SinglePlayerChoose").start();}).setNegativeButton("Close",null).show();
 }
 private static void apply(Activity a,Button b,String id,boolean on)throws Exception{
  JSONObject result=manage(a,"ui7_single_player_live",new JSONObject().put("enabled",on).put("player_id",id));
  if(!result.optBoolean("saved"))throw new Exception(result.optString("error","Single Player was not applied"));
  a.runOnUiThread(()->{b.setEnabled(true);paint(a,b,on?2:0);Toast.makeText(a,on?"Single Player requested · waiting for native control":"Single Player disabled",Toast.LENGTH_SHORT).show();});
 }
}
