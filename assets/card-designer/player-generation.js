/* Candidate preparation and game acceptance are separate, recoverable stages. */
(() => {
  'use strict';
  const host=document.getElementById('cardPlayerPanel');if(!host)return;
  const section=document.createElement('section');section.id='diyGeneration';
  section.innerHTML='<h3>生成独立球员</h3><ol id="diyGenerationSteps"><li>校验作品</li><li>确认候选</li><li>准备资源</li><li>加载与到账</li></ol><button id="diyGeneratePreview" class="primary" disabled>检查资源并预览</button><button id="diyGenerationRefresh">刷新生成记录</button><p id="diyGenerationStatus" class="status" role="status" aria-live="polite">正在检查生成后端…</p><details id="diyGenerationRecords"><summary>本机生成记录</summary><div id="diyGenerationHistory"></div></details>';
  host.prepend(section);
  const meter=document.createElement('div');meter.id='diyProgress';meter.hidden=true;meter.innerHTML='<progress id="diyGenerationProgress" max="100" aria-label="当前操作进度"></progress><p id="diyProgressLabel" role="status" aria-live="polite"></p>';section.querySelector('#diyGenerationStatus').before(meter);
  let lastPercent=0;
  function failProgress(message){progress(lastPercent,'已停止 · '+message);}
  function progress(value,label){if(value!=null)lastPercent=value;meter.hidden=false;const bar=document.getElementById('diyGenerationProgress');if(value==null)bar.removeAttribute('value');else bar.value=Math.max(0,Math.min(100,value));document.getElementById('diyProgressLabel').textContent=(value==null?'处理中 · ':Math.floor(value)+'% · ')+label;}
  const newWorkButton=document.createElement('button');newWorkButton.id='diyNewWork';newWorkButton.textContent='另存为新作品';section.querySelector('#diyGenerationRefresh').after(newWorkButton);
  const get=id=>document.getElementById(id);
  const shortcut=document.createElement('button');shortcut.id='diyImportShortcut';shortcut.type='button';shortcut.textContent='导入 / 状态';shortcut.setAttribute('aria-controls','diyGeneration');
  const actionHost=document.querySelector('header .toolbar')||document.querySelector('header');actionHost.classList.add('diy-actions-present');actionHost.append(shortcut);
  const status=s=>{get('diyGenerationStatus').textContent=s;shortcut.title=s;shortcut.setAttribute('aria-label','导入与发卡状态：'+s);};
  shortcut.onclick=()=>{if(window.cardChooseTool)window.cardChooseTool('player');const collapse=get('phoneCanvasToggle');if(collapse&&!document.querySelector('main').classList.contains('canvas-collapsed'))collapse.click();section.scrollIntoView({block:'start'});get('diyGenerationStatus').focus({preventScroll:true});};
  get('diyGenerationStatus').tabIndex=-1;
  const dialog=document.createElement('dialog');dialog.className='card-package-dialog';dialog.id='diyGenerationConfirm';
  dialog.innerHTML='<h2>确认生成球员</h2><p id="diyGenerationSummary"></p><p class="hint">确认后生成独立卡号并准备资源。准备成功后完全退出，再进入游戏校验；发卡入库与名单同步分别显示，请按记录中的下一步操作。</p><div class="buttons"><button id="diyGenerationCommit" class="primary">生成并准备导入</button><button id="diyGenerationCancel">取消</button></div>';
  document.body.append(dialog);
  const fork=document.createElement('dialog');fork.id='diyNewWorkDialog';fork.className='card-package-dialog';fork.innerHTML='<h2>另存为新作品</h2><p>保留当前卡面、姓名能力和模型，分配新的作品标识。旧候选和已拥有的卡不变；确认后仍需检查预览、生成并准备资源。</p><div class="buttons"><button id="diyNewWorkConfirm" class="primary">另存新作品</button><button id="diyNewWorkCancel">取消</button></div>';document.body.append(fork);
  let pending=null,busy=false,resourceMode=false,autoDelivery=false,enabled=false;
  const checkedFailures=new Set();
  const trash=document.createElement('details');trash.id='diyWorkTrash';trash.innerHTML='<summary>作品回收站</summary><p class="hint">可恢复删除：保留已入游戏的球员、素材和资源文件，不释放卡号，也不回收文件容量。</p><div id="diyWorkTrashList"></div>';section.append(trash);
  const remove=document.createElement('dialog');remove.id='diyWorkDeleteDialog';remove.className='card-package-dialog';remove.innerHTML='<h2>删除旧作品</h2><p id="diyWorkDeleteSummary"></p><p>作品移入回收站，可随时恢复。已入游戏的球员不会删除；使用中的卡面、模型和启动选择保留。此操作不回收资源文件容量。</p><div class="buttons"><button id="diyWorkDeleteConfirm">移入回收站</button><button id="diyWorkDeleteCancel">取消</button></div>';document.body.append(remove);
  let deleting=null;
  get('diyWorkDeleteCancel').onclick=()=>{if(!busy){deleting=null;remove.close();}};
  remove.addEventListener('cancel',e=>{if(busy)e.preventDefault();else deleting=null;});
  async function changeVisibility(c,deleted){
    lock(true);
    try{const result=await request(deleted?'/api/generation/delete':'/api/generation/restore',{uuid:c.uuid});await history(false);status(result.message||(deleted?'作品已移入回收站':'作品已恢复'));if(deleted)trash.open=true;}
    catch(e){try{await history(false);}catch(_ignored){}status('作品管理未确认完成：'+e.message+'。请刷新记录核对，重试不会重复发卡。');}
    finally{deleting=null;remove.close();lock(false);}
  }
  get('diyWorkDeleteConfirm').onclick=()=>{if(!busy&&deleting)return changeVisibility(deleting,true);};
  async function checkDelivery(c){
    stage(3,'正在核对 '+c.name+' 的发卡状态；等待加载与资源错误会分别显示…');
    progress(null,'核对候选、资源与到账回执');
    const result=await request('/api/generation/check',{uuid:c.uuid,repair:true});
    status(result.message||'状态校验完成');
    progress(result.status==='OWNED'&&result.phase==='ROSTER_SENT'?100:null,result.message||result.status);
    get('diyGenerationRecords').open=true;
    return result;
  }
  function stage(n,message){section.dataset.stage=String(n);for(const [i,li] of Array.from(get('diyGenerationSteps').children).entries())li.setAttribute('aria-current',i+1===n?'step':'false');status(message);if(busy)progress(null,n===4?'资源准备完成；等待游戏加载和名单同步':message);}
  const fingerprint=()=>JSON.stringify({who:player,project:state.players[player],backgrounds:state.backgroundLibrary||[]});
  function lock(value){busy=value;get('diyGeneratePreview').disabled=value||!enabled;get('diyGenerationRefresh').disabled=value;newWorkButton.disabled=value;get('diyNewWorkConfirm').disabled=value;get('diyNewWorkCancel').disabled=value;get('diyGenerationCommit').disabled=value;get('diyGenerationCancel').disabled=value;get('diyWorkDeleteConfirm').disabled=value;get('diyWorkDeleteCancel').disabled=value;section.setAttribute('aria-busy',String(value));if(!value&&!get('diyGenerationProgress').hasAttribute('value')){meter.hidden=true;get('diyProgressLabel').textContent='';}}
  newWorkButton.onclick=()=>{if(!busy)fork.showModal();};get('diyNewWorkCancel').onclick=()=>fork.close();fork.addEventListener('cancel',e=>{if(busy)e.preventDefault();});
  get('diyNewWorkConfirm').onclick=async()=>{if(busy)return;lock(true);pending=null;try{await CardPackage.newWork();fork.close();stage(1,'已另存为新作品，旧候选保留。现在检查资源并预览，再确认生成。');}catch(e){fork.close();stage(1,e.message);}finally{lock(false);}};
  async function build(){
    const who=player,before=revision,hadMetadata=!!state.players[who].diy;
    if(!state.players[who].cardSuite)throw Error('请先到背景页选择一套完整卡面套装');
    const p=await CardPackage.prepare({onProgress:message=>stage(1,message)}),expected=before+(hadMetadata?0:1);
    if(player!==who||revision!==expected)throw Error('作品在整理时发生变化，请重新预览');
    const portraits={};
    for(const kind of ['small','detail']){
      stage(1,'绘制'+(kind==='small'?'小框':'详情')+'人物卡面…');
      for(const l of state.players[who][kind])if(l.visible)await readyImage(l.asset);
      portraits[kind]=resource(who,kind).toDataURL('image/png');
    }
    if(player!==who||revision!==expected)throw Error('作品在整理时发生变化，请重新预览');
    return {request:{package:p,portraits},who,revision:expected,fingerprint:fingerprint()};
  }
  async function history(autoCheck=true){
    const result=await request('/api/generation');const list=get('diyGenerationHistory'),trashList=get('diyWorkTrashList');list.replaceChildren();trashList.replaceChildren();
    const seen=new Set();
    for(const c of result.candidates||[]){
      if(seen.has(c.uuid))continue;seen.add(c.uuid);
      if(c.trashed){
        const line=document.createElement('p');line.textContent=c.name+' · '+c.cardId+' · 已移入回收站';trashList.append(line);
        const restore=document.createElement('button');restore.textContent='恢复作品';restore.onclick=()=>{if(!busy)return changeVisibility(c,false);};trashList.append(restore);continue;
      }
      const delivery=c.delivery?.status;
      const phase=c.delivery?.phase;
      const label=c.readOnly?c.recoveryReason:delivery==='OWNED'?(phase==='ROSTER_SENT'?'已入库，名单已发送；请在游戏球员列表查看':'已入库，等待名单同步；到签约页第二个「DIY 待领取」卡池同步领取，不会新增副本'):delivery==='READY_TO_CLAIM'?'资源已加载；到游戏签约页第二个「DIY 待领取」卡池免费领取':delivery==='RELEASED'?'已解约，不会重复发放':delivery==='PENDING'?(phase==='BLOCKED'?'校验已阻断，保留作品并查看原因：':phase==='WAITING_SAVE'?'等待当前存档操作完成：':'等待游戏加载，发卡会自动重试：')+(c.delivery.reason||'等待启动校验'):c.startupQueued===true?'资源已排队；完全退出后进入游戏加载，尚未发卡':c.integration?.verified===false?'已有接入记录，未核验；使用前会完整校验':c.integration?(autoDelivery?'资源已准备，尚未确认排队；请校验状态':'资源已准备；当前后端未启用自动发卡'):'候选已保存，待准备资源';
      const line=document.createElement('p');line.className='hint';line.textContent=c.name+' · '+c.cardId+' · '+label;list.append(line);
      const del=document.createElement('button');del.textContent='删除作品';del.dataset.workUuid=c.uuid;del.onclick=()=>{if(busy)return;deleting=c;get('diyWorkDeleteSummary').textContent='将 '+c.name+' · '+c.cardId+' 移入回收站？';remove.showModal();};list.append(del);
      if(resourceMode&&!c.readOnly&&!['RELEASED','OWNED'].includes(delivery)){
        if(autoDelivery){
        const check=document.createElement('button');check.textContent='校验并修复发卡';
        check.onclick=async()=>{if(busy)return;lock(true);try{await checkDelivery(c);await history(false);}catch(e){status('校验停止，作品保留：'+e.message);failProgress('尚未发卡');}finally{lock(false);}};list.append(check);
        }
        const button=document.createElement('button');button.textContent=c.integration?'重新准备这张卡的资源':'准备这张卡的资源';
        button.onclick=async()=>{if(busy)return;lock(true);button.disabled=true;try{await resources(c);await history();}catch(e){stage(3,'候选 '+c.cardId+' 已保留。'+e.message+'；请确认记录状态后再操作。');failProgress('资源准备失败，候选已保留；可从记录重试');try{await history();}catch(refreshError){status(get('diyGenerationStatus').textContent+'；记录读取失败：'+refreshError.message);}}finally{lock(false);button.disabled=false;}};list.append(button);
      }
    }
    if(!list.children.length)list.textContent='尚无已登记的候选球员';
    if(!trashList.children.length)trashList.textContent='回收站为空';
    const outstanding=(result.candidates||[]).filter(c=>!c.trashed&&c.delivery?.status!=='RELEASED'&&(c.delivery?.status!=='OWNED'||c.delivery?.phase!=='ROSTER_SENT'));
    shortcut.dataset.pending=String(outstanding.length>0);shortcut.textContent=outstanding.length?'导入 / 状态 · '+outstanding.length:'导入 / 状态';
    if(outstanding.length)get('diyGenerationRecords').open=true;
    const failed=(result.candidates||[]).find(c=>!c.trashed&&!c.readOnly&&c.startupQueued&&c.delivery?.status==='PENDING');
    if(autoCheck&&autoDelivery&&failed&&!busy){
      const key=failed.uuid+':'+(failed.integration?.manifestHash||'');
      if(!checkedFailures.has(key)){checkedFailures.add(key);lock(true);try{await checkDelivery(failed);await history(false);}catch(e){status('自动校验停止，作品保留：'+e.message);failProgress('尚未发卡');}finally{lock(false);}}
    }
    return result;
  }
  async function resources(c){
    stage(3,'正在准备 '+c.name+' 的游戏资源，请保持编辑器打开…');
    progress(0,'提交资源准备任务');
    const started=Date.now()/1000;let active=true,polling=false;
    const poll=async()=>{if(!active||polling)return;polling=true;try{const p=await request('/api/generation/progress?uuid='+encodeURIComponent(c.uuid));if(active&&p.uuid===c.uuid&&p.updatedAt>=started&&Number.isFinite(p.percent)){const bytes=p.total>0&&p.stage==='复制游戏图片容器'?` · ${(p.done/1048576).toFixed(1)} / ${(p.total/1048576).toFixed(1)} MB`:'';progress(p.percent,p.stage+bytes);}}catch(e){/* Progress failure never resubmits or cancels resource writes. */}finally{polling=false;}};
    const timer=setInterval(poll,500);let receipt;
    try{receipt=await request('/api/generation/resources',{uuid:c.uuid});}
    finally{active=false;clearInterval(timer);}
    progress(100,'资源准备已返回，正在核对排队回执；不代表已发卡');
    if(!autoDelivery){stage(3,'资源已准备；当前后端未启用自动发卡，尚未加入球员列表。');return;}
    if(receipt.startupQueued!==true||receipt.restartRequired!==true||receipt.gameReady!==false)throw Error('未收到完整的启动排队回执；尚未确认自动发卡，请在记录中重新准备这张卡的资源');
    stage(4,'资源已排队 '+c.name+' · 卡号 '+c.cardId+'，尚未发卡。下一步：完全退出后进入游戏，资源加载后到签约页第二个「DIY 待领取」卡池免费领取；领取回复会带上新卡。');
  }
  get('diyGenerationRefresh').onclick=async()=>{if(busy)return;lock(true);try{await history();get('diyGenerationRecords').open=true;status('记录已刷新。请以每张卡的实际导入状态为准。');}catch(e){status('生成记录读取失败：'+e.message);}finally{lock(false);}};
  get('diyGeneratePreview').onclick=async()=>{
    if(busy)return;lock(true);pending=null;
    try{stage(1,'正在校验作品…');const b=await build();stage(1,'图片就绪，正在校验原生模型与候选…');const v=await request('/api/generation/preview',b.request,{timeout:60000});
      if(player!==b.who||revision!==b.revision||fingerprint()!==b.fingerprint)throw Error('作品已变化，请重新预览');
      pending={...b,token:v.token};get('diyGenerationSummary').textContent=v.name+' · 等级 '+v.level+'/'+v.maxLevel+' · '+v.suite+' · 模型 '+v.model+(Array.isArray(v.boosterLabels)?' · 增能 '+v.boosterLabels.join(' / '):'')+(v.existing?' · 已有相同作品，将复用原卡号':'');dialog.showModal();stage(2,'校验通过，等待确认；尚未新增候选。');
    }catch(e){stage(1,'校验未完成：'+e.message+'。修复后可重新检查。');}finally{lock(false);}
  };
  function cancel(){if(busy)return;pending=null;dialog.close();stage(1,'已取消，未新增候选球员');}
  get('diyGenerationCancel').onclick=cancel;dialog.addEventListener('cancel',e=>{if(busy)e.preventDefault();else{pending=null;stage(1,'已取消，未新增候选球员');}});
  get('diyGenerationCommit').onclick=async()=>{
    if(!pending||busy)return;lock(true);const current=pending;let result=null;
    try{
      if(player!==current.who||revision!==current.revision||fingerprint()!==current.fingerprint)throw Error('作品已变化，请重新预览');
      stage(2,'正在保存独立候选，请勿重复提交…');
      // The immutable preview stays bound to its token; the native backend revalidates it.
      result=await request('/api/generation/prepare',{request:current.request,token:current.token});pending=null;dialog.close();
      if(resourceMode)await resources(result);else stage(3,(result.reused?'已复用':'已生成')+'候选 '+result.name+' · 卡号 '+result.cardId+'。待资源挂载与游戏验收，尚未发入游戏。');
    }catch(e){pending=null;dialog.close();stage(result?3:2,result?'候选 '+result.name+' · '+result.cardId+' 已保存，资源准备未完成：'+e.message+'。可在生成记录中继续，无需重新生成。':e.message);get('diyGenerationRecords').open=true;failProgress('本次操作未完成，请查看下方原因；尚未发卡');}
    finally{try{await history();}catch(e){status(get('diyGenerationStatus').textContent+'；记录暂未刷新：'+e.message);}lock(false);}
  };
  async function init(){try{const info=await request('/api/info');if(!info.generation?.enabled){status(info.generation?.reason||'本机生成后端尚未配置；作品可保存/分享。');return;}autoDelivery=info.generation.mode==='auto-delivery';resourceMode=['resources-only','auto-delivery'].includes(info.generation.mode);enabled=true;lock(false);stage(1,autoDelivery?'选择套装并检查作品 → 确认生成 → 自动准备资源 → 重启游戏验收':'当前仅支持候选/资源准备，尚不能确认游戏内自动发卡');await history();}catch(e){status('生成后端检查失败：'+e.message);}}
  window.CardGeneration={build,history};init();
  let lastVisibleRefresh=0;document.addEventListener('visibilitychange',()=>{if(!document.hidden&&enabled&&!busy&&Date.now()-lastVisibleRefresh>2000){lastVisibleRefresh=Date.now();lock(true);history(false).catch(e=>status('记录暂未刷新，作品保留：'+e.message)).finally(()=>lock(false));}});
})();
