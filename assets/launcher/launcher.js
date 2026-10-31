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
  const t = s => window.UiLocalization.display(String(s ?? ""));
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
    await translate(nodes.map(n => n.dataset.t).concat(["English", "Offline game · Local save", "Manage local progress. Imports are backed up first.", "Save Manager", "Cancel", "Confirm", "OK", "Back", "Later", "Enter Game"]));
    nodes.forEach(n => {
      const s = t(n.dataset.t);
      // Tiles are short labels: break at the separator instead of mid-word.
      n.textContent = n.parentElement.classList.contains("tile") ? s.replace(/\s·\s/, "\n").replace(/（/, "\n（") : s;
    });
    $("title").textContent = "Private Football";
    $("subtitle").textContent = view === "saves" ? t("Manage local progress. Imports are backed up first.") : "Your players. Your game.";
  }

  function setStatus(text) { $("status").textContent = t(text || ""); }
  function setProgress(text) { $("progress").textContent = t(text || ""); }
  function setBusy(on) {
    busy = on; $("meter").classList.toggle("busy", on);
    // The players page manages its own button states.
    document.querySelectorAll(".page:not(#players) button").forEach(b => { b.disabled = on || (info.gameEntered && view === "saves"); });
    document.querySelectorAll("#dock button, #lang").forEach(b => { b.disabled = on; });
  }
  async function work(fn, opts) {
    if (busy) return;
    setBusy(true); setProgress(t("Working, please wait…"));
    try { const msg = await fn(); if (opts && opts.status) setStatus(msg); setProgress(opts && opts.status ? "" : msg || ""); }
    catch (e) { if (opts && opts.status) setStatus(t("Could not read the save. Go back and try again.")); setProgress(e.message || t("Operation could not complete. Please try again.")); }
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
  const confirmSheet = (title, body, ok) => sheet(t(title), t(body), [{label: t("Cancel"), value: false}, {label: t(ok || "Confirm"), value: true, kind: "primary"}]);
  const notice = (body) => sheet("Private Football", t(body), [{label: t("OK"), value: true, kind: "primary"}]);

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
  function paintHomeRecent() { const box=$("home-recent");if(box)box.remove(); }
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
    try { const r = await call("inspect"); if (view !== "saves") setStatus(r.text); } catch (e) { setStatus(t("Resources missing · Install the matching offline resource pack and try again.")); }
  }
  async function loadSummary() {
    if (info.gameEntered) { setStatus(t("The game has started. Close and reopen it first.")); setBusy(false); return; }
    setStatus(t("Reading save…"));
    work(async () => (await call("summary")).text, {status: true});
  }

  async function prepare(repair) {
    if (busy) return;
    setBusy(true); setProgress(t("Checking local resources…"));
    try {
      const r = await call("prepare", {repair});
      if (r.installed) {
        const go = await sheet(t("Resource Import Complete"), t("Resources have been saved to the main game; future overlay updates will not need to download them again. You can now uninstall “73efootball Offline Resources”; keep the main game data."),
          [{label: t("Later"), value: false}, {label: t("Enter Game"), value: true, kind: "primary"}]);
        if (!go) { setBusy(false); setProgress(""); return; }
      }
      await call("launch");
    } catch (e) { setBusy(false); setProgress(e.message || t("Preparation could not complete. Your existing save is preserved.")); }
  }

  async function cleanStorage() {
    if (info.gameEntered) { notice("Close the game and reopen this app before cleaning storage."); return; }
    if (busy) return;
    setBusy(true); setProgress(t("Working, please wait…"));
    try {
      const r = await call("storagePreview");
      setBusy(false); setProgress(r.message || "");
      if (r.recovery) {
        if (await confirmSheet("Resume interrupted cleanup", "The previous cleanup was interrupted. Restore unconfirmed staged files or finish the confirmed deletion, then scan again.", "Confirm"))
          work(async () => (await call("storageRecover")).message);
        return;
      }
      if (!await sheet(t("Storage usage and cleanup preview"), r.text, [{label: t("Back"), value: false}, {label: t("Choose cleanup items"), value: true, kind: "primary"}])) return;
      const list = document.createElement("div"), boxes = [];
      r.groups.forEach(g => {
        const row = document.createElement("label"); row.className = "pick" + (g.selected ? " on" : "");
        const box = document.createElement("input"); box.type = "checkbox"; box.checked = !!g.selected; boxes.push([g.id, box]);
        box.addEventListener("change", () => row.classList.toggle("on", box.checked));
        const name = document.createElement("span"); name.textContent = g.label;
        row.append(box, name); list.appendChild(row);
      });
      if (!await sheet(t("Choose cleanup items"), "", [{label: t("Cancel"), value: false}, {label: t("Confirm cleanup"), value: true, kind: "primary"}], list)) return;
      const ids = boxes.filter(([, b]) => b.checked).map(([id]) => id);
      if (ids.includes("backups") && !await confirmSheet("Permanently delete historical backups?", "Delete historical publication backups and confirmed unused recovery copies. Current resources, projects and saves are preserved. This cannot be undone.", "Confirm")) return;
      work(async () => (await call("storageClean", {token: r.token, ids})).message);
    } catch (e) { setBusy(false); setProgress(e.message || t("Operation could not complete. Please try again.")); }
  }

  async function dedupe() {
    if (busy) return;
    setBusy(true); setProgress(t("Working, please wait…"));
    try {
      const r = await call("dedupePreview"); setBusy(false); setProgress(r.count ? "" : r.text);
      if (r.count && await confirmSheet("Review Duplicate Cleanup", r.text, "Confirm")) work(async () => (await call("dedupeDelete", {token: r.token})).message);
    } catch (e) { setBusy(false); setProgress(e.message || t("Operation could not complete. Please try again.")); }
  }

  handlers.message = d => { setBusy(false); setProgress(d.text); };
  handlers.importPicked = async () => {
    if (await confirmSheet("Import Save", "This will replace current progress. A backup is created before import; resource files are preserved. Import now?", "Confirm")) work(async () => (await call("importCommit")).message);
    else call("importCancel").catch(() => {});
  };

  function bind() {
    $("private-diagnostics").addEventListener("click",()=>call("editor",{op:"privateTool",payload:{tool:"diagnostics"}}).catch(e=>setProgress(e.message)));
    $("private-transfer").addEventListener("click", () => window.PrivateTransfer.enter());
    $("native-launcher").addEventListener("click", () => { if (!busy) call("nativeLauncher").catch(e => setProgress(e.message)); });
    $("native-editor").addEventListener("click", () => call("openPanel", {name: "editor"}).catch(e => setProgress(e.message)));
    $("enter").addEventListener("click", () => prepare(false));
    $("repair").addEventListener("click", async () => { if (await confirmSheet("Repair Resources", "Use only if resources are damaged. Resources will be verified and repaired. Saves are preserved; missing files may require the offline resource pack.", "Confirm")) prepare(true); });
    document.querySelectorAll("#dock button").forEach(b => b.addEventListener("click", () => { if (!busy && b.dataset.page !== view) show(b.dataset.page); }));
    $("repair2").addEventListener("click", () => $("repair").click());
    $("open-designer").addEventListener("click", () => info.gameEntered ? notice("Close the game and reopen this app before using Card Art.") : call("openPanel", {name: "designer"}));
    $("open-storage").addEventListener("click", cleanStorage);
    $("max-level").addEventListener("click", async () => {
      if (await confirmSheet("Max-Level Players & Allocate Progression", "Only owned players below their level cap, including reserves, are maxed and automatically reallocated by position. Their manual allocations are replaced. Already max-level players and their remaining points are untouched. Skills, boosters, and squads are preserved. A backup is created first.", "Confirm"))
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
    $("ver").textContent = "V19.1 · Earth";
    info.language = "en";
    applyLanguage("en");
    await applyText(); show("home");
    window.LauncherStartup.ready();
  })().catch(error => window.LauncherStartup.fail(error && error.message));
})();
