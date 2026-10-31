"use strict";
/* Shared helpers for the player editor modules. All text goes through textContent. */
(() => {
  const A = () => window.LauncherApi;
  const U = {locked: false};
  window.EditorUI = Object.assign(window.EditorUI || {}, {U});

  U.h = (tag, props, ...kids) => {
    const e = document.createElement(tag);
    for (const [k, v] of Object.entries(props || {})) {
      if (k === "class") e.className = v;
      else if (k === "on") for (const [ev, fn] of Object.entries(v)) e.addEventListener(ev, fn);
      else if (v === true) e.setAttribute(k, "");
      else if (v !== false && v != null) e.setAttribute(k, v);
    }
    kids.flat().forEach(c => { if (c != null && c !== false) e.append(c.nodeType ? c : document.createTextNode(String(c))); });
    return e;
  };
  U.tx = s => { const a = A(); if (!s || a.lang() === "zh-CN") return s; if (a.lang() !== "en") return window.UiLocalization.t(s); if (a.cache.has(s)) return a.cache.get(s); a.need(s); return s; };
  // Leaf element whose text is re-translated when the host finishes a batch.
  U.t = (el, s) => { el.dataset.src = s; el.textContent = U.tx(s); return el; };
  U.ph = (el, s) => { el.dataset.ph = s; el.placeholder = U.tx(s); return el; };
  U.refresh = root => {
    root.querySelectorAll("[data-src]").forEach(e => { e.textContent = U.tx(e.dataset.src); });
    root.querySelectorAll("[data-ph]").forEach(e => { e.placeholder = U.tx(e.dataset.ph); });
  };
  U.pre = async list => {
    const a = A(); if (a.lang() !== "en") return;
    const need = [...new Set(list)].filter(s => s && !a.cache.has(s)); if (!need.length) return;
    try { const r = await a.call("translate", {items: need}); need.forEach((s, i) => a.cache.set(s, r.items[i] || s)); } catch (e) { /* show source text */ }
  };
  U.sheet = async (title, body, buttons, extra) => {
    await U.pre([title, body, ...buttons.map(b => b.label)]);
    return A().sheet(U.tx(title), U.tx(body || ""), buttons.map(b => Object.assign({}, b, {label: U.tx(b.label)})), extra);
  };
  U.ok = label => ({label: label || "知道了", value: true, kind: "primary"});
  U.toast = msg => {
    const el = U.h("div", {class: "ed-toast"}); U.t(el, msg); document.body.append(el);
    setTimeout(() => el.remove(), 1900);
  };
  U.api = (op, payload) => A().call("editor", {op, payload: payload || {}});
  // One long operation at a time; failures become a sheet, never a silent no-op.
  U.run = async (msg, fn) => {
    if (U.locked) return undefined;
    U.locked = true; A().meter(true); A().progress(U.tx(msg));
    try { return await fn(); }
    catch (e) { await U.sheet("编辑未完成", e.message || "请重试。", [U.ok()]); return undefined; }
    finally { U.locked = false; A().meter(false); A().progress(""); }
  };

  // Portraits: lazy, at most four requests in flight, small bounded cache.
  const cache = new Map(), waiting = [];
  let active = 0;
  const paint = (el, url) => { if (el.isConnected && url) { el.style.backgroundImage = `url(${url})`; el.classList.add("on"); el.dataset.art = url.startsWith("http") ? "card" : "head"; } };
  // Card art from the CDN first (the host caches it, so it also works offline once seen); the game's own
  // portrait is the fallback. After repeated CDN misses we skip it for a minute so lists stay quick.
  const CDN = id => "https://efimg.com/efootballhub22/images/player_cards/" + id + "_l.png";
  let cdnMiss = 0, cdnPause = 0;
  const cdn = id => new Promise((resolve, reject) => {
    if (Date.now() < cdnPause) { reject(new Error("paused")); return; }
    const img = new Image(), timer = setTimeout(() => { img.src = ""; reject(new Error("timeout")); }, 7000);
    img.onload = () => { clearTimeout(timer); cdnMiss = 0; resolve(img.src); };
    img.onerror = () => { clearTimeout(timer); if (++cdnMiss >= 3) { cdnPause = Date.now() + 60000; cdnMiss = 0; } reject(new Error("miss")); };
    img.src = CDN(id);
  });
  const remember = (key, url) => { cache.set(key, url); if (cache.size > 300) cache.delete(cache.keys().next().value); };
  const pump = () => {
    while (active < 4 && waiting.length) {
      const {el, key, id} = waiting.shift(); active++;
      U.api("portrait", {id}).then(r => {
        if(r.found){const url="data:image/png;base64,"+r.png;remember(key,url);paint(el,url);return;}
        return cdn(id).then(url=>{remember(key,url);paint(el,url);});
      }).catch(() => cache.set(key, null)).finally(() => { active--; pump(); });
    }
  };
  const seen = new IntersectionObserver(entries => entries.forEach(en => {
    if (!en.isIntersecting) return; seen.unobserve(en.target);
    const el = en.target, key = el.dataset.id + "/" + el.dataset.rev;
    if (cache.has(key)) paint(el, cache.get(key)); else { waiting.push({el, key, id: el.dataset.id}); pump(); }
  }), {rootMargin: "200px"});
  U.refreshPortrait = async id => {
    for(const key of [...cache.keys()])if(key.startsWith(String(id)+":"))cache.delete(key);
    const r=await U.api("portrait",{id:String(id)});if(!r.found)return;
    const url="data:image/png;base64,"+r.png;
    document.querySelectorAll("[data-id]").forEach(el=>{if(el.dataset.id===String(id))paint(el,url);});
  };
  U.portrait = (p, size) => {
    const el = U.h("span", {class: "pt"}); if (size) el.style.width = el.style.height = size + "px";
    // The CDN needs only the card id; the portrait revision just versions the game-resource fallback.
    if (/^[0-9]{1,18}$/.test(String(p.id))) { el.dataset.id = p.id; el.dataset.rev = p.portrait_revision == null ? "0" : p.portrait_revision; seen.observe(el); }
    return el;
  };

  // Same wording rules as PlayerEditorPanel.diffValue.
  U.diffValue = (field, value, s) => {
    const find = (rows, id) => (rows || []).filter(r => r.id === id).pop();
    if (field === "boosters" && Array.isArray(value))
      return value.map((id, i) => { const r = find(s.boosters, id); return "槽" + (i + 1) + "：" + (r ? r.label : id === 0 ? "未启用" : id === 136 ? "待制作（空槽）" : "保留原增能 · 编号 " + id); }).join(" / ");
    if (field === "play_style" && Array.isArray(value))
      return [0, 1].map(i => { const r = find(((s.play_styles || {})[i === 0 ? "attack" : "defense"]), value[i]); return (i === 0 ? "进攻：" : "防守：") + (r ? r.label : "保留原风格 · ID " + value[i]); }).join(" / ");
    if (field === "skills" && Array.isArray(value))
      return value.length ? value.map(id => { const r = find(s.skills, id); return r ? r.label : "ID " + id; }).join("、") : "无";
    if (field.startsWith("aptitude:") && typeof value === "number") return value >= 0 && value <= 2 ? ["不熟练", "部分熟练", "完全熟练"][value] : String(value);
    if (field === "condition" && typeof value === "number") return value >= 0 && value <= 4 ? "EDCBA"[value] : value === -1 ? "跟随游戏" : "原状态值 " + value;
    return String(value);
  };
})();
