/* Standalone persisted player controls; never writes game resources or saves. */
(() => {
  'use strict';
  const $=id=>document.getElementById(id), mainIndex=[12,9,10,11,5,6,7,8,4,2,3,1,0];
  let api,catalog;
  const ready=request('/editor-catalog.json').then(c=>{
    if(c.schema!=='diy-test-editor-catalog/v1'||c.positions.length!==13||c.aptitudes.length!==13)throw Error('编辑器目录版本错误');
    catalog=c;return c;
  });ready.catch(()=>{});
  function validate(s,{previous}={}){
    if(!s||typeof s!=='object'||Array.isArray(s)||Object.keys(s).some(k=>!['position','aptitudes','personalization','stars'].includes(k)))throw Error('球员扩展设置字段错误');
    if(Object.hasOwn(s,'stars')&&(!Number.isInteger(s.stars)||s.stars<1||(s.stars>4&&!(s.stars===5&&previous?.stars===5))))throw Error('球员星级应为1–4；5星在当前游戏显示异常');
    if(Object.hasOwn(s,'position')&&(!Number.isInteger(s.position)||s.position<0||s.position>12))throw Error('主位置超出范围');
    if(Object.hasOwn(s,'aptitudes')){
      if(!Object.hasOwn(s,'position')||!Array.isArray(s.aptitudes)||s.aptitudes.length!==13||s.aptitudes.some(v=>!Number.isInteger(v)||v<0||v>2)||s.aptitudes[mainIndex[s.position]]!==2)throw Error('位置适性错误，主位置须完全熟练');
    } else if(Object.hasOwn(s,'position'))throw Error('位置适性缺失');
    if(Object.hasOwn(s,'personalization')){
      const p=s.personalization;
      if(!p||typeof p!=='object'||Array.isArray(p)||Object.keys(p).some(k=>!['sleeve','boots_id','boots_color','celebration','motion_profile'].includes(k)))throw Error('个性化设置字段错误');
      if(!catalog&&Object.keys(p).length)throw Error('个性化目录未就绪，请稍后重试');
      if(Object.hasOwn(p,'sleeve')&&!catalog.sleeves.some(r=>r.id===p.sleeve))throw Error('袖长选项错误');
      if(Object.hasOwn(p,'boots_id')&&(!Number.isInteger(p.boots_id)||!catalog.boots.some(r=>r.id===p.boots_id)))throw Error('球鞋未登记');
      if(Object.hasOwn(p,'boots_color')&&(typeof p.boots_color!=='string'||!/^#[0-9a-f]{6}$/i.test(p.boots_color)))throw Error('球鞋颜色格式错误');
      if(Object.hasOwn(p,'celebration')&&(!Number.isInteger(p.celebration)||!catalog.celebrations.some(r=>r.id===p.celebration)))throw Error('纪念庆祝未登记');
      if(Object.hasOwn(p,'motion_profile')&&!catalog.motions.some(r=>r.id===p.motion_profile))throw Error('动作组合未登记');
    }
    return JSON.parse(JSON.stringify(s));
  }
  function change(fn){api.edit(d=>{const previous=d.editorSettings||{},s=JSON.parse(JSON.stringify(previous));fn(s);d.editorSettings=validate(s,{previous});});}
  function refresh(){
    if(!api||!catalog||typeof state==='undefined'||!state)return;
    const s=api.metadata().editorSettings||{},p=s.personalization||{};
    $('editor-stars').querySelector('[data-legacy]')?.remove();
    if(s.stars===5){const old=new Option('旧版5星（请选择1–4）','5');old.disabled=true;old.dataset.legacy='true';$('editor-stars').add(old);}
    $('editor-stars').value=Object.hasOwn(s,'stars')?String(s.stars):'';
    $('editor-position').value=Object.hasOwn(s,'position')?String(s.position):'';
    for(const b of $('editor-pitch').querySelectorAll('button')){
      const i=Number(b.dataset.aptitude),v=s.aptitudes?.[i],locked=mainIndex[s.position]===i;
      b.dataset.level=v===undefined?'inherit':String(v);b.disabled=s.position===undefined;
      b.textContent=catalog.aptitudes[i]+'\n'+(v===undefined?'沿用模型':['不熟练','部分熟练','完全熟练'][v])+(locked?' · 主':'');
      b.setAttribute('aria-label',b.textContent.replace('\n','，'));b.setAttribute('aria-pressed',String(v===2));
    }
    for(const k of ['sleeve','boots_id','celebration','motion_profile'])$('editor-'+k).value=Object.hasOwn(p,k)?String(p[k]):'';
    $('editor-boots_color').value=p.boots_color||'#ffffff';
    $('editor-color-label').textContent=p.boots_color||'沿用模型颜色';
  }
  function attach(callbacks){
    api=callbacks;
    const position=document.createElement('details');position.id='diyPositionSection';position.className='diy-setting-card';
    position.innerHTML='<summary>星级、位置与适性</summary><label>球员星级<select id="editor-stars"><option value="">沿用模型星级</option><option value="1">1 星</option><option value="2">2 星</option><option value="3">3 星</option><option value="4">4 星</option></select></label><p class="hint">当前游戏的自定义球员使用 1–4 星；5 星会导致星级不显示。</p><label>主位置<select id="editor-position" disabled><option value="">沿用模型</option></select></label><p class="hint">点按球场位置切换适性。主位置保持完全熟练。</p><div id="editor-pitch" class="editor-pitch"></div>';
    $('diyProfileSection').after(position);
    $('editor-stars').onchange=()=>change(s=>{if($('editor-stars').value==='')delete s.stars;else s.stars=Number($('editor-stars').value);});
    const personal=document.createElement('details');personal.id='diyPersonalizationSection';personal.className='diy-setting-card';
    personal.innerHTML='<summary>个性化设置</summary><div class="card-fields">'+[['sleeve','袖长'],['boots_id','球鞋型号'],['celebration','纪念庆祝'],['motion_profile','固定动作组合']].map(([id,label])=>`<label>${label}<select id="editor-${id}" disabled><option value="">沿用模型</option></select></label>`).join('')+'</div><label>球鞋设计颜色<input id="editor-boots_color" type="color" value="#ffffff" disabled></label><div class="buttons"><span id="editor-color-label">沿用模型颜色</span><button id="editor-color-reset" type="button">恢复模型颜色</button></div><p class="hint">袖长、球鞋和设计颜色随作品保存。纪念庆祝复用编辑器已有配置；动作组合包含跑动等整组动作。位置、适性、庆祝与动作组合写入新球员；袖长、球鞋与设计颜色作为作品设置保存，当前不改游戏服装资源。</p><p id="editor-catalog-status" role="status">正在读取编辑器目录…</p>';
    // The basics group always places this after the model controls.
    $('cardPlayerPanel').append(personal);
    ready.then(c=>{
      for(const [i,label] of c.positions.entries())$('editor-position').add(new Option(label,String(i)));
      $('editor-position').disabled=false;
      for(const columns of [[[2],[0,1],[3]],[[7],[4,6,5],[8]],[[10],[9,12],[11]]]){
        const band=document.createElement('div');band.className='editor-pitch-band';
        for(const indices of columns){const col=document.createElement('div');for(const i of indices){const b=document.createElement('button');b.type='button';b.dataset.aptitude=i;b.onclick=()=>change(s=>{if(!s.aptitudes)return;s.aptitudes[i]=mainIndex[s.position]===i?2:(s.aptitudes[i]+1)%3;});col.append(b);}band.append(col);}$('editor-pitch').append(band);
      }
      for(const [k,rows] of [['sleeve',c.sleeves],['boots_id',c.boots],['celebration',c.celebrations],['motion_profile',c.motions]]){
        const e=$('editor-'+k);for(const row of rows)e.add(new Option(row.label,String(row.id)));e.disabled=false;
        e.onchange=()=>change(s=>{s.personalization={...s.personalization};if(e.value==='')delete s.personalization[k];else s.personalization[k]=['boots_id','celebration'].includes(k)?Number(e.value):e.value;});
      }
      $('editor-boots_color').disabled=false;$('editor-boots_color').onchange=()=>change(s=>{s.personalization={...s.personalization,boots_color:$('editor-boots_color').value};});
      $('editor-color-reset').onclick=()=>change(s=>{s.personalization={...s.personalization};delete s.personalization.boots_color;});
      $('editor-position').onchange=()=>change(s=>{const v=$('editor-position').value;if(v===''){delete s.position;delete s.aptitudes;}else{s.position=Number(v);s.aptitudes=s.aptitudes||Array(13).fill(0);s.aptitudes[mainIndex[s.position]]=2;}});
      $('editor-catalog-status').textContent=c.boots.length+' 种球鞋 · '+c.celebrations.length+' 项纪念庆祝 · '+c.motions.length+' 组动作';refresh();
    }).catch(e=>$('editor-catalog-status').textContent='目录读取失败：'+e.message+'；原设置保留');
  }
  window.DiyEditorFields={validate,refresh,attach,ready};
})();
