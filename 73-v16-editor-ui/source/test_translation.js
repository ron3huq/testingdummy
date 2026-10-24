const vm=require('vm'),fs=require('fs'),assert=require('assert');
let queued=[],observe;
function el(tag,children=[],attrs={}){const e={nodeType:1,tagName:tag,childNodes:children,isConnected:true,attributes:attrs,hasAttribute(k){return k in this.attributes},getAttribute(k){return this.attributes[k]},setAttribute(k,v){this.attributes[k]=v},closest(){return ['SCRIPT','STYLE','TEXTAREA','CODE','PRE'].includes(this.tagName)?this:null}};for(const c of children)c.parentElement=e;return e;}
function text(s){return{nodeType:3,nodeValue:s,isConnected:true};}
const heading=text('球员卡面 · 布局工坊'),status=text('正在读取球员头像…'),code=text('球员姓名');const input=el('INPUT',[],{placeholder:'搜索模型'});input.value='张三';const root=el('HTML',[el('H1',[heading]),el('P',[status]),el('SCRIPT',[code]),input]);
const alerts=[];const window={alert(s){alerts.push(s)},confirm(s){alerts.push(s);return true},prompt(s){alerts.push(s);return 'original-response'}};
const context={document:{documentElement:root},window,MutationObserver:class{constructor(cb){observe=cb}observe(){}},setTimeout(cb){queued.push(cb);return queued.length},console};vm.runInNewContext(fs.readFileSync('/workspace/ronaldo-work/73-ui/editor-english.js','utf8'),context);
assert.equal(root.lang,'en');assert.equal(heading.nodeValue,'Player cards · Layout studio');assert.equal(status.nodeValue,'Reading player portraits…');assert.equal(input.attributes.placeholder,'Search models');assert.equal(input.value,'张三');assert.equal(code.nodeValue,'球员姓名');assert.equal(window.confirm('确认生成'),true);assert.equal(alerts.pop(),'Confirm generation');
const later=text('资源未就绪');el('DIV',[later]);observe([{type:'childList',addedNodes:[later]}]);queued.splice(0).forEach(fn=>fn());assert.equal(later.nodeValue,'Resources not ready');console.log('TRANSLATION_PASS');
