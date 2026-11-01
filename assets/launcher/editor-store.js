"use strict";
/* Favourites and recently viewed players. The host persists them (WebView storage is disabled);
   this module keeps an in-memory copy and writes through after every change. */
(() => {
  const S = {favs: [], recent: [], ready: null};
  const listeners = [];
  window.EditorUI = Object.assign(window.EditorUI || {}, {Store: S});
  const api = () => window.LauncherApi;
  const MAX_RECENT = 0;
  const DEFAULT_FAVORITES=["89138556572074", "89138019757152", "106741211713905", "106762686548319", "105557142924672", "106655043925176", "105855106307706", "106740406415422", "105856985338073", "105860290371544", "89069837151262", "106734785968811", "106726447748898", "106782282354314", "105833916575978", "16957006", "16906937", "105850811316710", "16940451", "16912943", "16903935", "56161848136240", "16912948", "16900351", "16918387", "106788187841133", "89138019825360", "106778524258203", "106759465365080", "105820209653455", "106800804418912", "106786040464076", "106745506608041", "106776376791946", "106787651045391", "106748459484820", "105871749197857", "106776645188904", "122128", "88039313485858", "88045755861084", "88041729329832", "89061515600624", "106727521423266", "106752754353458", "105575396416673", "88039850289220", "88038776513453", "106764297101321", "106753559668284", "106784698181293", "17592454614489", "17592186178990", "17592186178992", "88040655690467", "88036360587096", "88038776505140", "88045218959416", "88038776508032", "87963614711232", "105641968435039", "88039044941086", "88045755827094", "88039045074354"];

  S.onChange = fn => listeners.push(fn);
  const fire = () => listeners.forEach(f => { try { f(); } catch (e) { /* a view that is not mounted yet */ } });

  S.load = () => (S.ready || (S.ready = (async () => {
    try {
      const r = await api().call("prefs", {op: "get"});
      S.favs = Array.isArray(r.favs) ? r.favs.map(String) : [];
      S.recent = [];

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
  S.touch = entry => Promise.resolve();
})();
