/* Curated original backgrounds; portraits and exported PNGs remain separate. */
(() => {
  const panel=document.createElement('section');panel.id='backgroundPicker';
  panel.innerHTML='<p id="bgSummary" class="hint">正在读取精选背景…</p>';
  document.querySelector('aside.panel').insertBefore(panel,document.querySelector('aside.panel h3'));
  const css=document.createElement('style');css.textContent=`
    .game-bg-image,.game-frame-image{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;pointer-events:none}
    .game-bg-image{z-index:0}.game-frame-image{z-index:3}
    .small-card #smallPreview,.detail-card #detailPreview{position:absolute;z-index:1}
    .detail-card .card-text,.detail-card .detail-name{z-index:4}
    .small-card[data-game-style=true]:after{display:none}
    .small-card[data-game-style=true] .card-foot,.detail-card[data-game-style=true] .card-foot{display:none}
    .small-card[data-game-style=true],.detail-card[data-game-style=true]{background:#100c18;border:0}
    #backgroundPicker .suite-small{width:48px!important;height:48px!important;object-fit:contain!important;position:absolute;inset:auto 4px 4px auto!important;z-index:4;background:#171020!important;border-radius:4px!important}
    #backgroundPicker .suite-tile-art{position:relative;aspect-ratio:182/256;overflow:hidden}
    #backgroundPicker .suite-tile-art>.suite-bg{width:100%;height:100%;object-fit:contain!important}
    #videoToggle{min-height:30px;padding:4px 12px}.suite-mark{font-size:10px}
  `;document.head.append(css);
  let catalog=null,playing=false,lastFrame=0,raf=0;
  const byId=id=>document.getElementById(id);
  const resolve=id=>{const local=catalog?.assets.find(a=>a.id===id),saved=(state?.backgroundLibrary||[]).find(a=>a.id===id);return local?{...local,...saved,videoSrc:local.videoSrc}:saved;};
  for(const kind of ['small','detail'])for(const type of ['bg','frame']){
    const im=document.createElement('img');im.id=kind+'Game'+type;im.className='game-'+type+'-image';im.hidden=true;im.alt='';document.querySelector('.'+kind+'-card').append(im);
  }
  function tick(){} // Video elements animate independently; no full-editor repaint loop.
  function paint(){
    if(!catalog||!state)return;
    for(const kind of ['small','detail']){
      const cfg=state.players[player].appearance?.[kind]||{};
      document.querySelector('.'+kind+'-card').dataset.gameStyle=String(!!(resolve(cfg.background)||resolve(cfg.frame)));
      for(const [type,key]of [['bg','background'],['frame','frame']]){
        const a=resolve(cfg[key]),id=kind+'Game'+type;let node=byId(id);const isVideo=!!a?.videoSrc;
        if((node.tagName==='VIDEO')!==isVideo){
          if(node.tagName==='VIDEO'){node.pause();node.removeAttribute('src');node.load();}
          const next=document.createElement(isVideo?'video':'img');next.id=id;next.className=node.className;next.alt='';node.replaceWith(next);node=next;
          if(isVideo){node.muted=true;node.loop=true;node.playsInline=true;node.preload='metadata';node.addEventListener('loadeddata',()=>{render();tick();});node.addEventListener('play',tick);}
        }
        node.hidden=!a;if(!a)continue;
        const src=isVideo?a.videoSrc:a.src;if(node.getAttribute('src')!==src){if(isVideo)node.poster=a.src;node.src=src;}
        if(isVideo){if(playing&&!document.hidden){if(node.paused)node.play().catch(()=>{});}else node.pause();}
      }
    }
    tick();
  }
  function draw(context,who,kind,key){
    const a=resolve(state.players[who].appearance?.[kind]?.[key]);if(!a)return;
    const media=who===player&&key==='background'?byId(kind+'Gamebg'):null;
    const im=media?.tagName==='VIDEO'&&media.getAttribute('src')===a.videoSrc&&media.readyState>=2?media:imageFor(a.src);
    const width=im.videoWidth||im.naturalWidth,height=im.videoHeight||im.naturalHeight;if(!width||!height)return;
    const h=canvasHeight(who,kind),scale=Math.min(512/width,h/height),w=width*scale,hh=height*scale;
    context.drawImage(im,(512-w)/2,(h-hh)/2,w,hh);
  }
  const oldRender=render;render=function(){oldRender();paint();};
  const portable=portableProject;portableProject=async function(){
    const v=await portable(),ids=new Set();for(const p of Object.values(v.players))for(const c of Object.values(p.appearance||{}))for(const id of [c.background,c.frame])if(id)ids.add(id);
    v.backgroundLibrary=[];for(const id of ids){const a=resolve(id);if(!a)throw Error('背景素材缺失：'+id);const im=await readyImage(a.src),c=document.createElement('canvas');c.width=im.naturalWidth;c.height=im.naturalHeight;c.getContext('2d').drawImage(im,0,0);v.backgroundLibrary.push({...a,src:c.toDataURL()});}return v;
  };
  window.CardBackgrounds={resolve,paint,draw,ready:null,setPlaying(value){playing=!!value;paint();},get playing(){return playing;}};
  document.addEventListener('visibilitychange',paint);
  CardBackgrounds.ready=(async()=>{catalog=await request('/backgrounds.json');if(!catalog.curated)throw Error('精选视频目录未就绪，请更新完整编辑器资源');byId('bgSummary').textContent='仅保留精选完整背景；小框使用原版独立素材，不裁切详情图。人物导出保持透明，原生套装随工程保存。';if(state)render();return catalog;})();
  CardBackgrounds.ready.catch(e=>byId('bgSummary').textContent=e.message);
})();
