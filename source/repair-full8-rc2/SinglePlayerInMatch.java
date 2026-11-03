package org.efootballrevival.runtimeprobe;
import android.app.*;
import android.view.*;
import android.widget.*;
import org.json.*;
import java.lang.ref.WeakReference;
import java.util.WeakHashMap;

/** Ordinary in-app view; no system-overlay permission and no game-frame IO. */
public final class SinglePlayerInMatch {
 private static final WeakHashMap<Activity,WeakReference<Button>> attached=new WeakHashMap<>();
 private static int dp(Activity a,int n){return Math.round(n*a.getResources().getDisplayMetrics().density);}
 public static void attach(Activity a){
  if(!a.getClass().getName().equals("com.epicgames.ue4.GameActivity")||a.isFinishing())return;
  WeakReference<Button> old=attached.get(a);if(old!=null&&old.get()!=null)return;
  View decor=a.getWindow().getDecorView();if(!(decor instanceof ViewGroup))return;
  Button b=new Button(a);b.setText("1P");b.setContentDescription("Single Player: tap to toggle, hold to choose a player");b.setTextSize(12);b.setAllCaps(false);b.setAlpha(.85f);
  FrameLayout.LayoutParams lp=new FrameLayout.LayoutParams(dp(a,58),dp(a,42),Gravity.TOP|Gravity.RIGHT);lp.topMargin=dp(a,10);lp.rightMargin=dp(a,110);
  ((ViewGroup)decor).addView(b,lp);attached.put(a,new WeakReference<>(b));
  b.setOnClickListener(v->request(a,b,false));b.setOnLongClickListener(v->{request(a,b,true);return true;});
 }
 private static JSONObject manage(Activity a,String action,JSONObject req)throws Exception{return new JSONObject(EmbeddedGateway.manage(a,action,req.toString()));}
 private static void fail(Activity a,Button b,Exception e){a.runOnUiThread(()->{b.setEnabled(true);if(!a.isFinishing())Toast.makeText(a,e.getMessage(),Toast.LENGTH_LONG).show();});}
 private static void request(Activity a,Button b,boolean picker){
  b.setEnabled(false);new Thread(()->{try{
   JSONObject status=manage(a,"ui7_single_player_get",new JSONObject());
   String id=status.optString("player_id","");
   if(picker||id.isEmpty()||id.equals("null")||!status.optBoolean("known")){
    JSONObject rows=manage(a,"ui7_single_player_search",new JSONObject().put("query","").put("page",0));
    a.runOnUiThread(()->{b.setEnabled(true);choose(a,b,rows.optJSONArray("players"));});
   }else apply(a,b,id,!status.optBoolean("enabled"));
  }catch(Exception e){fail(a,b,e);}},"SinglePlayerInMatch").start();
 }
 private static void choose(Activity a,Button b,JSONArray rows){
  if(a.isFinishing())return;
  if(rows==null||rows.length()==0){Toast.makeText(a,"Your current squad is unavailable",Toast.LENGTH_LONG).show();return;}
  String[] labels=new String[rows.length()],ids=new String[rows.length()];
  for(int i=0;i<rows.length();i++){JSONObject row=rows.optJSONObject(i);ids[i]=row.optString("id");labels[i]=row.optString("name")+" · "+ids[i];}
  new AlertDialog.Builder(a).setTitle("Single Player · Current squad").setItems(labels,(dialog,i)->{b.setEnabled(false);new Thread(()->{try{apply(a,b,ids[i],true);}catch(Exception e){fail(a,b,e);}},"SinglePlayerChoose").start();}).setNegativeButton("Close",null).show();
 }
 private static void apply(Activity a,Button b,String id,boolean on)throws Exception{
  JSONObject result=manage(a,"ui7_single_player_live",new JSONObject().put("enabled",on).put("player_id",id));
  if(!result.optBoolean("saved"))throw new Exception(result.optString("error","Single Player was not applied"));
  a.runOnUiThread(()->{b.setEnabled(true);b.setText(on?"1P ON":"1P OFF");b.setSelected(on);Toast.makeText(a,on?"Single Player enabled · hold 1P to choose":"Native control restored",Toast.LENGTH_SHORT).show();});
 }
}
