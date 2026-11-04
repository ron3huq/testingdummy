.class public final Lorg/efootballrevival/runtimeprobe/RuntimeDiagnostics;
.super Ljava/lang/Object;
.source "RuntimeDiagnostics.java"


# static fields
.field private static final NAMES:[Ljava/lang/String;

.field private static final TAG:Ljava/lang/String; = "ui71-runtime-diagnostics"


# direct methods
.method static constructor <clinit>()V
    .registers 17

    .line 5
    const-string v15, "noodle-advertise-error.txt"

    const-string v16, "ui71-gateway-error.txt"

    const-string v0, "full3-gate-transport.json"

    const-string v1, "ui718-live-runtime-status.json"

    const-string v2, "resource-presence-status.json"

    const-string v3, "http-resource-status.json"

    const-string v4, "ui716-photo-status.json"

    const-string v5, "ui717-live-update-status.json"

    const-string v6, "ui717-pak-repair-status.json"

    const-string v7, "mod-last-error.json"

    const-string v8, "hook-arena-status.json"

    const-string v9, "ui71-gateway-startup.json"

    const-string v10, "v25-73-bootstrap-error.txt"

    const-string v11, "mod-startup-status.json"

    const-string v12, "select-team-status.json"

    const-string v13, "noodle-hair-status.json"

    const-string v14, "myleague-73-status.json"

    filled-new-array/range {v0 .. v16}, [Ljava/lang/String;

    move-result-object v0

    sput-object v0, Lorg/efootballrevival/runtimeprobe/RuntimeDiagnostics;->NAMES:[Ljava/lang/String;

    return-void
.end method

.method public constructor <init>()V
    .registers 1

    .line 3
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static attach(Landroid/app/Activity;Landroid/view/View;)V
    .registers 5

    .line 8
    instance-of v0, p1, Landroid/widget/LinearLayout;

    if-eqz v0, :cond_52

    const-string v0, "ui71-runtime-diagnostics"

    invoke-virtual {p1, v0}, Landroid/view/View;->findViewWithTag(Ljava/lang/Object;)Landroid/view/View;

    move-result-object v1

    if-eqz v1, :cond_d

    goto :goto_52

    :cond_d
    new-instance v1, Landroid/widget/Button;

    invoke-direct {v1, p0}, Landroid/widget/Button;-><init>(Landroid/content/Context;)V

    invoke-virtual {v1, v0}, Landroid/widget/Button;->setTag(Ljava/lang/Object;)V

    const-string v0, "Runtime Diagnostics"

    invoke-virtual {v1, v0}, Landroid/widget/Button;->setText(Ljava/lang/CharSequence;)V

    const/4 v0, 0x0

    invoke-virtual {v1, v0}, Landroid/widget/Button;->setAllCaps(Z)V

    const v0, -0x1d0a01

    invoke-virtual {v1, v0}, Landroid/widget/Button;->setTextColor(I)V

    const v0, -0xe6cab4

    invoke-virtual {v1, v0}, Landroid/widget/Button;->setBackgroundColor(I)V

    invoke-virtual {p0}, Landroid/app/Activity;->getResources()Landroid/content/res/Resources;

    move-result-object v0

    invoke-virtual {v0}, Landroid/content/res/Resources;->getDisplayMetrics()Landroid/util/DisplayMetrics;

    move-result-object v0

    iget v0, v0, Landroid/util/DisplayMetrics;->density:F

    const/high16 v2, 0x42400000    # 48.0f

    mul-float/2addr v0, v2

    invoke-static {v0}, Ljava/lang/Math;->round(F)I

    move-result v0

    invoke-virtual {v1, v0}, Landroid/widget/Button;->setMinHeight(I)V

    new-instance v0, Lorg/efootballrevival/runtimeprobe/RuntimeDiagnostics$$ExternalSyntheticLambda3;

    invoke-direct {v0, v1, p0}, Lorg/efootballrevival/runtimeprobe/RuntimeDiagnostics$$ExternalSyntheticLambda3;-><init>(Landroid/widget/Button;Landroid/app/Activity;)V

    invoke-virtual {v1, v0}, Landroid/widget/Button;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    check-cast p1, Landroid/widget/LinearLayout;

    new-instance p0, Landroid/widget/LinearLayout$LayoutParams;

    const/4 v0, -0x1

    const/4 v2, -0x2

    invoke-direct {p0, v0, v2}, Landroid/widget/LinearLayout$LayoutParams;-><init>(II)V

    invoke-virtual {p1, v1, p0}, Landroid/widget/LinearLayout;->addView(Landroid/view/View;Landroid/view/ViewGroup$LayoutParams;)V

    :cond_52
    :goto_52
    return-void
.end method

.method private static collect(Landroid/content/Context;)Ljava/lang/String;
    .registers 10

    .line 7
    const/4 v0, 0x1

    const/4 v1, 0x0

    :try_start_2
    const-string v2, "org.efootballrevival.runtimeprobe.EmbeddedGateway"

    invoke-static {v2}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;

    move-result-object v2

    const-string v3, "manage"

    const/4 v4, 0x3

    new-array v5, v4, [Ljava/lang/Class;

    const-class v6, Landroid/content/Context;

    aput-object v6, v5, v1

    const-class v6, Ljava/lang/String;

    aput-object v6, v5, v0

    const-class v6, Ljava/lang/String;

    const/4 v7, 0x2

    aput-object v6, v5, v7

    invoke-virtual {v2, v3, v5}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v2

    new-array v3, v4, [Ljava/lang/Object;

    aput-object p0, v3, v1

    const-string v4, "ui718_runtime_snapshot"

    aput-object v4, v3, v0

    const-string v4, "{}"

    aput-object v4, v3, v7

    const/4 v4, 0x0

    invoke-virtual {v2, v4, v3}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;
    :try_end_2e
    .catch Ljava/lang/Exception; {:try_start_2 .. :try_end_2e} :catch_2f

    goto :goto_30

    :catch_2f
    move-exception v2

    :goto_30
    new-instance v2, Ljava/io/File;

    invoke-virtual {p0}, Landroid/content/Context;->getFilesDir()Ljava/io/File;

    move-result-object v3

    const-string v4, "embedded-gateway/work/tools"

    invoke-direct {v2, v3, v4}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V

    new-instance v3, Ljava/lang/StringBuilder;

    const-string v4, "V19.1 FULL-8 RC5 HF1 runtime diagnostics\nNo save or player records included.\n"

    invoke-direct {v3, v4}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    const-string v4, "\n--- ui718-client-resource-probe ---\n"

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v4

    invoke-virtual {p0}, Landroid/content/Context;->getFilesDir()Ljava/io/File;

    move-result-object v5

    invoke-static {v5}, Lorg/efootballrevival/runtimeprobe/LiveUpdateProbe;->inspect(Ljava/io/File;)Ljava/lang/String;

    move-result-object v5

    invoke-virtual {p0}, Landroid/content/Context;->getFilesDir()Ljava/io/File;

    move-result-object v6

    invoke-static {v5, v6}, Lorg/efootballrevival/runtimeprobe/CpkCache;->decorate(Ljava/lang/String;Ljava/io/File;)Ljava/lang/String;

    move-result-object v5

    invoke-virtual {v4, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v4

    const-string v5, "\n"

    invoke-virtual {v4, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v4, "\n--- ui719-process-exits ---\n"

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v4

    invoke-static {p0}, Lorg/efootballrevival/runtimeprobe/ExitDiagnostics;->read(Landroid/content/Context;)Ljava/lang/String;

    move-result-object p0

    invoke-virtual {v4, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p0

    invoke-virtual {p0, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    sget-object p0, Lorg/efootballrevival/runtimeprobe/RuntimeDiagnostics;->NAMES:[Ljava/lang/String;

    array-length v4, p0

    move v5, v1

    :goto_76
    if-ge v1, v4, :cond_c0

    aget-object v6, p0, v1

    new-instance v7, Ljava/io/File;

    invoke-direct {v7, v2, v6}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V

    invoke-virtual {v7}, Ljava/io/File;->isFile()Z

    move-result v8

    if-nez v8, :cond_86

    goto :goto_bd

    :cond_86
    const-string v5, "\n--- "

    invoke-virtual {v3, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    const-string v6, " ---\n"

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    :try_start_95
    invoke-static {v7}, Lorg/efootballrevival/runtimeprobe/RuntimeDiagnostics;->read(Ljava/io/File;)Ljava/lang/String;

    move-result-object v5

    invoke-virtual {v3, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    :try_end_9c
    .catch Ljava/lang/Exception; {:try_start_95 .. :try_end_9c} :catch_9d

    goto :goto_b7

    :catch_9d
    move-exception v5

    invoke-virtual {v5}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v6

    invoke-virtual {v6}, Ljava/lang/Class;->getSimpleName()Ljava/lang/String;

    move-result-object v6

    invoke-virtual {v3, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v6

    const-string v7, ": "

    invoke-virtual {v6, v7}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v6

    invoke-virtual {v5}, Ljava/lang/Exception;->getMessage()Ljava/lang/String;

    move-result-object v5

    invoke-virtual {v6, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    :goto_b7
    const/16 v5, 0xa

    invoke-virtual {v3, v5}, Ljava/lang/StringBuilder;->append(C)Ljava/lang/StringBuilder;

    move v5, v0

    :goto_bd
    add-int/lit8 v1, v1, 0x1

    goto :goto_76

    :cond_c0
    if-nez v5, :cond_c7

    const-string p0, "\nNo diagnostic files yet. Try Enter Game once, then reopen this panel.\n"

    invoke-virtual {v3, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    :cond_c7
    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    return-object p0
.end method

.method static synthetic lambda$attach$0(Landroid/widget/Button;Landroid/app/Activity;Ljava/lang/String;)V
    .registers 4

    .line 8
    const/4 v0, 0x1

    invoke-virtual {p0, v0}, Landroid/widget/Button;->setEnabled(Z)V

    invoke-virtual {p1}, Landroid/app/Activity;->isFinishing()Z

    move-result p0

    if-nez p0, :cond_d

    invoke-static {p1, p2}, Lorg/efootballrevival/runtimeprobe/RuntimeDiagnostics;->show(Landroid/app/Activity;Ljava/lang/String;)V

    :cond_d
    return-void
.end method

.method static synthetic lambda$attach$1(Landroid/app/Activity;Landroid/widget/Button;)V
    .registers 4

    .line 8
    invoke-static {p0}, Lorg/efootballrevival/runtimeprobe/RuntimeDiagnostics;->collect(Landroid/content/Context;)Ljava/lang/String;

    move-result-object v0

    new-instance v1, Lorg/efootballrevival/runtimeprobe/RuntimeDiagnostics$$ExternalSyntheticLambda1;

    invoke-direct {v1, p1, p0, v0}, Lorg/efootballrevival/runtimeprobe/RuntimeDiagnostics$$ExternalSyntheticLambda1;-><init>(Landroid/widget/Button;Landroid/app/Activity;Ljava/lang/String;)V

    invoke-virtual {p0, v1}, Landroid/app/Activity;->runOnUiThread(Ljava/lang/Runnable;)V

    return-void
.end method

.method static synthetic lambda$attach$2(Landroid/widget/Button;Landroid/app/Activity;Landroid/view/View;)V
    .registers 4

    .line 8
    const/4 p2, 0x0

    invoke-virtual {p0, p2}, Landroid/widget/Button;->setEnabled(Z)V

    new-instance p2, Ljava/lang/Thread;

    new-instance v0, Lorg/efootballrevival/runtimeprobe/RuntimeDiagnostics$$ExternalSyntheticLambda0;

    invoke-direct {v0, p1, p0}, Lorg/efootballrevival/runtimeprobe/RuntimeDiagnostics$$ExternalSyntheticLambda0;-><init>(Landroid/app/Activity;Landroid/widget/Button;)V

    const-string p0, "ReadModDiagnostics"

    invoke-direct {p2, v0, p0}, Ljava/lang/Thread;-><init>(Ljava/lang/Runnable;Ljava/lang/String;)V

    invoke-virtual {p2}, Ljava/lang/Thread;->start()V

    return-void
.end method

.method static synthetic lambda$show$3(Landroid/app/Activity;Ljava/lang/String;Landroid/content/DialogInterface;I)V
    .registers 4

    .line 9
    const-string p2, "clipboard"

    invoke-virtual {p0, p2}, Landroid/app/Activity;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    move-result-object p2

    check-cast p2, Landroid/content/ClipboardManager;

    if-eqz p2, :cond_13

    const-string p3, "73 V19.1 FULL-8 RC5 HF1 diagnostics"

    invoke-static {p3, p1}, Landroid/content/ClipData;->newPlainText(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Landroid/content/ClipData;

    move-result-object p1

    invoke-virtual {p2, p1}, Landroid/content/ClipboardManager;->setPrimaryClip(Landroid/content/ClipData;)V

    :cond_13
    const-string p1, "Diagnostics copied"

    const/4 p2, 0x0

    invoke-static {p0, p1, p2}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;

    move-result-object p0

    invoke-virtual {p0}, Landroid/widget/Toast;->show()V

    return-void
.end method

.method private static read(Ljava/io/File;)Ljava/lang/String;
    .registers 7
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation

    .line 6
    new-instance v0, Ljava/io/FileInputStream;

    invoke-direct {v0, p0}, Ljava/io/FileInputStream;-><init>(Ljava/io/File;)V

    :try_start_5
    new-instance p0, Ljava/io/ByteArrayOutputStream;

    invoke-direct {p0}, Ljava/io/ByteArrayOutputStream;-><init>()V
    :try_end_a
    .catchall {:try_start_5 .. :try_end_a} :catchall_56

    const/16 v1, 0x800

    :try_start_c
    new-array v2, v1, [B

    const/16 v3, 0x2710

    :goto_10
    if-lez v3, :cond_22

    invoke-static {v1, v3}, Ljava/lang/Math;->min(II)I

    move-result v4

    const/4 v5, 0x0

    invoke-virtual {v0, v2, v5, v4}, Ljava/io/InputStream;->read([BII)I

    move-result v4

    if-lez v4, :cond_22

    invoke-virtual {p0, v2, v5, v4}, Ljava/io/ByteArrayOutputStream;->write([BII)V

    sub-int/2addr v3, v4

    goto :goto_10

    :cond_22
    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    new-instance v2, Ljava/lang/String;

    invoke-virtual {p0}, Ljava/io/ByteArrayOutputStream;->toByteArray()[B

    move-result-object v4

    const-string v5, "UTF-8"

    invoke-direct {v2, v4, v5}, Ljava/lang/String;-><init>([BLjava/lang/String;)V

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    if-nez v3, :cond_3b

    const-string v2, "\n[truncated]"

    goto :goto_3d

    :cond_3b
    const-string v2, ""

    :goto_3d
    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1
    :try_end_45
    .catchall {:try_start_c .. :try_end_45} :catchall_4c

    :try_start_45
    invoke-virtual {p0}, Ljava/io/ByteArrayOutputStream;->close()V
    :try_end_48
    .catchall {:try_start_45 .. :try_end_48} :catchall_56

    invoke-virtual {v0}, Ljava/io/InputStream;->close()V

    return-object v1

    :catchall_4c
    move-exception v1

    :try_start_4d
    invoke-virtual {p0}, Ljava/io/ByteArrayOutputStream;->close()V
    :try_end_50
    .catchall {:try_start_4d .. :try_end_50} :catchall_51

    goto :goto_55

    :catchall_51
    move-exception p0

    :try_start_52
    invoke-virtual {v1, p0}, Ljava/lang/Throwable;->addSuppressed(Ljava/lang/Throwable;)V

    :goto_55
    throw v1
    :try_end_56
    .catchall {:try_start_52 .. :try_end_56} :catchall_56

    :catchall_56
    move-exception p0

    :try_start_57
    invoke-virtual {v0}, Ljava/io/InputStream;->close()V
    :try_end_5a
    .catchall {:try_start_57 .. :try_end_5a} :catchall_5b

    goto :goto_5f

    :catchall_5b
    move-exception v0

    invoke-virtual {p0, v0}, Ljava/lang/Throwable;->addSuppressed(Ljava/lang/Throwable;)V

    :goto_5f
    throw p0
.end method

.method private static show(Landroid/app/Activity;Ljava/lang/String;)V
    .registers 6

    .line 9
    new-instance v0, Landroid/widget/ScrollView;

    invoke-direct {v0, p0}, Landroid/widget/ScrollView;-><init>(Landroid/content/Context;)V

    new-instance v1, Landroid/widget/TextView;

    invoke-direct {v1, p0}, Landroid/widget/TextView;-><init>(Landroid/content/Context;)V

    invoke-virtual {p0}, Landroid/app/Activity;->getResources()Landroid/content/res/Resources;

    move-result-object v2

    invoke-virtual {v2}, Landroid/content/res/Resources;->getDisplayMetrics()Landroid/util/DisplayMetrics;

    move-result-object v2

    iget v2, v2, Landroid/util/DisplayMetrics;->density:F

    const/high16 v3, 0x41800000    # 16.0f

    mul-float/2addr v2, v3

    invoke-static {v2}, Ljava/lang/Math;->round(F)I

    move-result v2

    invoke-virtual {v1, v2, v2, v2, v2}, Landroid/widget/TextView;->setPadding(IIII)V

    const/high16 v2, 0x41400000    # 12.0f

    invoke-virtual {v1, v2}, Landroid/widget/TextView;->setTextSize(F)V

    const/4 v2, 0x1

    invoke-virtual {v1, v2}, Landroid/widget/TextView;->setTextIsSelectable(Z)V

    invoke-virtual {v1, p1}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    invoke-virtual {v0, v1}, Landroid/widget/ScrollView;->addView(Landroid/view/View;)V

    new-instance v1, Landroid/app/AlertDialog$Builder;

    invoke-direct {v1, p0}, Landroid/app/AlertDialog$Builder;-><init>(Landroid/content/Context;)V

    const-string v2, "Runtime Diagnostics"

    invoke-virtual {v1, v2}, Landroid/app/AlertDialog$Builder;->setTitle(Ljava/lang/CharSequence;)Landroid/app/AlertDialog$Builder;

    move-result-object v1

    invoke-virtual {v1, v0}, Landroid/app/AlertDialog$Builder;->setView(Landroid/view/View;)Landroid/app/AlertDialog$Builder;

    move-result-object v0

    const-string v1, "Close"

    const/4 v2, 0x0

    invoke-virtual {v0, v1, v2}, Landroid/app/AlertDialog$Builder;->setNegativeButton(Ljava/lang/CharSequence;Landroid/content/DialogInterface$OnClickListener;)Landroid/app/AlertDialog$Builder;

    move-result-object v0

    new-instance v1, Lorg/efootballrevival/runtimeprobe/RuntimeDiagnostics$$ExternalSyntheticLambda2;

    invoke-direct {v1, p0, p1}, Lorg/efootballrevival/runtimeprobe/RuntimeDiagnostics$$ExternalSyntheticLambda2;-><init>(Landroid/app/Activity;Ljava/lang/String;)V

    const-string p1, "Copy"

    invoke-virtual {v0, p1, v1}, Landroid/app/AlertDialog$Builder;->setPositiveButton(Ljava/lang/CharSequence;Landroid/content/DialogInterface$OnClickListener;)Landroid/app/AlertDialog$Builder;

    move-result-object p1

    invoke-virtual {p1}, Landroid/app/AlertDialog$Builder;->create()Landroid/app/AlertDialog;

    move-result-object p1

    invoke-virtual {p1}, Landroid/app/AlertDialog;->show()V

    invoke-static {p0, p1}, Lorg/efootballrevival/runtimeprobe/ResponsiveUi;->fit(Landroid/app/Activity;Landroid/app/AlertDialog;)V

    return-void
.end method
