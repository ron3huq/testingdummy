.class public final Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;
.super Ljava/lang/Object;
.source "SinglePlayerInMatch.java"


# static fields
.field private static final attached:Ljava/util/WeakHashMap;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/WeakHashMap<",
            "Landroid/app/Activity;",
            "Ljava/lang/ref/WeakReference<",
            "Landroid/widget/Button;",
            ">;>;"
        }
    .end annotation
.end field

.field private static final waiting:Ljava/util/WeakHashMap;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/WeakHashMap<",
            "Landroid/widget/Button;",
            "Ljava/lang/Boolean;",
            ">;"
        }
    .end annotation
.end field

.field private static final waitingSince:Ljava/util/WeakHashMap;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/WeakHashMap<",
            "Landroid/widget/Button;",
            "Ljava/lang/Long;",
            ">;"
        }
    .end annotation
.end field


# direct methods
.method static constructor <clinit>()V
    .registers 1

    .line 15
    new-instance v0, Ljava/util/WeakHashMap;

    invoke-direct {v0}, Ljava/util/WeakHashMap;-><init>()V

    sput-object v0, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->attached:Ljava/util/WeakHashMap;

    .line 16
    new-instance v0, Ljava/util/WeakHashMap;

    invoke-direct {v0}, Ljava/util/WeakHashMap;-><init>()V

    sput-object v0, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->waiting:Ljava/util/WeakHashMap;

    .line 17
    new-instance v0, Ljava/util/WeakHashMap;

    invoke-direct {v0}, Ljava/util/WeakHashMap;-><init>()V

    sput-object v0, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->waitingSince:Ljava/util/WeakHashMap;

    return-void
.end method

.method public constructor <init>()V
    .registers 1

    .line 14
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method private static apply(Landroid/app/Activity;Landroid/widget/Button;Ljava/lang/String;Z)V
    .registers 6
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation

    .line 71
    new-instance v0, Lorg/json/JSONObject;

    invoke-direct {v0}, Lorg/json/JSONObject;-><init>()V

    const-string v1, "enabled"

    invoke-virtual {v0, v1, p3}, Lorg/json/JSONObject;->put(Ljava/lang/String;Z)Lorg/json/JSONObject;

    move-result-object v0

    const-string v1, "player_id"

    invoke-virtual {v0, v1, p2}, Lorg/json/JSONObject;->put(Ljava/lang/String;Ljava/lang/Object;)Lorg/json/JSONObject;

    move-result-object p2

    const-string v0, "ui7_single_player_live"

    invoke-static {p0, v0, p2}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->manage(Landroid/app/Activity;Ljava/lang/String;Lorg/json/JSONObject;)Lorg/json/JSONObject;

    move-result-object p2

    .line 72
    const-string v0, "saved"

    invoke-virtual {p2, v0}, Lorg/json/JSONObject;->optBoolean(Ljava/lang/String;)Z

    move-result v0

    if-eqz v0, :cond_28

    .line 73
    new-instance p2, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda9;

    invoke-direct {p2, p1, p0, p3}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda9;-><init>(Landroid/widget/Button;Landroid/app/Activity;Z)V

    invoke-virtual {p0, p2}, Landroid/app/Activity;->runOnUiThread(Ljava/lang/Runnable;)V

    .line 74
    return-void

    .line 72
    :cond_28
    new-instance p0, Ljava/lang/Exception;

    const-string p1, "error"

    const-string p3, "Single Player was not applied"

    invoke-virtual {p2, p1, p3}, Lorg/json/JSONObject;->optString(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object p1

    invoke-direct {p0, p1}, Ljava/lang/Exception;-><init>(Ljava/lang/String;)V

    throw p0
.end method

.method public static attach(Landroid/app/Activity;)V
    .registers 9

    .line 20
    invoke-virtual {p0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/Class;->getName()Ljava/lang/String;

    move-result-object v0

    const-string v1, "com.epicgames.ue4.GameActivity"

    invoke-virtual {v0, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_f0

    invoke-virtual {p0}, Landroid/app/Activity;->isFinishing()Z

    move-result v0

    if-eqz v0, :cond_18

    goto/16 :goto_f0

    .line 21
    :cond_18
    sget-object v0, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->attached:Ljava/util/WeakHashMap;

    invoke-virtual {v0, p0}, Ljava/util/WeakHashMap;->get(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Ljava/lang/ref/WeakReference;

    if-eqz v0, :cond_29

    invoke-virtual {v0}, Ljava/lang/ref/WeakReference;->get()Ljava/lang/Object;

    move-result-object v0

    if-eqz v0, :cond_29

    return-void

    .line 22
    :cond_29
    invoke-virtual {p0}, Landroid/app/Activity;->getWindow()Landroid/view/Window;

    move-result-object v0

    invoke-virtual {v0}, Landroid/view/Window;->getDecorView()Landroid/view/View;

    move-result-object v0

    instance-of v1, v0, Landroid/view/ViewGroup;

    if-nez v1, :cond_36

    return-void

    .line 23
    :cond_36
    new-instance v1, Landroid/widget/Button;

    invoke-direct {v1, p0}, Landroid/widget/Button;-><init>(Landroid/content/Context;)V

    const-string v2, "revival_single_player"

    invoke-virtual {v1, v2}, Landroid/widget/Button;->setTag(Ljava/lang/Object;)V

    const-string v2, "1P"

    invoke-virtual {v1, v2}, Landroid/widget/Button;->setText(Ljava/lang/CharSequence;)V

    const-string v2, "Single Player off: tap to choose, hold to change player"

    invoke-virtual {v1, v2}, Landroid/widget/Button;->setContentDescription(Ljava/lang/CharSequence;)V

    const/high16 v2, 0x41400000    # 12.0f

    invoke-virtual {v1, v2}, Landroid/widget/Button;->setTextSize(F)V

    const/4 v2, 0x1

    invoke-virtual {v1, v2}, Landroid/widget/Button;->setSingleLine(Z)V

    const/4 v3, 0x0

    invoke-virtual {v1, v3, v3, v3, v3}, Landroid/widget/Button;->setPadding(IIII)V

    invoke-virtual {v1, v3}, Landroid/widget/Button;->setAllCaps(Z)V

    invoke-virtual {v1, v3}, Landroid/widget/Button;->setMinHeight(I)V

    invoke-virtual {v1, v3}, Landroid/widget/Button;->setMinimumHeight(I)V

    invoke-virtual {v1, v3}, Landroid/widget/Button;->setMinWidth(I)V

    invoke-virtual {v1, v3}, Landroid/widget/Button;->setMinimumWidth(I)V

    invoke-virtual {v1, v3}, Landroid/widget/Button;->setIncludeFontPadding(Z)V

    :try_start_69
    invoke-virtual {v1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v4

    const-string v5, "setElevation"

    new-array v6, v2, [Ljava/lang/Class;

    sget-object v7, Ljava/lang/Float;->TYPE:Ljava/lang/Class;

    aput-object v7, v6, v3

    invoke-virtual {v4, v5, v6}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v4

    new-array v5, v2, [Ljava/lang/Object;

    const/4 v6, 0x0

    invoke-static {v6}, Ljava/lang/Float;->valueOf(F)Ljava/lang/Float;

    move-result-object v6

    aput-object v6, v5, v3

    invoke-virtual {v4, v1, v5}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    invoke-virtual {v1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v4

    const-string v5, "setStateListAnimator"

    new-array v2, v2, [Ljava/lang/Class;

    const-string v6, "android.animation.StateListAnimator"

    invoke-static {v6}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;

    move-result-object v6

    aput-object v6, v2, v3

    invoke-virtual {v4, v5, v2}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v2

    const/4 v4, 0x0

    filled-new-array {v4}, [Ljava/lang/Object;

    move-result-object v4

    invoke-virtual {v2, v1, v4}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;
    :try_end_a1
    .catch Ljava/lang/Exception; {:try_start_69 .. :try_end_a1} :catch_a2

    goto :goto_a3

    :catch_a2
    move-exception v2

    :goto_a3
    const/16 v2, 0x11

    invoke-virtual {v1, v2}, Landroid/widget/Button;->setGravity(I)V

    .line 24
    new-instance v2, Landroid/widget/FrameLayout$LayoutParams;

    const/16 v4, 0x28

    invoke-static {p0, v4}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->dp(Landroid/app/Activity;I)I

    move-result v5

    invoke-static {p0, v4}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->dp(Landroid/app/Activity;I)I

    move-result v4

    const/16 v6, 0x33

    invoke-direct {v2, v5, v4, v6}, Landroid/widget/FrameLayout$LayoutParams;-><init>(III)V

    .line 25
    move-object v4, v0

    check-cast v4, Landroid/view/ViewGroup;

    invoke-virtual {v4, v1, v2}, Landroid/view/ViewGroup;->addView(Landroid/view/View;Landroid/view/ViewGroup$LayoutParams;)V

    sget-object v2, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->attached:Ljava/util/WeakHashMap;

    new-instance v4, Ljava/lang/ref/WeakReference;

    invoke-direct {v4, v1}, Ljava/lang/ref/WeakReference;-><init>(Ljava/lang/Object;)V

    invoke-virtual {v2, p0, v4}, Ljava/util/WeakHashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    invoke-static {p0, v1, v3}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->paint(Landroid/app/Activity;Landroid/widget/Button;I)V

    new-instance v2, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda0;

    invoke-direct {v2, p0, v1}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda0;-><init>(Landroid/app/Activity;Landroid/widget/Button;)V

    invoke-virtual {v0, v2}, Landroid/view/View;->post(Ljava/lang/Runnable;)Z

    new-instance v2, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda1;

    invoke-direct {v2, p0, v1}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda1;-><init>(Landroid/app/Activity;Landroid/widget/Button;)V

    invoke-virtual {v0, v2}, Landroid/view/View;->addOnLayoutChangeListener(Landroid/view/View$OnLayoutChangeListener;)V

    invoke-static {p0, v1}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->poll(Landroid/app/Activity;Landroid/widget/Button;)V

    .line 26
    new-instance v0, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda2;

    invoke-direct {v0, p0, v1}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda2;-><init>(Landroid/app/Activity;Landroid/widget/Button;)V

    invoke-virtual {v1, v0}, Landroid/widget/Button;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    new-instance v0, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda3;

    invoke-direct {v0, p0, v1}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda3;-><init>(Landroid/app/Activity;Landroid/widget/Button;)V

    invoke-virtual {v1, v0}, Landroid/widget/Button;->setOnLongClickListener(Landroid/view/View$OnLongClickListener;)V

    .line 27
    return-void

    .line 20
    :cond_f0
    :goto_f0
    return-void
.end method

.method private static choose(Landroid/app/Activity;Landroid/widget/Button;Lorg/json/JSONArray;)V
    .registers 11

    .line 62
    invoke-virtual {p0}, Landroid/app/Activity;->isFinishing()Z

    move-result v0

    if-eqz v0, :cond_7

    return-void

    .line 63
    :cond_7
    if-eqz p2, :cond_ad

    invoke-virtual {p2}, Lorg/json/JSONArray;->length()I

    move-result v0

    if-nez v0, :cond_11

    goto/16 :goto_ad

    .line 64
    :cond_11
    new-instance v0, Lorg/json/JSONArray;

    invoke-direct {v0}, Lorg/json/JSONArray;-><init>()V

    const/4 v1, 0x0

    move v2, v1

    :goto_18
    invoke-virtual {p2}, Lorg/json/JSONArray;->length()I

    move-result v3

    const-string v4, "on_pitch"

    if-ge v2, v3, :cond_32

    invoke-virtual {p2, v2}, Lorg/json/JSONArray;->optJSONObject(I)Lorg/json/JSONObject;

    move-result-object v3

    if-eqz v3, :cond_2f

    invoke-virtual {v3, v4}, Lorg/json/JSONObject;->optBoolean(Ljava/lang/String;)Z

    move-result v4

    if-eqz v4, :cond_2f

    invoke-virtual {v0, v3}, Lorg/json/JSONArray;->put(Ljava/lang/Object;)Lorg/json/JSONArray;

    :cond_2f
    add-int/lit8 v2, v2, 0x1

    goto :goto_18

    .line 65
    :cond_32
    invoke-virtual {v0}, Lorg/json/JSONArray;->length()I

    move-result p2

    const/4 v2, 0x0

    if-nez p2, :cond_3d

    invoke-static {p0, p1, v2}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->choose(Landroid/app/Activity;Landroid/widget/Button;Lorg/json/JSONArray;)V

    return-void

    .line 66
    :cond_3d
    invoke-virtual {v0}, Lorg/json/JSONArray;->length()I

    move-result p2

    new-array p2, p2, [Ljava/lang/String;

    invoke-virtual {v0}, Lorg/json/JSONArray;->length()I

    move-result v3

    new-array v3, v3, [Ljava/lang/String;

    .line 67
    nop

    :goto_4a
    invoke-virtual {v0}, Lorg/json/JSONArray;->length()I

    move-result v5

    if-ge v1, v5, :cond_8f

    invoke-virtual {v0, v1}, Lorg/json/JSONArray;->optJSONObject(I)Lorg/json/JSONObject;

    move-result-object v5

    const-string v6, "id"

    invoke-virtual {v5, v6}, Lorg/json/JSONObject;->optString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v6

    aput-object v6, v3, v1

    new-instance v6, Ljava/lang/StringBuilder;

    invoke-direct {v6}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v5, v4}, Lorg/json/JSONObject;->optBoolean(Ljava/lang/String;)Z

    move-result v7

    if-eqz v7, :cond_6a

    const-string v7, "[XI] "

    goto :goto_6c

    :cond_6a
    const-string v7, "[Bench] "

    :goto_6c
    invoke-virtual {v6, v7}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v6

    const-string v7, "name"

    invoke-virtual {v5, v7}, Lorg/json/JSONObject;->optString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v5

    invoke-virtual {v6, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    const-string v6, " \u00b7 "

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    aget-object v6, v3, v1

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    invoke-virtual {v5}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v5

    aput-object v5, p2, v1

    add-int/lit8 v1, v1, 0x1

    goto :goto_4a

    .line 68
    :cond_8f
    new-instance v0, Landroid/app/AlertDialog$Builder;

    invoke-direct {v0, p0}, Landroid/app/AlertDialog$Builder;-><init>(Landroid/content/Context;)V

    const-string v1, "Single Player \u00b7 Live team"

    invoke-virtual {v0, v1}, Landroid/app/AlertDialog$Builder;->setTitle(Ljava/lang/CharSequence;)Landroid/app/AlertDialog$Builder;

    move-result-object v0

    new-instance v1, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda5;

    invoke-direct {v1, p1, p0, v3}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda5;-><init>(Landroid/widget/Button;Landroid/app/Activity;[Ljava/lang/String;)V

    invoke-virtual {v0, p2, v1}, Landroid/app/AlertDialog$Builder;->setItems([Ljava/lang/CharSequence;Landroid/content/DialogInterface$OnClickListener;)Landroid/app/AlertDialog$Builder;

    move-result-object p0

    const-string p1, "Close"

    invoke-virtual {p0, p1, v2}, Landroid/app/AlertDialog$Builder;->setNegativeButton(Ljava/lang/CharSequence;Landroid/content/DialogInterface$OnClickListener;)Landroid/app/AlertDialog$Builder;

    move-result-object p0

    invoke-virtual {p0}, Landroid/app/AlertDialog$Builder;->show()Landroid/app/AlertDialog;

    .line 69
    return-void

    .line 63
    :cond_ad
    :goto_ad
    sget-object p2, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->waiting:Ljava/util/WeakHashMap;

    const/4 v0, 0x1

    invoke-static {v0}, Ljava/lang/Boolean;->valueOf(Z)Ljava/lang/Boolean;

    move-result-object v1

    invoke-virtual {p2, p1, v1}, Ljava/util/WeakHashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    sget-object p2, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->waitingSince:Ljava/util/WeakHashMap;

    invoke-static {}, Landroid/os/SystemClock;->elapsedRealtime()J

    move-result-wide v1

    invoke-static {v1, v2}, Ljava/lang/Long;->valueOf(J)Ljava/lang/Long;

    move-result-object v1

    invoke-virtual {p2, p1, v1}, Ljava/util/WeakHashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    const/4 p2, 0x2

    invoke-static {p0, p1, p2}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->paint(Landroid/app/Activity;Landroid/widget/Button;I)V

    const-string p1, "Live team is not available yet. Resume the match; tap to cancel selection."

    invoke-static {p0, p1, v0}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;

    move-result-object p0

    invoke-virtual {p0}, Landroid/widget/Toast;->show()V

    return-void
.end method

.method private static dp(Landroid/app/Activity;I)I
    .registers 2

    .line 18
    int-to-float p1, p1

    invoke-virtual {p0}, Landroid/app/Activity;->getResources()Landroid/content/res/Resources;

    move-result-object p0

    invoke-virtual {p0}, Landroid/content/res/Resources;->getDisplayMetrics()Landroid/util/DisplayMetrics;

    move-result-object p0

    iget p0, p0, Landroid/util/DisplayMetrics;->density:F

    mul-float/2addr p1, p0

    invoke-static {p1}, Ljava/lang/Math;->round(F)I

    move-result p0

    return p0
.end method

.method private static fail(Landroid/app/Activity;Landroid/widget/Button;Ljava/lang/Exception;)V
    .registers 4

    .line 50
    new-instance v0, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda13;

    invoke-direct {v0, p1, p0, p2}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda13;-><init>(Landroid/widget/Button;Landroid/app/Activity;Ljava/lang/Exception;)V

    invoke-virtual {p0, v0}, Landroid/app/Activity;->runOnUiThread(Ljava/lang/Runnable;)V

    return-void
.end method

.method private static findAi(Landroid/view/View;Landroid/view/View;)Landroid/view/View;
    .registers 7

    .line 32
    const/4 v0, 0x0

    if-ne p0, p1, :cond_4

    return-object v0

    :cond_4
    invoke-virtual {p0}, Landroid/view/View;->getContentDescription()Ljava/lang/CharSequence;

    move-result-object v1

    if-nez v1, :cond_d

    const-string v1, ""

    goto :goto_1b

    :cond_d
    invoke-virtual {v1}, Ljava/lang/Object;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/String;->trim()Ljava/lang/String;

    move-result-object v1

    sget-object v2, Ljava/util/Locale;->ROOT:Ljava/util/Locale;

    invoke-virtual {v1, v2}, Ljava/lang/String;->toLowerCase(Ljava/util/Locale;)Ljava/lang/String;

    move-result-object v1

    :goto_1b
    instance-of v2, p0, Landroid/widget/TextView;

    const-string v3, "ai"

    if-eqz v2, :cond_4d

    move-object v2, p0

    check-cast v2, Landroid/widget/TextView;

    invoke-virtual {v2}, Landroid/widget/TextView;->getText()Ljava/lang/CharSequence;

    move-result-object v2

    invoke-virtual {v2}, Ljava/lang/Object;->toString()Ljava/lang/String;

    move-result-object v2

    invoke-virtual {v2}, Ljava/lang/String;->trim()Ljava/lang/String;

    move-result-object v2

    sget-object v4, Ljava/util/Locale;->ROOT:Ljava/util/Locale;

    invoke-virtual {v2, v4}, Ljava/lang/String;->toLowerCase(Ljava/util/Locale;)Ljava/lang/String;

    move-result-object v2

    invoke-virtual {v2, v3}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v4

    if-nez v4, :cond_4c

    const-string v4, "ai on"

    invoke-virtual {v2, v4}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v4

    if-nez v4, :cond_4c

    const-string v4, "ai off"

    invoke-virtual {v2, v4}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v2

    if-eqz v2, :cond_4d

    :cond_4c
    return-object p0

    :cond_4d
    invoke-virtual {v1, v3}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v2

    if-nez v2, :cond_8f

    const-string v2, "ai control"

    invoke-virtual {v1, v2}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v2

    if-nez v2, :cond_8f

    const-string v2, "ai mode"

    invoke-virtual {v1, v2}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v2

    if-nez v2, :cond_8f

    const-string v2, "ai toggle"

    invoke-virtual {v1, v2}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-eqz v1, :cond_6c

    goto :goto_8f

    .line 33
    :cond_6c
    instance-of v1, p0, Landroid/view/ViewGroup;

    if-eqz v1, :cond_8e

    const/4 v1, 0x0

    :goto_71
    move-object v2, p0

    check-cast v2, Landroid/view/ViewGroup;

    invoke-virtual {v2}, Landroid/view/ViewGroup;->getChildCount()I

    move-result v3

    if-ge v1, v3, :cond_8e

    invoke-virtual {v2, v1}, Landroid/view/ViewGroup;->getChildAt(I)Landroid/view/View;

    move-result-object v2

    invoke-static {v2, p1}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->findAi(Landroid/view/View;Landroid/view/View;)Landroid/view/View;

    move-result-object v2

    if-eqz v2, :cond_8b

    invoke-virtual {v2}, Landroid/view/View;->getVisibility()I

    move-result v3

    if-nez v3, :cond_8b

    return-object v2

    :cond_8b
    add-int/lit8 v1, v1, 0x1

    goto :goto_71

    :cond_8e
    return-object v0

    .line 32
    :cond_8f
    :goto_8f
    return-object p0
.end method

.method static synthetic lambda$apply$13(Landroid/widget/Button;Landroid/app/Activity;Z)V
    .registers 5

    .line 73
    const/4 v0, 0x1

    invoke-virtual {p0, v0}, Landroid/widget/Button;->setEnabled(Z)V

    const/4 v0, 0x0

    if-eqz p2, :cond_9

    const/4 v1, 0x2

    goto :goto_a

    :cond_9
    move v1, v0

    :goto_a
    invoke-static {p1, p0, v1}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->paint(Landroid/app/Activity;Landroid/widget/Button;I)V

    if-eqz p2, :cond_12

    const-string p0, "Single Player requested \u00b7 waiting for native control"

    goto :goto_14

    :cond_12
    const-string p0, "Single Player disabled"

    :goto_14
    invoke-static {p1, p0, v0}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;

    move-result-object p0

    invoke-virtual {p0}, Landroid/widget/Toast;->show()V

    return-void
.end method

.method static synthetic lambda$attach$0(Landroid/app/Activity;Landroid/widget/Button;)V
    .registers 2

    .line 25
    invoke-static {p0, p1}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->position(Landroid/app/Activity;Landroid/widget/Button;)V

    return-void
.end method

.method static synthetic lambda$attach$1(Landroid/app/Activity;Landroid/widget/Button;Landroid/view/View;IIIIIIII)V
    .registers 11

    .line 25
    if-ne p3, p7, :cond_8

    if-ne p4, p8, :cond_8

    if-ne p5, p9, :cond_8

    if-eq p6, p10, :cond_b

    :cond_8
    invoke-static {p0, p1}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->position(Landroid/app/Activity;Landroid/widget/Button;)V

    :cond_b
    return-void
.end method

.method static synthetic lambda$attach$2(Landroid/app/Activity;Landroid/widget/Button;Landroid/view/View;)V
    .registers 3

    .line 26
    const/4 p2, 0x0

    invoke-static {p0, p1, p2}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->request(Landroid/app/Activity;Landroid/widget/Button;Z)V

    return-void
.end method

.method static synthetic lambda$attach$3(Landroid/app/Activity;Landroid/widget/Button;Landroid/view/View;)Z
    .registers 3

    .line 26
    const/4 p2, 0x1

    invoke-static {p0, p1, p2}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->request(Landroid/app/Activity;Landroid/widget/Button;Z)V

    return p2
.end method

.method static synthetic lambda$choose$11(Landroid/app/Activity;Landroid/widget/Button;[Ljava/lang/String;I)V
    .registers 4

    .line 68
    :try_start_0
    aget-object p2, p2, p3

    const/4 p3, 0x1

    invoke-static {p0, p1, p2, p3}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->apply(Landroid/app/Activity;Landroid/widget/Button;Ljava/lang/String;Z)V
    :try_end_6
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_6} :catch_7

    goto :goto_b

    :catch_7
    move-exception p2

    invoke-static {p0, p1, p2}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->fail(Landroid/app/Activity;Landroid/widget/Button;Ljava/lang/Exception;)V

    :goto_b
    return-void
.end method

.method static synthetic lambda$choose$12(Landroid/widget/Button;Landroid/app/Activity;[Ljava/lang/String;Landroid/content/DialogInterface;I)V
    .registers 6

    .line 68
    const/4 p3, 0x0

    invoke-virtual {p0, p3}, Landroid/widget/Button;->setEnabled(Z)V

    new-instance p3, Ljava/lang/Thread;

    new-instance v0, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda6;

    invoke-direct {v0, p1, p0, p2, p4}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda6;-><init>(Landroid/app/Activity;Landroid/widget/Button;[Ljava/lang/String;I)V

    const-string p0, "SinglePlayerChoose"

    invoke-direct {p3, v0, p0}, Ljava/lang/Thread;-><init>(Ljava/lang/Runnable;Ljava/lang/String;)V

    invoke-virtual {p3}, Ljava/lang/Thread;->start()V

    return-void
.end method

.method static synthetic lambda$fail$8(Landroid/widget/Button;Landroid/app/Activity;Ljava/lang/Exception;)V
    .registers 4

    .line 50
    const/4 v0, 0x1

    invoke-virtual {p0, v0}, Landroid/widget/Button;->setEnabled(Z)V

    invoke-virtual {p1}, Landroid/app/Activity;->isFinishing()Z

    move-result p0

    if-nez p0, :cond_15

    invoke-virtual {p2}, Ljava/lang/Exception;->getMessage()Ljava/lang/String;

    move-result-object p0

    invoke-static {p1, p0, v0}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;

    move-result-object p0

    invoke-virtual {p0}, Landroid/widget/Toast;->show()V

    :cond_15
    return-void
.end method

.method static synthetic lambda$poll$4(Landroid/app/Activity;Landroid/widget/Button;ZZLorg/json/JSONObject;)V
    .registers 11

    .line 46
    invoke-virtual {p0}, Landroid/app/Activity;->isFinishing()Z

    move-result v0

    if-nez v0, :cond_bb

    invoke-virtual {p1}, Landroid/widget/Button;->isEnabled()Z

    move-result v0

    if-eqz v0, :cond_bb

    const/4 v0, 0x2

    const/4 v1, 0x1

    if-nez p2, :cond_12

    const/4 p2, 0x0

    goto :goto_17

    :cond_12
    if-eqz p3, :cond_16

    move p2, v1

    goto :goto_17

    :cond_16
    move p2, v0

    :goto_17
    invoke-static {p0, p1, p2}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->paint(Landroid/app/Activity;Landroid/widget/Button;I)V

    sget-object p2, Ljava/lang/Boolean;->TRUE:Ljava/lang/Boolean;

    sget-object p3, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->waiting:Ljava/util/WeakHashMap;

    invoke-virtual {p3, p1}, Ljava/util/WeakHashMap;->get(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object p3

    invoke-virtual {p2, p3}, Ljava/lang/Boolean;->equals(Ljava/lang/Object;)Z

    move-result p2

    const-string p3, "runtime"

    if-eqz p2, :cond_82

    invoke-static {}, Landroid/os/SystemClock;->elapsedRealtime()J

    move-result-wide v2

    sget-object p2, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->waitingSince:Ljava/util/WeakHashMap;

    const-wide/16 v4, 0x0

    invoke-static {v4, v5}, Ljava/lang/Long;->valueOf(J)Ljava/lang/Long;

    move-result-object v4

    invoke-virtual {p2, p1, v4}, Ljava/util/WeakHashMap;->getOrDefault(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object p2

    check-cast p2, Ljava/lang/Long;

    invoke-virtual {p2}, Ljava/lang/Long;->longValue()J

    move-result-wide v4

    sub-long/2addr v2, v4

    const-wide/16 v4, 0xbb8

    cmp-long p2, v2, v4

    if-lez p2, :cond_82

    sget-object p2, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->waiting:Ljava/util/WeakHashMap;

    invoke-virtual {p2, p1}, Ljava/util/WeakHashMap;->remove(Ljava/lang/Object;)Ljava/lang/Object;

    sget-object p2, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->waitingSince:Ljava/util/WeakHashMap;

    invoke-virtual {p2, p1}, Ljava/util/WeakHashMap;->remove(Ljava/lang/Object;)Ljava/lang/Object;

    new-instance p2, Ljava/lang/StringBuilder;

    invoke-direct {p2}, Ljava/lang/StringBuilder;-><init>()V

    const-string v2, "Active team could not be read. Native status: "

    invoke-virtual {p2, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p2

    invoke-virtual {p4, p3}, Lorg/json/JSONObject;->optJSONObject(Ljava/lang/String;)Lorg/json/JSONObject;

    move-result-object v2

    if-nez v2, :cond_65

    const-string v2, "unavailable"

    goto :goto_73

    :cond_65
    invoke-virtual {p4, p3}, Lorg/json/JSONObject;->optJSONObject(Ljava/lang/String;)Lorg/json/JSONObject;

    move-result-object v2

    const-string v3, "reason_code"

    invoke-virtual {v2, v3}, Lorg/json/JSONObject;->optInt(Ljava/lang/String;)I

    move-result v2

    invoke-static {v2}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v2

    :goto_73
    invoke-virtual {p2, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    move-result-object p2

    invoke-virtual {p2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p2

    invoke-static {p0, p2, v1}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;

    move-result-object p2

    invoke-virtual {p2}, Landroid/widget/Toast;->show()V

    :cond_82
    sget-object p2, Ljava/lang/Boolean;->TRUE:Ljava/lang/Boolean;

    sget-object v2, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->waiting:Ljava/util/WeakHashMap;

    invoke-virtual {v2, p1}, Ljava/util/WeakHashMap;->get(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v2

    invoke-virtual {p2, v2}, Ljava/lang/Boolean;->equals(Ljava/lang/Object;)Z

    move-result p2

    if-eqz p2, :cond_93

    invoke-static {p0, p1, v0}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->paint(Landroid/app/Activity;Landroid/widget/Button;I)V

    :cond_93
    sget-object p2, Ljava/lang/Boolean;->TRUE:Ljava/lang/Boolean;

    sget-object v0, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->waiting:Ljava/util/WeakHashMap;

    invoke-virtual {v0, p1}, Ljava/util/WeakHashMap;->get(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v0

    invoke-virtual {p2, v0}, Ljava/lang/Boolean;->equals(Ljava/lang/Object;)Z

    move-result p2

    if-eqz p2, :cond_bb

    invoke-virtual {p4, p3}, Lorg/json/JSONObject;->optJSONObject(Ljava/lang/String;)Lorg/json/JSONObject;

    move-result-object p2

    if-eqz p2, :cond_bb

    invoke-virtual {p4, p3}, Lorg/json/JSONObject;->optJSONObject(Ljava/lang/String;)Lorg/json/JSONObject;

    move-result-object p2

    const-string p3, "roster_count"

    invoke-virtual {p2, p3}, Lorg/json/JSONObject;->optInt(Ljava/lang/String;)I

    move-result p2

    if-lez p2, :cond_bb

    sget-object p2, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->waiting:Ljava/util/WeakHashMap;

    invoke-virtual {p2, p1}, Ljava/util/WeakHashMap;->remove(Ljava/lang/Object;)Ljava/lang/Object;

    invoke-static {p0, p1, v1}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->request(Landroid/app/Activity;Landroid/widget/Button;Z)V

    :cond_bb
    return-void
.end method

.method static synthetic lambda$poll$5(Landroid/app/Activity;Landroid/widget/Button;)V
    .registers 2

    .line 47
    invoke-static {p0, p1}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->poll(Landroid/app/Activity;Landroid/widget/Button;)V

    return-void
.end method

.method static synthetic lambda$poll$6(Landroid/app/Activity;Landroid/widget/Button;)V
    .registers 11

    .line 45
    const-string v0, "runtime"

    :try_start_2
    const-string v1, "ui7_single_player_get"

    new-instance v2, Lorg/json/JSONObject;

    invoke-direct {v2}, Lorg/json/JSONObject;-><init>()V

    invoke-static {p0, v1, v2}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->manage(Landroid/app/Activity;Ljava/lang/String;Lorg/json/JSONObject;)Lorg/json/JSONObject;

    move-result-object v8

    const-string v1, "enabled"

    invoke-virtual {v8, v1}, Lorg/json/JSONObject;->optBoolean(Ljava/lang/String;)Z

    move-result v6

    invoke-virtual {v8, v0}, Lorg/json/JSONObject;->optJSONObject(Ljava/lang/String;)Lorg/json/JSONObject;

    move-result-object v1

    if-eqz v1, :cond_27

    invoke-virtual {v8, v0}, Lorg/json/JSONObject;->optJSONObject(Ljava/lang/String;)Lorg/json/JSONObject;

    move-result-object v0

    const-string v1, "active"

    invoke-virtual {v0, v1}, Lorg/json/JSONObject;->optInt(Ljava/lang/String;)I

    move-result v0

    if-eqz v0, :cond_27

    const/4 v0, 0x1

    goto :goto_28

    :cond_27
    const/4 v0, 0x0

    :goto_28
    move v7, v0

    .line 46
    new-instance v0, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda7;

    move-object v3, v0

    move-object v4, p0

    move-object v5, p1

    invoke-direct/range {v3 .. v8}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda7;-><init>(Landroid/app/Activity;Landroid/widget/Button;ZZLorg/json/JSONObject;)V

    invoke-virtual {p0, v0}, Landroid/app/Activity;->runOnUiThread(Ljava/lang/Runnable;)V
    :try_end_34
    .catch Ljava/lang/Exception; {:try_start_2 .. :try_end_34} :catch_44
    .catchall {:try_start_2 .. :try_end_34} :catchall_3a

    .line 47
    new-instance v0, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda8;

    invoke-direct {v0, p0, p1}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda8;-><init>(Landroid/app/Activity;Landroid/widget/Button;)V

    goto :goto_4a

    :catchall_3a
    move-exception v0

    new-instance v1, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda8;

    invoke-direct {v1, p0, p1}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda8;-><init>(Landroid/app/Activity;Landroid/widget/Button;)V

    invoke-virtual {p0, v1}, Landroid/app/Activity;->runOnUiThread(Ljava/lang/Runnable;)V

    throw v0

    :catch_44
    move-exception v0

    new-instance v0, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda8;

    invoke-direct {v0, p0, p1}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda8;-><init>(Landroid/app/Activity;Landroid/widget/Button;)V

    :goto_4a
    invoke-virtual {p0, v0}, Landroid/app/Activity;->runOnUiThread(Ljava/lang/Runnable;)V

    return-void
.end method

.method static synthetic lambda$poll$7(Landroid/app/Activity;Landroid/widget/Button;)V
    .registers 4

    .line 44
    invoke-virtual {p0}, Landroid/app/Activity;->isFinishing()Z

    move-result v0

    if-nez v0, :cond_2d

    invoke-virtual {p1}, Landroid/widget/Button;->getWindowToken()Landroid/os/IBinder;

    move-result-object v0

    if-nez v0, :cond_d

    goto :goto_2d

    :cond_d
    invoke-virtual {p0}, Landroid/app/Activity;->hasWindowFocus()Z

    move-result v0

    if-eqz v0, :cond_2a

    invoke-virtual {p1}, Landroid/widget/Button;->isEnabled()Z

    move-result v0

    if-nez v0, :cond_1a

    goto :goto_2a

    .line 45
    :cond_1a
    new-instance v0, Ljava/lang/Thread;

    new-instance v1, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda4;

    invoke-direct {v1, p0, p1}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda4;-><init>(Landroid/app/Activity;Landroid/widget/Button;)V

    const-string p0, "SinglePlayerStatus"

    invoke-direct {v0, v1, p0}, Ljava/lang/Thread;-><init>(Ljava/lang/Runnable;Ljava/lang/String;)V

    .line 47
    invoke-virtual {v0}, Ljava/lang/Thread;->start()V

    return-void

    .line 44
    :cond_2a
    :goto_2a
    invoke-static {p0, p1}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->poll(Landroid/app/Activity;Landroid/widget/Button;)V

    :cond_2d
    :goto_2d
    return-void
.end method

.method static synthetic lambda$request$10(Landroid/app/Activity;ZLandroid/widget/Button;)V
    .registers 7

    .line 54
    const-string v0, ""

    :try_start_2
    const-string v1, "ui7_single_player_get"

    new-instance v2, Lorg/json/JSONObject;

    invoke-direct {v2}, Lorg/json/JSONObject;-><init>()V

    invoke-static {p0, v1, v2}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->manage(Landroid/app/Activity;Ljava/lang/String;Lorg/json/JSONObject;)Lorg/json/JSONObject;

    move-result-object v1

    .line 55
    const-string v2, "player_id"

    invoke-virtual {v1, v2, v0}, Lorg/json/JSONObject;->optString(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v2

    .line 56
    const/4 v3, 0x0

    if-nez p1, :cond_22

    const-string p1, "enabled"

    invoke-virtual {v1, p1}, Lorg/json/JSONObject;->optBoolean(Ljava/lang/String;)Z

    move-result p1

    if-eqz p1, :cond_22

    invoke-static {p0, p2, v2, v3}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->apply(Landroid/app/Activity;Landroid/widget/Button;Ljava/lang/String;Z)V

    return-void

    .line 57
    :cond_22
    const-string p1, "ui7_single_player_search"

    new-instance v1, Lorg/json/JSONObject;

    invoke-direct {v1}, Lorg/json/JSONObject;-><init>()V

    const-string v2, "query"

    invoke-virtual {v1, v2, v0}, Lorg/json/JSONObject;->put(Ljava/lang/String;Ljava/lang/Object;)Lorg/json/JSONObject;

    move-result-object v0

    const-string v1, "page"

    invoke-virtual {v0, v1, v3}, Lorg/json/JSONObject;->put(Ljava/lang/String;I)Lorg/json/JSONObject;

    move-result-object v0

    invoke-static {p0, p1, v0}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->manage(Landroid/app/Activity;Ljava/lang/String;Lorg/json/JSONObject;)Lorg/json/JSONObject;

    move-result-object p1

    .line 58
    new-instance v0, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda12;

    invoke-direct {v0, p2, p0, p1}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda12;-><init>(Landroid/widget/Button;Landroid/app/Activity;Lorg/json/JSONObject;)V

    invoke-virtual {p0, v0}, Landroid/app/Activity;->runOnUiThread(Ljava/lang/Runnable;)V
    :try_end_41
    .catch Ljava/lang/Exception; {:try_start_2 .. :try_end_41} :catch_42

    .line 59
    goto :goto_46

    :catch_42
    move-exception p1

    invoke-static {p0, p2, p1}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->fail(Landroid/app/Activity;Landroid/widget/Button;Ljava/lang/Exception;)V

    :goto_46
    return-void
.end method

.method static synthetic lambda$request$9(Landroid/widget/Button;Landroid/app/Activity;Lorg/json/JSONObject;)V
    .registers 4

    .line 58
    const/4 v0, 0x1

    invoke-virtual {p0, v0}, Landroid/widget/Button;->setEnabled(Z)V

    const-string v0, "players"

    invoke-virtual {p2, v0}, Lorg/json/JSONObject;->optJSONArray(Ljava/lang/String;)Lorg/json/JSONArray;

    move-result-object p2

    invoke-static {p1, p0, p2}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->choose(Landroid/app/Activity;Landroid/widget/Button;Lorg/json/JSONArray;)V

    return-void
.end method

.method private static manage(Landroid/app/Activity;Ljava/lang/String;Lorg/json/JSONObject;)Lorg/json/JSONObject;
    .registers 4
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation

    .line 49
    new-instance v0, Lorg/json/JSONObject;

    invoke-virtual {p2}, Lorg/json/JSONObject;->toString()Ljava/lang/String;

    move-result-object p2

    invoke-static {p0, p1, p2}, Lorg/efootballrevival/runtimeprobe/EmbeddedGateway;->manage(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object p0

    invoke-direct {v0, p0}, Lorg/json/JSONObject;-><init>(Ljava/lang/String;)V

    return-object v0
.end method

.method private static paint(Landroid/app/Activity;Landroid/widget/Button;I)V
    .registers 7

    .line 29
    const-string v0, "1P"

    invoke-virtual {p1, v0}, Landroid/widget/Button;->setText(Ljava/lang/CharSequence;)V

    if-nez p2, :cond_b

    const v0, -0xdad5d4

    goto :goto_c

    :cond_b
    const/4 v0, -0x1

    :goto_c
    invoke-virtual {p1, v0}, Landroid/widget/Button;->setTextColor(I)V

    new-instance v0, Landroid/graphics/drawable/GradientDrawable;

    invoke-direct {v0}, Landroid/graphics/drawable/GradientDrawable;-><init>()V

    const/4 v1, 0x2

    const/4 v2, 0x1

    if-ne p2, v2, :cond_1c

    const v3, -0x1ad2348a

    goto :goto_25

    :cond_1c
    if-ne p2, v1, :cond_22

    const v3, -0x1a579800

    goto :goto_25

    :cond_22
    const v3, -0x22191717

    :goto_25
    invoke-virtual {v0, v3}, Landroid/graphics/drawable/GradientDrawable;->setColor(I)V

    const/4 v3, 0x3

    invoke-static {p0, v3}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->dp(Landroid/app/Activity;I)I

    move-result p0

    int-to-float p0, p0

    invoke-virtual {v0, p0}, Landroid/graphics/drawable/GradientDrawable;->setCornerRadius(F)V

    invoke-virtual {p1, v0}, Landroid/widget/Button;->setBackground(Landroid/graphics/drawable/Drawable;)V

    if-ne p2, v2, :cond_38

    move p0, v2

    goto :goto_39

    :cond_38
    const/4 p0, 0x0

    :goto_39
    invoke-virtual {p1, p0}, Landroid/widget/Button;->setSelected(Z)V

    new-instance p0, Ljava/lang/StringBuilder;

    invoke-direct {p0}, Ljava/lang/StringBuilder;-><init>()V

    const-string v0, "Single Player "

    invoke-virtual {p0, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p0

    if-ne p2, v2, :cond_4c

    const-string p2, "on"

    goto :goto_53

    :cond_4c
    if-ne p2, v1, :cond_51

    const-string p2, "pending"

    goto :goto_53

    :cond_51
    const-string p2, "off"

    :goto_53
    invoke-virtual {p0, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p0

    const-string p2, ": tap to toggle, hold to choose a player"

    invoke-virtual {p0, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p0

    invoke-virtual {p0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-virtual {p1, p0}, Landroid/widget/Button;->setContentDescription(Ljava/lang/CharSequence;)V

    .line 30
    return-void
.end method

.method private static poll(Landroid/app/Activity;Landroid/widget/Button;)V
    .registers 5

    .line 44
    new-instance v0, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda11;

    invoke-direct {v0, p0, p1}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda11;-><init>(Landroid/app/Activity;Landroid/widget/Button;)V

    const-wide/16 v1, 0xc8

    invoke-virtual {p1, v0, v1, v2}, Landroid/widget/Button;->postDelayed(Ljava/lang/Runnable;J)Z

    .line 48
    return-void
.end method

.method private static position(Landroid/app/Activity;Landroid/widget/Button;)V
    .registers 12

    .line 36
    invoke-virtual {p0}, Landroid/app/Activity;->getWindow()Landroid/view/Window;

    move-result-object p0

    invoke-virtual {p0}, Landroid/view/Window;->getDecorView()Landroid/view/View;

    move-result-object p0

    invoke-virtual {p0}, Landroid/view/View;->getWidth()I

    move-result v0

    invoke-virtual {p0}, Landroid/view/View;->getHeight()I

    move-result v1

    if-eqz v0, :cond_c5

    if-nez v1, :cond_16

    goto/16 :goto_c5

    :cond_16
    invoke-virtual {p1}, Landroid/widget/Button;->getLayoutParams()Landroid/view/ViewGroup$LayoutParams;

    move-result-object v2

    check-cast v2, Landroid/widget/FrameLayout$LayoutParams;

    invoke-static {p0, p1}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->findAi(Landroid/view/View;Landroid/view/View;)Landroid/view/View;

    move-result-object v3

    int-to-float v1, v1

    const v4, 0x3bc49ba6    # 0.006f

    mul-float/2addr v4, v1

    invoke-static {v4}, Ljava/lang/Math;->round(F)I

    move-result v4

    const/4 v5, 0x2

    invoke-static {v5, v4}, Ljava/lang/Math;->max(II)I

    move-result v4

    .line 39
    const v6, 0x3d99999a    # 0.075f

    mul-float/2addr v6, v1

    invoke-static {v6}, Ljava/lang/Math;->round(F)I

    move-result v6

    iput v6, v2, Landroid/widget/FrameLayout$LayoutParams;->width:I

    iput v6, v2, Landroid/widget/FrameLayout$LayoutParams;->height:I

    int-to-float v6, v0

    const v7, 0x3f48f5c3    # 0.785f

    mul-float/2addr v6, v7

    invoke-static {v6}, Ljava/lang/Math;->round(F)I

    move-result v6

    add-int/2addr v6, v4

    iput v6, v2, Landroid/widget/FrameLayout$LayoutParams;->leftMargin:I

    const v6, 0x3c449ba6    # 0.012f

    mul-float/2addr v1, v6

    invoke-static {v1}, Ljava/lang/Math;->round(F)I

    move-result v1

    iput v1, v2, Landroid/widget/FrameLayout$LayoutParams;->topMargin:I

    .line 40
    const/4 v1, 0x1

    const/4 v6, 0x0

    if-eqz v3, :cond_88

    invoke-virtual {v3}, Landroid/view/View;->getWidth()I

    move-result v7

    if-lez v7, :cond_88

    invoke-virtual {v3}, Landroid/view/View;->getHeight()I

    move-result v7

    if-lez v7, :cond_88

    new-array v7, v5, [I

    new-array v8, v5, [I

    invoke-virtual {p0, v7}, Landroid/view/View;->getLocationOnScreen([I)V

    invoke-virtual {v3, v8}, Landroid/view/View;->getLocationOnScreen([I)V

    invoke-virtual {v3}, Landroid/view/View;->getWidth()I

    move-result v9

    iput v9, v2, Landroid/widget/FrameLayout$LayoutParams;->width:I

    invoke-virtual {v3}, Landroid/view/View;->getHeight()I

    move-result v3

    iput v3, v2, Landroid/widget/FrameLayout$LayoutParams;->height:I

    aget v3, v8, v6

    aget v9, v7, v6

    sub-int/2addr v3, v9

    iget v9, v2, Landroid/widget/FrameLayout$LayoutParams;->width:I

    add-int/2addr v3, v9

    add-int/2addr v3, v4

    iput v3, v2, Landroid/widget/FrameLayout$LayoutParams;->leftMargin:I

    aget v3, v8, v1

    aget v4, v7, v1

    sub-int/2addr v3, v4

    iput v3, v2, Landroid/widget/FrameLayout$LayoutParams;->topMargin:I

    .line 41
    :cond_88
    new-instance v3, Landroid/graphics/Rect;

    invoke-direct {v3}, Landroid/graphics/Rect;-><init>()V

    invoke-virtual {p0, v3}, Landroid/view/View;->getWindowVisibleDisplayFrame(Landroid/graphics/Rect;)V

    new-array v4, v5, [I

    invoke-virtual {p0, v4}, Landroid/view/View;->getLocationOnScreen([I)V

    iget p0, v2, Landroid/widget/FrameLayout$LayoutParams;->leftMargin:I

    iget v5, v2, Landroid/widget/FrameLayout$LayoutParams;->width:I

    sub-int/2addr v0, v5

    invoke-static {p0, v0}, Ljava/lang/Math;->min(II)I

    move-result p0

    invoke-static {v6, p0}, Ljava/lang/Math;->max(II)I

    move-result p0

    iput p0, v2, Landroid/widget/FrameLayout$LayoutParams;->leftMargin:I

    iget p0, v2, Landroid/widget/FrameLayout$LayoutParams;->topMargin:I

    iget v0, v3, Landroid/graphics/Rect;->top:I

    aget v1, v4, v1

    sub-int/2addr v0, v1

    invoke-static {p0, v0}, Ljava/lang/Math;->max(II)I

    move-result p0

    iput p0, v2, Landroid/widget/FrameLayout$LayoutParams;->topMargin:I

    iget p0, v2, Landroid/widget/FrameLayout$LayoutParams;->width:I

    iget v0, v2, Landroid/widget/FrameLayout$LayoutParams;->height:I

    invoke-static {p0, v0}, Ljava/lang/Math;->min(II)I

    move-result p0

    int-to-float p0, p0

    const v0, 0x3ea3d70a    # 0.32f

    mul-float/2addr p0, v0

    invoke-virtual {p1, v6, p0}, Landroid/widget/Button;->setTextSize(IF)V

    invoke-virtual {p1, v2}, Landroid/widget/Button;->setLayoutParams(Landroid/view/ViewGroup$LayoutParams;)V

    .line 42
    return-void

    .line 36
    :cond_c5
    :goto_c5
    return-void
.end method

.method private static request(Landroid/app/Activity;Landroid/widget/Button;Z)V
    .registers 5

    .line 52
    sget-object v0, Ljava/lang/Boolean;->TRUE:Ljava/lang/Boolean;

    sget-object v1, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->waiting:Ljava/util/WeakHashMap;

    invoke-virtual {v1, p1}, Ljava/util/WeakHashMap;->get(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v1

    invoke-virtual {v0, v1}, Ljava/lang/Boolean;->equals(Ljava/lang/Object;)Z

    move-result v0

    const/4 v1, 0x0

    if-eqz v0, :cond_18

    sget-object p2, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->waiting:Ljava/util/WeakHashMap;

    invoke-virtual {p2, p1}, Ljava/util/WeakHashMap;->remove(Ljava/lang/Object;)Ljava/lang/Object;

    invoke-static {p0, p1, v1}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch;->paint(Landroid/app/Activity;Landroid/widget/Button;I)V

    return-void

    .line 53
    :cond_18
    invoke-virtual {p1, v1}, Landroid/widget/Button;->setEnabled(Z)V

    new-instance v0, Ljava/lang/Thread;

    new-instance v1, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda10;

    invoke-direct {v1, p0, p2, p1}, Lorg/efootballrevival/runtimeprobe/SinglePlayerInMatch$$ExternalSyntheticLambda10;-><init>(Landroid/app/Activity;ZLandroid/widget/Button;)V

    const-string p0, "SinglePlayerInMatch"

    invoke-direct {v0, v1, p0}, Ljava/lang/Thread;-><init>(Ljava/lang/Runnable;Ljava/lang/String;)V

    .line 59
    invoke-virtual {v0}, Ljava/lang/Thread;->start()V

    .line 60
    return-void
.end method
