"use strict";
/* Player detail: five tabs plus the preview -> backup+save flow (PlayerEditorPanel.choose). */
(() => {
  const {h, t, tx} = window.EditorUI.U, U = window.EditorUI.U;
  const plans = p => {
    const names = (p.plans || []).map(x => x.name + (x.current ? "（当前）" : "")).join(" · ");
    return names || (p.warehouse ? "储备球员" : "未编入比赛计划");
  };
  window.EditorUI.plans = plans;

  window.EditorUI.detail = function (player, schema, host) {
    const tabs = [["能力值与培养", window.EditorUI.dev(player, schema)], ["位置与比赛风格", window.EditorUI.pos(player, schema)],
      ["球员技能（已有＋附加）", window.EditorUI.skills(player, schema)], ["3增能", window.EditorUI.boosters(player, schema)], ["Appearance & Motion", window.EditorUI.look(player, schema)]];
    const body = h("div", {class: "ed-body"}), bar = h("div", {class: "ed-tabs"});
    const SHORT = ["能力", "位置", "技能", "增能", "外观"], en = window.LauncherApi.lang() === "en";
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
      const paintStar = () => { star.classList.toggle("on", Store.isFav(player.id)); star.textContent = tx(Store.isFav(player.id) ? "★ 已收藏" : "☆ 收藏"); };
      star.onclick = async () => { await Store.toggleFav(player.id); paintStar(); };
      paintStar();
      const pk = cmp && cmp.fromOwned(player, schema);
      const vs = h("button", {type: "button", class: "ed-star"});
      const paintVs = () => { vs.classList.toggle("on", !!pk && cmp.has(pk.key)); t(vs, pk && cmp.has(pk.key) ? "移出对比" : "加入对比"); };
      vs.onclick = () => { if (!pk) return; cmp.setSchema(schema); if (cmp.add(pk)) U.toast("已加入对比"); paintVs(); };
      paintVs();
      return h("div", {class: "ed-hero-actions"}, star, vs);
    }
    const posName = (schema.positions || [])[player.position] || "";
    const art = U.portrait(player, 0); art.classList.add("ed-art");
    const card = h("div", {class: "ed-card3"}, art, h("span", {class: "ed-c-ovr"}, String(player.overall), h("small", {}, posName)));
    const roles = h("div", {class: "ed-roles"}); roles.textContent = tx([posName, player.card_type_label].filter(Boolean).join("  ·  "));
    const quick = (v, k) => { const s = h("span", {}, h("b", {}, String(v))); const l = h("small"); t(l, k); s.append(l); return s; };
    const dv = player.development || {};
    const plansLine = h("p", {class: "ed-plans"}); plansLine.textContent = tx(`实例 ${player.serial} · ${plans(player)}`);
    const hero = h("div", {class: "ed-hero3"}, card, h("div", {class: "ed-info"}, h("h2", {class: "ed-name"}, player.name || ""), roles,
      h("div", {class: "ed-quick"}, quick(player.overall, "总评"), quick(player.level, "等级"), quick(player.level_limit, "上限"), quick(dv.available ? dv.budget : "-", "培养点")), plansLine, heroActions()));
    const submit = h("button", {type: "button", class: "ed-btn wide primary"}); t(submit, "核对修改");
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
        submit.dataset.src = n ? `核对修改 · ${n} 项` : "核对修改"; submit.textContent = tx(submit.dataset.src);
        submit.classList.toggle("idle", n === 0);
      }, 30);
    };
    ["input", "change", "click", "ed-change"].forEach(ev => body.addEventListener(ev, sync));
    submit.onclick = () => U.run("正在核对修改…", async () => {
      const changes = {};
      for (const [, m] of tabs) if (m.apply) m.apply(changes);
      const dev = tabs[0][1].changes(); if (dev) changes.development = dev;
      const boosters = tabs[3][1].boosters();
      if (!Object.keys(changes).length && !boosters) { U.toast("尚未修改任何字段"); return; }
      const request = {id: player.id, serial: player.serial, changes}; if (boosters) request.boosters = boosters;
      const pv = await U.api("preview", request);
      if (!pv.changed) { U.toast("数据相同，无需修改"); return; }
      request.token = pv.token;
      const lines = h("div", {class: "ed-diff"}, pv.diff.map(c => {
        const row = h("div", {}), name = h("b"), val = h("span");
        name.textContent = tx(c.label); val.textContent = tx(U.diffValue(c.field, c.before, schema)) + "  →  " + tx(U.diffValue(c.field, c.after, schema));
        row.append(name, val); return row;
      }));
      const foot = h("p", {class: "ed-note"}); t(foot, "保存前自动备份；等级、培养点与培养记录一起保存；比赛统计和比赛计划保持。参考总评不在编辑器内重算，以游戏内计算为准。");
      const go = await U.sheet(`确认 ${pv.diff.length} 项修改`, `${player.name} · ${player.id} / ${player.serial}`,
        [{label: "返回编辑", value: false}, {label: "备份并保存", value: true, kind: "primary"}], h("div", {}, lines, foot));
      if (!go) return;
      const saved = await U.api("apply", request);
      let msg = saved.changed ? "已备份并保存，进入游戏检查效果。" : "数据相同，无需修改。";
      const rt = saved.live_condition_runtime;
      if (changes.condition !== undefined && rt && rt.status !== "installed") msg = "已备份并保存；实时状态尚待激活，请重启游戏后检查。";
      await U.sheet("保存完成", msg, [U.ok("返回列表")]); host.done();
    });
    const root = h("div", {class: "ed-detail"}, hero, bar, body, h("div", {class: "ed-submit"}, submit));
    sync();
    return {el: root};
  };
})();
