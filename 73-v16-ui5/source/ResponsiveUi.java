package org.efootballrevival.runtimeprobe;
import android.app.*;import android.graphics.Rect;import android.view.*;import android.widget.*;
public final class ResponsiveUi {
 public static void fit(final Activity activity,final AlertDialog dialog){
  final Window window=dialog.getWindow();if(window==null)return;
  window.setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_ADJUST_RESIZE);
  final View decor=window.getDecorView();decor.post(()->{
   Rect bounds=new Rect();activity.getWindow().getDecorView().getWindowVisibleDisplayFrame(bounds);
   float density=activity.getResources().getDisplayMetrics().density;
   int width=Math.min((int)(560*density),Math.max(1,bounds.width()-(int)(24*density)));
   int height=Math.max((int)(180*density),bounds.height()-(int)(24*density));
   int contentLimit=Math.max((int)(96*density),height-(int)(144*density));
   View custom=dialog.findViewById(android.R.id.custom);
   if(custom!=null){ViewGroup.LayoutParams lp=custom.getLayoutParams();if(lp!=null){lp.height=contentLimit;custom.setLayoutParams(lp);}custom.setMinimumWidth(0);}
   for(int id:new int[]{-1,-2,-3}){Button b=dialog.getButton(id);if(b!=null){b.setAllCaps(false);b.setSingleLine(false);b.setTextSize(12);b.setMinWidth(0);b.setMinimumWidth(0);b.setMinHeight((int)(44*density));b.setPadding((int)(8*density),0,(int)(8*density),0);}}
   window.setLayout(width,WindowManager.LayoutParams.WRAP_CONTENT);
  });
 }
}
