"use strict";
/* Skills, boosters and look/celebration tabs. Ports of the matching blocks in PlayerEditorPanel.choose / BoosterDraft. */
(() => {
  const {h, t, tx} = window.EditorUI.U, U = window.EditorUI.U, C = window.EditorCore;
  const select = (labels, selected) => {
    const s = h("select", {class: "ed-in"}, labels.map((l, i) => { const o = h("option", {value: i}); o.textContent = tx(l); return o; }));
    s.value = selected; return s;
  };
  const title = (k, tag) => { const e = h(tag || "h4"); t(e, k); return e; };
  const note = k => { const e = h("p", {class: "ed-note"}); t(e, k); return e; };
  const sub = k => { const e = h("p", {class: "ed-sub"}); t(e, k); return e; };

  window.EditorUI.skills = function (player, schema) {
    const cat = schema.skills || [], oldSkills = player.additional_skills || [], innate = player.innate_skills || [];
    const el = h("div", {});
    el.append(title(`已有固有技能 · ${innate.length} 项`, "h3"), note("随卡自带，保留原技能；下方10个附加槽单独编辑。"));
    if (!innate.length) el.append(note("暂无固有技能"));
    const inn = h("div", {class: "ed-chipsrow"});
    innate.forEach(id => { const r = cat.find(s => s.id === id); const c = h("span", {class: "ed-skill gold"}); c.textContent = r ? r.label : "技能 · ID " + id; inn.append(c); });
    el.append(inn);
    const head = title("", "h3"); el.append(head, note("全技能目录：68项已命名技能＋6项原生预留；点按空槽选择技能，可搜索。固有与重复项不可选。"));
    const ids = cat.map(s => s.id), label = i => (i > 0 ? cat[i - 1].label : "");
    let known = oldSkills.length <= 10;
    const values = [];
    for (let n = 0; n < 10; n++) {
      let selected = 0;
      if (n < oldSkills.length) { const i = ids.indexOf(oldSkills[n]); if (i >= 0) selected = i + 1; else known = false; }
      values.push(selected);
    }
    const slots = h("div", {class: "ed-slots"});
    const paint = () => {
      head.dataset.src = `已学附加技能 · ${values.filter(Boolean).length} / 10`; head.textContent = tx(head.dataset.src);
      slots.replaceChildren(...values.map((v, n) => {
        const b = h("button", {type: "button", class: "ed-slot" + (v ? " on" : ""), disabled: !known, on: {click: () => pick(n)}});
        const idx = h("i"); idx.textContent = String(n + 1);
        const txt = h("span"); if (v) txt.textContent = tx(label(v)); else t(txt, "空槽");
        b.append(idx, txt); return b;
      }));
    };
    async function pick(n) {
      const q = h("input", {type: "search", class: "ed-in", autocomplete: "off"}); U.ph(q, "搜索技能名称");
      const list = h("div", {class: "ed-pick"});
      let chosen = null;
      const draw = () => {
        const key = q.value.trim().toLowerCase();
        list.replaceChildren(...cat.map((s, i) => ({s, i: i + 1})).filter(({s}) => !key || (s.label + " " + s.id).toLowerCase().includes(key)).map(({s, i}) => {
          const taken = innate.includes(s.id) || values.some((v, k) => v === i && k !== n);
          const b = h("button", {type: "button", class: "ed-pickrow" + (values[n] === i ? " on" : ""), disabled: taken, on: {click: () => { chosen = i; document.querySelector("#sheet-actions .btn").click(); }}});
          b.textContent = tx(s.label) + (innate.includes(s.id) ? tx("（固有）") : values.some((v, k) => v === i && k !== n) ? tx("（已在其他槽）") : "");
          return b;
        }));
      };
      q.addEventListener("input", draw); draw();
      const r = await U.sheet(`附加槽 ${n + 1}`, "", [{label: "取消", value: false}, {label: "清空此槽", value: "clear"}], h("div", {}, q, list));
      if (chosen != null) values[n] = chosen; else if (r === "clear") values[n] = 0; else return;
      paint(); el.dispatchEvent(new CustomEvent("ed-change", {bubbles: true}));
    }
    const clear = h("button", {type: "button", class: "ed-btn wide", disabled: !known, on: {click: () => { values.fill(0); paint(); el.dispatchEvent(new CustomEvent("ed-change", {bubbles: true})); }}}); t(clear, "清空附加技能");
    el.append(slots, clear);
    if (!known) el.append(note("现有技能使用特殊格式，本页保持原数据。"));
    paint();
    return {el, apply(changes) {
      if (!known) return;
      const skills = C.skills(values.slice(), ids);
      if (JSON.stringify(skills) !== JSON.stringify(oldSkills)) changes.skills = skills;
    }};
  };
  window.EditorUI.boosters = function (player, schema) {
    const cur = player.boosters || [0, 0, 0], cat = (schema.boosters || []).filter(r => {const label=tx(r.label || "");const match=label.match(/\+\s*(\d+)/);return !/total\s*package|全能|全套/i.test(label) && match && Number(match[1])>=4;}).sort((a,b)=>Number(tx(a.label).match(/\+\s*(\d+)/)[1])-Number(tx(b.label).match(/\+\s*(\d+)/)[1])), limits = schema.editor_booster_limits || [0, 0, 0];
    const original = [0, 1, 2].map(i => cur[i] || 0), remembered = [], enabled = original.map(v => v !== 0 && v !== 136), touched = [false, false, false];
    const desc = {}; cat.forEach(r => { desc[r.id] = r.description || ""; });
    const el = h("div", {}), toggles = [], selects = [], details = [], ids = [];
    const top = h("div", {class: "ed-row"}); el.append(top);
    const paint = () => [0, 1, 2].forEach(i => {
      toggles[i].textContent = tx(`增能 ${i + 1} · ${enabled[i] ? "已启用" : "未启用"}`); toggles[i].classList.toggle("on", enabled[i]);
      selects[i].disabled = !enabled[i]; details[i].hidden = !enabled[i];
    });
    [0, 1, 2].forEach(n => {
      const opts = cat.filter(r => r.id <= limits[n]).map(r => ({id: r.id, label: r.label}));
      let sel = opts.findIndex(o => o.id === original[n]);
      if (enabled[n] && sel < 0) { opts.push({id: original[n], label: "保留原增能 · ID " + original[n]}); sel = opts.length - 1; }
      if (sel < 0) sel = 0;
      ids[n] = opts.map(o => o.id); remembered[n] = ids[n][sel];
      toggles[n] = h("button", {type: "button", class: "ed-btn big", on: {click: () => { enabled[n] = !enabled[n]; touched[n] = true; paint(); }}});
      selects[n] = select(opts.map(o => o.label), sel);
      details[n] = h("p", {class: "ed-note"}); details[n].textContent = tx(desc[remembered[n]] || "原增能保持");
      selects[n].onchange = () => {
        const v = ids[n][+selects[n].value]; if (remembered[n] !== v) { remembered[n] = v; touched[n] = true; }
        details[n].textContent = tx(desc[v] || "原增能保持");
      };
      top.append(toggles[n]); el.append(sub(`增能槽 ${n + 1}`), selects[n], details[n]);
    });
    el.append(note("全部增能目录 · 条件增能满足对应条件才生效。关闭后保留本次选择；再次点击恢复。")); paint();
    return {el, boosters() {
      const slots = original.map((o, i) => (touched[i] ? (enabled[i] ? remembered[i] : 0) : o));
      return slots.some((v, i) => v !== original[i]) ? slots : null;
    }};
  };

  window.EditorUI.look = function (player, schema) {
    const el = h("div", {});
    const old = {celebration: player.celebration, canCel: Number.isInteger(player.celebration)};
    el.append(title("进球庆祝", "h3"), note("按球员名称复制基础进球动作和纪念庆祝；下场比赛查看，比赛中选择该球员庆祝。"));
    let celIds = [old.celebration], celSel = select(["保持当前"], 0); celSel.disabled = true; el.append(celSel);
    let loaded = false, loading = false;
    el.append(title("固定动作组合（实验）", "h3"), note("选择会替换完整 p51–p59 动作组合，不是单独的进球庆祝；p60 纪念庆祝保持不变。具体比赛动画仍待设备验收。"));
    const motions = schema.motion_profiles || [], motionIds = [""].concat(motions.map(m => m.id));
    let motionStart = Math.max(0, motionIds.indexOf(player.motion_profile || ""));
    const motionSel = select(["保持当前组合"].concat(motions.map(m => m.label)), motionStart); el.append(motionSel);
    const ap = schema.appearance || {}, state = player.appearance || null;
    el.append(title("外观选择", "h3"), note("保存后下场比赛生效；同一卡号的副本共用球鞋和袖长设置。"));
    const bootRows = ap.boots || [], bootIds = [-1].concat(bootRows.map(b => b.id));
    let bootStart = 0; if (state && state.boots_id != null) bootStart = Math.max(0, bootIds.indexOf(state.boots_id));
    const bootSel = select(["保持当前球鞋"].concat(bootRows.map(b => b.label)), bootStart);
    const sleeveRows = ap.sleeves || [], sleeveIds = sleeveRows.map(s => s.id);
    let sleeveStart = Math.max(0, sleeveIds.indexOf(state ? state.sleeve || "keep" : "keep"));
    const sleeveSel = select(sleeveRows.map(s => s.label), sleeveStart);
    el.append(sub("球鞋"), bootSel, sub("袖长"), sleeveSel, note("球鞋显示已核验型号；没有可靠名称的条目保留目录编号。颜色尚无可靠标签。"));
    return {el, boots: bootSel,
      async onShow() {
        if (loaded || loading || !old.canCel) return;
        loading = true;
        try {
          const r = await U.api("celebrations"), rows = r.choices || [];
          const list = rows.filter(x => !x.value || x.value.goal_performance !== (player.celebration_pair || {}).goal_performance || x.value.memorial_celebration !== old.celebration);
          celIds = [old.celebration].concat(list.map(x => x.value || x.id));
          const next = select(["保持当前"].concat(list.map(x => x.label)), 0); celSel.replaceWith(next); celSel = next; celSel.disabled = celIds.length < 2; loaded = true;
        } catch (e) { /* keep the single "keep current" option */ } finally { loading = false; }
      },
      apply(changes) {
        if (old.canCel && +celSel.value > 0) changes.celebration = celIds[+celSel.value];
        if (+motionSel.value !== motionStart && +motionSel.value > 0) changes.motion_profile = motionIds[+motionSel.value];
        if (+bootSel.value !== bootStart || +sleeveSel.value !== sleeveStart) {
          const id = bootIds[+bootSel.value], a = {boots_id: id < 0 ? null : id, sleeve: sleeveIds[+sleeveSel.value]};
          if (state && state.base_player_id) a.base_player_id = state.base_player_id;
          changes.appearance = a;
        }
      }};
  };
})();
