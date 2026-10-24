from pathlib import Path
R=Path('/workspace/ronaldo-work/73-ui/smali/org/efootballrevival/runtimeprobe');p=R/'GatewayBootActivity.smali';s=p.read_text();C='Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;'
s=s.replace('# instance fields','# instance fields\n.field private idleLast:J\n.field private idleTouch:Z\n.field private idleRun:Ljava/lang/Runnable;')
for name,call in [('onResume','idleArm'),('onPause','idleStop')]:
 start=s.index('.method protected '+name+'()V');end=s.index('.end method',start);chunk=s[start:end];chunk=chunk.replace('    return-void',f'    invoke-direct {{p0}}, {C}->{call}()V\n    return-void');s=s[:start]+chunk+s[end:]
s+='''
.method private idleStop()V
 .registers 3
 iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->idleRun:Ljava/lang/Runnable;
 if-eqz v0, :done
 iget-object v1, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->noticeHandler:Landroid/os/Handler;
 invoke-virtual {v1,v0}, Landroid/os/Handler;->removeCallbacks(Ljava/lang/Runnable;)V
 :done
 return-void
.end method
.method private idleArm()V
 .registers 4
 invoke-direct {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->idleStop()V
 invoke-static {}, Landroid/os/SystemClock;->elapsedRealtime()J
 move-result-wide v0
 iput-wide v0,p0,Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->idleLast:J
 const/4 v0,0x0
 iput-boolean v0,p0,Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->idleTouch:Z
 new-instance v0,Lorg/efootballrevival/runtimeprobe/IdleEnter;
 invoke-direct {v0,p0},Lorg/efootballrevival/runtimeprobe/IdleEnter;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;)V
 iput-object v0,p0,Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->idleRun:Ljava/lang/Runnable;
 invoke-virtual {p0},Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->idleCheck()V
 return-void
.end method
.method public idleCheck()V
 .registers 8
 iget-boolean v0,p0,Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->resumed:Z
 if-eqz v0,:done
 invoke-static {},Landroid/os/SystemClock;->elapsedRealtime()J
 move-result-wide v1
 iget-boolean v0,p0,Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->busy:Z
 if-nez v0,:reset
 iget-boolean v0,p0,Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->manager:Z
 if-nez v0,:reset
 iget-boolean v0,p0,Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->idleTouch:Z
 if-nez v0,:reset
 iget-boolean v0,p0,Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->noticeAccepted:Z
 if-eqz v0,:reset
 invoke-virtual {p0},Landroid/app/Activity;->hasWindowFocus()Z
 move-result v0
 if-eqz v0,:reset
 iget-wide v3,p0,Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->idleLast:J
 sub-long v3,v1,v3
 const-wide/16 v5,0x2710
 cmp-long v0,v3,v5
 if-ltz v0,:schedule
 invoke-direct {p0},Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->idleStop()V
 const/4 v0,0x0
 invoke-direct {p0,v0},Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->prepare(Z)V
 return-void
 :reset
 iput-wide v1,p0,Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->idleLast:J
 :schedule
 iget-object v0,p0,Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->noticeHandler:Landroid/os/Handler;
 iget-object v1,p0,Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->idleRun:Ljava/lang/Runnable;
 const-wide/16 v2,0x3e8
 invoke-virtual {v0,v1,v2,v3},Landroid/os/Handler;->postDelayed(Ljava/lang/Runnable;J)Z
 :done
 return-void
.end method
.method public dispatchTouchEvent(Landroid/view/MotionEvent;)Z
 .registers 6
 invoke-static {},Landroid/os/SystemClock;->elapsedRealtime()J
 move-result-wide v0
 iput-wide v0,p0,Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->idleLast:J
 invoke-virtual {p1},Landroid/view/MotionEvent;->getActionMasked()I
 move-result v0
 if-nez v0,:up
 const/4 v1,0x1
 iput-boolean v1,p0,Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->idleTouch:Z
 :up
 const/4 v1,0x1
 if-eq v0,v1,:release
 const/4 v1,0x3
 if-ne v0,v1,:forward
 :release
 const/4 v1,0x0
 iput-boolean v1,p0,Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->idleTouch:Z
 :forward
 invoke-super {p0,p1},Landroid/app/Activity;->dispatchTouchEvent(Landroid/view/MotionEvent;)Z
 move-result v0
 return v0
.end method
'''
assert 'idleLast:J' in s;p.write_text(s)
(R/'IdleEnter.smali').write_text('''.class public final Lorg/efootballrevival/runtimeprobe/IdleEnter;
.super Ljava/lang/Object;
.implements Ljava/lang/Runnable;
.field private final activity:Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;
.method public constructor <init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;)V
 .registers 2
 invoke-direct {p0},Ljava/lang/Object;-><init>()V
 iput-object p1,p0,Lorg/efootballrevival/runtimeprobe/IdleEnter;->activity:Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;
 return-void
.end method
.method public run()V
 .registers 2
 iget-object v0,p0,Lorg/efootballrevival/runtimeprobe/IdleEnter;->activity:Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;
 invoke-virtual {v0},Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->idleCheck()V
 return-void
.end method
''')
