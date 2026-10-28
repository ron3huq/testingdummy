package org.efootballrevival.runtimeprobe;
import android.os.*;import android.view.View;import android.widget.*;import org.json.*;import java.util.*;import java.util.concurrent.*;
public final class CatalogFilter {
 private static final int TAG=0x7f0f7a70;
 private static final class Session implements View.OnAttachStateChangeListener {
  final Handler main=new Handler(Looper.getMainLooper());final ExecutorService worker=Executors.newSingleThreadExecutor(r->{Thread t=new Thread(r,"PlayerCatalogueSearch");t.setDaemon(true);return t;});volatile int generation;volatile boolean closed;Future<?> running;Runnable pending;JSONArray source;PlayerSearchIndex index;
  public void onViewAttachedToWindow(View v){}public void onViewDetachedFromWindow(View v){closed=true;generation++;if(pending!=null)main.removeCallbacks(pending);if(running!=null)running.cancel(true);worker.shutdownNow();}
 }
 public static void refresh(final ArrayList<JSONObject> visible,final EditText search,final JSONArray rows,final JSONArray positions,Spinner position,Spinner kind,ArrayList<String> kinds,Spinner sort,final BaseAdapter adapter,final TextView count){
  Session found=(Session)search.getTag(TAG);if(found!=null&&found.closed)return;if(found==null){found=new Session();search.setTag(TAG,found);search.addOnAttachStateChangeListener(found);}final Session s=found;
  final int generation=++s.generation;final String query=search.getText().toString();final int pos=position.getSelectedItemPosition()-1,order=sort.getSelectedItemPosition(),ki=kind.getSelectedItemPosition();final String type=ki>0&&ki<kinds.size()?kinds.get(ki):"";
  if(s.pending!=null)s.main.removeCallbacks(s.pending);if(s.running!=null)s.running.cancel(true);
  s.pending=()->{if(s.closed||s.generation!=generation)return;s.running=s.worker.submit(()->{try{
   java.util.function.BooleanSupplier cancelled=()->s.closed||s.generation!=generation||Thread.currentThread().isInterrupted();
   if(s.index==null||s.source!=rows){PlayerSearchIndex made=new PlayerSearchIndex(rows,positions,x->UiStrings.t(x),cancelled);if(cancelled.getAsBoolean())return;s.source=rows;s.index=made;}
   final ArrayList<JSONObject> matches=s.index.filter(query,pos,type,order,cancelled);s.main.post(()->{if(s.closed||s.generation!=generation)return;visible.clear();visible.addAll(matches);adapter.notifyDataSetChanged();count.setText(matches.isEmpty()?"No cards found. Try another name or ID.":"Showing "+matches.size()+" / "+rows.length()+" cards · Tap to add to warehouse");});
  }catch(CancellationException ignored){}catch(Exception ex){s.main.post(()->{if(!s.closed&&s.generation==generation)count.setText("Could not search players. Reopen the catalogue.");});}});};
  s.main.postDelayed(s.pending,120);
 }
}
