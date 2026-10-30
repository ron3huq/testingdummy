/* Curated full-area native movie suites, paired with original small-card art. */
(() => {
  let catalog=null,page=0,selecting=false;
  const get=id=>document.getElementById(id),panel=get('backgroundPicker');
  const picker=document.createElement('div');picker.id='suitePicker';
  picker.innerHTML=`<h2>精选动态卡面 · 小框配套</h2><div class="suite-filters"><select id="suiteSeries" aria-label="套装系列"><option value="">全部系列</option><option>ST</option><option>BT</option><option>Epic</option></select><input id="suiteSearch" type="text" placeholder="编号 / 球员姓名 / ID" aria-label="搜索套装"></div><div class="row"><button id="videoToggle" aria-pressed="false">动态预览：关</button><span id="suiteSelection" class="status" role="status">正在读取…</span></div><div id="suiteGallery"></div><div class="suite-pager"><button id="suitePrevious">上一页</button><span id="suitePage"></span><button id="suiteNext">下一页</button></div><p class="hint">点一款，同时应用配套小框和详情。缩略图右下角显示对应小框。只播放当前卡面，后台自动暂停。</p>`;panel.prepend(picker);
  const health=document.createElement('p');health.id='suiteResourceHealth';health.className='status';health.setAttribute('role','status');
  const retry=document.createElement('button');retry.id='suiteResourceRetry';retry.textContent='重新加载卡面';retry.onclick=()=>{for(const [src,im] of images)if(!im.complete||!im.naturalWidth)images.delete(src);list();render();};picker.append(health,retry);
  function list(){if(!catalog)return;const q=get('suiteSearch').value.trim().toLowerCase(),series=get('suiteSeries').value;let missing=0;
    health.textContent='';
    const all=catalog.suites.filter(s=>(!series||s.series===series)&&(!q||[s.id,s.reviewNo,s.donorName,s.donorPlayerId,s.donorVariation].some(v=>String(v??'').toLowerCase().includes(q))));
    const pages=Math.max(1,Math.ceil(all.length/12));page=Math.min(page,pages-1);get('suiteGallery').replaceChildren();
    for(const s of all.slice(page*12,page*12+12)){
      const b=document.createElement('button');b.className='suite-tile';b.dataset.suite=s.id;
      const art=document.createElement('div');art.className='suite-tile-art';
      for(const kind of ['detail','small']){const a=CardBackgrounds.resolve(s.appearance[kind].background);const im=document.createElement('img');im.alt=kind==='small'?'原版配套小框':'详情卡面';im.className=kind==='small'?'suite-small':'suite-bg';im.loading='lazy';im.onerror=()=>{if(!b.isConnected)return;im.hidden=true;b.dataset.resource='missing';missing++;health.textContent=`本页 ${missing} 张图片缺失或损坏。请重试；若全部缺失，需更新完整资源包，准备游戏资源不会修复编辑器图片。`;};art.append(im);if(a?.src)im.src=a.src;else queueMicrotask(()=>im.onerror());}
      const mark=document.createElement('span');mark.textContent=s.reviewNo+' · 动态';mark.className='suite-mark';art.append(mark);
      const title=document.createElement('strong');title.textContent=s.series+' · '+s.variant;
      const name=document.createElement('span');name.textContent=s.donorName;
      const id=document.createElement('small');id.textContent=s.donorPlayerId;b.append(art,title,name,id);b.onclick=async()=>{if(selecting)return;selecting=true;const who=player,before=revision;b.disabled=true;try{get('suiteSelection').textContent='正在校验配套图片…';await ensure(s,{retry:true});if(player!==who||revision!==before)throw Error('作品已变化，请重新选择套装');apply(s.id);}catch(e){health.textContent=e.message;selection();}finally{selecting=false;b.disabled=false;}};get('suiteGallery').append(b);
    }
    get('suitePage').textContent=`${page+1} / ${pages} · ${all.length}套`;get('suitePrevious').disabled=page===0;get('suiteNext').disabled=page===pages-1;selection();
  }
  function selection(){if(!state)return;const s=state.players[player].cardSuite;get('suiteSelection').textContent=s?`${s.reviewNo||''} ${s.id} · 小框/详情已配套`:'选择背景，自动配套小框';for(const b of get('suiteGallery').children)b.setAttribute('aria-pressed',String(b.dataset.suite===s?.id));}
  function apply(id){const s=catalog?.suites.find(v=>v.id===id);if(!s)return;snapshot();const p=state.players[player];p.cardSuite=copy(s);p.cardSuite.sourceVersion=catalog.sourceVersion;p.appearance=copy(s.appearance);p.detailCanvasHeight=720;changed();sync();}
  async function ensure(s,options={}){for(const cfg of Object.values(s.appearance||{}))for(const id of new Set(Object.values(cfg).filter(Boolean))){const a=CardBackgrounds.resolve(id);if(!a?.src)throw Error('套装图片目录缺失：'+id);await readyImage(a.src,options);}}
  let searchTimer=0;for(const id of ['suiteSeries','suiteSearch'])get(id).addEventListener(id==='suiteSeries'?'change':'input',()=>{clearTimeout(searchTimer);if(id==='suiteSeries'){page=0;list();}else searchTimer=setTimeout(()=>{page=0;list();},120);});
  get('suitePrevious').onclick=()=>{page--;list();};get('suiteNext').onclick=()=>{page++;list();};
  get('videoToggle').onclick=()=>{const value=!CardBackgrounds.playing;CardBackgrounds.setPlaying(value);get('videoToggle').textContent='动态预览：'+(value?'开':'关');get('videoToggle').setAttribute('aria-pressed',String(value));};
  const oldSync=sync;sync=function(){oldSync();selection();};
  const stable=v=>JSON.stringify(v,(k,x)=>x&&typeof x==='object'&&!Array.isArray(x)?Object.fromEntries(Object.entries(x).sort(([a],[b])=>a.localeCompare(b))):x);
  window.CardSuites={apply,ensure,drawBase:(c,w,k)=>CardBackgrounds.draw(c,w,k,'background'),drawFrame:(c,w,k)=>CardBackgrounds.draw(c,w,k,'frame'),ready:null,get catalog(){return catalog;},async validate(s){await this.ready;const known=catalog.suites.find(v=>v.id===s?.id);if(!known||stable({...known,sourceVersion:catalog.sourceVersion})!==stable(s))throw Error('套装与精选目录不匹配，请重新选择');return s;}};
  CardSuites.ready=(async()=>{await CardBackgrounds.ready;catalog=await request('/card-suites.json');list();render();})();
  CardSuites.ready.catch(e=>get('suiteSelection').textContent=e.message);
})();
