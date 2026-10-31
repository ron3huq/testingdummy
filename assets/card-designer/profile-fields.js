/* Optional fields are preserved in projects/shares and checked by all hosts. */
(() => {
 'use strict';
 let catalog=null,api=null;
 const fields=['nationality','club','foot','weakAccuracy','weakUsage','skills'];
 function validate(p,{previous}={}){
  if(!p||typeof p!=='object'||Array.isArray(p)||Object.keys(p).some(k=>!fields.includes(k)))throw Error('球员资料字段错误');
  for(const [k,min,max]of [['nationality',1,511],['club',0,2147483647],['foot',0,1],['weakAccuracy',1,3],['weakUsage',1,3]])if(Object.hasOwn(p,k)&&(!Number.isInteger(p[k])||p[k]<min||(p[k]>max&&!(max===3&&p[k]===4&&previous?.[k]===4))))throw Error('球员资料选项错误：'+k);
  if(Object.hasOwn(p,'skills')&&(!Array.isArray(p.skills)||new Set(p.skills).size!==p.skills.length||p.skills.some(i=>!Number.isInteger(i))))throw Error('技能选择错误');
  if(catalog){for(const [k,rows]of [['nationality',catalog.countries],['club',catalog.clubs]])if(Object.hasOwn(p,k)&&!rows.some(r=>r.id===p[k]))throw Error('未登记的球员资料：'+k);if(p.skills?.some(i=>!catalog.skills.some(r=>r.id===i)))throw Error('未验证技能不可选');}
  return JSON.parse(JSON.stringify(p));
 }
 const get=id=>document.getElementById(id);
 function refresh(){if(!api||!catalog||typeof state==='undefined'||!state)return;const p=api.metadata().profile||{};
  for(const k of fields.filter(k=>k!=='skills')){const e=get('profile-'+k);if(e){e.querySelector('[data-legacy]')?.remove();if(['weakAccuracy','weakUsage'].includes(k)&&p[k]===4){const old=new Option('旧版4档（请选择1–3）','4');old.disabled=true;old.dataset.legacy='true';e.add(old);}e.value=Object.hasOwn(p,k)?String(p[k]):'';}}
  const selected=new Set(p.skills||[]),q=(get('profile-skillQuery')?.value||'').trim().toLocaleLowerCase();
  get('profile-skills').replaceChildren();
  for(const s of catalog.skills){if(q&&!(s.label+' '+s.english+' '+s.id).toLocaleLowerCase().includes(q))continue;const label=document.createElement('label'),input=document.createElement('input');input.type='checkbox';input.value=s.id;input.checked=selected.has(s.id);input.onchange=()=>api.edit(d=>{d.profile={...d.profile};const ids=new Set(d.profile.skills||[]);input.checked?ids.add(s.id):ids.delete(s.id);d.profile.skills=[...ids].sort((a,b)=>a-b);});label.append(input,document.createTextNode(s.label));get('profile-skills').append(label);}
  get('profile-skillCount').textContent=Object.hasOwn(p,'skills')?`${selected.size} 项已选`:'沿用模型自带技能';
 }
 function attach(callbacks){api=callbacks;const box=document.createElement('details');box.className='diy-setting-card';box.id='diyProfileSection';box.innerHTML='<summary>国籍、俱乐部与左右脚</summary><p class="hint">不设置时沿用所选模型的资料。逆足精度与频率各 1–3 档；4/4 会在游戏中被误读为 1/1，不改变惯用脚。</p><input id="profile-affiliationQuery" type="search" placeholder="筛选国籍 / 俱乐部英文名或编号"><div class="card-fields">'+[['nationality','国籍'],['club','俱乐部'],['foot','惯用脚'],['weakAccuracy','逆足精度'],['weakUsage','逆足使用频率']].map(([k,v])=>`<label>${v}<select id="profile-${k}" disabled><option value="">沿用模型</option></select></label>`).join('')+'</div><p id="profile-loadStatus" role="status">正在读取资料目录…</p>';
  get('diyAbilitySection').before(box);
  const skills=document.createElement('details');skills.className='diy-setting-card';skills.id='diySkillSection';skills.innerHTML='<summary>自带技能 <span id="profile-skillCount">沿用模型</span></summary><input id="profile-skillQuery" type="search" placeholder="技能名称 / English / 编号"><div class="buttons"><button id="profile-skillClear" type="button">清空可编辑技能</button><button id="profile-skillInherit" type="button">恢复沿用模型</button></div><p class="hint">默认沿用所选模型自带技能。自选前请对照原卡；只选择能确认的技能，无法确认时保持“沿用模型”，避免生成空技能。仅映射已核对技能，目录外模型技能保留。</p><div id="profile-skills" class="profile-skill-grid"></div>';box.after(skills);
  for(const k of fields.filter(k=>k!=='skills'))get('profile-'+k).onchange=()=>api.edit(d=>{d.profile={...d.profile};const v=get('profile-'+k).value;if(v==='')delete d.profile[k];else d.profile[k]=Number(v);});
  get('profile-skillQuery').oninput=refresh;
  get('profile-skillClear').onclick=()=>api.edit(d=>{d.profile={...d.profile,skills:[]};});
  get('profile-skillInherit').onclick=()=>api.edit(d=>{d.profile={...d.profile};delete d.profile.skills;});
  function choices(){if(!catalog)return;const q=get('profile-affiliationQuery').value.toLocaleLowerCase().trim(),p=(typeof state!=='undefined'&&state?api.metadata().profile:null)||{};for(const [k,rows]of [['nationality',catalog.countries],['club',catalog.clubs],['foot',[{id:0,label:'右脚 Right'},{id:1,label:'左脚 Left'}]],['weakAccuracy',[1,2,3].map(id=>({id,label:String(id)}))],['weakUsage',[1,2,3].map(id=>({id,label:String(id)}))]]){const e=get('profile-'+k);e.replaceChildren(new Option('沿用模型',''));for(const r of rows)if(!['nationality','club'].includes(k)||!q||(r.label+' '+r.id).toLocaleLowerCase().includes(q)||p[k]===r.id)e.add(new Option(['weakAccuracy','weakUsage','foot'].includes(k)?r.label:r.label+' · '+r.id,String(r.id)));e.disabled=false;}refresh();}
  get('profile-affiliationQuery').oninput=choices;
  request('/profile-catalog.json').then(c=>{if(c.schema!=='efootball-diy-profile/v1'||!Array.isArray(c.skills))throw Error('目录格式错误');catalog=c;choices();get('profile-loadStatus').textContent=`${c.countries.length} 个国籍 · ${c.clubs.length} 个俱乐部选项 · ${c.skills.length} 项可编辑自带技能`;}).catch(e=>get('profile-loadStatus').textContent='目录读取失败：'+e.message+'；已有作品设置仍保留');
 }
 window.CardProfile={validate,refresh,attach};
})();
