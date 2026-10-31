/* Phone-first workflow: import up to two portraits, drag/scale, choose game art. */
(() => {
  if(getComputedStyle(document.documentElement).getPropertyValue('--workspace-theme').trim()!=='black-purple')throw Error('黑紫工作区样式未加载');
  let resizeFrame=0;
  const root=document.documentElement,version='E169-mobile-10';
  if(root.dataset.workspaceVersion!==version||getComputedStyle(root).getPropertyValue('--workspace-version').trim()!==version)throw Error('编辑器资源版本不一致，请重新加载');
  const query=matchMedia('(max-width:700px), (max-height:500px) and (max-width:1000px), (pointer:coarse)');
  const phone=()=>root.dataset.workspaceMode==='phone'||query.matches;
  if(phone()&&getComputedStyle(root).getPropertyValue('--phone-layout-version').trim()!==version)throw Error('手机布局资源未加载，请重新加载');
  const main=document.querySelector('main'),left=main.querySelector('aside'),stage=main.querySelector(':scope > section'),controls=main.querySelector('.controls'),bg=document.getElementById('backgroundPicker');
  const anchor=document.createComment('background home');bg.before(anchor);
  const common=document.createElement('div');common.className='phone-common panel';
  const selector=document.getElementById('player'),tabs=document.getElementById('smallTab').parentElement;
  const selectorAnchor=document.createComment('selector home'),tabsAnchor=document.createComment('tabs home');selector.before(selectorAnchor);tabs.before(tabsAnchor);
  const quick=document.createElement('section');quick.className='phone-quick panel';quick.id='cardArtworkPanel';quick.dataset.phonePart='images';
  quick.innerHTML=`<h2>图片 · 点选后拖动画布</h2><button id="quickImport" class="primary full">＋ 导入图片（最多两张）</button><input id="quickFiles" type="file" accept="image/*" multiple><div id="quickSlots"></div><div class="quick-actions"><button id="quickLess">－ 缩小</button><button id="quickMore">＋ 放大</button><button id="quickCenter">居中</button><button id="quickFit">完整显示</button><button id="quickFlip" aria-pressed="false">左右翻转</button></div><p id="quickStatus" class="status" role="status" aria-live="polite"></p>`;
  main.prepend(quick);main.before(common);
  const preview=document.querySelector('.preview-grid'),previewAnchor=document.createComment('preview home');preview.before(previewAnchor);
  const previewDetails=document.createElement('div');previewDetails.className='phone-preview';
  const previewToggle=document.createElement('button');previewToggle.id='phonePreviewToggle';previewToggle.textContent='看成品';previewToggle.setAttribute('aria-pressed','false');
  stage.firstElementChild.append(previewToggle);let showingPreview=false;
  const collapseToggle=document.createElement('button');collapseToggle.id='phoneCanvasToggle';collapseToggle.type='button';collapseToggle.setAttribute('aria-controls','editor');stage.firstElementChild.append(collapseToggle);
  let canvasCollapsed=false;
  function setCanvasCollapsed(value){canvasCollapsed=value;main.classList.toggle('canvas-collapsed',value);collapseToggle.textContent=value?'展开制图':'收起制图';collapseToggle.setAttribute('aria-expanded',String(!value));resizeCanvas();}
  collapseToggle.onclick=()=>setCanvasCollapsed(!canvasCollapsed);setCanvasCollapsed(canvasCollapsed);
  previewToggle.onclick=()=>{showingPreview=!showingPreview;stage.classList.toggle('show-game-preview',showingPreview);previewToggle.textContent=showingPreview?'继续编辑':'看成品';previewToggle.setAttribute('aria-pressed',String(showingPreview));resizeCanvas();};
  const nav=document.createElement('nav');nav.className='phone-nav';nav.setAttribute('aria-label','制卡步骤');document.body.append(nav);
  const parts={canvas:stage,background:bg,adjust:controls};for(const [key,part]of Object.entries(parts))part.dataset.phonePart=key;
  left.dataset.phonePart='legacy';let view='canvas',replaceSlot=null;
  const extra={};
  window.cardToolPanel=(key,part)=>{extra[key]=part;part.dataset.phonePart=key;main.append(part);choose(view);};
  window.cardChooseTool=choose;
  function choose(next){view=next;if(next==='canvas'&&canvasCollapsed)setCanvasCollapsed(false);for(const [key,part]of Object.entries(extra))part.classList.toggle('phone-selected',key===view);for(const [key,part]of Object.entries(parts))part.classList.toggle('phone-selected',key===view||key==='canvas');quick.classList.toggle('phone-selected',view==='canvas');for(const b of nav.children){b.classList.toggle('active',b.dataset.view===view);b.setAttribute('aria-pressed',String(b.dataset.view===view));}resizeCanvas();}
  for(const [key,label]of Object.entries({canvas:'做卡面',background:'选模板',adjust:'调构图',player:'球员属性',share:'保存分享'})){const b=document.createElement('button');b.textContent=label;b.dataset.view=key;b.onclick=()=>{choose(key);window.dispatchEvent(new CustomEvent('card-tool-change',{detail:key}));};nav.append(b);}
  function slots(){if(typeof state==='undefined'||!state)return;const parent=document.getElementById('quickSlots');parent.replaceChildren();for(let n=0;n<2;n++){
    const layer=layers()[n],row=document.createElement('div');row.className='quick-slot';
    const pick=document.createElement('button');pick.className='quick-pick'+(n===selected?' active':'');pick.disabled=!layer;
    if(layer){const im=document.createElement('img');im.src=layer.asset;im.alt='';pick.append(im);}const text=document.createElement('span');text.textContent='图片 '+(n+1)+(n===0?' · 后景':' · 前景');pick.append(text);pick.onclick=()=>{selected=n;sync();};row.append(pick);
    const replace=document.createElement('button');replace.textContent=layer?'换图':'添加';replace.onclick=()=>{replaceSlot=n;document.getElementById('quickFiles').click();};row.append(replace);
    if(layer){const remove=document.createElement('button');remove.textContent='移除';remove.onclick=()=>{if(layer.locked){document.getElementById('quickStatus').textContent='图层已锁定，请先解锁';return;}snapshot();layers().splice(n,1);selected=Math.max(0,Math.min(selected,layers().length-1));changed();sync();};row.append(remove);}parent.append(row);
  }}
  const oldSync=sync;sync=function(){oldSync();slots();resizeCanvas();const b=document.getElementById('quickFlip');b.classList.toggle('active',!!current()?.flipX);b.setAttribute('aria-pressed',String(!!current()?.flipX));};
  document.getElementById('quickImport').onclick=()=>{replaceSlot=null;document.getElementById('quickFiles').click();};
  document.getElementById('quickFiles').onchange=async event=>{
    const status=document.getElementById('quickStatus'),files=Array.from(event.target.files||[]),who=player,kind=scene,target=replaceSlot;event.target.value='';
    if(!files.length)return;
    if(files.length>2||(target!==null&&files.length>1)){status.textContent=target===null?'最多选择两张图片，请重新选择':'换图时请选择一张图片';return;}
    try{status.textContent='正在处理图片…';const prepared=[];for(const file of files){if(!file.type.startsWith('image/'))throw Error('请选择图片文件');if(file.size>20*1024*1024)throw Error('单张图片请小于20MB');const a=await cropped(await fileData(file));await readyImage(a.src);prepared.push({...a,name:file.name});}
      if(player!==who||scene!==kind)throw Error('编辑页面已切换，请在当前页重新导入');
      if(prepared.some((_,n)=>layers()[target===null?n:target]?.locked))throw Error('目标图层已锁定，请先解锁');
      snapshot();const list=layers();prepared.forEach((a,n)=>{const index=target===null?n:target,prior=list[index];let width=prior?.width||Math.min(460,canvasHeight(player,scene)/(a.height/a.width));list[Math.min(index,list.length)]={asset:a.src,ratio:a.height/a.width,width,x:prior?.x??(512-width)/2,y:prior?.y??0,opacity:prior?.opacity??1,visible:true,flipX:prior?.flipX??false,name:a.name};});selected=Math.min(target??0,list.length-1);changed();sync();status.textContent='图片已导入，拖动调整即可 · 自动保存';
    }catch(error){status.textContent=error.message;}finally{replaceSlot=null;}
  };
  document.getElementById('quickFlip').onclick=()=>document.getElementById('flipX').click();
  document.getElementById('quickLess').onclick=()=>mutate(l=>l.width=clamp(l.width/1.1,1,4096));
  document.getElementById('quickMore').onclick=()=>mutate(l=>l.width=clamp(l.width*1.1,1,4096));
  document.getElementById('quickCenter').onclick=()=>mutate(l=>{l.x=(512-l.width)/2;l.y=(canvasHeight(player,scene)-l.width*l.ratio)/2;});
  document.getElementById('quickFit').onclick=()=>document.getElementById('fit').click();
  function resizeCanvas(){if(!phone()||resizeFrame)return;resizeFrame=requestAnimationFrame(()=>{resizeFrame=0;const box=stage.querySelector('.stage'),wrap=stage.querySelector('.canvas-wrap');if(!box||!state)return;const r=512/canvasHeight(player,scene);const width=Math.max(40,Math.min(box.clientWidth-16,(box.clientHeight-12)*r))+'px';if(wrap.style.width!==width)wrap.style.width=width;preview.querySelectorAll('.panel').forEach((p,i)=>p.hidden=showingPreview&&i!==(scene==='small'?0:1));});}
  new ResizeObserver(resizeCanvas).observe(stage);window.addEventListener('resize',resizeCanvas);
  function adapt(){if(phone()){common.append(selector,tabs);main.append(bg);previewDetails.append(preview);stage.append(previewDetails);}else{selectorAnchor.after(selector);tabsAnchor.after(tabs);anchor.after(bg);previewAnchor.after(preview);previewDetails.remove();stage.querySelector('.canvas-wrap').style.width='';preview.querySelectorAll('.panel').forEach(p=>p.hidden=false);}choose(view);slots();resizeCanvas();}
  query.addEventListener('change',adapt);adapt();
  document.documentElement.dataset.workspaceReady='true';
  window.dispatchEvent(new Event('card-workspace-ready'));
})();
