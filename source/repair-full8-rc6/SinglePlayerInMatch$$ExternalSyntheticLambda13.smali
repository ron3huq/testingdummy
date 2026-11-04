.class public final synthetic Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda13;
.super Ljava/lang/Object;
.source "D8$$SyntheticClass"

# interfaces
.implements Ljava/lang/Runnable;


# instance fields
.field public final synthetic f$0:Landroid/widget/Button;

.field public final synthetic f$1:Landroid/app/Activity;

.field public final synthetic f$2:Ljava/lang/Exception;


# direct methods
.method public synthetic constructor <init>(Landroid/widget/Button;Landroid/app/Activity;Ljava/lang/Exception;)V
    .registers 4

    .line 0
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    iput-object p1, p0, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda13;->f$0:Landroid/widget/Button;

    iput-object p2, p0, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda13;->f$1:Landroid/app/Activity;

    iput-object p3, p0, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda13;->f$2:Ljava/lang/Exception;

    return-void
.end method


# virtual methods
.method public final run()V
    .registers 4

    .line 0
    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda13;->f$0:Landroid/widget/Button;

    iget-object v1, p0, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda13;->f$1:Landroid/app/Activity;

    iget-object v2, p0, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda13;->f$2:Ljava/lang/Exception;

    invoke-static {v0, v1, v2}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->lambda$fail$8(Landroid/widget/Button;Landroid/app/Activity;Ljava/lang/Exception;)V

    return-void
.end method
