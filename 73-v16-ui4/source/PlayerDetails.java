package org.efootballrevival.runtimeprobe;
import android.app.*;import android.content.*;import android.widget.*;import android.view.*;import android.text.InputType;import org.json.*;
public final class PlayerDetails {
 private static JSONObject selected;private static boolean armed;
 public static void select(JSONObject p){selected=p;armed=true;}
 public static void builder(AlertDialog.Builder b){if(armed&&selected!=null){armed=false;b.setNeutralButton("Height / skills",null);}}
 public static void decorate(final Activity a,AlertDialog d){Button b=d.getButton(-3);if(b!=null&&"Height / skills".contentEquals(b.getText())){final JSONObject p=selected;b.setOnClickListener(v->open(a,p));}}
 private static String manage(Activity a,String action,JSONObject p)throws Exception{return(String)Class.forName("org.efootballrevival.runtimeprobe.EmbeddedGateway").getMethod("manage",Context.class,String.class,String.class).invoke(null,a,action,p.toString());}
 private static void error(Activity a,Exception e){new AlertDialog.Builder(a).setTitle("Could not save").setMessage(String.valueOf(e.getCause()!=null?e.getCause().getMessage():e.getMessage())).setPositiveButton("Close",null).show();}
 private static EditText number(Activity a,LinearLayout col,String label,int value){TextView text=new TextView(a);text.setText(label);col.addView(text);EditText e=new EditText(a);e.setInputType(InputType.TYPE_CLASS_NUMBER);e.setText(String.valueOf(value));col.addView(e);return e;}
 public static void open(final Activity a,final JSONObject p){if(p==null)return;new Thread(()->{try{final JSONObject data=new JSONObject(manage(a,"ui4_details_get",p));a.runOnUiThread(()->{try{form(a,p,data);}catch(Exception e){error(a,e);}});}catch(Exception e){a.runOnUiThread(()->error(a,e));}},"PlayerDetailsLoad").start();}
 private static void form(final Activity a,final JSONObject p,JSONObject data)throws Exception{
  ScrollView scroll=new ScrollView(a);LinearLayout col=new LinearLayout(a);col.setOrientation(1);int pad=(int)(18*a.getResources().getDisplayMetrics().density);col.setPadding(pad,pad,pad,pad);scroll.addView(col);
  final EditText height=number(a,col,"Height (140–220 cm)",data.getInt("height"));final EditText weight=number(a,col,"Weight (40–130 kg)",data.getInt("weight"));
  TextView note=new TextView(a);note.setText("Built-in skills: untick to remove, tick another to replace. Additional skills remain available in their existing five-slot editor. Save before entering the game.");col.addView(note);
  final JSONArray skills=data.getJSONArray("skills"),chosen=data.getJSONArray("selected");final CheckBox[] boxes=new CheckBox[skills.length()];
  for(int i=0;i<boxes.length;i++){JSONObject skill=skills.getJSONObject(i);CheckBox b=new CheckBox(a);b.setText(skill.getString("label"));for(int j=0;j<chosen.length();j++)if(chosen.getInt(j)==skill.getInt("id"))b.setChecked(true);col.addView(b);boxes[i]=b;}
  final AlertDialog d=new AlertDialog.Builder(a).setTitle("Height, weight & built-in skills").setView(scroll).setNegativeButton("Cancel",null).setPositiveButton("Save",null).create();d.show();d.getButton(-1).setOnClickListener(v->{try{JSONObject req=new JSONObject(p.toString());req.put("height",Integer.parseInt(height.getText().toString()));req.put("weight",Integer.parseInt(weight.getText().toString()));JSONArray ids=new JSONArray();for(int i=0;i<boxes.length;i++)if(boxes[i].isChecked())ids.put(skills.getJSONObject(i).getInt("id"));req.put("skills",ids);d.getButton(-1).setEnabled(false);new Thread(()->{try{manage(a,"ui4_details_apply",req);a.runOnUiThread(()->{d.dismiss();Toast.makeText(a,"Saved. Reopen the player to verify.",Toast.LENGTH_LONG).show();});}catch(Exception e){a.runOnUiThread(()->{d.getButton(-1).setEnabled(true);error(a,e);});}},"PlayerDetailsSave").start();}catch(Exception e){error(a,e);}});
 }
}
