.class public final Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;
.super Ljava/lang/Object;
.source "MlLeaguePanel.java"


# annotations
.annotation system Ldalvik/annotation/MemberClasses;
    value = {
        Lorg/efootballrevival/runtimeprobe/MlLeaguePanel$Bridge;
    }
.end annotation


# static fields
.field private static final ART_CACHE:I = 0x8

.field private static final ASSETS:Ljava/lang/String; = "ml-league/"

.field private static final FACE_CACHE:I = 0x140

.field private static final FACE_TTL_MS:J = 0xf731400L

.field private static final HOST:Ljava/lang/String; = "ml-league.local"

.field private static final LIMIT:I = 0xb71b00

.field private static final NO_FACE:[B

.field private static final PAGE_HINT_AFTER_MS:J = 0x4b0L

.field private static final PAGE_TIMEOUT_MS:J = 0x1d4c0L

.field private static final TAG:Ljava/lang/String; = "ML_LEAGUE"

.field private static active:Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;

.field private static final artVideos:Ljava/util/Map;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/Map<",
            "Ljava/lang/String;",
            "[B>;"
        }
    .end annotation
.end field

.field private static final artWhy:Ljava/util/Map;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/Map<",
            "Ljava/lang/String;",
            "Ljava/lang/String;",
            ">;"
        }
    .end annotation
.end field

.field private static final arts:Ljava/util/Map;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/Map<",
            "Ljava/lang/String;",
            "[B>;"
        }
    .end annotation
.end field

.field private static crestIndex:Ljava/util/Map;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/Map<",
            "Ljava/lang/Integer;",
            "[I>;"
        }
    .end annotation
.end field

.field private static crestPack:[B

.field private static final faces:Ljava/util/Map;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/Map<",
            "Ljava/lang/String;",
            "[B>;"
        }
    .end annotation
.end field

.field private static final leaving:Ljava/util/concurrent/atomic/AtomicBoolean;

.field private static final simulating:Ljava/util/concurrent/atomic/AtomicBoolean;


# instance fields
.field private final activity:Landroid/app/Activity;

.field private volatile closed:Z

.field private dialog:Landroid/app/Dialog;

.field private pageReady:Z

.field private pendingPostMatch:I

.field private safeLeft:I

.field private safeRight:I

.field private final starting:Ljava/util/concurrent/atomic/AtomicBoolean;

.field private web:Landroid/webkit/WebView;


# direct methods
.method static constructor <clinit>()V
    .registers 5

    .line 59
    new-instance v0, Ljava/util/concurrent/atomic/AtomicBoolean;

    const/4 v1, 0x0

    invoke-direct {v0, v1}, Ljava/util/concurrent/atomic/AtomicBoolean;-><init>(Z)V

    sput-object v0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->simulating:Ljava/util/concurrent/atomic/AtomicBoolean;

    .line 288
    new-instance v0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel$2;

    const/16 v2, 0x40

    const/high16 v3, 0x3f400000    # 0.75f

    const/4 v4, 0x1

    invoke-direct {v0, v2, v3, v4}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel$2;-><init>(IFZ)V

    invoke-static {v0}, Ljava/util/Collections;->synchronizedMap(Ljava/util/Map;)Ljava/util/Map;

    move-result-object v0

    sput-object v0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->faces:Ljava/util/Map;

    new-array v0, v1, [B

    .line 291
    sput-object v0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->NO_FACE:[B

    .line 339
    new-instance v0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel$3;

    const/16 v2, 0x10

    invoke-direct {v0, v2, v3, v4}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel$3;-><init>(IFZ)V

    invoke-static {v0}, Ljava/util/Collections;->synchronizedMap(Ljava/util/Map;)Ljava/util/Map;

    move-result-object v0

    sput-object v0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->artWhy:Ljava/util/Map;

    .line 342
    new-instance v0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel$4;

    invoke-direct {v0, v2, v3, v4}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel$4;-><init>(IFZ)V

    invoke-static {v0}, Ljava/util/Collections;->synchronizedMap(Ljava/util/Map;)Ljava/util/Map;

    move-result-object v0

    sput-object v0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->arts:Ljava/util/Map;

    .line 345
    new-instance v0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel$5;

    const/16 v2, 0x8

    invoke-direct {v0, v2, v3, v4}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel$5;-><init>(IFZ)V

    invoke-static {v0}, Ljava/util/Collections;->synchronizedMap(Ljava/util/Map;)Ljava/util/Map;

    move-result-object v0

    sput-object v0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->artVideos:Ljava/util/Map;

    .line 540
    new-instance v0, Ljava/util/concurrent/atomic/AtomicBoolean;

    invoke-direct {v0, v1}, Ljava/util/concurrent/atomic/AtomicBoolean;-><init>(Z)V

    sput-object v0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->leaving:Ljava/util/concurrent/atomic/AtomicBoolean;

    return-void
.end method

.method private constructor <init>(Landroid/app/Activity;)V
    .registers 4

    .line 61
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    const/4 v0, -0x1

    .line 53
    iput v0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->safeLeft:I

    iput v0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->safeRight:I

    .line 57
    new-instance v0, Ljava/util/concurrent/atomic/AtomicBoolean;

    const/4 v1, 0x0

    invoke-direct {v0, v1}, Ljava/util/concurrent/atomic/AtomicBoolean;-><init>(Z)V

    iput-object v0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->starting:Ljava/util/concurrent/atomic/AtomicBoolean;

    .line 61
    iput-object p1, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->activity:Landroid/app/Activity;

    return-void
.end method

.method static synthetic access$100(Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;Landroid/webkit/WebResourceRequest;)Landroid/webkit/WebResourceResponse;
    .registers 2

    .line 44
    invoke-direct {p0, p1}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->serve(Landroid/webkit/WebResourceRequest;)Landroid/webkit/WebResourceResponse;

    move-result-object p0

    return-object p0
.end method

.method static synthetic access$1000(Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;)V
    .registers 1

    .line 44
    invoke-direct {p0}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->hide()V

    return-void
.end method

.method static synthetic access$1100(Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;)Ljava/util/concurrent/atomic/AtomicBoolean;
    .registers 1

    .line 44
    iget-object p0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->starting:Ljava/util/concurrent/atomic/AtomicBoolean;

    return-object p0
.end method

.method static synthetic access$1200()Ljava/util/concurrent/atomic/AtomicBoolean;
    .registers 1

    .line 44
    sget-object v0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->leaving:Ljava/util/concurrent/atomic/AtomicBoolean;

    return-object v0
.end method

.method static synthetic access$1300(Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;)Landroid/app/Activity;
    .registers 1

    .line 44
    iget-object p0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->activity:Landroid/app/Activity;

    return-object p0
.end method

.method static synthetic access$1400(Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;)Z
    .registers 1

    .line 44
    iget-boolean p0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->closed:Z

    return p0
.end method

.method static synthetic access$1500(Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;Ljava/lang/String;)V
    .registers 2

    .line 44
    invoke-direct {p0, p1}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->js(Ljava/lang/String;)V

    return-void
.end method

.method static synthetic access$1600(Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;)V
    .registers 1

    .line 44
    invoke-direct {p0}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->runMatchStart()V

    return-void
.end method

.method static synthetic access$1700(Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;)V
    .registers 1

    .line 44
    invoke-direct {p0}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->runLeave()V

    return-void
.end method

.method static synthetic access$200(Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;)V
    .registers 1

    .line 44
    invoke-direct {p0}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->applySafe()V

    return-void
.end method

.method static synthetic access$302(Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;Z)Z
    .registers 2

    .line 44
    iput-boolean p1, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->pageReady:Z

    return p1
.end method

.method static synthetic access$400(Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;)I
    .registers 1

    .line 44
    iget p0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->pendingPostMatch:I

    return p0
.end method

.method static synthetic access$402(Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;I)I
    .registers 2

    .line 44
    iput p1, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->pendingPostMatch:I

    return p1
.end method

.method static synthetic access$500(Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;I)V
    .registers 2

    .line 44
    invoke-direct {p0, p1}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->runPostMatch(I)V

    return-void
.end method

.method static synthetic access$600(Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;)Landroid/webkit/WebView;
    .registers 1

    .line 44
    iget-object p0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->web:Landroid/webkit/WebView;

    return-object p0
.end method

.method static synthetic access$700(Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;)V
    .registers 1

    .line 44
    invoke-direct {p0}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->dispose()V

    return-void
.end method

.method static synthetic access$800()Ljava/util/concurrent/atomic/AtomicBoolean;
    .registers 1

    .line 44
    sget-object v0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->simulating:Ljava/util/concurrent/atomic/AtomicBoolean;

    return-object v0
.end method

.method static synthetic access$900(Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;Ljava/lang/String;)V
    .registers 2

    .line 44
    invoke-direct {p0, p1}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->toast(Ljava/lang/String;)V

    return-void
.end method

.method private api(Ljava/lang/String;Landroid/net/Uri;)Landroid/webkit/WebResourceResponse;
    .registers 7

    const-string v0, "GET"

    .line 269
    invoke-virtual {v0, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result p1

    const-string v1, "application/json"

    const/16 v2, 0xc8

    if-nez p1, :cond_19

    const-string p1, "{}"

    sget-object p2, Ljava/nio/charset/StandardCharsets;->UTF_8:Ljava/nio/charset/Charset;

    invoke-virtual {p1, p2}, Ljava/lang/String;->getBytes(Ljava/nio/charset/Charset;)[B

    move-result-object p1

    invoke-static {v1, v2, p1}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->response(Ljava/lang/String;I[B)Landroid/webkit/WebResourceResponse;

    move-result-object p1

    return-object p1

    .line 273
    :cond_19
    :try_start_19
    new-instance p1, Lorg/json/JSONObject;

    invoke-direct {p1}, Lorg/json/JSONObject;-><init>()V

    const-string v3, "method"

    invoke-virtual {p1, v3, v0}, Lorg/json/JSONObject;->put(Ljava/lang/String;Ljava/lang/Object;)Lorg/json/JSONObject;

    move-result-object p1

    const-string v0, "path"

    invoke-virtual {p2}, Landroid/net/Uri;->getPath()Ljava/lang/String;

    move-result-object p2

    invoke-virtual {p1, v0, p2}, Lorg/json/JSONObject;->put(Ljava/lang/String;Ljava/lang/Object;)Lorg/json/JSONObject;

    move-result-object p1

    .line 274
    iget-object p2, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->activity:Landroid/app/Activity;

    const-string v0, "iml_api"

    invoke-virtual {p1}, Lorg/json/JSONObject;->toString()Ljava/lang/String;

    move-result-object p1

    invoke-static {p2, v0, p1}, Lorg/efootballrevival/runtimeprobe/EmbeddedGateway;->manage(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object p1

    .line 276
    new-instance p2, Lorg/json/JSONObject;

    invoke-direct {p2, p1}, Lorg/json/JSONObject;-><init>(Ljava/lang/String;)V

    const-string v0, "error"

    invoke-virtual {p2, v0}, Lorg/json/JSONObject;->isNull(Ljava/lang/String;)Z

    move-result p2
    :try_end_45
    .catch Ljava/lang/Exception; {:try_start_19 .. :try_end_45} :catch_4a

    if-nez p2, :cond_56

    const/16 v2, 0x194

    goto :goto_56

    :catch_4a
    move-exception p1

    const-string p2, "ML_LEAGUE"

    const-string v0, "iml_api failed"

    .line 278
    invoke-static {p2, v0, p1}, Landroid/util/Log;->w(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I

    const-string p1, "{\"error\":\"\u6570\u636e\u6682\u65f6\u4e0d\u53ef\u7528\"}"

    const/16 v2, 0x1f4

    .line 282
    :cond_56
    :goto_56
    sget-object p2, Ljava/nio/charset/StandardCharsets;->UTF_8:Ljava/nio/charset/Charset;

    invoke-virtual {p1, p2}, Ljava/lang/String;->getBytes(Ljava/nio/charset/Charset;)[B

    move-result-object p1

    invoke-static {v1, v2, p1}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->response(Ljava/lang/String;I[B)Landroid/webkit/WebResourceResponse;

    move-result-object p1

    return-object p1
.end method

.method private applySafe()V
    .registers 5

    .line 196
    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->web:Landroid/webkit/WebView;

    if-eqz v0, :cond_46

    iget v0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->safeLeft:I

    if-gez v0, :cond_9

    goto :goto_46

    .line 197
    :cond_9
    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->activity:Landroid/app/Activity;

    invoke-virtual {v0}, Landroid/app/Activity;->getResources()Landroid/content/res/Resources;

    move-result-object v0

    invoke-virtual {v0}, Landroid/content/res/Resources;->getDisplayMetrics()Landroid/util/DisplayMetrics;

    move-result-object v0

    iget v0, v0, Landroid/util/DisplayMetrics;->density:F

    .line 198
    iget-object v1, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->web:Landroid/webkit/WebView;

    new-instance v2, Ljava/lang/StringBuilder;

    const-string v3, "document.documentElement.style.setProperty(\'--safe-l\',\'"

    invoke-direct {v2, v3}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    iget v3, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->safeLeft:I

    int-to-float v3, v3

    div-float/2addr v3, v0

    invoke-static {v3}, Ljava/lang/Math;->round(F)I

    move-result v3

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    const-string v3, "px\');document.documentElement.style.setProperty(\'--safe-r\',\'"

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    iget v3, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->safeRight:I

    int-to-float v3, v3

    div-float/2addr v3, v0

    .line 199
    invoke-static {v3}, Ljava/lang/Math;->round(F)I

    move-result v0

    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    const-string v0, "px\');"

    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    const/4 v2, 0x0

    .line 198
    invoke-virtual {v1, v0, v2}, Landroid/webkit/WebView;->evaluateJavascript(Ljava/lang/String;Landroid/webkit/ValueCallback;)V

    :cond_46
    :goto_46
    return-void
.end method

.method public static busy()Z
    .registers 1

    .line 109
    sget-object v0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->simulating:Ljava/util/concurrent/atomic/AtomicBoolean;

    invoke-virtual {v0}, Ljava/util/concurrent/atomic/AtomicBoolean;->get()Z

    move-result v0

    if-nez v0, :cond_1f

    sget-object v0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->leaving:Ljava/util/concurrent/atomic/AtomicBoolean;

    invoke-virtual {v0}, Ljava/util/concurrent/atomic/AtomicBoolean;->get()Z

    move-result v0

    if-nez v0, :cond_1f

    sget-object v0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->active:Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;

    if-eqz v0, :cond_1d

    iget-object v0, v0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->starting:Ljava/util/concurrent/atomic/AtomicBoolean;

    invoke-virtual {v0}, Ljava/util/concurrent/atomic/AtomicBoolean;->get()Z

    move-result v0

    if-eqz v0, :cond_1d

    goto :goto_1f

    :cond_1d
    const/4 v0, 0x0

    goto :goto_20

    :cond_1f
    :goto_1f
    const/4 v0, 0x1

    :goto_20
    return v0
.end method

.method private cardArt(Ljava/lang/String;Ljava/lang/String;)[B
    .registers 15

    const-string v0, "ML_LEAGUE"

    const-string v1, "card art "

    const-string v2, "no recipe in the reply: "

    const-string v3, "[0-9]{1,18}"

    .line 351
    invoke-virtual {p1, v3}, Ljava/lang/String;->matches(Ljava/lang/String;)Z

    move-result v3

    const/4 v4, 0x0

    if-nez v3, :cond_10

    return-object v4

    :cond_10
    const-string v3, "video"

    .line 352
    invoke-virtual {v3, p2}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v3

    if-eqz v3, :cond_1b

    .line 353
    sget-object v5, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->artVideos:Ljava/util/Map;

    goto :goto_1d

    :cond_1b
    sget-object v5, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->arts:Ljava/util/Map;

    .line 354
    :goto_1d
    new-instance v6, Ljava/lang/StringBuilder;

    invoke-direct {v6}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v6, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v7, ":"

    invoke-virtual {v6, v7}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v6, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v6}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v6

    .line 355
    invoke-interface {v5, v6}, Ljava/util/Map;->get(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v7

    check-cast v7, [B

    if-eqz v7, :cond_3f

    .line 356
    array-length p1, v7

    if-nez p1, :cond_3d

    goto :goto_3e

    :cond_3d
    move-object v4, v7

    :goto_3e
    return-object v4

    .line 358
    :cond_3f
    :try_start_3f
    new-instance v7, Lorg/json/JSONObject;

    iget-object v8, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->activity:Landroid/app/Activity;

    const-string v9, "card_art"

    new-instance v10, Lorg/json/JSONObject;

    invoke-direct {v10}, Lorg/json/JSONObject;-><init>()V

    const-string v11, "id"

    invoke-virtual {v10, v11, p1}, Lorg/json/JSONObject;->put(Ljava/lang/String;Ljava/lang/Object;)Lorg/json/JSONObject;

    move-result-object p1

    const-string v10, "part"

    invoke-virtual {p1, v10, p2}, Lorg/json/JSONObject;->put(Ljava/lang/String;Ljava/lang/Object;)Lorg/json/JSONObject;

    move-result-object p1

    invoke-virtual {p1}, Lorg/json/JSONObject;->toString()Ljava/lang/String;

    move-result-object p1

    invoke-static {v8, v9, p1}, Lorg/efootballrevival/runtimeprobe/EmbeddedGateway;->manage(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object p1

    invoke-direct {v7, p1}, Lorg/json/JSONObject;-><init>(Ljava/lang/String;)V

    const-string p1, "found"

    .line 359
    invoke-virtual {v7, p1}, Lorg/json/JSONObject;->optBoolean(Ljava/lang/String;)Z

    move-result p1

    const/4 p2, 0x0

    if-eqz p1, :cond_7a

    if-eqz v3, :cond_6f

    const-string p1, "webm"

    goto :goto_71

    :cond_6f
    const-string p1, "png"

    :goto_71
    invoke-virtual {v7, p1}, Lorg/json/JSONObject;->optString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object p1

    invoke-static {p1, p2}, Landroid/util/Base64;->decode(Ljava/lang/String;I)[B

    move-result-object p1

    goto :goto_7b

    :cond_7a
    move-object p1, v4

    :goto_7b
    if-eqz p1, :cond_83

    .line 360
    array-length v3, p1

    const/16 v8, 0x8

    if-le v3, v8, :cond_83

    const/4 p2, 0x1

    :cond_83
    if-eqz p2, :cond_87

    move-object v3, p1

    goto :goto_89

    .line 361
    :cond_87
    sget-object v3, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->NO_FACE:[B

    :goto_89
    invoke-interface {v5, v6, v3}, Ljava/util/Map;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    if-nez p2, :cond_fa

    const-string v3, "recipe"

    .line 363
    invoke-virtual {v7, v3}, Lorg/json/JSONObject;->optJSONObject(Ljava/lang/String;)Lorg/json/JSONObject;

    move-result-object v3

    if-eqz v3, :cond_ca

    .line 364
    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V

    const-string v5, "status"

    invoke-virtual {v3, v5}, Lorg/json/JSONObject;->optString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v5

    invoke-virtual {v2, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v5, ": "

    invoke-virtual {v2, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v5, "reason"

    invoke-virtual {v3, v5}, Lorg/json/JSONObject;->optString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v5

    invoke-virtual {v2, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v5, " (kind "

    invoke-virtual {v2, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v5, "kind"

    invoke-virtual {v3, v5}, Lorg/json/JSONObject;->optString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v3

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v3, ")"

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v2

    goto :goto_de

    :cond_ca
    new-instance v3, Ljava/lang/StringBuilder;

    invoke-direct {v3, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    const-string v2, "error"

    const-string v5, "unknown"

    invoke-virtual {v7, v2, v5}, Lorg/json/JSONObject;->optString(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v2

    invoke-virtual {v3, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v2

    .line 365
    :goto_de
    sget-object v3, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->artWhy:Ljava/util/Map;

    invoke-interface {v3, v6, v2}, Ljava/util/Map;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    .line 366
    new-instance v3, Ljava/lang/StringBuilder;

    invoke-direct {v3, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v3, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v5, " not rendered: "

    invoke-virtual {v3, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v3, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v2

    invoke-static {v0, v2}, Landroid/util/Log;->w(Ljava/lang/String;Ljava/lang/String;)I
    :try_end_fa
    .catch Ljava/lang/Exception; {:try_start_3f .. :try_end_fa} :catch_fe

    :cond_fa
    if-eqz p2, :cond_fd

    move-object v4, p1

    :cond_fd
    return-object v4

    :catch_fe
    move-exception p1

    .line 370
    new-instance p2, Ljava/lang/StringBuilder;

    invoke-direct {p2, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {p2, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v1, " unavailable"

    invoke-virtual {p2, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {p2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p2

    invoke-static {v0, p2, p1}, Landroid/util/Log;->w(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I

    .line 371
    sget-object p2, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->artWhy:Ljava/util/Map;

    new-instance v0, Ljava/lang/StringBuilder;

    const-string v1, "exception: "

    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v0, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1

    invoke-interface {p2, v6, p1}, Ljava/util/Map;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    return-object v4
.end method

.method private crest(Ljava/lang/String;)[B
    .registers 18

    const/4 v1, 0x0

    .line 382
    :try_start_1
    invoke-static/range {p1 .. p1}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    move-result v2
    :try_end_5
    .catch Ljava/lang/NumberFormatException; {:try_start_1 .. :try_end_5} :catch_c1

    .line 383
    const-class v3, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;

    monitor-enter v3

    .line 384
    :try_start_8
    sget-object v0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->crestIndex:Ljava/util/Map;

    const/4 v4, 0x1

    const/4 v5, 0x0

    if-nez v0, :cond_98

    .line 385
    new-instance v6, Ljava/util/HashMap;

    invoke-direct {v6}, Ljava/util/HashMap;-><init>()V
    :try_end_13
    .catchall {:try_start_8 .. :try_end_13} :catchall_ba

    move-object/from16 v7, p0

    .line 387
    :try_start_15
    iget-object v0, v7, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->activity:Landroid/app/Activity;

    invoke-virtual {v0}, Landroid/app/Activity;->getAssets()Landroid/content/res/AssetManager;

    move-result-object v0

    const-string v8, "cup-crests/crests.bin"

    invoke-virtual {v0, v8}, Landroid/content/res/AssetManager;->open(Ljava/lang/String;)Ljava/io/InputStream;

    move-result-object v0

    const v8, 0xb71b00

    invoke-static {v0, v8}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->read(Ljava/io/InputStream;I)[B

    move-result-object v0

    .line 388
    invoke-static {v0}, Ljava/nio/ByteBuffer;->wrap([B)Ljava/nio/ByteBuffer;

    move-result-object v8

    sget-object v9, Ljava/nio/ByteOrder;->LITTLE_ENDIAN:Ljava/nio/ByteOrder;

    invoke-virtual {v8, v9}, Ljava/nio/ByteBuffer;->order(Ljava/nio/ByteOrder;)Ljava/nio/ByteBuffer;

    move-result-object v8

    .line 389
    array-length v9, v0

    const/16 v10, 0x8

    if-lt v9, v10, :cond_95

    aget-byte v9, v0, v5

    const/16 v11, 0x43

    if-ne v9, v11, :cond_95

    aget-byte v9, v0, v4

    const/16 v11, 0x52

    if-ne v9, v11, :cond_95

    const/4 v9, 0x2

    aget-byte v9, v0, v9

    const/16 v11, 0x53

    if-ne v9, v11, :cond_95

    const/4 v9, 0x3

    aget-byte v9, v0, v9

    const/16 v11, 0x54

    if-ne v9, v11, :cond_95

    const/4 v9, 0x4

    .line 390
    invoke-virtual {v8, v9}, Ljava/nio/ByteBuffer;->getInt(I)I

    move-result v9

    move v11, v5

    :goto_57
    if-ge v11, v9, :cond_8a

    mul-int/lit8 v12, v11, 0xc

    add-int/2addr v12, v10

    add-int/lit8 v13, v12, 0xc

    .line 391
    array-length v14, v0

    if-gt v13, v14, :cond_8a

    add-int/lit8 v13, v12, 0x4

    .line 392
    invoke-virtual {v8, v13}, Ljava/nio/ByteBuffer;->getInt(I)I

    move-result v13

    add-int/lit8 v14, v12, 0x8

    invoke-virtual {v8, v14}, Ljava/nio/ByteBuffer;->getInt(I)I

    move-result v14

    if-ltz v13, :cond_85

    if-lez v14, :cond_85

    add-int v15, v13, v14

    .line 393
    array-length v10, v0

    if-gt v15, v10, :cond_85

    invoke-virtual {v8, v12}, Ljava/nio/ByteBuffer;->getInt(I)I

    move-result v10

    invoke-static {v10}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v10

    filled-new-array {v13, v14}, [I

    move-result-object v12

    invoke-interface {v6, v10, v12}, Ljava/util/Map;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    :cond_85
    add-int/lit8 v11, v11, 0x1

    const/16 v10, 0x8

    goto :goto_57

    .line 395
    :cond_8a
    sput-object v0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->crestPack:[B
    :try_end_8c
    .catch Ljava/io/IOException; {:try_start_15 .. :try_end_8c} :catch_8d
    .catchall {:try_start_15 .. :try_end_8c} :catchall_bf

    goto :goto_95

    :catch_8d
    move-exception v0

    :try_start_8e
    const-string v8, "ML_LEAGUE"

    const-string v9, "crest pack unavailable"

    .line 398
    invoke-static {v8, v9, v0}, Landroid/util/Log;->w(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I

    .line 400
    :cond_95
    :goto_95
    sput-object v6, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->crestIndex:Ljava/util/Map;

    goto :goto_9a

    :cond_98
    move-object/from16 v7, p0

    .line 402
    :goto_9a
    sget-object v0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->crestIndex:Ljava/util/Map;

    invoke-static {v2}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v2

    invoke-interface {v0, v2}, Ljava/util/Map;->get(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, [I

    if-eqz v0, :cond_b8

    .line 403
    sget-object v2, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->crestPack:[B

    if-nez v2, :cond_ad

    goto :goto_b8

    .line 404
    :cond_ad
    aget v1, v0, v4

    new-array v4, v1, [B

    .line 405
    aget v0, v0, v5

    invoke-static {v2, v0, v4, v5, v1}, Ljava/lang/System;->arraycopy(Ljava/lang/Object;ILjava/lang/Object;II)V

    .line 406
    monitor-exit v3

    return-object v4

    .line 403
    :cond_b8
    :goto_b8
    monitor-exit v3

    return-object v1

    :catchall_ba
    move-exception v0

    move-object/from16 v7, p0

    .line 407
    :goto_bd
    monitor-exit v3
    :try_end_be
    .catchall {:try_start_8e .. :try_end_be} :catchall_bf

    throw v0

    :catchall_bf
    move-exception v0

    goto :goto_bd

    :catch_c1
    move-object/from16 v7, p0

    return-object v1
.end method

.method public static destroy(Landroid/app/Activity;)V
    .registers 3

    .line 95
    sget-object v0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->active:Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;

    if-eqz v0, :cond_b

    iget-object v1, v0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->activity:Landroid/app/Activity;

    if-ne v1, p0, :cond_b

    invoke-direct {v0}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->dispose()V

    :cond_b
    return-void
.end method

.method private dispose()V
    .registers 4

    .line 219
    iget-boolean v0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->closed:Z

    if-eqz v0, :cond_5

    return-void

    :cond_5
    const/4 v0, 0x1

    .line 220
    iput-boolean v0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->closed:Z

    .line 221
    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->web:Landroid/webkit/WebView;

    const/4 v1, 0x0

    if-eqz v0, :cond_30

    const-string v2, "AndroidMlLeague"

    .line 222
    invoke-virtual {v0, v2}, Landroid/webkit/WebView;->removeJavascriptInterface(Ljava/lang/String;)V

    .line 223
    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->web:Landroid/webkit/WebView;

    invoke-virtual {v0}, Landroid/webkit/WebView;->getParent()Landroid/view/ViewParent;

    move-result-object v0

    instance-of v0, v0, Landroid/view/ViewGroup;

    if-eqz v0, :cond_29

    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->web:Landroid/webkit/WebView;

    invoke-virtual {v0}, Landroid/webkit/WebView;->getParent()Landroid/view/ViewParent;

    move-result-object v0

    check-cast v0, Landroid/view/ViewGroup;

    iget-object v2, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->web:Landroid/webkit/WebView;

    invoke-virtual {v0, v2}, Landroid/view/ViewGroup;->removeView(Landroid/view/View;)V

    .line 224
    :cond_29
    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->web:Landroid/webkit/WebView;

    invoke-virtual {v0}, Landroid/webkit/WebView;->destroy()V

    .line 225
    iput-object v1, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->web:Landroid/webkit/WebView;

    .line 227
    :cond_30
    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->dialog:Landroid/app/Dialog;

    if-eqz v0, :cond_3f

    invoke-virtual {v0}, Landroid/app/Dialog;->isShowing()Z

    move-result v0

    if-eqz v0, :cond_3f

    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->dialog:Landroid/app/Dialog;

    invoke-virtual {v0}, Landroid/app/Dialog;->dismiss()V

    .line 228
    :cond_3f
    sget-object v0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->active:Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;

    if-ne v0, p0, :cond_45

    sput-object v1, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->active:Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;

    :cond_45
    return-void
.end method

.method private faceFile(Ljava/lang/String;)Ljava/io/File;
    .registers 5

    # RC29.17: no disk face cache - every miniface is rendered fresh from the game data
    const/4 v0, 0x0

    return-object v0

    .line 295
    new-instance v0, Ljava/io/File;

    iget-object v1, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->activity:Landroid/app/Activity;

    invoke-virtual {v1}, Landroid/app/Activity;->getCacheDir()Ljava/io/File;

    move-result-object v1

    const-string v2, "ml-faces-r29"

    invoke-direct {v0, v1, v2}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V

    .line 296
    invoke-virtual {v0}, Ljava/io/File;->isDirectory()Z

    move-result v1

    if-nez v1, :cond_21

    invoke-virtual {v0}, Ljava/io/File;->mkdirs()Z

    move-result v1

    if-nez v1, :cond_21

    invoke-virtual {v0}, Ljava/io/File;->isDirectory()Z

    move-result v1

    if-nez v1, :cond_21

    const/4 p1, 0x0

    return-object p1

    .line 297
    :cond_21
    new-instance v1, Ljava/io/File;

    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v2, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string p1, ".png"

    invoke-virtual {v2, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1

    invoke-direct {v1, v0, p1}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V

    return-object v1
.end method

.method private fail(Ljava/lang/String;)V
    .registers 2

    .line 515
    invoke-static {p1}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->reasonText(Ljava/lang/String;)Ljava/lang/String;

    move-result-object p1

    invoke-direct {p0, p1}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->failText(Ljava/lang/String;)V

    return-void
.end method

.method private failText(Ljava/lang/String;)V
    .registers 4

    const/4 v0, 0x0

    .line 534
    invoke-direct {p0, v0}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->passTouches(Z)V

    .line 535
    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->activity:Landroid/app/Activity;

    new-instance v1, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel$$ExternalSyntheticLambda7;

    invoke-direct {v1, p0}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel$$ExternalSyntheticLambda7;-><init>(Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;)V

    invoke-virtual {v0, v1}, Landroid/app/Activity;->runOnUiThread(Ljava/lang/Runnable;)V

    .line 536
    new-instance v0, Ljava/lang/StringBuilder;

    const-string v1, "window.MlLeague&&window.MlLeague.matchFailed("

    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-static {p1}, Lorg/json/JSONObject;->quote(Ljava/lang/String;)Ljava/lang/String;

    move-result-object p1

    invoke-virtual {v0, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string p1, ")"

    invoke-virtual {v0, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1

    invoke-direct {p0, p1}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->js(Ljava/lang/String;)V

    return-void
.end method

.method private failWith(Lorg/json/JSONObject;)V
    .registers 6

    const-string v0, "reason"

    .line 519
    invoke-virtual {p1, v0}, Lorg/json/JSONObject;->optString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    const-string v1, "blocked"

    .line 520
    invoke-virtual {v1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-nez v1, :cond_12

    invoke-direct {p0, v0}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->fail(Ljava/lang/String;)V

    return-void

    :cond_12
    const-string v0, "detail"

    .line 522
    invoke-virtual {p1, v0}, Lorg/json/JSONObject;->optJSONObject(Ljava/lang/String;)Lorg/json/JSONObject;

    move-result-object p1

    const/4 v0, 0x0

    if-nez p1, :cond_1d

    move-object p1, v0

    goto :goto_23

    :cond_1d
    const-string v1, "blockers"

    .line 523
    invoke-virtual {p1, v1}, Lorg/json/JSONObject;->optJSONArray(Ljava/lang/String;)Lorg/json/JSONArray;

    move-result-object p1

    :goto_23
    if-eqz p1, :cond_6d

    .line 524
    invoke-virtual {p1}, Lorg/json/JSONArray;->length()I

    move-result v1

    if-lez v1, :cond_6d

    const/4 v1, 0x0

    .line 525
    invoke-virtual {p1, v1}, Lorg/json/JSONArray;->optJSONObject(I)Lorg/json/JSONObject;

    move-result-object v1

    if-nez v1, :cond_34

    move-object v1, v0

    goto :goto_3c

    :cond_34
    const-string v2, "text"

    const-string v3, ""

    .line 526
    invoke-virtual {v1, v2, v3}, Lorg/json/JSONObject;->optString(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    :goto_3c
    if-eqz v1, :cond_45

    .line 527
    invoke-virtual {v1}, Ljava/lang/String;->isEmpty()Z

    move-result v2

    if-eqz v2, :cond_45

    goto :goto_46

    :cond_45
    move-object v0, v1

    :goto_46
    if-eqz v0, :cond_6d

    .line 528
    invoke-virtual {p1}, Lorg/json/JSONArray;->length()I

    move-result v1

    const/4 v2, 0x1

    if-le v1, v2, :cond_6d

    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v0, "\uff08\u53e6\u6709 "

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {p1}, Lorg/json/JSONArray;->length()I

    move-result p1

    sub-int/2addr p1, v2

    invoke-virtual {v1, p1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    const-string p1, " \u9879\uff09"

    invoke-virtual {v1, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    :cond_6d
    if-eqz v0, :cond_70

    goto :goto_72

    :cond_70
    const-string v0, "\u5f00\u8d5b\u524d\u68c0\u67e5\u6ca1\u6709\u901a\u8fc7\uff0c\u8bf7\u8c03\u6574\u9635\u5bb9\u540e\u518d\u8bd5"

    .line 530
    :goto_72
    invoke-direct {p0, v0}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->failText(Ljava/lang/String;)V

    return-void
.end method

.method private hide()V
    .registers 3

    .line 202
    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->activity:Landroid/app/Activity;

    new-instance v1, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel$$ExternalSyntheticLambda1;

    invoke-direct {v1, p0}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel$$ExternalSyntheticLambda1;-><init>(Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;)V

    invoke-virtual {v0, v1}, Landroid/app/Activity;->runOnUiThread(Ljava/lang/Runnable;)V

    return-void
.end method

.method public static hideActive()V
    .registers 1

    .line 91
    sget-object v0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->active:Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;

    if-eqz v0, :cond_19

    iget-boolean v0, v0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->closed:Z

    if-nez v0, :cond_19

    sget-object v0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->active:Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;

    iget-object v0, v0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->dialog:Landroid/app/Dialog;

    if-eqz v0, :cond_19

    invoke-virtual {v0}, Landroid/app/Dialog;->isShowing()Z

    move-result v0

    if-eqz v0, :cond_19

    sget-object v0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->active:Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;

    invoke-direct {v0}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->hideDialog()V

    :cond_19
    return-void
.end method

.method private hideDialog()V
    .registers 2

    .line 207
    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->dialog:Landroid/app/Dialog;

    if-nez v0, :cond_5

    return-void

    .line 208
    :cond_5
    invoke-virtual {v0}, Landroid/app/Dialog;->hide()V

    const-string v0, "window.MlLeague&&window.MlLeague.setHidden&&window.MlLeague.setHidden(true)"

    .line 209
    invoke-direct {p0, v0}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->js(Ljava/lang/String;)V

    return-void
.end method

.method public static isShowing()Z
    .registers 1

    .line 106
    sget-object v0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->active:Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;

    if-eqz v0, :cond_16

    iget-boolean v0, v0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->closed:Z

    if-nez v0, :cond_16

    sget-object v0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->active:Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;

    iget-object v0, v0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->dialog:Landroid/app/Dialog;

    if-eqz v0, :cond_16

    invoke-virtual {v0}, Landroid/app/Dialog;->isShowing()Z

    move-result v0

    if-eqz v0, :cond_16

    const/4 v0, 0x1

    goto :goto_17

    :cond_16
    const/4 v0, 0x0

    :goto_17
    return v0
.end method

.method private js(Ljava/lang/String;)V
    .registers 4

    .line 438
    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->activity:Landroid/app/Activity;

    new-instance v1, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel$$ExternalSyntheticLambda10;

    invoke-direct {v1, p0, p1}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel$$ExternalSyntheticLambda10;-><init>(Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;Ljava/lang/String;)V

    invoke-virtual {v0, v1}, Landroid/app/Activity;->runOnUiThread(Ljava/lang/Runnable;)V

    return-void
.end method

.method private static leaveFailText(Ljava/lang/String;)Ljava/lang/String;
    .registers 3

    const-string v0, "cancelled"

    .line 581
    invoke-virtual {v0, p0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_a

    const/4 p0, 0x0

    return-object p0

    :cond_a
    const-string v0, "not-on-match-page"

    .line 582
    invoke-virtual {v0, p0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_2f

    const-string v0, "timeout"

    invoke-virtual {v0, p0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_1b

    goto :goto_2f

    .line 584
    :cond_1b
    new-instance v0, Ljava/lang/StringBuilder;

    const-string v1, "\u5207\u56de\u4e3b\u5b58\u6863\u6ca1\u6709\u5b8c\u6210\uff08"

    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v0, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string p0, "\uff09\uff1b\u6e38\u620f\u91cd\u542f\u540e\u4f1a\u81ea\u52a8\u56de\u5230\u4e3b\u5b58\u6863"

    invoke-virtual {v0, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    return-object p0

    :cond_2f
    :goto_2f
    const-string p0, "\u6ca1\u80fd\u5207\u56de\u4e3b\u5b58\u6863\uff08\u6ca1\u7b49\u5230\u300c\u6bd4\u8d5b\u300d\u9875\uff09\uff1b\u6e38\u620f\u91cd\u542f\u540e\u4f1a\u81ea\u52a8\u56de\u5230\u4e3b\u5b58\u6863"

    return-object p0
.end method

.method private static mime(Ljava/lang/String;)Ljava/lang/String;
    .registers 2

    const-string v0, ".html"

    .line 418
    invoke-virtual {p0, v0}, Ljava/lang/String;->endsWith(Ljava/lang/String;)Z

    move-result v0

    if-eqz v0, :cond_b

    const-string p0, "text/html"

    goto :goto_65

    :cond_b
    const-string v0, ".js"

    invoke-virtual {p0, v0}, Ljava/lang/String;->endsWith(Ljava/lang/String;)Z

    move-result v0

    if-eqz v0, :cond_16

    const-string p0, "application/javascript"

    goto :goto_65

    :cond_16
    const-string v0, ".css"

    invoke-virtual {p0, v0}, Ljava/lang/String;->endsWith(Ljava/lang/String;)Z

    move-result v0

    if-eqz v0, :cond_21

    const-string p0, "text/css"

    goto :goto_65

    :cond_21
    const-string v0, ".json"

    .line 419
    invoke-virtual {p0, v0}, Ljava/lang/String;->endsWith(Ljava/lang/String;)Z

    move-result v0

    if-eqz v0, :cond_2c

    const-string p0, "application/json"

    goto :goto_65

    :cond_2c
    const-string v0, ".svg"

    invoke-virtual {p0, v0}, Ljava/lang/String;->endsWith(Ljava/lang/String;)Z

    move-result v0

    if-eqz v0, :cond_37

    const-string p0, "image/svg+xml"

    goto :goto_65

    :cond_37
    const-string v0, ".png"

    invoke-virtual {p0, v0}, Ljava/lang/String;->endsWith(Ljava/lang/String;)Z

    move-result v0

    if-eqz v0, :cond_42

    const-string p0, "image/png"

    goto :goto_65

    :cond_42
    const-string v0, ".jpg"

    .line 420
    invoke-virtual {p0, v0}, Ljava/lang/String;->endsWith(Ljava/lang/String;)Z

    move-result v0

    if-eqz v0, :cond_4d

    const-string p0, "image/jpeg"

    goto :goto_65

    :cond_4d
    const-string v0, ".wav"

    invoke-virtual {p0, v0}, Ljava/lang/String;->endsWith(Ljava/lang/String;)Z

    move-result v0

    if-eqz v0, :cond_58

    const-string p0, "audio/wav"

    goto :goto_65

    :cond_58
    const-string v0, ".ttf"

    invoke-virtual {p0, v0}, Ljava/lang/String;->endsWith(Ljava/lang/String;)Z

    move-result p0

    if-eqz p0, :cond_63

    const-string p0, "font/ttf"

    goto :goto_65

    :cond_63
    const-string p0, "application/octet-stream"

    :goto_65
    return-object p0
.end method

.method private open()V
    .registers 9

    .line 112
    new-instance v0, Landroid/app/Dialog;

    iget-object v1, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->activity:Landroid/app/Activity;

    const v2, 0x103022e

    invoke-direct {v0, v1, v2}, Landroid/app/Dialog;-><init>(Landroid/content/Context;I)V

    iput-object v0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->dialog:Landroid/app/Dialog;

    .line 113
    new-instance v0, Landroid/widget/LinearLayout;

    iget-object v1, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->activity:Landroid/app/Activity;

    invoke-direct {v0, v1}, Landroid/widget/LinearLayout;-><init>(Landroid/content/Context;)V

    const/4 v1, 0x1

    .line 114
    invoke-virtual {v0, v1}, Landroid/widget/LinearLayout;->setOrientation(I)V

    const v2, -0xf4f4f4

    .line 115
    invoke-virtual {v0, v2}, Landroid/widget/LinearLayout;->setBackgroundColor(I)V

    .line 116
    new-instance v3, Landroid/webkit/WebView;

    iget-object v4, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->activity:Landroid/app/Activity;

    invoke-direct {v3, v4}, Landroid/webkit/WebView;-><init>(Landroid/content/Context;)V

    iput-object v3, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->web:Landroid/webkit/WebView;

    .line 117
    invoke-virtual {v3, v2}, Landroid/webkit/WebView;->setBackgroundColor(I)V

    .line 118
    iget-object v3, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->web:Landroid/webkit/WebView;

    invoke-virtual {v3}, Landroid/webkit/WebView;->getSettings()Landroid/webkit/WebSettings;

    move-result-object v3

    .line 119
    invoke-virtual {v3, v1}, Landroid/webkit/WebSettings;->setJavaScriptEnabled(Z)V

    .line 120
    invoke-virtual {v3, v1}, Landroid/webkit/WebSettings;->setDomStorageEnabled(Z)V

    const/4 v4, 0x2

    .line 121
    invoke-virtual {v3, v4}, Landroid/webkit/WebSettings;->setCacheMode(I)V

    const/4 v4, 0x0

    .line 122
    invoke-virtual {v3, v4}, Landroid/webkit/WebSettings;->setAllowFileAccess(Z)V

    .line 123
    invoke-virtual {v3, v4}, Landroid/webkit/WebSettings;->setAllowContentAccess(Z)V

    .line 124
    invoke-virtual {v3, v1}, Landroid/webkit/WebSettings;->setMixedContentMode(I)V

    .line 125
    invoke-virtual {v3, v4}, Landroid/webkit/WebSettings;->setSupportZoom(Z)V

    .line 126
    invoke-virtual {v3, v4}, Landroid/webkit/WebSettings;->setMediaPlaybackRequiresUserGesture(Z)V

    .line 127
    iget-object v3, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->web:Landroid/webkit/WebView;

    new-instance v5, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel$Bridge;

    const/4 v6, 0x0

    invoke-direct {v5, p0, v6}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel$Bridge;-><init>(Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;Lorg/efootballrevival/runtimeprobe/MlLeaguePanel$1;)V

    const-string v6, "AndroidMlLeague"

    invoke-virtual {v3, v5, v6}, Landroid/webkit/WebView;->addJavascriptInterface(Ljava/lang/Object;Ljava/lang/String;)V

    .line 128
    iget-object v3, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->web:Landroid/webkit/WebView;

    new-instance v5, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel$1;

    invoke-direct {v5, p0}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel$1;-><init>(Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;)V

    invoke-virtual {v3, v5}, Landroid/webkit/WebView;->setWebViewClient(Landroid/webkit/WebViewClient;)V

    .line 146
    new-instance v3, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel$$ExternalSyntheticLambda3;

    invoke-direct {v3, p0}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel$$ExternalSyntheticLambda3;-><init>(Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;)V

    invoke-virtual {v0, v3}, Landroid/widget/LinearLayout;->setOnApplyWindowInsetsListener(Landroid/view/View$OnApplyWindowInsetsListener;)V

    .line 154
    iget-object v3, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->web:Landroid/webkit/WebView;

    new-instance v5, Landroid/widget/LinearLayout$LayoutParams;

    const/high16 v6, 0x3f800000    # 1.0f

    const/4 v7, -0x1

    invoke-direct {v5, v7, v4, v6}, Landroid/widget/LinearLayout$LayoutParams;-><init>(IIF)V

    invoke-virtual {v0, v3, v5}, Landroid/widget/LinearLayout;->addView(Landroid/view/View;Landroid/view/ViewGroup$LayoutParams;)V

    .line 155
    iget-object v3, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->dialog:Landroid/app/Dialog;

    invoke-virtual {v3, v0}, Landroid/app/Dialog;->setContentView(Landroid/view/View;)V

    .line 156
    iget-object v3, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->dialog:Landroid/app/Dialog;

    invoke-virtual {v3, v4}, Landroid/app/Dialog;->setCancelable(Z)V

    .line 157
    iget-object v3, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->dialog:Landroid/app/Dialog;

    new-instance v5, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel$$ExternalSyntheticLambda4;

    invoke-direct {v5, p0}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel$$ExternalSyntheticLambda4;-><init>(Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;)V

    invoke-virtual {v3, v5}, Landroid/app/Dialog;->setOnKeyListener(Landroid/content/DialogInterface$OnKeyListener;)V

    .line 164
    iget-object v3, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->dialog:Landroid/app/Dialog;

    new-instance v5, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel$$ExternalSyntheticLambda5;

    invoke-direct {v5, p0}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel$$ExternalSyntheticLambda5;-><init>(Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;)V

    invoke-virtual {v3, v5}, Landroid/app/Dialog;->setOnDismissListener(Landroid/content/DialogInterface$OnDismissListener;)V

    .line 165
    iget-object v3, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->dialog:Landroid/app/Dialog;

    invoke-virtual {v3}, Landroid/app/Dialog;->show()V

    .line 166
    iget-object v3, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->dialog:Landroid/app/Dialog;

    invoke-virtual {v3}, Landroid/app/Dialog;->getWindow()Landroid/view/Window;

    move-result-object v3

    if-eqz v3, :cond_ee

    .line 167
    iget-object v3, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->dialog:Landroid/app/Dialog;

    invoke-virtual {v3}, Landroid/app/Dialog;->getWindow()Landroid/view/Window;

    move-result-object v3

    invoke-static {v3}, Lorg/efootballrevival/runtimeprobe/InsetsCompat;->drawBehindBars(Landroid/view/Window;)V

    .line 168
    iget-object v3, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->dialog:Landroid/app/Dialog;

    invoke-virtual {v3}, Landroid/app/Dialog;->getWindow()Landroid/view/Window;

    move-result-object v3

    invoke-virtual {v3, v7, v7}, Landroid/view/Window;->setLayout(II)V

    .line 169
    iget-object v3, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->dialog:Landroid/app/Dialog;

    invoke-virtual {v3}, Landroid/app/Dialog;->getWindow()Landroid/view/Window;

    move-result-object v3

    invoke-virtual {v3, v4}, Landroid/view/Window;->setStatusBarColor(I)V

    .line 170
    iget-object v3, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->dialog:Landroid/app/Dialog;

    invoke-virtual {v3}, Landroid/app/Dialog;->getWindow()Landroid/view/Window;

    move-result-object v3

    invoke-virtual {v3, v2}, Landroid/view/Window;->setNavigationBarColor(I)V

    .line 171
    iget-object v2, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->dialog:Landroid/app/Dialog;

    invoke-virtual {v2}, Landroid/app/Dialog;->getWindow()Landroid/view/Window;

    move-result-object v2

    invoke-static {v2}, Lorg/efootballrevival/runtimeprobe/InsetsCompat;->hideBarsImmersive(Landroid/view/Window;)V

    .line 174
    iget-object v2, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->dialog:Landroid/app/Dialog;

    invoke-virtual {v2}, Landroid/app/Dialog;->getWindow()Landroid/view/Window;

    move-result-object v2

    const/16 v3, 0x300

    invoke-virtual {v2, v3}, Landroid/view/Window;->addFlags(I)V

    .line 175
    iget-object v2, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->dialog:Landroid/app/Dialog;

    invoke-virtual {v2}, Landroid/app/Dialog;->getWindow()Landroid/view/Window;

    move-result-object v2

    invoke-virtual {v2}, Landroid/view/Window;->getAttributes()Landroid/view/WindowManager$LayoutParams;

    move-result-object v2

    const/4 v3, 0x3

    .line 176
    iput v3, v2, Landroid/view/WindowManager$LayoutParams;->layoutInDisplayCutoutMode:I

    .line 177
    iget-object v3, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->dialog:Landroid/app/Dialog;

    invoke-virtual {v3}, Landroid/app/Dialog;->getWindow()Landroid/view/Window;

    move-result-object v3

    invoke-virtual {v3, v2}, Landroid/view/Window;->setAttributes(Landroid/view/WindowManager$LayoutParams;)V

    .line 179
    :cond_ee
    new-instance v2, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel$$ExternalSyntheticLambda6;

    invoke-direct {v2, v0}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel$$ExternalSyntheticLambda6;-><init>(Landroid/widget/LinearLayout;)V

    invoke-virtual {v0, v2}, Landroid/widget/LinearLayout;->post(Ljava/lang/Runnable;)Z

    .line 181
    invoke-static {}, Lorg/efootballrevival/runtimeprobe/UiStrings;->language()Ljava/lang/String;

    move-result-object v0

    const-string v2, "zh"

    if-eqz v0, :cond_10b

    .line 182
    sget-object v3, Ljava/util/Locale;->ROOT:Ljava/util/Locale;

    invoke-virtual {v0, v3}, Ljava/lang/String;->toLowerCase(Ljava/util/Locale;)Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v0, v2}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result v0

    if-eqz v0, :cond_10b

    goto :goto_10c

    :cond_10b
    move v1, v4

    .line 183
    :goto_10c
    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->web:Landroid/webkit/WebView;

    if-eqz v1, :cond_111

    goto :goto_113

    :cond_111
    const-string v2, "en"

    :goto_113
    const-string v1, "https://ml-league.local/index.html?lang="

    invoke-virtual {v1, v2}, Ljava/lang/String;->concat(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Landroid/webkit/WebView;->loadUrl(Ljava/lang/String;)V

    return-void
.end method

.method private passTouches(Z)V
    .registers 4

    .line 442
    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->activity:Landroid/app/Activity;

    new-instance v1, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel$$ExternalSyntheticLambda2;

    invoke-direct {v1, p0, p1}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel$$ExternalSyntheticLambda2;-><init>(Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;Z)V

    invoke-virtual {v0, v1}, Landroid/app/Activity;->runOnUiThread(Ljava/lang/Runnable;)V

    return-void
.end method

.method private playerFace(Ljava/lang/String;)[B
    .registers 11

    const-string v0, "[0-9]{1,18}"

    .line 302
    invoke-virtual {p1, v0}, Ljava/lang/String;->matches(Ljava/lang/String;)Z

    move-result v0

    const/4 v1, 0x0

    if-nez v0, :cond_a

    return-object v1

    .line 303
    :cond_a
    sget-object v0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->faces:Ljava/util/Map;

    invoke-interface {v0, p1}, Ljava/util/Map;->get(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v2

    check-cast v2, [B

    if-eqz v2, :cond_1a

    .line 304
    array-length p1, v2

    if-nez p1, :cond_18

    goto :goto_19

    :cond_18
    move-object v1, v2

    :goto_19
    return-object v1

    .line 305
    :cond_1a
    invoke-direct {p0, p1}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->faceFile(Ljava/lang/String;)Ljava/io/File;

    move-result-object v2

    const/16 v3, 0x8

    const-string v4, "ML_LEAGUE"

    if-eqz v2, :cond_6e

    .line 306
    invoke-virtual {v2}, Ljava/io/File;->isFile()Z

    move-result v5

    if-eqz v5, :cond_6e

    invoke-virtual {v2}, Ljava/io/File;->length()J

    move-result-wide v5

    const-wide/16 v7, 0x8

    cmp-long v5, v5, v7

    if-lez v5, :cond_6e

    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v5

    invoke-virtual {v2}, Ljava/io/File;->lastModified()J

    move-result-wide v7

    sub-long/2addr v5, v7

    const-wide/32 v7, 0x1b7740

    cmp-long v5, v5, v7

    if-gez v5, :cond_6e

    .line 308
    :try_start_44
    new-instance v5, Ljava/io/FileInputStream;

    invoke-direct {v5, v2}, Ljava/io/FileInputStream;-><init>(Ljava/io/File;)V

    const v6, 0xb71b00

    invoke-static {v5, v6}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->read(Ljava/io/InputStream;I)[B

    move-result-object v5

    .line 309
    array-length v6, v5

    if-le v6, v3, :cond_6e

    invoke-interface {v0, p1, v5}, Ljava/util/Map;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    :try_end_56
    .catch Ljava/io/IOException; {:try_start_44 .. :try_end_56} :catch_57

    return-object v5

    :catch_57
    move-exception v0

    .line 311
    new-instance v5, Ljava/lang/StringBuilder;

    const-string v6, "face cache "

    invoke-direct {v5, v6}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v5, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v6, " unreadable"

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v5}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v5

    invoke-static {v4, v5, v0}, Landroid/util/Log;->w(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I

    .line 316
    :cond_6e
    :try_start_6e
    new-instance v0, Lorg/json/JSONObject;

    iget-object v5, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->activity:Landroid/app/Activity;

    const-string v6, "editor_portrait"

    new-instance v7, Lorg/json/JSONObject;

    invoke-direct {v7}, Lorg/json/JSONObject;-><init>()V

    const-string v8, "id"

    invoke-virtual {v7, v8, p1}, Lorg/json/JSONObject;->put(Ljava/lang/String;Ljava/lang/Object;)Lorg/json/JSONObject;

    move-result-object v7

    invoke-virtual {v7}, Lorg/json/JSONObject;->toString()Ljava/lang/String;

    move-result-object v7

    invoke-static {v5, v6, v7}, Lorg/efootballrevival/runtimeprobe/EmbeddedGateway;->manage(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v5

    invoke-direct {v0, v5}, Lorg/json/JSONObject;-><init>(Ljava/lang/String;)V

    const-string v5, "found"

    .line 317
    invoke-virtual {v0, v5}, Lorg/json/JSONObject;->optBoolean(Ljava/lang/String;)Z

    move-result v5

    const/4 v6, 0x0

    if-eqz v5, :cond_9e

    const-string v5, "png"

    invoke-virtual {v0, v5}, Lorg/json/JSONObject;->optString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    invoke-static {v0, v6}, Landroid/util/Base64;->decode(Ljava/lang/String;I)[B

    move-result-object v0
    :try_end_9d
    .catch Ljava/lang/Exception; {:try_start_6e .. :try_end_9d} :catch_fb

    goto :goto_9f

    :cond_9e
    move-object v0, v1

    :goto_9f
    if-eqz v0, :cond_a5

    .line 322
    array-length v4, v0

    if-le v4, v3, :cond_a5

    const/4 v6, 0x1

    .line 323
    :cond_a5
    sget-object v3, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->faces:Ljava/util/Map;

    if-eqz v6, :cond_ab

    move-object v4, v0

    goto :goto_ad

    :cond_ab
    sget-object v4, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->NO_FACE:[B

    :goto_ad
    invoke-interface {v3, p1, v4}, Ljava/util/Map;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    if-eqz v6, :cond_f7

    if-eqz v2, :cond_f7

    .line 325
    new-instance p1, Ljava/io/File;

    new-instance v3, Ljava/lang/StringBuilder;

    invoke-direct {v3}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v2}, Ljava/io/File;->getPath()Ljava/lang/String;

    move-result-object v4

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v4, ".tmp"

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v3

    invoke-direct {p1, v3}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    .line 326
    :try_start_ce
    new-instance v3, Ljava/io/FileOutputStream;

    invoke-direct {v3, p1}, Ljava/io/FileOutputStream;-><init>(Ljava/io/File;)V
    :try_end_d3
    .catch Ljava/io/IOException; {:try_start_ce .. :try_end_d3} :catch_f4

    .line 327
    :try_start_d3
    invoke-virtual {v3, v0}, Ljava/io/FileOutputStream;->write([B)V

    .line 328
    invoke-virtual {v3}, Ljava/io/FileOutputStream;->getFD()Ljava/io/FileDescriptor;

    move-result-object v4

    invoke-virtual {v4}, Ljava/io/FileDescriptor;->sync()V

    .line 329
    invoke-virtual {p1, v2}, Ljava/io/File;->renameTo(Ljava/io/File;)Z

    move-result v2

    if-nez v2, :cond_e6

    invoke-virtual {p1}, Ljava/io/File;->delete()Z
    :try_end_e6
    .catchall {:try_start_d3 .. :try_end_e6} :catchall_ea

    .line 330
    :cond_e6
    :try_start_e6
    invoke-virtual {v3}, Ljava/io/FileOutputStream;->close()V
    :try_end_e9
    .catch Ljava/io/IOException; {:try_start_e6 .. :try_end_e9} :catch_f4

    goto :goto_f7

    :catchall_ea
    move-exception v2

    .line 326
    :try_start_eb
    invoke-virtual {v3}, Ljava/io/FileOutputStream;->close()V
    :try_end_ee
    .catchall {:try_start_eb .. :try_end_ee} :catchall_ef

    goto :goto_f3

    :catchall_ef
    move-exception v3

    :try_start_f0
    invoke-virtual {v2, v3}, Ljava/lang/Throwable;->addSuppressed(Ljava/lang/Throwable;)V

    :goto_f3
    throw v2
    :try_end_f4
    .catch Ljava/io/IOException; {:try_start_f0 .. :try_end_f4} :catch_f4

    .line 331
    :catch_f4
    invoke-virtual {p1}, Ljava/io/File;->delete()Z

    :cond_f7
    :goto_f7
    if-eqz v6, :cond_fa

    move-object v1, v0

    :cond_fa
    return-object v1

    :catch_fb
    move-exception v0

    .line 319
    new-instance v2, Ljava/lang/StringBuilder;

    const-string v3, "portrait "

    invoke-direct {v2, v3}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v2, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string p1, " unavailable"

    invoke-virtual {v2, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1

    invoke-static {v4, p1, v0}, Landroid/util/Log;->w(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I

    return-object v1
.end method

.method private pushSafe(II)V
    .registers 4

    .line 188
    iget v0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->safeLeft:I

    if-ne p1, v0, :cond_9

    iget v0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->safeRight:I

    if-ne p2, v0, :cond_9

    return-void

    .line 189
    :cond_9
    iput p1, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->safeLeft:I

    .line 190
    iput p2, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->safeRight:I

    .line 191
    invoke-direct {p0}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->applySafe()V

    return-void
.end method

.method private static read(Ljava/io/InputStream;I)[B
    .registers 8
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 424
    :try_start_0
    new-instance v0, Ljava/io/ByteArrayOutputStream;

    invoke-direct {v0}, Ljava/io/ByteArrayOutputStream;-><init>()V
    :try_end_5
    .catchall {:try_start_0 .. :try_end_5} :catchall_39

    const v1, 0x8000

    :try_start_8
    new-array v1, v1, [B

    const/4 v2, 0x0

    move v3, v2

    .line 427
    :goto_c
    invoke-virtual {p0, v1}, Ljava/io/InputStream;->read([B)I

    move-result v4

    const/4 v5, -0x1

    if-eq v4, v5, :cond_22

    add-int/2addr v3, v4

    if-gt v3, p1, :cond_1a

    .line 430
    invoke-virtual {v0, v1, v2, v4}, Ljava/io/ByteArrayOutputStream;->write([BII)V

    goto :goto_c

    .line 429
    :cond_1a
    new-instance p1, Ljava/io/IOException;

    const-string v1, "asset too large"

    invoke-direct {p1, v1}, Ljava/io/IOException;-><init>(Ljava/lang/String;)V

    throw p1

    .line 432
    :cond_22
    invoke-virtual {v0}, Ljava/io/ByteArrayOutputStream;->toByteArray()[B

    move-result-object p1
    :try_end_26
    .catchall {:try_start_8 .. :try_end_26} :catchall_2f

    .line 433
    :try_start_26
    invoke-virtual {v0}, Ljava/io/ByteArrayOutputStream;->close()V
    :try_end_29
    .catchall {:try_start_26 .. :try_end_29} :catchall_39

    if-eqz p0, :cond_2e

    invoke-virtual {p0}, Ljava/io/InputStream;->close()V

    :cond_2e
    return-object p1

    :catchall_2f
    move-exception p1

    .line 424
    :try_start_30
    invoke-virtual {v0}, Ljava/io/ByteArrayOutputStream;->close()V
    :try_end_33
    .catchall {:try_start_30 .. :try_end_33} :catchall_34

    goto :goto_38

    :catchall_34
    move-exception v0

    :try_start_35
    invoke-virtual {p1, v0}, Ljava/lang/Throwable;->addSuppressed(Ljava/lang/Throwable;)V

    :goto_38
    throw p1
    :try_end_39
    .catchall {:try_start_35 .. :try_end_39} :catchall_39

    :catchall_39
    move-exception p1

    if-eqz p0, :cond_44

    :try_start_3c
    invoke-virtual {p0}, Ljava/io/InputStream;->close()V
    :try_end_3f
    .catchall {:try_start_3c .. :try_end_3f} :catchall_40

    goto :goto_44

    :catchall_40
    move-exception p0

    invoke-virtual {p1, p0}, Ljava/lang/Throwable;->addSuppressed(Ljava/lang/Throwable;)V

    :cond_44
    :goto_44
    throw p1
.end method

.method private ready()V
    .registers 3

    const-string v0, "window.MlLeague&&window.MlLeague.matchReady()"

    .line 511
    invoke-direct {p0, v0}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->js(Ljava/lang/String;)V

    .line 512
    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->activity:Landroid/app/Activity;

    new-instance v1, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel$$ExternalSyntheticLambda0;

    invoke-direct {v1, p0}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel$$ExternalSyntheticLambda0;-><init>(Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;)V

    invoke-virtual {v0, v1}, Landroid/app/Activity;->runOnUiThread(Ljava/lang/Runnable;)V

    return-void
.end method

.method private static reasonText(Ljava/lang/String;)Ljava/lang/String;
    .registers 3

    if-nez p0, :cond_5

    const-string p0, "\u5f00\u8d5b\u6ca1\u6709\u5b8c\u6210\uff0c\u8bf7\u91cd\u8bd5"

    return-object p0

    :cond_5
    const-string v0, "not-on-ai-division"

    .line 451
    invoke-virtual {p0, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_10

    const-string p0, "\u6ca1\u7b49\u5230 AI Division \u4e3b\u9875\uff1a\u8bf7\u4ece\u300c\u6bd4\u8d5b\u300d\u8fdb\u5165 AI Division \u540e\u518d\u5f00\u8d5b"

    return-object p0

    :cond_10
    const-string v0, "not-on-match-page"

    .line 452
    invoke-virtual {p0, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_1b

    const-string p0, "\u6ca1\u7b49\u5230\u300c\u6bd4\u8d5b\u300d\u9875\uff1a\u5207\u6362\u5927\u5e08\u8054\u8d5b\u9635\u5bb9\u8981\u5728\u300c\u6bd4\u8d5b\u300d\u9875\u8fdb\u884c\uff0c\u8bf7\u56de\u5230\u8be5\u9875\u540e\u518d\u5f00\u8d5b"

    return-object p0

    :cond_1b
    const-string v0, "page-unavailable"

    .line 453
    invoke-virtual {p0, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_26

    const-string p0, "\u65e0\u6cd5\u8bc6\u522b\u5f53\u524d\u6e38\u620f\u9875\u9762\uff0c\u8bf7\u91cd\u542f\u6e38\u620f\u540e\u518d\u8bd5"

    return-object p0

    :cond_26
    const-string v0, "open-card-unavailable"

    .line 454
    invoke-virtual {p0, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_31

    const-string p0, "AI Division \u73b0\u5728\u4e0d\u53ef\u8fdb\u5165\uff0c\u8bf7\u5728\u300c\u6bd4\u8d5b\u300d\u9875\u786e\u8ba4\u540e\u518d\u8bd5"

    return-object p0

    :cond_31
    const-string v0, "open-"

    .line 455
    invoke-virtual {p0, v0}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result v0

    if-eqz v0, :cond_3c

    const-string p0, "\u6ca1\u80fd\u4ece\u300c\u6bd4\u8d5b\u300d\u9875\u8fdb\u5165 AI Division\uff0c\u8bf7\u624b\u52a8\u8fdb\u5165\u540e\u518d\u5f00\u8d5b"

    return-object p0

    :cond_3c
    const-string v0, "hop-"

    .line 456
    invoke-virtual {p0, v0}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result v0

    if-eqz v0, :cond_47

    const-string p0, "\u6ca1\u80fd\u4ece\u8054\u8d5b\u5206\u7c7b\u9875\u8fdb\u5165 AI Division\uff0c\u8bf7\u624b\u52a8\u70b9\u300c\u5bf9\u9635AI\u7c7b\u522b\u300d\u540e\u518d\u5f00\u8d5b"

    return-object p0

    :cond_47
    const-string v0, "switch"

    .line 457
    invoke-virtual {p0, v0}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result v0

    if-eqz v0, :cond_52

    const-string p0, "\u5207\u6362\u5230\u5927\u5e08\u8054\u8d5b\u5b58\u6863\u5931\u8d25\uff0c\u8bf7\u91cd\u8bd5"

    return-object p0

    :cond_52
    const-string v0, "proceed-timeout"

    .line 458
    invoke-virtual {p0, v0}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result v0

    if-nez v0, :cond_82

    const-string v0, "proceed-not-idle"

    invoke-virtual {p0, v0}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result v0

    if-eqz v0, :cond_63

    goto :goto_82

    :cond_63
    const-string v0, "proceed-busy"

    .line 459
    invoke-virtual {p0, v0}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result v0

    if-eqz v0, :cond_6e

    const-string p0, "\u4e0a\u4e00\u6b21\u64cd\u4f5c\u8fd8\u6ca1\u7ed3\u675f\uff0c\u8bf7\u7a0d\u7b49\u518d\u8bd5"

    return-object p0

    .line 460
    :cond_6e
    new-instance v0, Ljava/lang/StringBuilder;

    const-string v1, "\u5f00\u8d5b\u6ca1\u6709\u5b8c\u6210\uff08"

    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v0, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string p0, "\uff09\uff0c\u8bf7\u91cd\u8bd5"

    invoke-virtual {v0, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    return-object p0

    :cond_82
    :goto_82
    const-string p0, "AI Division \u4e3b\u9875\u8fd8\u6ca1\u51c6\u5907\u597d\uff0c\u8bf7\u505c\u5728\u8be5\u9875\u518d\u8bd5"

    return-object p0
.end method

.method private static response(Ljava/lang/String;I[B)Landroid/webkit/WebResourceResponse;
    .registers 11

    .line 411
    new-instance v5, Ljava/util/HashMap;

    invoke-direct {v5}, Ljava/util/HashMap;-><init>()V

    const-string v0, "Cache-Control"

    const-string v1, "no-store"

    .line 412
    invoke-interface {v5, v0, v1}, Ljava/util/Map;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    const/16 v0, 0xc8

    if-ne p1, v0, :cond_14

    const-string v0, "OK"

    :goto_12
    move-object v4, v0

    goto :goto_1e

    :cond_14
    const/16 v0, 0x194

    if-ne p1, v0, :cond_1b

    const-string v0, "Not Found"

    goto :goto_12

    :cond_1b
    const-string v0, "Error"

    goto :goto_12

    .line 414
    :goto_1e
    new-instance v7, Landroid/webkit/WebResourceResponse;

    const-string v2, "UTF-8"

    new-instance v6, Ljava/io/ByteArrayInputStream;

    invoke-direct {v6, p2}, Ljava/io/ByteArrayInputStream;-><init>([B)V

    move-object v0, v7

    move-object v1, p0

    move v3, p1

    invoke-direct/range {v0 .. v6}, Landroid/webkit/WebResourceResponse;-><init>(Ljava/lang/String;Ljava/lang/String;ILjava/lang/String;Ljava/util/Map;Ljava/io/InputStream;)V

    return-object v7
.end method

.method private runLeave()V
    .registers 12

    const/4 v0, 0x0

    .line 550
    :try_start_1
    new-instance v1, Lorg/json/JSONObject;

    invoke-direct {v1}, Lorg/json/JSONObject;-><init>()V

    const-string v2, "pageTimeout"

    const-wide/high16 v3, 0x405e000000000000L    # 120.0

    invoke-virtual {v1, v2, v3, v4}, Lorg/json/JSONObject;->put(Ljava/lang/String;D)Lorg/json/JSONObject;

    move-result-object v1

    .line 551
    new-instance v2, Lorg/json/JSONObject;

    iget-object v3, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->activity:Landroid/app/Activity;

    const-string v4, "iml_leave"

    invoke-virtual {v1}, Lorg/json/JSONObject;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-static {v3, v4, v1}, Lorg/efootballrevival/runtimeprobe/EmbeddedGateway;->manage(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    invoke-direct {v2, v1}, Lorg/json/JSONObject;-><init>(Ljava/lang/String;)V

    .line 552
    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v3

    const-wide/32 v5, 0x1d4c0

    add-long/2addr v5, v3

    const-wide/32 v7, 0x15f90

    add-long/2addr v5, v7

    move v1, v0

    .line 555
    :goto_2c
    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v7

    cmp-long v7, v7, v5

    if-gez v7, :cond_b1

    const-string v7, "leave"

    const-string v8, "kind"

    .line 557
    invoke-virtual {v2, v8}, Lorg/json/JSONObject;->optString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v8

    invoke-virtual {v7, v8}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v7
    :try_end_40
    .catch Ljava/lang/Exception; {:try_start_1 .. :try_end_40} :catch_bd
    .catchall {:try_start_1 .. :try_end_40} :catchall_bb

    if-nez v7, :cond_48

    .line 576
    :cond_42
    :goto_42
    sget-object v1, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->leaving:Ljava/util/concurrent/atomic/AtomicBoolean;

    invoke-virtual {v1, v0}, Ljava/util/concurrent/atomic/AtomicBoolean;->set(Z)V

    return-void

    :cond_48
    :try_start_48
    const-string v7, "state"

    .line 558
    invoke-virtual {v2, v7}, Lorg/json/JSONObject;->optString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v7

    const-string v8, "ready"

    .line 559
    invoke-virtual {v8, v7}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v8

    if-eqz v8, :cond_6a

    const-string v1, "elapsed"

    const-wide/16 v3, 0x0

    .line 560
    invoke-virtual {v2, v1, v3, v4}, Lorg/json/JSONObject;->optDouble(Ljava/lang/String;D)D

    move-result-wide v1

    const-wide/high16 v3, 0x3ff0000000000000L    # 1.0

    cmpl-double v1, v1, v3

    if-ltz v1, :cond_42

    const-string v1, "\u5df2\u5207\u56de\u4e3b\u5b58\u6863"

    invoke-direct {p0, v1}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->toast(Ljava/lang/String;)V

    goto :goto_42

    :cond_6a
    const-string v8, "failed"

    .line 563
    invoke-virtual {v8, v7}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v7

    if-eqz v7, :cond_80

    const-string v1, "reason"

    invoke-virtual {v2, v1}, Lorg/json/JSONObject;->optString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    invoke-static {v1}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->leaveFailText(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    invoke-direct {p0, v1}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->toast(Ljava/lang/String;)V

    goto :goto_42

    :cond_80
    if-nez v1, :cond_9b

    const-string v7, "need_user"

    .line 564
    invoke-virtual {v2, v7}, Lorg/json/JSONObject;->optBoolean(Ljava/lang/String;)Z

    move-result v2

    if-eqz v2, :cond_9b

    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v7

    sub-long/2addr v7, v3

    const-wide/16 v9, 0x4b0

    cmp-long v2, v7, v9

    if-lez v2, :cond_9b

    const-string v1, "\u8bf7\u56de\u5230\u300c\u6bd4\u8d5b\u300d\u9875\uff0c\u56de\u5230\u540e\u81ea\u52a8\u5207\u56de\u4e3b\u5b58\u6863"

    .line 566
    invoke-direct {p0, v1}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->toast(Ljava/lang/String;)V

    const/4 v1, 0x1

    :cond_9b
    const-wide/16 v7, 0x12c

    .line 568
    invoke-static {v7, v8}, Ljava/lang/Thread;->sleep(J)V

    .line 569
    new-instance v2, Lorg/json/JSONObject;

    iget-object v7, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->activity:Landroid/app/Activity;

    const-string v8, "iml_status"

    const-string v9, "{}"

    invoke-static {v7, v8, v9}, Lorg/efootballrevival/runtimeprobe/EmbeddedGateway;->manage(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v7

    invoke-direct {v2, v7}, Lorg/json/JSONObject;-><init>(Ljava/lang/String;)V

    goto/16 :goto_2c

    :cond_b1
    const-string v1, "timeout"

    .line 571
    invoke-static {v1}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->leaveFailText(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    invoke-direct {p0, v1}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->toast(Ljava/lang/String;)V
    :try_end_ba
    .catch Ljava/lang/Exception; {:try_start_48 .. :try_end_ba} :catch_bd
    .catchall {:try_start_48 .. :try_end_ba} :catchall_bb

    goto :goto_ce

    :catchall_bb
    move-exception v1

    goto :goto_d4

    :catch_bd
    move-exception v1

    :try_start_be
    const-string v2, "ML_LEAGUE"

    const-string v3, "leave failed"

    .line 573
    invoke-static {v2, v3, v1}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I

    const-string v1, "exception"

    .line 574
    invoke-static {v1}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->leaveFailText(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    invoke-direct {p0, v1}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->toast(Ljava/lang/String;)V
    :try_end_ce
    .catchall {:try_start_be .. :try_end_ce} :catchall_bb

    .line 576
    :goto_ce
    sget-object v1, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->leaving:Ljava/util/concurrent/atomic/AtomicBoolean;

    invoke-virtual {v1, v0}, Ljava/util/concurrent/atomic/AtomicBoolean;->set(Z)V

    return-void

    :goto_d4
    sget-object v2, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->leaving:Ljava/util/concurrent/atomic/AtomicBoolean;

    invoke-virtual {v2, v0}, Ljava/util/concurrent/atomic/AtomicBoolean;->set(Z)V

    .line 577
    throw v1
.end method

.method private runMatchStart()V
    .registers 18

    move-object/from16 v1, p0

    const-string v0, "state"

    const-string v2, "failed"

    const-string v3, "kind"

    const-string v4, "start"

    const/4 v5, 0x0

    .line 479
    :try_start_b
    new-instance v6, Lorg/json/JSONObject;

    invoke-direct {v6}, Lorg/json/JSONObject;-><init>()V

    const-string v7, "pageTimeout"

    const-wide/high16 v8, 0x405e000000000000L    # 120.0

    invoke-virtual {v6, v7, v8, v9}, Lorg/json/JSONObject;->put(Ljava/lang/String;D)Lorg/json/JSONObject;

    move-result-object v6

    .line 480
    new-instance v7, Lorg/json/JSONObject;

    iget-object v8, v1, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->activity:Landroid/app/Activity;

    const-string v9, "iml_start"

    invoke-virtual {v6}, Lorg/json/JSONObject;->toString()Ljava/lang/String;

    move-result-object v6

    invoke-static {v8, v9, v6}, Lorg/efootballrevival/runtimeprobe/EmbeddedGateway;->manage(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v6

    invoke-direct {v7, v6}, Lorg/json/JSONObject;-><init>(Ljava/lang/String;)V

    .line 482
    invoke-virtual {v7, v3}, Lorg/json/JSONObject;->optString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v6

    invoke-virtual {v4, v6}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v6
    :try_end_31
    .catch Ljava/lang/Exception; {:try_start_b .. :try_end_31} :catch_c9
    .catchall {:try_start_b .. :try_end_31} :catchall_c7

    const-string v8, "proceed-busy"

    if-nez v6, :cond_3e

    :try_start_35
    invoke-direct {v1, v8}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->fail(Ljava/lang/String;)V
    :try_end_38
    .catch Ljava/lang/Exception; {:try_start_35 .. :try_end_38} :catch_c9
    .catchall {:try_start_35 .. :try_end_38} :catchall_c7

    .line 506
    :goto_38
    iget-object v0, v1, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->starting:Ljava/util/concurrent/atomic/AtomicBoolean;

    invoke-virtual {v0, v5}, Ljava/util/concurrent/atomic/AtomicBoolean;->set(Z)V

    return-void

    .line 483
    :cond_3e
    :try_start_3e
    invoke-virtual {v7, v0}, Lorg/json/JSONObject;->optString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v6

    invoke-virtual {v2, v6}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v6

    if-eqz v6, :cond_4c

    invoke-direct {v1, v7}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->failWith(Lorg/json/JSONObject;)V

    goto :goto_38

    .line 486
    :cond_4c
    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v6

    const-wide/32 v9, 0x1d4c0

    add-long/2addr v9, v6

    const-wide/32 v11, 0x15f90

    add-long/2addr v9, v11

    move v11, v5

    .line 488
    :cond_59
    :goto_59
    iget-boolean v12, v1, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->closed:Z

    if-nez v12, :cond_c1

    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v12

    cmp-long v12, v12, v9

    if-gez v12, :cond_c1

    const-wide/16 v12, 0x12c

    .line 489
    invoke-static {v12, v13}, Ljava/lang/Thread;->sleep(J)V

    .line 490
    new-instance v12, Lorg/json/JSONObject;

    iget-object v13, v1, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->activity:Landroid/app/Activity;

    const-string v14, "iml_status"

    const-string v15, "{}"

    invoke-static {v13, v14, v15}, Lorg/efootballrevival/runtimeprobe/EmbeddedGateway;->manage(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v13

    invoke-direct {v12, v13}, Lorg/json/JSONObject;-><init>(Ljava/lang/String;)V

    .line 491
    invoke-virtual {v12, v3}, Lorg/json/JSONObject;->optString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v13

    invoke-virtual {v4, v13}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v13

    if-nez v13, :cond_87

    invoke-direct {v1, v8}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->fail(Ljava/lang/String;)V

    goto :goto_38

    .line 492
    :cond_87
    invoke-virtual {v12, v0}, Lorg/json/JSONObject;->optString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v13

    const-string v14, "ready"

    .line 493
    invoke-virtual {v14, v13}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v14

    if-eqz v14, :cond_97

    invoke-direct/range {p0 .. p0}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->ready()V

    goto :goto_38

    .line 494
    :cond_97
    invoke-virtual {v2, v13}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v13

    if-eqz v13, :cond_a1

    invoke-direct {v1, v12}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->failWith(Lorg/json/JSONObject;)V

    goto :goto_38

    :cond_a1
    if-nez v11, :cond_59

    const-string v13, "need_user"

    .line 496
    invoke-virtual {v12, v13}, Lorg/json/JSONObject;->optBoolean(Ljava/lang/String;)Z

    move-result v13

    if-eqz v13, :cond_59

    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v13

    sub-long/2addr v13, v6

    const-wide/16 v15, 0x4b0

    cmp-long v13, v13, v15

    if-lez v13, :cond_59

    const-string v11, "hint"

    .line 498
    invoke-virtual {v12, v11}, Lorg/json/JSONObject;->optString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v11

    invoke-direct {v1, v11}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->showPageHint(Ljava/lang/String;)V

    const/4 v11, 0x1

    goto :goto_59

    :cond_c1
    const-string v0, "timeout"

    .line 501
    invoke-direct {v1, v0}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->fail(Ljava/lang/String;)V
    :try_end_c6
    .catch Ljava/lang/Exception; {:try_start_3e .. :try_end_c6} :catch_c9
    .catchall {:try_start_3e .. :try_end_c6} :catchall_c7

    goto :goto_d6

    :catchall_c7
    move-exception v0

    goto :goto_dc

    :catch_c9
    move-exception v0

    :try_start_ca
    const-string v2, "ML_LEAGUE"

    const-string v3, "match start failed"

    .line 503
    invoke-static {v2, v3, v0}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I

    const-string v0, "exception"

    .line 504
    invoke-direct {v1, v0}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->fail(Ljava/lang/String;)V
    :try_end_d6
    .catchall {:try_start_ca .. :try_end_d6} :catchall_c7

    .line 506
    :goto_d6
    iget-object v0, v1, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->starting:Ljava/util/concurrent/atomic/AtomicBoolean;

    invoke-virtual {v0, v5}, Ljava/util/concurrent/atomic/AtomicBoolean;->set(Z)V

    return-void

    :goto_dc
    iget-object v2, v1, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->starting:Ljava/util/concurrent/atomic/AtomicBoolean;

    invoke-virtual {v2, v5}, Ljava/util/concurrent/atomic/AtomicBoolean;->set(Z)V

    .line 507
    throw v0
.end method

.method private runPostMatch(I)V
    .registers 5

    .line 86
    iget-boolean v0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->closed:Z

    if-nez v0, :cond_1f

    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->web:Landroid/webkit/WebView;

    if-eqz v0, :cond_1f

    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "window.MlLeague&&window.MlLeague.postMatch&&window.MlLeague.postMatch("

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1, p1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    const-string p1, ")"

    invoke-virtual {v1, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1

    const/4 v1, 0x0

    invoke-virtual {v0, p1, v1}, Landroid/webkit/WebView;->evaluateJavascript(Ljava/lang/String;Landroid/webkit/ValueCallback;)V

    :cond_1f
    return-void
.end method

.method static saveTransferDone(Ljava/lang/String;Ljava/lang/String;)V
    .registers 5

    .line 100
    sget-object v0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->active:Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;

    if-eqz v0, :cond_37

    .line 101
    iget-boolean v1, v0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->closed:Z

    if-eqz v1, :cond_9

    goto :goto_37

    .line 102
    :cond_9
    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "window.MlLeague&&window.MlLeague.saveTransferDone&&window.MlLeague.saveTransferDone("

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    if-nez p0, :cond_14

    const-string p0, ""

    .line 103
    :cond_14
    invoke-static {p0}, Lorg/json/JSONObject;->quote(Ljava/lang/String;)Ljava/lang/String;

    move-result-object p0

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string p0, ","

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    if-nez p1, :cond_24

    const-string p1, "{}"

    :cond_24
    invoke-static {p1}, Lorg/json/JSONObject;->quote(Ljava/lang/String;)Ljava/lang/String;

    move-result-object p0

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string p0, ")"

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    .line 102
    invoke-direct {v0, p0}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->js(Ljava/lang/String;)V

    :cond_37
    :goto_37
    return-void
.end method

.method private serve(Landroid/webkit/WebResourceRequest;)Landroid/webkit/WebResourceResponse;
    .registers 12

    const-string v0, "ml-league/"

    .line 233
    invoke-interface {p1}, Landroid/webkit/WebResourceRequest;->getUrl()Landroid/net/Uri;

    move-result-object v1

    .line 234
    invoke-virtual {v1}, Landroid/net/Uri;->getPath()Ljava/lang/String;

    move-result-object v2

    const-string v3, "ml-league.local"

    .line 235
    invoke-virtual {v1}, Landroid/net/Uri;->getHost()Ljava/lang/String;

    move-result-object v4

    invoke-virtual {v3, v4}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v3

    const-string v4, "Not found"

    const/16 v5, 0x194

    const-string v6, "text/plain"

    if-eqz v3, :cond_170

    if-eqz v2, :cond_170

    const-string v3, ".."

    invoke-virtual {v2, v3}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z

    move-result v3

    if-nez v3, :cond_170

    const-string v3, "\\"

    invoke-virtual {v2, v3}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z

    move-result v3

    if-eqz v3, :cond_30

    goto/16 :goto_170

    :cond_30
    :try_start_30
    const-string v3, "/"

    .line 238
    invoke-virtual {v2, v3}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v3

    if-eqz v3, :cond_3a

    const-string v2, "/index.html"

    :cond_3a
    const-string v3, "/fonts.css"

    .line 239
    invoke-virtual {v2, v3}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v3

    const/16 v7, 0xc8

    if-eqz v3, :cond_4e

    const-string p1, "text/css"

    const/4 v0, 0x0

    new-array v0, v0, [B

    invoke-static {p1, v7, v0}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->response(Ljava/lang/String;I[B)Landroid/webkit/WebResourceResponse;

    move-result-object p1

    return-object p1

    :cond_4e
    const-string v3, "/i18n.js"

    .line 240
    invoke-virtual {v2, v3}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v3

    if-eqz v3, :cond_65

    const-string p1, "application/javascript"

    const-string v0, "window.LANG_PACKS={};"

    sget-object v1, Ljava/nio/charset/StandardCharsets;->UTF_8:Ljava/nio/charset/Charset;

    invoke-virtual {v0, v1}, Ljava/lang/String;->getBytes(Ljava/nio/charset/Charset;)[B

    move-result-object v0

    invoke-static {p1, v7, v0}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->response(Ljava/lang/String;I[B)Landroid/webkit/WebResourceResponse;

    move-result-object p1

    return-object p1

    :cond_65
    const-string v3, "/api/"

    .line 241
    invoke-virtual {v2, v3}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result v3

    if-eqz v3, :cond_76

    invoke-interface {p1}, Landroid/webkit/WebResourceRequest;->getMethod()Ljava/lang/String;

    move-result-object p1

    invoke-direct {p0, p1, v1}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->api(Ljava/lang/String;Landroid/net/Uri;)Landroid/webkit/WebResourceResponse;

    move-result-object p1

    return-object p1

    :cond_76
    const-string p1, "/img/emblem/"

    .line 242
    invoke-virtual {v2, p1}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result p1
    :try_end_7c
    .catch Ljava/io/IOException; {:try_start_30 .. :try_end_7c} :catch_165

    const-string v1, "\\.png$"

    const/16 v3, 0xc

    const-string v8, "image/png"

    const-string v9, ""

    if-eqz p1, :cond_a6

    .line 243
    :try_start_86
    invoke-virtual {v2, v3}, Ljava/lang/String;->substring(I)Ljava/lang/String;

    move-result-object p1

    invoke-virtual {p1, v1, v9}, Ljava/lang/String;->replaceAll(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object p1

    invoke-direct {p0, p1}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->crest(Ljava/lang/String;)[B

    move-result-object p1

    if-eqz p1, :cond_99

    .line 244
    invoke-static {v8, v7, p1}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->response(Ljava/lang/String;I[B)Landroid/webkit/WebResourceResponse;

    move-result-object p1

    goto :goto_a5

    :cond_99
    const-string p1, "No crest"

    sget-object v0, Ljava/nio/charset/StandardCharsets;->UTF_8:Ljava/nio/charset/Charset;

    invoke-virtual {p1, v0}, Ljava/lang/String;->getBytes(Ljava/nio/charset/Charset;)[B

    move-result-object p1

    invoke-static {v6, v5, p1}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->response(Ljava/lang/String;I[B)Landroid/webkit/WebResourceResponse;

    move-result-object p1

    :goto_a5
    return-object p1

    :cond_a6
    const-string p1, "/img/player/"

    .line 246
    invoke-virtual {v2, p1}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result p1

    if-eqz p1, :cond_ce

    .line 247
    invoke-virtual {v2, v3}, Ljava/lang/String;->substring(I)Ljava/lang/String;

    move-result-object p1

    invoke-virtual {p1, v1, v9}, Ljava/lang/String;->replaceAll(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object p1

    invoke-direct {p0, p1}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->playerFace(Ljava/lang/String;)[B

    move-result-object p1

    if-eqz p1, :cond_c1

    .line 248
    invoke-static {v8, v7, p1}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->response(Ljava/lang/String;I[B)Landroid/webkit/WebResourceResponse;

    move-result-object p1

    goto :goto_cd

    :cond_c1
    const-string p1, "No portrait"

    sget-object v0, Ljava/nio/charset/StandardCharsets;->UTF_8:Ljava/nio/charset/Charset;

    invoke-virtual {p1, v0}, Ljava/lang/String;->getBytes(Ljava/nio/charset/Charset;)[B

    move-result-object p1

    invoke-static {v6, v5, p1}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->response(Ljava/lang/String;I[B)Landroid/webkit/WebResourceResponse;

    move-result-object p1

    :goto_cd
    return-object p1

    :cond_ce
    const-string p1, "/img/card/"

    .line 250
    invoke-virtual {v2, p1}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result p1

    if-eqz p1, :cond_13a

    const/16 p1, 0xa

    .line 252
    invoke-virtual {v2, p1}, Ljava/lang/String;->substring(I)Ljava/lang/String;

    move-result-object p1

    const-string v0, ".webm"

    .line 253
    invoke-virtual {p1, v0}, Ljava/lang/String;->endsWith(Ljava/lang/String;)Z

    move-result v0
    :try_end_e2
    .catch Ljava/io/IOException; {:try_start_86 .. :try_end_e2} :catch_165

    const-string v1, "video"

    if-eqz v0, :cond_e8

    move-object v0, v1

    goto :goto_f5

    :cond_e8
    :try_start_e8
    const-string v0, ".over.png"

    invoke-virtual {p1, v0}, Ljava/lang/String;->endsWith(Ljava/lang/String;)Z

    move-result v0

    if-eqz v0, :cond_f3

    const-string v0, "overlay"

    goto :goto_f5

    :cond_f3
    const-string v0, "card"

    :goto_f5
    const-string v2, "(\\.over)?\\.(png|webm)$"

    .line 254
    invoke-virtual {p1, v2, v9}, Ljava/lang/String;->replaceAll(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object p1

    .line 255
    invoke-direct {p0, p1, v0}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->cardArt(Ljava/lang/String;Ljava/lang/String;)[B

    move-result-object v2

    if-eqz v2, :cond_10e

    .line 256
    invoke-virtual {v1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result p1

    if-eqz p1, :cond_109

    const-string v8, "video/webm"

    :cond_109
    invoke-static {v8, v7, v2}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->response(Ljava/lang/String;I[B)Landroid/webkit/WebResourceResponse;

    move-result-object p1

    return-object p1

    .line 257
    :cond_10e
    sget-object v1, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->artWhy:Ljava/util/Map;

    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v0, ":"

    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1

    invoke-interface {v1, p1}, Ljava/util/Map;->get(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object p1

    check-cast p1, Ljava/lang/String;

    if-eqz p1, :cond_12d

    goto :goto_12f

    :cond_12d
    const-string p1, "No card art"

    .line 258
    :goto_12f
    sget-object v0, Ljava/nio/charset/StandardCharsets;->UTF_8:Ljava/nio/charset/Charset;

    invoke-virtual {p1, v0}, Ljava/lang/String;->getBytes(Ljava/nio/charset/Charset;)[B

    move-result-object p1

    invoke-static {v6, v5, p1}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->response(Ljava/lang/String;I[B)Landroid/webkit/WebResourceResponse;

    move-result-object p1

    return-object p1

    .line 260
    :cond_13a
    iget-object p1, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->activity:Landroid/app/Activity;

    invoke-virtual {p1}, Landroid/app/Activity;->getAssets()Landroid/content/res/AssetManager;

    move-result-object p1

    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1, v0}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    const/4 v0, 0x1

    invoke-virtual {v2, v0}, Ljava/lang/String;->substring(I)Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-virtual {p1, v0}, Landroid/content/res/AssetManager;->open(Ljava/lang/String;)Ljava/io/InputStream;

    move-result-object p1

    const v0, 0xb71b00

    invoke-static {p1, v0}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->read(Ljava/io/InputStream;I)[B

    move-result-object p1

    .line 261
    invoke-static {v2}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->mime(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    invoke-static {v0, v7, p1}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->response(Ljava/lang/String;I[B)Landroid/webkit/WebResourceResponse;

    move-result-object p1
    :try_end_164
    .catch Ljava/io/IOException; {:try_start_e8 .. :try_end_164} :catch_165

    return-object p1

    .line 263
    :catch_165
    sget-object p1, Ljava/nio/charset/StandardCharsets;->UTF_8:Ljava/nio/charset/Charset;

    invoke-virtual {v4, p1}, Ljava/lang/String;->getBytes(Ljava/nio/charset/Charset;)[B

    move-result-object p1

    invoke-static {v6, v5, p1}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->response(Ljava/lang/String;I[B)Landroid/webkit/WebResourceResponse;

    move-result-object p1

    return-object p1

    .line 236
    :cond_170
    :goto_170
    sget-object p1, Ljava/nio/charset/StandardCharsets;->UTF_8:Ljava/nio/charset/Charset;

    invoke-virtual {v4, p1}, Ljava/lang/String;->getBytes(Ljava/nio/charset/Charset;)[B

    move-result-object p1

    invoke-static {v6, v5, p1}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->response(Ljava/lang/String;I[B)Landroid/webkit/WebResourceResponse;

    move-result-object p1

    return-object p1
.end method

.method public static show(Landroid/app/Activity;)V
    .registers 3

    .line 65
    sget-object v0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->active:Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;

    if-eqz v0, :cond_1e

    iget-object v1, v0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->activity:Landroid/app/Activity;

    if-ne v1, p0, :cond_1e

    iget-boolean v0, v0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->closed:Z

    if-nez v0, :cond_1e

    .line 66
    sget-object p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->active:Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;

    iget-object p0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->dialog:Landroid/app/Dialog;

    if-eqz p0, :cond_1d

    invoke-virtual {p0}, Landroid/app/Dialog;->isShowing()Z

    move-result p0

    if-nez p0, :cond_1d

    sget-object p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->active:Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;

    invoke-direct {p0}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->showDialog()V

    :cond_1d
    return-void

    .line 69
    :cond_1e
    sget-object v0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->active:Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;

    if-eqz v0, :cond_25

    invoke-direct {v0}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->dispose()V

    .line 70
    :cond_25
    new-instance v0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;

    invoke-direct {v0, p0}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;-><init>(Landroid/app/Activity;)V

    sput-object v0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->active:Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;

    .line 71
    invoke-direct {v0}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->open()V

    return-void
.end method

.method private showDialog()V
    .registers 2

    .line 213
    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->dialog:Landroid/app/Dialog;

    if-nez v0, :cond_5

    return-void

    .line 214
    :cond_5
    invoke-virtual {v0}, Landroid/app/Dialog;->show()V

    const-string v0, "window.MlLeague&&window.MlLeague.setHidden&&window.MlLeague.setHidden(false)"

    .line 215
    invoke-direct {p0, v0}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->js(Ljava/lang/String;)V

    return-void
.end method

.method private showPageHint(Ljava/lang/String;)V
    .registers 4

    const-string v0, "match"

    .line 468
    invoke-virtual {v0, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result p1

    if-eqz p1, :cond_b

    const-string p1, "\u8bf7\u5148\u56de\u5230\u300c\u6bd4\u8d5b\u300d\u9875\uff1a\u5728\u90a3\u91cc\u5207\u6362\u5230\u5927\u5e08\u8054\u8d5b\u9635\u5bb9\u540e\u81ea\u52a8\u8fdb\u5165 AI Division \u5f00\u8d5b"

    goto :goto_d

    :cond_b
    const-string p1, "\u8bf7\u8fdb\u5165\u300c\u6bd4\u8d5b\u300d\u2192 AI Division \u4e3b\u9875\uff0c\u8fdb\u5165\u540e\u81ea\u52a8\u5f00\u8d5b"

    .line 470
    :goto_d
    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->activity:Landroid/app/Activity;

    new-instance v1, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel$$ExternalSyntheticLambda8;

    invoke-direct {v1, p0, p1}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel$$ExternalSyntheticLambda8;-><init>(Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;Ljava/lang/String;)V

    invoke-virtual {v0, v1}, Landroid/app/Activity;->runOnUiThread(Ljava/lang/Runnable;)V

    return-void
.end method

.method public static showPostMatch(Landroid/app/Activity;I)V
    .registers 3

    .line 79
    invoke-static {p0}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->show(Landroid/app/Activity;)V

    .line 80
    sget-object p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->active:Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;

    if-eqz p0, :cond_18

    iget-boolean p0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->closed:Z

    if-eqz p0, :cond_c

    goto :goto_18

    .line 81
    :cond_c
    sget-object p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->active:Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;

    iget-boolean v0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->pageReady:Z

    if-eqz v0, :cond_16

    invoke-direct {p0, p1}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->runPostMatch(I)V

    goto :goto_18

    .line 82
    :cond_16
    iput p1, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->pendingPostMatch:I

    :cond_18
    :goto_18
    return-void
.end method

.method private toast(Ljava/lang/String;)V
    .registers 4

    if-nez p1, :cond_3

    return-void

    .line 589
    :cond_3
    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->activity:Landroid/app/Activity;

    new-instance v1, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel$$ExternalSyntheticLambda9;

    invoke-direct {v1, p0, p1}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel$$ExternalSyntheticLambda9;-><init>(Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;Ljava/lang/String;)V

    invoke-virtual {v0, v1}, Landroid/app/Activity;->runOnUiThread(Ljava/lang/Runnable;)V

    return-void
.end method


# virtual methods
.method synthetic lambda$failText$8$org-efootballrevival-runtimeprobe-MlLeaguePanel()V
    .registers 2

    .line 535
    iget-boolean v0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->closed:Z

    if-nez v0, :cond_11

    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->dialog:Landroid/app/Dialog;

    if-eqz v0, :cond_11

    invoke-virtual {v0}, Landroid/app/Dialog;->isShowing()Z

    move-result v0

    if-nez v0, :cond_11

    invoke-direct {p0}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->showDialog()V

    :cond_11
    return-void
.end method

.method synthetic lambda$hide$3$org-efootballrevival-runtimeprobe-MlLeaguePanel()V
    .registers 2

    .line 202
    iget-boolean v0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->closed:Z

    if-nez v0, :cond_b

    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->dialog:Landroid/app/Dialog;

    if-eqz v0, :cond_b

    invoke-direct {p0}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->hideDialog()V

    :cond_b
    return-void
.end method

.method synthetic lambda$js$4$org-efootballrevival-runtimeprobe-MlLeaguePanel(Ljava/lang/String;)V
    .registers 4

    .line 438
    iget-boolean v0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->closed:Z

    if-nez v0, :cond_c

    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->web:Landroid/webkit/WebView;

    if-eqz v0, :cond_c

    const/4 v1, 0x0

    invoke-virtual {v0, p1, v1}, Landroid/webkit/WebView;->evaluateJavascript(Ljava/lang/String;Landroid/webkit/ValueCallback;)V

    :cond_c
    return-void
.end method

.method synthetic lambda$open$0$org-efootballrevival-runtimeprobe-MlLeaguePanel(Landroid/view/View;Landroid/view/WindowInsets;)Landroid/view/WindowInsets;
    .registers 5

    .line 149
    invoke-static {p2}, Lorg/efootballrevival/runtimeprobe/InsetsCompat;->safe(Landroid/view/WindowInsets;)[I

    move-result-object v0

    const/4 v1, 0x0

    .line 150
    invoke-virtual {p1, v1, v1, v1, v1}, Landroid/view/View;->setPadding(IIII)V

    .line 151
    aget p1, v0, v1

    const/4 v1, 0x2

    aget v0, v0, v1

    invoke-direct {p0, p1, v0}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->pushSafe(II)V

    .line 152
    invoke-static {p2}, Lorg/efootballrevival/runtimeprobe/InsetsCompat;->consumeBars(Landroid/view/WindowInsets;)Landroid/view/WindowInsets;

    move-result-object p1

    return-object p1
.end method

.method synthetic lambda$open$1$org-efootballrevival-runtimeprobe-MlLeaguePanel(Landroid/content/DialogInterface;ILandroid/view/KeyEvent;)Z
    .registers 4

    .line 0
    const/4 p1, 0x4

    if-ne p2, p1, :cond_e

    .line 159
    invoke-virtual {p3}, Landroid/view/KeyEvent;->getAction()I

    move-result p1

    const/4 p2, 0x1

    if-ne p1, p2, :cond_d

    invoke-direct {p0}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->hide()V

    :cond_d
    return p2

    :cond_e
    const/4 p1, 0x0

    return p1
.end method

.method synthetic lambda$open$2$org-efootballrevival-runtimeprobe-MlLeaguePanel(Landroid/content/DialogInterface;)V
    .registers 2

    .line 164
    iget-boolean p1, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->closed:Z

    if-nez p1, :cond_7

    invoke-direct {p0}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->dispose()V

    :cond_7
    return-void
.end method

.method synthetic lambda$passTouches$5$org-efootballrevival-runtimeprobe-MlLeaguePanel(Z)V
    .registers 3

    .line 443
    iget-boolean v0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->closed:Z

    if-nez v0, :cond_26

    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->dialog:Landroid/app/Dialog;

    if-eqz v0, :cond_26

    invoke-virtual {v0}, Landroid/app/Dialog;->getWindow()Landroid/view/Window;

    move-result-object v0

    if-nez v0, :cond_f

    goto :goto_26

    :cond_f
    const/16 v0, 0x10

    if-eqz p1, :cond_1d

    .line 444
    iget-object p1, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->dialog:Landroid/app/Dialog;

    invoke-virtual {p1}, Landroid/app/Dialog;->getWindow()Landroid/view/Window;

    move-result-object p1

    invoke-virtual {p1, v0}, Landroid/view/Window;->addFlags(I)V

    goto :goto_26

    .line 445
    :cond_1d
    iget-object p1, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->dialog:Landroid/app/Dialog;

    invoke-virtual {p1}, Landroid/app/Dialog;->getWindow()Landroid/view/Window;

    move-result-object p1

    invoke-virtual {p1, v0}, Landroid/view/Window;->clearFlags(I)V

    :cond_26
    :goto_26
    return-void
.end method

.method synthetic lambda$ready$7$org-efootballrevival-runtimeprobe-MlLeaguePanel()V
    .registers 3

    .line 512
    iget-boolean v0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->closed:Z

    if-nez v0, :cond_14

    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->dialog:Landroid/app/Dialog;

    if-eqz v0, :cond_14

    invoke-virtual {v0}, Landroid/app/Dialog;->getWindow()Landroid/view/Window;

    move-result-object v0

    const/16 v1, 0x10

    invoke-virtual {v0, v1}, Landroid/view/Window;->clearFlags(I)V

    invoke-direct {p0}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->hideDialog()V

    :cond_14
    return-void
.end method

.method synthetic lambda$showPageHint$6$org-efootballrevival-runtimeprobe-MlLeaguePanel(Ljava/lang/String;)V
    .registers 4

    .line 471
    iget-boolean v0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->closed:Z

    if-nez v0, :cond_16

    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->dialog:Landroid/app/Dialog;

    if-nez v0, :cond_9

    goto :goto_16

    .line 472
    :cond_9
    invoke-direct {p0}, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->hideDialog()V

    .line 473
    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->activity:Landroid/app/Activity;

    const/4 v1, 0x1

    invoke-static {v0, p1, v1}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;

    move-result-object p1

    invoke-virtual {p1}, Landroid/widget/Toast;->show()V

    :cond_16
    :goto_16
    return-void
.end method

.method synthetic lambda$toast$9$org-efootballrevival-runtimeprobe-MlLeaguePanel(Ljava/lang/String;)V
    .registers 4

    .line 589
    iget-object v0, p0, Lorg/efootballrevival/runtimeprobe/MlLeaguePanel;->activity:Landroid/app/Activity;

    const/4 v1, 0x1

    invoke-static {v0, p1, v1}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;

    move-result-object p1

    invoke-virtual {p1}, Landroid/widget/Toast;->show()V

    return-void
.end method
