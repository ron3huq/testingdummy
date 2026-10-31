"use strict";
/* Full-database picker (PlayerEditorPanel.catalog / confirmAdd). Filtering runs on the host so tens of
   thousands of cards never cross the bridge at once; the page asks for 60 rows at a time. */
(() => {
  const {h, t, tx} = window.EditorUI.U, U = window.EditorUI.U, W = window.EditorUI.W, Store = window.EditorUI.Store;
  const PAGE = 60;

  window.EditorUI.catalog = function (schema, host) {
    const positions = schema.positions || [];
    const list = W.container(), count = h("p", {class: "ed-note"}), more = h("button", {type: "button", class: "ed-btn wide", hidden: true});
    let F = W.emptyFilter(), board = 0;
    const abils = (schema.abilities || []).map(a => ({label: a.label}));
    const sb = W.searchBar("名字 / 卡片ID / 位置 / 卡型", async () => { const next = await W.filterSheet(positions, types, F, abils); if (next) { F = next; query(true); } });
    // Boards are presets over the host query: sort order plus an ownership filter.
    const BOARDS = [["最高评分", 0, ""], ["收藏", 0, "fav"], ["未持有", 3, "unowned"], ["已持有", 0, "owned"], ["名称顺序", 1, ""]];
    const boards = W.pills(BOARDS.map(b => b[0]), 0, i => { board = i; order.value = BOARDS[i][1]; query(true); });
    const q = sb.input;
    const sel = labels => h("select", {class: "ed-in"}, labels.map((l, i) => { const o = h("option", {value: i}); o.textContent = tx(l); return o; }));
    const order = sel(["总评降序", "名称顺序", "等级上限降序", "优先未持有"]);
    let types = [], total = 0, shown = 0, gen = 0, squad = null, timer = 0, lastCards = [];
    t(more, "显示更多");

    const row = c => W.entry(c, positions, [`${c.id} · 总评 ${c.overall} · ${c.card_type_label}`, `${positions[c.position] || ""} · 等级上限 ${c.level_limit} · 已持有 ${c.owned} 张`], () => view(c));
    async function query(reset) {
      const my = ++gen; sb.mark(W.filterActive(F)); if (reset) { W.setMode(list); list.replaceChildren(); shown = 0; }
      try {
        const r = await U.api("catalogQuery", {q: q.value, positions: [...F.pos], types: [...F.type], omin: F.omin, omax: F.omax, ab: F.ab, own: BOARDS[board][2] === "fav" ? "" : BOARDS[board][2], only: BOARDS[board][2] === "fav" ? Store.favs : undefined, order: +order.value, offset: shown, limit: PAGE});
        if (my !== gen) return;
        total = r.total; r.cards.forEach(c => list.append(row(c))); shown += r.cards.length; lastCards = reset ? r.cards.slice() : lastCards.concat(r.cards);
        count.textContent = tx(total === 0 ? (BOARDS[board][2] === "fav" ? "还没有收藏，点开卡片后点星标收藏" : "未找到卡片，请调整关键词") : `显示 ${shown} / ${total} 张 · 点按查看详情`);
        more.hidden = shown >= total;
      } catch (e) { count.textContent = e.message; }
    }
    const later = () => { clearTimeout(timer); timer = setTimeout(() => query(true), 200); };
    [q].forEach(e => e.addEventListener("input", later)); order.addEventListener("change", () => { boards.set(-1); query(true); });
    more.onclick = () => query(false);

    // Read-only look at a card (ratings and abilities) before deciding to add it.
    async function view(c) {
      const names = {}; (schema.abilities || []).forEach((a, i) => { names[i] = a.label; });
      const art = U.portrait(c, 0); art.classList.add("ed-art");
      const card = h("div", {class: "ed-card3"}, art, h("span", {class: "ed-c-ovr"}, String(c.overall), h("small", {}, positions[c.position] || "")));
      const meta = h("div", {class: "ed-info"}, h("h2", {class: "ed-name"}, c.name));
      const roles = h("div", {class: "ed-roles"}); roles.textContent = tx([positions[c.position], c.card_type_label].filter(Boolean).join("  ·  "));
      const sub = h("p", {class: "ed-plans"}); sub.textContent = tx(`${c.id} · 等级上限 ${c.level_limit} · 已持有 ${c.owned} 张`);
      const star = h("button", {type: "button", class: "ed-star"});
      const paintStar = () => { star.classList.toggle("on", Store.isFav(c.id)); star.textContent = tx(Store.isFav(c.id) ? "★ 已收藏" : "☆ 收藏"); };
      star.onclick = async () => { await Store.toggleFav(c.id); paintStar(); if (BOARDS[board][2] === "fav") query(true); };
      paintStar();
      meta.append(roles, sub, star);
      Store.touch({id: c.id, name: c.name, overall: c.overall, position: c.position, kind: "card"});
      const body = h("div", {}, h("div", {class: "ed-hero3"}, card, meta));
      if (Array.isArray(c.ab)) {
        const grid = h("div", {class: "ed-abil"});
        c.ab.forEach((v, i) => { const chip = h("b", {class: "ed-chip"}, String(v)); chip.dataset.band = window.EditorCore.abilityBand(v);
          const cell = h("div", {class: "ed-cell"}, h("span", {}, tx(names[i] || "")), chip); cell.dataset.band = chip.dataset.band; grid.append(cell); });
        body.append(grid);
      }
      const cmp = window.EditorUI.compare, inCmp = cmp && cmp.has("c" + c.id);
      const go = await U.sheet("卡片详情", "", [{label: "返回", value: false}, {label: inCmp ? "移出对比" : "加入对比", value: "compare"}, {label: c.editable ? "加入仓库…" : "不可加入", value: true, kind: "primary"}], body);
      if (go === "compare") { cmp.setSchema(schema); const on = cmp.add(cmp.fromCard(c)); if (on) U.toast("已加入对比"); return; }
      if (go === true && c.editable) await confirmAdd(c);
    }

    const cart = new Map();
    const cartBar=h("div",{class:"ed-submit private-cart"});
    const cartCount=h("span",{}),cartAdd=h("button",{type:"button",class:"ed-btn primary"},"Add selected to storage");
    const paintCart=()=>{cartCount.textContent=cart.size+" selected";cartAdd.disabled=!cart.size;};
    cartAdd.onclick=()=>U.run("Adding selected players…",async()=>{
      if(!cart.size)return;
      const ok=await U.sheet("Add selected players",[...cart.values()].map(c=>c.name).join("\n"),[{label:"Cancel",value:false},{label:"Add to storage",value:true,kind:"primary"}]);
      if(!ok)return;
      for(const [id,c]of [...cart]){await U.api("add",{card_id:c.id,destination:"inventory"});cart.delete(id);paintCart();}
      U.toast("Players added to storage");
    });
    cartBar.append(cartCount,cartAdd);paintCart();
    async function confirmAdd(c) {
      if(!c.editable)return;
      if(cart.size>=50&&!cart.has(String(c.id)))throw new Error("Add the current 50 selections first");
      cart.set(String(c.id),c);paintCart();U.toast("Added to cart · Continue choosing players");
    }

    const head = h("div", {class: "ed-head"}, h("h2", {}, ""));
    return {el: h("div", {}, head, sb.el, boards.el, h("div", {class: "ed-bar"}, count, order, W.viewToggle(() => query(true))), list, more, cartBar),
      setQuery(v) { q.value = v; },
      viewOnly() { if (total === 1 && lastCards[0]) view(lastCards[0]); },
      async open() {
        const r = await U.api("catalogOpen"); types = r.types || []; squad = r.squad || null;
        const title = head.firstChild; title.textContent = tx(`全数据库选人 · ${r.count} 张`);
        await query(true);
      }};
  };
})();
