/* Raster edits keep the existing project/share/native layer contract unchanged. */
(() => {
  'use strict';
  const pointers = new Map();
  let target = null, start = null, gesture = false, erasing = false, brush = null;
  let busy = false, radians = 0, stroke = null;
  const get = id => document.getElementById(id);
  const actions = document.querySelector('#artTools .art-actions');
  const toggle = document.createElement('button'); toggle.id = 'artErase';
  toggle.textContent = '擦除素材'; toggle.setAttribute('aria-pressed', 'false');
  actions.append(toggle);
  const tools = document.createElement('label'); tools.id = 'artEraseOptions'; tools.hidden = true;
  tools.innerHTML = '擦除笔刷大小 <input id="artEraseSize" type="range" min="4" max="120" value="30"><button id="artEraseDone" type="button">完成擦除</button><small>只擦当前素材，支持撤销；不会擦掉背景或其他图层。</small>';
  actions.after(tools);
  function mode(value) {
    erasing = value; tools.hidden = !value;
    toggle.setAttribute('aria-pressed', String(value));
    toggle.textContent = value ? '正在擦除 · 点此退出' : '擦除素材';
    get('labCanvasHint') && (get('labCanvasHint').textContent = value ? '在素材上涂抹擦除 · 可撤销' : '单指移动 · 双指缩放旋转');
  }
  toggle.onclick = () => mode(!erasing);
  get('artEraseDone').onclick = () => mode(false);
  function hit(p) {
    for (let i = layers().length - 1; i >= 0; i--) {
      const l = layers()[i];
      if (l.visible && !l.locked && p.x >= l.x && p.x <= l.x + l.width && p.y >= l.y && p.y <= l.y + l.width*l.ratio) return i;
    }
    return -1;
  }
  function raster(l) {
    const im = imageFor(l.asset);
    if (!im.complete || !im.naturalWidth) throw Error('素材尚未加载，请稍后重试');
    const r = sourceRect(im,l), c = document.createElement('canvas');
    c.width = r.w; c.height = r.h;
    const x = c.getContext('2d');
    if(l.flipX){x.translate(c.width,0);x.scale(-1,1);}
    x.drawImage(im,r.x,r.y,r.w,r.h,0,0,c.width,c.height);
    return c;
  }
  function local(p) {return {x:(p.x-target.x)*brush.width/target.width,y:(p.y-target.y)*brush.height/(target.width*target.ratio)};}
  function erase(p) {
    const q=local(p), x=brush.getContext('2d');
    x.globalCompositeOperation='destination-out'; x.lineCap=x.lineJoin='round';
    x.lineWidth=Number(get('artEraseSize').value)*brush.width/target.width;
    x.beginPath();x.moveTo((stroke||q).x,(stroke||q).y);x.lineTo(q.x+.001,q.y);x.stroke();stroke=q;
    target.asset=brush.toDataURL('image/png');target.flipX=false;delete target.crop;
    imageFor(target.asset);render();
  }
  function beginPair() {
    const [a,b]=[...pointers.values()];
    const cx=(a.x+b.x)/2,cy=(a.y+b.y)/2;
    start={distance:Math.max(1,Math.hypot(b.x-a.x,b.y-a.y)),angle:Math.atan2(b.y-a.y,b.x-a.x),
      cx,cy,x:target.x,y:target.y,width:target.width,centerX:target.x+target.width/2,centerY:target.y+target.width*target.ratio/2};
    gesture=true;dragging=null;radians=0;
  }
  editor.onpointerdown=e=>{
    if(busy||pointers.size>=2)return;
    const p=point(e);
    if(!pointers.size){
      const i=hit(p);if(i<0)return;selected=i;sync();target=current();snapshot();
      if(erasing){try{brush=raster(target);stroke=null;}catch(error){inform(error.message,true);return;}}
      else dragging={id:e.pointerId,x:p.x,y:p.y,lx:target.x,ly:target.y};
    } else if(erasing) return;
    pointers.set(e.pointerId,p);editor.setPointerCapture(e.pointerId);e.preventDefault();
    if(pointers.size===2)beginPair();else if(erasing)erase(p);
  };
  editor.onpointermove=e=>{
    if(!pointers.has(e.pointerId)||!target||target!==current()||target.locked)return;
    const p=point(e);pointers.set(e.pointerId,p);e.preventDefault();
    if(erasing){erase(p);return;}
    if(gesture&&pointers.size===2){
      const [a,b]=[...pointers.values()],scale=clamp(Math.hypot(b.x-a.x,b.y-a.y)/start.distance,1/start.width,4096/start.width);
      radians=Math.atan2(b.y-a.y,b.x-a.x)-start.angle;
      const dx=(start.centerX-start.cx)*scale,dy=(start.centerY-start.cy)*scale;
      const cx=(a.x+b.x)/2+dx*Math.cos(radians)-dy*Math.sin(radians),cy=(a.y+b.y)/2+dx*Math.sin(radians)+dy*Math.cos(radians);
      target.width=start.width*scale;target.x=clamp(cx-target.width/2,-4096,4096);target.y=clamp(cy-target.width*target.ratio/2,-4096,4096);render();
    }else if(dragging){target.x=clamp(dragging.lx+p.x-dragging.x,-4096,4096);target.y=clamp(dragging.ly+p.y-dragging.y,-4096,4096);render();}
  };
  function bakeRotation(l,angle){
    if(Math.abs(angle)<.001)return;
    const source=raster(l),w=l.width,h=w*l.ratio,cs=Math.abs(Math.cos(angle)),sn=Math.abs(Math.sin(angle));
    const outW=w*cs+h*sn,outH=w*sn+h*cs;
    if(outW>4096||outH/outW>100)throw Error('旋转后尺寸超出范围，请缩小素材');
    const c=document.createElement('canvas'),scale=Math.min(1,2000/Math.max(outW,outH));
    c.width=Math.max(1,Math.round(outW*scale));c.height=Math.max(1,Math.round(outH*scale));
    const x=c.getContext('2d');x.translate(c.width/2,c.height/2);x.rotate(angle);x.drawImage(source,-w*scale/2,-h*scale/2,w*scale,h*scale);
    l.x=clamp(l.x+(w-outW)/2,-4096,4096);l.y=clamp(l.y+(h-outH)/2,-4096,4096);l.width=outW;l.ratio=outH/outW;
    l.asset=c.toDataURL('image/png');l.flipX=false;delete l.crop;
  }
  function finish(e){
    if(!pointers.has(e.pointerId))return;
    pointers.delete(e.pointerId);
    if(gesture&&pointers.size){return;}
    if(pointers.size)return;
    try{if(gesture)bakeRotation(target,radians);}catch(error){inform(error.message,true);}
    radians=0;gesture=false;dragging=null;brush=null;stroke=null;
    changed();sync();target=null;
  }
  editor.onpointerup=finish;editor.onpointercancel=finish;
  editor.addEventListener('lostpointercapture',finish);
  window.CardGestures={angle:l=>gesture&&target===l?radians:0,eraseMode:mode};
})();
