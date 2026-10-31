"use strict";
/* Level / level limit / career-point allocation. Port of PlayerEditorPanel.DevelopmentDraft. */
(() => {
  const {h, t, tx} = window.EditorUI.U, C = window.EditorCore;
  const U = window.EditorUI.U;

  window.EditorUI.dev = function (player, schema) {
    const st = player.development, groups = schema.development_groups || [];
    const available = !!(st && st.available) && groups.length === 10;
    const old = player.abilities || {};
    const initialLevel = player.level || 1, initialLimit = player.level_limit || initialLevel;
    const levelCap = player.level_cap || C.DEFAULT_LEVEL_CAP, limitCap = Math.max(levelCap, initialLimit);
    const budget = available ? st.budget : 0;
    const original = groups.map(g => (available ? st.counts[g.key] : 0)), counts = original.slice();
    let level = initialLevel, limit = initialLimit;
    const names = {}; (schema.abilities || []).forEach(a => { names[a.index] = a.label; });

    const balance = () => (available ? C.remaining(budget, initialLevel, level, limit, counts) : 0);
    const ability = key => {
      if (!available) return old[key] || 0;
      const base = (st.base || {})[key] || 0; let inc = 0;
      groups.forEach((g, i) => { if (g.indices.includes(+key)) inc += counts[i]; });
      return C.developmentAbility(base, old[key] || 0, inc);
    };
    const stepCost = i => C.careerCost(counts[i] + 1) - C.careerCost(counts[i]);
    const canIncrease = i => {
      if (!available || counts[i] >= 1000) return false;
      return groups[i].indices.some(key => { const before = ability(key); counts[i]++; let after; try { after = ability(key); } finally { counts[i]--; } return after > before; });
    };
    const maximum = i => {
      if (!available) return counts[i];
      let cap = 0;
      groups[i].indices.forEach(key => { cap = Math.max(cap, Math.max(105, old[key] || 0) - ((st.base || {})[key] || 0)); });
      return C.allocationMaximum(counts[i], budget + 2 * (level - initialLevel), Math.max(0, cap));
    };
    const setCount = (i, target) => {
      target = C.allocationTarget(counts[i], target, balance());
      if (target < counts[i]) { counts[i] = Math.max(0, target); return; }
      while (counts[i] < Math.min(1000, target) && canIncrease(i) && balance() >= stepCost(i)) counts[i]++;
    };

    const levelLabel = h("div", {class: "ed-lv"}), balanceLabel = h("div", {class: "ed-bal"}), summary = h("div", {class: "ed-sum"});
    const upBtn = h("button", {type: "button", class: "ed-btn"}), limitBtn = h("button", {type: "button", class: "ed-btn wide"});
    t(upBtn, "Max Level");
    const panel = h("div", {class: "ed-alloc"}), expand = h("button", {type: "button", class: "ed-btn wide"}), panelBal = h("div", {class: "ed-bal sticky"});
    panel.append(panelBal);
    const rows = groups.map((g, i) => {
      const minus = h("button", {type: "button", class: "ed-step"}, "−"), plus = h("button", {type: "button", class: "ed-step"}, "+");
      const num = h("span", {class: "ed-num"}), range = h("input", {type: "range", min: 0, max: 1, step: 1, class: "ed-range"});
      const nameEl = h("b"), aff = h("small");
      t(nameEl, g.label); aff.textContent = g.indices.map(k => tx(names[k])).join(" · ");
      minus.onclick = () => { if (available && counts[i] > 0) { counts[i]--; refresh(); } };
      plus.onclick = () => { if (available && counts[i] < 1000 && canIncrease(i) && balance() >= stepCost(i)) { counts[i]++; refresh(); } };
      range.oninput = () => { if (available) { setCount(i, +range.value); refresh(); } };
      panel.append(h("div", {class: "ed-grp"}, h("div", {class: "ed-grp-top"}, h("div", {}, nameEl, aff), minus, num, plus), range));
      return {minus, plus, num, range};
    });

    const chips = {}, deltas = {};
    const left = [14, 18, 17, 19, 21, 22, 20, 23, 27, 28, 40, 16, 30, 32], right = [15, 24, 25, 26, 34, 38, 37, 39, 35, 36, -1, 29, 31, -1];
    const grid = h("div", {class: "ed-abil"});
    left.forEach((l, i) => [l, right[i]].forEach(key => {
      if (key < 0) { grid.append(h("div", {class: "ed-cell empty"})); return; }
      const chip = h("b", {class: "ed-chip"}), d = h("small");
      chips[key] = chip; deltas[key] = d;
      grid.append(h("div", {class: "ed-cell"}, h("span", {}, tx(names[key] || key)), d, chip));
    }));

    const short = window.LauncherApi.lang() === "en" ? ["Sht", "Pas", "Dri", "Dex", "Leg", "Air", "Def", "GK1", "GK2", "GK3"] : ["Shooting", "Passing", "Dribbling", "Agility", "Lower body", "Aerial", "Defending", "GK1", "GK2", "GK3"];
    function refresh() {
      const cap = (player.card_type_label || player.card_type || "") ? (player.card_type_label || player.card_type) + "Limit " : "Limit ";
      levelLabel.dataset.src = `Lv. ${level} / ${limit}  ·  ${cap} ${levelCap}`; levelLabel.textContent = tx(levelLabel.dataset.src);
      upBtn.disabled = !(available && level < Math.min(limit, levelCap));
      limitBtn.dataset.src = `Level limit  ${limit}  · Edit`; limitBtn.textContent = tx(limitBtn.dataset.src); limitBtn.disabled = !(available && level <= limitCap);
      balanceLabel.dataset.src = available ? `Available points  ${balance()}  · +2 per level` : (st ? (st.error || "Progression data needs checking.") : "Progression data is missing."); balanceLabel.textContent = tx(balanceLabel.dataset.src);
      panelBal.textContent = balanceLabel.textContent;
      summary.textContent = counts.map((c, i) => tx(short[i]) + c).join("  ");
      rows.forEach((r, i) => {
        r.range.max = maximum(i); r.range.value = counts[i]; r.range.disabled = !available;
        r.num.textContent = counts[i]; r.minus.disabled = !(available && counts[i] > 0);
        r.plus.disabled = !(available && counts[i] < 1000 && canIncrease(i) && balance() >= stepCost(i));
      });
      Object.keys(chips).forEach(key => {
        const next = ability(key), delta = next - (old[key] || 0);
        chips[key].textContent = next; chips[key].dataset.band = C.abilityBand(next); chips[key].parentNode.dataset.band = chips[key].dataset.band;
        deltas[key].textContent = delta === 0 ? "" : delta > 0 ? "+" + delta : String(delta);
      });
      if (typeof el !== "undefined") el.dispatchEvent(new CustomEvent("ed-change", {bubbles: true}));
    }
    upBtn.onclick = () => { if (available) { level = Math.max(initialLevel, Math.min(limit, levelCap)); refresh(); } };
    limitBtn.onclick = async () => {
      const input = h("input", {type: "number", inputmode: "numeric", class: "ed-in", value: limit});
      const note = h("p", {class: "ed-note"}); note.textContent = tx(`Adjusts the limit only; does not level up or grant training points. Range ${level}～${limitCap}` + (initialLimit > levelCap ? ` (original limit ${initialLimit} preserved)` : `；Limit ${levelCap} levels`));
      const presets = h("div", {class: "ed-row"}, (levelCap <= 10 ? [5, 8, 10] : [30, 40, 50]).map(n => h("button", {type: "button", class: "ed-btn", disabled: n < level, on: {click: () => { input.value = n; }}}, String(n))));
      const err = h("p", {class: "ed-err"});
      for (;;) {
        const go = await U.sheet("Edit Level Limit", "", [{label: "Cancel", value: false}, {label: "Apply to Draft", value: true, kind: "primary"}], h("div", {}, input, note, presets, err));
        if (!go) return;
        try { limit = C.levelLimit(input.value, level, levelCap, initialLimit); refresh(); return; } catch (e) { err.textContent = tx(e.message); }
      }
    };
    expand.onclick = () => { panel.hidden = !panel.hidden; t(expand, panel.hidden ? "Allocate Progression ▾" : "Collapse training items ▴"); };
    expand.disabled = !available; t(expand, "Collapse training items ▴"); panel.hidden = false;
    const reset = h("button", {type: "button", class: "ed-btn wide"}); t(reset, "Reset Progression Draft");
    reset.onclick = () => { level = initialLevel; limit = initialLimit; counts.splice(0, counts.length, ...original); refresh(); };
    const hint = h("p", {class: "ed-note"}); t(hint, "Abilities · No boosters · Read-only preview · Allocations capped at 105");
    const el = h("div", {}, h("div", {class: "ed-card"}, h("div", {class: "ed-row spread"}, levelLabel, upBtn), limitBtn, balanceLabel, summary), hint, grid, expand, panel, reset);
    refresh();
    return {el, changes() {
      if (!available || (level === initialLevel && limit === initialLimit && counts.every((c, i) => c === original[i]))) return null;
      const allocation = {}; groups.forEach((g, i) => { allocation[g.key] = counts[i]; });
      const out = {level, allocation}; if (limit !== initialLimit) out.level_limit = limit; return out;
    }};
  };
})();
