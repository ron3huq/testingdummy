/* Async transport keeps rendering responsive; aborting a wait never cancels native writes. */
(() => {
  if(!window.AndroidCardDesigner)return;
  const original=window.fetch.bind(window),pending=new Map();let sequence=0;
  window.CardDesignerTransport={deliver(id,result){pending.get(id)?.resolve(result);}};
  function nativeRequest(method,path,body,signal){
    if(typeof AndroidCardDesigner.requestAsync!=='function'){
      // Compatibility for old installed hosts. Full responsiveness requires the new host.
      return Promise.resolve().then(()=>AndroidCardDesigner.request(method,path,body));
    }
    return new Promise((resolve,reject)=>{
      const id=String(++sequence);let timer;
      const cleanup=()=>{clearTimeout(timer);pending.delete(id);signal?.removeEventListener('abort',abort);};
      const abort=()=>{cleanup();reject(Error('等待已中止；原生操作可能仍在执行，请刷新记录确认结果'));};
      pending.set(id,{resolve(result){cleanup();resolve(result);}});
      signal?.addEventListener('abort',abort,{once:true});
      if(signal?.aborted){abort();return;}
      timer=setTimeout(()=>{cleanup();reject(Error('原生处理超时，请刷新记录确认结果，勿重复提交'));},190000);
      try{AndroidCardDesigner.requestAsync(id,method,path,body);}catch(e){cleanup();reject(e);}
    });
  }
  window.fetch=async(input,options={})=>{
    const url=new URL(typeof input==='string'?input:input.url,location.href);
    if(url.origin!==location.origin||!url.pathname.startsWith('/api/'))return original(input,options);
    // Progress is a tiny read-only receipt, never queued behind resource work.
    if(url.pathname==='/api/generation/progress'&&typeof AndroidCardDesigner.generationProgress==='function')return new Response(AndroidCardDesigner.generationProgress(url.searchParams.get('uuid')||''),{status:200,headers:{'Content-Type':'application/json'}});
    const result=await nativeRequest(options.method||'GET',url.pathname,options.body||'',options.signal),value=JSON.parse(result);
    return new Response(result,{status:value.error?400:200,headers:{'Content-Type':'application/json'}});
  };
  window.addEventListener('DOMContentLoaded',()=>{download=(data,name,type)=>AndroidCardDesigner.download(data,name,type);});
  document.addEventListener('visibilitychange',()=>{
    if(document.hidden&&typeof state!=='undefined'&&state)request('/api/save',state).catch(e=>inform(e.message,true));
  });
})();
