.class public final synthetic Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda6;
.super Ljava/lang/Object;
.source "D8$$SyntheticClass"

# interfaces
.implements Ljava/lang/Runnable;


# instance fields
.field public final synthetic f$0:Landroid/app/Activity;

.field public final synthetic f$1:Landroid/widget/Button;

.field public final synthetic f$2:[Ljava/lang/String;

.field public final synthetic f$3:I


# direct methods
.method public synthetic constructor <init>(Landroid/app/Activity;Landroid/widget/Button;[Ljava/lang/String;I)V
    .registers 5

    .line 0
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    iput-object p1, p0, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda6;->f$0:Landroid/app/Activity;

    iput-object p2, p0, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda6;->f$1:Landroid/widget/Button;

    iput-object p3, p0, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda6;->f$2:[Ljava/lang/String;

    iput p4, p0, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda6;->f$3:I

    return-void
.end method


# virtual methods
.method public final run()V
    .registers 5

    .line 0
    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda6;->f$0:Landroid/app/Activity;

    iget-object v1, p0, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda6;->f$1:Landroid/widget/Button;

    iget-object v2, p0, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda6;->f$2:[Ljava/lang/String;

    iget v3, p0, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda6;->f$3:I

    invoke-static {v0, v1, v2, v3}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->lambda$choose$11(Landroid/app/Activity;Landroid/widget/Button;[Ljava/lang/String;I)V

    return-void
.end method
