/* Visual UI projection; original validated fields remain the only saved truth. */
(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const el = (tag, cls, text) => { const e=document.createElement(tag); if(cls)e.className=cls; if(text!==undefined)e.textContent=text; return e; };
  const button = (text, fn, cls='') => { const b=el('button',cls,text); b.type='button'; b.onclick=fn; return b; };
  let catalog;
  const flag = code => { if(!code)return el('span','vp-flag vp-flag-empty','—'); const i=el('img','vp-flag'); i.alt=''; i.src='/flags/'+encodeURIComponent(code)+'.svg'; return i; };
  const dialogs = new Map();
  function modal(id,title) {
    if(dialogs.has(id))return dialogs.get(id);
    const d=el('dialog','vp-dialog'); d.id=id; d.setAttribute('aria-labelledby',id+'-title');
    const head=el('div','vp-head'),h=el('h2','',title); h.id=id+'-title';
    head.append(h,button('关闭',()=>d.close())); const body=el('div','vp-body'); d.append(head,body); document.body.append(d);
    const obj={d,body}; dialogs.set(id,obj); return obj;
  }
  function search(placeholder) { const i=el('input','vp-search');i.type='search';i.placeholder=placeholder;i.setAttribute('aria-label',placeholder);return i; }
  function chooseProfile(kind) {
    const id='profile-'+kind, e=$(id), target=player;
    choose(kind,e.value,value=>{
      if(player!==target)return;
      // Keep native validation/onchange and inherit semantics; never reassign identity.
      if(![...e.options].some(o=>o.value===String(value)))throw Error('选项不在原始目录');
      e.value=String(value);e.dispatchEvent(new Event('change',{bubbles:true}));refreshLabels();
    });
  }
  function choose(kind,selected,onChoose) {
    const country=kind==='nationality', {d,body}=modal('vp-'+kind,country?'选择国家 / 地区':'选择俱乐部');
    const rows=country?catalog.countries:catalog.clubs, input=search('名称 / English / 编号');
    const tabs=el('div','vp-tabs'),grid=el('div','vp-grid');
    const groups=country?['亚洲','欧洲','南美洲','北美洲','非洲','大洋洲','其他'].map(id=>({id,label:id})):catalog.leagues.concat([{id:'other',label:'其他俱乐部'}]);
    let active=rows.find(r=>String(r.id)===String(selected))?.group||groups[0].id;
    body.replaceChildren(input,tabs,grid);
    const accept=value=>{onChoose(value);d.close();};
    function render() {
      const q=input.value.trim().toLocaleLowerCase();
      tabs.querySelectorAll('button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.group===active)));
      grid.replaceChildren();
      const inherit=button('沿用模型 / 不限',()=>accept(''),'vp-option vp-inherit');inherit.dataset.id='';grid.append(inherit);
      const list=rows.filter(r=>(q||r.group===active)&&(!q||`${r.zh||''} ${r.label} ${r.id}`.toLocaleLowerCase().includes(q)));
      for(const r of list){const b=button('',()=>accept(r.id),'vp-option');b.dataset.id=r.id;b.setAttribute('aria-pressed',String(String(r.id)===String(selected)));if(String(r.id)===String(selected))b.classList.add('selected');const name=el('span','',r.zh||r.label);name.append(el('small','',r.zh?r.label+' · '+r.id:String(r.id)));b.append(flag(r.flag),name);grid.append(b);}
      if(!list.length)grid.append(el('p','vp-empty','没有匹配项，试试其他分组或名称。'));
    }
    for(const g of groups){const b=button('',()=>{active=g.id;input.value='';render();});b.dataset.group=g.id;if(g.flag)b.append(flag(g.flag));b.append(document.createTextNode(g.label));tabs.append(b);}
    body.append(el('p','vp-note',country?'按地理大洲分组，搜索会查全部国家 / 地区。':'五大联赛目录按固定 V16 数据分组，非实时赛季名单；其他已保存俱乐部仍可选。'));
    input.oninput=render;render();d.showModal();
  }
  function refreshLabels() {
    if(!catalog)return;
    for(const [kind,rows,title] of [['nationality',catalog.countries,'国家 / 地区'],['club',catalog.clubs,'俱乐部']]){
      const e=$('profile-'+kind),b=document.querySelector('.vp-launch[data-for="profile-'+kind+'"]');if(!e||!b)continue;
      const row=rows.find(r=>String(r.id)===e.value);b.replaceChildren(flag(row?.flag),document.createTextNode(title+' · '+(row?.zh||row?.label||'沿用模型')));b.disabled=e.disabled;
    }
  }
  function attachProfile() {
    const section=$('diyProfileSection'); $('profile-affiliationQuery').hidden=true;
    for(const kind of ['nationality','club']){const e=$('profile-'+kind);e.hidden=true;const b=button('',()=>chooseProfile(kind),'vp-launch');b.dataset.for=e.id;e.after(b);}
    const base=sync;sync=function(){base();refreshLabels();};refreshLabels();
  }
  // All preview pixels use the existing image endpoint, including SHA/PNG/dimensions checks.
  const imageCache=new Map(), imagePending=new Map(), queue=[];let busy=0;
  function checkedImage(id) {
    if(imageCache.has(id))return Promise.resolve(imageCache.get(id));
    if(imagePending.has(id))return imagePending.get(id);
    const promise=new Promise((resolve,reject)=>{queue.push({id,resolve,reject});pump();});imagePending.set(id,promise);return promise;
  }
  function pump() {
    while(busy<3&&queue.length){const {id,resolve,reject}=queue.shift();busy++;
      request('/api/materials/image',{id}).then(v=>{if(!v.src?.startsWith('data:image/png;base64,'))throw Error('缩略图格式错误');imageCache.set(id,v.src);while(imageCache.size>30)imageCache.delete(imageCache.keys().next().value);resolve(v.src);}).catch(reject).finally(()=>{busy--;imagePending.delete(id);pump();});
    }
  }
  const thumbObserver=new IntersectionObserver(entries=>{for(const x of entries){if(!x.isIntersecting)continue;thumbObserver.unobserve(x.target);const image=x.target;checkedImage(image.dataset.materialId).then(src=>{if(image.isConnected){image.src=src;image.alt='球员素材';image.dataset.loaded='true';}}).catch(e=>{image.alt='图片读取失败';image.title=e.message;image.dataset.failed='true';});}},{rootMargin:'100px'});
  function thumb(id) {const image=el('img','material-thumb');image.alt='正在读取';image.dataset.materialId=id;thumbObserver.observe(image);return image;}
  function decorateMaterials() {
    const root=$('materialItems');for(const b of root.querySelectorAll('button[data-material-id]')){
      if(b.dataset.visualReady)continue;b.dataset.visualReady='true';const name=b.textContent;b.title=name;b.setAttribute('aria-label',name);const caption=el('span','vp-material-label',catalog?.materials.find(x=>x.id===b.dataset.materialId)?.label||name);caption.title=name;b.replaceChildren(thumb(b.dataset.materialId),caption);b.classList.add('vp-material-tile');
    }
  }
  function filters(body,onChange) {
    const f={nationality:'',club:'',legend:false},bar=el('div','vp-filterbar');
    const country=button('国家 / 大洲',()=>choose('nationality',f.nationality,v=>{f.nationality=String(v);refresh();onChange(f);}));country.dataset.filter='nationality';
    const club=button('联赛 / 俱乐部',()=>choose('club',f.club,v=>{f.club=String(v);refresh();onChange(f);}));club.dataset.filter='club';
    const legend=button('★ 传奇名单',()=>{f.legend=!f.legend;refresh();onChange(f);});legend.dataset.filter='legend';
    const reset=button('清除筛选',()=>{Object.assign(f,{nationality:'',club:'',legend:false});refresh();onChange(f);});reset.dataset.filter='reset';
    function refresh(){country.replaceChildren(flag(catalog.countries.find(r=>String(r.id)===f.nationality)?.flag),document.createTextNode(catalog.countries.find(r=>String(r.id)===f.nationality)?.zh||'国家 / 大洲'));club.replaceChildren(flag(catalog.clubs.find(r=>String(r.id)===f.club)?.flag),document.createTextNode(catalog.clubs.find(r=>String(r.id)===f.club)?.label||'联赛 / 俱乐部'));legend.setAttribute('aria-pressed',String(f.legend));}
    bar.append(country,club,legend,reset);body.append(bar);return f;
  }
  function materialDialog() {
    const {d,body}=modal('vp-material','检索球员素材');body.replaceChildren();
    const input=search('姓名 / English / 素材编号'),kind=el('select','vp-search'),grid=el('div','vp-grid'),status=el('p','vp-note');
    kind.setAttribute('aria-label','素材类型');
    for(const [value,label] of [['','全部图片'],['portrait','全部球员图片'],['thumbnail','阵容小头像'],['full','球员大图'],['card','卡面图层']])kind.add(new Option(label,value));
    let page=0,epoch=0,timer;const pager=el('div','vp-pager'),previous=button('上一页',()=>{page--;draw();}),next=button('下一页',()=>{page++;draw();});
    pager.append(previous,next);body.append(input,kind,status,grid,pager,el('p','vp-note','检索当前游戏完整图片资源；未收录姓名的素材仍可按编号查找。'));
    d.onclose=()=>{epoch++;clearTimeout(timer);};
    async function draw(){const token=++epoch;previous.disabled=next.disabled=true;status.textContent='正在读取素材索引…';
      try{const result=await request('/api/materials/list',{query:input.value.trim(),kind:kind.value,page});if(token!==epoch||!d.open)return;
        if(!Array.isArray(result.items)||!Number.isInteger(result.total)||!Number.isInteger(result.pageSize)||result.pageSize<1)throw Error('素材目录响应不完整');
        grid.replaceChildren();status.textContent=`${result.total} 项 · ${page+1}/${Math.max(1,Math.ceil(result.total/result.pageSize))} 页`+(result.warning?' · '+result.warning:'');
        previous.disabled=page===0;next.disabled=(page+1)*result.pageSize>=result.total;
        for(const row of result.items){const b=button('',()=>{const host=$('referenceMaterials');host.open=true;$('materialKind').value=kind.value;$('materialQuery').value=row.name;$('materialSearch').click();d.close();},'vp-option vp-material-tile');b.dataset.materialId=row.id;const name=el('span','',row.label||row.name);name.append(el('small','',row.name));b.append(thumb(row.id),name);grid.append(b);}
        if(!result.items.length)grid.append(el('p','vp-empty','没有匹配素材，试试其他姓名或编号。'));
      }catch(e){if(token===epoch){status.textContent='目录读取失败：'+e.message+'；可重试。';previous.disabled=page===0;next.disabled=true;}}
    }
    input.oninput=()=>{clearTimeout(timer);epoch++;timer=setTimeout(()=>{page=0;draw();},250);};kind.onchange=()=>{page=0;draw();};d.showModal();draw();
  }
  function modelDialog() {
    const {d,body}=modal('vp-model','搜索球员模型'), target=player;body.replaceChildren();const input=search('姓名 / English / 球员编号');body.append(input);
    let epoch=0,offset=0,all=[],total=0,timer;const f=filters(body,()=>run(false)),status=el('p','vp-note'),grid=el('div','vp-grid'),more=button('加载下一页',()=>run(true));more.dataset.modelMore='true';body.append(status,grid,more);
    d.onclose=()=>{epoch++;clearTimeout(timer);};
    async function run(append){const token=++epoch;if(!append){offset=0;all=[];}more.disabled=true;status.textContent='正在读取模型目录…';
      try{const result=await request('/api/models/search',{q:input.value.trim(),offset,limit:60,club:f.club,nationality:f.nationality,legend:f.legend});if(token!==epoch||!d.open)return;if(!Array.isArray(result.models)||!Number.isInteger(result.total))throw Error('模型目录响应不完整');offset+=result.models.length;total=result.total;all.push(...result.models);
        const rows=all.filter(m=>m.available&&/^\d{1,16}$/.test(String(m.id)));grid.replaceChildren();
        for(const row of rows){const b=button('',()=>{if(player!==target)return;const id=String(row.id),select=$('diyModel');if(!CardPackage.models.some(m=>m.id===id))CardPackage.models.push({id,label:row.label});if(![...select.options].some(o=>o.value===id))select.add(new Option(row.label,id));select.value=id;select.dispatchEvent(new Event('change',{bubbles:true}));d.close();},'vp-option');b.dataset.id=row.id;const picture=catalog.materials.find(m=>m.name.replace(/[_fl]+$/,'')===String(row.id));b.append(picture?thumb(picture.id):el('span','vp-model-avatar','模型'),el('span','',row.label));grid.append(b);}
        status.textContent=`显示 ${rows.length} 项 · 已检索 ${offset}/${total}`;
        if(!rows.length)grid.append(el('p','vp-empty',result.testApp?'独立测试 APP 尚未连接完整模型目录；当前模型引用保留。':'当前筛选没有匹配模型，试试其他姓名或清除筛选。'));
        more.hidden=offset>=total||result.models.length===0;more.disabled=false;
      }catch(e){if(token===epoch){status.textContent='目录读取失败：'+e.message+'；当前模型保留，可重试。';more.disabled=false;}}
    }
    body.append(el('p','vp-note','选择头像用于确认人物，不代表 3D 预览。关闭或筛选不会改动当前模型。'));
    input.oninput=()=>{clearTimeout(timer);epoch++;timer=setTimeout(()=>run(false),250);};d.showModal();run(false);
  }
  function attachModels() {
    const old=$('diyModelSearch').parentElement;old.hidden=true;
    const select=$('diyModel');select.hidden=true;
    const launch=button('搜索模型 · 国家 / 俱乐部 / 传奇',modelDialog,'vp-launch');launch.id='vpModelLaunch';old.after(launch);
  }
  async function boot() {
    try{catalog=await request('/visual-catalog.json');if(catalog.schema!=='diy-visual-catalog/v1'||catalog.countries.length!==214)throw Error('可视化目录版本不匹配');attachProfile();attachModels();
      const source=$('materialItems');new MutationObserver(decorateMaterials).observe(source,{childList:true});decorateMaterials();
      const launch=button('可视化检索球员素材',materialDialog,'vp-launch');launch.id='vpMaterialLaunch';$('materialSearch').after(launch);document.documentElement.dataset.visualPickersReady='true';
    }catch(e){const status=$('profile-loadStatus');if(status)status.textContent='可视化目录读取失败：'+e.message+'；保留原选择控件。';}
  }
  const ready=setInterval(()=>{if($('diyProfileSection')&&$('diyModelSearch')){clearInterval(ready);boot();}},50);
})();
