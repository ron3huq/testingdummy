.class public final synthetic Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda12;
.super Ljava/lang/Object;
.source "D8$$SyntheticClass"

# interfaces
.implements Ljava/lang/Runnable;


# instance fields
.field public final synthetic f$0:Landroid/widget/Button;

.field public final synthetic f$1:Landroid/app/Activity;

.field public final synthetic f$2:Lorg/json/JSONObject;


# direct methods
.method public synthetic constructor <init>(Landroid/widget/Button;Landroid/app/Activity;Lorg/json/JSONObject;)V
    .registers 4

    .line 0
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    iput-object p1, p0, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda12;->f$0:Landroid/widget/Button;

    iput-object p2, p0, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda12;->f$1:Landroid/app/Activity;

    iput-object p3, p0, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda12;->f$2:Lorg/json/JSONObject;

    return-void
.end method


# virtual methods
.method public final run()V
    .registers 4

    .line 0
    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda12;->f$0:Landroid/widget/Button;

    iget-object v1, p0, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda12;->f$1:Landroid/app/Activity;

    iget-object v2, p0, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda12;->f$2:Lorg/json/JSONObject;

    invoke-static {v0, v1, v2}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->lambda$request$9(Landroid/widget/Button;Landroid/app/Activity;Lorg/json/JSONObject;)V

    return-void
.end method
