"use strict";
/* Live condition, main position, pitch aptitudes and play styles (PositionDraft / StyleChoice). */
(() => {
  const {h, t, tx, toast} = window.EditorUI.U, C = window.EditorCore;

  const select = (labels, selected, onChange) => {
    const s = h("select", {class: "ed-in"}, labels.map((l, i) => { const o = h("option", {value: i}); o.textContent = tx(l); return o; }));
    s.value = selected; if (onChange) s.onchange = onChange; return s;
  };

  window.EditorUI.pos = function (player, schema) {
    const grades = [4, 3, 2, 1, 0, -1], gradeNames = ["A", "B", "C", "D", "E", "跟随游戏"];
    const oldCondition = player.condition == null ? -1 : player.condition;
    let condition = oldCondition >= -1 && oldCondition <= 4 ? oldCondition : -1;
    const condLabel = h("p", {class: "ed-note"});
    const condBtns = grades.map((g, i) => h("button", {type: "button", class: "ed-cond", "data-k": g < 0 ? "x" : gradeNames[i], on: {click: () => { condition = g; paintCond(); t(condLabel, "待保存状态：" + gradeNames[i]); }}}, gradeNames[i]));
    condBtns[5].textContent = tx("跟随游戏"); condBtns[5].dataset.src = "跟随游戏";
    const paintCond = () => condBtns.forEach((b, i) => b.classList.toggle("on", grades[i] === condition));
    t(condLabel, "当前状态：" + window.EditorUI.U.diffValue("condition", oldCondition, schema)); paintCond();

    const positions = schema.positions || [], aptNames = schema.aptitudes || [];
    let main = player.position;
    const values = (player.aptitudes || []).slice(0, 13);
    values[C.aptitudeIndexForPosition(main)] = 2;
    const tiles = [];
    const mainTile = () => C.aptitudeIndexForPosition(main);
    const paintTiles = () => {
      const states = ["不熟练", "部分熟练", "完全熟练"];
      tiles.forEach((tile, i) => {
        const locked = i === mainTile();
        tile.dataset.state = values[i]; tile.classList.toggle("main", locked);
        tile.textContent = tx(aptNames[i] || "") + "\n" + tx(states[values[i]]) + (locked ? " · " + tx("主") : "");
      });
    };
    const band = (cols, tall) => h("div", {class: "ed-band" + (tall ? " tall" : "")}, cols.map(col => h("div", {class: "ed-col"}, col.map(i => {
      const tile = h("button", {type: "button", class: "ed-tile", on: {click: () => {
        const locked = i === mainTile(); values[i] = C.nextAptitude(values[i], locked); paintTiles();
        if (locked) toast("主位置保持完全熟练");
      }}}); tiles[i] = tile; return tile;
    }))));
    const pitch = h("div", {class: "ed-pitch"}, band([[2], [0, 1], [3]]), band([[7], [4, 6, 5], [8]], true), band([[10], [9, 12], [11]]));
    paintTiles();
    const posSel = select(positions, Math.max(0, main), () => { main = +posSel.value; values[mainTile()] = 2; paintTiles(); });

    const oldStyle = player.play_style, canStyle = Array.isArray(oldStyle) && oldStyle.length === 2 && oldStyle.every(v => Number.isInteger(v) && v >= 0 && v <= 63);
    const styleSel = [];
    const styleBox = h("div", {});
    if (canStyle) [0, 1].forEach(i => {
      const rows = (schema.play_styles || {})[i === 0 ? "attack" : "defense"] || [];
      const known = rows.some(r => r.id === oldStyle[i]);
      const opts = rows.map(r => ({id: r.id, label: r.label + " · ID " + r.id}));
      if (!known) opts.push({id: oldStyle[i], label: "保留原风格 · ID " + oldStyle[i]});
      const sel = select(opts.map(o => o.label), Math.max(0, opts.findIndex(o => o.id === oldStyle[i])));
      styleSel[i] = () => opts[+sel.value].id;
      const lab = h("p", {class: "ed-sub"}); t(lab, i === 0 ? "进攻风格" : "防守风格"); styleBox.append(lab, sel);
    });
    const styleNote = h("p", {class: "ed-note"}); t(styleNote, canStyle ? "两槽独立修改；选择无风格可清除此槽。风格在对应位置生效，以游戏内表现为准。" : "现有风格使用特殊格式，保持原数据。");

    const title = k => { const e = h("h4"); t(e, k); return e; };
    const el = h("div", {},
      title("实时状态（A/B/C/D/E）"), condLabel, h("div", {class: "ed-conds"}, condBtns),
      (() => { const n = h("p", {class: "ed-note"}); t(n, "同一卡种的所有副本共用实时状态；不影响状态持续性。保存后重新打开球员页面，下场比赛重新生成状态箭头。"); return n; })(),
      title("主位置（主位置适性须为完全熟练）"), posSel,
      (() => { const n = h("p", {class: "ed-note"}); t(n, "点按位置切换：灰色不熟练 → 部分熟练 → 完全熟练。主位置锁定完全熟练；不显示位置总评。"); return n; })(),
      pitch, (() => { const lg = h("div", {class: "ed-legend"}); [["0", "不熟练"], ["1", "部分熟练"], ["2", "完全熟练"]].forEach(([k, l]) => { const s = h("span", {}, h("i", {"data-state": k})); const x = h("em"); t(x, l); s.append(x); lg.append(s); }); return lg; })(), title("比赛风格"), styleBox, styleNote);

    return {el, apply(changes) {
      if (+posSel.value !== player.position) changes.position = +posSel.value;
      const apt = {}; values.forEach((v, i) => { if (v !== (player.aptitudes || [])[i]) apt[String(i + 1)] = v; });
      if (Object.keys(apt).length) changes.aptitudes = apt;
      if (condition !== oldCondition) changes.condition = condition;
      if (canStyle && (styleSel[0]() !== oldStyle[0] || styleSel[1]() !== oldStyle[1])) changes.play_style = [styleSel[0](), styleSel[1]()];
    }};
  };
})();
