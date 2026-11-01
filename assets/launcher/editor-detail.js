"use strict";
/* Player detail: five tabs plus the preview -> backup+save flow (PlayerEditorPanel.choose). */
(() => {
  const {h, t, tx} = window.EditorUI.U, U = window.EditorUI.U;
  const plans = p => {
    const names = (p.plans || []).map(x => x.name + (x.current ? " (current)" : "")).join(" · ");
    return names || (p.warehouse ? "Storage player" : "Not in a game plan");
  };
  window.EditorUI.plans = plans;

  window.EditorUI.detail = function (player, schema, host) {
    const lazy = factory => {let actual=null;const m={el:h('div'),onShow(){if(!actual){actual=factory();m.el.append(actual.el);}actual.onShow?.();},apply(c){actual?.apply?.(c);},changes(){return actual?.changes?.()||null;},boosters(){return actual?.boosters?.()||null;}};return m;};
    const tabs = [["Abilities & Training",lazy(()=>window.EditorUI.dev(player,schema))],["Positions & Style",lazy(()=>window.EditorUI.pos(player,schema))],
      ["Player Skills",lazy(()=>window.EditorUI.skills(player,schema))],["Boosters",lazy(()=>window.EditorUI.boosters(player,schema))],["Appearance & Motion",lazy(()=>window.EditorUI.look(player,schema))]];
    const body = h("div", {class: "ed-body"}), bar = h("div", {class: "ed-tabs"});
    const SHORT = ["Abilities", "Positions", "Skills", "Boosters", "Appearance"], en = false;
    const buttons = tabs.map(([label, mod], i) => {
      const b = h("button", {type: "button", class: "ed-tab", on: {click: () => show(i)}}); t(b, en ? label : SHORT[i]); bar.append(b);
      mod.el.hidden = i !== 0; body.append(mod.el); return b;
    });
    function show(n) { tabs.forEach(([, m], i) => { m.el.hidden = i !== n; buttons[i].classList.toggle("on", i === n); }); if (tabs[n][1].onShow) tabs[n][1].onShow(); }
    show(0);

    const Store = window.EditorUI.Store, cmp = window.EditorUI.compare;
    Store.touch({id: player.id, serial: player.serial, name: player.name, overall: player.overall, position: player.position, kind: "owned"});
    function heroActions() {
      const star = h("button", {type: "button", class: "ed-star"});
      const paintStar = () => { star.classList.toggle("on", Store.isFav(player.id)); star.textContent = tx(Store.isFav(player.id) ? "★ Saved" : "☆ Save"); };
      star.onclick = async () => { await Store.toggleFav(player.id); paintStar(); };
      paintStar();
      const pk = cmp && cmp.fromOwned(player, schema);
      const vs = h("button", {type: "button", class: "ed-star"});
      const paintVs = () => { vs.classList.toggle("on", !!pk && cmp.has(pk.key)); t(vs, pk && cmp.has(pk.key) ? "Remove from compare" : "Add to compare"); };
      vs.onclick = () => { if (!pk) return; cmp.setSchema(schema); if (cmp.add(pk)) U.toast("Added to compare"); paintVs(); };
      paintVs();
      return h("div", {class: "ed-hero-actions"}, star, vs);
    }
    const posName = (schema.positions || [])[player.position] || "";
    const art = U.portrait(player, 0); art.classList.add("ed-art");
    const card = h("div", {class: "ed-card3"}, art, h("span", {class: "ed-c-ovr"}, String(player.overall), h("small", {}, posName)));
    const roles = h("div", {class: "ed-roles"}); roles.textContent = tx([posName, player.card_type_label].filter(Boolean).join("  ·  "));
    const quick = (v, k) => { const s = h("span", {}, h("b", {}, String(v))); const l = h("small"); t(l, k); s.append(l); return s; };
    const dv = player.development || {};
    const plansLine = h("p", {class: "ed-plans"}); plansLine.textContent = tx(`Instance ${player.serial} · ${plans(player)}`);
    const hero = h("div", {class: "ed-hero3"}, card, h("div", {class: "ed-info"}, h("h2", {class: "ed-name"}, player.name || ""), roles,
      h("div", {class: "ed-quick"}, quick(player.overall, "Overall"), quick(player.level, "Level"), quick(player.level_limit, "Cap"), quick(dv.available ? dv.budget : "-", "Points")), plansLine, heroActions()));
    const submit = h("button", {type: "button", class: "ed-btn wide primary"}); t(submit, "Review Changes");
    const pending = () => {
      const c = {};
      for (const [, m] of tabs) if (m.apply) { try { m.apply(c); } catch (e) { /* surfaced when the user presses check */ } }
      return Object.keys(c).length + (tabs[0][1].changes() ? 1 : 0) + (tabs[3][1].boosters() ? 1 : 0);
    };
    let tick = 0;
    const sync = () => {
      clearTimeout(tick);
      tick = setTimeout(() => {
        const n = pending();
        submit.dataset.src = n ? `Review Changes · ${n} ` : "Review Changes"; submit.textContent = tx(submit.dataset.src);
        submit.classList.toggle("idle", n === 0);
      }, 30);
    };
    ["input", "change", "click", "ed-change"].forEach(ev => body.addEventListener(ev, sync));
    submit.onclick = () => U.run("Reviewing changes…", async () => {
      const changes = {};
      for (const [, m] of tabs) if (m.apply) m.apply(changes);
      const dev = tabs[0][1].changes(); if (dev) changes.development = dev;
      const boosters = tabs[3][1].boosters();
      if (!Object.keys(changes).length && !boosters) { U.toast("No fields were changed"); return; }
      const request = {id: player.id, serial: player.serial, changes}; if (boosters) request.boosters = boosters;
      const pv = await U.api("preview", request);
      if (!pv.changed) { U.toast("No changes to save"); return; }
      request.token = pv.token;
      const lines = h("div", {class: "ed-diff"}, pv.diff.map(c => {
        const row = h("div", {}), name = h("b"), val = h("span");
        name.textContent = tx(c.label); val.textContent = tx(U.diffValue(c.field, c.before, schema)) + "  →  " + tx(U.diffValue(c.field, c.after, schema));
        row.append(name, val); return row;
      }));
      const foot = h("p", {class: "ed-note"}); t(foot, "A backup is created before saving. Level, progression points, and progression records are saved together; match stats and game plans are preserved. Reference overall is not recalculated here; verify it in game.");
      const go = await U.sheet(`Confirm ${pv.diff.length} changes`, `${player.name} · ${player.id} / ${player.serial}`,
        [{label: "Back to Editor", value: false}, {label: "Back Up & Save", value: true, kind: "primary"}], h("div", {}, lines, foot));
      if (!go) return;
      const saved = await U.api("apply", request);
      let msg = saved.changed ? "Backed up and saved. Enter the game to check the result." : "Data is identical; no changes needed.";
      const rt = saved.live_condition_runtime;
      if (changes.condition !== undefined && rt && rt.status !== "installed") msg = "Backed up and saved. Restart the game to activate live form.";
      await U.sheet("Saved", msg, [U.ok("Back to List")]); host.done();
    });
    async function leave(refresh){if(U.locked)return;if(pending()){const ok=await U.sheet('Unsaved changes','Discard the current unsaved changes?', [{label:'Keep editing',value:false},{label:'Discard',value:true}]);if(!ok)return;}if(refresh)host.refresh();else host.back();}
    const navigation=h('div',{class:'ed-detail-navigation'},h('button',{type:'button',class:'ed-btn',on:{click:()=>leave(false)}},'← Back to players'),h('button',{type:'button',class:'ed-btn',on:{click:()=>leave(true)}},'↻ Refresh'));
    const root = h("div", {class: "ed-detail"}, navigation, hero, bar, body, h("div", {class: "ed-submit"}, submit));
    sync();
    return {el: root};
  };
})();
