"use strict";
/* Side-by-side comparison of two players (owned or from the full database).
   Values are read-only ability numbers in schema order; nothing is written anywhere. */
(() => {
  const U = window.EditorUI.U, {h, t, tx} = U, C = window.EditorCore;
  const slots = [];
  let schema = null, tray = null;
  const Cmp = {};
  window.EditorUI.compare = Cmp;

  Cmp.setSchema = s => { schema = s; };
  Cmp.has = key => slots.some(s => s.key === key);

  // entry: {key, name, overall, position (index), type, ab: number[] in schema order}
  Cmp.add = entry => {
    if (!Array.isArray(entry.ab) || !entry.ab.length) { U.toast("This player has no ability data to compare"); return false; }
    const i = slots.findIndex(s => s.key === entry.key);
    if (i >= 0) { slots.splice(i, 1); render(); return false; }
    slots.push(entry); if (slots.length > 2) slots.shift();
    render(); return true;
  };
  Cmp.clear = () => { slots.length = 0; render(); };
  Cmp.fromOwned = (player, sch) => {
    const order = (sch || schema || {}).abilities || [];
    return {key: "o" + player.id + "/" + player.serial, name: player.name, overall: player.overall, position: player.position, type: player.card_type_label || "",
      ab: order.map(a => (player.abilities || {})[String(a.index)] | 0)};
  };
  Cmp.fromCard = card => ({key: "c" + card.id, name: card.name, overall: card.overall, position: card.position, type: card.card_type_label || "", ab: card.ab});

  function render() {
    if (!tray) {
      tray = h("div", {class: "ed-tray", hidden: true});
      const host = document.getElementById("players"); if (host) host.append(tray);
    }
    tray.replaceChildren();
    tray.hidden = slots.length === 0;
    if (!slots.length) return;
    const label = h("span", {class: "ed-tray-text"});
    label.textContent = tx(slots.length === 1 ? `Compare 1/2 · ${slots[0].name}` : `${slots[0].name}  vs  ${slots[1].name}`);
    const go = h("button", {type: "button", class: "ed-tray-go", disabled: slots.length < 2, on: {click: open}}); t(go, "Compare");
    const x = h("button", {type: "button", class: "ed-tray-x", "aria-label": "clear", on: {click: Cmp.clear}}, "×");
    tray.append(label, go, x);
  }

  async function open() {
    if (slots.length < 2 || !schema) return;
    const [a, b] = slots, names = (schema.abilities || []), positions = schema.positions || [];
    let winA = 0, winB = 0;
    const head = who => { const d = h("div", {class: "ed-cmp-h"}, h("b", {}, who.name)); const s = h("small"); s.textContent = tx(`${positions[who.position] || ""} · ${who.type || ""} · ${who.overall}`); d.append(s); return d; };
    const rows = names.map((n, i) => {
      const va = a.ab[i] | 0, vb = b.ab[i] | 0;
      if (va > vb) winA++; else if (vb > va) winB++;
      const cell = (v, other) => { const c = h("b", {class: "ed-chip" + (v > other ? " win" : "")}, String(v)); c.dataset.band = C.abilityBand(v); return c; };
      const diff = h("small", {class: "ed-cmp-d"}); diff.textContent = va === vb ? "" : (va > vb ? "◀ " + (va - vb) : (vb - va) + " ▶");
      const label = h("span", {class: "ed-cmp-n"}); label.textContent = tx(n.label);
      return h("div", {class: "ed-cmp-row"}, cell(va, vb), h("div", {class: "ed-cmp-mid"}, label, diff), cell(vb, va));
    });
    const sum = h("p", {class: "ed-cmp-sum"}); sum.textContent = tx(`Leading: ${a.name} ${winA} · ${b.name} ${winB}`);
    const body = h("div", {class: "ed-cmp"}, h("div", {class: "ed-cmp-top"}, head(a), head(b)), sum, h("div", {class: "ed-cmp-rows"}, rows));
    const go = await U.sheet("Compare players", "", [{label: "Clear comparison", value: "clear"}, {label: "Close", value: true, kind: "primary"}], body);
    if (go === "clear") Cmp.clear();
  }
})();
