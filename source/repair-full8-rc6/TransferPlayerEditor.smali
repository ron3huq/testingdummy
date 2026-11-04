.class public final Lorg/efootballrevival/runtimeprobe/TransferPlayerEditor;
.super Ljava/lang/Object;
.source "TransferPlayerEditor.java"


# direct methods
.method public constructor <init>()V
    .registers 1

    .line 3
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method static form(Landroid/app/Activity;Lorg/json/JSONObject;Lorg/json/JSONObject;Ljava/lang/String;I)V
    .registers 27
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation

    .line 9
    move-object/from16 v7, p0

    move-object/from16 v0, p2

    move/from16 v1, p4

    invoke-static/range {p0 .. p0}, Lorg/efootballrevival/runtimeprobe/TransferEditor;->column(Landroid/app/Activity;)Landroid/widget/LinearLayout;

    move-result-object v2

    const-string v3, "The data source is shown below. Changing an ability exempts only this player in this league from My League stat balancing; unedited players keep balancing. Other abilities keep their displayed values. Save before Enter Game, then reopen the app. Blank fields keep the current value."

    invoke-static {v7, v2, v3}, Lorg/efootballrevival/runtimeprobe/TransferEditor;->text(Landroid/app/Activity;Landroid/widget/LinearLayout;Ljava/lang/String;)Landroid/widget/TextView;

    const-string v3, "data_source_label"

    invoke-virtual {v0, v3}, Lorg/json/JSONObject;->optString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v3

    invoke-static {v7, v2, v3}, Lorg/efootballrevival/runtimeprobe/TransferEditor;->text(Landroid/app/Activity;Landroid/widget/LinearLayout;Ljava/lang/String;)Landroid/widget/TextView;

    const-string v3, "values"

    invoke-virtual {v0, v3}, Lorg/json/JSONObject;->getJSONObject(Ljava/lang/String;)Lorg/json/JSONObject;

    move-result-object v3

    new-instance v4, Ljava/util/LinkedHashMap;

    invoke-direct {v4}, Ljava/util/LinkedHashMap;-><init>()V

    const/16 v5, 0xa

    new-array v6, v5, [Landroid/widget/Spinner;

    const/4 v8, 0x2

    new-array v9, v8, [Landroid/widget/Spinner;

    .line 10
    const-string v10, ""

    if-nez v1, :cond_78

    const-string v12, "fields"

    invoke-virtual {v0, v12}, Lorg/json/JSONObject;->getJSONArray(Ljava/lang/String;)Lorg/json/JSONArray;

    move-result-object v12

    const-string v13, "parameters"

    invoke-virtual {v3, v13}, Lorg/json/JSONObject;->getJSONObject(Ljava/lang/String;)Lorg/json/JSONObject;

    move-result-object v13

    const/4 v14, 0x0

    :goto_32
    invoke-virtual {v12}, Lorg/json/JSONArray;->length()I

    move-result v15

    if-ge v14, v15, :cond_78

    invoke-virtual {v12, v14}, Lorg/json/JSONArray;->getJSONObject(I)Lorg/json/JSONObject;

    move-result-object v15

    const-string v11, "index"

    invoke-virtual {v15, v11}, Lorg/json/JSONObject;->getInt(Ljava/lang/String;)I

    move-result v11

    invoke-static {v11}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    move-result-object v11

    new-instance v5, Ljava/lang/StringBuilder;

    invoke-direct {v5}, Ljava/lang/StringBuilder;-><init>()V

    const-string v8, "name"

    invoke-virtual {v15, v8}, Lorg/json/JSONObject;->getString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v8

    invoke-virtual {v5, v8}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    const-string v8, " \u00b7 0\u2013127"

    invoke-virtual {v5, v8}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    invoke-virtual {v5}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v5

    invoke-virtual {v13, v11}, Lorg/json/JSONObject;->has(Ljava/lang/String;)Z

    move-result v8

    if-eqz v8, :cond_6a

    invoke-virtual {v13, v11}, Lorg/json/JSONObject;->getString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v8

    goto :goto_6b

    :cond_6a
    move-object v8, v10

    :goto_6b
    invoke-static {v7, v2, v5, v8}, Lorg/efootballrevival/runtimeprobe/TransferPlayerEditor;->number(Landroid/app/Activity;Landroid/widget/LinearLayout;Ljava/lang/String;Ljava/lang/String;)Landroid/widget/EditText;

    move-result-object v5

    invoke-interface {v4, v11, v5}, Ljava/util/Map;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    add-int/lit8 v14, v14, 0x1

    const/16 v5, 0xa

    const/4 v8, 0x2

    goto :goto_32

    .line 11
    :cond_78
    const/4 v5, 0x1

    if-ne v1, v5, :cond_d9

    const-string v8, "celebrations"

    invoke-virtual {v3, v8}, Lorg/json/JSONObject;->getJSONObject(Ljava/lang/String;)Lorg/json/JSONObject;

    move-result-object v8

    const-string v11, "celebration_choices"

    invoke-virtual {v0, v11}, Lorg/json/JSONObject;->getJSONObject(Ljava/lang/String;)Lorg/json/JSONObject;

    move-result-object v11

    const-string v12, "60"

    const-string v13, "59"

    filled-new-array {v13, v12}, [Ljava/lang/String;

    move-result-object v12

    const/4 v14, 0x0

    :goto_90
    const/4 v15, 0x2

    if-ge v14, v15, :cond_d9

    aget-object v15, v12, v14

    invoke-virtual {v15, v13}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v16

    if-eqz v16, :cond_9e

    const-string v16, "Goal celebration ID"

    goto :goto_a0

    :cond_9e
    const-string v16, "Memorial celebration ID"

    :goto_a0
    move-object/from16 v5, v16

    invoke-virtual {v8, v15}, Lorg/json/JSONObject;->has(Ljava/lang/String;)Z

    move-result v16

    if-eqz v16, :cond_b3

    invoke-virtual {v8, v15}, Lorg/json/JSONObject;->getString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v16

    move-object/from16 v21, v16

    move-object/from16 v16, v8

    move-object/from16 v8, v21

    goto :goto_b6

    :cond_b3
    move-object/from16 v16, v8

    move-object v8, v10

    :goto_b6
    invoke-static {v7, v2, v5, v8}, Lorg/efootballrevival/runtimeprobe/TransferPlayerEditor;->number(Landroid/app/Activity;Landroid/widget/LinearLayout;Ljava/lang/String;Ljava/lang/String;)Landroid/widget/EditText;

    move-result-object v5

    invoke-interface {v4, v15, v5}, Ljava/util/Map;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    invoke-virtual {v11, v15}, Lorg/json/JSONObject;->getJSONArray(Ljava/lang/String;)Lorg/json/JSONArray;

    move-result-object v8

    const-string v15, "Choose existing celebration"

    invoke-static {v7, v2, v15}, Lorg/efootballrevival/runtimeprobe/TransferEditor;->button(Landroid/app/Activity;Landroid/widget/LinearLayout;Ljava/lang/String;)Landroid/widget/Button;

    move-result-object v15

    move-object/from16 v17, v10

    new-instance v10, Lorg/efootballrevival/runtimeprobe/TransferPlayerEditor$$ExternalSyntheticLambda0;

    invoke-direct {v10, v8, v7, v5}, Lorg/efootballrevival/runtimeprobe/TransferPlayerEditor$$ExternalSyntheticLambda0;-><init>(Lorg/json/JSONArray;Landroid/app/Activity;Landroid/widget/EditText;)V

    invoke-virtual {v15, v10}, Landroid/widget/Button;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    add-int/lit8 v14, v14, 0x1

    move-object/from16 v8, v16

    move-object/from16 v10, v17

    const/4 v5, 0x1

    goto :goto_90

    .line 12
    :cond_d9
    const-string v5, " \u00b7 "

    const/4 v8, 0x0

    const/4 v10, 0x2

    if-ne v1, v10, :cond_1f2

    const-string v11, "accessories"

    invoke-virtual {v3, v11}, Lorg/json/JSONObject;->getJSONObject(Ljava/lang/String;)Lorg/json/JSONObject;

    move-result-object v11

    const-string v12, "accessory_choices"

    invoke-virtual {v0, v12}, Lorg/json/JSONObject;->getJSONObject(Ljava/lang/String;)Lorg/json/JSONObject;

    move-result-object v0

    const/16 v12, 0xa

    new-array v13, v12, [I

    fill-array-data v13, :array_264

    filled-new-array {v8}, [Landroid/widget/LinearLayout;

    move-result-object v14

    const/4 v15, 0x0

    :goto_f7
    const-string v10, "Original"

    if-ge v15, v12, :cond_1be

    aget v12, v13, v15

    invoke-static/range {p0 .. p0}, Lorg/efootballrevival/runtimeprobe/TransferEditor;->column(Landroid/app/Activity;)Landroid/widget/LinearLayout;

    move-result-object v8

    move-object/from16 v17, v13

    new-instance v13, Ljava/lang/StringBuilder;

    invoke-direct {v13}, Ljava/lang/StringBuilder;-><init>()V

    move-object/from16 v18, v4

    invoke-static {v12}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    move-result-object v4

    invoke-virtual {v0, v4}, Lorg/json/JSONObject;->optString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v4

    invoke-virtual {v13, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v4

    invoke-virtual {v4, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v4

    const-string v13, "Off"

    const-string v1, "On"

    filled-new-array {v10, v13, v1}, [Ljava/lang/String;

    move-result-object v19

    move-object/from16 v20, v5

    invoke-static {v12}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    move-result-object v5

    invoke-virtual {v11, v5}, Lorg/json/JSONObject;->optInt(Ljava/lang/String;)I

    move-result v5

    aget-object v5, v19, v5

    invoke-virtual {v4, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v4

    invoke-virtual {v4}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v4

    invoke-static {v7, v2, v4}, Lorg/efootballrevival/runtimeprobe/TransferEditor;->button(Landroid/app/Activity;Landroid/widget/LinearLayout;Ljava/lang/String;)Landroid/widget/Button;

    move-result-object v4

    invoke-virtual {v2, v8}, Landroid/widget/LinearLayout;->addView(Landroid/view/View;)V

    const/16 v5, 0x8

    invoke-virtual {v8, v5}, Landroid/widget/LinearLayout;->setVisibility(I)V

    new-instance v5, Lorg/efootballrevival/runtimeprobe/TransferPlayerEditor$$ExternalSyntheticLambda1;

    invoke-direct {v5, v8, v14}, Lorg/efootballrevival/runtimeprobe/TransferPlayerEditor$$ExternalSyntheticLambda1;-><init>(Landroid/widget/LinearLayout;[Landroid/widget/LinearLayout;)V

    invoke-virtual {v4, v5}, Landroid/widget/Button;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    filled-new-array {v10, v13, v1}, [Ljava/lang/String;

    move-result-object v1

    invoke-static {v12}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    move-result-object v5

    invoke-virtual {v11, v5}, Lorg/json/JSONObject;->optInt(Ljava/lang/String;)I

    move-result v5

    const-string v10, "State"

    invoke-static {v7, v8, v10, v1, v5}, Lorg/efootballrevival/runtimeprobe/TransferPlayerEditor;->select(Landroid/app/Activity;Landroid/widget/LinearLayout;Ljava/lang/String;[Ljava/lang/String;I)Landroid/widget/Spinner;

    move-result-object v1

    aput-object v1, v6, v12

    const/4 v1, 0x4

    if-eq v12, v1, :cond_169

    const/4 v5, 0x5

    if-ne v12, v5, :cond_165

    goto :goto_169

    :cond_165
    move-object/from16 v19, v11

    const/4 v11, 0x0

    goto :goto_19a

    :cond_169
    :goto_169
    add-int/lit8 v5, v12, -0x4

    const-string v10, "Black wide wrap"

    const-string v13, "Yellow wrap"

    const-string v1, "Use native wrist tape"

    move-object/from16 v19, v11

    const-string v11, "White wrap"

    filled-new-array {v1, v11, v10, v13}, [Ljava/lang/String;

    move-result-object v1

    const/4 v10, 0x4

    if-ne v12, v10, :cond_17f

    const-string v10, "bandage_left"

    goto :goto_181

    :cond_17f
    const-string v10, "bandage_right"

    :goto_181
    const/4 v11, 0x0

    invoke-virtual {v3, v10, v11}, Lorg/json/JSONObject;->optInt(Ljava/lang/String;I)I

    move-result v10

    const-string v13, "Pack bandage"

    invoke-static {v7, v8, v13, v1, v10}, Lorg/efootballrevival/runtimeprobe/TransferPlayerEditor;->select(Landroid/app/Activity;Landroid/widget/LinearLayout;Ljava/lang/String;[Ljava/lang/String;I)Landroid/widget/Spinner;

    move-result-object v1

    aput-object v1, v9, v5

    aget-object v1, v6, v12

    aget-object v5, v9, v5

    new-instance v8, Lorg/efootballrevival/runtimeprobe/TransferPlayerEditor$1;

    invoke-direct {v8, v1, v4, v0, v12}, Lorg/efootballrevival/runtimeprobe/TransferPlayerEditor$1;-><init>(Landroid/widget/Spinner;Landroid/widget/Button;Lorg/json/JSONObject;I)V

    invoke-virtual {v5, v8}, Landroid/widget/Spinner;->setOnItemSelectedListener(Landroid/widget/AdapterView$OnItemSelectedListener;)V

    :goto_19a
    aget-object v1, v6, v12

    invoke-static {v12}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    move-result-object v5

    invoke-virtual {v0, v5}, Lorg/json/JSONObject;->optString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v5

    new-instance v8, Lorg/efootballrevival/runtimeprobe/TransferPlayerEditor$2;

    invoke-direct {v8, v4, v5, v12, v9}, Lorg/efootballrevival/runtimeprobe/TransferPlayerEditor$2;-><init>(Landroid/widget/Button;Ljava/lang/String;I[Landroid/widget/Spinner;)V

    invoke-virtual {v1, v8}, Landroid/widget/Spinner;->setOnItemSelectedListener(Landroid/widget/AdapterView$OnItemSelectedListener;)V

    add-int/lit8 v15, v15, 0x1

    move/from16 v1, p4

    move-object/from16 v13, v17

    move-object/from16 v4, v18

    move-object/from16 v11, v19

    move-object/from16 v5, v20

    const/4 v8, 0x0

    const/4 v10, 0x2

    const/16 v12, 0xa

    goto/16 :goto_f7

    :cond_1be
    move-object/from16 v18, v4

    move-object/from16 v20, v5

    const/4 v11, 0x0

    const-string v0, "Short"

    const-string v1, "Long"

    filled-new-array {v10, v0, v1}, [Ljava/lang/String;

    move-result-object v0

    const-string v1, "short"

    const-string v4, "sleeve"

    invoke-virtual {v3, v4}, Lorg/json/JSONObject;->optString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v5

    invoke-virtual {v1, v5}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-eqz v1, :cond_1db

    const/4 v8, 0x1

    goto :goto_1ea

    :cond_1db
    const-string v1, "long"

    invoke-virtual {v3, v4}, Lorg/json/JSONObject;->optString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v3

    invoke-virtual {v1, v3}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-eqz v1, :cond_1e9

    const/4 v8, 0x2

    goto :goto_1ea

    :cond_1e9
    move v8, v11

    :goto_1ea
    const-string v1, "Sleeves"

    invoke-static {v7, v2, v1, v0, v8}, Lorg/efootballrevival/runtimeprobe/TransferPlayerEditor;->select(Landroid/app/Activity;Landroid/widget/LinearLayout;Ljava/lang/String;[Ljava/lang/String;I)Landroid/widget/Spinner;

    move-result-object v0

    move-object v5, v0

    goto :goto_1f7

    :cond_1f2
    move-object/from16 v18, v4

    move-object/from16 v20, v5

    const/4 v5, 0x0

    .line 13
    :goto_1f7
    new-instance v0, Landroid/widget/ScrollView;

    invoke-direct {v0, v7}, Landroid/widget/ScrollView;-><init>(Landroid/content/Context;)V

    invoke-virtual {v0, v2}, Landroid/widget/ScrollView;->addView(Landroid/view/View;)V

    new-instance v1, Landroid/app/AlertDialog$Builder;

    invoke-direct {v1, v7}, Landroid/app/AlertDialog$Builder;-><init>(Landroid/content/Context;)V

    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V

    move-object/from16 v3, p3

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v2

    move-object/from16 v3, v20

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v2

    move/from16 v3, p4

    if-nez v3, :cond_21c

    const-string v4, "Abilities"

    goto :goto_224

    :cond_21c
    const/4 v4, 0x1

    if-ne v3, v4, :cond_222

    const-string v4, "Celebrations"

    goto :goto_224

    :cond_222
    const-string v4, "Accessories"

    :goto_224
    invoke-virtual {v2, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v2

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v2

    invoke-virtual {v1, v2}, Landroid/app/AlertDialog$Builder;->setTitle(Ljava/lang/CharSequence;)Landroid/app/AlertDialog$Builder;

    move-result-object v1

    invoke-virtual {v1, v0}, Landroid/app/AlertDialog$Builder;->setView(Landroid/view/View;)Landroid/app/AlertDialog$Builder;

    move-result-object v0

    const-string v1, "Cancel"

    const/4 v2, 0x0

    invoke-virtual {v0, v1, v2}, Landroid/app/AlertDialog$Builder;->setNegativeButton(Ljava/lang/CharSequence;Landroid/content/DialogInterface$OnClickListener;)Landroid/app/AlertDialog$Builder;

    move-result-object v0

    const-string v1, "Save"

    invoke-virtual {v0, v1, v2}, Landroid/app/AlertDialog$Builder;->setPositiveButton(Ljava/lang/CharSequence;Landroid/content/DialogInterface$OnClickListener;)Landroid/app/AlertDialog$Builder;

    move-result-object v0

    invoke-virtual {v0}, Landroid/app/AlertDialog$Builder;->create()Landroid/app/AlertDialog;

    move-result-object v8

    invoke-virtual {v8}, Landroid/app/AlertDialog;->show()V

    invoke-static {v7, v8}, Lorg/efootballrevival/runtimeprobe/ResponsiveUi;->fit(Landroid/app/Activity;Landroid/app/AlertDialog;)V

    const/4 v0, -0x1

    invoke-virtual {v8, v0}, Landroid/app/AlertDialog;->getButton(I)Landroid/widget/Button;

    move-result-object v10

    new-instance v11, Lorg/efootballrevival/runtimeprobe/TransferPlayerEditor$$ExternalSyntheticLambda2;

    move-object v0, v11

    move/from16 v1, p4

    move-object/from16 v2, v18

    move-object v3, v6

    move-object v4, v9

    move-object/from16 v6, p1

    move-object/from16 v7, p0

    invoke-direct/range {v0 .. v8}, Lorg/efootballrevival/runtimeprobe/TransferPlayerEditor$$ExternalSyntheticLambda2;-><init>(ILjava/util/Map;[Landroid/widget/Spinner;[Landroid/widget/Spinner;Landroid/widget/Spinner;Lorg/json/JSONObject;Landroid/app/Activity;Landroid/app/AlertDialog;)V

    invoke-virtual {v10, v11}, Landroid/widget/Button;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 14
    return-void

    :array_264
    .array-data 4
        0x4
        0x5
        0x0
        0x1
        0x2
        0x3
        0x6
        0x7
        0x8
        0x9
    .end array-data
.end method

.method static synthetic lambda$form$2(Landroid/widget/EditText;Lorg/json/JSONArray;Landroid/content/DialogInterface;I)V
    .registers 4

    .line 11
    invoke-virtual {p1, p3}, Lorg/json/JSONArray;->optJSONObject(I)Lorg/json/JSONObject;

    move-result-object p1

    const-string p2, "id"

    invoke-virtual {p1, p2}, Lorg/json/JSONObject;->optInt(Ljava/lang/String;)I

    move-result p1

    invoke-static {p1}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    move-result-object p1

    invoke-virtual {p0, p1}, Landroid/widget/EditText;->setText(Ljava/lang/CharSequence;)V

    return-void
.end method

.method static synthetic lambda$form$3(Lorg/json/JSONArray;Landroid/app/Activity;Landroid/widget/EditText;Landroid/view/View;)V
    .registers 11

    .line 11
    :try_start_0
    invoke-virtual {p0}, Lorg/json/JSONArray;->length()I

    move-result p3

    new-array v0, p3, [Ljava/lang/String;

    const/4 v1, 0x0

    :goto_7
    if-ge v1, p3, :cond_3d

    invoke-virtual {p0, v1}, Lorg/json/JSONArray;->getJSONObject(I)Lorg/json/JSONObject;

    move-result-object v2

    new-instance v3, Ljava/lang/StringBuilder;

    invoke-direct {v3}, Ljava/lang/StringBuilder;-><init>()V

    const-string v4, "id"

    invoke-virtual {v2, v4}, Lorg/json/JSONObject;->getInt(Ljava/lang/String;)I

    move-result v4

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v3

    const-string v4, " \u00b7 "

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    const-string v4, "name"

    const-string v5, "label"

    const-string v6, "Celebration"

    invoke-virtual {v2, v5, v6}, Lorg/json/JSONObject;->optString(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v5

    invoke-virtual {v2, v4, v5}, Lorg/json/JSONObject;->optString(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v2

    invoke-virtual {v3, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v2

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v2

    aput-object v2, v0, v1

    add-int/lit8 v1, v1, 0x1

    goto :goto_7

    :cond_3d
    new-instance p3, Landroid/app/AlertDialog$Builder;

    invoke-direct {p3, p1}, Landroid/app/AlertDialog$Builder;-><init>(Landroid/content/Context;)V

    const-string v1, "Existing celebration IDs"

    invoke-virtual {p3, v1}, Landroid/app/AlertDialog$Builder;->setTitle(Ljava/lang/CharSequence;)Landroid/app/AlertDialog$Builder;

    move-result-object p3

    new-instance v1, Lorg/efootballrevival/runtimeprobe/TransferPlayerEditor$$ExternalSyntheticLambda4;

    invoke-direct {v1, p2, p0}, Lorg/efootballrevival/runtimeprobe/TransferPlayerEditor$$ExternalSyntheticLambda4;-><init>(Landroid/widget/EditText;Lorg/json/JSONArray;)V

    invoke-virtual {p3, v0, v1}, Landroid/app/AlertDialog$Builder;->setItems([Ljava/lang/CharSequence;Landroid/content/DialogInterface$OnClickListener;)Landroid/app/AlertDialog$Builder;

    move-result-object p0

    const-string p2, "Cancel"

    const/4 p3, 0x0

    invoke-virtual {p0, p2, p3}, Landroid/app/AlertDialog$Builder;->setNegativeButton(Ljava/lang/CharSequence;Landroid/content/DialogInterface$OnClickListener;)Landroid/app/AlertDialog$Builder;

    move-result-object p0

    invoke-virtual {p0}, Landroid/app/AlertDialog$Builder;->show()Landroid/app/AlertDialog;
    :try_end_5b
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_5b} :catch_5c

    goto :goto_60

    :catch_5c
    move-exception p0

    invoke-static {p1, p0}, Lorg/efootballrevival/runtimeprobe/TransferEditor;->error(Landroid/app/Activity;Ljava/lang/Exception;)V

    :goto_60
    return-void
.end method

.method static synthetic lambda$form$4(Landroid/widget/LinearLayout;[Landroid/widget/LinearLayout;Landroid/view/View;)V
    .registers 5

    .line 12
    invoke-virtual {p0}, Landroid/widget/LinearLayout;->getVisibility()I

    move-result p2

    const/16 v0, 0x8

    const/4 v1, 0x0

    if-nez p2, :cond_10

    invoke-virtual {p0, v0}, Landroid/widget/LinearLayout;->setVisibility(I)V

    const/4 p0, 0x0

    aput-object p0, p1, v1

    goto :goto_1e

    :cond_10
    aget-object p2, p1, v1

    if-eqz p2, :cond_19

    aget-object p2, p1, v1

    invoke-virtual {p2, v0}, Landroid/widget/LinearLayout;->setVisibility(I)V

    :cond_19
    invoke-virtual {p0, v1}, Landroid/widget/LinearLayout;->setVisibility(I)V

    aput-object p0, p1, v1

    :goto_1e
    return-void
.end method

.method static synthetic lambda$form$5(Landroid/app/AlertDialog;Landroid/app/Activity;Lorg/json/JSONObject;)V
    .registers 4
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation

    .line 13
    const-string v0, "saved"

    invoke-virtual {p2, v0}, Lorg/json/JSONObject;->optBoolean(Ljava/lang/String;)Z

    move-result p2

    if-eqz p2, :cond_16

    invoke-virtual {p0}, Landroid/app/AlertDialog;->dismiss()V

    const-string p0, "Player saved. Reopen the app."

    const/4 p2, 0x1

    invoke-static {p1, p0, p2}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;

    move-result-object p0

    invoke-virtual {p0}, Landroid/widget/Toast;->show()V

    return-void

    :cond_16
    new-instance p0, Ljava/lang/Exception;

    const-string p1, "Save not confirmed"

    invoke-direct {p0, p1}, Ljava/lang/Exception;-><init>(Ljava/lang/String;)V

    throw p0
.end method

.method static synthetic lambda$form$6(ILjava/util/Map;[Landroid/widget/Spinner;[Landroid/widget/Spinner;Landroid/widget/Spinner;Lorg/json/JSONObject;Landroid/app/Activity;Landroid/app/AlertDialog;Landroid/view/View;)V
    .registers 13

    .line 13
    :try_start_0
    new-instance p8, Lorg/json/JSONObject;

    invoke-direct {p8}, Lorg/json/JSONObject;-><init>()V

    const/4 v0, 0x2

    if-ge p0, v0, :cond_52

    new-instance p2, Lorg/json/JSONObject;

    invoke-direct {p2}, Lorg/json/JSONObject;-><init>()V

    invoke-interface {p1}, Ljava/util/Map;->entrySet()Ljava/util/Set;

    move-result-object p1

    invoke-interface {p1}, Ljava/util/Set;->iterator()Ljava/util/Iterator;

    move-result-object p1

    :cond_15
    :goto_15
    invoke-interface {p1}, Ljava/util/Iterator;->hasNext()Z

    move-result p3

    if-eqz p3, :cond_47

    invoke-interface {p1}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    move-result-object p3

    check-cast p3, Ljava/util/Map$Entry;

    invoke-interface {p3}, Ljava/util/Map$Entry;->getValue()Ljava/lang/Object;

    move-result-object p4

    check-cast p4, Landroid/widget/EditText;

    invoke-virtual {p4}, Landroid/widget/EditText;->getText()Landroid/text/Editable;

    move-result-object p4

    invoke-virtual {p4}, Ljava/lang/Object;->toString()Ljava/lang/String;

    move-result-object p4

    invoke-virtual {p4}, Ljava/lang/String;->trim()Ljava/lang/String;

    move-result-object p4

    invoke-virtual {p4}, Ljava/lang/String;->isEmpty()Z

    move-result v0

    if-nez v0, :cond_15

    invoke-interface {p3}, Ljava/util/Map$Entry;->getKey()Ljava/lang/Object;

    move-result-object p3

    check-cast p3, Ljava/lang/String;

    invoke-static {p4}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    move-result p4

    invoke-virtual {p2, p3, p4}, Lorg/json/JSONObject;->put(Ljava/lang/String;I)Lorg/json/JSONObject;

    goto :goto_15

    :cond_47
    if-nez p0, :cond_4c

    const-string p0, "parameters"

    goto :goto_4e

    :cond_4c
    const-string p0, "celebrations"

    :goto_4e
    invoke-virtual {p8, p0, p2}, Lorg/json/JSONObject;->put(Ljava/lang/String;Ljava/lang/Object;)Lorg/json/JSONObject;

    goto :goto_a5

    :cond_52
    new-instance p0, Lorg/json/JSONObject;

    invoke-direct {p0}, Lorg/json/JSONObject;-><init>()V

    const/4 p1, 0x0

    move v1, p1

    :goto_59
    const/16 v2, 0xa

    if-ge v1, v2, :cond_6d

    invoke-static {v1}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    move-result-object v2

    aget-object v3, p2, v1

    invoke-virtual {v3}, Landroid/widget/Spinner;->getSelectedItemPosition()I

    move-result v3

    invoke-virtual {p0, v2, v3}, Lorg/json/JSONObject;->put(Ljava/lang/String;I)Lorg/json/JSONObject;

    add-int/lit8 v1, v1, 0x1

    goto :goto_59

    :cond_6d
    const-string p2, "bandage_left"

    aget-object v1, p3, p1

    invoke-virtual {v1}, Landroid/widget/Spinner;->getSelectedItemPosition()I

    move-result v1

    invoke-virtual {p8, p2, v1}, Lorg/json/JSONObject;->put(Ljava/lang/String;I)Lorg/json/JSONObject;

    move-result-object p2

    const-string v1, "bandage_right"

    const/4 v2, 0x1

    aget-object p3, p3, v2

    invoke-virtual {p3}, Landroid/widget/Spinner;->getSelectedItemPosition()I

    move-result p3

    invoke-virtual {p2, v1, p3}, Lorg/json/JSONObject;->put(Ljava/lang/String;I)Lorg/json/JSONObject;

    const-string p2, "accessories"

    invoke-virtual {p8, p2, p0}, Lorg/json/JSONObject;->put(Ljava/lang/String;Ljava/lang/Object;)Lorg/json/JSONObject;

    move-result-object p0

    const-string p2, "sleeve"

    const/4 p3, 0x3

    new-array p3, p3, [Ljava/lang/String;

    const-string v1, "original"

    aput-object v1, p3, p1

    const-string p1, "short"

    aput-object p1, p3, v2

    const-string p1, "long"

    aput-object p1, p3, v0

    invoke-virtual {p4}, Landroid/widget/Spinner;->getSelectedItemPosition()I

    move-result p1

    aget-object p1, p3, p1

    invoke-virtual {p0, p2, p1}, Lorg/json/JSONObject;->put(Ljava/lang/String;Ljava/lang/Object;)Lorg/json/JSONObject;

    :goto_a5
    new-instance p0, Lorg/json/JSONObject;

    invoke-virtual {p5}, Lorg/json/JSONObject;->toString()Ljava/lang/String;

    move-result-object p1

    invoke-direct {p0, p1}, Lorg/json/JSONObject;-><init>(Ljava/lang/String;)V

    const-string p1, "values"

    invoke-virtual {p0, p1, p8}, Lorg/json/JSONObject;->put(Ljava/lang/String;Ljava/lang/Object;)Lorg/json/JSONObject;

    move-result-object p0

    const/4 p1, -0x1

    invoke-virtual {p7, p1}, Landroid/app/AlertDialog;->getButton(I)Landroid/widget/Button;

    move-result-object p1

    const-string p2, "ui712_transfer_player_apply"

    new-instance p3, Lorg/efootballrevival/runtimeprobe/TransferPlayerEditor$$ExternalSyntheticLambda3;

    invoke-direct {p3, p7, p6}, Lorg/efootballrevival/runtimeprobe/TransferPlayerEditor$$ExternalSyntheticLambda3;-><init>(Landroid/app/AlertDialog;Landroid/app/Activity;)V

    invoke-static {p6, p1, p2, p0, p3}, Lorg/efootballrevival/runtimeprobe/TransferEditor;->request(Landroid/app/Activity;Landroid/widget/Button;Ljava/lang/String;Lorg/json/JSONObject;Lorg/efootballrevival/runtimeprobe/TransferEditor$Result;)V
    :try_end_c3
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_c3} :catch_c4

    goto :goto_c8

    :catch_c4
    move-exception p0

    invoke-static {p6, p0}, Lorg/efootballrevival/runtimeprobe/TransferEditor;->error(Landroid/app/Activity;Ljava/lang/Exception;)V

    :goto_c8
    return-void
.end method

.method static synthetic lambda$load$1(Landroid/app/Activity;Lorg/json/JSONObject;Ljava/lang/String;ILorg/json/JSONObject;)V
    .registers 5
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation

    .line 5
    invoke-static {p0, p1, p4, p2, p3}, Lorg/efootballrevival/runtimeprobe/TransferPlayerEditor;->form(Landroid/app/Activity;Lorg/json/JSONObject;Lorg/json/JSONObject;Ljava/lang/String;I)V

    return-void
.end method

.method static synthetic lambda$open$0(Landroid/app/Activity;Lorg/json/JSONObject;Ljava/lang/String;Ljava/lang/String;Landroid/content/DialogInterface;I)V
    .registers 6

    .line 4
    invoke-static {p0, p1, p2, p3, p5}, Lorg/efootballrevival/runtimeprobe/TransferPlayerEditor;->load(Landroid/app/Activity;Lorg/json/JSONObject;Ljava/lang/String;Ljava/lang/String;I)V

    return-void
.end method

.method static load(Landroid/app/Activity;Lorg/json/JSONObject;Ljava/lang/String;Ljava/lang/String;I)V
    .registers 6

    .line 5
    :try_start_0
    new-instance v0, Lorg/json/JSONObject;

    invoke-virtual {p1}, Lorg/json/JSONObject;->toString()Ljava/lang/String;

    move-result-object p1

    invoke-direct {v0, p1}, Lorg/json/JSONObject;-><init>(Ljava/lang/String;)V

    const-string p1, "player_id"

    invoke-virtual {v0, p1, p2}, Lorg/json/JSONObject;->put(Ljava/lang/String;Ljava/lang/Object;)Lorg/json/JSONObject;

    move-result-object p1

    const-string p2, "section"

    const/4 v0, 0x1

    if-ne p4, v0, :cond_17

    const-string v0, "celebrations"

    goto :goto_19

    :cond_17
    const-string v0, ""

    :goto_19
    invoke-virtual {p1, p2, v0}, Lorg/json/JSONObject;->put(Ljava/lang/String;Ljava/lang/Object;)Lorg/json/JSONObject;

    move-result-object p1

    const-string p2, "ui712_transfer_player_get"

    new-instance v0, Lorg/efootballrevival/runtimeprobe/TransferPlayerEditor$$ExternalSyntheticLambda5;

    invoke-direct {v0, p0, p1, p3, p4}, Lorg/efootballrevival/runtimeprobe/TransferPlayerEditor$$ExternalSyntheticLambda5;-><init>(Landroid/app/Activity;Lorg/json/JSONObject;Ljava/lang/String;I)V

    const/4 p3, 0x0

    invoke-static {p0, p3, p2, p1, v0}, Lorg/efootballrevival/runtimeprobe/TransferEditor;->request(Landroid/app/Activity;Landroid/widget/Button;Ljava/lang/String;Lorg/json/JSONObject;Lorg/efootballrevival/runtimeprobe/TransferEditor$Result;)V
    :try_end_28
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_28} :catch_29

    goto :goto_2d

    :catch_29
    move-exception p1

    invoke-static {p0, p1}, Lorg/efootballrevival/runtimeprobe/TransferEditor;->error(Landroid/app/Activity;Ljava/lang/Exception;)V

    :goto_2d
    return-void
.end method

.method static number(Landroid/app/Activity;Landroid/widget/LinearLayout;Ljava/lang/String;Ljava/lang/String;)Landroid/widget/EditText;
    .registers 4

    .line 6
    invoke-static {p0, p1, p2}, Lorg/efootballrevival/runtimeprobe/TransferEditor;->text(Landroid/app/Activity;Landroid/widget/LinearLayout;Ljava/lang/String;)Landroid/widget/TextView;

    new-instance p2, Landroid/widget/EditText;

    invoke-direct {p2, p0}, Landroid/widget/EditText;-><init>(Landroid/content/Context;)V

    const/4 p0, 0x1

    invoke-virtual {p2, p0}, Landroid/widget/EditText;->setSingleLine(Z)V

    const/4 p0, 0x2

    invoke-virtual {p2, p0}, Landroid/widget/EditText;->setInputType(I)V

    const-string p0, "Original game value"

    invoke-virtual {p2, p0}, Landroid/widget/EditText;->setHint(Ljava/lang/CharSequence;)V

    invoke-virtual {p2, p3}, Landroid/widget/EditText;->setText(Ljava/lang/CharSequence;)V

    invoke-virtual {p1, p2}, Landroid/widget/LinearLayout;->addView(Landroid/view/View;)V

    return-object p2
.end method

.method static open(Landroid/app/Activity;Lorg/json/JSONObject;Ljava/lang/String;Ljava/lang/String;)V
    .registers 4
    invoke-static {p0, p1, p2, p3}, Lorg/efootballrevival/runtimeprobe/TransferTraitsEditor;->menu(Landroid/app/Activity;Lorg/json/JSONObject;Ljava/lang/String;Ljava/lang/String;)V
    return-void
.end method

.method static select(Landroid/app/Activity;Landroid/widget/LinearLayout;Ljava/lang/String;[Ljava/lang/String;I)Landroid/widget/Spinner;
    .registers 7

    .line 7
    invoke-static {p0, p1, p2}, Lorg/efootballrevival/runtimeprobe/TransferEditor;->text(Landroid/app/Activity;Landroid/widget/LinearLayout;Ljava/lang/String;)Landroid/widget/TextView;

    new-instance p2, Landroid/widget/Spinner;

    invoke-direct {p2, p0}, Landroid/widget/Spinner;-><init>(Landroid/content/Context;)V

    new-instance v0, Landroid/widget/ArrayAdapter;

    const v1, 0x1090009

    invoke-direct {v0, p0, v1, p3}, Landroid/widget/ArrayAdapter;-><init>(Landroid/content/Context;I[Ljava/lang/Object;)V

    invoke-virtual {p2, v0}, Landroid/widget/Spinner;->setAdapter(Landroid/widget/SpinnerAdapter;)V

    array-length p0, p3

    add-int/lit8 p0, p0, -0x1

    invoke-static {p4, p0}, Ljava/lang/Math;->min(II)I

    move-result p0

    const/4 p3, 0x0

    invoke-static {p3, p0}, Ljava/lang/Math;->max(II)I

    move-result p0

    invoke-virtual {p2, p0}, Landroid/widget/Spinner;->setSelection(I)V

    invoke-virtual {p1, p2}, Landroid/widget/LinearLayout;->addView(Landroid/view/View;)V

    return-object p2
.end method
