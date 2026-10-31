"use strict";
(() => {
 const U=window.EditorUI.U,{h}=U;
 const open=(tool,player)=>U.api("privateTool",{tool,player:{id:String(player.id),serial:Number(player.serial),name:player.name||""}});
 window.EditorUI.privateTools=(player)=>{
  const el=h("div",{class:"private-tools"});
  const groups=[
   ["Appearance & Motion",[["model","Player Model","Current proportions and body shape"],["measurements","Height & Weight","Native limits: 140–220 cm · 40–130 kg"],["equipment","Equipment & Card Art","Sleeves, socks, accessories, colours and portrait import"],["skin-celebration","Skin & Celebrations","Game skin palettes and celebration IDs"],["motion","Animation","Copy a donor or edit individual motion values"]]],
   ["Player Profile",[["identity","Identity & Model Copy","Name, shirt name, age, affiliation and model donor"],["traits","Foot & Resistance","Preferred foot, weak foot and injury resistance"],["stats","Abilities","Edit native ability values within verified storage limits"],["skills","Existing Player Skills","Read, add or remove this card’s innate skills"]]]];
  for(const [title,allItems]of groups){const items=allItems.filter(row=>!["traits","stats","skills"].includes(row[0]));el.append(h("h3",{},title));const grid=h("div",{class:"private-grid"});for(const [tool,label,description]of items){const button=h("button",{type:"button",class:"private-tool"},h("b",{},label),h("small",{},description));button.onclick=()=>U.run("Opening "+label+"…",()=>open(tool,player));grid.append(button);}el.append(grid);}
  el.append(h("p",{class:"ed-note"},"Save before Enter Game. Reopen the app after changing native appearance. Existing unsaved training changes are separate."));return {el};
 };
 const originalLook=window.EditorUI.look;
 window.EditorUI.look=(player,schema)=>{const native=originalLook(player,schema),panel=window.EditorUI.privateTools(player);panel.el.prepend(h("h3",{},"Boots"),native.boots);return {el:panel.el,apply:changes=>native.apply(changes)};};
 for(const [method,tool,label]of [["dev","stats","Edit abilities"],["pos","traits","Preferred foot · Weak foot · Injury resistance"],["skills","skills","Add or remove existing player skills"]]){
  const original=window.EditorUI[method];window.EditorUI[method]=(player,schema)=>{const panel=original(player,schema);const button=h("button",{type:"button",class:"private-tool"},h("b",{},label));button.onclick=()=>U.run("Opening editor…",()=>open(tool,player));panel.el.append(button);return panel;};
 }
 window.PrivateTransfer={enter(){U.run("Opening Transfer…",()=>U.api("privateTool",{tool:"transfer"}));}};
})();
