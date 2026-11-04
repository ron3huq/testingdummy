.class public final synthetic Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda7;
.super Ljava/lang/Object;
.source "D8$$SyntheticClass"

# interfaces
.implements Ljava/lang/Runnable;


# instance fields
.field public final synthetic f$0:Landroid/app/Activity;

.field public final synthetic f$1:Landroid/widget/Button;

.field public final synthetic f$2:Z

.field public final synthetic f$3:Z

.field public final synthetic f$4:Lorg/json/JSONObject;


# direct methods
.method public synthetic constructor <init>(Landroid/app/Activity;Landroid/widget/Button;ZZLorg/json/JSONObject;)V
    .registers 6

    .line 0
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    iput-object p1, p0, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda7;->f$0:Landroid/app/Activity;

    iput-object p2, p0, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda7;->f$1:Landroid/widget/Button;

    iput-boolean p3, p0, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda7;->f$2:Z

    iput-boolean p4, p0, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda7;->f$3:Z

    iput-object p5, p0, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda7;->f$4:Lorg/json/JSONObject;

    return-void
.end method


# virtual methods
.method public final run()V
    .registers 6

    .line 0
    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda7;->f$0:Landroid/app/Activity;

    iget-object v1, p0, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda7;->f$1:Landroid/widget/Button;

    iget-boolean v2, p0, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda7;->f$2:Z

    iget-boolean v3, p0, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda7;->f$3:Z

    iget-object v4, p0, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda7;->f$4:Lorg/json/JSONObject;

    invoke-static {v0, v1, v2, v3, v4}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->lambda$poll$4(Landroid/app/Activity;Landroid/widget/Button;ZZLorg/json/JSONObject;)V

    return-void
.end method
