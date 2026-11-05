.class public final Lorg/efootballrevival/runtimeprobe/AppearanceChoices;
.super Ljava/lang/Object;
.source "AppearanceChoices.java"


# direct methods
.method public constructor <init>()V
    .registers 1

    .line 3
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static attach(Landroid/app/Activity;Landroid/widget/LinearLayout;Lorg/json/JSONObject;)V
    .registers 4

    .line 6
    const/4 v0, 0x1

    invoke-static {p0, p1, p2, v0}, Lorg/efootballrevival/runtimeprobe/AppearanceChoices;->button(Landroid/app/Activity;Landroid/widget/LinearLayout;Lorg/json/JSONObject;Z)V

    const/4 v0, 0x0

    invoke-static {p0, p1, p2, v0}, Lorg/efootballrevival/runtimeprobe/AppearanceChoices;->button(Landroid/app/Activity;Landroid/widget/LinearLayout;Lorg/json/JSONObject;Z)V

    invoke-static {p0, p1, p2}, Lorg/efootballrevival/runtimeprobe/MotionEditor;->attach(Landroid/app/Activity;Landroid/widget/LinearLayout;Lorg/json/JSONObject;)V

    invoke-static {p0, p1, p2}, Lorg/efootballrevival/runtimeprobe/EquipmentEditor;->attach(Landroid/app/Activity;Landroid/widget/LinearLayout;Lorg/json/JSONObject;)V

    invoke-static {p0, p1, p2}, Lorg/efootballrevival/runtimeprobe/ProfileEditor;->attach(Landroid/app/Activity;Landroid/widget/LinearLayout;Lorg/json/JSONObject;)V

    return-void
.end method

.method private static button(Landroid/app/Activity;Landroid/widget/LinearLayout;Lorg/json/JSONObject;Z)V
    .registers 6

    .line 7
    new-instance v0, Landroid/widget/Button;

    invoke-direct {v0, p0}, Landroid/widget/Button;-><init>(Landroid/content/Context;)V

    if-eqz p3, :cond_a

    const-string v1, "Skin \u00b7 Game palettes"

    goto :goto_c

    :cond_a
    const-string v1, "Celebration IDs"

    :goto_c
    invoke-virtual {v0, v1}, Landroid/widget/Button;->setText(Ljava/lang/CharSequence;)V

    const/4 v1, 0x0

    invoke-virtual {v0, v1}, Landroid/widget/Button;->setAllCaps(Z)V

    new-instance v1, Lorg/efootballrevival/runtimeprobe/AppearanceChoices$$ExternalSyntheticLambda3;

    invoke-direct {v1, v0, p2, p3, p0}, Lorg/efootballrevival/runtimeprobe/AppearanceChoices$$ExternalSyntheticLambda3;-><init>(Landroid/widget/Button;Lorg/json/JSONObject;ZLandroid/app/Activity;)V

    invoke-virtual {v0, v1}, Landroid/widget/Button;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    new-instance p0, Landroid/widget/LinearLayout$LayoutParams;

    const/4 p2, -0x1

    const/4 p3, -0x2

    invoke-direct {p0, p2, p3}, Landroid/widget/LinearLayout$LayoutParams;-><init>(II)V

    invoke-virtual {p1, v0, p0}, Landroid/widget/LinearLayout;->addView(Landroid/view/View;Landroid/view/ViewGroup$LayoutParams;)V

    return-void
.end method

.method private static error(Landroid/app/Activity;Ljava/lang/Exception;)V
    .registers 3

    .line 5
    invoke-virtual {p0}, Landroid/app/Activity;->isFinishing()Z

    move-result v0

    if-nez v0, :cond_36

    new-instance v0, Landroid/app/AlertDialog$Builder;

    invoke-direct {v0, p0}, Landroid/app/AlertDialog$Builder;-><init>(Landroid/content/Context;)V

    const-string p0, "Appearance & Motion"

    invoke-virtual {v0, p0}, Landroid/app/AlertDialog$Builder;->setTitle(Ljava/lang/CharSequence;)Landroid/app/AlertDialog$Builder;

    move-result-object p0

    invoke-virtual {p1}, Ljava/lang/Exception;->getCause()Ljava/lang/Throwable;

    move-result-object v0

    if-nez v0, :cond_1c

    invoke-virtual {p1}, Ljava/lang/Exception;->getMessage()Ljava/lang/String;

    move-result-object p1

    goto :goto_24

    :cond_1c
    invoke-virtual {p1}, Ljava/lang/Exception;->getCause()Ljava/lang/Throwable;

    move-result-object p1

    invoke-virtual {p1}, Ljava/lang/Throwable;->getMessage()Ljava/lang/String;

    move-result-object p1

    :goto_24
    invoke-static {p1}, Ljava/lang/String;->valueOf(Ljava/lang/Object;)Ljava/lang/String;

    move-result-object p1

    invoke-virtual {p0, p1}, Landroid/app/AlertDialog$Builder;->setMessage(Ljava/lang/CharSequence;)Landroid/app/AlertDialog$Builder;

    move-result-object p0

    const-string p1, "Close"

    const/4 v0, 0x0

    invoke-virtual {p0, p1, v0}, Landroid/app/AlertDialog$Builder;->setPositiveButton(Ljava/lang/CharSequence;Landroid/content/DialogInterface$OnClickListener;)Landroid/app/AlertDialog$Builder;

    move-result-object p0

    invoke-virtual {p0}, Landroid/app/AlertDialog$Builder;->show()Landroid/app/AlertDialog;

    :cond_36
    return-void
.end method

.method private static form(Landroid/app/Activity;Lorg/json/JSONObject;Lorg/json/JSONObject;Z)V
    .registers 22

    .line 12
    move-object/from16 v10, p0

    move-object/from16 v2, p2

    new-instance v0, Landroid/widget/LinearLayout;

    invoke-direct {v0, v10}, Landroid/widget/LinearLayout;-><init>(Landroid/content/Context;)V

    const/4 v1, 0x1

    invoke-virtual {v0, v1}, Landroid/widget/LinearLayout;->setOrientation(I)V

    invoke-virtual/range {p0 .. p0}, Landroid/app/Activity;->getResources()Landroid/content/res/Resources;

    move-result-object v1

    invoke-virtual {v1}, Landroid/content/res/Resources;->getDisplayMetrics()Landroid/util/DisplayMetrics;

    move-result-object v1

    iget v1, v1, Landroid/util/DisplayMetrics;->density:F

    const/high16 v3, 0x41800000    # 16.0f

    mul-float/2addr v1, v3

    invoke-static {v1}, Ljava/lang/Math;->round(F)I

    move-result v1

    invoke-virtual {v0, v1, v1, v1, v1}, Landroid/widget/LinearLayout;->setPadding(IIII)V

    const v1, -0xefe0c8

    invoke-virtual {v0, v1}, Landroid/widget/LinearLayout;->setBackgroundColor(I)V

    new-instance v1, Landroid/widget/ScrollView;

    invoke-direct {v1, v10}, Landroid/widget/ScrollView;-><init>(Landroid/content/Context;)V

    invoke-virtual {v1, v0}, Landroid/widget/ScrollView;->addView(Landroid/view/View;)V

    new-instance v3, Landroid/widget/TextView;

    invoke-direct {v3, v10}, Landroid/widget/TextView;-><init>(Landroid/content/Context;)V

    const v4, -0x362012

    invoke-virtual {v3, v4}, Landroid/widget/TextView;->setTextColor(I)V

    invoke-virtual {v0, v3}, Landroid/widget/LinearLayout;->addView(Landroid/view/View;)V

    .line 13
    const/4 v4, 0x0

    if-eqz p3, :cond_6a

    const-string v5, "Choose a skin tone. For Ronaldo2027 this changes the head and body together. Other imported faces keep their source colouring. Save before entering the game, then restart to apply."

    invoke-virtual {v3, v5}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    const-string v16, "Palette5"

    const-string v17, "Palette6"

    const-string v11, "Keep current / default"

    const-string v12, "Palette1"

    const-string v13, "Palette2"

    const-string v14, "Palette3"

    const-string v15, "Palette4"

    filled-new-array/range {v11 .. v17}, [Ljava/lang/String;

    move-result-object v3

    const-string v5, "skin"

    invoke-virtual {v2, v5}, Lorg/json/JSONObject;->optInt(Ljava/lang/String;)I

    move-result v5

    const-string v6, "Skin palette"

    invoke-static {v10, v0, v6, v3, v5}, Lorg/efootballrevival/runtimeprobe/AppearanceChoices;->select(Landroid/app/Activity;Landroid/widget/LinearLayout;Ljava/lang/String;[Ljava/lang/String;I)Landroid/widget/Spinner;

    move-result-object v0

    move-object v7, v0

    move-object v3, v4

    move-object v5, v3

    move-object v6, v5

    move-object v9, v6

    goto/16 :goto_e2

    .line 14
    :cond_6a
    const-string v5, "Select IDs stored in the card\'s actual game parameters. Main and Memorial use separate ID tables. These IDs are not animation filenames. Close and reopen the app after saving before entering a match."

    invoke-virtual {v3, v5}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    const-string v3, "choices"

    invoke-virtual {v2, v3}, Lorg/json/JSONObject;->optJSONObject(Ljava/lang/String;)Lorg/json/JSONObject;

    move-result-object v3

    const-string v5, "59"

    invoke-virtual {v3, v5}, Lorg/json/JSONObject;->optJSONArray(Ljava/lang/String;)Lorg/json/JSONArray;

    move-result-object v6

    const-string v7, "60"

    invoke-virtual {v3, v7}, Lorg/json/JSONObject;->optJSONArray(Ljava/lang/String;)Lorg/json/JSONArray;

    move-result-object v3

    invoke-static {v6}, Lorg/efootballrevival/runtimeprobe/AppearanceChoices;->ids(Lorg/json/JSONArray;)[I

    move-result-object v8

    invoke-static {v3}, Lorg/efootballrevival/runtimeprobe/AppearanceChoices;->ids(Lorg/json/JSONArray;)[I

    move-result-object v9

    new-instance v11, Ljava/lang/StringBuilder;

    invoke-direct {v11}, Ljava/lang/StringBuilder;-><init>()V

    const-string v12, "Main \u00b7 Current ID "

    invoke-virtual {v11, v12}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v11

    invoke-virtual {v2, v5}, Lorg/json/JSONObject;->optInt(Ljava/lang/String;)I

    move-result v12

    invoke-virtual {v11, v12}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v11

    invoke-virtual {v11}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v11

    invoke-virtual {v2, v5}, Lorg/json/JSONObject;->optInt(Ljava/lang/String;)I

    move-result v12

    invoke-static {v6, v12}, Lorg/efootballrevival/runtimeprobe/AppearanceChoices;->names(Lorg/json/JSONArray;I)[Ljava/lang/String;

    move-result-object v6

    invoke-virtual {v2, v5}, Lorg/json/JSONObject;->optInt(Ljava/lang/String;)I

    move-result v5

    invoke-static {v8, v5}, Lorg/efootballrevival/runtimeprobe/AppearanceChoices;->position([II)I

    move-result v5

    invoke-static {v10, v0, v11, v6, v5}, Lorg/efootballrevival/runtimeprobe/AppearanceChoices;->select(Landroid/app/Activity;Landroid/widget/LinearLayout;Ljava/lang/String;[Ljava/lang/String;I)Landroid/widget/Spinner;

    move-result-object v5

    new-instance v6, Ljava/lang/StringBuilder;

    invoke-direct {v6}, Ljava/lang/StringBuilder;-><init>()V

    const-string v11, "Memorial \u00b7 Current ID "

    invoke-virtual {v6, v11}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v6

    invoke-virtual {v2, v7}, Lorg/json/JSONObject;->optInt(Ljava/lang/String;)I

    move-result v11

    invoke-virtual {v6, v11}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v6

    invoke-virtual {v6}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v6

    invoke-virtual {v2, v7}, Lorg/json/JSONObject;->optInt(Ljava/lang/String;)I

    move-result v11

    invoke-static {v3, v11}, Lorg/efootballrevival/runtimeprobe/AppearanceChoices;->names(Lorg/json/JSONArray;I)[Ljava/lang/String;

    move-result-object v3

    invoke-virtual {v2, v7}, Lorg/json/JSONObject;->optInt(Ljava/lang/String;)I

    move-result v7

    invoke-static {v9, v7}, Lorg/efootballrevival/runtimeprobe/AppearanceChoices;->position([II)I

    move-result v7

    invoke-static {v10, v0, v6, v3, v7}, Lorg/efootballrevival/runtimeprobe/AppearanceChoices;->select(Landroid/app/Activity;Landroid/widget/LinearLayout;Ljava/lang/String;[Ljava/lang/String;I)Landroid/widget/Spinner;

    move-result-object v0

    move-object v6, v0

    move-object v7, v4

    move-object v3, v8

    .line 15
    :goto_e2
    new-instance v0, Landroid/app/AlertDialog$Builder;

    invoke-direct {v0, v10}, Landroid/app/AlertDialog$Builder;-><init>(Landroid/content/Context;)V

    if-eqz p3, :cond_ec

    const-string v8, "Skin \u00b7 Game palettes"

    goto :goto_ee

    :cond_ec
    const-string v8, "Celebration IDs"

    :goto_ee
    invoke-virtual {v0, v8}, Landroid/app/AlertDialog$Builder;->setTitle(Ljava/lang/CharSequence;)Landroid/app/AlertDialog$Builder;

    move-result-object v0

    invoke-virtual {v0, v1}, Landroid/app/AlertDialog$Builder;->setView(Landroid/view/View;)Landroid/app/AlertDialog$Builder;

    move-result-object v0

    const-string v1, "Cancel"

    invoke-virtual {v0, v1, v4}, Landroid/app/AlertDialog$Builder;->setNegativeButton(Ljava/lang/CharSequence;Landroid/content/DialogInterface$OnClickListener;)Landroid/app/AlertDialog$Builder;

    move-result-object v0

    const-string v1, "Save"

    invoke-virtual {v0, v1, v4}, Landroid/app/AlertDialog$Builder;->setPositiveButton(Ljava/lang/CharSequence;Landroid/content/DialogInterface$OnClickListener;)Landroid/app/AlertDialog$Builder;

    move-result-object v0

    invoke-virtual {v0}, Landroid/app/AlertDialog$Builder;->create()Landroid/app/AlertDialog;

    move-result-object v11

    invoke-virtual {v11}, Landroid/app/AlertDialog;->show()V

    invoke-static {v10, v11}, Lorg/efootballrevival/runtimeprobe/ResponsiveUi;->fit(Landroid/app/Activity;Landroid/app/AlertDialog;)V

    const/4 v0, -0x1

    invoke-virtual {v11, v0}, Landroid/app/AlertDialog;->getButton(I)Landroid/widget/Button;

    move-result-object v12

    new-instance v13, Lorg/efootballrevival/runtimeprobe/AppearanceChoices$$ExternalSyntheticLambda4;

    move-object v0, v13

    move/from16 v1, p3

    move-object/from16 v2, p2

    move-object v4, v5

    move-object v5, v9

    move-object/from16 v8, p1

    move-object v9, v11

    move-object/from16 v10, p0

    invoke-direct/range {v0 .. v10}, Lorg/efootballrevival/runtimeprobe/AppearanceChoices$$ExternalSyntheticLambda4;-><init>(ZLorg/json/JSONObject;[ILandroid/widget/Spinner;[ILandroid/widget/Spinner;Landroid/widget/Spinner;Lorg/json/JSONObject;Landroid/app/AlertDialog;Landroid/app/Activity;)V

    invoke-virtual {v12, v13}, Landroid/widget/Button;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 16
    return-void
.end method

.method private static ids(Lorg/json/JSONArray;)[I
    .registers 6

    .line 9
    invoke-virtual {p0}, Lorg/json/JSONArray;->length()I

    move-result v0

    new-array v1, v0, [I

    const/4 v2, 0x0

    :goto_7
    if-ge v2, v0, :cond_18

    invoke-virtual {p0, v2}, Lorg/json/JSONArray;->optJSONObject(I)Lorg/json/JSONObject;

    move-result-object v3

    const-string v4, "id"

    invoke-virtual {v3, v4}, Lorg/json/JSONObject;->optInt(Ljava/lang/String;)I

    move-result v3

    aput v3, v1, v2

    add-int/lit8 v2, v2, 0x1

    goto :goto_7

    :cond_18
    return-object v1
.end method

.method static synthetic lambda$button$0(Landroid/widget/Button;Landroid/app/Activity;ZLorg/json/JSONObject;Lorg/json/JSONObject;)V
    .registers 6

    .line 7
    const/4 v0, 0x1

    invoke-virtual {p0, v0}, Landroid/widget/Button;->setEnabled(Z)V

    invoke-virtual {p1}, Landroid/app/Activity;->isFinishing()Z

    move-result p0

    if-nez p0, :cond_14

    if-eqz p2, :cond_10

    invoke-static {p1, p3, p4}, Lorg/efootballrevival/runtimeprobe/SkinColourEditor;->form(Landroid/app/Activity;Lorg/json/JSONObject;Lorg/json/JSONObject;)V

    goto :goto_14

    :cond_10
    const/4 p0, 0x0

    invoke-static {p1, p3, p4, p0}, Lorg/efootballrevival/runtimeprobe/AppearanceChoices;->form(Landroid/app/Activity;Lorg/json/JSONObject;Lorg/json/JSONObject;Z)V

    :cond_14
    :goto_14
    return-void
.end method

.method static synthetic lambda$button$1(Landroid/widget/Button;Landroid/app/Activity;Ljava/lang/Exception;)V
    .registers 4

    .line 7
    const/4 v0, 0x1

    invoke-virtual {p0, v0}, Landroid/widget/Button;->setEnabled(Z)V

    invoke-static {p1, p2}, Lorg/efootballrevival/runtimeprobe/AppearanceChoices;->error(Landroid/app/Activity;Ljava/lang/Exception;)V

    return-void
.end method

.method static synthetic lambda$button$2(Lorg/json/JSONObject;ZLandroid/app/Activity;Landroid/widget/Button;)V
    .registers 11

    .line 7
    :try_start_0
    new-instance v0, Lorg/json/JSONObject;

    invoke-virtual {p0}, Lorg/json/JSONObject;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-direct {v0, v1}, Lorg/json/JSONObject;-><init>(Ljava/lang/String;)V

    const-string v1, "section"

    if-eqz p1, :cond_10

    const-string v2, "skin"

    goto :goto_12

    :cond_10
    const-string v2, "celebration"

    :goto_12
    invoke-virtual {v0, v1, v2}, Lorg/json/JSONObject;->put(Ljava/lang/String;Ljava/lang/Object;)Lorg/json/JSONObject;

    move-result-object v0

    new-instance v6, Lorg/json/JSONObject;

    const-string v1, "ui78_appearance_get"

    invoke-static {p2, v1, v0}, Lorg/efootballrevival/runtimeprobe/AppearanceChoices;->manage(Landroid/app/Activity;Ljava/lang/String;Lorg/json/JSONObject;)Ljava/lang/String;

    move-result-object v0

    invoke-direct {v6, v0}, Lorg/json/JSONObject;-><init>(Ljava/lang/String;)V

    new-instance v0, Lorg/efootballrevival/runtimeprobe/AppearanceChoices$$ExternalSyntheticLambda1;

    move-object v1, v0

    move-object v2, p3

    move-object v3, p2

    move v4, p1

    move-object v5, p0

    invoke-direct/range {v1 .. v6}, Lorg/efootballrevival/runtimeprobe/AppearanceChoices$$ExternalSyntheticLambda1;-><init>(Landroid/widget/Button;Landroid/app/Activity;ZLorg/json/JSONObject;Lorg/json/JSONObject;)V

    invoke-virtual {p2, v0}, Landroid/app/Activity;->runOnUiThread(Ljava/lang/Runnable;)V
    :try_end_2e
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_2e} :catch_2f

    goto :goto_38

    :catch_2f
    move-exception p0

    new-instance p1, Lorg/efootballrevival/runtimeprobe/AppearanceChoices$$ExternalSyntheticLambda2;

    invoke-direct {p1, p3, p2, p0}, Lorg/efootballrevival/runtimeprobe/AppearanceChoices$$ExternalSyntheticLambda2;-><init>(Landroid/widget/Button;Landroid/app/Activity;Ljava/lang/Exception;)V

    invoke-virtual {p2, p1}, Landroid/app/Activity;->runOnUiThread(Ljava/lang/Runnable;)V

    :goto_38
    return-void
.end method

.method static synthetic lambda$button$3(Landroid/widget/Button;Lorg/json/JSONObject;ZLandroid/app/Activity;Landroid/view/View;)V
    .registers 6

    .line 7
    const/4 p4, 0x0

    invoke-virtual {p0, p4}, Landroid/widget/Button;->setEnabled(Z)V

    new-instance p4, Ljava/lang/Thread;

    new-instance v0, Lorg/efootballrevival/runtimeprobe/AppearanceChoices$$ExternalSyntheticLambda0;

    invoke-direct {v0, p1, p2, p3, p0}, Lorg/efootballrevival/runtimeprobe/AppearanceChoices$$ExternalSyntheticLambda0;-><init>(Lorg/json/JSONObject;ZLandroid/app/Activity;Landroid/widget/Button;)V

    const-string p0, "AppearanceChoicesLoad"

    invoke-direct {p4, v0, p0}, Ljava/lang/Thread;-><init>(Ljava/lang/Runnable;Ljava/lang/String;)V

    invoke-virtual {p4}, Ljava/lang/Thread;->start()V

    return-void
.end method

.method static synthetic lambda$form$4(Landroid/app/AlertDialog;Landroid/app/Activity;)V
    .registers 3

    .line 15
    invoke-virtual {p0}, Landroid/app/AlertDialog;->dismiss()V

    const-string p0, "Saved. Reopen the app before entering a match."

    const/4 v0, 0x1

    invoke-static {p1, p0, v0}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;

    move-result-object p0

    invoke-virtual {p0}, Landroid/widget/Toast;->show()V

    return-void
.end method

.method static synthetic lambda$form$5(Landroid/app/AlertDialog;Landroid/app/Activity;Ljava/lang/Exception;)V
    .registers 4

    .line 15
    const/4 v0, -0x1

    invoke-virtual {p0, v0}, Landroid/app/AlertDialog;->getButton(I)Landroid/widget/Button;

    move-result-object p0

    const/4 v0, 0x1

    invoke-virtual {p0, v0}, Landroid/widget/Button;->setEnabled(Z)V

    invoke-static {p1, p2}, Lorg/efootballrevival/runtimeprobe/AppearanceChoices;->error(Landroid/app/Activity;Ljava/lang/Exception;)V

    return-void
.end method

.method static synthetic lambda$form$6(Landroid/app/Activity;Lorg/json/JSONObject;Landroid/app/AlertDialog;)V
    .registers 5

    .line 15
    :try_start_0
    new-instance v0, Lorg/json/JSONObject;

    const-string v1, "ui78_appearance_apply"

    invoke-static {p0, v1, p1}, Lorg/efootballrevival/runtimeprobe/AppearanceChoices;->manage(Landroid/app/Activity;Ljava/lang/String;Lorg/json/JSONObject;)Ljava/lang/String;

    move-result-object p1

    invoke-direct {v0, p1}, Lorg/json/JSONObject;-><init>(Ljava/lang/String;)V

    const-string p1, "saved"

    invoke-virtual {v0, p1}, Lorg/json/JSONObject;->optBoolean(Ljava/lang/String;)Z

    move-result p1

    if-eqz p1, :cond_1c

    new-instance p1, Lorg/efootballrevival/runtimeprobe/AppearanceChoices$$ExternalSyntheticLambda5;

    invoke-direct {p1, p2, p0}, Lorg/efootballrevival/runtimeprobe/AppearanceChoices$$ExternalSyntheticLambda5;-><init>(Landroid/app/AlertDialog;Landroid/app/Activity;)V

    invoke-virtual {p0, p1}, Landroid/app/Activity;->runOnUiThread(Ljava/lang/Runnable;)V

    goto :goto_2d

    :cond_1c
    new-instance p1, Ljava/lang/Exception;

    const-string v0, "Save was not confirmed"

    invoke-direct {p1, v0}, Ljava/lang/Exception;-><init>(Ljava/lang/String;)V

    throw p1
    :try_end_24
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_24} :catch_24

    :catch_24
    move-exception p1

    new-instance v0, Lorg/efootballrevival/runtimeprobe/AppearanceChoices$$ExternalSyntheticLambda6;

    invoke-direct {v0, p2, p0, p1}, Lorg/efootballrevival/runtimeprobe/AppearanceChoices$$ExternalSyntheticLambda6;-><init>(Landroid/app/AlertDialog;Landroid/app/Activity;Ljava/lang/Exception;)V

    invoke-virtual {p0, v0}, Landroid/app/Activity;->runOnUiThread(Ljava/lang/Runnable;)V

    :goto_2d
    return-void
.end method

.method static synthetic lambda$form$7(ZLorg/json/JSONObject;[ILandroid/widget/Spinner;[ILandroid/widget/Spinner;Landroid/widget/Spinner;Lorg/json/JSONObject;Landroid/app/AlertDialog;Landroid/app/Activity;Landroid/view/View;)V
    .registers 12

    .line 15
    :try_start_0
    new-instance p10, Lorg/json/JSONObject;

    invoke-direct {p10}, Lorg/json/JSONObject;-><init>()V
    :try_end_5
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_5} :catch_65

    const-string v0, "59"

    if-eqz p0, :cond_e

    :try_start_9
    invoke-virtual {p1, v0}, Lorg/json/JSONObject;->optInt(Ljava/lang/String;)I

    move-result p2

    goto :goto_14

    :cond_e
    invoke-virtual {p3}, Landroid/widget/Spinner;->getSelectedItemPosition()I

    move-result p3

    aget p2, p2, p3

    :goto_14
    invoke-virtual {p10, v0, p2}, Lorg/json/JSONObject;->put(Ljava/lang/String;I)Lorg/json/JSONObject;

    move-result-object p2
    :try_end_18
    .catch Ljava/lang/Exception; {:try_start_9 .. :try_end_18} :catch_65

    const-string p3, "60"

    if-eqz p0, :cond_21

    :try_start_1c
    invoke-virtual {p1, p3}, Lorg/json/JSONObject;->optInt(Ljava/lang/String;)I

    move-result p4

    goto :goto_27

    :cond_21
    invoke-virtual {p5}, Landroid/widget/Spinner;->getSelectedItemPosition()I

    move-result p5

    aget p4, p4, p5

    :goto_27
    invoke-virtual {p2, p3, p4}, Lorg/json/JSONObject;->put(Ljava/lang/String;I)Lorg/json/JSONObject;

    move-result-object p2
    :try_end_2b
    .catch Ljava/lang/Exception; {:try_start_1c .. :try_end_2b} :catch_65

    const-string p3, "skin"

    if-eqz p0, :cond_34

    :try_start_2f
    invoke-virtual {p6}, Landroid/widget/Spinner;->getSelectedItemPosition()I

    move-result p0

    goto :goto_38

    :cond_34
    invoke-virtual {p1, p3}, Lorg/json/JSONObject;->optInt(Ljava/lang/String;)I

    move-result p0

    :goto_38
    if-lez p0, :cond_3d

    invoke-virtual {p2, p3, p0}, Lorg/json/JSONObject;->put(Ljava/lang/String;I)Lorg/json/JSONObject;

    :cond_3d
    new-instance p0, Lorg/json/JSONObject;

    invoke-virtual {p7}, Lorg/json/JSONObject;->toString()Ljava/lang/String;

    move-result-object p1

    invoke-direct {p0, p1}, Lorg/json/JSONObject;-><init>(Ljava/lang/String;)V

    const-string p1, "values"

    invoke-virtual {p0, p1, p2}, Lorg/json/JSONObject;->put(Ljava/lang/String;Ljava/lang/Object;)Lorg/json/JSONObject;

    move-result-object p0

    const/4 p1, -0x1

    invoke-virtual {p8, p1}, Landroid/app/AlertDialog;->getButton(I)Landroid/widget/Button;

    move-result-object p1

    const/4 p2, 0x0

    invoke-virtual {p1, p2}, Landroid/widget/Button;->setEnabled(Z)V

    new-instance p1, Ljava/lang/Thread;

    new-instance p2, Lorg/efootballrevival/runtimeprobe/AppearanceChoices$$ExternalSyntheticLambda7;

    invoke-direct {p2, p9, p0, p8}, Lorg/efootballrevival/runtimeprobe/AppearanceChoices$$ExternalSyntheticLambda7;-><init>(Landroid/app/Activity;Lorg/json/JSONObject;Landroid/app/AlertDialog;)V

    const-string p0, "AppearanceChoicesSave"

    invoke-direct {p1, p2, p0}, Ljava/lang/Thread;-><init>(Ljava/lang/Runnable;Ljava/lang/String;)V

    invoke-virtual {p1}, Ljava/lang/Thread;->start()V
    :try_end_64
    .catch Ljava/lang/Exception; {:try_start_2f .. :try_end_64} :catch_65

    goto :goto_69

    :catch_65
    move-exception p0

    invoke-static {p9, p0}, Lorg/efootballrevival/runtimeprobe/AppearanceChoices;->error(Landroid/app/Activity;Ljava/lang/Exception;)V

    :goto_69
    return-void
.end method

.method private static manage(Landroid/app/Activity;Ljava/lang/String;Lorg/json/JSONObject;)Ljava/lang/String;
    .registers 7
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation

    .line 4
    const-string v0, "org.efootballrevival.runtimeprobe.EmbeddedGateway"

    invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;

    move-result-object v0

    const/4 v1, 0x3

    new-array v1, v1, [Ljava/lang/Class;

    const-class v2, Landroid/content/Context;

    const/4 v3, 0x0

    aput-object v2, v1, v3

    const-class v2, Ljava/lang/String;

    const/4 v3, 0x1

    aput-object v2, v1, v3

    const/4 v3, 0x2

    aput-object v2, v1, v3

    const-string v2, "manage"

    invoke-virtual {v0, v2, v1}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    invoke-virtual {p2}, Lorg/json/JSONObject;->toString()Ljava/lang/String;

    move-result-object p2

    filled-new-array {p0, p1, p2}, [Ljava/lang/Object;

    move-result-object p0

    const/4 p1, 0x0

    invoke-virtual {v0, p1, p0}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object p0

    check-cast p0, Ljava/lang/String;

    return-object p0
.end method

.method private static names(Lorg/json/JSONArray;I)[Ljava/lang/String;
    .registers 13

    .line 10
    invoke-virtual {p0}, Lorg/json/JSONArray;->length()I

    move-result v0

    new-array v1, v0, [Ljava/lang/String;

    const/4 v2, 0x0

    move v3, v2

    :goto_8
    if-ge v3, v0, :cond_80

    invoke-virtual {p0, v3}, Lorg/json/JSONArray;->optJSONObject(I)Lorg/json/JSONObject;

    move-result-object v4

    const-string v5, "cards"

    invoke-virtual {v4, v5}, Lorg/json/JSONObject;->optJSONArray(Ljava/lang/String;)Lorg/json/JSONArray;

    move-result-object v5

    if-nez v5, :cond_18

    const/4 v5, 0x0

    goto :goto_1c

    :cond_18
    invoke-virtual {v5, v2}, Lorg/json/JSONArray;->optJSONObject(I)Lorg/json/JSONObject;

    move-result-object v5

    :goto_1c
    new-instance v6, Ljava/lang/StringBuilder;

    invoke-direct {v6}, Ljava/lang/StringBuilder;-><init>()V

    sget-object v7, Ljava/util/Locale;->US:Ljava/util/Locale;

    const-string v8, "id"

    invoke-virtual {v4, v8}, Lorg/json/JSONObject;->optInt(Ljava/lang/String;)I

    move-result v9

    invoke-static {v9}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v9

    filled-new-array {v9}, [Ljava/lang/Object;

    move-result-object v9

    const-string v10, "%04d"

    invoke-static {v7, v10, v9}, Ljava/lang/String;->format(Ljava/util/Locale;Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/String;

    move-result-object v7

    invoke-virtual {v6, v7}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v6

    invoke-virtual {v4, v8}, Lorg/json/JSONObject;->optInt(Ljava/lang/String;)I

    move-result v4

    const-string v7, ""

    if-ne v4, p1, :cond_46

    const-string v4, " \u00b7 Current"

    goto :goto_47

    :cond_46
    move-object v4, v7

    :goto_47
    invoke-virtual {v6, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v4

    if-nez v5, :cond_4e

    goto :goto_73

    :cond_4e
    new-instance v6, Ljava/lang/StringBuilder;

    invoke-direct {v6}, Ljava/lang/StringBuilder;-><init>()V

    const-string v7, " \u00b7 "

    invoke-virtual {v6, v7}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v6

    const-string v9, "name"

    invoke-virtual {v5, v9}, Lorg/json/JSONObject;->optString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v9

    invoke-virtual {v6, v9}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v6

    invoke-virtual {v6, v7}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v6

    invoke-virtual {v5, v8}, Lorg/json/JSONObject;->optString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v5

    invoke-virtual {v6, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    invoke-virtual {v5}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v7

    :goto_73
    invoke-virtual {v4, v7}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v4

    invoke-virtual {v4}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v4

    aput-object v4, v1, v3

    add-int/lit8 v3, v3, 0x1

    goto :goto_8

    :cond_80
    return-object v1
.end method

.method private static position([II)I
    .registers 5

    .line 11
    const/4 v0, 0x0

    move v1, v0

    :goto_2
    array-length v2, p0

    if-ge v1, v2, :cond_d

    aget v2, p0, v1

    if-ne v2, p1, :cond_a

    return v1

    :cond_a
    add-int/lit8 v1, v1, 0x1

    goto :goto_2

    :cond_d
    return v0
.end method

.method private static select(Landroid/app/Activity;Landroid/widget/LinearLayout;Ljava/lang/String;[Ljava/lang/String;I)Landroid/widget/Spinner;
    .registers 8

    .line 8
    new-instance v0, Landroid/widget/TextView;

    invoke-direct {v0, p0}, Landroid/widget/TextView;-><init>(Landroid/content/Context;)V

    invoke-virtual {v0, p2}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    const p2, -0x1b1001

    invoke-virtual {v0, p2}, Landroid/widget/TextView;->setTextColor(I)V

    const/16 p2, 0x10

    const/16 v1, 0x8

    const/4 v2, 0x0

    invoke-virtual {v0, v2, p2, v2, v1}, Landroid/widget/TextView;->setPadding(IIII)V

    invoke-virtual {p1, v0}, Landroid/widget/LinearLayout;->addView(Landroid/view/View;)V

    new-instance p2, Landroid/widget/Spinner;

    invoke-direct {p2, p0}, Landroid/widget/Spinner;-><init>(Landroid/content/Context;)V

    new-instance v0, Landroid/widget/ArrayAdapter;

    const v1, 0x1090008

    invoke-direct {v0, p0, v1, p3}, Landroid/widget/ArrayAdapter;-><init>(Landroid/content/Context;I[Ljava/lang/Object;)V

    const p0, 0x1090009

    invoke-virtual {v0, p0}, Landroid/widget/ArrayAdapter;->setDropDownViewResource(I)V

    invoke-virtual {p2, v0}, Landroid/widget/Spinner;->setAdapter(Landroid/widget/SpinnerAdapter;)V

    invoke-static {v2, p4}, Ljava/lang/Math;->max(II)I

    move-result p0

    invoke-virtual {p2, p0}, Landroid/widget/Spinner;->setSelection(I)V

    new-instance p0, Landroid/widget/LinearLayout$LayoutParams;

    const/4 p3, -0x1

    const/4 p4, -0x2

    invoke-direct {p0, p3, p4}, Landroid/widget/LinearLayout$LayoutParams;-><init>(II)V

    invoke-virtual {p1, p2, p0}, Landroid/widget/LinearLayout;->addView(Landroid/view/View;Landroid/view/ViewGroup$LayoutParams;)V

    return-object p2
.end method
