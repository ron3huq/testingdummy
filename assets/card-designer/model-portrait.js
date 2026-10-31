/* Recognition portrait only; never changes artwork or claims a 3D render. */
(() => {
  const get=id=>document.getElementById(id),section=get('diyModelSection');
  const box=document.createElement('div');box.className='diy-model-portrait';
  box.innerHTML='<img id="diyModelPortrait" alt="已选球员头像" hidden><div><strong id="diyModelPortraitName"></strong><p id="diyModelPortraitStatus" role="status">选择球员模型后显示头像</p><button id="diyModelPortraitRetry" type="button" hidden>重试加载头像</button></div>';
  section.append(box);
  const style=document.createElement('style');style.textContent='.diy-model-portrait{display:flex;gap:12px;align-items:center;margin-top:12px;min-height:70px}.diy-model-portrait img{width:96px;height:112px;flex-shrink:0;object-fit:contain;border-radius:10px;background:#20172d}.diy-model-portrait p{font-size:12px;color:#c2b7d5;margin:6px 0}.diy-model-portrait strong{overflow-wrap:anywhere}';document.head.append(style);
  const cache=new Map();let last='',epoch=0;
  async function show(force=false){
    if(!state||!section.open)return;
    const select=get('diyModel'),id=select.value;
    if(!force&&id===last)return;last=id;const token=++epoch;
    const image=get('diyModelPortrait'),status=get('diyModelPortraitStatus'),retry=get('diyModelPortraitRetry');
    image.hidden=true;image.removeAttribute('src');retry.hidden=true;
    get('diyModelPortraitName').textContent=select.selectedOptions[0]?.textContent||id;
    if(!id){status.textContent='选择球员模型后显示头像';return;}
    status.textContent='正在读取球员头像…';
    try{
      let portrait=cache.get(id);
      if(!portrait){
        const list=await request('/api/materials/list',{playerId:id,query:'',kind:'portrait',page:0});
        if(token!==epoch)return;
        // Alternative keys come only from the trusted exact-player endpoint.
        const exactKeys=list.portraitKeys||[id];
        const names=exactKeys.flatMap(key=>[key+'_',key+'f',key+'_l',key]);
        const item=(list.items||[]).filter(row=>names.includes(row.name)).sort((a,b)=>names.indexOf(a.name)-names.indexOf(b.name))[0];
        if(!item){status.textContent='当前资源未找到对应头像，模型仍可选择';return;}
        portrait=await request('/api/materials/image',{id:item.id});
        if(token!==epoch)return;
        if(!portrait.src?.startsWith('data:image/png;base64,'))throw Error('头像图片格式错误');
        await readyImage(portrait.src);
        if(token!==epoch)return;
        cache.set(id,portrait);while(cache.size>24)cache.delete(cache.keys().next().value);
      }
      if(token!==epoch)return;
      image.src=portrait.src;image.alt=(portrait.label||select.selectedOptions[0]?.textContent||id)+' 头像';image.hidden=false;
      status.textContent='球员头像 · 用于确认人物';
    }catch(error){if(token===epoch){status.textContent='头像加载失败：'+error.message;retry.hidden=false;}}
  }
  const baseSync=sync;sync=function(){baseSync();show();};
  get('diyModel').addEventListener('change',()=>show());
  section.addEventListener('toggle',()=>show());
  get('diyModelPortraitRetry').onclick=()=>show(true);
})();
