"use strict";
/* Shared helpers for the player editor modules. All text goes through textContent. */
(() => {
  const A = () => window.LauncherApi;
  const U = {locked: false};
  window.EditorUI = Object.assign(window.EditorUI || {}, {U});

  U.h = (tag, props, ...kids) => {
    const e = document.createElement(tag);
    for (const [k, v] of Object.entries(props || {})) {
      if (k === "class") e.className = v;
      else if (k === "on") for (const [ev, fn] of Object.entries(v)) e.addEventListener(ev, fn);
      else if (v === true) e.setAttribute(k, "");
      else if (v !== false && v != null) e.setAttribute(k, v);
    }
    kids.flat().forEach(c => { if (c != null && c !== false) e.append(c.nodeType ? c : document.createTextNode(String(c))); });
    return e;
  };
  U.tx = s => window.UiLocalization.display(String(s ?? ""));
  // Leaf element whose text is re-translated when the host finishes a batch.
  U.t = (el, s) => { el.dataset.src = s; el.textContent = U.tx(s); return el; };
  U.ph = (el, s) => { el.dataset.ph = s; el.placeholder = U.tx(s); return el; };
  U.refresh = root => {
    root.querySelectorAll("[data-src]").forEach(e => { e.textContent = U.tx(e.dataset.src); });
    root.querySelectorAll("[data-ph]").forEach(e => { e.placeholder = U.tx(e.dataset.ph); });
  };
  U.pre = async list => { const a=A(); for(const text of list)a.cache.set(text,U.tx(text)); };
  U.sheet = async (title, body, buttons, extra) => {
    await U.pre([title, body, ...buttons.map(b => b.label)]);
    return A().sheet(U.tx(title), U.tx(body || ""), buttons.map(b => Object.assign({}, b, {label: U.tx(b.label)})), extra);
  };
  U.ok = label => ({label: label || "OK", value: true, kind: "primary"});
  U.toast = msg => {
    const el = U.h("div", {class: "ed-toast"}); U.t(el, msg); document.body.append(el);
    setTimeout(() => el.remove(), 1900);
  };
  U.api = (op, payload) => A().call("editor", {op, payload: payload || {}});
  // One long operation at a time; failures become a sheet, never a silent no-op.
  U.run = async (msg, fn) => {
    if (U.locked) return undefined;
    U.locked = true; A().meter(true); A().progress(U.tx(msg));
    try { return await fn(); }
    catch (e) { await U.sheet("Edit Failed", e.message || "Please try again.", [U.ok()]); return undefined; }
    finally { U.locked = false; A().meter(false); A().progress(""); }
  };

  // Visible portraits only. Shared jobs and revision keys keep scrolling light.
  const cache=new Map(),jobs=new Map(),queue=[];let active=0;
  const paint=(el,url)=>{if(el.isConnected&&url){el.style.backgroundImage=`url(${url})`;el.classList.add("on");el.dataset.art=url.startsWith("http")?"card":"head";}};
  const keyFor=el=>el.dataset.id+"/"+el.dataset.rev;
  const remember=(key,url)=>{cache.delete(key);cache.set(key,url);while(cache.size>160)cache.delete(cache.keys().next().value);};
  function remote(id){return new Promise(resolve=>{const img=new Image();const timer=setTimeout(()=>{img.src="";resolve(null)},2500);img.onload=()=>{clearTimeout(timer);resolve(img.src)};img.onerror=()=>{clearTimeout(timer);resolve(null)};img.src="https://efimg.com/efootballhub22/images/player_cards/"+id+"_l.png";});}
  async function load(id){const r=await U.api("portrait",{id});if(r.found)return r.url||"data:image/png;base64,"+r.png;return remote(id);}
  function pump(){while(active<4&&queue.length){const job=queue.shift();job.targets=job.targets.filter(el=>el.isConnected&&keyFor(el)===job.key);if(!job.targets.length){jobs.delete(job.key);continue;}active++;load(job.id).then(url=>{if(url)remember(job.key,url);job.targets.forEach(el=>{if(keyFor(el)===job.key)paint(el,url)});}).catch(()=>{}).finally(()=>{active--;jobs.delete(job.key);pump();});}}
  function request(el){const key=keyFor(el);if(cache.has(key)){paint(el,cache.get(key));return;}let job=jobs.get(key);if(!job){job={key,id:el.dataset.id,targets:[]};jobs.set(key,job);queue.push(job);}job.targets.push(el);pump();}
  const seen=new IntersectionObserver(rows=>rows.forEach(row=>{if(row.isIntersecting){seen.unobserve(row.target);request(row.target);}}),{rootMargin:"120px"});
  U.portrait=(p,size)=>{const el=U.h("span",{class:"pt"});if(size)el.style.width=el.style.height=size+"px";if(/^[0-9]{1,18}$/.test(String(p.id))){el.dataset.id=String(p.id);el.dataset.rev=String(p.portrait_revision??0);seen.observe(el);}return el;};
  U.refreshPortrait=async id=>{id=String(id);for(const key of [...cache.keys()])if(key.startsWith(id+"/"))cache.delete(key);const rev="saved-"+Date.now();document.querySelectorAll(".pt[data-id]").forEach(el=>{if(el.dataset.id===id){el.dataset.rev=rev;request(el);}});};

  // Same wording rules as PlayerEditorPanel.diffValue.
  U.diffValue = (field, value, s) => {
    const find = (rows, id) => (rows || []).filter(r => r.id === id).pop();
    if (field === "boosters" && Array.isArray(value))
      return value.map((id, i) => { const r = find(s.boosters, id); return "Slot" + (i + 1) + "：" + (r ? r.label : id === 0 ? "Disabled" : id === 136 ? "Unimplemented (empty slot)" : "Keep original booster · ID " + id); }).join(" / ");
    if (field === "play_style" && Array.isArray(value))
      return [0, 1].map(i => { const r = find(((s.play_styles || {})[i === 0 ? "attack" : "defense"]), value[i]); return (i === 0 ? "Attack: " : "Defence: ") + (r ? r.label : "Keep original style · ID " + value[i]); }).join(" / ");
    if (field === "skills" && Array.isArray(value))
      return value.length ? value.map(id => { const r = find(s.skills, id); return r ? r.label : "ID " + id; }).join("、") : "None";
    if (field.startsWith("aptitude:") && typeof value === "number") return value >= 0 && value <= 2 ? ["Untrained", "Partial", "Proficient"][value] : String(value);
    if (field === "condition" && typeof value === "number") return value >= 0 && value <= 4 ? "EDCBA"[value] : value === -1 ? "Game default" : "Original form value " + value;
    return String(value);
  };
})();
