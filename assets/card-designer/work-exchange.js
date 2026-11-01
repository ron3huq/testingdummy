/* Non-destructive selected-work exchange and the existing finished-card preview. */
(() => {
  'use strict';
  const $=id=>document.getElementById(id), MAX=40_000_000, encoder=new TextEncoder();
  let selecting=false,busy=false,pending=null;const chosen=new Set();
  const say=s=>DiyLab.notify(s);
  const stable=v=>JSON.stringify(v,(_,x)=>x&&typeof x==='object'&&!Array.isArray(x)?Object.fromEntries(Object.entries(x).sort(([a],[b])=>a.localeCompare(b))):x);
  function checkSize(text){if(encoder.encode(text).length>MAX)throw Error('导出工程超过40MB，请减少所选作品后重试');}
  function active(key){return state.players[key]&&!state.diyTestLibrary?.trash?.[key];}
  function update(){
    // The original navigator owns visibility; the new actions follow its trash state.
    const inTrash=$('labLibraryTitle').textContent==='回收站';
    if(inTrash){selecting=false;chosen.clear();}
    $('labSelectExport').hidden=inTrash;$('labSelectExport').disabled=busy;
    $('labSelectExport').textContent=selecting?'取消选择':'导出';
    $('labExportSelectionBar').hidden=!selecting;
    $('labExportSelected').disabled=busy||!chosen.size;
    $('labExportSelected').textContent=busy?'正在整理…':`导出所选（${chosen.size}）`;
    $('labSelectCount').textContent=`已选择 ${chosen.size} 张 · 搜索后保留选择`;
    $('labImport').disabled=selecting||busy;$('labNew').disabled=selecting||busy;
    $('labTrash').disabled=busy;
    for(const card of $('labWorks').children){
      const key=card.dataset.work;if(!key)continue;
      let box=card.querySelector('.lab-work-select');
      if(!box){box=document.createElement('input');box.type='checkbox';box.className='lab-work-select';box.setAttribute('aria-label','选择 '+(state.players[key].diy?.name||'草稿'));box.onchange=()=>{if(box.checked)chosen.add(key);else chosen.delete(key);update();};card.prepend(box);}
      box.hidden=!selecting;box.disabled=busy;box.checked=chosen.has(key);
      card.classList.toggle('lab-work-selected',selecting&&chosen.has(key));
      card.querySelector('.lab-work-action').hidden=selecting;
      card.querySelector('.lab-work-action').disabled=busy;
      card.querySelector('.lab-work-edit').disabled=busy||inTrash;
      card.querySelector('.lab-work-edit').setAttribute('aria-pressed',String(selecting&&chosen.has(key)));
    }
  }
  async function portable(keys){
    if(!Array.isArray(keys)||!keys.length||new Set(keys).size!==keys.length||keys.some(k=>!active(k)))throw Error('请选择有效作品，回收站作品请先恢复');
    await DiyLab.persist();
    const before=revision, players=Object.fromEntries(keys.map(k=>[k,copy(state.players[k])])), backgrounds=new Set();
    const project={schema:state.schema,canvas:copy(state.canvas),assets:{},players,backgroundLibrary:[],diyTestLibrary:{schema:'diy-test-library/v1',trash:{},updated:{}},diyTestExchange:{schema:'diy-test-works/v1',count:keys.length}};
    const converted=new Map();let estimated=0;
    async function embed(src){
      if(typeof src!=='string'||!src)throw Error('作品图片引用缺失');
      if(converted.has(src))return converted.get(src);
      const im=await readyImage(src);if(im.naturalWidth>4096||im.naturalHeight>4096)throw Error('图片尺寸超过4096，请缩小图片后导出');
      const c=document.createElement('canvas');c.width=im.naturalWidth;c.height=im.naturalHeight;c.getContext('2d').drawImage(im,0,0);
      const data=c.toDataURL('image/png');if(data==='data:,')throw Error('图片转换失败');estimated+=data.length;if(estimated>MAX)throw Error('作品素材超过40MB，请减少选择');converted.set(src,data);return data;
    }
    for(const [key,p]of Object.entries(players)){
      for(const kind of ['small','detail'])for(const layer of p[kind])layer.asset=await embed(layer.asset);
      for(const cfg of Object.values(p.appearance||{}))for(const id of Object.values(cfg))if(id)backgrounds.add(id);
      for(const v of Object.values(p.calibration||{}))if(v.screenshot)v.screenshot=await embed(v.screenshot);
      if(state.diyTestLibrary?.updated?.[key])project.diyTestLibrary.updated[key]=copy(state.diyTestLibrary.updated[key]);
    }
    for(const [id,a]of Object.entries(state.assets))if(converted.has(a.src))project.assets[id]={...copy(a),src:converted.get(a.src)};
    await CardBackgrounds.ready;
    for(const id of backgrounds){const a=CardBackgrounds.resolve(id);if(!a)throw Error('背景素材缺失：'+id);project.backgroundLibrary.push({...copy(a),src:await embed(a.src)});}
    if(revision!==before||keys.some(k=>!active(k)))throw Error('整理期间作品发生变化，请重新导出');
    const text=JSON.stringify(project);checkSize(text);await request('/api/validate',project);
    if(revision!==before)throw Error('校验期间作品发生变化，请重新导出');
    return {project,text};
  }
  async function exportChosen(){
    if(busy||!chosen.size)return;busy=true;update();
    try{const before=revision,{project}=await portable([...chosen]),archive=await WorkArchive.encode(project);if(revision!==before)throw Error('整理ZIP期间作品发生变化，请重新导出');WorkArchive.downloadZip(archive,`DIY作品-${chosen.size}张.zip`);say('ZIP已准备，请选择保存位置；包含所选作品和全部图片');}
    catch(e){say('导出未完成：'+e.message);}finally{busy=false;update();}
  }
  async function canonicalImage(src){
    const im=await readyImage(src);if(im.naturalWidth>4096||im.naturalHeight>4096)throw Error('分享图片尺寸超过4096');
    const c=document.createElement('canvas');c.width=im.naturalWidth;c.height=im.naturalHeight;c.getContext('2d').drawImage(im,0,0);return c.toDataURL('image/png');
  }
  async function canonicalPlayer(p){const v=copy(p);for(const kind of ['small','detail'])for(const l of v[kind])l.asset=await canonicalImage(l.asset);for(const c of Object.values(v.calibration||{}))if(c.screenshot)c.screenshot=await canonicalImage(c.screenshot);return stable(v);}
  async function merge(local,incoming){
    const v=copy(local),seen=new Map(Object.entries(v.players).filter(([,p])=>p.diy?.uuid).map(([k,p])=>[p.diy.uuid.toLowerCase(),k]));
    let added=0,skipped=0;
    const lib=v.diyTestLibrary||(v.diyTestLibrary={schema:'diy-test-library/v1',trash:{},updated:{}});
    for(const [oldKey,p]of Object.entries(incoming.players)){
      const existing=p.diy?.uuid?seen.get(p.diy.uuid.toLowerCase()):undefined;
      if(existing){if(await canonicalPlayer(v.players[existing])!==await canonicalPlayer(p))throw Error('相同作品编号的内容不同，原作品保留；请先在来源另存为新作品');skipped++;continue;}
      let key=oldKey;if(Object.hasOwn(v.players,key))key='work_'+crypto.randomUUID().replaceAll('-','');
      v.players[key]=copy(p);if(p.diy?.uuid)seen.set(p.diy.uuid.toLowerCase(),key);
      if(incoming.diyTestLibrary?.updated?.[oldKey])lib.updated[key]=copy(incoming.diyTestLibrary.updated[oldKey]);added++;
    }
    v.backgroundLibrary=v.backgroundLibrary||[];
    for(const a of incoming.backgroundLibrary||[]){const old=v.backgroundLibrary.find(x=>x.id===a.id);if(old&&stable({...old,src:await canonicalImage(old.src)})!==stable({...a,src:await canonicalImage(a.src)}))throw Error('背景素材编号冲突，原工程保留');if(!old)v.backgroundLibrary.push(copy(a));}
    for(const [key,a]of Object.entries(incoming.assets||{})){if(!Object.hasOwn(v.assets,key))v.assets[key]=copy(a);else if(stable(v.assets[key])!==stable(a)&&stable({...v.assets[key],src:await canonicalImage(v.assets[key].src)})!==stable({...a,src:await canonicalImage(a.src)}))v.assets['import_'+crypto.randomUUID().replaceAll('-','')]=copy(a);}
    delete v.diyTestExchange;
    return {project:v,added,skipped};
  }
  async function importSelected(file){
    if(file.size>MAX)throw Error('导入文件超过40MB');
    const header=new Uint8Array(await file.slice(0,4).arrayBuffer());
    const isZip=header[0]===80&&header[1]===75;
    if(file.name.toLowerCase().endsWith('.zip')&&!isZip)throw Error('ZIP文件头已损坏');
    const v=isZip?await WorkArchive.decode(new Uint8Array(await file.arrayBuffer())):JSON.parse(await file.text());
    if(v.diyTestExchange?.schema!=='diy-test-works/v1')return false;
    await DiyEditorFields.ready;
    if(v.diyTestExchange.count!==Object.keys(v.players||{}).length||Object.keys(v.diyTestLibrary?.trash||{}).length)throw Error('分享作品数量或回收站标记错误');
    await request('/api/validate',v);
    for(const p of Object.values(v.players)){
      for(const kind of ['small','detail'])for(const l of p[kind]){if(!l.asset.startsWith('data:image/'))throw Error('分享缺少内嵌人物图片');await readyImage(l.asset);}
      for(const cfg of Object.values(p.appearance||{}))for(const id of Object.values(cfg))if(id&&!(v.backgroundLibrary||[]).some(b=>b.id===id))throw Error('分享缺少所选背景：'+id);
      for(const c of Object.values(p.calibration||{}))if(c.screenshot){if(!c.screenshot.startsWith('data:image/'))throw Error('分享缺少内嵌校准图片');await readyImage(c.screenshot);}
    }
    for(const a of Object.values(v.assets)){if(!a.src.startsWith('data:image/'))throw Error('分享缺少内嵌素材');await readyImage(a.src);}
    for(const b of v.backgroundLibrary||[]){if(!b.src.startsWith('data:image/'))throw Error('分享缺少内嵌背景图片');await readyImage(b.src);}
    await DiyLab.persist();pending={incoming:v};
    // Detect conflicts before showing confirmation. Recompute again at commit.
    const result=await merge(state,v);$('labImportSelectionInfo').textContent=`包含 ${v.diyTestExchange.count} 张作品，新增 ${result.added} 张，已有相同作品 ${result.skipped} 张。原有作品与回收站保持。`;
    $('labImportSelectionDialog').showModal();return true;
  }
  async function confirmImport(){
    if(!pending||busy)return;busy=true;$('labImportSelectionConfirm').disabled=true;
    try{
      await DiyLab.persist();const before=revision,{project:v,added,skipped}=await merge(state,pending.incoming);
      const text=JSON.stringify(v);checkSize(text);await request('/api/validate',v);
      if(before!==revision)throw Error('校验期间工程已变化，请重新导入');
      // request before changing local state: save failure leaves local/undo intact.
      await request('/api/save',v);snapshot();state=portraitProject(v);revision++;savedRevision=revision;
      if(!state.players[player])player=Object.keys(state.players)[0];selected=0;sync();
      pending=null;$('labImportSelectionDialog').close();await DiyLab.refreshHome();say(`已导入 ${added} 张，跳过相同作品 ${skipped} 张`);
    }catch(e){say('导入未完成：'+e.message);}finally{busy=false;$('labImportSelectionConfirm').disabled=false;update();}
  }
  function boot(){
    const b=document.createElement('button');b.id='labSelectExport';b.textContent='导出';$('labImport').before(b);
    const bar=document.createElement('div');bar.id='labExportSelectionBar';bar.hidden=true;
    bar.innerHTML='<span id="labSelectCount"></span><div class="buttons"><button id="labSelectAll" type="button">全选当前结果</button><button id="labClearSelection" type="button">清空选择</button><button id="labExportSelected" class="lab-primary" type="button" disabled>导出所选（0）</button></div>';
    $('labWorks').before(bar);
    b.onclick=()=>{if(busy)return;selecting=!selecting;chosen.clear();update();};
    $('labSelectAll').onclick=()=>{for(const c of $('labWorks').children)if(active(c.dataset.work))chosen.add(c.dataset.work);update();};
    $('labClearSelection').onclick=()=>{chosen.clear();update();};$('labExportSelected').onclick=exportChosen;
    $('labWorks').addEventListener('click',e=>{if(!selecting)return;const card=e.target.closest('.lab-work');if(!card||e.target.matches('.lab-work-select'))return;if(e.target.closest('.lab-work-edit')){e.preventDefault();e.stopImmediatePropagation();if(!busy){const k=card.dataset.work;chosen.has(k)?chosen.delete(k):chosen.add(k);update();}}},true);
    new MutationObserver(update).observe($('labWorks'),{childList:true});
    new MutationObserver(update).observe($('labLibraryTitle'),{childList:true});
    const d=document.createElement('dialog');d.id='labImportSelectionDialog';d.className='lab-dialog';d.innerHTML='<h2>导入分享作品</h2><p id="labImportSelectionInfo"></p><button id="labImportSelectionConfirm" class="lab-primary">确认添加作品</button><button id="labImportSelectionCancel">取消</button>';document.body.append(d);
    $('labImportSelectionConfirm').onclick=confirmImport;$('labImportSelectionCancel').onclick=()=>{pending=null;d.close();};
    $('projectInput').accept='application/json,.json,application/zip,.zip';
    const previousImport=$('projectInput').onchange;
    $('projectInput').onchange=async e=>{
      const file=e.target.files[0];if(!file)return;
      if(busy){e.target.value='';say('请先完成当前导出或导入');return;}busy=true;update();
      try{await DiyEditorFields.ready;if(await importSelected(file)){e.target.value='';return;}await previousImport(e);await DiyLab.refreshHome();}
      catch(error){pending=null;e.target.value='';say('导入未完成：'+error.message);}
      finally{busy=false;update();}
    };
    const preview=document.createElement('dialog');preview.id='labFinishedPreview';preview.className='lab-dialog lab-finished-preview';preview.innerHTML='<div class="lab-preview-heading"><h2>成品预览</h2><button id="labFinishedPreviewClose">返回编辑</button></div><p>小框与大框同时预览，游戏内遮挡以实际显示为准。</p>';
    // Reuse the original preview DOM and live canvases, keeping the render pipeline.
    preview.append(document.querySelector('.preview-grid'));document.body.append(preview);
    const view=document.createElement('button');view.id='labPreview';view.textContent='成品预览';view.onclick=()=>{render();preview.showModal();};$('labScene').append(view);
    $('labFinishedPreviewClose').onclick=()=>preview.close();update();
    window.WorkExchange={portable,merge,checkSize};document.documentElement.dataset.diyControlsReady='true';
  }
  const timer=setInterval(()=>{if(document.documentElement.dataset.diyLabReady==='true'){clearInterval(timer);boot();}},50);
})();
