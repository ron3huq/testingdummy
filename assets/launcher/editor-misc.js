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
    el.append(title(`Existing Skills · ${innate.length}`, "h3"), note("The card’s existing skills are shown here. Edit the 10 additional slots separately below."));
    if (!innate.length) el.append(note("No existing skills"));
    const inn = h("div", {class: "ed-chipsrow"});
    innate.forEach(id => { const r = cat.find(s => s.id === id); const c = h("span", {class: "ed-skill gold"}); c.textContent = r ? r.label : "Skills · ID " + id; inn.append(c); });
    el.append(inn);
    const head = title("", "h3"); el.append(head, note("Search the skill catalogue or tap an empty slot. Existing skills and duplicates cannot be selected twice."));
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
      head.dataset.src = `Additional Skills · ${values.filter(Boolean).length} / 10`; head.textContent = tx(head.dataset.src);
      slots.replaceChildren(...values.map((v, n) => {
        const b = h("button", {type: "button", class: "ed-slot" + (v ? " on" : ""), disabled: !known, on: {click: () => pick(n)}});
        const idx = h("i"); idx.textContent = String(n + 1);
        const txt = h("span"); if (v) txt.textContent = tx(label(v)); else t(txt, "Empty slot");
        b.append(idx, txt); return b;
      }));
    };
    async function pick(n) {
      const q = h("input", {type: "search", class: "ed-in", autocomplete: "off"}); U.ph(q, "Search skills");
      const list = h("div", {class: "ed-pick"});
      let chosen = null;
      const draw = () => {
        const key = q.value.trim().toLowerCase();
        list.replaceChildren(...cat.map((s, i) => ({s, i: i + 1})).filter(({s}) => !key || (s.label + " " + s.id).toLowerCase().includes(key)).map(({s, i}) => {
          const taken = innate.includes(s.id) || values.some((v, k) => v === i && k !== n);
          const b = h("button", {type: "button", class: "ed-pickrow" + (values[n] === i ? " on" : ""), disabled: taken, on: {click: () => { chosen = i; document.querySelector("#sheet-actions .btn").click(); }}});
          b.textContent = tx(s.label) + (innate.includes(s.id) ? tx("(Innate)") : values.some((v, k) => v === i && k !== n) ? tx(" (in another slot)") : "");
          return b;
        }));
      };
      q.addEventListener("input", draw); draw();
      const r = await U.sheet(`Additional slot ${n + 1}`, "", [{label: "Cancel", value: false}, {label: "Clear this slot", value: "clear"}], h("div", {}, q, list));
      if (chosen != null) values[n] = chosen; else if (r === "clear") values[n] = 0; else return;
      paint(); el.dispatchEvent(new CustomEvent("ed-change", {bubbles: true}));
    }
    const clear = h("button", {type: "button", class: "ed-btn wide", disabled: !known, on: {click: () => { values.fill(0); paint(); el.dispatchEvent(new CustomEvent("ed-change", {bubbles: true})); }}}); t(clear, "Clear Additional Skills");
    el.append(slots, clear);
    if (!known) el.append(note("Existing skills use an unsupported format; original data is preserved."));
    paint();
    return {el, apply(changes) {
      if (!known) return;
      const skills = C.skills(values.slice(), ids);
      if (JSON.stringify(skills) !== JSON.stringify(oldSkills)) changes.skills = skills;
    }};
  };
  window.EditorUI.boosters = function (player, schema) {
    const cur = player.boosters || [0, 0, 0], cat = (schema.boosters || []).filter(r => {const label=tx(r.label || "");const match=label.match(/\+\s*(\d+)/);return !/total\s*package|Total Package|Total Package/i.test(label) && match && Number(match[1])>=4;}).sort((a,b)=>Number(tx(a.label).match(/\+\s*(\d+)/)[1])-Number(tx(b.label).match(/\+\s*(\d+)/)[1])), limits = schema.editor_booster_limits || [0, 0, 0];
    const original = [0, 1, 2].map(i => cur[i] || 0), remembered = [], enabled = original.map(v => v !== 0 && v !== 136), touched = [false, false, false];
    const desc = {}; cat.forEach(r => { desc[r.id] = r.description || ""; });
    const el = h("div", {}), toggles = [], selects = [], details = [], ids = [];
    const top = h("div", {class: "ed-row"}); el.append(top);
    const paint = () => [0, 1, 2].forEach(i => {
      toggles[i].textContent = tx(`Booster ${i + 1} · ${enabled[i] ? "Enabled" : "Disabled"}`); toggles[i].classList.toggle("on", enabled[i]);
      selects[i].disabled = !enabled[i]; details[i].hidden = !enabled[i];
    });
    [0, 1, 2].forEach(n => {
      const opts = cat.filter(r => r.id <= limits[n]).map(r => ({id: r.id, label: r.label}));
      let sel = opts.findIndex(o => o.id === original[n]);
      if (enabled[n] && sel < 0) { el.append(note("Current booster is preserved until you choose a replacement.")); }
      if (sel < 0) sel = 0;
      ids[n] = opts.map(o => o.id); remembered[n] = ids[n][sel];
      toggles[n] = h("button", {type: "button", class: "ed-btn big", on: {click: () => { enabled[n] = !enabled[n]; touched[n] = true; paint(); }}});
      selects[n] = select(opts.map(o => o.label), sel);
      details[n] = h("p", {class: "ed-note"}); details[n].textContent = tx(desc[remembered[n]] || "Original booster kept");
      selects[n].onchange = () => {
        const v = ids[n][+selects[n].value]; if (remembered[n] !== v) { remembered[n] = v; touched[n] = true; }
        details[n].textContent = tx(desc[v] || "Original booster kept");
      };
      top.append(toggles[n]); el.append(sub(`Booster slot ${n + 1}`), selects[n], details[n]);
    });
    el.append(note("Full booster catalogue · conditional boosters apply only when their condition is met. Closing keeps the current choice; tap again to restore.")); paint();
    return {el, boosters() {
      const slots = original.map((o, i) => (touched[i] ? (enabled[i] ? remembered[i] : 0) : o));
      return slots.some((v, i) => v !== original[i]) ? slots : null;
    }};
  };

  window.EditorUI.look = function (player, schema) {
    const el = h("div", {});
    const old = {celebration: player.celebration, canCel: Number.isInteger(player.celebration)};
    el.append(title("Goal Celebration", "h3"), note("Choose a player to copy the goal celebration. Check the selected player in the next match."));
    let celIds = [old.celebration], celSel = select(["Keep current"], 0); celSel.disabled = true; el.append(celSel);
    let loaded = false, loading = false;
    el.append(title("Native Motion Set", "h3"), note("Replaces motion fields p51–p59. Celebration p60 is preserved. In-game animation needs device confirmation."));
    const motions = schema.motion_profiles || [], motionIds = [""].concat(motions.map(m => m.id));
    let motionStart = Math.max(0, motionIds.indexOf(player.motion_profile || ""));
    const motionSel = select(["Keep current motion"].concat(motions.map(m => m.label)), motionStart); el.append(motionSel);
    const ap = schema.appearance || {}, state = player.appearance || null;
    el.append(title("Appearance Options", "h3"), note("Save before the next match. Copies of the same card share boots and sleeves."));
    const bootRows = ap.boots || [], bootIds = [-1].concat(bootRows.map(b => b.id));
    let bootStart = 0; if (state && state.boots_id != null) bootStart = Math.max(0, bootIds.indexOf(state.boots_id));
    const bootSel = select(["Keep current boots"].concat(bootRows.map(b => b.label)), bootStart);
    const sleeveRows = ap.sleeves || [], sleeveIds = sleeveRows.map(s => s.id);
    let sleeveStart = Math.max(0, sleeveIds.indexOf(state ? state.sleeve || "keep" : "keep"));
    const sleeveSel = select(sleeveRows.map(s => s.label), sleeveStart);
    el.append(sub("Boots"), bootSel, sub("Sleeve length"), sleeveSel, note("Verified boot models use their names. Unidentified entries retain their catalogue ID."));
    return {el, boots: bootSel,
      async onShow() {
        if (loaded || loading || !old.canCel) return;
        loading = true;
        try {
          const r = await U.api("celebrations"), rows = r.choices || [];
          const list = rows.filter(x => !x.value || x.value.goal_performance !== (player.celebration_pair || {}).goal_performance || x.value.memorial_celebration !== old.celebration);
          celIds = [old.celebration].concat(list.map(x => x.value || x.id));
          const next = select(["Keep current"].concat(list.map(x => x.label)), 0); celSel.replaceWith(next); celSel = next; celSel.disabled = celIds.length < 2; loaded = true;
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
