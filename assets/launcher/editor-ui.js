"use strict";
/* Shared list widgets for the player pages: scope pills, grid/list tiles, filter sheet.
   Layout ideas follow the reference offline pack manager (tabs, card grid, filter sheet). */
(() => {
  const U = window.EditorUI.U, {h, t, tx} = U;
  const W = {};
  window.EditorUI.W = W;

  // Horizontal pill row. Returns {el, set(i), get()}.
  W.pills = (labels, start, onPick) => {
    let cur = start || 0;
    const btns = [], paint = () => btns.forEach((b, i) => b.classList.toggle("on", i === cur));
    labels.forEach((l, i) => {
      const b = h("button", {type: "button", class: "ed-pill", on: {click: () => { cur = i; paint(); onPick(i); }}});
      t(b, l); btns.push(b);
    });
    paint();
    return {el: h("div", {class: "ed-pills"}, btns), set: i => { cur = i; paint(); }, get: () => cur};
  };

  // Search box with a filter button; the button shows a dot while any filter is active.
  W.searchBar = (placeholder, onFilter) => {
    const input = h("input", {type: "search", class: "ed-in", autocomplete: "off"}); U.ph(input, placeholder);
    const btn = h("button", {type: "button", class: "ed-fbtn", "aria-label": "filter", on: {click: onFilter}},
      h("span", {class: "ed-fico"}), h("i", {class: "ed-fdot", hidden: true}));
    return {el: h("div", {class: "ed-search"}, input, btn), input, mark: on => { btn.querySelector(".ed-fdot").hidden = !on; }};
  };

  // Grid / list switch. The choice lives in memory only (WebView DOM storage is off).
  W.viewMode = {grid: true};
  W.viewToggle = onChange => {
    const b = h("button", {type: "button", class: "ed-vbtn", "aria-label": "view"});
    const paint = () => { b.dataset.mode = W.viewMode.grid ? "grid" : "list"; };
    b.onclick = () => { W.viewMode.grid = !W.viewMode.grid; paint(); onChange(); };
    paint(); return b;
  };

  const apply = (el, grid) => { el.className = grid ? "ed-grid" : "ed-list"; };
  W.container = () => h("div", {class: "ed-grid"});
  W.setMode = el => apply(el, W.viewMode.grid);

  // One entry. In grid mode: card art with rating/position badges and the name below.
  // In list mode: the row layout with up to three detail lines.
  W.entry = (p, positions, lines, onClick) => {
    const pos = positions[p.position] || "";
    if (W.viewMode.grid) {
      const badge = h("span", {class: "ed-ovr"}, h("b", {}, p.overall), h("small", {}, pos));
      const art = U.portrait(p, 0); art.classList.add("ed-art");
      const owned = p.owned ? h("i", {class: "ed-own"}, "×" + p.owned) : null;
      const name = h("span", {class: "ed-nm"}, p.name);
      return h("button", {type: "button", class: "ed-tile", on: {click: onClick}}, art, badge, owned, name);
    }
    const body = h("div", {}, h("b", {}, p.name), lines.map(s => { const e = h("small"); e.textContent = tx(s); return e; }));
    return h("button", {type: "button", class: "ed-item", on: {click: onClick}}, U.portrait(p, 48), body);
  };

  // Filter sheet. state = {pos:Set<number>, type:Set<string>, omin:string, omax:string}; returns the new state or null.
  W.emptyFilter = () => ({pos: new Set(), type: new Set(), omin: "", omax: "", ab: {}});
  W.filterActive = f => f.pos.size > 0 || f.type.size > 0 || f.omin !== "" || f.omax !== "" || Object.keys(f.ab || {}).length > 0;
  // abilities (optional): [{label}] in the order of a card's compact `ab` array; adds a "minimum ability" section.
  W.filterSheet = async (positions, types, state, abilities) => {
    const cur = {pos: new Set(state.pos), type: new Set(state.type), omin: state.omin, omax: state.omax, ab: Object.assign({}, state.ab || {})};
    for (;;) {
      const chip = (label, on, flip) => { const b = h("button", {type: "button", class: "ed-chipb" + (on ? " on" : ""), on: {click: () => { flip(); b.classList.toggle("on"); }}}); b.textContent = tx(label); return b; };
      const flipIn = (set, v) => () => { if (set.has(v)) set.delete(v); else set.add(v); };
      const posGrid = h("div", {class: "ed-chips"}, positions.map((l, i) => chip(l, cur.pos.has(i), flipIn(cur.pos, i))));
      const typeGrid = types.length ? h("div", {class: "ed-chips"}, types.map(l => chip(l, cur.type.has(l), flipIn(cur.type, l)))) : null;
      const lo = h("input", {type: "number", inputmode: "numeric", class: "ed-in", value: cur.omin, min: 0, max: 130}), hi = h("input", {type: "number", inputmode: "numeric", class: "ed-in", value: cur.omax, min: 0, max: 130});
      U.ph(lo, "最低"); U.ph(hi, "最高");
      const title = k => { const e = h("h4"); t(e, k); return e; };
      let abBox = null;
      if (abilities && abilities.length) {
        const sum = h("summary"); t(sum, "能力值下限");
        const grid = h("div", {class: "ed-abmin"}, abilities.map((a, i) => {
          const inp = h("input", {type: "number", inputmode: "numeric", class: "ed-in", min: 0, max: 130, value: cur.ab[i] == null ? "" : cur.ab[i]});
          inp.addEventListener("input", () => { const v = inp.value.trim(); if (v === "" || isNaN(+v)) delete cur.ab[i]; else cur.ab[i] = +v; });
          const name = h("span"); name.textContent = tx(a.label);
          return h("label", {}, name, inp);
        }));
        abBox = h("details", {class: "ed-fold", open: Object.keys(cur.ab).length > 0}, sum, grid);
      }
      const body = h("div", {class: "ed-filter"}, title("位置"), posGrid, typeGrid ? title("卡型") : null, typeGrid, title("参考总评"), h("div", {class: "ed-row"}, lo, hi), abBox);
      const go = await U.sheet("筛选", "", [{label: "重置", value: "reset"}, {label: "应用", value: true, kind: "primary"}], body);
      if (go === "reset") { cur.pos.clear(); cur.type.clear(); cur.omin = cur.omax = ""; cur.ab = {}; continue; }
      if (!go) return null;
      cur.omin = lo.value.trim(); cur.omax = hi.value.trim();
      return cur;
    }
  };
  W.rangeOk = (f, overall) => (f.omin === "" || overall >= +f.omin) && (f.omax === "" || overall <= +f.omax);
})();
