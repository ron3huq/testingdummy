.class public final Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;
.super Landroid/app/Activity;
.source "GatewayBootActivity.java"


# annotations
.annotation system Ldalvik/annotation/MemberClasses;
    value = {
        Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$BackHook;,
        Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$Work;
    }
.end annotation


# static fields
.field private static final BACKGROUND:I = -0xe6e5db

.field private static final FOREGROUND:I = -0x191710

.field private static final MUTED:I = -0x4b4430

.field private static final PRIMARY:I = -0x8baf64

.field private static final SURFACE:I = -0xdad9c8

.field static volatile gameEntered:Z


# instance fields
.field private antiScam:Lorg/efootballrevival/runtimeprobe/AntiScamGate;

.field private backCallback:Ljava/lang/Object;

.field private volatile busy:Z

.field private final buttons:Ljava/util/ArrayList;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/ArrayList<",
            "Landroid/widget/Button;",
            ">;"
        }
    .end annotation
.end field

.field private volatile cancelled:Z

.field private content:Landroid/widget/LinearLayout;

.field private diagnostics:Lorg/efootballrevival/runtimeprobe/DiagnosticExport;

.field private exported:Ljava/io/File;

.field private launcherWeb:Lorg/efootballrevival/runtimeprobe/LauncherWeb;

.field private manager:Z

.field private pickerRequest:I

.field private progress:Landroid/widget/TextView;

.field private renderEpoch:I

.field private status:Landroid/widget/TextView;

.field private telegramMembership:Lorg/efootballrevival/runtimeprobe/TelegramMembershipGate;


# direct methods
.method public static synthetic $r8$lambda$1VZ21Hh8p9wlSBzJ-QGkBGkKlSU(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;)V
    .registers 1

    invoke-direct {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->previewStorage()V

    return-void
.end method

.method public static synthetic $r8$lambda$A85qrmNXsABBMb_HTNYwpZAyfl8(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;)V
    .registers 1

    invoke-direct {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->previewDuplicatePlayers()V

    return-void
.end method

.method public static synthetic $r8$lambda$T0ZrWAoVZ6EsXkG3Q9prLTEl-2o(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;)V
    .registers 1

    invoke-direct {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->chooseDrawCount()V

    return-void
.end method

.method public static synthetic $r8$lambda$WOu7AjaMTC9RQc2C5Wr4Dt-OdoU(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;Ljava/lang/String;)V
    .registers 2

    invoke-direct {p0, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->useNativeLauncher(Ljava/lang/String;)V

    return-void
.end method

.method public static synthetic $r8$lambda$bsc7oZs8wOE06FeCdpiwlOTRiHM(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;)V
    .registers 1

    invoke-direct {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->exportSave()V

    return-void
.end method

.method public static synthetic $r8$lambda$c93ktj50lcR6jfU0pnGi_pfF8pQ(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;)V
    .registers 1

    invoke-direct {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->chooseLanguage()V

    return-void
.end method

.method public constructor <init>()V
    .registers 2

    .line 16
    invoke-direct {p0}, Landroid/app/Activity;-><init>()V

    .line 40
    new-instance v0, Ljava/util/ArrayList;

    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    iput-object v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->buttons:Ljava/util/ArrayList;

    return-void
.end method

.method static synthetic access$000(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;)V
    .registers 1

    .line 16
    invoke-direct {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->handleBack()V

    return-void
.end method

.method static synthetic access$101(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;)V
    .registers 1

    .line 16
    invoke-super {p0}, Landroid/app/Activity;->onBackPressed()V

    return-void
.end method

.method private button(Ljava/lang/String;ZLjava/lang/Runnable;)Landroid/widget/Button;
    .registers 9

    .line 105
    new-instance v0, Landroid/widget/Button;

    invoke-direct {v0, p0}, Landroid/widget/Button;-><init>(Landroid/content/Context;)V

    invoke-static {p1}, Lorg/efootballrevival/runtimeprobe/UiStrings;->t(Ljava/lang/String;)Ljava/lang/String;

    move-result-object p1

    invoke-virtual {v0, p1}, Landroid/widget/Button;->setText(Ljava/lang/CharSequence;)V

    const/high16 p1, 0x41800000    # 16.0f

    invoke-virtual {v0, p1}, Landroid/widget/Button;->setTextSize(F)V

    const/4 p1, 0x0

    invoke-virtual {v0, p1}, Landroid/widget/Button;->setAllCaps(Z)V

    .line 106
    new-instance v1, Landroid/content/res/ColorStateList;

    const v2, 0x101009e

    filled-new-array {v2}, [I

    move-result-object v2

    new-array v3, p1, [I

    filled-new-array {v2, v3}, [[I

    move-result-object v2

    const v3, -0x191710

    const v4, -0x888270

    filled-new-array {v3, v4}, [I

    move-result-object v3

    invoke-direct {v1, v2, v3}, Landroid/content/res/ColorStateList;-><init>([[I[I)V

    invoke-virtual {v0, v1}, Landroid/widget/Button;->setTextColor(Landroid/content/res/ColorStateList;)V

    .line 107
    new-instance v1, Landroid/graphics/drawable/StateListDrawable;

    invoke-direct {v1}, Landroid/graphics/drawable/StateListDrawable;-><init>()V

    const v2, -0x101009e

    .line 108
    filled-new-array {v2}, [I

    move-result-object v2

    const v3, -0xcfcebd    # -2.341999E38f

    invoke-direct {p0, v3}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->surface(I)Landroid/graphics/drawable/GradientDrawable;

    move-result-object v4

    invoke-virtual {v1, v2, v4}, Landroid/graphics/drawable/StateListDrawable;->addState([ILandroid/graphics/drawable/Drawable;)V

    new-array p1, p1, [I

    if-eqz p2, :cond_51

    const v3, -0x8baf64

    :cond_51
    invoke-direct {p0, v3}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->surface(I)Landroid/graphics/drawable/GradientDrawable;

    move-result-object p2

    invoke-virtual {v1, p1, p2}, Landroid/graphics/drawable/StateListDrawable;->addState([ILandroid/graphics/drawable/Drawable;)V

    .line 109
    new-instance p1, Landroid/graphics/drawable/RippleDrawable;

    const p2, 0x337d62ab

    invoke-static {p2}, Landroid/content/res/ColorStateList;->valueOf(I)Landroid/content/res/ColorStateList;

    move-result-object p2

    const/4 v2, -0x1

    invoke-direct {p0, v2}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->surface(I)Landroid/graphics/drawable/GradientDrawable;

    move-result-object v3

    invoke-direct {p1, p2, v1, v3}, Landroid/graphics/drawable/RippleDrawable;-><init>(Landroid/content/res/ColorStateList;Landroid/graphics/drawable/Drawable;Landroid/graphics/drawable/Drawable;)V

    invoke-virtual {v0, p1}, Landroid/widget/Button;->setBackground(Landroid/graphics/drawable/Drawable;)V

    const/16 p1, 0xc

    .line 110
    invoke-direct {p0, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->dp(I)I

    move-result p2

    const/16 v1, 0x8

    invoke-direct {p0, v1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->dp(I)I

    move-result v3

    invoke-direct {p0, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->dp(I)I

    move-result p1

    invoke-direct {p0, v1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->dp(I)I

    move-result v1

    invoke-virtual {v0, p2, v3, p1, v1}, Landroid/widget/Button;->setPadding(IIII)V

    const/16 p1, 0x36

    invoke-direct {p0, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->dp(I)I

    move-result p1

    invoke-virtual {v0, p1}, Landroid/widget/Button;->setMinimumHeight(I)V

    .line 111
    new-instance p1, Landroid/widget/LinearLayout$LayoutParams;

    const/4 p2, -0x2

    invoke-direct {p1, v2, p2}, Landroid/widget/LinearLayout$LayoutParams;-><init>(II)V

    const/16 p2, 0xa

    invoke-direct {p0, p2}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->dp(I)I

    move-result p2

    iput p2, p1, Landroid/widget/LinearLayout$LayoutParams;->topMargin:I

    .line 112
    iget-object p2, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->content:Landroid/widget/LinearLayout;

    invoke-virtual {p2, v0, p1}, Landroid/widget/LinearLayout;->addView(Landroid/view/View;Landroid/view/ViewGroup$LayoutParams;)V

    iget-object p1, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->buttons:Ljava/util/ArrayList;

    invoke-virtual {p1, v0}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    new-instance p1, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda58;

    invoke-direct {p1, p0, p3}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda58;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;Ljava/lang/Runnable;)V

    invoke-virtual {v0, p1}, Landroid/widget/Button;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    return-object v0
.end method

.method private chooseDrawCount()V
    .registers 5

    .line 127
    iget-boolean v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->busy:Z

    if-nez v0, :cond_41

    sget-boolean v0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->gameEntered:Z

    if-eqz v0, :cond_9

    goto :goto_41

    .line 128
    :cond_9
    new-instance v0, Landroid/app/AlertDialog$Builder;

    invoke-direct {v0, p0}, Landroid/app/AlertDialog$Builder;-><init>(Landroid/content/Context;)V

    const-string v1, "\u666e\u901a\u5361\u6c60\u62bd\u6570"

    invoke-static {v1}, Lorg/efootballrevival/runtimeprobe/UiStrings;->t(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Landroid/app/AlertDialog$Builder;->setTitle(Ljava/lang/CharSequence;)Landroid/app/AlertDialog$Builder;

    move-result-object v0

    const-string v1, "20 / 73"

    const-string v2, "30 / 73"

    const-string v3, "10 / 73"

    filled-new-array {v3, v1, v2}, [Ljava/lang/String;

    move-result-object v1

    .line 129
    invoke-static {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->drawCount(Landroid/content/Context;)I

    move-result v2

    div-int/lit8 v2, v2, 0xa

    add-int/lit8 v2, v2, -0x1

    new-instance v3, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda30;

    invoke-direct {v3, p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda30;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;)V

    invoke-virtual {v0, v1, v2, v3}, Landroid/app/AlertDialog$Builder;->setSingleChoiceItems([Ljava/lang/CharSequence;ILandroid/content/DialogInterface$OnClickListener;)Landroid/app/AlertDialog$Builder;

    move-result-object v0

    const-string v1, "\u53d6\u6d88"

    .line 132
    invoke-static {v1}, Lorg/efootballrevival/runtimeprobe/UiStrings;->t(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    const/4 v2, 0x0

    invoke-virtual {v0, v1, v2}, Landroid/app/AlertDialog$Builder;->setNegativeButton(Ljava/lang/CharSequence;Landroid/content/DialogInterface$OnClickListener;)Landroid/app/AlertDialog$Builder;

    move-result-object v0

    invoke-virtual {v0}, Landroid/app/AlertDialog$Builder;->show()Landroid/app/AlertDialog;

    :cond_41
    :goto_41
    return-void
.end method

.method private chooseLanguage()V
    .registers 5

    .line 183
    iget-boolean v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->busy:Z

    if-nez v0, :cond_42

    iget v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->pickerRequest:I

    if-eqz v0, :cond_9

    goto :goto_42

    .line 184
    :cond_9
    invoke-direct {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->dialog()Landroid/app/AlertDialog$Builder;

    move-result-object v0

    const-string v1, "\u8bed\u8a00 / Language"

    invoke-virtual {v0, v1}, Landroid/app/AlertDialog$Builder;->setTitle(Ljava/lang/CharSequence;)Landroid/app/AlertDialog$Builder;

    move-result-object v0

    .line 185
    invoke-static {}, Lorg/efootballrevival/runtimeprobe/UiStrings;->languageLabels()[Ljava/lang/String;

    move-result-object v1

    invoke-static {}, Lorg/efootballrevival/runtimeprobe/UiStrings;->languageCodes()[Ljava/lang/String;

    move-result-object v2

    invoke-static {v2}, Ljava/util/Arrays;->asList([Ljava/lang/Object;)Ljava/util/List;

    move-result-object v2

    invoke-static {}, Lorg/efootballrevival/runtimeprobe/UiStrings;->language()Ljava/lang/String;

    move-result-object v3

    invoke-interface {v2, v3}, Ljava/util/List;->indexOf(Ljava/lang/Object;)I

    move-result v2

    new-instance v3, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda59;

    invoke-direct {v3, p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda59;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;)V

    invoke-virtual {v0, v1, v2, v3}, Landroid/app/AlertDialog$Builder;->setSingleChoiceItems([Ljava/lang/CharSequence;ILandroid/content/DialogInterface$OnClickListener;)Landroid/app/AlertDialog$Builder;

    move-result-object v0

    const-string v1, "\u53d6\u6d88"

    .line 191
    invoke-static {v1}, Lorg/efootballrevival/runtimeprobe/UiStrings;->t(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    const/4 v2, 0x0

    invoke-virtual {v0, v1, v2}, Landroid/app/AlertDialog$Builder;->setNegativeButton(Ljava/lang/CharSequence;Landroid/content/DialogInterface$OnClickListener;)Landroid/app/AlertDialog$Builder;

    move-result-object v0

    invoke-virtual {v0}, Landroid/app/AlertDialog$Builder;->create()Landroid/app/AlertDialog;

    move-result-object v0

    .line 192
    invoke-direct {p0, v0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->showDialog(Landroid/app/AlertDialog;)V

    :cond_42
    :goto_42
    return-void
.end method

.method private confirm(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Runnable;)V
    .registers 5

    .line 206
    invoke-direct {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->dialog()Landroid/app/AlertDialog$Builder;

    move-result-object v0

    invoke-static {p1}, Lorg/efootballrevival/runtimeprobe/UiStrings;->t(Ljava/lang/String;)Ljava/lang/String;

    move-result-object p1

    invoke-virtual {v0, p1}, Landroid/app/AlertDialog$Builder;->setTitle(Ljava/lang/CharSequence;)Landroid/app/AlertDialog$Builder;

    move-result-object p1

    invoke-static {p2}, Lorg/efootballrevival/runtimeprobe/UiStrings;->t(Ljava/lang/String;)Ljava/lang/String;

    move-result-object p2

    invoke-virtual {p1, p2}, Landroid/app/AlertDialog$Builder;->setMessage(Ljava/lang/CharSequence;)Landroid/app/AlertDialog$Builder;

    move-result-object p1

    const-string p2, "\u53d6\u6d88"

    invoke-static {p2}, Lorg/efootballrevival/runtimeprobe/UiStrings;->t(Ljava/lang/String;)Ljava/lang/String;

    move-result-object p2

    const/4 v0, 0x0

    invoke-virtual {p1, p2, v0}, Landroid/app/AlertDialog$Builder;->setNegativeButton(Ljava/lang/CharSequence;Landroid/content/DialogInterface$OnClickListener;)Landroid/app/AlertDialog$Builder;

    move-result-object p1

    const-string p2, "\u786e\u8ba4"

    invoke-static {p2}, Lorg/efootballrevival/runtimeprobe/UiStrings;->t(Ljava/lang/String;)Ljava/lang/String;

    move-result-object p2

    new-instance v0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda21;

    invoke-direct {v0, p3}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda21;-><init>(Ljava/lang/Runnable;)V

    invoke-virtual {p1, p2, v0}, Landroid/app/AlertDialog$Builder;->setPositiveButton(Ljava/lang/CharSequence;Landroid/content/DialogInterface$OnClickListener;)Landroid/app/AlertDialog$Builder;

    move-result-object p1

    invoke-virtual {p1}, Landroid/app/AlertDialog$Builder;->create()Landroid/app/AlertDialog;

    move-result-object p1

    invoke-direct {p0, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->showDialog(Landroid/app/AlertDialog;)V

    return-void
.end method

.method private static copy(Ljava/io/InputStream;Ljava/io/OutputStream;J)V
    .registers 10
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    const/high16 v0, 0x10000

    new-array v0, v0, [B

    const-wide/16 v1, 0x0

    .line 317
    :goto_6
    invoke-virtual {p0, v0}, Ljava/io/InputStream;->read([B)I

    move-result v3

    const/4 v4, -0x1

    if-eq v3, v4, :cond_20

    int-to-long v4, v3

    add-long/2addr v1, v4

    cmp-long v4, v1, p2

    if-gtz v4, :cond_18

    const/4 v4, 0x0

    invoke-virtual {p1, v0, v4, v3}, Ljava/io/OutputStream;->write([BII)V

    goto :goto_6

    :cond_18
    new-instance p0, Ljava/io/IOException;

    const-string p1, "\u5b58\u6863\u6587\u4ef6\u8fc7\u5927"

    invoke-direct {p0, p1}, Ljava/io/IOException;-><init>(Ljava/lang/String;)V

    throw p0

    :cond_20
    invoke-virtual {p1}, Ljava/io/OutputStream;->flush()V

    return-void
.end method

.method private dialog()Landroid/app/AlertDialog$Builder;
    .registers 3

    .line 195
    new-instance v0, Landroid/app/AlertDialog$Builder;

    const v1, 0x1030226

    invoke-direct {v0, p0, v1}, Landroid/app/AlertDialog$Builder;-><init>(Landroid/content/Context;I)V

    return-object v0
.end method

.method private dp(I)I
    .registers 3

    int-to-float p1, p1

    .line 42
    invoke-virtual {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->getResources()Landroid/content/res/Resources;

    move-result-object v0

    invoke-virtual {v0}, Landroid/content/res/Resources;->getDisplayMetrics()Landroid/util/DisplayMetrics;

    move-result-object v0

    iget v0, v0, Landroid/util/DisplayMetrics;->density:F

    mul-float/2addr p1, v0

    float-to-int p1, p1

    return p1
.end method

.method static drawCount(Landroid/content/Context;)I
    .registers 3

    const-string v0, "launcher-prefs"

    const/4 v1, 0x0

    .line 115
    invoke-virtual {p0, v0, v1}, Landroid/content/Context;->getSharedPreferences(Ljava/lang/String;I)Landroid/content/SharedPreferences;

    move-result-object p0

    const-string v0, "ordinary-draw-count"

    const/16 v1, 0x1e

    invoke-interface {p0, v0, v1}, Landroid/content/SharedPreferences;->getInt(Ljava/lang/String;I)I

    move-result p0

    const/16 v0, 0xa

    if-eq p0, v0, :cond_19

    const/16 v0, 0x14

    if-eq p0, v0, :cond_19

    if-ne p0, v1, :cond_1a

    :cond_19
    move v1, p0

    :cond_1a
    return v1
.end method

.method private exportSave()V
    .registers 2

    .line 294
    new-instance v0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda55;

    invoke-direct {v0, p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda55;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;)V

    invoke-direct {p0, v0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->task(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$Work;)V

    return-void
.end method

.method private friendly(Ljava/lang/Exception;)Ljava/lang/String;
    .registers 4

    .line 207
    invoke-virtual {p1}, Ljava/lang/Exception;->getMessage()Ljava/lang/String;

    move-result-object p1

    if-nez p1, :cond_9

    const-string p1, "\u8bf7\u91cd\u8bd5\u3002"

    goto :goto_16

    :cond_9
    invoke-virtual {p1}, Ljava/lang/String;->length()I

    move-result v0

    const/16 v1, 0xdc

    if-le v0, v1, :cond_16

    const/4 v0, 0x0

    invoke-virtual {p1, v0, v1}, Ljava/lang/String;->substring(II)Ljava/lang/String;

    move-result-object p1

    :cond_16
    :goto_16
    return-object p1
.end method

.method private handleBack()V
    .registers 3

    .line 338
    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->launcherWeb:Lorg/efootballrevival/runtimeprobe/LauncherWeb;

    if-eqz v0, :cond_d

    new-instance v1, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda34;

    invoke-direct {v1, p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda34;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;)V

    invoke-virtual {v0, v1}, Lorg/efootballrevival/runtimeprobe/LauncherWeb;->back(Ljava/lang/Runnable;)V

    return-void

    :cond_d
    iget-boolean v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->busy:Z

    const/4 v1, 0x0

    if-eqz v0, :cond_20

    const-string v0, "\u6b63\u5728\u5904\u7406\uff0c\u8bf7\u7a0d\u5019"

    invoke-static {v0}, Lorg/efootballrevival/runtimeprobe/UiStrings;->t(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    invoke-static {p0, v0, v1}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;

    move-result-object v0

    invoke-virtual {v0}, Landroid/widget/Toast;->show()V

    return-void

    :cond_20
    iget-boolean v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->manager:Z

    if-eqz v0, :cond_28

    invoke-direct {p0, v1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->render(Z)V

    goto :goto_2b

    :cond_28
    invoke-super {p0}, Landroid/app/Activity;->onBackPressed()V

    :goto_2b
    return-void
.end method

.method static synthetic lambda$confirm$22(Ljava/lang/Runnable;Landroid/content/DialogInterface;I)V
    .registers 3

    .line 206
    invoke-interface {p0}, Ljava/lang/Runnable;->run()V

    return-void
.end method

.method static synthetic lambda$onCreate$1()V
    .registers 0

    return-void
.end method

.method static synthetic lambda$prepare$49(Ljava/lang/Runnable;Landroid/content/DialogInterface;I)V
    .registers 3

    .line 332
    invoke-interface {p0}, Ljava/lang/Runnable;->run()V

    return-void
.end method

.method static synthetic lambda$previewStorage$26([ZLandroid/content/DialogInterface;IZ)V
    .registers 4

    .line 244
    aput-boolean p3, p0, p2

    return-void
.end method

.method private message(Ljava/lang/String;)V
    .registers 4

    .line 205
    iget-boolean v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->cancelled:Z

    if-nez v0, :cond_2c

    invoke-direct {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->dialog()Landroid/app/AlertDialog$Builder;

    move-result-object v0

    const-string v1, "73efootball"

    invoke-static {v1}, Lorg/efootballrevival/runtimeprobe/UiStrings;->t(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Landroid/app/AlertDialog$Builder;->setTitle(Ljava/lang/CharSequence;)Landroid/app/AlertDialog$Builder;

    move-result-object v0

    invoke-static {p1}, Lorg/efootballrevival/runtimeprobe/UiStrings;->t(Ljava/lang/String;)Ljava/lang/String;

    move-result-object p1

    invoke-virtual {v0, p1}, Landroid/app/AlertDialog$Builder;->setMessage(Ljava/lang/CharSequence;)Landroid/app/AlertDialog$Builder;

    move-result-object p1

    const-string v0, "\u77e5\u9053\u4e86"

    invoke-static {v0}, Lorg/efootballrevival/runtimeprobe/UiStrings;->t(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    const/4 v1, 0x0

    invoke-virtual {p1, v0, v1}, Landroid/app/AlertDialog$Builder;->setPositiveButton(Ljava/lang/CharSequence;Landroid/content/DialogInterface$OnClickListener;)Landroid/app/AlertDialog$Builder;

    move-result-object p1

    invoke-virtual {p1}, Landroid/app/AlertDialog$Builder;->create()Landroid/app/AlertDialog;

    move-result-object p1

    invoke-direct {p0, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->showDialog(Landroid/app/AlertDialog;)V

    :cond_2c
    return-void
.end method

.method private panel(Landroid/widget/LinearLayout;Ljava/lang/String;Z)Landroid/widget/LinearLayout;
    .registers 10

    .line 92
    new-instance v0, Landroid/widget/LinearLayout;

    invoke-direct {v0, p0}, Landroid/widget/LinearLayout;-><init>(Landroid/content/Context;)V

    const/4 v1, 0x1

    invoke-virtual {v0, v1}, Landroid/widget/LinearLayout;->setOrientation(I)V

    const/16 v1, 0x12

    .line 93
    invoke-direct {p0, v1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->dp(I)I

    move-result v2

    const/16 v3, 0xe

    invoke-direct {p0, v3}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->dp(I)I

    move-result v4

    invoke-direct {p0, v1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->dp(I)I

    move-result v1

    invoke-direct {p0, v3}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->dp(I)I

    move-result v5

    invoke-virtual {v0, v2, v4, v1, v5}, Landroid/widget/LinearLayout;->setPadding(IIII)V

    if-eqz p3, :cond_41

    .line 94
    new-instance p3, Landroid/graphics/drawable/GradientDrawable;

    sget-object v1, Landroid/graphics/drawable/GradientDrawable$Orientation;->TL_BR:Landroid/graphics/drawable/GradientDrawable$Orientation;

    const v2, -0xabdc94

    const v4, -0xcfdfb8

    filled-new-array {v2, v4}, [I

    move-result-object v2

    invoke-direct {p3, v1, v2}, Landroid/graphics/drawable/GradientDrawable;-><init>(Landroid/graphics/drawable/GradientDrawable$Orientation;[I)V

    const/16 v1, 0x10

    invoke-direct {p0, v1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->dp(I)I

    move-result v1

    int-to-float v1, v1

    invoke-virtual {p3, v1}, Landroid/graphics/drawable/GradientDrawable;->setCornerRadius(F)V

    invoke-virtual {v0, p3}, Landroid/widget/LinearLayout;->setBackground(Landroid/graphics/drawable/Drawable;)V

    goto :goto_4b

    :cond_41
    const p3, -0xdad9c8

    .line 95
    invoke-direct {p0, p3}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->surface(I)Landroid/graphics/drawable/GradientDrawable;

    move-result-object p3

    invoke-virtual {v0, p3}, Landroid/widget/LinearLayout;->setBackground(Landroid/graphics/drawable/Drawable;)V

    .line 96
    :goto_4b
    new-instance p3, Landroid/widget/LinearLayout$LayoutParams;

    const/4 v1, -0x1

    const/4 v2, -0x2

    invoke-direct {p3, v1, v2}, Landroid/widget/LinearLayout$LayoutParams;-><init>(II)V

    invoke-direct {p0, v3}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->dp(I)I

    move-result v1

    iput v1, p3, Landroid/widget/LinearLayout$LayoutParams;->bottomMargin:I

    invoke-virtual {p1, v0, p3}, Landroid/widget/LinearLayout;->addView(Landroid/view/View;Landroid/view/ViewGroup$LayoutParams;)V

    .line 97
    invoke-virtual {p2}, Ljava/lang/String;->isEmpty()Z

    move-result p1

    if-nez p1, :cond_84

    new-instance p1, Landroid/widget/TextView;

    invoke-direct {p1, p0}, Landroid/widget/TextView;-><init>(Landroid/content/Context;)V

    invoke-static {p2}, Lorg/efootballrevival/runtimeprobe/UiStrings;->t(Ljava/lang/String;)Ljava/lang/String;

    move-result-object p2

    invoke-virtual {p1, p2}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    const/high16 p2, 0x41500000    # 13.0f

    invoke-virtual {p1, p2}, Landroid/widget/TextView;->setTextSize(F)V

    const p2, -0x4b4430

    invoke-virtual {p1, p2}, Landroid/widget/TextView;->setTextColor(I)V

    const/4 p2, 0x6

    invoke-direct {p0, p2}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->dp(I)I

    move-result p2

    const/4 p3, 0x0

    invoke-virtual {p1, p3, p3, p3, p2}, Landroid/widget/TextView;->setPadding(IIII)V

    invoke-virtual {v0, p1}, Landroid/widget/LinearLayout;->addView(Landroid/view/View;)V

    :cond_84
    return-object v0
.end method

.method private prepare(Z)V
    .registers 4

    .line 319
    iget-boolean v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->busy:Z

    if-eqz v0, :cond_5

    return-void

    :cond_5
    const/4 v0, 0x1

    iput-boolean v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->busy:Z

    const/4 v0, 0x0

    invoke-direct {p0, v0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->setEnabled(Z)V

    invoke-virtual {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->getWindow()Landroid/view/Window;

    move-result-object v0

    const/16 v1, 0x80

    invoke-virtual {v0, v1}, Landroid/view/Window;->addFlags(I)V

    .line 320
    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->progress:Landroid/widget/TextView;

    const-string v1, "\u6b63\u5728\u68c0\u67e5\u672c\u5730\u8d44\u6e90\u2026"

    invoke-static {v1}, Lorg/efootballrevival/runtimeprobe/UiStrings;->t(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 321
    new-instance v0, Ljava/lang/Thread;

    new-instance v1, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda47;

    invoke-direct {v1, p0, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda47;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;Z)V

    const-string p1, "v9-bootstrap"

    invoke-direct {v0, v1, p1}, Ljava/lang/Thread;-><init>(Ljava/lang/Runnable;Ljava/lang/String;)V

    .line 334
    invoke-virtual {v0}, Ljava/lang/Thread;->start()V

    return-void
.end method

.method private previewDuplicatePlayers()V
    .registers 2

    .line 278
    new-instance v0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda60;

    invoke-direct {v0, p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda60;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;)V

    invoke-direct {p0, v0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->task(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$Work;)V

    return-void
.end method

.method private previewStorage()V
    .registers 3

    .line 213
    sget-boolean v0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->gameEntered:Z

    if-eqz v0, :cond_a

    const-string v0, "\u8bf7\u5b8c\u5168\u9000\u51fa\u6e38\u620f\u5e76\u91cd\u65b0\u6253\u5f00\uff0c\u5728\u8fdb\u5165\u6e38\u620f\u524d\u6e05\u7406\u3002"

    invoke-direct {p0, v0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->message(Ljava/lang/String;)V

    return-void

    .line 214
    :cond_a
    iget v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->renderEpoch:I

    .line 215
    new-instance v1, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda50;

    invoke-direct {v1, p0, v0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda50;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;I)V

    invoke-direct {p0, v1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->task(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$Work;)V

    return-void
.end method

.method private render(Z)V
    .registers 13

    .line 135
    invoke-virtual {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->getWindow()Landroid/view/Window;

    move-result-object v0

    invoke-virtual {v0}, Landroid/view/Window;->getDecorView()Landroid/view/View;

    move-result-object v0

    invoke-static {}, Lorg/efootballrevival/runtimeprobe/UiStrings;->isRtl()Z

    move-result v1

    invoke-virtual {v0, v1}, Landroid/view/View;->setLayoutDirection(I)V

    .line 136
    iput-boolean p1, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->manager:Z

    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->buttons:Ljava/util/ArrayList;

    invoke-virtual {v0}, Ljava/util/ArrayList;->clear()V

    iget v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->renderEpoch:I

    const/4 v1, 0x1

    add-int/2addr v0, v1

    iput v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->renderEpoch:I

    .line 137
    new-instance v2, Landroid/widget/ScrollView;

    invoke-direct {v2, p0}, Landroid/widget/ScrollView;-><init>(Landroid/content/Context;)V

    invoke-virtual {v2, v1}, Landroid/widget/ScrollView;->setFillViewport(Z)V

    const v3, -0xe6e5db

    invoke-virtual {v2, v3}, Landroid/widget/ScrollView;->setBackgroundColor(I)V

    .line 138
    new-instance v3, Landroid/widget/LinearLayout;

    invoke-direct {v3, p0}, Landroid/widget/LinearLayout;-><init>(Landroid/content/Context;)V

    const/16 v4, 0x31

    invoke-virtual {v3, v4}, Landroid/widget/LinearLayout;->setGravity(I)V

    const/16 v4, 0x10

    invoke-direct {p0, v4}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->dp(I)I

    move-result v5

    const/16 v6, 0x14

    invoke-direct {p0, v6}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->dp(I)I

    move-result v7

    invoke-direct {p0, v4}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->dp(I)I

    move-result v4

    invoke-direct {p0, v6}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->dp(I)I

    move-result v6

    invoke-virtual {v3, v5, v7, v4, v6}, Landroid/widget/LinearLayout;->setPadding(IIII)V

    invoke-virtual {v2, v3}, Landroid/widget/ScrollView;->addView(Landroid/view/View;)V

    .line 139
    new-instance v4, Landroid/widget/LinearLayout;

    invoke-direct {v4, p0}, Landroid/widget/LinearLayout;-><init>(Landroid/content/Context;)V

    iput-object v4, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->content:Landroid/widget/LinearLayout;

    invoke-virtual {v4, v1}, Landroid/widget/LinearLayout;->setOrientation(I)V

    const/16 v4, 0x230

    .line 140
    invoke-direct {p0, v4}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->dp(I)I

    move-result v4

    invoke-virtual {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->getResources()Landroid/content/res/Resources;

    move-result-object v5

    invoke-virtual {v5}, Landroid/content/res/Resources;->getDisplayMetrics()Landroid/util/DisplayMetrics;

    move-result-object v5

    iget v5, v5, Landroid/util/DisplayMetrics;->widthPixels:I

    const/16 v6, 0x20

    invoke-direct {p0, v6}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->dp(I)I

    move-result v6

    sub-int/2addr v5, v6

    invoke-static {v4, v5}, Ljava/lang/Math;->min(II)I

    move-result v4

    .line 141
    iget-object v5, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->content:Landroid/widget/LinearLayout;

    new-instance v6, Landroid/widget/LinearLayout$LayoutParams;

    const/4 v7, -0x2

    invoke-direct {v6, v4, v7}, Landroid/widget/LinearLayout$LayoutParams;-><init>(II)V

    invoke-virtual {v3, v5, v6}, Landroid/widget/LinearLayout;->addView(Landroid/view/View;Landroid/view/ViewGroup$LayoutParams;)V

    invoke-virtual {p0, v2}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->setContentView(Landroid/view/View;)V

    .line 142
    iget-object v2, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->content:Landroid/widget/LinearLayout;

    const-string v3, ""

    invoke-direct {p0, v2, v3, v1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->panel(Landroid/widget/LinearLayout;Ljava/lang/String;Z)Landroid/widget/LinearLayout;

    move-result-object v4

    iput-object v4, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->content:Landroid/widget/LinearLayout;

    .line 143
    invoke-direct {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->versionLabel()Ljava/lang/String;

    move-result-object v4

    const/16 v5, 0xd

    const v6, -0x2b4221

    invoke-direct {p0, v4, v5, v6}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->text(Ljava/lang/String;II)Landroid/widget/TextView;

    const-string v4, "\u5b58\u6863\u7ba1\u7406\u5668"

    if-eqz p1, :cond_9d

    move-object v7, v4

    goto :goto_9f

    :cond_9d
    const-string v7, "73efootball"

    :goto_9f
    const/16 v8, 0x1c

    const v9, -0x191710

    .line 144
    invoke-direct {p0, v7, v8, v9}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->text(Ljava/lang/String;II)Landroid/widget/TextView;

    move-result-object v7

    const/4 v8, 0x0

    invoke-virtual {v7, v8, v1}, Landroid/widget/TextView;->setTypeface(Landroid/graphics/Typeface;I)V

    if-eqz p1, :cond_b1

    const-string v7, "\u7ba1\u7406\u672c\u673a\u8fdb\u5ea6\u3002\u5bfc\u5165\u524d\u4f1a\u4fdd\u7559\u5907\u4efd\u3002"

    goto :goto_b3

    :cond_b1
    const-string v7, "UI ideas by @berwtproxy"

    :goto_b3
    const/16 v8, 0xe

    .line 145
    invoke-direct {p0, v7, v8, v6}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->text(Ljava/lang/String;II)Landroid/widget/TextView;

    .line 146
    new-instance v6, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda1;

    invoke-direct {v6, p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda1;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;)V

    const-string v7, "\u8bed\u8a00 / Language"

    const/4 v10, 0x0

    invoke-direct {p0, v7, v10, v6}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->button(Ljava/lang/String;ZLjava/lang/Runnable;)Landroid/widget/Button;

    const-string v6, "\u672c\u5730\u72b6\u6001"

    .line 147
    invoke-direct {p0, v2, v6, v10}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->panel(Landroid/widget/LinearLayout;Ljava/lang/String;Z)Landroid/widget/LinearLayout;

    move-result-object v6

    iput-object v6, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->content:Landroid/widget/LinearLayout;

    if-eqz p1, :cond_d0

    const-string v6, "\u6b63\u5728\u8bfb\u53d6\u5b58\u6863\u2026"

    goto :goto_d2

    :cond_d0
    const-string v6, "\u6b63\u5728\u68c0\u67e5\u672c\u5730\u8d44\u6e90\u2026"

    :goto_d2
    const/16 v7, 0xf

    .line 148
    invoke-direct {p0, v6, v7, v9}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->text(Ljava/lang/String;II)Landroid/widget/TextView;

    move-result-object v6

    iput-object v6, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->status:Landroid/widget/TextView;

    const v6, -0x4b4430

    invoke-direct {p0, v3, v5, v6}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->text(Ljava/lang/String;II)Landroid/widget/TextView;

    move-result-object v3

    iput-object v3, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->progress:Landroid/widget/TextView;

    if-eqz p1, :cond_e8

    const-string v3, "\u5b58\u6863\u64cd\u4f5c"

    goto :goto_ea

    :cond_e8
    const-string v3, "\u5f00\u59cb\u4e0e\u7ba1\u7406"

    .line 149
    :goto_ea
    invoke-direct {p0, v2, v3, v10}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->panel(Landroid/widget/LinearLayout;Ljava/lang/String;Z)Landroid/widget/LinearLayout;

    move-result-object v3

    iput-object v3, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->content:Landroid/widget/LinearLayout;

    if-eqz p1, :cond_168

    .line 151
    new-instance p1, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda9;

    invoke-direct {p1, p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda9;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;)V

    const-string v0, "\u672a\u6ee1\u7ea7\u7403\u5458\u4e00\u952e\u5347\u7ea7\u5e76\u52a0\u70b9"

    invoke-direct {p0, v0, v1, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->button(Ljava/lang/String;ZLjava/lang/Runnable;)Landroid/widget/Button;

    .line 153
    new-instance p1, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda10;

    invoke-direct {p1, p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda10;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;)V

    const-string v0, "\u6e05\u7406\u672a\u6ee1\u7ea7\u91cd\u590d\u7403\u5458"

    invoke-direct {p0, v0, v10, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->button(Ljava/lang/String;ZLjava/lang/Runnable;)Landroid/widget/Button;

    .line 154
    new-instance p1, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda11;

    invoke-direct {p1, p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda11;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;)V

    const-string v0, "\u5bfc\u51fa\u5b58\u6863"

    invoke-direct {p0, v0, v10, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->button(Ljava/lang/String;ZLjava/lang/Runnable;)Landroid/widget/Button;

    .line 155
    new-instance p1, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda12;

    invoke-direct {p1, p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda12;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;)V

    const-string v0, "\u5bfc\u5165\u5b58\u6863"

    invoke-direct {p0, v0, v10, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->button(Ljava/lang/String;ZLjava/lang/Runnable;)Landroid/widget/Button;

    const-string p1, "\u5bfc\u5165\u5c06\u66ff\u6362\u5f53\u524d\u8fdb\u5ea6\uff1b\u53ea\u63a5\u53d7\u672c\u7a0b\u5e8f\u5bfc\u51fa\u7684 .efsave \u6587\u4ef6\u3002\n\u8fdb\u5165\u6e38\u620f\u540e\uff0c\u8bf7\u5173\u95ed\u6e38\u620f\u5e76\u91cd\u65b0\u6253\u5f00\uff0c\u518d\u7ba1\u7406\u5b58\u6863\u3002"

    .line 156
    invoke-direct {p0, p1, v5, v6}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->text(Ljava/lang/String;II)Landroid/widget/TextView;

    .line 157
    new-instance p1, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda13;

    invoke-direct {p1, p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda13;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;)V

    const-string v0, "\u8fd4\u56de"

    invoke-direct {p0, v0, v10, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->button(Ljava/lang/String;ZLjava/lang/Runnable;)Landroid/widget/Button;

    .line 158
    sget-boolean p1, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->gameEntered:Z

    if-eqz p1, :cond_14d

    iget-object p1, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->status:Landroid/widget/TextView;

    const-string v0, "\u6e38\u620f\u5df2\u7ecf\u8fdb\u5165\uff0c\u8bf7\u5148\u5173\u95ed\u6e38\u620f\u5e76\u91cd\u65b0\u6253\u5f00\u3002"

    invoke-static {v0}, Lorg/efootballrevival/runtimeprobe/UiStrings;->t(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    invoke-virtual {p1, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    invoke-direct {p0, v10}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->setEnabled(Z)V

    iget-object p1, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->buttons:Ljava/util/ArrayList;

    invoke-virtual {p1}, Ljava/util/ArrayList;->size()I

    move-result v0

    sub-int/2addr v0, v1

    invoke-virtual {p1, v0}, Ljava/util/ArrayList;->get(I)Ljava/lang/Object;

    move-result-object p1

    check-cast p1, Landroid/widget/Button;

    invoke-virtual {p1, v1}, Landroid/widget/Button;->setEnabled(Z)V

    goto/16 :goto_1f3

    .line 159
    :cond_14d
    iget p1, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->pickerRequest:I

    if-eqz p1, :cond_15e

    iget-object p1, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->status:Landroid/widget/TextView;

    const-string v0, "\u6b63\u5728\u9009\u62e9\u5b58\u6863\u6587\u4ef6\u6216\u4fdd\u5b58\u4f4d\u7f6e\u2026"

    invoke-static {v0}, Lorg/efootballrevival/runtimeprobe/UiStrings;->t(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    invoke-virtual {p1, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    goto/16 :goto_1f3

    .line 160
    :cond_15e
    new-instance p1, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda14;

    invoke-direct {p1, p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda14;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;)V

    invoke-direct {p0, p1, v1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->task(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$Work;Z)V

    goto/16 :goto_1f3

    .line 162
    :cond_168
    new-instance p1, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda15;

    invoke-direct {p1, p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda15;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;)V

    const-string v3, "\u8fdb\u5165\u6e38\u620f"

    invoke-direct {p0, v3, v1, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->button(Ljava/lang/String;ZLjava/lang/Runnable;)Landroid/widget/Button;

    new-instance p1, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda16;

    invoke-direct {p1, p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda16;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;)V

    invoke-direct {p0, v4, v10, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->button(Ljava/lang/String;ZLjava/lang/Runnable;)Landroid/widget/Button;

    .line 163
    new-instance p1, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda17;

    invoke-direct {p1, p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda17;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;)V

    const-string v1, "\u7403\u5458\u7f16\u8f91\u5668 \u00b7 \u57f9\u517b\u4e0e\u9635\u5bb9"

    invoke-direct {p0, v1, v10, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->button(Ljava/lang/String;ZLjava/lang/Runnable;)Landroid/widget/Button;

    const-string p1, "\u57f9\u517b\u52a0\u70b9 / \u72b6\u6001 ABCD / \u6280\u80fd\u4e0e\u589e\u80fd / \u5168\u6570\u636e\u5e93\u9009\u4eba"

    .line 164
    invoke-direct {p0, p1, v5, v6}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->text(Ljava/lang/String;II)Landroid/widget/TextView;

    .line 165
    new-instance p1, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda2;

    invoke-direct {p1, p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda2;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;)V

    const-string v1, "DIY \u5236\u5361\uff08\u80cc\u666f\u4e0e\u5361\u9762\uff09"

    invoke-direct {p0, v1, v10, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->button(Ljava/lang/String;ZLjava/lang/Runnable;)Landroid/widget/Button;

    .line 166
    new-instance p1, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda3;

    invoke-direct {p1, p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda3;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;)V

    const-string v1, "\u5b58\u50a8\u7ba1\u7406 \u00b7 \u626b\u63cf\u4e0e\u6e05\u7406"

    invoke-direct {p0, v1, v10, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->button(Ljava/lang/String;ZLjava/lang/Runnable;)Landroid/widget/Button;

    .line 167
    new-instance p1, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda4;

    invoke-direct {p1, p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda4;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;)V

    const-string v1, "\u91cd\u65b0\u68c0\u67e5\u5e76\u4fee\u590d\u8d44\u6e90"

    invoke-direct {p0, v1, v10, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->button(Ljava/lang/String;ZLjava/lang/Runnable;)Landroid/widget/Button;

    .line 168
    new-instance p1, Ljava/lang/StringBuilder;

    invoke-direct {p1}, Ljava/lang/StringBuilder;-><init>()V

    const-string v1, "\u666e\u901a\u5361\u6c60\u62bd\u6570"

    invoke-static {v1}, Lorg/efootballrevival/runtimeprobe/UiStrings;->t(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    invoke-virtual {p1, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v1, " \u00b7 "

    invoke-virtual {p1, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-static {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->drawCount(Landroid/content/Context;)I

    move-result v1

    invoke-virtual {p1, v1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    const-string v1, " / 73"

    invoke-virtual {p1, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {p1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1

    new-instance v1, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda5;

    invoke-direct {v1, p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda5;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;)V

    invoke-direct {p0, p1, v10, v1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->button(Ljava/lang/String;ZLjava/lang/Runnable;)Landroid/widget/Button;

    const-string p1, "\u4f7f\u7528\u63d0\u793a"

    .line 169
    invoke-direct {p0, v2, p1, v10}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->panel(Landroid/widget/LinearLayout;Ljava/lang/String;Z)Landroid/widget/LinearLayout;

    move-result-object p1

    iput-object p1, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->content:Landroid/widget/LinearLayout;

    const-string p1, "\u8d44\u6e90\u7f3a\u5931\uff1a\u5b89\u88c5\u79bb\u7ebf\u8d44\u6e90\u5305\u540e\u8fdb\u5165\u6e38\u620f\uff0c\u81ea\u52a8\u5bfc\u5165\u3002\n\u8d44\u6e90\u5b8c\u6574\uff1a\u76f4\u63a5\u8fdb\u5165\u3002\u8986\u76d6\u66f4\u65b0\u4fdd\u7559\u8d44\u6e90\u4e0e\u5b58\u6863\uff1b\u8bf7\u52ff\u6e05\u9664\u6570\u636e\u6216\u5378\u8f7d\u4e3b\u6e38\u620f\u3002"

    .line 170
    invoke-direct {p0, p1, v5, v6}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->text(Ljava/lang/String;II)Landroid/widget/TextView;

    const-string p1, "\u5982\u679c\u9047\u5230\u8f7d\u5165\u8d44\u6e90\u5361\u4f4f\u7684\u60c5\u51b5\uff0c\u8bf7\u5207\u4e00\u4e0b\u5230\u8d44\u6e90\u5b89\u88c5\u5305\u5230\u524d\u53f0\u518d\u5207\u56de\u53bb\u3002\n\u5982\u679c\u6e38\u620f\u8fdb\u5165\u9ed1\u5c4f\u9000\u51fa\u518d\u8fdb\u4e00\u6b21\u5373\u53ef"

    .line 171
    invoke-direct {p0, p1, v8, v9}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->text(Ljava/lang/String;II)Landroid/widget/TextView;

    .line 172
    new-instance p1, Ljava/lang/Thread;

    new-instance v1, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda6;

    invoke-direct {v1, p0, v0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda6;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;I)V

    const-string v0, "resource-status"

    invoke-direct {p1, v1, v0}, Ljava/lang/Thread;-><init>(Ljava/lang/Runnable;Ljava/lang/String;)V

    invoke-virtual {p1}, Ljava/lang/Thread;->start()V

    :goto_1f3
    const-string p1, "\u8054\u7cfb"

    .line 174
    invoke-direct {p0, v2, p1, v10}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->panel(Landroid/widget/LinearLayout;Ljava/lang/String;Z)Landroid/widget/LinearLayout;

    move-result-object p1

    iput-object p1, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->content:Landroid/widget/LinearLayout;

    .line 175
    new-instance p1, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda7;

    invoke-direct {p1, p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda7;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;)V

    const-string v0, "\u5bfc\u51fa\u9519\u8bef\u65e5\u5fd7"

    invoke-direct {p0, v0, v10, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->button(Ljava/lang/String;ZLjava/lang/Runnable;)Landroid/widget/Button;

    const-string p1, "\u53ea\u5305\u542b\u7248\u672c\u3001\u8bbe\u5907\u548c\u672c\u5e94\u7528\u8fd1\u671f\u9519\u8bef\uff0c\u4e0d\u5305\u542b\u5b58\u6863\u6216\u7403\u5458\u6570\u636e\u3002\u5bfc\u51fa\u540e\u53ef\u76f4\u63a5\u53d1\u7ed9\u5f00\u53d1\u8005\u3002"

    .line 176
    invoke-direct {p0, p1, v5, v6}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->text(Ljava/lang/String;II)Landroid/widget/TextView;

    const-string p1, "TG  t.me/efootball_73  \u2197"

    const v0, -0x273901

    .line 177
    invoke-direct {p0, p1, v5, v0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->text(Ljava/lang/String;II)Landroid/widget/TextView;

    move-result-object p1

    .line 178
    new-instance v0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda8;

    invoke-direct {v0, p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda8;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;)V

    invoke-virtual {p1, v0}, Landroid/widget/TextView;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    iput-object v2, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->content:Landroid/widget/LinearLayout;

    return-void
.end method

.method private runStorageClean(Lorg/json/JSONObject;Lorg/json/JSONArray;[ZI)V
    .registers 6

    .line 260
    iget-boolean v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->cancelled:Z

    if-nez v0, :cond_15

    sget-boolean v0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->gameEntered:Z

    if-nez v0, :cond_15

    iget v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->renderEpoch:I

    if-eq p4, v0, :cond_d

    goto :goto_15

    .line 261
    :cond_d
    new-instance p4, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda56;

    invoke-direct {p4, p0, p3, p2, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda56;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;[ZLorg/json/JSONArray;Lorg/json/JSONObject;)V

    invoke-direct {p0, p4}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->task(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$Work;)V

    :cond_15
    :goto_15
    return-void
.end method

.method static saveDrawCount(Landroid/content/Context;I)V
    .registers 4
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    const/16 v0, 0xa

    if-eq p1, v0, :cond_15

    const/16 v0, 0x14

    if-eq p1, v0, :cond_15

    const/16 v0, 0x1e

    if-ne p1, v0, :cond_d

    goto :goto_15

    .line 119
    :cond_d
    new-instance p0, Ljava/io/IOException;

    const-string p1, "Invalid draw count"

    invoke-direct {p0, p1}, Ljava/io/IOException;-><init>(Ljava/lang/String;)V

    throw p0

    :cond_15
    :goto_15
    const-string v0, "launcher-prefs"

    const/4 v1, 0x0

    .line 120
    invoke-virtual {p0, v0, v1}, Landroid/content/Context;->getSharedPreferences(Ljava/lang/String;I)Landroid/content/SharedPreferences;

    move-result-object p0

    invoke-interface {p0}, Landroid/content/SharedPreferences;->edit()Landroid/content/SharedPreferences$Editor;

    move-result-object p0

    const-string v0, "ordinary-draw-count"

    invoke-interface {p0, v0, p1}, Landroid/content/SharedPreferences$Editor;->putInt(Ljava/lang/String;I)Landroid/content/SharedPreferences$Editor;

    move-result-object p0

    invoke-interface {p0}, Landroid/content/SharedPreferences$Editor;->commit()Z

    move-result p0

    if-eqz p0, :cond_2d

    return-void

    .line 121
    :cond_2d
    new-instance p0, Ljava/io/IOException;

    const-string p1, "Draw setting was not saved"

    invoke-direct {p0, p1}, Ljava/io/IOException;-><init>(Ljava/lang/String;)V

    throw p0
.end method

.method private setEnabled(Z)V
    .registers 4

    .line 194
    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->buttons:Ljava/util/ArrayList;

    invoke-virtual {v0}, Ljava/util/ArrayList;->iterator()Ljava/util/Iterator;

    move-result-object v0

    :goto_6
    invoke-interface {v0}, Ljava/util/Iterator;->hasNext()Z

    move-result v1

    if-eqz v1, :cond_16

    invoke-interface {v0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    move-result-object v1

    check-cast v1, Landroid/widget/Button;

    invoke-virtual {v1, p1}, Landroid/widget/Button;->setEnabled(Z)V

    goto :goto_6

    :cond_16
    return-void
.end method

.method private showDialog(Landroid/app/AlertDialog;)V
    .registers 2

    .line 204
    invoke-virtual {p1}, Landroid/app/AlertDialog;->show()V

    invoke-direct {p0, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->styleDialog(Landroid/app/AlertDialog;)V

    return-void
.end method

.method private storageSize(J)Ljava/lang/String;
    .registers 9

    .line 209
    sget-object v0, Ljava/util/Locale;->ROOT:Ljava/util/Locale;

    const-wide/32 v1, 0x40000000

    cmp-long v1, p1, v1

    if-ltz v1, :cond_c

    const-string v2, "%.2f GiB"

    goto :goto_e

    :cond_c
    const-string v2, "%.1f MiB"

    :goto_e
    const/4 v3, 0x1

    new-array v3, v3, [Ljava/lang/Object;

    long-to-double p1, p1

    if-ltz v1, :cond_17

    const-wide/high16 v4, 0x41d0000000000000L    # 1.073741824E9

    goto :goto_19

    :cond_17
    const-wide/high16 v4, 0x4130000000000000L    # 1048576.0

    :goto_19
    div-double/2addr p1, v4

    .line 210
    invoke-static {p1, p2}, Ljava/lang/Double;->valueOf(D)Ljava/lang/Double;

    move-result-object p1

    const/4 p2, 0x0

    aput-object p1, v3, p2

    .line 209
    invoke-static {v0, v2, v3}, Ljava/lang/String;->format(Ljava/util/Locale;Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/String;

    move-result-object p1

    return-object p1
.end method

.method private styleDialog(Landroid/app/AlertDialog;)V
    .registers 10

    .line 197
    invoke-virtual {p1}, Landroid/app/AlertDialog;->getWindow()Landroid/view/Window;

    move-result-object v0

    if-eqz v0, :cond_15

    invoke-virtual {p1}, Landroid/app/AlertDialog;->getWindow()Landroid/view/Window;

    move-result-object v0

    invoke-virtual {v0}, Landroid/view/Window;->getDecorView()Landroid/view/View;

    move-result-object v0

    invoke-static {}, Lorg/efootballrevival/runtimeprobe/UiStrings;->isRtl()Z

    move-result v1

    invoke-virtual {v0, v1}, Landroid/view/View;->setLayoutDirection(I)V

    .line 198
    :cond_15
    invoke-virtual {p1}, Landroid/app/AlertDialog;->getWindow()Landroid/view/Window;

    move-result-object v0

    if-eqz v0, :cond_29

    invoke-virtual {p1}, Landroid/app/AlertDialog;->getWindow()Landroid/view/Window;

    move-result-object v0

    const v1, -0xdad9c8

    invoke-direct {p0, v1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->surface(I)Landroid/graphics/drawable/GradientDrawable;

    move-result-object v1

    invoke-virtual {v0, v1}, Landroid/view/Window;->setBackgroundDrawable(Landroid/graphics/drawable/Drawable;)V

    :cond_29
    const v0, 0x102000b

    .line 199
    invoke-virtual {p1, v0}, Landroid/app/AlertDialog;->findViewById(I)Landroid/view/View;

    move-result-object v0

    check-cast v0, Landroid/widget/TextView;

    if-eqz v0, :cond_3a

    const v1, -0x191710

    invoke-virtual {v0, v1}, Landroid/widget/TextView;->setTextColor(I)V

    :cond_3a
    const/4 v0, -0x2

    const/4 v1, -0x3

    const/4 v2, -0x1

    .line 200
    filled-new-array {v2, v0, v1}, [I

    move-result-object v0

    const/4 v1, 0x0

    move v2, v1

    :goto_43
    const/4 v3, 0x3

    if-ge v2, v3, :cond_70

    aget v3, v0, v2

    .line 201
    invoke-virtual {p1, v3}, Landroid/app/AlertDialog;->getButton(I)Landroid/widget/Button;

    move-result-object v3

    if-eqz v3, :cond_6d

    new-instance v4, Landroid/content/res/ColorStateList;

    const v5, 0x101009e

    filled-new-array {v5}, [I

    move-result-object v5

    new-array v6, v1, [I

    filled-new-array {v5, v6}, [[I

    move-result-object v5

    const v6, -0x273901

    const v7, -0x888270

    filled-new-array {v6, v7}, [I

    move-result-object v6

    invoke-direct {v4, v5, v6}, Landroid/content/res/ColorStateList;-><init>([[I[I)V

    invoke-virtual {v3, v4}, Landroid/widget/Button;->setTextColor(Landroid/content/res/ColorStateList;)V

    :cond_6d
    add-int/lit8 v2, v2, 0x1

    goto :goto_43

    :cond_70
    return-void
.end method

.method private surface(I)Landroid/graphics/drawable/GradientDrawable;
    .registers 3

    .line 89
    new-instance v0, Landroid/graphics/drawable/GradientDrawable;

    invoke-direct {v0}, Landroid/graphics/drawable/GradientDrawable;-><init>()V

    invoke-virtual {v0, p1}, Landroid/graphics/drawable/GradientDrawable;->setColor(I)V

    const/16 p1, 0xe

    invoke-direct {p0, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->dp(I)I

    move-result p1

    int-to-float p1, p1

    invoke-virtual {v0, p1}, Landroid/graphics/drawable/GradientDrawable;->setCornerRadius(F)V

    return-object v0
.end method

.method static syncDrawCount(Landroid/content/Context;)V
    .registers 4
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation

    .line 124
    new-instance v0, Lorg/json/JSONObject;

    invoke-direct {v0}, Lorg/json/JSONObject;-><init>()V

    const-string v1, "count"

    invoke-static {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->drawCount(Landroid/content/Context;)I

    move-result v2

    invoke-virtual {v0, v1, v2}, Lorg/json/JSONObject;->put(Ljava/lang/String;I)Lorg/json/JSONObject;

    move-result-object v0

    invoke-virtual {v0}, Lorg/json/JSONObject;->toString()Ljava/lang/String;

    move-result-object v0

    const-string v1, "gacha_settings"

    invoke-static {p0, v1, v0}, Lorg/efootballrevival/runtimeprobe/EmbeddedGateway;->manage(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    return-void
.end method

.method private task(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$Work;)V
    .registers 3

    const/4 v0, 0x0

    .line 271
    invoke-direct {p0, p1, v0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->task(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$Work;Z)V

    return-void
.end method

.method private task(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$Work;Z)V
    .registers 5

    .line 274
    iget-boolean v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->busy:Z

    if-eqz v0, :cond_5

    return-void

    :cond_5
    const/4 v0, 0x1

    iput-boolean v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->busy:Z

    const/4 v0, 0x0

    invoke-direct {p0, v0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->setEnabled(Z)V

    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->progress:Landroid/widget/TextView;

    const-string v1, "\u6b63\u5728\u5904\u7406\uff0c\u8bf7\u7a0d\u5019\u2026"

    invoke-static {v1}, Lorg/efootballrevival/runtimeprobe/UiStrings;->t(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    invoke-virtual {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->getWindow()Landroid/view/Window;

    move-result-object v0

    const/16 v1, 0x80

    invoke-virtual {v0, v1}, Landroid/view/Window;->addFlags(I)V

    .line 275
    new-instance v0, Ljava/lang/Thread;

    new-instance v1, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda39;

    invoke-direct {v1, p0, p1, p2}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda39;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$Work;Z)V

    const-string p1, "v9-save-manager"

    invoke-direct {v0, v1, p1}, Ljava/lang/Thread;-><init>(Ljava/lang/Runnable;Ljava/lang/String;)V

    .line 276
    invoke-virtual {v0}, Ljava/lang/Thread;->start()V

    return-void
.end method

.method private text(Ljava/lang/String;II)Landroid/widget/TextView;
    .registers 5

    .line 85
    new-instance v0, Landroid/widget/TextView;

    invoke-direct {v0, p0}, Landroid/widget/TextView;-><init>(Landroid/content/Context;)V

    invoke-static {p1}, Lorg/efootballrevival/runtimeprobe/UiStrings;->t(Ljava/lang/String;)Ljava/lang/String;

    move-result-object p1

    invoke-virtual {v0, p1}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    int-to-float p1, p2

    invoke-virtual {v0, p1}, Landroid/widget/TextView;->setTextSize(F)V

    invoke-virtual {v0, p3}, Landroid/widget/TextView;->setTextColor(I)V

    const/16 p1, 0x8

    .line 86
    invoke-direct {p0, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->dp(I)I

    move-result p2

    invoke-direct {p0, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->dp(I)I

    move-result p1

    const/4 p3, 0x0

    invoke-virtual {v0, p3, p2, p3, p1}, Landroid/widget/TextView;->setPadding(IIII)V

    iget-object p1, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->content:Landroid/widget/LinearLayout;

    invoke-virtual {p1, v0}, Landroid/widget/LinearLayout;->addView(Landroid/view/View;)V

    return-object v0
.end method

.method private useNativeLauncher(Ljava/lang/String;)V
    .registers 3

    .line 72
    iget-boolean p1, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->cancelled:Z

    if-nez p1, :cond_26

    invoke-virtual {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->isFinishing()Z

    move-result p1

    if-nez p1, :cond_26

    sget-boolean p1, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->gameEntered:Z

    if-eqz p1, :cond_f

    goto :goto_26

    .line 73
    :cond_f
    iget-object p1, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->launcherWeb:Lorg/efootballrevival/runtimeprobe/LauncherWeb;

    const/4 v0, 0x0

    iput-object v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->launcherWeb:Lorg/efootballrevival/runtimeprobe/LauncherWeb;

    if-eqz p1, :cond_19

    .line 74
    invoke-virtual {p1}, Lorg/efootballrevival/runtimeprobe/LauncherWeb;->destroy()V

    :cond_19
    const/4 p1, 0x0

    .line 75
    invoke-direct {p0, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->render(Z)V

    const-string v0, "\u5df2\u5207\u6362\u5230\u517c\u5bb9\u754c\u9762"

    .line 76
    invoke-static {p0, v0, p1}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;

    move-result-object p1

    invoke-virtual {p1}, Landroid/widget/Toast;->show()V

    :cond_26
    :goto_26
    return-void
.end method

.method private versionLabel()Ljava/lang/String;
    .registers 5

    const-string v0, "73efootball  /  "

    .line 101
    :try_start_2
    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1, v0}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->getPackageManager()Landroid/content/pm/PackageManager;

    move-result-object v0

    invoke-virtual {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->getPackageName()Ljava/lang/String;

    move-result-object v2

    const/4 v3, 0x0

    invoke-virtual {v0, v2, v3}, Landroid/content/pm/PackageManager;->getPackageInfo(Ljava/lang/String;I)Landroid/content/pm/PackageInfo;

    move-result-object v0

    iget-object v0, v0, Landroid/content/pm/PackageInfo;->versionName:Ljava/lang/String;

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0
    :try_end_1d
    .catch Landroid/content/pm/PackageManager$NameNotFoundException; {:try_start_2 .. :try_end_1d} :catch_1e

    return-object v0

    :catch_1e
    const-string v0, "73efootball"

    return-object v0
.end method


# virtual methods
.method exportDiagnostics()V
    .registers 2

    .line 181
    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->diagnostics:Lorg/efootballrevival/runtimeprobe/DiagnosticExport;

    invoke-virtual {v0}, Lorg/efootballrevival/runtimeprobe/DiagnosticExport;->start()V

    return-void
.end method

.method synthetic lambda$button$3$org-efootballrevival-runtimeprobe-GatewayBootActivity(Ljava/lang/Runnable;Landroid/view/View;)V
    .registers 3

    .line 112
    iget-boolean p2, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->busy:Z

    if-nez p2, :cond_d

    invoke-static {}, Lorg/efootballrevival/runtimeprobe/EmbeddedGateway;->storageBusy()Z

    move-result p2

    if-nez p2, :cond_d

    invoke-interface {p1}, Ljava/lang/Runnable;->run()V

    :cond_d
    return-void
.end method

.method synthetic lambda$chooseDrawCount$4$org-efootballrevival-runtimeprobe-GatewayBootActivity(Landroid/content/DialogInterface;I)V
    .registers 3

    .line 0
    add-int/lit8 p2, p2, 0x1

    mul-int/lit8 p2, p2, 0xa

    .line 130
    :try_start_4
    invoke-static {p0, p2}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->saveDrawCount(Landroid/content/Context;I)V

    invoke-interface {p1}, Landroid/content/DialogInterface;->dismiss()V

    const/4 p1, 0x0

    invoke-direct {p0, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->render(Z)V
    :try_end_e
    .catch Ljava/io/IOException; {:try_start_4 .. :try_end_e} :catch_f

    goto :goto_17

    :catch_f
    move-exception p1

    .line 131
    invoke-virtual {p1}, Ljava/io/IOException;->getMessage()Ljava/lang/String;

    move-result-object p1

    invoke-direct {p0, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->message(Ljava/lang/String;)V

    :goto_17
    return-void
.end method

.method synthetic lambda$chooseLanguage$21$org-efootballrevival-runtimeprobe-GatewayBootActivity(Landroid/content/DialogInterface;I)V
    .registers 6

    .line 186
    invoke-static {}, Lorg/efootballrevival/runtimeprobe/UiStrings;->languageCodes()[Ljava/lang/String;

    move-result-object v0

    aget-object p2, v0, p2

    const-string v0, "ui-language"

    const/4 v1, 0x0

    .line 187
    invoke-virtual {p0, v0, v1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->getSharedPreferences(Ljava/lang/String;I)Landroid/content/SharedPreferences;

    move-result-object v0

    invoke-interface {v0}, Landroid/content/SharedPreferences;->edit()Landroid/content/SharedPreferences$Editor;

    move-result-object v0

    const-string v2, "language"

    invoke-interface {v0, v2, p2}, Landroid/content/SharedPreferences$Editor;->putString(Ljava/lang/String;Ljava/lang/String;)Landroid/content/SharedPreferences$Editor;

    move-result-object v0

    invoke-interface {v0}, Landroid/content/SharedPreferences$Editor;->commit()Z

    move-result v0

    if-nez v0, :cond_2b

    const-string p1, "\u8bed\u8a00\u9009\u62e9\u4fdd\u5b58\u672a\u5b8c\u6210\uff0c\u8bf7\u91cd\u8bd5\u3002"

    .line 188
    invoke-static {p1}, Lorg/efootballrevival/runtimeprobe/UiStrings;->t(Ljava/lang/String;)Ljava/lang/String;

    move-result-object p1

    invoke-static {p0, p1, v1}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;

    move-result-object p1

    invoke-virtual {p1}, Landroid/widget/Toast;->show()V

    return-void

    .line 190
    :cond_2b
    invoke-static {p2}, Lorg/efootballrevival/runtimeprobe/UiStrings;->setLanguage(Ljava/lang/String;)V

    invoke-interface {p1}, Landroid/content/DialogInterface;->dismiss()V

    iget-boolean p1, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->manager:Z

    invoke-direct {p0, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->render(Z)V

    return-void
.end method

.method synthetic lambda$exportSave$39$org-efootballrevival-runtimeprobe-GatewayBootActivity()V
    .registers 6

    .line 297
    new-instance v0, Landroid/content/Intent;

    const-string v1, "android.intent.action.CREATE_DOCUMENT"

    invoke-direct {v0, v1}, Landroid/content/Intent;-><init>(Ljava/lang/String;)V

    const-string v1, "application/octet-stream"

    invoke-virtual {v0, v1}, Landroid/content/Intent;->setType(Ljava/lang/String;)Landroid/content/Intent;

    const-string v1, "android.intent.category.OPENABLE"

    invoke-virtual {v0, v1}, Landroid/content/Intent;->addCategory(Ljava/lang/String;)Landroid/content/Intent;

    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "73efootball-V9-"

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    new-instance v2, Ljava/text/SimpleDateFormat;

    const-string v3, "yyyyMMdd-HHmmss"

    sget-object v4, Ljava/util/Locale;->ROOT:Ljava/util/Locale;

    invoke-direct {v2, v3, v4}, Ljava/text/SimpleDateFormat;-><init>(Ljava/lang/String;Ljava/util/Locale;)V

    new-instance v3, Ljava/util/Date;

    invoke-direct {v3}, Ljava/util/Date;-><init>()V

    invoke-virtual {v2, v3}, Ljava/text/SimpleDateFormat;->format(Ljava/util/Date;)Ljava/lang/String;

    move-result-object v2

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v2, ".efsave"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    const-string v2, "android.intent.extra.TITLE"

    invoke-virtual {v0, v2, v1}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Ljava/lang/String;)Landroid/content/Intent;

    const/16 v1, 0xb

    :try_start_3d
    iput v1, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->pickerRequest:I

    invoke-virtual {p0, v0, v1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->startActivityForResult(Landroid/content/Intent;I)V
    :try_end_42
    .catch Landroid/content/ActivityNotFoundException; {:try_start_3d .. :try_end_42} :catch_43

    goto :goto_4b

    :catch_43
    const/4 v0, 0x0

    iput v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->pickerRequest:I

    const-string v0, "\u8bf7\u542f\u7528\u7cfb\u7edf\u6587\u4ef6\u7ba1\u7406\u5668\u3002"

    invoke-direct {p0, v0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->message(Ljava/lang/String;)V

    :goto_4b
    return-void
.end method

.method synthetic lambda$exportSave$40$org-efootballrevival-runtimeprobe-GatewayBootActivity()Ljava/lang/String;
    .registers 6
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation

    .line 295
    new-instance v0, Ljava/io/File;

    invoke-virtual {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->getCacheDir()Ljava/io/File;

    move-result-object v1

    new-instance v2, Ljava/lang/StringBuilder;

    const-string v3, "export-"

    invoke-direct {v2, v3}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-static {}, Ljava/lang/System;->nanoTime()J

    move-result-wide v3

    invoke-virtual {v2, v3, v4}, Ljava/lang/StringBuilder;->append(J)Ljava/lang/StringBuilder;

    const-string v3, ".efsave"

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v2

    invoke-direct {v0, v1, v2}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V

    const-string v1, "export"

    invoke-virtual {v0}, Ljava/io/File;->getAbsolutePath()Ljava/lang/String;

    move-result-object v2

    invoke-static {p0, v1, v2}, Lorg/efootballrevival/runtimeprobe/EmbeddedGateway;->manage(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    .line 296
    iget-object v1, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->exported:Ljava/io/File;

    if-eqz v1, :cond_30

    invoke-virtual {v1}, Ljava/io/File;->delete()Z

    :cond_30
    iput-object v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->exported:Ljava/io/File;

    .line 297
    new-instance v0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda48;

    invoke-direct {v0, p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda48;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;)V

    invoke-virtual {p0, v0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->runOnUiThread(Ljava/lang/Runnable;)V

    const-string v0, "\u8bf7\u9009\u62e9\u5b58\u6863\u4fdd\u5b58\u4f4d\u7f6e\u3002"

    return-object v0
.end method

.method synthetic lambda$handleBack$54$org-efootballrevival-runtimeprobe-GatewayBootActivity()V
    .registers 1

    .line 338
    # invokes: Landroid/app/Activity;->onBackPressed()V
    invoke-static {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->access$101(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;)V

    return-void
.end method

.method synthetic lambda$onActivityResult$41$org-efootballrevival-runtimeprobe-GatewayBootActivity(Landroid/net/Uri;)Ljava/lang/String;
    .registers 5
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation

    .line 308
    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->exported:Ljava/io/File;

    if-eqz v0, :cond_55

    invoke-virtual {v0}, Ljava/io/File;->isFile()Z

    move-result v0

    if-eqz v0, :cond_55

    .line 309
    new-instance v0, Ljava/io/FileInputStream;

    iget-object v1, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->exported:Ljava/io/File;

    invoke-direct {v0, v1}, Ljava/io/FileInputStream;-><init>(Ljava/io/File;)V

    :try_start_11
    invoke-virtual {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->getContentResolver()Landroid/content/ContentResolver;

    move-result-object v1

    const-string v2, "wt"

    invoke-virtual {v1, p1, v2}, Landroid/content/ContentResolver;->openOutputStream(Landroid/net/Uri;Ljava/lang/String;)Ljava/io/OutputStream;

    move-result-object p1
    :try_end_1b
    .catchall {:try_start_11 .. :try_end_1b} :catchall_4b

    if-eqz p1, :cond_38

    const-wide/32 v1, 0x25800000

    :try_start_20
    invoke-static {v0, p1, v1, v2}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->copy(Ljava/io/InputStream;Ljava/io/OutputStream;J)V
    :try_end_23
    .catchall {:try_start_20 .. :try_end_23} :catchall_36

    if-eqz p1, :cond_28

    :try_start_25
    invoke-virtual {p1}, Ljava/io/OutputStream;->close()V
    :try_end_28
    .catchall {:try_start_25 .. :try_end_28} :catchall_4b

    :cond_28
    invoke-virtual {v0}, Ljava/io/InputStream;->close()V

    .line 310
    iget-object p1, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->exported:Ljava/io/File;

    invoke-virtual {p1}, Ljava/io/File;->delete()Z

    const/4 p1, 0x0

    iput-object p1, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->exported:Ljava/io/File;

    const-string p1, "\u5b58\u6863\u5df2\u5bfc\u51fa\uff0c\u8bf7\u59a5\u5584\u4fdd\u5b58\u3002"

    return-object p1

    :catchall_36
    move-exception v1

    goto :goto_40

    .line 309
    :cond_38
    :try_start_38
    new-instance v1, Ljava/io/IOException;

    const-string v2, "\u4fdd\u5b58\u4f4d\u7f6e\u4e0d\u53ef\u5199"

    invoke-direct {v1, v2}, Ljava/io/IOException;-><init>(Ljava/lang/String;)V

    throw v1
    :try_end_40
    .catchall {:try_start_38 .. :try_end_40} :catchall_36

    :goto_40
    if-eqz p1, :cond_4a

    :try_start_42
    invoke-virtual {p1}, Ljava/io/OutputStream;->close()V
    :try_end_45
    .catchall {:try_start_42 .. :try_end_45} :catchall_46

    goto :goto_4a

    :catchall_46
    move-exception p1

    :try_start_47
    invoke-virtual {v1, p1}, Ljava/lang/Throwable;->addSuppressed(Ljava/lang/Throwable;)V

    :cond_4a
    :goto_4a
    throw v1
    :try_end_4b
    .catchall {:try_start_47 .. :try_end_4b} :catchall_4b

    :catchall_4b
    move-exception p1

    :try_start_4c
    invoke-virtual {v0}, Ljava/io/InputStream;->close()V
    :try_end_4f
    .catchall {:try_start_4c .. :try_end_4f} :catchall_50

    goto :goto_54

    :catchall_50
    move-exception v0

    invoke-virtual {p1, v0}, Ljava/lang/Throwable;->addSuppressed(Ljava/lang/Throwable;)V

    :goto_54
    throw p1

    .line 308
    :cond_55
    new-instance p1, Ljava/io/IOException;

    const-string v0, "\u5bfc\u51fa\u7f13\u5b58\u5df2\u5931\u6548\uff0c\u8bf7\u91cd\u65b0\u70b9\u51fb\u5bfc\u51fa\u5b58\u6863\u3002"

    invoke-direct {p1, v0}, Ljava/io/IOException;-><init>(Ljava/lang/String;)V

    throw p1
.end method

.method synthetic lambda$onActivityResult$42$org-efootballrevival-runtimeprobe-GatewayBootActivity(Landroid/net/Uri;)Ljava/lang/String;
    .registers 8
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation

    .line 0
    const-string v0, "\u5b58\u6863\u5df2\u5bfc\u5165 \u00b7 "

    .line 312
    new-instance v1, Ljava/io/File;

    invoke-virtual {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->getCacheDir()Ljava/io/File;

    move-result-object v2

    new-instance v3, Ljava/lang/StringBuilder;

    const-string v4, "save-import-"

    invoke-direct {v3, v4}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-static {}, Ljava/lang/System;->nanoTime()J

    move-result-wide v4

    invoke-virtual {v3, v4, v5}, Ljava/lang/StringBuilder;->append(J)Ljava/lang/StringBuilder;

    const-string v4, ".efsave"

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v3

    invoke-direct {v1, v2, v3}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V

    .line 313
    :try_start_22
    invoke-virtual {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->getContentResolver()Landroid/content/ContentResolver;

    move-result-object v2

    invoke-virtual {v2, p1}, Landroid/content/ContentResolver;->openInputStream(Landroid/net/Uri;)Ljava/io/InputStream;

    move-result-object p1
    :try_end_2a
    .catchall {:try_start_22 .. :try_end_2a} :catchall_88

    :try_start_2a
    new-instance v2, Ljava/io/FileOutputStream;

    invoke-direct {v2, v1}, Ljava/io/FileOutputStream;-><init>(Ljava/io/File;)V
    :try_end_2f
    .catchall {:try_start_2a .. :try_end_2f} :catchall_7c

    if-eqz p1, :cond_6b

    const-wide/32 v3, 0x25800000

    :try_start_34
    invoke-static {p1, v2, v3, v4}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->copy(Ljava/io/InputStream;Ljava/io/OutputStream;J)V
    :try_end_37
    .catchall {:try_start_34 .. :try_end_37} :catchall_69

    :try_start_37
    invoke-virtual {v2}, Ljava/io/OutputStream;->close()V
    :try_end_3a
    .catchall {:try_start_37 .. :try_end_3a} :catchall_7c

    if-eqz p1, :cond_3f

    :try_start_3c
    invoke-virtual {p1}, Ljava/io/InputStream;->close()V

    .line 314
    :cond_3f
    new-instance p1, Lorg/json/JSONObject;

    const-string v2, "import"

    invoke-virtual {v1}, Ljava/io/File;->getAbsolutePath()Ljava/lang/String;

    move-result-object v3

    invoke-static {p0, v2, v3}, Lorg/efootballrevival/runtimeprobe/EmbeddedGateway;->manage(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v2

    invoke-direct {p1, v2}, Lorg/json/JSONObject;-><init>(Ljava/lang/String;)V

    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2, v0}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    const-string v0, "players"

    invoke-virtual {p1, v0}, Lorg/json/JSONObject;->getInt(Ljava/lang/String;)I

    move-result p1

    invoke-virtual {v2, p1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    const-string p1, " \u540d\u7403\u5458\u3002\u539f\u8fdb\u5ea6\u5df2\u81ea\u52a8\u5907\u4efd\u3002"

    invoke-virtual {v2, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1
    :try_end_65
    .catchall {:try_start_3c .. :try_end_65} :catchall_88

    .line 315
    invoke-virtual {v1}, Ljava/io/File;->delete()Z

    return-object p1

    :catchall_69
    move-exception v0

    goto :goto_73

    .line 313
    :cond_6b
    :try_start_6b
    new-instance v0, Ljava/io/IOException;

    const-string v3, "\u6587\u4ef6\u4e0d\u53ef\u8bfb"

    invoke-direct {v0, v3}, Ljava/io/IOException;-><init>(Ljava/lang/String;)V

    throw v0
    :try_end_73
    .catchall {:try_start_6b .. :try_end_73} :catchall_69

    :goto_73
    :try_start_73
    invoke-virtual {v2}, Ljava/io/OutputStream;->close()V
    :try_end_76
    .catchall {:try_start_73 .. :try_end_76} :catchall_77

    goto :goto_7b

    :catchall_77
    move-exception v2

    :try_start_78
    invoke-virtual {v0, v2}, Ljava/lang/Throwable;->addSuppressed(Ljava/lang/Throwable;)V

    :goto_7b
    throw v0
    :try_end_7c
    .catchall {:try_start_78 .. :try_end_7c} :catchall_7c

    :catchall_7c
    move-exception v0

    if-eqz p1, :cond_87

    :try_start_7f
    invoke-virtual {p1}, Ljava/io/InputStream;->close()V
    :try_end_82
    .catchall {:try_start_7f .. :try_end_82} :catchall_83

    goto :goto_87

    :catchall_83
    move-exception p1

    :try_start_84
    invoke-virtual {v0, p1}, Ljava/lang/Throwable;->addSuppressed(Ljava/lang/Throwable;)V

    :cond_87
    :goto_87
    throw v0
    :try_end_88
    .catchall {:try_start_84 .. :try_end_88} :catchall_88

    :catchall_88
    move-exception p1

    .line 315
    invoke-virtual {v1}, Ljava/io/File;->delete()Z

    throw p1
.end method

.method synthetic lambda$onActivityResult$43$org-efootballrevival-runtimeprobe-GatewayBootActivity(Landroid/net/Uri;)V
    .registers 3

    .line 311
    new-instance v0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda61;

    invoke-direct {v0, p0, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda61;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;Landroid/net/Uri;)V

    invoke-direct {p0, v0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->task(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$Work;)V

    return-void
.end method

.method synthetic lambda$onCreate$2$org-efootballrevival-runtimeprobe-GatewayBootActivity()V
    .registers 3

    .line 66
    iget-boolean v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->cancelled:Z

    if-nez v0, :cond_24

    invoke-virtual {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->isFinishing()Z

    move-result v0

    if-nez v0, :cond_24

    sget-boolean v0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->gameEntered:Z

    if-eqz v0, :cond_f

    goto :goto_24

    .line 67
    :cond_f
    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->antiScam:Lorg/efootballrevival/runtimeprobe/AntiScamGate;

    if-nez v0, :cond_1a

    new-instance v0, Lorg/efootballrevival/runtimeprobe/AntiScamGate;

    invoke-direct {v0, p0}, Lorg/efootballrevival/runtimeprobe/AntiScamGate;-><init>(Landroid/app/Activity;)V

    iput-object v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->antiScam:Lorg/efootballrevival/runtimeprobe/AntiScamGate;

    .line 68
    :cond_1a
    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->antiScam:Lorg/efootballrevival/runtimeprobe/AntiScamGate;

    new-instance v1, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda52;

    invoke-direct {v1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda52;-><init>()V

    invoke-virtual {v0, v1}, Lorg/efootballrevival/runtimeprobe/AntiScamGate;->request(Ljava/lang/Runnable;)V

    :cond_24
    :goto_24
    return-void
.end method

.method synthetic lambda$prepare$44$org-efootballrevival-runtimeprobe-GatewayBootActivity(Ljava/lang/String;JJ)V
    .registers 10

    .line 325
    iget-boolean v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->cancelled:Z

    if-nez v0, :cond_36

    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->progress:Landroid/widget/TextView;

    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v1, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string p1, " \u00b7 "

    invoke-virtual {v1, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-wide/16 v2, 0x0

    cmp-long p1, p2, v2

    if-nez p1, :cond_1c

    const/16 p1, 0x64

    goto :goto_23

    :cond_1c
    const-wide/high16 v2, 0x4059000000000000L    # 100.0

    long-to-double p4, p4

    mul-double/2addr p4, v2

    long-to-double p1, p2

    div-double/2addr p4, p1

    double-to-int p1, p4

    :goto_23
    invoke-virtual {v1, p1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    const-string p1, "%"

    invoke-virtual {v1, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1

    invoke-static {p1}, Lorg/efootballrevival/runtimeprobe/UiStrings;->t(Ljava/lang/String;)Ljava/lang/String;

    move-result-object p1

    invoke-virtual {v0, p1}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    :cond_36
    return-void
.end method

.method synthetic lambda$prepare$45$org-efootballrevival-runtimeprobe-GatewayBootActivity([JLjava/lang/String;JJ)V
    .registers 14

    .line 323
    iget-boolean v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->cancelled:Z

    if-nez v0, :cond_41

    invoke-static {}, Landroid/os/SystemClock;->elapsedRealtime()J

    move-result-wide v0

    const/4 v2, 0x0

    aget-wide v3, p1, v2

    sub-long v3, v0, v3

    const-wide/16 v5, 0x96

    cmp-long v3, v3, v5

    if-gez v3, :cond_18

    cmp-long v3, p3, p5

    if-eqz v3, :cond_18

    return-void

    :cond_18
    aput-wide v0, p1, v2

    const-string p1, "verify"

    .line 324
    invoke-virtual {p2, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result p1

    if-eqz p1, :cond_26

    const-string p1, "\u6821\u9a8c\u8d44\u6e90"

    :goto_24
    move-object v2, p1

    goto :goto_34

    :cond_26
    const-string p1, "extract"

    invoke-virtual {p2, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result p1

    if-eqz p1, :cond_31

    const-string p1, "\u5bfc\u5165\u8d44\u6e90"

    goto :goto_24

    :cond_31
    const-string p1, "\u5b8c\u6210\u8d44\u6e90\u51c6\u5907"

    goto :goto_24

    .line 325
    :goto_34
    new-instance p1, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda57;

    move-object v0, p1

    move-object v1, p0

    move-wide v3, p5

    move-wide v5, p3

    invoke-direct/range {v0 .. v6}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda57;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;Ljava/lang/String;JJ)V

    invoke-virtual {p0, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->runOnUiThread(Ljava/lang/Runnable;)V

    return-void

    .line 323
    :cond_41
    new-instance p1, Ljava/util/concurrent/CancellationException;

    invoke-direct {p1}, Ljava/util/concurrent/CancellationException;-><init>()V

    throw p1
.end method

.method synthetic lambda$prepare$46$org-efootballrevival-runtimeprobe-GatewayBootActivity()V
    .registers 3

    .line 326
    iget-boolean v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->cancelled:Z

    if-nez v0, :cond_f

    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->progress:Landroid/widget/TextView;

    const-string v1, "\u6b63\u5728\u542f\u52a8\u672c\u5730\u670d\u52a1\u2026"

    invoke-static {v1}, Lorg/efootballrevival/runtimeprobe/UiStrings;->t(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    :cond_f
    return-void
.end method

.method synthetic lambda$prepare$47$org-efootballrevival-runtimeprobe-GatewayBootActivity()V
    .registers 4

    .line 0
    const/4 v0, 0x1

    .line 330
    sput-boolean v0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->gameEntered:Z

    new-instance v0, Landroid/content/Intent;

    invoke-direct {v0}, Landroid/content/Intent;-><init>()V

    invoke-virtual {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->getPackageName()Ljava/lang/String;

    move-result-object v1

    const-string v2, "com.epicgames.ue4.SplashActivity"

    invoke-virtual {v0, v1, v2}, Landroid/content/Intent;->setClassName(Ljava/lang/String;Ljava/lang/String;)Landroid/content/Intent;

    invoke-virtual {p0, v0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->startActivity(Landroid/content/Intent;)V

    invoke-virtual {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->finish()V

    return-void
.end method

.method synthetic lambda$prepare$48$org-efootballrevival-runtimeprobe-GatewayBootActivity()V
    .registers 2

    .line 330
    new-instance v0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda20;

    invoke-direct {v0, p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda20;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;)V

    invoke-virtual {p0, v0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->requestGameLaunch(Ljava/lang/Runnable;)V

    return-void
.end method

.method synthetic lambda$prepare$50$org-efootballrevival-runtimeprobe-GatewayBootActivity(Landroid/content/DialogInterface;I)V
    .registers 3

    .line 0
    const/4 p1, 0x0

    .line 332
    invoke-direct {p0, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->render(Z)V

    return-void
.end method

.method synthetic lambda$prepare$51$org-efootballrevival-runtimeprobe-GatewayBootActivity(Ljava/lang/String;)V
    .registers 5

    .line 329
    iget-boolean v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->cancelled:Z

    if-eqz v0, :cond_5

    return-void

    :cond_5
    const/4 v0, 0x0

    iput-boolean v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->busy:Z

    const/4 v0, 0x1

    invoke-direct {p0, v0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->setEnabled(Z)V

    invoke-virtual {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->getWindow()Landroid/view/Window;

    move-result-object v0

    const/16 v1, 0x80

    invoke-virtual {v0, v1}, Landroid/view/Window;->clearFlags(I)V

    .line 330
    new-instance v0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda31;

    invoke-direct {v0, p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda31;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;)V

    const-string v1, "INSTALLED"

    .line 331
    invoke-virtual {p1, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result p1

    if-eqz p1, :cond_60

    invoke-direct {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->dialog()Landroid/app/AlertDialog$Builder;

    move-result-object p1

    const-string v1, "\u8d44\u6e90\u5bfc\u5165\u5b8c\u6210"

    invoke-static {v1}, Lorg/efootballrevival/runtimeprobe/UiStrings;->t(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    invoke-virtual {p1, v1}, Landroid/app/AlertDialog$Builder;->setTitle(Ljava/lang/CharSequence;)Landroid/app/AlertDialog$Builder;

    move-result-object p1

    const-string v1, "\u8d44\u6e90\u5df2\u4fdd\u5b58\u5230\u4e3b\u6e38\u620f\uff0c\u540e\u7eed\u8986\u76d6\u66f4\u65b0\u65e0\u9700\u518d\u6b21\u4e0b\u8f7d\u3002\u73b0\u5728\u53ef\u4ee5\u5378\u8f7d\u201c73efootball\u79bb\u7ebf\u8d44\u6e90\u201d\uff1b\u8bf7\u4fdd\u7559\u4e3b\u6e38\u620f\u6570\u636e\u3002"

    invoke-static {v1}, Lorg/efootballrevival/runtimeprobe/UiStrings;->t(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    invoke-virtual {p1, v1}, Landroid/app/AlertDialog$Builder;->setMessage(Ljava/lang/CharSequence;)Landroid/app/AlertDialog$Builder;

    move-result-object p1

    const-string v1, "\u8fdb\u5165\u6e38\u620f"

    .line 332
    invoke-static {v1}, Lorg/efootballrevival/runtimeprobe/UiStrings;->t(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    new-instance v2, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda32;

    invoke-direct {v2, v0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda32;-><init>(Ljava/lang/Runnable;)V

    invoke-virtual {p1, v1, v2}, Landroid/app/AlertDialog$Builder;->setPositiveButton(Ljava/lang/CharSequence;Landroid/content/DialogInterface$OnClickListener;)Landroid/app/AlertDialog$Builder;

    move-result-object p1

    const-string v0, "\u7a0d\u540e"

    invoke-static {v0}, Lorg/efootballrevival/runtimeprobe/UiStrings;->t(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    new-instance v1, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda33;

    invoke-direct {v1, p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda33;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;)V

    invoke-virtual {p1, v0, v1}, Landroid/app/AlertDialog$Builder;->setNegativeButton(Ljava/lang/CharSequence;Landroid/content/DialogInterface$OnClickListener;)Landroid/app/AlertDialog$Builder;

    move-result-object p1

    invoke-virtual {p1}, Landroid/app/AlertDialog$Builder;->create()Landroid/app/AlertDialog;

    move-result-object p1

    .line 331
    invoke-direct {p0, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->showDialog(Landroid/app/AlertDialog;)V

    goto :goto_63

    .line 332
    :cond_60
    invoke-interface {v0}, Ljava/lang/Runnable;->run()V

    :goto_63
    return-void
.end method

.method synthetic lambda$prepare$52$org-efootballrevival-runtimeprobe-GatewayBootActivity(Ljava/lang/Exception;)V
    .registers 5

    .line 0
    const/4 v0, 0x0

    .line 333
    iput-boolean v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->busy:Z

    iget-boolean v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->cancelled:Z

    if-eqz v0, :cond_8

    return-void

    :cond_8
    const/4 v0, 0x1

    invoke-direct {p0, v0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->setEnabled(Z)V

    invoke-virtual {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->getWindow()Landroid/view/Window;

    move-result-object v0

    const/16 v1, 0x80

    invoke-virtual {v0, v1}, Landroid/view/Window;->clearFlags(I)V

    invoke-virtual {p1}, Ljava/lang/Exception;->getMessage()Ljava/lang/String;

    move-result-object v0

    .line 334
    iget-object v1, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->progress:Landroid/widget/TextView;

    if-eqz v0, :cond_28

    const-string v2, "RESOURCE_COMPANION_REQUIRED"

    invoke-virtual {v0, v2}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result v2

    if-eqz v2, :cond_28

    const-string p1, "\u8d44\u6e90\u7f3a\u5931\uff1a\u8bf7\u5148\u5b89\u88c5\u79bb\u7ebf\u8d44\u6e90APK\uff0c\u518d\u70b9\u51fb\u8fdb\u5165\u6e38\u620f\u3002"

    goto :goto_47

    :cond_28
    if-eqz v0, :cond_35

    const-string v2, "INSUFFICIENT_SPACE"

    invoke-virtual {v0, v2}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result v0

    if-eqz v0, :cond_35

    const-string p1, "\u7a7a\u95f4\u4e0d\u8db3\uff1a\u8bf7\u6e05\u7406\u5b58\u50a8\u7a7a\u95f4\u540e\u91cd\u8bd5\u3002"

    goto :goto_47

    :cond_35
    new-instance v0, Ljava/lang/StringBuilder;

    const-string v2, "\u51c6\u5907\u672a\u5b8c\u6210\uff0c\u8bf7\u91cd\u8bd5\u3002\u5df2\u6709\u5b58\u6863\u4fdd\u7559\u3002\n"

    invoke-direct {v0, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-direct {p0, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->friendly(Ljava/lang/Exception;)Ljava/lang/String;

    move-result-object p1

    invoke-virtual {v0, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1

    :goto_47
    invoke-static {p1}, Lorg/efootballrevival/runtimeprobe/UiStrings;->t(Ljava/lang/String;)Ljava/lang/String;

    move-result-object p1

    invoke-virtual {v1, p1}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    return-void
.end method

.method synthetic lambda$prepare$53$org-efootballrevival-runtimeprobe-GatewayBootActivity(Z)V
    .registers 11

    .line 0
    const/4 v0, 0x1

    :try_start_1
    new-array v1, v0, [J

    const-wide/16 v2, 0x0

    const/4 v4, 0x0

    aput-wide v2, v1, v4

    .line 322
    new-instance v2, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda25;

    invoke-direct {v2, p0, v1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda25;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;[J)V

    invoke-static {p0, v2, p1}, Lorg/efootballrevival/runtimeprobe/EmbeddedResources;->prepare(Landroid/content/Context;Lorg/efootballrevival/runtimeprobe/ResourceInstaller$Progress;Z)Ljava/lang/String;

    move-result-object p1

    .line 326
    new-instance v1, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda26;

    invoke-direct {v1, p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda26;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;)V

    invoke-virtual {p0, v1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->runOnUiThread(Ljava/lang/Runnable;)V

    .line 327
    invoke-static {p0}, Lorg/efootballrevival/runtimeprobe/CpkCache;->repair(Landroid/content/Context;)V

    invoke-static {p0}, Lorg/efootballrevival/runtimeprobe/EmbeddedGateway;->ensureStarted(Landroid/content/Context;)V

    invoke-static {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->syncDrawCount(Landroid/content/Context;)V

    const-string v1, "UE4Game/PesMobile/PesMobile.uproject"

    const/4 v2, 0x2

    new-array v3, v2, [Ljava/io/File;

    .line 328
    invoke-virtual {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->getFilesDir()Ljava/io/File;

    move-result-object v5

    aput-object v5, v3, v4

    const/4 v5, 0x0

    invoke-virtual {p0, v5}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->getExternalFilesDir(Ljava/lang/String;)Ljava/io/File;

    move-result-object v5

    aput-object v5, v3, v0

    :goto_34
    if-ge v4, v2, :cond_7b

    aget-object v0, v3, v4

    if-nez v0, :cond_3b

    goto :goto_62

    :cond_3b
    new-instance v5, Ljava/io/File;

    invoke-direct {v5, v0, v1}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V

    invoke-virtual {v5}, Ljava/io/File;->getParentFile()Ljava/io/File;

    move-result-object v0

    invoke-virtual {v0}, Ljava/io/File;->mkdirs()Z

    invoke-virtual {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->getAssets()Landroid/content/res/AssetManager;

    move-result-object v0

    invoke-virtual {v0, v1}, Landroid/content/res/AssetManager;->open(Ljava/lang/String;)Ljava/io/InputStream;

    move-result-object v0
    :try_end_4f
    .catch Ljava/lang/Exception; {:try_start_1 .. :try_end_4f} :catch_84

    :try_start_4f
    new-instance v6, Ljava/io/FileOutputStream;

    invoke-direct {v6, v5}, Ljava/io/FileOutputStream;-><init>(Ljava/io/File;)V
    :try_end_54
    .catchall {:try_start_4f .. :try_end_54} :catchall_6f

    const-wide/32 v7, 0x100000

    :try_start_57
    invoke-static {v0, v6, v7, v8}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->copy(Ljava/io/InputStream;Ljava/io/OutputStream;J)V
    :try_end_5a
    .catchall {:try_start_57 .. :try_end_5a} :catchall_65

    :try_start_5a
    invoke-virtual {v6}, Ljava/io/OutputStream;->close()V
    :try_end_5d
    .catchall {:try_start_5a .. :try_end_5d} :catchall_6f

    if-eqz v0, :cond_62

    :try_start_5f
    invoke-virtual {v0}, Ljava/io/InputStream;->close()V
    :try_end_62
    .catch Ljava/lang/Exception; {:try_start_5f .. :try_end_62} :catch_84

    :cond_62
    :goto_62
    add-int/lit8 v4, v4, 0x1

    goto :goto_34

    :catchall_65
    move-exception p1

    :try_start_66
    invoke-virtual {v6}, Ljava/io/OutputStream;->close()V
    :try_end_69
    .catchall {:try_start_66 .. :try_end_69} :catchall_6a

    goto :goto_6e

    :catchall_6a
    move-exception v1

    :try_start_6b
    invoke-virtual {p1, v1}, Ljava/lang/Throwable;->addSuppressed(Ljava/lang/Throwable;)V

    :goto_6e
    throw p1
    :try_end_6f
    .catchall {:try_start_6b .. :try_end_6f} :catchall_6f

    :catchall_6f
    move-exception p1

    if-eqz v0, :cond_7a

    :try_start_72
    invoke-virtual {v0}, Ljava/io/InputStream;->close()V
    :try_end_75
    .catchall {:try_start_72 .. :try_end_75} :catchall_76

    goto :goto_7a

    :catchall_76
    move-exception v0

    :try_start_77
    invoke-virtual {p1, v0}, Ljava/lang/Throwable;->addSuppressed(Ljava/lang/Throwable;)V

    :cond_7a
    :goto_7a
    throw p1

    .line 329
    :cond_7b
    new-instance v0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda27;

    invoke-direct {v0, p0, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda27;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;Ljava/lang/String;)V

    invoke-virtual {p0, v0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->runOnUiThread(Ljava/lang/Runnable;)V
    :try_end_83
    .catch Ljava/lang/Exception; {:try_start_77 .. :try_end_83} :catch_84

    goto :goto_94

    :catch_84
    move-exception p1

    const-string v0, "V9_BOOT"

    const-string v1, "startup failed"

    .line 333
    invoke-static {v0, v1, p1}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I

    new-instance v0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda28;

    invoke-direct {v0, p0, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda28;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;Ljava/lang/Exception;)V

    invoke-virtual {p0, v0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->runOnUiThread(Ljava/lang/Runnable;)V

    :goto_94
    return-void
.end method

.method synthetic lambda$previewDuplicatePlayers$35$org-efootballrevival-runtimeprobe-GatewayBootActivity(Ljava/lang/String;)Ljava/lang/String;
    .registers 4
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation

    .line 286
    iget-boolean v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->cancelled:Z

    if-nez v0, :cond_4d

    iget-boolean v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->manager:Z

    if-eqz v0, :cond_4d

    sget-boolean v0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->gameEntered:Z

    if-nez v0, :cond_4d

    .line 287
    new-instance v0, Lorg/json/JSONObject;

    invoke-direct {v0}, Lorg/json/JSONObject;-><init>()V

    const-string v1, "token"

    invoke-virtual {v0, v1, p1}, Lorg/json/JSONObject;->put(Ljava/lang/String;Ljava/lang/Object;)Lorg/json/JSONObject;

    .line 288
    new-instance p1, Lorg/json/JSONObject;

    const-string v1, "duplicate_delete"

    invoke-virtual {v0}, Lorg/json/JSONObject;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {p0, v1, v0}, Lorg/efootballrevival/runtimeprobe/EmbeddedGateway;->manage(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    invoke-direct {p1, v0}, Lorg/json/JSONObject;-><init>(Ljava/lang/String;)V

    .line 289
    new-instance v0, Ljava/lang/StringBuilder;

    const-string v1, "\u5df2\u6e05\u7406 "

    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    const-string v1, "deleted"

    invoke-virtual {p1, v1}, Lorg/json/JSONObject;->getInt(Ljava/lang/String;)I

    move-result v1

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    const-string v1, " \u5f20\u672a\u6ee1\u7ea7\u91cd\u590d\u7403\u5458\uff0c\u5269\u4f59 "

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v1, "total"

    invoke-virtual {p1, v1}, Lorg/json/JSONObject;->getInt(Ljava/lang/String;)I

    move-result p1

    invoke-virtual {v0, p1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    const-string p1, " \u5f20\u3002\u539f\u5b58\u6863\u5df2\u81ea\u52a8\u5907\u4efd\u3002"

    invoke-virtual {v0, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1

    return-object p1

    .line 286
    :cond_4d
    new-instance p1, Ljava/io/IOException;

    const-string v0, "\u9875\u9762\u5df2\u5207\u6362\uff0c\u8bf7\u91cd\u65b0\u626b\u63cf\u3002"

    invoke-direct {p1, v0}, Ljava/io/IOException;-><init>(Ljava/lang/String;)V

    throw p1
.end method

.method synthetic lambda$previewDuplicatePlayers$36$org-efootballrevival-runtimeprobe-GatewayBootActivity(Ljava/lang/String;)V
    .registers 3

    .line 285
    new-instance v0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda18;

    invoke-direct {v0, p0, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda18;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;Ljava/lang/String;)V

    invoke-direct {p0, v0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->task(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$Work;)V

    return-void
.end method

.method synthetic lambda$previewDuplicatePlayers$37$org-efootballrevival-runtimeprobe-GatewayBootActivity(Ljava/lang/String;Ljava/lang/String;)V
    .registers 4

    .line 284
    iget-boolean v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->cancelled:Z

    if-nez v0, :cond_17

    iget-boolean v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->manager:Z

    if-eqz v0, :cond_17

    sget-boolean v0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->gameEntered:Z

    if-eqz v0, :cond_d

    goto :goto_17

    .line 285
    :cond_d
    new-instance v0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda22;

    invoke-direct {v0, p0, p2}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda22;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;Ljava/lang/String;)V

    const-string p2, "\u6e05\u7406\u91cd\u590d\u7403\u5458\u9884\u89c8"

    invoke-direct {p0, p2, p1, v0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->confirm(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Runnable;)V

    :cond_17
    :goto_17
    return-void
.end method

.method synthetic lambda$previewDuplicatePlayers$38$org-efootballrevival-runtimeprobe-GatewayBootActivity()Ljava/lang/String;
    .registers 6
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation

    .line 279
    new-instance v0, Lorg/json/JSONObject;

    const-string v1, "duplicate_preview"

    const-string v2, ""

    invoke-static {p0, v1, v2}, Lorg/efootballrevival/runtimeprobe/EmbeddedGateway;->manage(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    invoke-direct {v0, v1}, Lorg/json/JSONObject;-><init>(Ljava/lang/String;)V

    const-string v1, "delete_count"

    .line 280
    invoke-virtual {v0, v1}, Lorg/json/JSONObject;->getInt(Ljava/lang/String;)I

    move-result v1

    if-nez v1, :cond_1c

    const-string v0, "\u6ca1\u6709\u53ef\u6e05\u7406\u7684\u672a\u6ee1\u7ea7\u91cd\u590d\u7403\u5458\u3002\u6ee1\u7ea7\u3001\u9501\u5b9a\u3001\u9635\u5bb9\u5185\u53ca\u79df\u501f\u7403\u5458\u5747\u4fdd\u7559\u3002"

    .line 281
    invoke-static {v0}, Lorg/efootballrevival/runtimeprobe/UiStrings;->t(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    return-object v0

    :cond_1c
    const-string v2, "token"

    .line 282
    invoke-virtual {v0, v2}, Lorg/json/JSONObject;->getString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v2

    .line 283
    new-instance v3, Ljava/lang/StringBuilder;

    const-string v4, "\u53d1\u73b0 "

    invoke-direct {v3, v4}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    const-string v4, "duplicate_ids"

    invoke-virtual {v0, v4}, Lorg/json/JSONObject;->getInt(Ljava/lang/String;)I

    move-result v4

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    const-string v4, " \u7ec4\u540c\u5361ID\u7403\u5458\uff0c\u9884\u8ba1\u5220\u9664 "

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v3, v1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    const-string v4, " \u5f20\u672a\u6ee1\u7ea7\u91cd\u590d\u5361\uff08\u542b\u50a8\u5907\uff09\u3002\n\n\u6ee1\u7ea7\u5361\u5168\u90e8\u4fdd\u7559\uff1b\u6ca1\u6709\u6ee1\u7ea7\u5361\u65f6\u81f3\u5c11\u4fdd\u7559\u7b49\u7ea7\u6700\u9ad8\u7684\u4e00\u5f20\u3002\u9501\u5b9a\u3001\u4efb\u610f\u9635\u5bb9\u5185\u548c\u79df\u501f\u7403\u5458\u8df3\u8fc7\uff0c\u4e0d\u6309\u540c\u540d\u5408\u5e76\u4e0d\u540c\u7248\u672c\u5361\u3002\n\n\u4fdd\u7559\u6ee1\u7ea7\u5361 "

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v4, "full_kept"

    invoke-virtual {v0, v4}, Lorg/json/JSONObject;->getInt(Ljava/lang/String;)I

    move-result v4

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    const-string v4, " \u5f20\uff0c\u53d7\u4fdd\u62a4\u672a\u6ee1\u7ea7\u5361 "

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v4, "protected_kept"

    invoke-virtual {v0, v4}, Lorg/json/JSONObject;->getInt(Ljava/lang/String;)I

    move-result v4

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    const-string v4, " \u5f20\uff0c\u5f02\u5e38\u7ec4\u8df3\u8fc7 "

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v4, "invalid_groups"

    invoke-virtual {v0, v4}, Lorg/json/JSONObject;->getInt(Ljava/lang/String;)I

    move-result v0

    invoke-virtual {v3, v0}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    const-string v0, " \u7ec4\u3002\n\n\u5220\u9664\u524d\u81ea\u52a8\u5907\u4efd\uff0c\u4e0d\u589e\u52a0GP\u6216\u5176\u4ed6\u5956\u52b1\u3002\u786e\u8ba4\u6e05\u7406\uff1f"

    invoke-virtual {v3, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lorg/efootballrevival/runtimeprobe/UiStrings;->t(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    .line 284
    new-instance v3, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda53;

    invoke-direct {v3, p0, v0, v2}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda53;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;Ljava/lang/String;Ljava/lang/String;)V

    invoke-virtual {p0, v3}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->runOnUiThread(Ljava/lang/Runnable;)V

    .line 292
    new-instance v0, Ljava/lang/StringBuilder;

    const-string v2, "\u626b\u63cf\u5b8c\u6210\uff0c\u9884\u8ba1\u6e05\u7406 "

    invoke-direct {v0, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    const-string v1, " \u5f20\uff0c\u7b49\u5f85\u786e\u8ba4\u3002"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method

.method synthetic lambda$previewStorage$23$org-efootballrevival-runtimeprobe-GatewayBootActivity()Ljava/lang/String;
    .registers 4
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation

    .line 220
    new-instance v0, Lorg/json/JSONObject;

    const-string v1, "recover"

    const-string v2, "{}"

    invoke-static {p0, v1, v2}, Lorg/efootballrevival/runtimeprobe/EmbeddedGateway;->storage(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    invoke-direct {v0, v1}, Lorg/json/JSONObject;-><init>(Ljava/lang/String;)V

    const-string v1, "message"

    invoke-virtual {v0, v1}, Lorg/json/JSONObject;->getString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method

.method synthetic lambda$previewStorage$24$org-efootballrevival-runtimeprobe-GatewayBootActivity()V
    .registers 2

    .line 220
    new-instance v0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda44;

    invoke-direct {v0, p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda44;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;)V

    invoke-direct {p0, v0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->task(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$Work;)V

    return-void
.end method

.method synthetic lambda$previewStorage$25$org-efootballrevival-runtimeprobe-GatewayBootActivity(I)V
    .registers 4

    .line 218
    iget-boolean v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->cancelled:Z

    if-nez v0, :cond_19

    sget-boolean v0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->gameEntered:Z

    if-nez v0, :cond_19

    iget v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->renderEpoch:I

    if-eq p1, v0, :cond_d

    goto :goto_19

    .line 219
    :cond_d
    new-instance p1, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda29;

    invoke-direct {p1, p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda29;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;)V

    const-string v0, "\u6062\u590d\u4e2d\u65ad\u7684\u6e05\u7406"

    const-string v1, "\u4e0a\u6b21\u6e05\u7406\u672a\u7ed3\u675f\u3002\u5c06\u6062\u590d\u5c1a\u672a\u786e\u8ba4\u5220\u9664\u7684\u6682\u5b58\u6570\u636e\uff0c\u6216\u5b8c\u6210\u4e0a\u6b21\u5df2\u786e\u8ba4\u7684\u5220\u9664\uff0c\u518d\u91cd\u65b0\u626b\u63cf\u3002"

    invoke-direct {p0, v0, v1, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->confirm(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Runnable;)V

    :cond_19
    :goto_19
    return-void
.end method

.method synthetic lambda$previewStorage$27$org-efootballrevival-runtimeprobe-GatewayBootActivity(Lorg/json/JSONObject;Lorg/json/JSONArray;[ZI)V
    .registers 5

    .line 250
    invoke-direct {p0, p1, p2, p3, p4}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->runStorageClean(Lorg/json/JSONObject;Lorg/json/JSONArray;[ZI)V

    return-void
.end method

.method synthetic lambda$previewStorage$28$org-efootballrevival-runtimeprobe-GatewayBootActivity(I[ZLorg/json/JSONArray;Lorg/json/JSONObject;Landroid/content/DialogInterface;I)V
    .registers 13

    .line 247
    iget-boolean p5, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->cancelled:Z

    if-nez p5, :cond_46

    sget-boolean p5, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->gameEntered:Z

    if-nez p5, :cond_46

    iget p5, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->renderEpoch:I

    if-eq p1, p5, :cond_d

    goto :goto_46

    :cond_d
    const/4 p5, 0x0

    move p6, p5

    .line 249
    :goto_f
    array-length v0, p2

    if-ge p5, v0, :cond_2e

    invoke-virtual {p3, p5}, Lorg/json/JSONArray;->optJSONObject(I)Lorg/json/JSONObject;

    move-result-object v0

    aget-boolean v1, p2, p5

    if-eqz v1, :cond_2b

    if-eqz v0, :cond_2b

    const-string v1, "id"

    invoke-virtual {v0, v1}, Lorg/json/JSONObject;->optString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    const-string v1, "backups"

    invoke-virtual {v1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_2b

    const/4 p6, 0x1

    :cond_2b
    add-int/lit8 p5, p5, 0x1

    goto :goto_f

    .line 250
    :cond_2e
    new-instance p5, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda49;

    move-object v0, p5

    move-object v1, p0

    move-object v2, p4

    move-object v3, p3

    move-object v4, p2

    move v5, p1

    invoke-direct/range {v0 .. v5}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda49;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;Lorg/json/JSONObject;Lorg/json/JSONArray;[ZI)V

    if-eqz p6, :cond_43

    const-string p1, "\u6c38\u4e45\u5220\u9664\u5168\u90e8\u5386\u53f2\u5907\u4efd\uff1f"

    const-string p2, "\u5c06\u5220\u9664\u5168\u90e8\u5386\u53f2\u53d1\u5e03\u5907\u4efd\uff08\u5305\u62ec\u6700\u65b0\u4e00\u4efd\uff09\u53ca\u5df2\u786e\u8ba4\u95f2\u7f6e\u7684\u6062\u590d\u526f\u672c\u3002\u4e4b\u540e\u4e0d\u80fd\u7528\u8fd9\u4e9b\u5907\u4efd\u56de\u6eda\uff1b\u5f53\u524d\u53d1\u5e03\u8d44\u6e90\u3001\u4f5c\u54c1\u548c\u5b58\u6863\u4fdd\u7559\u3002\u6b64\u64cd\u4f5c\u4e0d\u53ef\u64a4\u9500\u3002"

    .line 251
    invoke-direct {p0, p1, p2, p5}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->confirm(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Runnable;)V

    goto :goto_46

    .line 252
    :cond_43
    invoke-interface {p5}, Ljava/lang/Runnable;->run()V

    :cond_46
    :goto_46
    return-void
.end method

.method synthetic lambda$previewStorage$29$org-efootballrevival-runtimeprobe-GatewayBootActivity([Ljava/lang/String;[ZILorg/json/JSONArray;Lorg/json/JSONObject;Landroid/content/DialogInterface;I)V
    .registers 14

    .line 243
    invoke-direct {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->dialog()Landroid/app/AlertDialog$Builder;

    move-result-object p6

    const-string p7, "\u9009\u62e9\u6e05\u7406\u9879\u76ee"

    invoke-static {p7}, Lorg/efootballrevival/runtimeprobe/UiStrings;->t(Ljava/lang/String;)Ljava/lang/String;

    move-result-object p7

    invoke-virtual {p6, p7}, Landroid/app/AlertDialog$Builder;->setTitle(Ljava/lang/CharSequence;)Landroid/app/AlertDialog$Builder;

    move-result-object p6

    new-instance p7, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda37;

    invoke-direct {p7, p2}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda37;-><init>([Z)V

    .line 244
    invoke-virtual {p6, p1, p2, p7}, Landroid/app/AlertDialog$Builder;->setMultiChoiceItems([Ljava/lang/CharSequence;[ZLandroid/content/DialogInterface$OnMultiChoiceClickListener;)Landroid/app/AlertDialog$Builder;

    move-result-object p1

    const-string p6, "\u53d6\u6d88"

    .line 245
    invoke-static {p6}, Lorg/efootballrevival/runtimeprobe/UiStrings;->t(Ljava/lang/String;)Ljava/lang/String;

    move-result-object p6

    const/4 p7, 0x0

    invoke-virtual {p1, p6, p7}, Landroid/app/AlertDialog$Builder;->setNegativeButton(Ljava/lang/CharSequence;Landroid/content/DialogInterface$OnClickListener;)Landroid/app/AlertDialog$Builder;

    move-result-object p1

    const-string p6, "\u786e\u8ba4\u6e05\u7406"

    .line 246
    invoke-static {p6}, Lorg/efootballrevival/runtimeprobe/UiStrings;->t(Ljava/lang/String;)Ljava/lang/String;

    move-result-object p6

    new-instance p7, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda38;

    move-object v0, p7

    move-object v1, p0

    move v2, p3

    move-object v3, p2

    move-object v4, p4

    move-object v5, p5

    invoke-direct/range {v0 .. v5}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda38;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;I[ZLorg/json/JSONArray;Lorg/json/JSONObject;)V

    invoke-virtual {p1, p6, p7}, Landroid/app/AlertDialog$Builder;->setPositiveButton(Ljava/lang/CharSequence;Landroid/content/DialogInterface$OnClickListener;)Landroid/app/AlertDialog$Builder;

    move-result-object p1

    .line 253
    invoke-virtual {p1}, Landroid/app/AlertDialog$Builder;->create()Landroid/app/AlertDialog;

    move-result-object p1

    .line 243
    invoke-direct {p0, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->showDialog(Landroid/app/AlertDialog;)V

    return-void
.end method

.method synthetic lambda$previewStorage$30$org-efootballrevival-runtimeprobe-GatewayBootActivity(ILjava/lang/String;[Ljava/lang/String;[ZLorg/json/JSONArray;Lorg/json/JSONObject;)V
    .registers 16

    .line 237
    iget-boolean v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->cancelled:Z

    if-nez v0, :cond_47

    sget-boolean v0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->gameEntered:Z

    if-nez v0, :cond_47

    iget v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->renderEpoch:I

    if-eq p1, v0, :cond_d

    goto :goto_47

    .line 240
    :cond_d
    invoke-direct {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->dialog()Landroid/app/AlertDialog$Builder;

    move-result-object v0

    const-string v1, "\u5b58\u50a8\u5360\u7528\u4e0e\u6e05\u7406\u9884\u89c8"

    invoke-static {v1}, Lorg/efootballrevival/runtimeprobe/UiStrings;->t(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Landroid/app/AlertDialog$Builder;->setTitle(Ljava/lang/CharSequence;)Landroid/app/AlertDialog$Builder;

    move-result-object v0

    invoke-virtual {v0, p2}, Landroid/app/AlertDialog$Builder;->setMessage(Ljava/lang/CharSequence;)Landroid/app/AlertDialog$Builder;

    move-result-object p2

    const-string v0, "\u8fd4\u56de"

    .line 241
    invoke-static {v0}, Lorg/efootballrevival/runtimeprobe/UiStrings;->t(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    const/4 v1, 0x0

    invoke-virtual {p2, v0, v1}, Landroid/app/AlertDialog$Builder;->setNegativeButton(Ljava/lang/CharSequence;Landroid/content/DialogInterface$OnClickListener;)Landroid/app/AlertDialog$Builder;

    move-result-object p2

    const-string v0, "\u9009\u62e9\u6e05\u7406\u9879\u76ee"

    .line 242
    invoke-static {v0}, Lorg/efootballrevival/runtimeprobe/UiStrings;->t(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    new-instance v8, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda42;

    move-object v1, v8

    move-object v2, p0

    move-object v3, p3

    move-object v4, p4

    move v5, p1

    move-object v6, p5

    move-object v7, p6

    invoke-direct/range {v1 .. v7}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda42;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;[Ljava/lang/String;[ZILorg/json/JSONArray;Lorg/json/JSONObject;)V

    invoke-virtual {p2, v0, v8}, Landroid/app/AlertDialog$Builder;->setPositiveButton(Ljava/lang/CharSequence;Landroid/content/DialogInterface$OnClickListener;)Landroid/app/AlertDialog$Builder;

    move-result-object p1

    .line 254
    invoke-virtual {p1}, Landroid/app/AlertDialog$Builder;->create()Landroid/app/AlertDialog;

    move-result-object p1

    .line 240
    invoke-direct {p0, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->showDialog(Landroid/app/AlertDialog;)V

    :cond_47
    :goto_47
    return-void
.end method

.method synthetic lambda$previewStorage$31$org-efootballrevival-runtimeprobe-GatewayBootActivity(I)Ljava/lang/String;
    .registers 18
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation

    .line 0
    move-object/from16 v8, p0

    .line 216
    new-instance v7, Lorg/json/JSONObject;

    const-string v0, "preview"

    const-string v1, "{}"

    invoke-static {v8, v0, v1}, Lorg/efootballrevival/runtimeprobe/EmbeddedGateway;->storage(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    invoke-direct {v7, v0}, Lorg/json/JSONObject;-><init>(Ljava/lang/String;)V

    const-string v0, "recoveryRequired"

    .line 217
    invoke-virtual {v7, v0}, Lorg/json/JSONObject;->optBoolean(Ljava/lang/String;)Z

    move-result v0

    if-eqz v0, :cond_24

    .line 218
    new-instance v0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda45;

    move/from16 v2, p1

    invoke-direct {v0, v8, v2}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda45;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;I)V

    invoke-virtual {v8, v0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->runOnUiThread(Ljava/lang/Runnable;)V

    const-string v0, "\u53d1\u73b0\u4e2d\u65ad\u7684\u6e05\u7406\uff0c\u8bf7\u5148\u6062\u590d\u3002"

    return-object v0

    :cond_24
    move/from16 v2, p1

    const-string v0, "usage"

    .line 224
    invoke-virtual {v7, v0}, Lorg/json/JSONObject;->getJSONArray(Ljava/lang/String;)Lorg/json/JSONArray;

    move-result-object v0

    const-string v1, "groups"

    invoke-virtual {v7, v1}, Lorg/json/JSONObject;->getJSONArray(Ljava/lang/String;)Lorg/json/JSONArray;

    move-result-object v6

    .line 225
    new-instance v1, Ljava/lang/StringBuilder;

    const-string v3, "\u65e7\u4f5c\u54c1\u63a5\u5165\u7f13\u5b58\u53ef\u5355\u72ec\u6e05\u7406\uff1a\u4fdd\u7559\u4f5c\u54c1\u3001\u7403\u5458\u4e0e\u5b58\u6863\uff0c\u518d\u6b21\u4f7f\u7528\u65f6\u91cd\u65b0\u751f\u6210\u3002\u5f53\u524d\u4f7f\u7528\u548c\u5f85\u6062\u590d\u7684\u8d44\u6e90\u4fdd\u7559\u3002\u5360\u7528\u6309\u72ec\u7acb\u6587\u4ef6\u7edf\u8ba1\uff0c\u5171\u4eab\u786c\u94fe\u63a5\u4e0d\u91cd\u590d\u8ba1\u6570\u3002\u82e5\u52fe\u9009\u5386\u53f2\u5907\u4efd\uff0c\u5c06\u6c38\u4e45\u5220\u9664\u5168\u90e8\u53d1\u5e03\u5907\u4efd\u53ca\u5df2\u786e\u8ba4\u95f2\u7f6e\u7684\u6062\u590d\u526f\u672c\u3002\n\n"

    invoke-direct {v1, v3}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    const/4 v4, 0x0

    .line 226
    :goto_3a
    invoke-virtual {v0}, Lorg/json/JSONArray;->length()I

    move-result v5

    const-string v9, "\n"

    const-string v10, "label"

    const-string v11, "bytes"

    if-ge v4, v5, :cond_67

    invoke-virtual {v0, v4}, Lorg/json/JSONArray;->getJSONObject(I)Lorg/json/JSONObject;

    move-result-object v5

    invoke-virtual {v5, v10}, Lorg/json/JSONObject;->getString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v10

    invoke-virtual {v1, v10}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v10, "\uff1a"

    invoke-virtual {v1, v10}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v5, v11}, Lorg/json/JSONObject;->getLong(Ljava/lang/String;)J

    move-result-wide v10

    invoke-direct {v8, v10, v11}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->storageSize(J)Ljava/lang/String;

    move-result-object v5

    invoke-virtual {v1, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1, v9}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    add-int/lit8 v4, v4, 0x1

    goto :goto_3a

    :cond_67
    const-string v0, "skipped"

    .line 227
    invoke-virtual {v7, v0}, Lorg/json/JSONObject;->getJSONArray(Ljava/lang/String;)Lorg/json/JSONArray;

    move-result-object v4

    invoke-virtual {v4}, Lorg/json/JSONArray;->length()I

    move-result v4

    const-string v5, "\n\u4fdd\u7559\u65e0\u6cd5\u786e\u8ba4\u5197\u4f59\u7684\u9879\u76ee\uff1a"

    .line 228
    invoke-virtual {v1, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1, v4}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    const-string v5, " \u9879\u3002\n\u52fe\u9009\u8981\u6e05\u7406\u7684\u7c7b\u522b\uff0c\u6267\u884c\u524d\u4f1a\u91cd\u65b0\u6838\u9a8c\u3002"

    invoke-virtual {v1, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const/4 v5, 0x0

    :goto_7f
    const/4 v12, 0x3

    .line 229
    invoke-static {v4, v12}, Ljava/lang/Math;->min(II)I

    move-result v12

    if-ge v5, v12, :cond_97

    invoke-virtual {v1, v9}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v7, v0}, Lorg/json/JSONObject;->getJSONArray(Ljava/lang/String;)Lorg/json/JSONArray;

    move-result-object v12

    invoke-virtual {v12, v5}, Lorg/json/JSONArray;->getString(I)Ljava/lang/String;

    move-result-object v12

    invoke-virtual {v1, v12}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    add-int/lit8 v5, v5, 0x1

    goto :goto_7f

    .line 230
    :cond_97
    invoke-virtual {v6}, Lorg/json/JSONArray;->length()I

    move-result v0

    new-array v4, v0, [Ljava/lang/String;

    invoke-virtual {v6}, Lorg/json/JSONArray;->length()I

    move-result v0

    new-array v5, v0, [Z

    const-wide/16 v12, 0x0

    const/4 v0, 0x0

    .line 232
    :goto_a6
    invoke-virtual {v6}, Lorg/json/JSONArray;->length()I

    move-result v9

    if-ge v0, v9, :cond_10f

    invoke-virtual {v6, v0}, Lorg/json/JSONArray;->getJSONObject(I)Lorg/json/JSONObject;

    move-result-object v9

    invoke-virtual {v9, v11}, Lorg/json/JSONObject;->getLong(Ljava/lang/String;)J

    move-result-wide v14

    add-long/2addr v12, v14

    .line 233
    new-instance v14, Ljava/lang/StringBuilder;

    invoke-direct {v14}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v9, v10}, Lorg/json/JSONObject;->getString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v15

    invoke-virtual {v14, v15}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v15, " \u00b7 "

    invoke-virtual {v14, v15}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v15, "count"

    invoke-virtual {v9, v15}, Lorg/json/JSONObject;->getInt(Ljava/lang/String;)I

    move-result v3

    invoke-virtual {v14, v3}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    const-string v3, " \u9879 \u00b7 \u7ea6 "

    invoke-virtual {v14, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v9, v11}, Lorg/json/JSONObject;->getLong(Ljava/lang/String;)J

    move-result-wide v2

    invoke-direct {v8, v2, v3}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->storageSize(J)Ljava/lang/String;

    move-result-object v2

    invoke-virtual {v14, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v14}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v2

    aput-object v2, v4, v0

    const-string v2, "id"

    .line 234
    invoke-virtual {v9, v2}, Lorg/json/JSONObject;->getString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v3

    const-string v14, "duplicates"

    invoke-virtual {v3, v14}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v3

    if-nez v3, :cond_ff

    invoke-virtual {v9, v2}, Lorg/json/JSONObject;->getString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v2

    const-string v3, "diy_cache"

    invoke-virtual {v2, v3}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v2

    if-eqz v2, :cond_107

    :cond_ff
    invoke-virtual {v9, v15}, Lorg/json/JSONObject;->getInt(Ljava/lang/String;)I

    move-result v2

    if-lez v2, :cond_107

    const/4 v2, 0x1

    goto :goto_108

    :cond_107
    const/4 v2, 0x0

    :goto_108
    aput-boolean v2, v5, v0

    add-int/lit8 v0, v0, 0x1

    move/from16 v2, p1

    goto :goto_a6

    .line 236
    :cond_10f
    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v3

    .line 237
    new-instance v9, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda46;

    move-object v0, v9

    move-object/from16 v1, p0

    move/from16 v2, p1

    invoke-direct/range {v0 .. v7}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda46;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;ILjava/lang/String;[Ljava/lang/String;[ZLorg/json/JSONArray;Lorg/json/JSONObject;)V

    invoke-virtual {v8, v9}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->runOnUiThread(Ljava/lang/Runnable;)V

    .line 256
    new-instance v0, Ljava/lang/StringBuilder;

    const-string v1, "\u626b\u63cf\u5b8c\u6210\uff0c\u53ef\u56de\u6536\u7ea6 "

    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-direct {v8, v12, v13}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->storageSize(J)Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v1, "\uff1b\u7b49\u5f85\u9009\u62e9\u548c\u786e\u8ba4\u3002"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method

.method synthetic lambda$render$10$org-efootballrevival-runtimeprobe-GatewayBootActivity()Ljava/lang/String;
    .registers 4
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation

    .line 160
    new-instance v0, Lorg/json/JSONObject;

    const-string v1, "summary"

    const-string v2, ""

    invoke-static {p0, v1, v2}, Lorg/efootballrevival/runtimeprobe/EmbeddedGateway;->manage(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    invoke-direct {v0, v1}, Lorg/json/JSONObject;-><init>(Ljava/lang/String;)V

    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "\u5df2\u6301\u6709 "

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    const-string v2, "players"

    invoke-virtual {v0, v2}, Lorg/json/JSONObject;->getInt(Ljava/lang/String;)I

    move-result v2

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    const-string v2, " \u540d\u7403\u5458 \u00b7 "

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v2, "squads"

    invoke-virtual {v0, v2}, Lorg/json/JSONObject;->getInt(Ljava/lang/String;)I

    move-result v0

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    const-string v0, " \u5957\u9635\u5bb9"

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lorg/efootballrevival/runtimeprobe/UiStrings;->t(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method

.method synthetic lambda$render$11$org-efootballrevival-runtimeprobe-GatewayBootActivity()V
    .registers 2

    .line 0
    const/4 v0, 0x0

    .line 162
    invoke-direct {p0, v0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->prepare(Z)V

    return-void
.end method

.method synthetic lambda$render$12$org-efootballrevival-runtimeprobe-GatewayBootActivity()V
    .registers 2

    .line 0
    const/4 v0, 0x1

    .line 162
    invoke-direct {p0, v0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->render(Z)V

    return-void
.end method

.method synthetic lambda$render$13$org-efootballrevival-runtimeprobe-GatewayBootActivity()V
    .registers 2

    .line 163
    sget-boolean v0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->gameEntered:Z

    if-eqz v0, :cond_a

    const-string v0, "\u8bf7\u5173\u95ed\u6e38\u620f\u5e76\u91cd\u65b0\u6253\u5f00\uff0c\u518d\u7f16\u8f91\u7403\u5458\u3002"

    invoke-direct {p0, v0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->message(Ljava/lang/String;)V

    return-void

    :cond_a
    invoke-static {p0}, Lorg/efootballrevival/runtimeprobe/PlayerEditorPanel;->show(Landroid/app/Activity;)V

    return-void
.end method

.method synthetic lambda$render$14$org-efootballrevival-runtimeprobe-GatewayBootActivity()V
    .registers 2

    .line 165
    sget-boolean v0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->gameEntered:Z

    if-eqz v0, :cond_a

    const-string v0, "\u8bf7\u5173\u95ed\u6e38\u620f\u5e76\u91cd\u65b0\u6253\u5f00\uff0c\u518d\u4f7f\u7528\u5236\u5361\u5668\u3002"

    invoke-direct {p0, v0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->message(Ljava/lang/String;)V

    return-void

    :cond_a
    invoke-static {p0}, Lorg/efootballrevival/runtimeprobe/CardDesignerPanel;->show(Landroid/app/Activity;)V

    return-void
.end method

.method synthetic lambda$render$15$org-efootballrevival-runtimeprobe-GatewayBootActivity()V
    .registers 2

    .line 0
    const/4 v0, 0x1

    .line 167
    invoke-direct {p0, v0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->prepare(Z)V

    return-void
.end method

.method synthetic lambda$render$16$org-efootballrevival-runtimeprobe-GatewayBootActivity()V
    .registers 4

    .line 167
    new-instance v0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda19;

    invoke-direct {v0, p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda19;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;)V

    const-string v1, "\u4fee\u590d\u8d44\u6e90"

    const-string v2, "\u4ec5\u5728\u8d44\u6e90\u5f02\u5e38\u65f6\u4f7f\u7528\uff0c\u5c06\u5b8c\u6574\u6821\u9a8c\u5e76\u4fee\u590d\u8d44\u6e90\u3002\u5b58\u6863\u4fdd\u7559\uff1b\u7f3a\u5931\u6587\u4ef6\u53ef\u80fd\u9700\u8981\u79bb\u7ebf\u8d44\u6e90\u5305\u3002"

    invoke-direct {p0, v1, v2, v0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->confirm(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Runnable;)V

    return-void
.end method

.method synthetic lambda$render$17$org-efootballrevival-runtimeprobe-GatewayBootActivity(ILjava/lang/String;)V
    .registers 4

    .line 172
    iget v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->renderEpoch:I

    if-ne p1, v0, :cond_15

    iget-boolean p1, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->cancelled:Z

    if-nez p1, :cond_15

    iget-boolean p1, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->manager:Z

    if-nez p1, :cond_15

    iget-object p1, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->status:Landroid/widget/TextView;

    invoke-static {p2}, Lorg/efootballrevival/runtimeprobe/UiStrings;->t(Ljava/lang/String;)Ljava/lang/String;

    move-result-object p2

    invoke-virtual {p1, p2}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    :cond_15
    return-void
.end method

.method synthetic lambda$render$18$org-efootballrevival-runtimeprobe-GatewayBootActivity(I)V
    .registers 3

    .line 172
    iget v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->renderEpoch:I

    if-ne p1, v0, :cond_17

    iget-boolean p1, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->cancelled:Z

    if-nez p1, :cond_17

    iget-boolean p1, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->manager:Z

    if-nez p1, :cond_17

    iget-object p1, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->status:Landroid/widget/TextView;

    const-string v0, "\u8d44\u6e90\u7f3a\u5931 \u00b7 \u8bf7\u5b89\u88c5\u914d\u5957\u79bb\u7ebf\u8d44\u6e90\u5305\u540e\u91cd\u8bd5\u3002"

    invoke-static {v0}, Lorg/efootballrevival/runtimeprobe/UiStrings;->t(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    invoke-virtual {p1, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    :cond_17
    return-void
.end method

.method synthetic lambda$render$19$org-efootballrevival-runtimeprobe-GatewayBootActivity(I)V
    .registers 4

    .line 172
    :try_start_0
    invoke-static {p0}, Lorg/efootballrevival/runtimeprobe/EmbeddedResources;->inspect(Landroid/content/Context;)Ljava/lang/String;

    move-result-object v0

    new-instance v1, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda35;

    invoke-direct {v1, p0, p1, v0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda35;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;ILjava/lang/String;)V

    invoke-virtual {p0, v1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->runOnUiThread(Ljava/lang/Runnable;)V
    :try_end_c
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_c} :catch_d

    goto :goto_15

    :catch_d
    new-instance v0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda36;

    invoke-direct {v0, p0, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda36;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;I)V

    invoke-virtual {p0, v0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->runOnUiThread(Ljava/lang/Runnable;)V

    :goto_15
    return-void
.end method

.method synthetic lambda$render$20$org-efootballrevival-runtimeprobe-GatewayBootActivity(Landroid/view/View;)V
    .registers 4

    .line 178
    :try_start_0
    new-instance p1, Landroid/content/Intent;

    const-string v0, "android.intent.action.VIEW"

    const-string v1, "https://t.me/efootball_73"

    invoke-static {v1}, Landroid/net/Uri;->parse(Ljava/lang/String;)Landroid/net/Uri;

    move-result-object v1

    invoke-direct {p1, v0, v1}, Landroid/content/Intent;-><init>(Ljava/lang/String;Landroid/net/Uri;)V

    invoke-virtual {p0, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->startActivity(Landroid/content/Intent;)V
    :try_end_10
    .catch Landroid/content/ActivityNotFoundException; {:try_start_0 .. :try_end_10} :catch_11

    goto :goto_16

    :catch_11
    const-string p1, "\u8bf7\u901a\u8fc7\u6d4f\u89c8\u5668\u8bbf\u95ee t.me/efootball_73"

    invoke-direct {p0, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->message(Ljava/lang/String;)V

    :goto_16
    return-void
.end method

.method synthetic lambda$render$5$org-efootballrevival-runtimeprobe-GatewayBootActivity()Ljava/lang/String;
    .registers 4
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation

    .line 152
    new-instance v0, Lorg/json/JSONObject;

    const-string v1, "max_level"

    const-string v2, ""

    invoke-static {p0, v1, v2}, Lorg/efootballrevival/runtimeprobe/EmbeddedGateway;->manage(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    invoke-direct {v0, v1}, Lorg/json/JSONObject;-><init>(Ljava/lang/String;)V

    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "\u5df2\u5347\u7ea7 "

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    const-string v2, "changed"

    invoke-virtual {v0, v2}, Lorg/json/JSONObject;->getInt(Ljava/lang/String;)I

    move-result v2

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    const-string v2, " \u540d\u7403\u5458\uff0c\u81ea\u52a8\u52a0\u70b9 "

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v2, "allocated"

    invoke-virtual {v0, v2}, Lorg/json/JSONObject;->getInt(Ljava/lang/String;)I

    move-result v0

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    const-string v0, " \u540d\u3002"

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method

.method synthetic lambda$render$6$org-efootballrevival-runtimeprobe-GatewayBootActivity()V
    .registers 2

    .line 151
    new-instance v0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda51;

    invoke-direct {v0, p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda51;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;)V

    invoke-direct {p0, v0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->task(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$Work;)V

    return-void
.end method

.method synthetic lambda$render$7$org-efootballrevival-runtimeprobe-GatewayBootActivity()V
    .registers 4

    .line 151
    new-instance v0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda43;

    invoke-direct {v0, p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda43;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;)V

    const-string v1, "\u672a\u6ee1\u7ea7\u7403\u5458\u5347\u7ea7\u5e76\u52a0\u70b9"

    const-string v2, "\u4ec5\u5c06\u672a\u6ee1\u7ea7\u7684\u5df2\u6301\u6709\u7403\u5458\uff08\u542b\u50a8\u5907\uff09\u5347\u81f3\u7b49\u7ea7\u4e0a\u9650\uff0c\u5e76\u6309\u4f4d\u7f6e\u91cd\u65b0\u81ea\u52a8\u5206\u914d\u80fd\u529b\u70b9\uff0c\u8986\u76d6\u8fd9\u4e9b\u7403\u5458\u539f\u6709\u624b\u52a8\u52a0\u70b9\uff1b\u5df2\u6ee1\u7ea7\u7403\u5458\u5b8c\u5168\u8df3\u8fc7\uff0c\u4fdd\u7559\u73b0\u6709\u52a0\u70b9\u548c\u5269\u4f59\u70b9\u6570\u3002\u6280\u80fd\u3001\u589e\u80fd\u4e0e\u9635\u5bb9\u4fdd\u7559\u3002\u64cd\u4f5c\u524d\u81ea\u52a8\u5907\u4efd\u3002"

    invoke-direct {p0, v1, v2, v0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->confirm(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Runnable;)V

    return-void
.end method

.method synthetic lambda$render$8$org-efootballrevival-runtimeprobe-GatewayBootActivity()V
    .registers 3

    .line 155
    new-instance v0, Landroid/content/Intent;

    const-string v1, "android.intent.action.OPEN_DOCUMENT"

    invoke-direct {v0, v1}, Landroid/content/Intent;-><init>(Ljava/lang/String;)V

    const-string v1, "android.intent.category.OPENABLE"

    invoke-virtual {v0, v1}, Landroid/content/Intent;->addCategory(Ljava/lang/String;)Landroid/content/Intent;

    const-string v1, "*/*"

    invoke-virtual {v0, v1}, Landroid/content/Intent;->setType(Ljava/lang/String;)Landroid/content/Intent;

    const/16 v1, 0xc

    :try_start_13
    iput v1, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->pickerRequest:I

    invoke-virtual {p0, v0, v1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->startActivityForResult(Landroid/content/Intent;I)V
    :try_end_18
    .catch Landroid/content/ActivityNotFoundException; {:try_start_13 .. :try_end_18} :catch_19

    goto :goto_21

    :catch_19
    const/4 v0, 0x0

    iput v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->pickerRequest:I

    const-string v0, "\u8bf7\u542f\u7528\u7cfb\u7edf\u6587\u4ef6\u7ba1\u7406\u5668\u540e\u91cd\u8bd5\u3002"

    invoke-direct {p0, v0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->message(Ljava/lang/String;)V

    :goto_21
    return-void
.end method

.method synthetic lambda$render$9$org-efootballrevival-runtimeprobe-GatewayBootActivity()V
    .registers 2

    .line 0
    const/4 v0, 0x0

    .line 157
    invoke-direct {p0, v0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->render(Z)V

    return-void
.end method

.method synthetic lambda$requestGameLaunch$0$org-efootballrevival-runtimeprobe-GatewayBootActivity(Ljava/lang/Runnable;)V
    .registers 3

    .line 27
    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->telegramMembership:Lorg/efootballrevival/runtimeprobe/TelegramMembershipGate;

    if-nez v0, :cond_b

    new-instance v0, Lorg/efootballrevival/runtimeprobe/TelegramMembershipGate;

    invoke-direct {v0, p0}, Lorg/efootballrevival/runtimeprobe/TelegramMembershipGate;-><init>(Landroid/app/Activity;)V

    iput-object v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->telegramMembership:Lorg/efootballrevival/runtimeprobe/TelegramMembershipGate;

    .line 28
    :cond_b
    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->telegramMembership:Lorg/efootballrevival/runtimeprobe/TelegramMembershipGate;

    invoke-virtual {v0, p1}, Lorg/efootballrevival/runtimeprobe/TelegramMembershipGate;->request(Ljava/lang/Runnable;)V

    return-void
.end method

.method synthetic lambda$runStorageClean$32$org-efootballrevival-runtimeprobe-GatewayBootActivity([ZLorg/json/JSONArray;Lorg/json/JSONObject;)Ljava/lang/String;
    .registers 8
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation

    .line 262
    new-instance v0, Lorg/json/JSONArray;

    invoke-direct {v0}, Lorg/json/JSONArray;-><init>()V

    const/4 v1, 0x0

    .line 263
    :goto_6
    array-length v2, p1

    if-ge v1, v2, :cond_29

    aget-boolean v2, p1, v1

    if-eqz v2, :cond_26

    invoke-virtual {p2, v1}, Lorg/json/JSONArray;->getJSONObject(I)Lorg/json/JSONObject;

    move-result-object v2

    const-string v3, "count"

    invoke-virtual {v2, v3}, Lorg/json/JSONObject;->getInt(Ljava/lang/String;)I

    move-result v2

    if-lez v2, :cond_26

    invoke-virtual {p2, v1}, Lorg/json/JSONArray;->getJSONObject(I)Lorg/json/JSONObject;

    move-result-object v2

    const-string v3, "id"

    invoke-virtual {v2, v3}, Lorg/json/JSONObject;->getString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v2

    invoke-virtual {v0, v2}, Lorg/json/JSONArray;->put(Ljava/lang/Object;)Lorg/json/JSONArray;

    :cond_26
    add-int/lit8 v1, v1, 0x1

    goto :goto_6

    .line 264
    :cond_29
    invoke-virtual {v0}, Lorg/json/JSONArray;->length()I

    move-result p1

    if-nez p1, :cond_32

    const-string p1, "\u6ca1\u6709\u9009\u4e2d\u53ef\u6e05\u7406\u9879\u76ee\u3002"

    return-object p1

    .line 265
    :cond_32
    new-instance p1, Lorg/json/JSONObject;

    invoke-direct {p1}, Lorg/json/JSONObject;-><init>()V

    const-string p2, "token"

    invoke-virtual {p3, p2}, Lorg/json/JSONObject;->getString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object p3

    invoke-virtual {p1, p2, p3}, Lorg/json/JSONObject;->put(Ljava/lang/String;Ljava/lang/Object;)Lorg/json/JSONObject;

    const-string p2, "categories"

    invoke-virtual {p1, p2, v0}, Lorg/json/JSONObject;->put(Ljava/lang/String;Ljava/lang/Object;)Lorg/json/JSONObject;

    .line 266
    new-instance p2, Lorg/json/JSONObject;

    const-string p3, "clean"

    invoke-virtual {p1}, Lorg/json/JSONObject;->toString()Ljava/lang/String;

    move-result-object p1

    invoke-static {p0, p3, p1}, Lorg/efootballrevival/runtimeprobe/EmbeddedGateway;->storage(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object p1

    invoke-direct {p2, p1}, Lorg/json/JSONObject;-><init>(Ljava/lang/String;)V

    .line 267
    new-instance p1, Ljava/lang/StringBuilder;

    const-string p3, "\u5df2\u6e05\u7406 "

    invoke-direct {p1, p3}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    const-string p3, "removed"

    invoke-virtual {p2, p3}, Lorg/json/JSONObject;->getInt(Ljava/lang/String;)I

    move-result p3

    invoke-virtual {p1, p3}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    const-string p3, " \u9879\uff0c\u9884\u8ba1\u91ca\u653e "

    invoke-virtual {p1, p3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string p3, "releasedBytes"

    invoke-virtual {p2, p3}, Lorg/json/JSONObject;->getLong(Ljava/lang/String;)J

    move-result-wide p2

    invoke-direct {p0, p2, p3}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->storageSize(J)Ljava/lang/String;

    move-result-object p2

    invoke-virtual {p1, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string p2, "\u3002\n\u4f5c\u54c1\u3001\u5b58\u6863\u548c\u5f53\u524d\u8d44\u6e90\u4fdd\u7559\uff1b\u7cfb\u7edf\u5b58\u50a8\u7edf\u8ba1\u53ef\u80fd\u5ef6\u8fdf\u5237\u65b0\u3002"

    invoke-virtual {p1, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {p1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1

    return-object p1
.end method

.method synthetic lambda$task$33$org-efootballrevival-runtimeprobe-GatewayBootActivity(ZZLjava/lang/String;)V
    .registers 6

    .line 0
    const/4 v0, 0x0

    .line 276
    iput-boolean v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->busy:Z

    iget-boolean v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->cancelled:Z

    if-eqz v0, :cond_8

    return-void

    :cond_8
    const/4 v0, 0x1

    invoke-direct {p0, v0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->setEnabled(Z)V

    if-eqz p1, :cond_1d

    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->status:Landroid/widget/TextView;

    if-eqz p2, :cond_14

    move-object v1, p3

    goto :goto_16

    :cond_14
    const-string v1, "\u5b58\u6863\u8bfb\u53d6\u672a\u5b8c\u6210\uff0c\u8bf7\u8fd4\u56de\u540e\u91cd\u8bd5\u3002"

    :goto_16
    invoke-static {v1}, Lorg/efootballrevival/runtimeprobe/UiStrings;->t(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    :cond_1d
    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->progress:Landroid/widget/TextView;

    if-eqz p1, :cond_25

    if-eqz p2, :cond_25

    const-string p3, ""

    :cond_25
    invoke-static {p3}, Lorg/efootballrevival/runtimeprobe/UiStrings;->t(Ljava/lang/String;)Ljava/lang/String;

    move-result-object p1

    invoke-virtual {v0, p1}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    invoke-virtual {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->getWindow()Landroid/view/Window;

    move-result-object p1

    const/16 p2, 0x80

    invoke-virtual {p1, p2}, Landroid/view/Window;->clearFlags(I)V

    return-void
.end method

.method synthetic lambda$task$34$org-efootballrevival-runtimeprobe-GatewayBootActivity(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$Work;Z)V
    .registers 5

    .line 275
    :try_start_0
    invoke-interface {p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$Work;->run()Ljava/lang/String;

    move-result-object p1
    :try_end_4
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_4} :catch_6

    const/4 v0, 0x1

    goto :goto_2d

    :catch_6
    move-exception p1

    const-string v0, "V9_SAVE"

    const-string v1, "operation failed"

    invoke-static {v0, v1, p1}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I

    const-string v0, "native-action"

    invoke-static {p0, v0, v1, p1}, Lorg/efootballrevival/runtimeprobe/DiagnosticLog;->record(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)V

    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    const-string v1, "\u64cd\u4f5c\u672a\u5b8c\u6210\uff0c\u8bf7\u91cd\u8bd5\u3002\n"

    invoke-static {v1}, Lorg/efootballrevival/runtimeprobe/UiStrings;->t(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-direct {p0, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->friendly(Ljava/lang/Exception;)Ljava/lang/String;

    move-result-object p1

    invoke-virtual {v0, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1

    const/4 v0, 0x0

    .line 276
    :goto_2d
    new-instance v1, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda54;

    invoke-direct {v1, p0, p2, v0, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda54;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;ZZLjava/lang/String;)V

    invoke-virtual {p0, v1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->runOnUiThread(Ljava/lang/Runnable;)V

    return-void
.end method

.method protected onActivityResult(IILandroid/content/Intent;)V
    .registers 7

    .line 299
    invoke-super {p0, p1, p2, p3}, Landroid/app/Activity;->onActivityResult(IILandroid/content/Intent;)V

    .line 300
    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->diagnostics:Lorg/efootballrevival/runtimeprobe/DiagnosticExport;

    invoke-virtual {v0, p1, p2, p3}, Lorg/efootballrevival/runtimeprobe/DiagnosticExport;->onActivityResult(IILandroid/content/Intent;)Z

    move-result v0

    if-eqz v0, :cond_c

    return-void

    .line 301
    :cond_c
    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->launcherWeb:Lorg/efootballrevival/runtimeprobe/LauncherWeb;

    if-eqz v0, :cond_17

    invoke-virtual {v0, p1, p2, p3}, Lorg/efootballrevival/runtimeprobe/LauncherWeb;->onActivityResult(IILandroid/content/Intent;)Z

    move-result v0

    if-eqz v0, :cond_17

    return-void

    .line 302
    :cond_17
    invoke-static {p0, p1, p2, p3}, Lorg/efootballrevival/runtimeprobe/CardDesignerPanel;->onActivityResult(Landroid/app/Activity;IILandroid/content/Intent;)Z

    move-result v0

    if-eqz v0, :cond_1e

    return-void

    :cond_1e
    const/16 v0, 0xc

    const/16 v1, 0xb

    if-eq p1, v1, :cond_27

    if-eq p1, v0, :cond_27

    return-void

    :cond_27
    const/4 v2, 0x0

    .line 304
    iput v2, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->pickerRequest:I

    const/4 v2, -0x1

    if-ne p2, v2, :cond_53

    if-eqz p3, :cond_53

    .line 305
    invoke-virtual {p3}, Landroid/content/Intent;->getData()Landroid/net/Uri;

    move-result-object p2

    if-nez p2, :cond_36

    goto :goto_53

    .line 306
    :cond_36
    invoke-virtual {p3}, Landroid/content/Intent;->getData()Landroid/net/Uri;

    move-result-object p2

    if-ne p1, v1, :cond_44

    .line 307
    new-instance p3, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda23;

    invoke-direct {p3, p0, p2}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda23;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;Landroid/net/Uri;)V

    invoke-direct {p0, p3}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->task(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$Work;)V

    :cond_44
    if-ne p1, v0, :cond_52

    .line 311
    new-instance p1, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda24;

    invoke-direct {p1, p0, p2}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda24;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;Landroid/net/Uri;)V

    const-string p2, "\u5bfc\u5165\u5b58\u6863"

    const-string p3, "\u5c06\u66ff\u6362\u5f53\u524d\u8fdb\u5ea6\uff0c\u5bfc\u5165\u524d\u81ea\u52a8\u5907\u4efd\uff1b\u8d44\u6e90\u6587\u4ef6\u4fdd\u7559\u3002\u786e\u5b9a\u5bfc\u5165\uff1f"

    invoke-direct {p0, p2, p3, p1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->confirm(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Runnable;)V

    :cond_52
    return-void

    :cond_53
    :goto_53
    if-ne p1, v1, :cond_5c

    .line 305
    iget-object p1, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->exported:Ljava/io/File;

    if-eqz p1, :cond_5c

    invoke-virtual {p1}, Ljava/io/File;->delete()Z

    :cond_5c
    return-void
.end method

.method public onBackPressed()V
    .registers 1

    .line 339
    invoke-direct {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->handleBack()V

    return-void
.end method

.method public onCreate(Landroid/os/Bundle;)V
    .registers 7

    const-string v0, "V9_BOOT"

    const v1, 0x103022e

    .line 44
    invoke-virtual {p0, v1}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->setTheme(I)V

    .line 45
    invoke-super {p0, p1}, Landroid/app/Activity;->onCreate(Landroid/os/Bundle;)V

    .line 46
    invoke-static {p0}, Lorg/efootballrevival/runtimeprobe/DiagnosticLog;->install(Landroid/content/Context;)V

    .line 47
    new-instance v1, Lorg/efootballrevival/runtimeprobe/DiagnosticExport;

    invoke-direct {v1, p0, p1}, Lorg/efootballrevival/runtimeprobe/DiagnosticExport;-><init>(Landroid/app/Activity;Landroid/os/Bundle;)V

    iput-object v1, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->diagnostics:Lorg/efootballrevival/runtimeprobe/DiagnosticExport;

    const-string v1, "ui-language"

    const/4 v2, 0x0

    .line 48
    invoke-virtual {p0, v1, v2}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->getSharedPreferences(Ljava/lang/String;I)Landroid/content/SharedPreferences;

    move-result-object v1

    const-string v3, "language"

    const-string v4, "zh-CN"

    invoke-interface {v1, v3, v4}, Landroid/content/SharedPreferences;->getString(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    invoke-static {v1}, Lorg/efootballrevival/runtimeprobe/UiStrings;->setLanguage(Ljava/lang/String;)V

    .line 49
    invoke-virtual {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->getWindow()Landroid/view/Window;

    move-result-object v1

    const v3, -0xe6e5db

    invoke-virtual {v1, v3}, Landroid/view/Window;->setStatusBarColor(I)V

    invoke-virtual {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->getWindow()Landroid/view/Window;

    move-result-object v1

    invoke-virtual {v1, v3}, Landroid/view/Window;->setNavigationBarColor(I)V

    .line 50
    invoke-virtual {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->getWindow()Landroid/view/Window;

    move-result-object v1

    invoke-virtual {v1}, Landroid/view/Window;->getDecorView()Landroid/view/View;

    move-result-object v1

    invoke-virtual {v1, v2}, Landroid/view/View;->setSystemUiVisibility(I)V

    if-eqz p1, :cond_6e

    const-string v1, "save-picker"

    .line 52
    invoke-virtual {p1, v1, v2}, Landroid/os/Bundle;->getInt(Ljava/lang/String;I)I

    move-result v1

    iput v1, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->pickerRequest:I

    const-string v1, "save-export"

    const-string v3, ""

    .line 53
    invoke-virtual {p1, v1, v3}, Landroid/os/Bundle;->getString(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    const-string v3, "export-[0-9]+\\.efsave"

    .line 54
    invoke-virtual {v1, v3}, Ljava/lang/String;->matches(Ljava/lang/String;)Z

    move-result v3

    if-eqz v3, :cond_6e

    .line 55
    new-instance v3, Ljava/io/File;

    invoke-virtual {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->getCacheDir()Ljava/io/File;

    move-result-object v4

    invoke-direct {v3, v4, v1}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V

    invoke-virtual {v3}, Ljava/io/File;->isFile()Z

    move-result v1

    if-eqz v1, :cond_6e

    iput-object v3, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->exported:Ljava/io/File;

    :cond_6e
    const/4 v1, 0x0

    .line 58
    :try_start_6f
    new-instance v3, Lorg/efootballrevival/runtimeprobe/LauncherWeb;

    new-instance v4, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda40;

    invoke-direct {v4, p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda40;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;)V

    invoke-direct {v3, p0, v4}, Lorg/efootballrevival/runtimeprobe/LauncherWeb;-><init>(Landroid/app/Activity;Lorg/efootballrevival/runtimeprobe/LauncherWeb$Fallback;)V

    iput-object v3, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->launcherWeb:Lorg/efootballrevival/runtimeprobe/LauncherWeb;
    :try_end_7b
    .catch Ljava/lang/RuntimeException; {:try_start_6f .. :try_end_7b} :catch_7c

    goto :goto_92

    :catch_7c
    move-exception v3

    const-string v4, "HTML launcher unavailable, using native screen"

    .line 59
    invoke-static {v0, v4, v3}, Landroid/util/Log;->w(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I

    iput-object v1, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->launcherWeb:Lorg/efootballrevival/runtimeprobe/LauncherWeb;

    if-eqz p1, :cond_8f

    const-string v3, "save-manager"

    invoke-virtual {p1, v3, v2}, Landroid/os/Bundle;->getBoolean(Ljava/lang/String;Z)Z

    move-result p1

    if-eqz p1, :cond_8f

    const/4 v2, 0x1

    :cond_8f
    invoke-direct {p0, v2}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->render(Z)V

    .line 60
    :goto_92
    sget p1, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v2, 0x21

    if-lt p1, v2, :cond_a7

    .line 61
    :try_start_98
    invoke-static {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$BackHook;->register(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;)Ljava/lang/Object;

    move-result-object p1

    iput-object p1, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->backCallback:Ljava/lang/Object;
    :try_end_9e
    .catch Ljava/lang/RuntimeException; {:try_start_98 .. :try_end_9e} :catch_9f

    goto :goto_a7

    :catch_9f
    move-exception p1

    const-string v2, "back callback unavailable"

    invoke-static {v0, v2, p1}, Landroid/util/Log;->w(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I

    iput-object v1, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->backCallback:Ljava/lang/Object;

    .line 65
    :cond_a7
    :goto_a7
    invoke-virtual {p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->getWindow()Landroid/view/Window;

    move-result-object p1

    invoke-virtual {p1}, Landroid/view/Window;->getDecorView()Landroid/view/View;

    move-result-object p1

    new-instance v0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda41;

    invoke-direct {v0, p0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$$ExternalSyntheticLambda41;-><init>(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;)V

    invoke-virtual {p1, v0}, Landroid/view/View;->post(Ljava/lang/Runnable;)Z

    return-void
.end method

.method protected onDestroy()V
    .registers 3

    .line 355
    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->backCallback:Ljava/lang/Object;

    if-eqz v0, :cond_12

    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v1, 0x21

    if-lt v0, v1, :cond_12

    :try_start_a
    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->backCallback:Ljava/lang/Object;

    invoke-static {p0, v0}, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity$BackHook;->unregister(Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;Ljava/lang/Object;)V
    :try_end_f
    .catch Ljava/lang/RuntimeException; {:try_start_a .. :try_end_f} :catch_f

    :catch_f
    const/4 v0, 0x0

    iput-object v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->backCallback:Ljava/lang/Object;

    .line 356
    :cond_12
    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->antiScam:Lorg/efootballrevival/runtimeprobe/AntiScamGate;

    if-eqz v0, :cond_19

    invoke-virtual {v0}, Lorg/efootballrevival/runtimeprobe/AntiScamGate;->destroy()V

    :cond_19
    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->telegramMembership:Lorg/efootballrevival/runtimeprobe/TelegramMembershipGate;

    if-eqz v0, :cond_20

    invoke-virtual {v0}, Lorg/efootballrevival/runtimeprobe/TelegramMembershipGate;->destroy()V

    :cond_20
    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->launcherWeb:Lorg/efootballrevival/runtimeprobe/LauncherWeb;

    if-eqz v0, :cond_27

    invoke-virtual {v0}, Lorg/efootballrevival/runtimeprobe/LauncherWeb;->destroy()V

    :cond_27
    invoke-static {p0}, Lorg/efootballrevival/runtimeprobe/CardDesignerPanel;->destroy(Landroid/app/Activity;)V

    const/4 v0, 0x1

    iput-boolean v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->cancelled:Z

    invoke-super {p0}, Landroid/app/Activity;->onDestroy()V

    return-void
.end method

.method protected onPause()V
    .registers 2

    .line 353
    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->telegramMembership:Lorg/efootballrevival/runtimeprobe/TelegramMembershipGate;

    if-eqz v0, :cond_7

    invoke-virtual {v0}, Lorg/efootballrevival/runtimeprobe/TelegramMembershipGate;->pause()V

    :cond_7
    invoke-super {p0}, Landroid/app/Activity;->onPause()V

    return-void
.end method

.method protected onResume()V
    .registers 2

    .line 352
    invoke-super {p0}, Landroid/app/Activity;->onResume()V

    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->telegramMembership:Lorg/efootballrevival/runtimeprobe/TelegramMembershipGate;

    if-eqz v0, :cond_a

    invoke-virtual {v0}, Lorg/efootballrevival/runtimeprobe/TelegramMembershipGate;->resume()V

    :cond_a
    return-void
.end method

.method protected onSaveInstanceState(Landroid/os/Bundle;)V
    .registers 4

    const-string v0, "save-manager"

    .line 79
    iget-boolean v1, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->manager:Z

    invoke-virtual {p1, v0, v1}, Landroid/os/Bundle;->putBoolean(Ljava/lang/String;Z)V

    const-string v0, "save-picker"

    iget v1, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->pickerRequest:I

    invoke-virtual {p1, v0, v1}, Landroid/os/Bundle;->putInt(Ljava/lang/String;I)V

    .line 80
    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->exported:Ljava/io/File;

    if-eqz v0, :cond_1b

    const-string v1, "save-export"

    invoke-virtual {v0}, Ljava/io/File;->getName()Ljava/lang/String;

    move-result-object v0

    invoke-virtual {p1, v1, v0}, Landroid/os/Bundle;->putString(Ljava/lang/String;Ljava/lang/String;)V

    .line 81
    :cond_1b
    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/GatewayBootActivity;->diagnostics:Lorg/efootballrevival/runtimeprobe/DiagnosticExport;

    invoke-virtual {v0, p1}, Lorg/efootballrevival/runtimeprobe/DiagnosticExport;->saveState(Landroid/os/Bundle;)V

    .line 82
    invoke-super {p0, p1}, Landroid/app/Activity;->onSaveInstanceState(Landroid/os/Bundle;)V

    return-void
.end method

.method requestGameLaunch(Ljava/lang/Runnable;)V
    .registers 2

    # RC29.2: V32 Telegram / anti-scam prompts removed; the RC26 launcher hides them and the game never starts.
    invoke-interface {p1}, Ljava/lang/Runnable;->run()V

    return-void
.end method
