"use strict";
/* Favourites and recently viewed players. The host persists them (WebView storage is disabled);
   this module keeps an in-memory copy and writes through after every change. */
(() => {
  const S = {favs: [], recent: [], ready: null};
  const listeners = [];
  window.EditorUI = Object.assign(window.EditorUI || {}, {Store: S});
  const api = () => window.LauncherApi;
  const MAX_RECENT = 12;

  S.onChange = fn => listeners.push(fn);
  const fire = () => listeners.forEach(f => { try { f(); } catch (e) { /* a view that is not mounted yet */ } });

  S.load = () => (S.ready || (S.ready = (async () => {
    try {
      const r = await api().call("prefs", {op: "get"});
      S.favs = Array.isArray(r.favs) ? r.favs.map(String) : [];
      S.recent = Array.isArray(r.recent) ? r.recent : [];
    } catch (e) { S.favs = []; S.recent = []; }
    fire();
  })()));

  const save = (key, value) => api().call("prefs", {op: "set", key, value}).catch(() => { /* losing a star is not worth an error sheet */ });

  S.isFav = id => S.favs.includes(String(id));
  S.toggleFav = id => {
    id = String(id);
    S.favs = S.favs.includes(id) ? S.favs.filter(x => x !== id) : [id].concat(S.favs).slice(0, 300);
    fire(); return save("favs", S.favs).then(() => S.isFav(id));
  };

  // entry: {id, name, overall, position, kind: "owned"|"card", serial?}
  S.touch = entry => {
    const e = {id: String(entry.id), name: String(entry.name || ""), overall: entry.overall | 0, position: entry.position == null ? -1 : entry.position | 0, kind: entry.kind === "owned" ? "owned" : "card"};
    if (entry.serial != null) e.serial = entry.serial | 0;
    const same = x => x.id === e.id && x.kind === e.kind && (x.serial | 0) === (e.serial | 0);
    S.recent = [e].concat(S.recent.filter(x => !same(x))).slice(0, MAX_RECENT);
    fire(); return save("recent", S.recent);
  };
})();
