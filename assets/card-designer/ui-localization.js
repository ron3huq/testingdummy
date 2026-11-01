/* Shared display engine. Values and protocol objects never pass through this API. */
(() => {
  'use strict';
  const data = window.UiLocaleData;
  if (!data) throw new Error('UI locale data is missing');
  const escape = text => text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  let language = 'zh-CN', words = {}, templates = [], fragments;
  const locales = data.locales;
  function setLanguage(code) {
    if (!locales.some(locale => locale.code === code)) throw new Error('Unsupported UI language: ' + code);
    const next = data.data[code] || {words: {}, templates: []};
    language = code; words = next.words;
    templates = next.templates.map(row => ({...row, regex: new RegExp('^(?:' + row.pattern + ')$', 's')}));
    // Original English dictionary remains the fallback for legacy DIY English mode.
    if (code === 'en') words = window.DiyEnglishWords || {};
    const keys = Object.keys(words).filter(key => /[\u3400-\u9fff]/.test(key) && !/[%{}]/.test(key)).sort((a,b) => b.length-a.length);
    fragments = keys.length ? new RegExp(keys.map(escape).join('|'), 'g') : null;
  }
  function exact(text, depth = 0) {
    if (language === 'zh-CN' || depth > 6 || !text) return text;
    if (Object.prototype.hasOwnProperty.call(words, text)) return words[text];
    for (const template of templates) {
      const match = template.regex.exec(text);
      if (!match) continue;
      let n = 0;
      return template.output.replace(/%%|%s/g, token => token === '%%' ? '%' :
        (template.raw ? match[++n] : exact(match[++n], depth + 1)));
    }
    return text;
  }
  function t(value) { return exact(String(value ?? '')); }
  function display(value) {
    const text = String(value ?? ''), translated = exact(text);
    if (translated !== text || language === 'zh-CN' || !fragments) return translated;
    return text.replace(fragments, key => words[key]);
  }
  function applyDocument() {
    document.documentElement.lang = language;
    document.documentElement.dir = language === 'fa-IR' ? 'rtl' : 'ltr';
  }
  window.UiLocalization = {locales, setLanguage, t, display, applyDocument, get language(){ return language; }};
})();
