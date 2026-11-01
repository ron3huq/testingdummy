/* Display-only localization. Project payloads, IDs and input values stay untouched. */
(() => {
  'use strict';
  const words = window.DiyEnglishWords || {};
  const chinese = /[\u3400-\u9fff]/;
  const escape = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const keys = Object.keys(words).filter(k => k && chinese.test(k)).sort((a,b) => b.length-a.length);
  const pattern = new RegExp(keys.map(escape).join('|'), 'g');
  let language = 'en';
  if (!window.UiLocalization.locales.some(row => row.code === language)) language = 'en';
  window.UiLocalization.setLanguage(language);
  const originals = new WeakMap(), attributes = new WeakMap();
  const skip = 'script,style,textarea,canvas,[contenteditable="true"],[data-i18n-user],#player,#labTitle,#labDeleteName,#cardName,#cardImportName,.lab-work-edit>strong,.lab-work-preview img';
  function t(value) {
    const text = String(value ?? '');
    if (language !== 'en') return window.UiLocalization.display(text);
    if (!chinese.test(text)) return text;
    return text.replace(pattern, key => words[key])
      .replace(/，/g, ', ').replace(/。/g, '. ').replace(/：/g, ': ')
      .replace(/；/g, '; ').replace(/（/g, '(').replace(/）/g, ')')
      .replace(/「|」|“|”/g, '"').replace(/？/g, '?');
  }
  function userText(node) {
    const parent = node.nodeType === 1 ? node : node.parentElement;
    return !parent || !!parent.closest(skip);
  }
  function textNode(node) {
    if (userText(node)) return;
    const previous = originals.get(node), current = node.nodeValue;
    const source = previous && current === previous.translated ? previous.source : current;
    const translated = t(source);
    originals.set(node, {source, translated});
    if (current === translated) return;
    // An option without an explicit value otherwise derives its protocol value
    // from its displayed text. Pin that value before changing its label.
    const option = node.parentElement;
    if (option?.tagName === 'OPTION' && !option.hasAttribute('value')) option.value = option.value;
    node.nodeValue = translated;
  }
  function element(node) {
    if (userText(node)) return;
    const saved = attributes.get(node) || {};
    for (const name of ['placeholder','title','aria-label','alt','label']) {
      if (!node.hasAttribute(name)) continue;
      const current = node.getAttribute(name), previous = saved[name];
      const source = previous && current === previous.translated ? previous.source : current;
      const translated = t(source); saved[name] = {source, translated};
      if (current !== translated) node.setAttribute(name, translated);
    }
    attributes.set(node, saved);
  }
  function walk(root) {
    if (!root || !root.isConnected) return;
    if (root.nodeType === 3) { textNode(root); return; }
    if (root.nodeType === 1) element(root);
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT);
    let node; while ((node = walker.nextNode())) node.nodeType === 3 ? textNode(node) : element(node);
  }
  const pending = new Set(); let scheduled = false, observer;
  const options = {subtree:true, childList:true, characterData:true, attributes:true,
    attributeFilter:['placeholder','title','aria-label','alt','label']};
  function flush() {
    scheduled = false; observer.disconnect();
    for (const node of pending) walk(node);
    pending.clear(); observer.observe(document.documentElement, options);
  }
  function refresh() { pending.add(document.documentElement); flush(); }
  observer = new MutationObserver(records => {
    for (const record of records) {
      if (record.type === 'childList') for (const node of record.addedNodes) pending.add(node);
      else pending.add(record.target);
    }
    if (!scheduled) { scheduled = true; queueMicrotask(flush); }
  });
  function setLanguage(value) {
    value = "en";
    window.UiLocalization.setLanguage(value); language = value;
    window.UiLocalization.applyDocument(); refresh();
    window.dispatchEvent(new CustomEvent('diy-language-changed', {detail:language}));
  }
  window.UiLocalization.applyDocument();
  observer.observe(document.documentElement, options);
  for (const name of ['alert','confirm','prompt']) {
    const original = window[name].bind(window);
    window[name] = (message, ...args) => original(t(message), ...args);
  }
  window.DiyI18n = {t, refresh, setLanguage, get language(){return language;}};
  document.addEventListener('DOMContentLoaded', refresh);
})();
