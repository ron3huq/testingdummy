"use strict";
/* Launcher UI. Talks to the host only through AndroidLauncher.call(id, action, json);
   every reply arrives as Launcher.deliver(id, json). Display text is translated by the host (UiStrings). */
(() => {
  const $ = id => document.getElementById(id);
  const pending = new Map();
  const words = new Map(Object.entries(window.DiyEnglishWords || {}));
  let seq = 0, busy = false, info = {gameEntered: false, version: "", language: "en"}, view = "home";
  const handlers = {};
  // How far the status bar / display cutout reaches into the page (CSS px, pushed by the host).
  function applyInsets(top, right, left) {
    const s = document.documentElement.style;
    s.setProperty("--safe-top", (Number(top) || 0) + "px");
    s.setProperty("--safe-right", (Number(right) || 0) + "px");
    s.setProperty("--safe-left", (Number(left) || 0) + "px");
  }

  window.Launcher = {
    deliver(id, json) {
      const p = pending.get(id); if (!p) return; pending.delete(id);
      try { const v = JSON.parse(json); v && v.error ? p.reject(new Error(v.error)) : p.resolve(v); } catch (e) { p.reject(e); }
    },
    progress(text) { setProgress(text); },
    insets(top, right, left) { applyInsets(top, right, left); },
    event(name, data) { if (handlers[name]) handlers[name](data || {}); },
    back() {
      if (!$("scrim").hidden) { closeSheet(false); return true; }
      if (busy) return true;
      if (view === "players" && window.EditorUI && window.EditorUI.back()) return true;
      if (view !== "home") { show("home"); return true; }
      return false;
    }
  };

  // Text that is composed at run time is translated by the host in batches; listeners re-apply it afterwards.
  const pendingTx = new Set(), textListeners = [];
  let txTimer = 0;
  function needText(s) {
    if (!s || words.has(s) || info.language === "zh-CN") return;
    pendingTx.add(s);
    if (!txTimer) txTimer = setTimeout(async () => {
      const list = [...pendingTx]; pendingTx.clear(); txTimer = 0;
      await translate(list); textListeners.forEach(f => f());
    }, 0);
  }

  function call(action, args) {
    return new Promise((resolve, reject) => {
      const id = String(++seq); pending.set(id, {resolve, reject});
      try { AndroidLauncher.call(id, action, JSON.stringify(args || {})); } catch (e) { pending.delete(id); reject(e); }
    });
  }
  const t = s => info.language !== "en" ? window.UiLocalization.t(s) : words.get(s) || s;
  function applyLanguage(code) { window.UiLocalization.setLanguage(code); window.UiLocalization.applyDocument(); }

  async function translate(list) {
    if (info.language !== "en") { list.forEach(s => words.set(s, window.UiLocalization.t(s))); return; }
    const need = [...new Set(list)].filter(s => s && !words.has(s));
    if (!need.length) return;
    try { const r = await call("translate", {items: need}); need.forEach((s, i) => words.set(s, r.items[i] || s)); }
    catch (e) { need.forEach(s => words.set(s, s)); }
  }
  async function applyText() {
    const nodes = [...document.querySelectorAll("[data-t]")];
    nodes.forEach(n => { n.dataset.t = n.dataset.t.replace(/\\n/g, "\n"); });
    await translate(nodes.map(n => n.dataset.t).concat(["语言 / Language", "离线游戏 · 本地存档", "管理本机进度。导入前会保留备份。", "存档管理器", "取消", "确认", "知道了", "返回", "稍后", "进入游戏"]));
    nodes.forEach(n => {
      const s = t(n.dataset.t);
      // Tiles are short labels: break at the separator instead of mid-word.
      n.textContent = n.parentElement.classList.contains("tile") ? s.replace(/\s·\s/, "\n").replace(/（/, "\n（") : s;
    });
    $("title").textContent = "Private Football";
    $("subtitle").textContent = view === "saves" ? t("管理本机进度。导入前会保留备份。") : "Your players. Your game.";
  }

  function setStatus(text) { $("status").textContent = text || ""; }
  function setProgress(text) { $("progress").textContent = text || ""; }
  function setBusy(on) {
    busy = on; $("meter").classList.toggle("busy", on);
    // The players page manages its own button states.
    document.querySelectorAll(".page:not(#players) button").forEach(b => { b.disabled = on || (info.gameEntered && view === "saves"); });
    document.querySelectorAll("#dock button, #lang").forEach(b => { b.disabled = on; });
  }
  async function work(fn, opts) {
    if (busy) return;
    setBusy(true); setProgress(t("正在处理，请稍候…"));
    try { const msg = await fn(); if (opts && opts.status) setStatus(msg); setProgress(opts && opts.status ? "" : msg || ""); }
    catch (e) { if (opts && opts.status) setStatus(t("存档读取未完成，请返回后重试。")); setProgress(e.message || t("操作未完成，请重试。")); }
    finally { setBusy(false); }
  }

  function sheet(title, body, buttons, extra) {
    return new Promise(resolve => {
      $("sheet-title").textContent = title; $("sheet-body").textContent = body || "";
      const ex = $("sheet-extra"); ex.replaceChildren(); if (extra) ex.appendChild(extra);
      const row = $("sheet-actions"); row.replaceChildren();
      buttons.forEach(b => {
        const el = document.createElement("button"); el.type = "button"; el.className = "btn" + (b.kind ? " " + b.kind : ""); el.textContent = b.label;
        el.addEventListener("click", () => { closeSheet(b.value); });
        row.appendChild(el);
      });
      sheet.resolve = resolve; $("scrim").hidden = false;
    });
  }
  function closeSheet(value) { $("scrim").hidden = true; const r = sheet.resolve; sheet.resolve = null; if (r) r(value); }
  const confirmSheet = (title, body, ok) => sheet(t(title), t(body), [{label: t("取消"), value: false}, {label: t(ok || "确认"), value: true, kind: "primary"}]);
  const notice = (body) => sheet("Private Football", t(body), [{label: t("知道了"), value: true, kind: "primary"}]);

  function show(next) {
    view = next;
    document.querySelectorAll(".page").forEach(p => { p.hidden = p.id !== next; });
    document.querySelectorAll("#dock button").forEach(b => b.classList.toggle("on", b.dataset.page === next));
    applyText(); setBusy(false);
    if (next === "players" && window.EditorUI) window.EditorUI.enter();
    if (next === "saves") loadSummary(); else refreshStatus();
    if (next === "home") renderHome();
  }

  // Home: save summary (read-only, skipped once the game is running), recent players, shortcuts.
  let summaryBusy = false;
  function paintHomeRecent() {
    const S = window.EditorUI && window.EditorUI.Store, box = $("home-recent"), row = $("home-recent-row");
    if (!S || !box) return;
    const items = S.recent.slice(0, 8);
    box.hidden = items.length === 0; row.replaceChildren();
    items.forEach(e => {
      const b = document.createElement("button"); b.type = "button"; b.className = "home-recent-card"; b.setAttribute("aria-label", e.name);
      const art = window.EditorUI.U.portrait({id: e.id, portrait_revision: 0}, 0); art.classList.add("ed-art");
      const ovr = document.createElement("span"); ovr.className = "hr-ovr"; ovr.textContent = String(e.overall || "");
      const nm = document.createElement("span"); nm.className = "hr-nm"; nm.textContent = e.name;
      b.append(art, ovr, nm);
      b.addEventListener("click", () => { if (busy) return; show("players"); window.EditorUI.openEntry(e); });
      row.appendChild(b);
    });
  }
  async function renderHome() {
    const S = window.EditorUI && window.EditorUI.Store;
    if (S) { await S.load(); paintHomeRecent(); }
    if (info.gameEntered || summaryBusy) return;
    summaryBusy = true;
    try { const r = await call("summary"); if (view === "home") { $("home-sum-text").textContent = r.text || ""; $("home-sum").hidden = !r.text; } }
    catch (e) { $("home-sum").hidden = true; }
    finally { summaryBusy = false; }
  }
  async function refreshStatus() {
    try { const r = await call("inspect"); if (view !== "saves") setStatus(r.text); } catch (e) { setStatus(t("资源缺失 · 请安装配套离线资源包后重试。")); }
  }
  async function loadSummary() {
    if (info.gameEntered) { setStatus(t("游戏已经进入，请先关闭游戏并重新打开。")); setBusy(false); return; }
    setStatus(t("正在读取存档…"));
    work(async () => (await call("summary")).text, {status: true});
  }

  async function prepare(repair) {
    if (busy) return;
    setBusy(true); setProgress(t("正在检查本地资源…"));
    try {
      const r = await call("prepare", {repair});
      if (r.installed) {
        const go = await sheet(t("资源导入完成"), t("资源已保存到主游戏，后续覆盖更新无需再次下载。现在可以卸载“73efootball离线资源”；请保留主游戏数据。"),
          [{label: t("稍后"), value: false}, {label: t("进入游戏"), value: true, kind: "primary"}]);
        if (!go) { setBusy(false); setProgress(""); return; }
      }
      await call("launch");
    } catch (e) { setBusy(false); setProgress(e.message || t("准备未完成，请重试。已有存档保留。")); }
  }

  async function cleanStorage() {
    if (info.gameEntered) { notice("请完全退出游戏并重新打开，在进入游戏前清理。"); return; }
    if (busy) return;
    setBusy(true); setProgress(t("正在处理，请稍候…"));
    try {
      const r = await call("storagePreview");
      setBusy(false); setProgress(r.message || "");
      if (r.recovery) {
        if (await confirmSheet("恢复中断的清理", "上次清理未结束。将恢复尚未确认删除的暂存数据，或完成上次已确认的删除，再重新扫描。", "确认"))
          work(async () => (await call("storageRecover")).message);
        return;
      }
      if (!await sheet(t("存储占用与清理预览"), r.text, [{label: t("返回"), value: false}, {label: t("选择清理项目"), value: true, kind: "primary"}])) return;
      const list = document.createElement("div"), boxes = [];
      r.groups.forEach(g => {
        const row = document.createElement("label"); row.className = "pick" + (g.selected ? " on" : "");
        const box = document.createElement("input"); box.type = "checkbox"; box.checked = !!g.selected; boxes.push([g.id, box]);
        box.addEventListener("change", () => row.classList.toggle("on", box.checked));
        const name = document.createElement("span"); name.textContent = g.label;
        row.append(box, name); list.appendChild(row);
      });
      if (!await sheet(t("选择清理项目"), "", [{label: t("取消"), value: false}, {label: t("确认清理"), value: true, kind: "primary"}], list)) return;
      const ids = boxes.filter(([, b]) => b.checked).map(([id]) => id);
      if (ids.includes("backups") && !await confirmSheet("永久删除全部历史备份？", "将删除全部历史发布备份（包括最新一份）及已确认闲置的恢复副本。之后不能用这些备份回滚；当前发布资源、作品和存档保留。此操作不可撤销。", "确认")) return;
      work(async () => (await call("storageClean", {token: r.token, ids})).message);
    } catch (e) { setBusy(false); setProgress(e.message || t("操作未完成，请重试。")); }
  }

  async function dedupe() {
    if (busy) return;
    setBusy(true); setProgress(t("正在处理，请稍候…"));
    try {
      const r = await call("dedupePreview"); setBusy(false); setProgress(r.count ? "" : r.text);
      if (r.count && await confirmSheet("清理重复球员预览", r.text, "确认")) work(async () => (await call("dedupeDelete", {token: r.token})).message);
    } catch (e) { setBusy(false); setProgress(e.message || t("操作未完成，请重试。")); }
  }

  handlers.message = d => { setBusy(false); setProgress(d.text); };
  handlers.importPicked = async () => {
    if (await confirmSheet("导入存档", "将替换当前进度，导入前自动备份；资源文件保留。确定导入？", "确认")) work(async () => (await call("importCommit")).message);
    else call("importCancel").catch(() => {});
  };

  function bind() {
    $("private-diagnostics").addEventListener("click",()=>call("editor",{op:"privateTool",payload:{tool:"diagnostics"}}).catch(e=>setProgress(e.message)));
    $("private-transfer").addEventListener("click", () => window.PrivateTransfer.enter());
    $("native-launcher").addEventListener("click", () => { if (!busy) call("nativeLauncher").catch(e => setProgress(e.message)); });
    $("native-editor").addEventListener("click", () => call("openPanel", {name: "editor"}).catch(e => setProgress(e.message)));
    $("enter").addEventListener("click", () => prepare(false));
    $("repair").addEventListener("click", async () => { if (await confirmSheet("修复资源", "仅在资源异常时使用，将完整校验并修复资源。存档保留；缺失文件可能需要离线资源包。", "确认")) prepare(true); });
    document.querySelectorAll("#dock button").forEach(b => b.addEventListener("click", () => { if (!busy && b.dataset.page !== view) show(b.dataset.page); }));
    $("repair2").addEventListener("click", () => $("repair").click());
    $("open-designer").addEventListener("click", () => info.gameEntered ? notice("请关闭游戏并重新打开，再使用制卡器。") : call("openPanel", {name: "designer"}));
    $("open-storage").addEventListener("click", cleanStorage);
    $("max-level").addEventListener("click", async () => {
      if (await confirmSheet("未满级球员升级并加点", "仅将未满级的已持有球员（含储备）升至等级上限，并按位置重新自动分配能力点，覆盖这些球员原有手动加点；已满级球员完全跳过，保留现有加点和剩余点数。技能、增能与阵容保留。操作前自动备份。", "确认"))
        work(async () => (await call("maxLevel")).message);
    });
    $("dedupe").addEventListener("click", dedupe);
    $("export").addEventListener("click", () => work(async () => (await call("exportSave")).message));
    $("import").addEventListener("click", () => call("importPick").catch(e => setProgress(e.message)));
    document.querySelectorAll(".quick").forEach(b => b.addEventListener("click", () => { if (!busy) show(b.dataset.go); }));
    if (window.EditorUI && window.EditorUI.Store) window.EditorUI.Store.onChange(paintHomeRecent);
    $("scrim").addEventListener("click", e => { if (e.target === $("scrim")) closeSheet(false); });
  }

  // Shared with the player editor modules (editor-*.js).
  window.LauncherApi = {
    call, sheet, closeSheet, confirmSheet, notice,
    cache: words, need: needText, onText: f => textListeners.push(f),
    lang: () => info.language, gameEntered: () => info.gameEntered,
    progress: setProgress,
    meter: on => $("meter").classList.toggle("busy", !!on)
  };

  // Browser preview: with no Android host, load the stand-in bridge that lives outside the APK assets.
  function loadMock() {
    return new Promise(resolve => {
      const s = document.createElement("script"); s.src = "../../../../preview/mock-bridge.js";
      s.onload = s.onerror = () => resolve(); document.head.appendChild(s);
    });
  }

  (async () => {
    if (typeof AndroidLauncher === "undefined") await loadMock();
    try { if (typeof AndroidLauncher.insets === "function") { const p = String(AndroidLauncher.insets()).split(",").map(Number); applyInsets(p[0], p[1], p[2]); } } catch (e) { /* the host pushes it later */ }
    bind();
    try { info = Object.assign(info, await call("info")); } catch (e) { /* keep defaults */ }
    $("ver").textContent = (info.versionLabel || "").replace(/^73efootball\s*\/\s*/, "");
    info.language = "en";
    applyLanguage("en");
    await applyText(); show("home");
    window.LauncherStartup.ready();
  })().catch(error => window.LauncherStartup.fail(error && error.message));
})();
