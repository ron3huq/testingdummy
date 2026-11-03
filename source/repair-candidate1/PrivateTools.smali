.class public final Lorg/efootballrevival/runtimeprobe/PrivateTools;
.super Ljava/lang/Object;
.source "PrivateTools.java"


# static fields
.field private static launcher:Ljava/lang/ref/WeakReference;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/lang/ref/WeakReference<",
            "Landroid/webkit/WebView;",
            ">;"
        }
    .end annotation
.end field


# direct methods
.method static constructor <clinit>()V
    .registers 2

    .line 4
    new-instance v0, Ljava/lang/ref/WeakReference;

    const/4 v1, 0x0

    invoke-direct {v0, v1}, Ljava/lang/ref/WeakReference;-><init>(Ljava/lang/Object;)V

    sput-object v0, Lorg/efootballrevival/runtimeprobe/PrivateTools;->launcher:Ljava/lang/ref/WeakReference;

    return-void
.end method

.method public constructor <init>()V
    .registers 1

    .line 3
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static bind(Landroid/webkit/WebView;)V
    .registers 2

    .line 5
    new-instance v0, Ljava/lang/ref/WeakReference;

    invoke-direct {v0, p0}, Ljava/lang/ref/WeakReference;-><init>(Ljava/lang/Object;)V

    sput-object v0, Lorg/efootballrevival/runtimeprobe/PrivateTools;->launcher:Ljava/lang/ref/WeakReference;

    return-void
.end method

.method static synthetic lambda$open$1(Landroid/app/Activity;Ljava/lang/String;Lorg/json/JSONObject;)V
    .registers 12

    .line 11
    const-string v0, "Close"

    const/4 v1, 0x0

    :try_start_3
    invoke-virtual {p0}, Landroid/app/Activity;->isFinishing()Z

    move-result v2

    if-eqz v2, :cond_a

    return-void

    .line 12
    :cond_a
    const-string v2, "transfer"

    invoke-virtual {v2, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v2

    if-eqz v2, :cond_16

    invoke-static {p0}, Lorg/efootballrevival/runtimeprobe/TransferEditor;->show(Landroid/app/Activity;)V

    return-void

    .line 13
    :cond_16
    const-string v2, "single-player"

    invoke-virtual {v2, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z
    move-result v2
    if-eqz v2, :full8_existing_tools

    invoke-static {p0}, Lorg/efootballrevival/runtimeprobe/SinglePlayerSettings;->open(Landroid/app/Activity;)V
    return-void

    :full8_existing_tools
    const-string v2, "diagnostics"

    invoke-virtual {v2, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v2

    const/4 v3, 0x0

    if-eqz v2, :cond_35

    new-instance p1, Landroid/widget/LinearLayout;

    invoke-direct {p1, p0}, Landroid/widget/LinearLayout;-><init>(Landroid/content/Context;)V

    invoke-static {p0, p1}, Lorg/efootballrevival/runtimeprobe/RuntimeDiagnostics;->attach(Landroid/app/Activity;Landroid/view/View;)V

    invoke-virtual {p1}, Landroid/widget/LinearLayout;->getChildCount()I

    move-result p2

    if-lez p2, :cond_34

    invoke-virtual {p1, v3}, Landroid/widget/LinearLayout;->getChildAt(I)Landroid/view/View;

    move-result-object p1

    invoke-virtual {p1}, Landroid/view/View;->performClick()Z

    :cond_34
    return-void

    .line 14
    :cond_35
    if-eqz p2, :cond_17a

    .line 15
    new-instance v2, Landroid/widget/LinearLayout;

    invoke-direct {v2, p0}, Landroid/widget/LinearLayout;-><init>(Landroid/content/Context;)V

    const/4 v4, 0x1

    invoke-virtual {v2, v4}, Landroid/widget/LinearLayout;->setOrientation(I)V

    .line 16
    nop

    .line 17
    invoke-virtual {p1}, Ljava/lang/String;->hashCode()I

    move-result v5

    const/4 v6, -0x1

    sparse-switch v5, :sswitch_data_1a2

    :cond_49
    goto :goto_a4

    :sswitch_4a
    const-string v4, "equipment"

    invoke-virtual {p1, v4}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result p1

    if-eqz p1, :cond_49

    const/4 v4, 0x2

    goto :goto_a5

    :sswitch_54
    const-string v4, "stats"

    invoke-virtual {p1, v4}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result p1

    if-eqz p1, :cond_49

    const/4 v4, 0x5

    goto :goto_a5

    :sswitch_5e
    const-string v5, "model"

    invoke-virtual {p1, v5}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result p1

    if-eqz p1, :cond_49

    goto :goto_a5

    :sswitch_67
    const-string v4, "identity"

    invoke-virtual {p1, v4}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result p1

    if-eqz p1, :cond_49

    const/4 v4, 0x3

    goto :goto_a5

    :sswitch_71
    const-string v4, "measurements"

    invoke-virtual {p1, v4}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result p1

    if-eqz p1, :cond_49

    move v4, v3

    goto :goto_a5

    :sswitch_7b
    const-string v4, "skin-celebration"

    invoke-virtual {p1, v4}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result p1

    if-eqz p1, :cond_49

    const/4 v4, 0x7

    goto :goto_a5

    :sswitch_85
    const-string v4, "traits"

    invoke-virtual {p1, v4}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result p1

    if-eqz p1, :cond_49

    const/4 v4, 0x4

    goto :goto_a5

    :sswitch_8f
    const-string v4, "skills"

    invoke-virtual {p1, v4}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result p1

    if-eqz p1, :cond_49

    const/16 v4, 0x8

    goto :goto_a5

    :sswitch_9a
    const-string v4, "motion"

    invoke-virtual {p1, v4}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result p1

    if-eqz p1, :cond_49

    const/4 v4, 0x6

    goto :goto_a5

    :goto_a4
    move v4, v6

    :goto_a5
    packed-switch v4, :pswitch_data_1c8

    .line 27
    new-instance p1, Ljava/lang/IllegalArgumentException;

    goto/16 :goto_174

    .line 26
    :pswitch_ac
    const-string p1, "Player Skills"

    invoke-static {p0, v2, p2}, Lorg/efootballrevival/runtimeprobe/TuningEditor;->attachSkills(Landroid/app/Activity;Landroid/widget/LinearLayout;Lorg/json/JSONObject;)V

    move p2, v3

    goto :goto_ea

    .line 25
    :pswitch_b3
    const-string p1, "Skin & Celebrations"

    invoke-static {p0, v2, p2}, Lorg/efootballrevival/runtimeprobe/AppearanceChoices;->attach(Landroid/app/Activity;Landroid/widget/LinearLayout;Lorg/json/JSONObject;)V

    move p2, v6

    goto :goto_ea

    .line 24
    :pswitch_ba
    const-string p1, "Animation"

    invoke-static {p0, v2, p2}, Lorg/efootballrevival/runtimeprobe/MotionEditor;->attach(Landroid/app/Activity;Landroid/widget/LinearLayout;Lorg/json/JSONObject;)V

    move p2, v3

    goto :goto_ea

    .line 23
    :pswitch_c1
    const-string p1, "Abilities"

    invoke-static {p0, v2, p2}, Lorg/efootballrevival/runtimeprobe/StatEditor;->attach(Landroid/app/Activity;Landroid/widget/LinearLayout;Lorg/json/JSONObject;)V

    move p2, v3

    goto :goto_ea

    .line 22
    :pswitch_c8
    const-string p1, "Foot & Resistance"

    invoke-static {p0, v2, p2}, Lorg/efootballrevival/runtimeprobe/ProfileEditor;->attachTraits(Landroid/app/Activity;Landroid/widget/LinearLayout;Lorg/json/JSONObject;)V

    move p2, v3

    goto :goto_ea

    .line 21
    :pswitch_cf
    const-string p1, "Identity & Model Copy"

    invoke-static {p0, v2, p2}, Lorg/efootballrevival/runtimeprobe/ProfileEditor;->attach(Landroid/app/Activity;Landroid/widget/LinearLayout;Lorg/json/JSONObject;)V

    move p2, v6

    goto :goto_ea

    .line 20
    :pswitch_d6
    const-string p1, "Equipment"

    invoke-static {p0, v2, p2}, Lorg/efootballrevival/runtimeprobe/EquipmentEditor;->attach(Landroid/app/Activity;Landroid/widget/LinearLayout;Lorg/json/JSONObject;)V

    move p2, v6

    goto :goto_ea

    .line 19
    :pswitch_dd
    const-string p1, "Player Model"

    invoke-static {p0, v2, p2}, Lorg/efootballrevival/runtimeprobe/PlayerModelEditor;->attach(Landroid/app/Activity;Landroid/widget/LinearLayout;Lorg/json/JSONObject;)V

    move p2, v3

    goto :goto_ea

    .line 18
    :pswitch_e4
    const-string p1, "Height & Weight"

    invoke-static {p0, v2, p2}, Lorg/efootballrevival/runtimeprobe/BodyEditor;->attach(Landroid/app/Activity;Landroid/widget/LinearLayout;Lorg/json/JSONObject;)V

    move p2, v3

    .line 29
    :goto_ea
    if-ltz p2, :cond_fa

    invoke-virtual {v2}, Landroid/widget/LinearLayout;->getChildCount()I

    move-result v4

    if-le v4, p2, :cond_fa

    invoke-virtual {v2, p2}, Landroid/widget/LinearLayout;->getChildAt(I)Landroid/view/View;

    move-result-object p1

    invoke-virtual {p1}, Landroid/view/View;->performClick()Z

    return-void

    .line 30
    :cond_fa
    invoke-virtual {p0}, Landroid/app/Activity;->getResources()Landroid/content/res/Resources;

    move-result-object p2

    invoke-virtual {p2}, Landroid/content/res/Resources;->getDisplayMetrics()Landroid/util/DisplayMetrics;

    move-result-object p2

    iget p2, p2, Landroid/util/DisplayMetrics;->density:F

    const/high16 v4, 0x41800000    # 16.0f

    mul-float/2addr p2, v4

    invoke-static {p2}, Ljava/lang/Math;->round(F)I

    move-result p2

    invoke-virtual {v2, p2, p2, p2, p2}, Landroid/widget/LinearLayout;->setPadding(IIII)V

    const v4, -0xf8e8dc

    invoke-virtual {v2, v4}, Landroid/widget/LinearLayout;->setBackgroundColor(I)V

    .line 31
    move v4, v3

    :goto_115
    invoke-virtual {v2}, Landroid/widget/LinearLayout;->getChildCount()I

    move-result v5

    if-ge v4, v5, :cond_150

    invoke-virtual {v2, v4}, Landroid/widget/LinearLayout;->getChildAt(I)Landroid/view/View;

    move-result-object v5

    instance-of v7, v5, Landroid/widget/Button;

    if-eqz v7, :cond_14d

    check-cast v5, Landroid/widget/Button;

    invoke-virtual {v5, v3}, Landroid/widget/Button;->setAllCaps(Z)V

    const v7, -0x170c08

    invoke-virtual {v5, v7}, Landroid/widget/Button;->setTextColor(I)V

    new-instance v7, Landroid/graphics/drawable/GradientDrawable;

    invoke-direct {v7}, Landroid/graphics/drawable/GradientDrawable;-><init>()V

    const v8, -0xefd4c3

    invoke-virtual {v7, v8}, Landroid/graphics/drawable/GradientDrawable;->setColor(I)V

    int-to-float v8, p2

    invoke-virtual {v7, v8}, Landroid/graphics/drawable/GradientDrawable;->setCornerRadius(F)V

    invoke-virtual {v5, v7}, Landroid/widget/Button;->setBackground(Landroid/graphics/drawable/Drawable;)V

    new-instance v7, Landroid/widget/LinearLayout$LayoutParams;

    const/4 v8, -0x2

    invoke-direct {v7, v6, v8}, Landroid/widget/LinearLayout$LayoutParams;-><init>(II)V

    div-int/lit8 v8, p2, 0x2

    iput v8, v7, Landroid/widget/LinearLayout$LayoutParams;->bottomMargin:I

    invoke-virtual {v5, v7}, Landroid/widget/Button;->setLayoutParams(Landroid/view/ViewGroup$LayoutParams;)V

    :cond_14d
    add-int/lit8 v4, v4, 0x1

    goto :goto_115

    .line 32
    :cond_150
    new-instance p2, Landroid/widget/ScrollView;

    invoke-direct {p2, p0}, Landroid/widget/ScrollView;-><init>(Landroid/content/Context;)V

    invoke-virtual {p2, v2}, Landroid/widget/ScrollView;->addView(Landroid/view/View;)V

    new-instance v2, Landroid/app/AlertDialog$Builder;

    invoke-direct {v2, p0}, Landroid/app/AlertDialog$Builder;-><init>(Landroid/content/Context;)V

    invoke-virtual {v2, p1}, Landroid/app/AlertDialog$Builder;->setTitle(Ljava/lang/CharSequence;)Landroid/app/AlertDialog$Builder;

    move-result-object p1

    invoke-virtual {p1, p2}, Landroid/app/AlertDialog$Builder;->setView(Landroid/view/View;)Landroid/app/AlertDialog$Builder;

    move-result-object p1

    invoke-virtual {p1, v0, v1}, Landroid/app/AlertDialog$Builder;->setNegativeButton(Ljava/lang/CharSequence;Landroid/content/DialogInterface$OnClickListener;)Landroid/app/AlertDialog$Builder;

    move-result-object p1

    invoke-virtual {p1}, Landroid/app/AlertDialog$Builder;->create()Landroid/app/AlertDialog;

    move-result-object p1

    invoke-virtual {p1}, Landroid/app/AlertDialog;->show()V

    invoke-static {p0, p1}, Lorg/efootballrevival/runtimeprobe/ResponsiveUi;->fit(Landroid/app/Activity;Landroid/app/AlertDialog;)V

    .line 33
    goto :goto_1a1

    .line 27
    :goto_174
    const-string p2, "Unknown editor tool"

    invoke-direct {p1, p2}, Ljava/lang/IllegalArgumentException;-><init>(Ljava/lang/String;)V

    throw p1

    .line 14
    :cond_17a
    new-instance p1, Ljava/lang/IllegalArgumentException;

    const-string p2, "Select an owned player first"

    invoke-direct {p1, p2}, Ljava/lang/IllegalArgumentException;-><init>(Ljava/lang/String;)V

    throw p1
    :try_end_182
    .catch Ljava/lang/Exception; {:try_start_3 .. :try_end_182} :catch_182

    .line 33
    :catch_182
    move-exception p1

    new-instance p2, Landroid/app/AlertDialog$Builder;

    invoke-direct {p2, p0}, Landroid/app/AlertDialog$Builder;-><init>(Landroid/content/Context;)V

    const-string p0, "Editor"

    invoke-virtual {p2, p0}, Landroid/app/AlertDialog$Builder;->setTitle(Ljava/lang/CharSequence;)Landroid/app/AlertDialog$Builder;

    move-result-object p0

    invoke-virtual {p1}, Ljava/lang/Exception;->getMessage()Ljava/lang/String;

    move-result-object p1

    invoke-static {p1}, Ljava/lang/String;->valueOf(Ljava/lang/Object;)Ljava/lang/String;

    move-result-object p1

    invoke-virtual {p0, p1}, Landroid/app/AlertDialog$Builder;->setMessage(Ljava/lang/CharSequence;)Landroid/app/AlertDialog$Builder;

    move-result-object p0

    invoke-virtual {p0, v0, v1}, Landroid/app/AlertDialog$Builder;->setPositiveButton(Ljava/lang/CharSequence;Landroid/content/DialogInterface$OnClickListener;)Landroid/app/AlertDialog$Builder;

    move-result-object p0

    invoke-virtual {p0}, Landroid/app/AlertDialog$Builder;->show()Landroid/app/AlertDialog;

    :goto_1a1
    return-void

    :sswitch_data_1a2
    .sparse-switch
        -0x3fad404a -> :sswitch_9a
        -0x35ad7fbe -> :sswitch_8f
        -0x3399afdb -> :sswitch_85
        -0x1becb166 -> :sswitch_7b
        -0x159763c9 -> :sswitch_71
        -0x8178f42 -> :sswitch_67
        0x633fb29 -> :sswitch_5e
        0x68ac49f -> :sswitch_54
        0x4027e58e -> :sswitch_4a
    .end sparse-switch

    :pswitch_data_1c8
    .packed-switch 0x0
        :pswitch_e4
        :pswitch_dd
        :pswitch_d6
        :pswitch_cf
        :pswitch_c8
        :pswitch_c1
        :pswitch_ba
        :pswitch_b3
        :pswitch_ac
    .end packed-switch
.end method

.method static synthetic lambda$portraitSaved$0(Landroid/app/Activity;Lorg/json/JSONObject;)V
    .registers 9

    .line 6
    sget-object v0, Lorg/efootballrevival/runtimeprobe/PrivateTools;->launcher:Ljava/lang/ref/WeakReference;

    invoke-virtual {v0}, Ljava/lang/ref/WeakReference;->get()Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Landroid/webkit/WebView;

    if-eqz v0, :cond_5b

    invoke-virtual {p0}, Landroid/app/Activity;->isFinishing()Z

    move-result p0

    if-eqz p0, :cond_11

    goto :goto_5b

    :cond_11
    :try_start_11
    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object p0

    const-string v1, "evaluateJavascript"

    const/4 v2, 0x2

    new-array v3, v2, [Ljava/lang/Class;

    const-class v4, Ljava/lang/String;

    const/4 v5, 0x0

    aput-object v4, v3, v5

    const-string v4, "android.webkit.ValueCallback"

    invoke-static {v4}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;

    move-result-object v4

    const/4 v6, 0x1

    aput-object v4, v3, v6

    invoke-virtual {p0, v1, v3}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object p0

    new-array v1, v2, [Ljava/lang/Object;

    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V

    const-string v3, "window.EditorUI && window.EditorUI.U.refreshPortrait("

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v2

    const-string v3, "id"

    invoke-virtual {p1, v3}, Lorg/json/JSONObject;->optString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object p1

    invoke-static {p1}, Lorg/json/JSONObject;->quote(Ljava/lang/String;)Ljava/lang/String;

    move-result-object p1

    invoke-virtual {v2, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p1

    const-string v2, ")"

    invoke-virtual {p1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p1

    invoke-virtual {p1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1

    aput-object p1, v1, v5

    const/4 p1, 0x0

    aput-object p1, v1, v6

    invoke-virtual {p0, v0, v1}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;
    :try_end_59
    .catch Ljava/lang/Exception; {:try_start_11 .. :try_end_59} :catch_5a

    goto :goto_5b

    :catch_5a
    move-exception p0

    :cond_5b
    :goto_5b
    return-void
.end method

.method public static open(Landroid/app/Activity;Lorg/json/JSONObject;)V
    .registers 4

    .line 9
    const-string v0, "tool"

    invoke-virtual {p1, v0}, Lorg/json/JSONObject;->optString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    const-string v1, "player"

    invoke-virtual {p1, v1}, Lorg/json/JSONObject;->optJSONObject(Ljava/lang/String;)Lorg/json/JSONObject;

    move-result-object p1

    .line 10
    new-instance v1, Lorg/efootballrevival/runtimeprobe/PrivateTools$$ExternalSyntheticLambda0;

    invoke-direct {v1, p0, v0, p1}, Lorg/efootballrevival/runtimeprobe/PrivateTools$$ExternalSyntheticLambda0;-><init>(Landroid/app/Activity;Ljava/lang/String;Lorg/json/JSONObject;)V

    invoke-virtual {p0, v1}, Landroid/app/Activity;->runOnUiThread(Ljava/lang/Runnable;)V

    .line 34
    return-void
.end method

.method public static portraitSaved(Landroid/app/Activity;Lorg/json/JSONObject;)V
    .registers 3

    .line 6
    new-instance v0, Lorg/efootballrevival/runtimeprobe/PrivateTools$$ExternalSyntheticLambda1;

    invoke-direct {v0, p0, p1}, Lorg/efootballrevival/runtimeprobe/PrivateTools$$ExternalSyntheticLambda1;-><init>(Landroid/app/Activity;Lorg/json/JSONObject;)V

    invoke-virtual {p0, v0}, Landroid/app/Activity;->runOnUiThread(Ljava/lang/Runnable;)V

    return-void
.end method
