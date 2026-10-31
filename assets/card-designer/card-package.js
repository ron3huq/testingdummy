/* Single-card exchange. Artwork/configuration only; game registration is a separate transaction. */
(() => {
  'use strict';
  const MAX=32*1024*1024, SCHEMA='efootball-diy-card/v1';
  const models=[];
  const legacyModels={Ronaldo:'37576',Zidane:'9901397',Henry:'88046312750111'};
  const abilities=['进攻意识','防守意识','守门','盘球','控球','紧密控球','射门','地面传球','空中传球','头球','抢球','积极性','防守参与','定位球','弧线','接球','解围','扑救反应','扑救范围','速度','身体接触','身体控制','脚下力量','加速','跳跃','体力'];
  const indices=[14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,34,35,36,37,38,39,40];
  let boosterRows=null,boosterReady=Promise.resolve();
  const byId=id=>document.getElementById(id), uuid=()=>crypto.randomUUID();
  const panel=document.createElement('section');panel.className='card-tool-panel';panel.id='cardPlayerPanel';
  panel.innerHTML=`<div class="diy-profile"><span class="diy-profile-icon" aria-hidden="true">DIY</span><div><h2>我的自定义球员</h2><p id="diyProfileSummary">姓名、能力与增能随作品保存</p></div></div><section class="diy-setting-card"><h3>基本资料</h3><label>球员姓名<input id="diyName" type="text" maxlength="40" placeholder="给球员起个名字"></label><div class="card-fields"><label>初始等级<input id="diyLevel" type="number" min="1" max="50" inputmode="numeric"></label><label>等级上限<input id="diyMaxLevel" type="number" min="1" max="50" inputmode="numeric"></label></div></section><details class="diy-setting-card" id="diyAbilitySection"><summary>基础能力 <span>26项 · 按类别调整</span></summary><div id="diyAbilities"></div><p class="hint">这里编辑基础能力，不包含培养与条件增能加成。</p></details><details class="diy-setting-card" id="diyBoosterSection"><summary>双增能 <span id="diyBoosterSummary">未启用</span></summary><label>查找增能<input id="diyBoosterQuery" type="search" placeholder="搜索名称、能力或编号" maxlength="80"></label><div class="diy-booster-slot"><label><span class="booster-badge gold">1</span> 第一增能<select id="diyBooster0" disabled><option value="0">未启用</option></select></label><p id="diyBoosterDescription0" class="hint"></p></div><div class="diy-booster-slot"><label><span class="booster-badge cyan">2</span> 第二增能<select id="diyBooster1" disabled><option value="0">未启用</option></select></label><p id="diyBoosterDescription1" class="hint"></p></div><p id="diyBoosterStatus" class="hint" role="status">正在读取球员编辑器增能目录…</p><button id="diyBoosterRetry" type="button" hidden>重试加载增能</button></details><details class="diy-setting-card" id="diyModelSection"><summary>外观模型 · 全库搜索 <span id="diyModelSummary">使用已有球员模型</span></summary><label>已选模型<select id="diyModel"></select></label><p class="hint">从游戏目录选择已有球员的脸型与身体引用，不修改原球员。直接使用游戏内已有脸型与身体，不要求已拥有对应球员。头像用于认人，不代表3D预览。</p></details><p class="status" id="diyPlayerStatus" role="status"></p>`;
  for(const m of models)byIdIn(panel,'diyModel').add(new Option(m.label,m.id));
  for(const section of panel.querySelectorAll('details.diy-setting-card'))section.addEventListener('toggle',()=>{if(section.open)for(const other of panel.querySelectorAll('details.diy-setting-card'))if(other!==section)other.open=false;});
  function byIdIn(p,id){return p.querySelector('#'+id);}
  const share=document.createElement('section');share.className='card-tool-panel';share.id='cardSharePanel';
  share.innerHTML=`<h2>分享当前一张作品</h2><div class="buttons"><button id="shareCard" class="primary">导出单卡分享包</button><button id="openCard">导入分享包</button></div><input id="cardPackageInput" type="file" accept=".efcard,application/json"><p class="hint">包含这张卡的小框、详情、背景边框、姓名能力和模型引用。接收方导入后可继续编辑。分享包不包含存档；导入游戏请到球员页完成生成流程。</p><details><summary>工程备份与图片导出</summary><div id="cardProjectActions" class="buttons"></div></details><p id="cardShareStatus" class="status" role="status" aria-live="polite"></p>`;
  window.cardToolPanel('player',panel);window.cardToolPanel('share',share);
  for(const id of ['importProject','saveProject','export','exportAll','exportLayers']){
    const b=document.createElement('button');b.id='cardAction-'+id;b.textContent=byId(id).textContent;b.onclick=()=>byId(id).click();byId('cardProjectActions').append(b);
  }
  const undoRow=document.createElement('div');undoRow.className='row';
  for(const [id,label]of [['undo','↶'],['redo','↷']]){const b=document.createElement('button');b.id=id==='undo'?'quickUndo':'quickRedo';b.textContent=label;b.title=id==='undo'?'撤销':'重做';b.style.cssText='min-height:26px;padding:3px 8px';b.onclick=()=>byId(id).click();undoRow.append(b);}
  byId('phonePreviewToggle').before(undoRow);
  const abilityGroups=[['进攻与技术',[14,17,18,19,20,21,22,27,28]],['防守与体能',[15,23,24,25,34,35,36,37,38,39,40]],['门将能力',[16,26,29,30,31,32]]],abilityHosts=new Map();
  for(const [title,fields]of abilityGroups){const group=document.createElement('section');group.className='diy-ability-group';const heading=document.createElement('h4');heading.textContent=title;const rows=document.createElement('div');rows.className='card-fields';group.append(heading,rows);byId('diyAbilities').append(group);for(const i of fields)abilityHosts.set(i,rows);}
  for(let n=0;n<indices.length;n++){
    const label=document.createElement('label');label.textContent=abilities[n];const input=document.createElement('input');input.type='number';input.min=0;input.max=99;input.id='diyAbility'+indices[n];
    input.inputMode='numeric';input.onchange=()=>edit(d=>{const v=Number(input.value);if(input.value.trim()===''||!Number.isInteger(v)||v<0||v>99)throw Error('基础能力请填写0–99的整数');d.abilities[String(indices[n])]=v;});input.setAttribute('aria-label',abilities[n]+'数值');
    const range=document.createElement('input');range.type='range';range.min=0;range.max=99;range.step=1;range.id='diyRange'+indices[n];range.setAttribute('aria-label',abilities[n]+'滑条');
    range.oninput=()=>{input.value=range.value;};range.onchange=()=>{input.value=range.value;input.dispatchEvent(new Event('change'));};
    label.classList.add('editor-ability-row');label.append(input,range);abilityHosts.get(indices[n]).append(label);
  }
  function defaults(who=player){return {uuid:uuid(),name:{Ronaldo:'Ronaldo',Zidane:'Zidane',Henry:'Thierry Henry'}[who]||'New player',initialLevel:1,maxLevel:35,model:{playerId:legacyModels[who]||'',version:'11.1.1'},abilities:Object.fromEntries(indices.map(i=>[String(i),70]))};}
  // Never mint identities while merely rendering a project: edits/export are explicit commits.
  function metadata(){return state.players[player].diy||{...defaults(),uuid:''};}
  function validateMeta(d,{previous}={}){
    if(!d||typeof d!=='object'||!/^[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}$/i.test(d.uuid||''))throw Error('作品标识格式错误');
    if(typeof d.name!=='string'||!d.name.trim()||d.name.length>40)throw Error('姓名请填写1–40个字符');
    if(!Number.isInteger(d.initialLevel)||!Number.isInteger(d.maxLevel)||d.initialLevel<1||d.maxLevel>50||d.initialLevel>d.maxLevel)throw Error('等级应为1–50，初始等级应小于等于上限');
    if(d.model?.version!=='11.1.1'||(d.model?.playerId!==''&&!/^[1-9][0-9]{0,15}$/.test(d.model?.playerId||'')))throw Error('模型引用格式或版本错误');
    if(!d.abilities||Object.keys(d.abilities).length!==indices.length)throw Error('能力项数量错误');
    if(Object.hasOwn(d,'cardDate')&&d.cardDate!==''&&!/^(?:0?[1-9]|[12][0-9]|3[01]) (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) '[0-9]{2}$/.test(d.cardDate))throw Error("卡面日期格式应为 19 Jun '00");
    for(const i of indices)if(!Number.isInteger(d.abilities[i])||d.abilities[i]<0||d.abilities[i]>99)throw Error('基础能力请填写0–99的整数');
    if(Object.hasOwn(d,'boosters'))validateBoosters(d.boosters);
    if(Object.hasOwn(d,'profile'))CardProfile.validate(d.profile,{previous:previous?.profile});
    if(Object.hasOwn(d,'editorSettings'))DiyEditorFields.validate(d.editorSettings,{previous:previous?.editorSettings});
    return d;
  }
  function cleanMeta(d){validateMeta(d);return {uuid:d.uuid,name:d.name.trim(),initialLevel:d.initialLevel,maxLevel:d.maxLevel,model:{playerId:d.model.playerId,version:d.model.version},abilities:Object.fromEntries(indices.map(i=>[String(i),d.abilities[i]])),...(d.cardDate?{cardDate:d.cardDate}:{}),...(Object.hasOwn(d,'boosters')?{boosters:[...d.boosters]}:{}),...(Object.hasOwn(d,'profile')?{profile:CardProfile.validate(d.profile)}:{}),...(Object.hasOwn(d,'editorSettings')?{editorSettings:DiyEditorFields.validate(d.editorSettings)}:{})};}
  function edit(fn){try{const previous=copy(state.players[player].diy||defaults()),d=copy(previous);fn(d);validateMeta(d,{previous});snapshot();state.players[player].diy=d;changed();refresh();byId('diyPlayerStatus').textContent=(d.editorSettings?.stars===5||d.profile?.weakAccuracy===4||d.profile?.weakUsage===4)?'设置已保存；旧版数值保留。生成前请将星级设为1–4、逆足精度和频率设为1–3；已生成的卡请另存新作品。':'球员设置已保存到作品';}catch(e){byId('diyPlayerStatus').textContent=e.message;refresh();}}
  byId('diyName').onchange=()=>edit(d=>d.name=byId('diyName').value.trim());
  byId('diyLevel').onchange=()=>edit(d=>d.initialLevel=Number(byId('diyLevel').value));
  byId('diyMaxLevel').onchange=()=>edit(d=>d.maxLevel=Number(byId('diyMaxLevel').value));
  byId('diyModel').onchange=()=>edit(d=>d.model={playerId:byId('diyModel').value,version:'11.1.1'});
  function refresh(){if(!state)return;const d=metadata(),select=byId('diyModel');if(![...select.options].some(o=>o.value===d.model.playerId))select.add(new Option(d.model.playerId?d.model.playerId+' · 已保存模型':'请选择游戏中的球员模型',d.model.playerId));byId('diyName').value=d.name;byId('diyLevel').value=d.initialLevel;byId('diyMaxLevel').value=d.maxLevel;select.value=d.model.playerId;for(const i of indices){const input=byId('diyAbility'+i);input.value=d.abilities[i];byId('diyRange'+i).value=d.abilities[i];input.dataset.rating=d.abilities[i]>=85?'high':d.abilities[i]>=70?'mid':'low';}byId('cardName').textContent=d.name;byId('diyProfileSummary').textContent=d.name+' · 等级 '+d.initialLevel+' / '+d.maxLevel;byId('diyModelSummary').textContent=select.selectedOptions[0]?.textContent||d.model.playerId;refreshBoosters();workPicker();window.CardProfile?.refresh();window.DiyEditorFields?.refresh();}
  const previousSync=sync;sync=function(){previousSync();refresh();window.CardSuites?.refreshDate?.();};
  const previousRender=render;render=function(){previousRender();if(state?.players[player]?.diy)byId('cardName').textContent=state.players[player].diy.name;};
  const encoder=new TextEncoder();
  async function sha(bytes){const digest=await crypto.subtle.digest('SHA-256',bytes);return Array.from(new Uint8Array(digest),x=>x.toString(16).padStart(2,'0')).join('');}
  function bytesOf(src){if(typeof src!=='string'||!/^data:image\/png;base64,[A-Za-z0-9+/]*={0,2}$/.test(src)||src.length>12*1024*1024)throw Error('分享图片格式或大小错误');const b=Uint8Array.from(atob(src.split(',')[1]),c=>c.charCodeAt(0));if(b.length<24||[137,80,78,71,13,10,26,10].some((v,i)=>b[i]!==v))throw Error('图片不是PNG');const v=new DataView(b.buffer),w=v.getUint32(16),h=v.getUint32(20);if(w<1||h<1||w>2048||h>2048)throw Error('图片尺寸应在2048以内');return b;}
  async function png(src){if(!src.startsWith('data:image/')&&!/^\/(assets|backgrounds)\/[\w.-]+\.png$/.test(src))throw Error('素材来源错误');const im=await readyImage(src);if(im.naturalWidth>2048||im.naturalHeight>2048)throw Error('图片尺寸应在2048以内');const c=document.createElement('canvas');c.width=im.naturalWidth;c.height=im.naturalHeight;c.getContext('2d').drawImage(im,0,0);return c.toDataURL();}
  const assetId=id=>typeof id==='string'&&/^(0500|0501|0601)(_[0-9]+)?_[bfm][0-9]{2}$/.test(id);
  function checkedLayer(l){
    for(const k of ['x','y','width','ratio','opacity'])if(typeof l?.[k]!=='number'||!Number.isFinite(l[k]))throw Error('图层数值错误');
    if(Math.abs(l.x)>4096||Math.abs(l.y)>4096||l.width<1||l.width>4096||l.ratio<=0||l.ratio>100||l.opacity<0||l.opacity>1||typeof l.visible!=='boolean'||(l.flipX!==undefined&&typeof l.flipX!=='boolean'))throw Error('图层数值超出范围');
    return {asset:l.asset,x:l.x,y:l.y,width:l.width,ratio:l.ratio,opacity:l.opacity,visible:l.visible,flipX:!!l.flipX,name:typeof l.name==='string'?l.name.slice(0,60):''};
  }
  async function prepare({onProgress=()=>{}}={}){
    if(state.players[player].diy?.boosters?.some(Boolean))await boosterReady;
    const who=player,before=revision,p=copy(state.players[who]),meta=cleanMeta(p.diy||defaults(who)),assets={},converted=new Map();
    if(!meta.model.playerId)throw Error('请先展开游戏模型，搜索并选择一位已有球员的模型');
    if(['small','detail'].some(kind=>p[kind].some(layer=>layer.placeholder)))throw Error('请为小框和详情选择人物图片，再预览生成');
    onProgress('校验球员设置与套装');
    async function embed(src,crop){const key=src+JSON.stringify(crop||null);if(converted.has(key))return converted.get(key);let data;if(crop){const im=await readyImage(src),r=sourceRect(im,{crop}),c=document.createElement('canvas');c.width=r.w;c.height=r.h;c.getContext('2d').drawImage(im,r.x,r.y,r.w,r.h,0,0,r.w,r.h);data=c.toDataURL('image/png');}else data=await png(src);const hash=await sha(bytesOf(data));assets[hash]={sha256:hash,png:data};converted.set(key,hash);return hash;}
    const layout={detailCanvasHeight:p.detailCanvasHeight||720,small:[],detail:[],appearance:copy(p.appearance||{})};if(p.cardSuite){await CardSuites.validate(p.cardSuite);layout.cardSuite=copy(p.cardSuite);}
    for(const kind of ['small','detail']){if(p[kind].length>8)throw Error('每个构图最多8层');for(const [i,l] of p[kind].entries()){onProgress(`读取${kind==='small'?'小框':'详情'}人物 ${i+1}/${p[kind].length}`);layout[kind].push({...checkedLayer(l),asset:await embed(l.asset,l.crop)});}}
    await CardBackgrounds.ready;const backgrounds=[];
    for(const id of new Set(Object.values(layout.appearance).flatMap(v=>[v.background,v.frame]).filter(Boolean))){onProgress('校验套装图片：'+id);const a=CardBackgrounds.resolve(id);if(!a)throw Error('背景缺失：'+id);backgrounds.push({id,series:a.series,asset:await embed(a.src)});}
    if(Object.values(meta.abilities).some(v=>v<40))throw Error('作品支持保存0–99；当前游戏原生制卡仅支持40–99，请调整低于40的能力后生成，原作品保留');
    const data={schema:SCHEMA,metadata:meta,layout,backgrounds,assets};const text=JSON.stringify(data);if(encoder.encode(text).length>MAX)throw Error('分享包请控制在32MB以内');
    // Identity is persisted only after the entire package has been prepared successfully.
    if(player!==who||revision!==before)throw Error('作品在整理时发生变化，请重新预览');if(!state.players[who].diy){snapshot();state.players[who].diy=meta;changed();const expected=revision;onProgress('保存作品标识');await save();if(savedRevision<expected)throw Error('作品标识未保存，请检查保存错误后重试');if(player!==who||revision!==expected)throw Error('作品在保存时发生变化，请重新预览');refresh();}
    return data;
  }
  // Generation and sharing use one validated envelope; only sharing downloads it.
  async function build(){return prepare();}
  async function newWork(){
    const who=player,previous=state.players[who].diy?.uuid;
    const metadata=cleanMeta({...copy(state.players[who].diy||defaults(who)),uuid:uuid()});
    snapshot();state.players[who].diy=metadata;changed();refresh();const expected=revision;
    await save();if(savedRevision<expected)throw Error('新作品尚未保存，请先处理工程保存错误；旧候选没有修改');
    if(player!==who||revision!==expected)throw Error('保存期间作品已变化，请检查当前作品后重新预览');
    return {uuid:metadata.uuid,previousUuid:previous};
  }
  async function inspect(text){
    if(typeof text!=='string'||encoder.encode(text).length>MAX)throw Error('分享包请控制在32MB以内');let p;try{p=JSON.parse(text);}catch(e){throw Error('分享包内容损坏');}
    if(Array.isArray(p.metadata?.boosters)&&p.metadata.boosters.some(Boolean))await boosterReady;
    if(p.schema!==SCHEMA)throw Error('分享包版本不匹配');const meta=cleanMeta(p.metadata),l=p.layout;
    if(!l||![512,720].includes(l.detailCanvasHeight)||!p.assets||typeof p.assets!=='object'||Array.isArray(p.assets)||Object.keys(p.assets).length>20)throw Error('分享包结构错误');
    const assets={};
    for(const [id,a]of Object.entries(p.assets)){if(!/^[a-f0-9]{64}$/.test(id)||a?.sha256!==id||await sha(bytesOf(a.png))!==id)throw Error('素材校验失败');await readyImage(a.png);assets[id]=a.png;}
    const layout={detailCanvasHeight:l.detailCanvasHeight,calibration:{},appearance:{}};if(l.cardSuite){await CardSuites.validate(l.cardSuite);layout.cardSuite=copy(l.cardSuite);}const referenced=new Set();
    for(const kind of ['small','detail']){if(!Array.isArray(l[kind])||l[kind].length>8)throw Error('人物图层数量应为0–8');layout[kind]=l[kind].map(layer=>{const v=checkedLayer(layer);if(!Object.hasOwn(assets,v.asset))throw Error('人物图片缺失');referenced.add(v.asset);return {...v,asset:assets[v.asset]};});}
    if(!Array.isArray(p.backgrounds)||p.backgrounds.length>4)throw Error('背景数量错误');const backgrounds=[],ids=new Set();
    for(const b of p.backgrounds){if(!assetId(b.id)||!['ST','BT','Epic'].includes(b.series)||ids.has(b.id)||!Object.hasOwn(assets,b.asset))throw Error('背景素材错误');ids.add(b.id);referenced.add(b.asset);backgrounds.push({id:b.id,series:b.series,src:assets[b.asset]});}
    for(const [kind,cfg]of Object.entries(l.appearance||{})){if(!['small','detail'].includes(kind)||!cfg||Object.keys(cfg).some(k=>!['background','frame'].includes(k)))throw Error('背景布局错误');layout.appearance[kind]={};for(const [k,id]of Object.entries(cfg)){if(id!==''&&(!assetId(id)||!ids.has(id)))throw Error('背景引用缺失');layout.appearance[kind][k]=id;}}
    if(layout.cardSuite&&JSON.stringify(layout.appearance)!==JSON.stringify(layout.cardSuite.appearance))throw Error('套装与背景选择不一致');
    if(referenced.size!==Object.keys(assets).length)throw Error('分享包含有未使用素材');
    return {metadata:meta,layout,backgrounds,modelAvailable:models.some(m=>m.id===meta.model.playerId)};
  }
  const modal=document.createElement('dialog');modal.className='card-package-dialog';modal.innerHTML=`<h2>导入作品预览</h2><div class="row"><img id="cardImportPreview" alt="导入卡面预览"><div><strong id="cardImportName"></strong><p id="cardImportInfo"></p></div></div><label>本机模型<select id="cardImportModel"></select></label><p class="hint" id="cardImportWarning"></p><p class="hint">确认后替换当前编辑槽的作品。其他编辑槽保持；可用撤销恢复。此操作保存制卡工程，不写入游戏存档。</p><div class="buttons"><button id="confirmCardImport" class="primary">确认导入</button><button id="cancelCardImport">取消</button></div>`;document.body.append(modal);
  for(const m of models)byId('cardImportModel').add(new Option(m.label,m.id));
  let pending=null;
  function status(s){byId('cardShareStatus').textContent=s;}
  byId('shareCard').onclick=async()=>{try{byId('shareCard').disabled=true;status('正在整理当前卡片…');const p=await build();download(JSON.stringify(p),p.metadata.name.replace(/[\\/:*?"<>|\x00-\x1f]/g,'_')+'.efcard','application/octet-stream');status('单卡分享包已准备，请选择保存位置');}catch(e){status(e.message);}finally{byId('shareCard').disabled=false;}};
  byId('openCard').onclick=()=>byId('cardPackageInput').click();
  byId('cardPackageInput').onchange=async e=>{const f=e.target.files[0];e.target.value='';if(!f)return;try{if(f.size>MAX)throw Error('分享包请控制在32MB以内');await preview(await inspect(await f.text()));}catch(e){status(e.message);}};
  function drawBackground(x,im,h){const scale=Math.min(512/im.naturalWidth,h/im.naturalHeight),w=im.naturalWidth*scale,hh=im.naturalHeight*scale;x.drawImage(im,(512-w)/2,(h-hh)/2,w,hh);}
  async function preview(p){
    pending=null;
    // Search by exact ID rather than relying on the initially empty model cache.
    let modelNote='';
    try{const result=await request('/api/models/search',{q:p.metadata.model.playerId,offset:0,limit:60});const row=result.models?.find(m=>m.id===p.metadata.model.playerId);p.modelAvailable=!!row?.available;if(p.modelAvailable&&!models.some(m=>m.id===row.id))models.push({id:row.id,label:row.label});if(row&&!row.available)modelNote=row.reason||'资源未就绪';}catch(e){p.modelAvailable=false;modelNote='目录暂时读取失败';}
    const chooser=byId('cardImportModel');chooser.replaceChildren();for(const m of models)chooser.add(new Option(m.label,m.id));if(!p.modelAvailable){chooser.add(new Option('保留原模型引用（草稿，生成前需重新选择）',p.metadata.model.playerId));}
    const c=document.createElement('canvas');c.width=512;c.height=720;const x=c.getContext('2d');x.scale(1,720/p.layout.detailCanvasHeight);
    const cfg=p.layout.appearance.detail||{};for(const b of p.backgrounds)if(b.id===cfg.background)drawBackground(x,await readyImage(b.src),p.layout.detailCanvasHeight);
    for(const l of p.layout.detail){if(!l.visible)continue;x.save();x.globalAlpha=l.opacity;if(l.flipX){x.translate(2*l.x+l.width,0);x.scale(-1,1);}x.drawImage(await readyImage(l.asset),l.x,l.y,l.width,l.width*l.ratio);x.restore();}
    for(const b of p.backgrounds)if(b.id===cfg.frame)drawBackground(x,await readyImage(b.src),p.layout.detailCanvasHeight);
    byId('cardImportPreview').src=c.toDataURL();byId('cardImportName').textContent=p.metadata.name;byId('cardImportInfo').textContent=`等级 ${p.metadata.initialLevel}/${p.metadata.maxLevel} · 26项基础能力${p.layout.cardSuite?' · 套装 '+p.layout.cardSuite.id:''}`;
    const clash=Object.values(state.players).some(v=>v.diy?.uuid===p.metadata.uuid);
    byId('cardImportWarning').textContent=(p.modelAvailable?'已找到本机模型引用。':'模型尚未确认可用：'+modelNote+'。可保留为草稿，生成前须在模型库选择可用模型。')+(clash?' 检测到相同作品标识，导入为新副本。':'');
    byId('cardImportModel').value=p.metadata.model.playerId;byId('confirmCardImport').disabled=false;pending={p,target:player};modal.showModal();
  }
  byId('cardImportModel').onchange=()=>byId('confirmCardImport').disabled=!byId('cardImportModel').value;
  byId('cancelCardImport').onclick=()=>{pending=null;modal.close();};modal.addEventListener('cancel',()=>pending=null);
  byId('confirmCardImport').onclick=async()=>{
    if(!pending)return;const {p,target}=pending;if(target!==player){pending=null;modal.close();status('编辑对象已切换，请重新导入');return;}
    try{const model=byId('cardImportModel').value;if(!models.some(m=>m.id===model)&&model!==p.metadata.model.playerId)throw Error('请选择模型或保留原引用为草稿');
      // Build and validate the complete candidate before changing live state.
      const next=copy(state),meta=copy(p.metadata);if(Object.values(next.players).some(v=>v.diy?.uuid===meta.uuid))meta.uuid=uuid();meta.model.playerId=model;
      next.players[target]={...copy(p.layout),diy:meta};const all=new Map((next.backgroundLibrary||[]).map(a=>[a.id,a]));
      const otherUses=new Set(Object.entries(next.players).filter(([k])=>k!==target).flatMap(([,v])=>Object.values(v.appearance||{}).flatMap(c=>[c.background,c.frame])).filter(Boolean));
      for(const a of p.backgrounds){const old=all.get(a.id);if(old&&otherUses.has(a.id)&&await png(old.src)!==a.src)throw Error('同编号背景与其他作品冲突，请先更换背景');all.set(a.id,a);}
      const used=new Set(Object.values(next.players).flatMap(v=>Object.values(v.appearance||{}).flatMap(c=>[c.background,c.frame])).filter(Boolean));next.backgroundLibrary=[...all.values()].filter(a=>used.has(a.id));
      if(encoder.encode(JSON.stringify(next)).length>39_000_000)throw Error('合并后工程超过容量，请先备份并减少图片');
      // Server/AtomicFile is the authority. A failed save leaves the current editor untouched.
      clearTimeout(saveTimer);await save();await request('/api/save',next);snapshot();state=next;selected=0;revision++;savedRevision=revision;sync();pending=null;modal.close();status('已导入当前编辑槽，可继续修改；游戏存档未改动');byId('saveStatus').textContent='已保存到本地';
    }catch(e){status(e.message);}
  };
  window.CardPackage={build,prepare,newWork,inspect,preview,models,indices,cardDate:()=>metadata().cardDate||'',setCardDate:value=>edit(d=>{d.cardDate=value;}),refreshCardDate:()=>{const input=byId('diyCardDate');if(input)input.value=metadata().cardDate||'';}};
  window.dispatchEvent(new Event('card-package-ready'));
  CardProfile.attach({edit,metadata});
  DiyEditorFields.attach({edit,metadata});
  const createButton=document.createElement('button');createButton.id='diyCreatePlayer';createButton.textContent='＋ 新建球员';panel.prepend(createButton);
  const createDialog=document.createElement('dialog');createDialog.id='diyCreatePlayerDialog';createDialog.className='card-package-dialog';createDialog.innerHTML='<h2>新建球员</h2><label>姓名<input id="diyCreateName" maxlength="40" value="New Player"></label><div class="buttons"><button id="diyCreateConfirm" class="primary">创建</button><button id="diyCreateCancel">取消</button></div><p id="diyCreateStatus" role="status"></p>';document.body.append(createDialog);
  function workPicker(){if(!state)return;const picker=byId('player'),keys=Object.keys(state.players);if(keys.some(k=>![...picker.options].some(o=>o.value===k))||picker.options.length!==keys.length){picker.replaceChildren(...keys.map(k=>new Option(state.players[k].diy?.name||playerLabels[k]||k,k)));}for(const option of picker.options)option.textContent=state.players[option.value]?.diy?.name||playerLabels[option.value]||option.value;picker.value=player;}
  const librarySync=sync;sync=function(){if(state&&!state.players[player])player=Object.keys(state.players)[0];if(state){for(const [key,value]of Object.entries(state.players))if(!initial.players[key])initial.players[key]=copy(value);workPicker();}librarySync();};
  let newPlayerDraft=null;
  createButton.onclick=()=>{newPlayerDraft=null;byId('diyCreateStatus').textContent='';createDialog.showModal();};
  byId('diyCreateCancel').onclick=()=>createDialog.close();
  byId('diyCreateConfirm').onclick=async()=>{
    const button=byId('diyCreateConfirm');if(button.disabled)return;button.disabled=true;
    try{
      if(!newPlayerDraft){
        if(Object.keys(state.players).length>=1000)throw Error('作品库已达1000个球员，请先备份整理');
        const name=byId('diyCreateName').value.trim();
        if(!name||name.length>40||new TextEncoder().encode(name).length>60)throw Error('姓名请填写1–40字符且不超过60字节');
        const id=uuid(),key='work_'+id.replaceAll('-',''),canvas=document.createElement('canvas');canvas.width=canvas.height=1;
        const layer={asset:canvas.toDataURL(),x:32,y:32,width:448,ratio:1,opacity:1,visible:true,flipX:false,placeholder:true,name:'导入人物图片'};
        snapshot();state.players[key]={small:[copy(layer)],detail:[copy(layer)],detailCanvasHeight:720,calibration:{},diy:{...defaults(''),uuid:id,name}};
        newPlayerDraft=key;player=key;selected=0;changed();sync();
      }
      const expected=revision;await save();
      if(savedRevision<expected)throw Error('新球员尚未保存；请处理保存错误，再点击创建重试，不会重复新增');
      createDialog.close();byId('diyPlayerStatus').textContent='已创建独立作品；请选择模型、卡面套装并导入人物图片';
    }catch(e){byId('diyCreateStatus').textContent=e.message;}finally{button.disabled=false;}
  };
  setTimeout(workPicker,0);
  const modelSearch=document.createElement('div');modelSearch.className='card-fields';modelSearch.innerHTML='<label>游戏模型搜索<input id="diyModelQuery" type="search" maxlength="80" placeholder="English name / ID · 支持分词"></label><button id="diyModelSearch" type="button">搜索模型</button><button id="diyModelMore" type="button" hidden>下一页</button><p id="diyModelSearchStatus" role="status"></p>';byId('diyModel').parentElement.before(modelSearch);
  let modelOffset=0,modelQuery='',modelEpoch=0;
  async function searchModels(more=false){const epoch=++modelEpoch,button=byId('diyModelSearch');button.disabled=true;byId('diyModelMore').disabled=true;const query=byId('diyModelQuery').value.trim(),offset=more&&query===modelQuery?modelOffset:0;byId('diyModelSearchStatus').textContent='正在读取游戏模型目录…';try{const result=await request('/api/models/search',{q:query,offset,limit:60});if(epoch!==modelEpoch)return;if(!Array.isArray(result.models)||!Number.isInteger(result.total))throw Error('模型目录响应不完整');const select=byId('diyModel'),chosen=metadata().model.playerId;select.replaceChildren();for(const row of result.models){if(!row.available||!/^\d{1,16}$/.test(row.id))continue;const option=new Option(row.label+(row.available?'':' · '+row.reason),row.id);option.disabled=!row.available;select.add(option);if(row.available&&!models.some(m=>m.id===row.id))models.push({id:row.id,label:row.label});}if(![...select.options].some(o=>o.value===chosen)){const known=models.find(m=>m.id===chosen);const preserved=new Option(chosen?(known?.label||chosen)+' · 当前引用':'请选择游戏中的球员模型',chosen);preserved.hidden=!!chosen;select.add(preserved);}select.value=chosen;modelQuery=query;modelOffset=offset+result.models.length;byId('diyModelMore').hidden=modelOffset>=result.total;byId('diyModelSearchStatus').textContent='匹配 '+result.total+' 个游戏模型，当前第 '+(result.total?offset+1:0)+'–'+modelOffset+' 项；仅显示可用模型';}catch(e){if(epoch===modelEpoch)byId('diyModelSearchStatus').textContent='目录读取失败：'+e.message+'。保留当前模型，可重试搜索。';}finally{if(epoch===modelEpoch){button.disabled=false;byId('diyModelMore').disabled=false;}}}
  let modelLoaded=false;byId('diyModelSection').addEventListener('toggle',()=>{if(byId('diyModelSection').open&&!modelLoaded){modelLoaded=true;searchModels();}});
  let modelSearchTimer;byId('diyModelQuery').oninput=()=>{clearTimeout(modelSearchTimer);modelEpoch++;modelSearchTimer=setTimeout(()=>searchModels(),350);};byId('diyModelSearch').onclick=()=>{clearTimeout(modelSearchTimer);searchModels();};byId('diyModelMore').onclick=()=>searchModels(true);byId('diyModelQuery').onkeydown=e=>{if(e.key==='Enter'){e.preventDefault();searchModels();}};
  function validateBoosters(values){
    if(!Array.isArray(values)||values.length!==2||values.some((v,i)=>!Number.isInteger(v)||v<0||v>[255,1023][i]))throw Error('增能应为两个有效槽位，第一槽≤255、第二槽≤1023');
    if(values.some(v=>v!==0&&(!boosterRows||!boosterRows.some(r=>r.id===v))))throw Error(boosterRows?'增能编号不在球员编辑器目录中':'增能目录未就绪，请重试加载');
  }
  function refreshBoosters(){
    if(!state)return;const chosen=metadata().boosters||[0,0],term=byId('diyBoosterQuery').value.trim().toLowerCase();
    for(let slot=0;slot<2;slot++){
      const select=byId('diyBooster'+slot);select.replaceChildren(new Option('未启用',0));
      for(const row of (boosterRows||[]).filter(r=>Number(r.amount)>=4&&!/total\s*package|全能|全套/i.test((window.DiyI18n?.t(r.label)||r.label))).sort((a,b)=>a.amount-b.amount||a.id-b.id)){if(row.id>[255,1023][slot])continue;if(term&&!`${row.label} ${row.description} ${row.id}`.toLowerCase().includes(term)&&row.id!==chosen[slot])continue;select.add(new Option(row.label,row.id));}
      if(chosen[slot]&&!Array.from(select.options).some(o=>Number(o.value)===chosen[slot])){const option=new Option('已保存增能 · '+chosen[slot],chosen[slot]);option.disabled=true;select.add(option);}
      select.value=String(chosen[slot]);select.disabled=!boosterRows;
      byId('diyBoosterDescription'+slot).textContent=chosen[slot]?boosterRows?.find(r=>r.id===chosen[slot])?.description||'正在核对已保存增能；未确认前不能重新生成':'不附加此槽的增能，不继承模型球员的增能。';
    }
    byId('diyBoosterSummary').textContent=chosen.some(Boolean)?chosen.map(v=>v?boosterRows?.find(r=>r.id===v)?.label||('编号 '+v):'未启用').join(' / '):'未启用 · 可选双槽';
  }
  function loadBoosters(){
    byId('diyBoosterRetry').hidden=true;byId('diyBoosterStatus').textContent='正在读取增能目录…';
    boosterReady=request('/booster-catalog.json').then(c=>{
      if(c.schema!=='efootball-diy-boosters/v1'||JSON.stringify(c.limits)!=='[255,1023]'||!Array.isArray(c.rows)||!c.rows.length||new Set(c.rows.map(r=>r.id)).size!==c.rows.length||c.rows.some(r=>!Number.isInteger(r.id)||r.id<=0||r.id===136||r.id>1023||typeof r.label!=='string'||typeof r.description!=='string'))throw Error('增能目录格式错误');
      boosterRows=c.rows;refreshBoosters();byId('diyBoosterStatus').textContent='与球员编辑器共用 '+c.rows.length+' 项增能。条件增能仍需满足游戏条件，不会直接改写基础能力。';
    }).catch(e=>{boosterRows=null;refreshBoosters();byId('diyBoosterStatus').textContent='增能加载失败：'+e.message+'。原选择保留，可继续编辑卡面。';byId('diyBoosterRetry').hidden=false;throw e;});
    boosterReady.catch(()=>{});return boosterReady;
  }
  for(let slot=0;slot<2;slot++)byId('diyBooster'+slot).onchange=()=>edit(d=>{d.boosters=[...(d.boosters||[0,0])];d.boosters[slot]=Number(byId('diyBooster'+slot).value);});
  byId('diyBoosterQuery').oninput=refreshBoosters;byId('diyBoosterRetry').onclick=()=>loadBoosters();loadBoosters();
  if(state)refresh();
})();
