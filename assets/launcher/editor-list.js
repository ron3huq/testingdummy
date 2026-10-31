"use strict";
/* Players page: owned-player list with search/scope/order, plus entry points to the catalog and undo. */
(() => {
  const {h, t, tx} = window.EditorUI.U, U = window.EditorUI.U, C = window.EditorCore, W = window.EditorUI.W, Store = window.EditorUI.Store;
  const PAGE = 60;
  const root = () => document.getElementById("ed-root");
  let data = null, view = "list", labels = new Map(), shownCount = 0, visible = [], timer = 0;
  const S = {query: "", scope: 0, order: 0};
  let listEl, countEl, moreEl, qEl, orderEl, undoEl, panes, markEl, recentEl, F = W.emptyFilter();

  const searchLabel = p => { let s = labels.get(p); if (!s) { s = `${p.name} ${p.name_en || ""} ${p.id} ${p.serial} ${window.EditorUI.plans(p)}`; labels.set(p, s); } return s; };
  const cmp = (a, b) => (a < b ? -1 : a > b ? 1 : 0);
  function filter() {
    S.query = qEl.value; S.order = +orderEl.value; markEl(W.filterActive(F));
    visible = data.players.filter(p => C.matches(S.query, searchLabel(p), S.scope, !!p.current_squad, !!p.in_squad, !!p.warehouse)
      && (S.scope !== 5 || Store.isFav(p.id)) && (!F.pos.size || F.pos.has(p.position)) && (!F.type.size || F.type.has(p.card_type_label)) && W.rangeOk(F, p.overall));
    visible.sort((a, b) => {
      let c = S.order === 1 ? b.overall - a.overall : S.order === 2 ? b.level - a.level : 0;
      if (!c) c = cmp(a.name, b.name); if (!c) c = cmp(a.id, b.id); return c || a.serial - b.serial;
    });
    shownCount = 0; W.setMode(listEl); listEl.replaceChildren(); more();
    countEl.textContent = tx(visible.length ? `Showing ${visible.length} / ${data.players.length} players · distinguished by card instance` : "No players found. Adjust the search or filters.");
  }
  function more() {
    const names = data.schema.positions || [];
    visible.slice(shownCount, shownCount + PAGE).forEach(p => {
      const l1 = h("small"), l2 = h("small"), l3 = h("small"), plans = window.EditorUI.plans(p);
      l1.textContent = tx(`${p.id} · Instance ${p.serial}`); l2.textContent = tx(plans);
      l3.textContent = tx(`${names[p.position] || ""} · Lv. ${p.level} · Reference overall ${p.overall} · Additional skills ${(p.additional_skills || []).length} / 10 · Booster ${U.diffValue("boosters", p.boosters || [], data.schema)}`);
      listEl.append(W.entry(p, names, [l1.textContent, l2.textContent, l3.textContent], () => open(p)));
    });
    shownCount = Math.min(visible.length, shownCount + PAGE); moreEl.hidden = shownCount >= visible.length;
  }

  function go(next) {
    view = next; Object.entries(panes).forEach(([k, e]) => { e.hidden = k !== next; });
    if (next === "list") U.refresh(root());
  }
  async function load() {
    await Store.load();
    await U.run("Reading local save…", async () => { data = await U.api("list"); if (window.EditorUI.compare) window.EditorUI.compare.setSchema(data.schema); labels = new Map(); build(); filter(); go("list"); });
  }
  async function open(p) {
    if (!p.editable) { U.toast("Invalid work ID"); return; }
    await U.run("Reading local save…", async () => {
      const r = await U.api("detail", {id: p.id, serial: p.serial});
      const d = window.EditorUI.detail(r.player, data.schema, {done: () => { load(); }});
      panes.detail.replaceChildren(d.el); go("detail");
    });
  }
  async function openCatalog(preset) {
    await U.run("Loading player catalogue…", async () => {
      const c = window.EditorUI.catalog(data.schema, {done: () => { load(); }});
      if (typeof preset === "string") c.setQuery(preset);
      panes.catalog.replaceChildren(c.el); await c.open(); go("catalog");
      if (typeof preset === "string") c.viewOnly();
    });
  }
  async function undo() {
    if (!data.has_undo) { U.toast("No undo record"); return; }
    const ok = await U.sheet("Undo last edit?", "Only the last edited player instance is restored; newer match progress triggers protection.", [{label: "Cancel", value: false}, {label: "Confirm Undo", value: true, kind: "primary"}]);
    if (ok) await U.run("Restoring the previous edit…", async () => { await U.api("undo"); await load(); });
  }

  function build() {
    const title = h("h2"); title.textContent = tx(`Player Editor · ${data.players.length} players`);
    const sub = h("p", {class: "ed-note"}); t(sub, "Select an owned card to edit progression, form, positions, skills and boosters.");
    const sb = W.searchBar("Name / Card ID / Game plan (space-separated)", async () => {
      const types = [...new Set(data.players.map(p => p.card_type_label).filter(Boolean))].sort();
      const next = await W.filterSheet(data.schema.positions || [], types, F); if (next) { F = next; filter(); }
    });
    qEl = sb.input; qEl.value = S.query; markEl = sb.mark;
    const sel = (ls, v) => { const s = h("select", {class: "ed-in"}, ls.map((l, i) => { const o = h("option", {value: i}); o.textContent = tx(l); return o; })); s.value = v; return s; };
    const pills = W.pills(["All owned", "Current game plan", "In any game plan", "Storage player", "Not in a game plan", "Favorites"], S.scope, i => { S.scope = i; filter(); });
    orderEl = sel(["Sort by name", "Reference overall: highest first", "Level: highest first"], S.order);
    countEl = h("p", {class: "ed-note"}); listEl = W.container();
    moreEl = h("button", {type: "button", class: "ed-btn wide", hidden: true, on: {click: more}}); t(moreEl, "Show more");
    undoEl = h("button", {type: "button", class: "ed-btn", on: {click: undo}}); t(undoEl, "Undo Last Edit");
    const catBtn = h("button", {type: "button", class: "ed-btn primary", on: {click: () => openCatalog()}}); t(catBtn, "Player Catalogue");
    [qEl].forEach(e => e.addEventListener("input", () => { clearTimeout(timer); timer = setTimeout(filter, 120); })); orderEl.addEventListener("change", filter);
    recentEl = h("div", {class: "ed-recent", hidden: true});
    panes = {list: h("div", {}, h("div", {class: "ed-head"}, title, sub), recentEl, sb.el, pills.el, h("div", {class: "ed-row"}, catBtn, undoEl), h("div", {class: "ed-bar"}, countEl, orderEl, W.viewToggle(filter)), listEl, moreEl),
      catalog: h("div", {hidden: true}), detail: h("div", {hidden: true})};
    root().replaceChildren(panes.list, panes.catalog, panes.detail);
    paintRecent();
  }

  function paintRecent() {
    if (!recentEl) return;
    recentEl.replaceChildren();
    const items = Store.recent.slice(0, 8);
    recentEl.hidden = items.length === 0;
    if (!items.length) return;
    const head = h("p", {class: "ed-recent-h"}); t(head, "Recently viewed");
    const row = h("div", {class: "ed-recent-row"}, items.map(e => {
      const art = U.portrait({id: e.id, portrait_revision: 0}, 0); art.classList.add("ed-art");
      const b = h("button", {type: "button", class: "ed-recent-card", "aria-label": e.name, on: {click: () => window.EditorUI.openEntry(e)}},
        art, h("span", {class: "ed-ovr"}, h("b", {}, e.overall)), h("span", {class: "ed-nm"}, e.name));
      return b;
    }));
    recentEl.append(head, row);
  }
  Store.onChange(paintRecent);

  // Jump to a player from anywhere (home page, recent strip). The launcher has already switched to this page.
  window.EditorUI.openEntry = async entry => {
    for (let i = 0; i < 80 && !data; i++) await new Promise(r => setTimeout(r, 100));
    if (!data) return;
    if (entry.kind === "owned") {
      const p = data.players.find(x => x.id === entry.id && x.serial === entry.serial);
      if (p) { go("list"); await open(p); return; }
    }
    await openCatalog(entry.id);
  };

  window.EditorUI.enter = () => {
    const api = window.LauncherApi;
    if (api.gameEntered()) { root().replaceChildren(); const n = h("p", {class: "ed-note"}); t(n, "Close and reopen the game before editing players."); root().append(n); data = null; return; }
    if (!data) load(); else U.refresh(root());
  };
  window.EditorUI.back = () => { if (view === "list" || !data) return false; go("list"); return true; };
  document.addEventListener("DOMContentLoaded", () => window.LauncherApi.onText(() => U.refresh(root())));
})();
