/* Self-contained ZIP32 STORE bundles: PNGs are already compressed. No network library. */
(() => {
  'use strict';
  const MAX=40_000_000, MAX_FILES=4096, enc=new TextEncoder(), dec=new TextDecoder('utf-8',{fatal:true});
  const fail=s=>{throw Error('分享ZIP：'+s);};
  const table=Uint32Array.from({length:256},(_,n)=>{for(let i=0;i<8;i++)n=n&1?0xedb88320^(n>>>1):n>>>1;return n>>>0;});
  function crc(b){let n=0xffffffff;for(const v of b)n=table[(n^v)&255]^(n>>>8);return(n^0xffffffff)>>>0;}
  const hash=async b=>Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',b)),v=>v.toString(16).padStart(2,'0')).join('');
  function base64(b){let s='';for(let i=0;i<b.length;i+=24576)s+=String.fromCharCode(...b.subarray(i,i+24576));return btoa(s);}
  function bytes(s){const b=atob(s);return Uint8Array.from(b,c=>c.charCodeAt(0));}
  function filename(s){if(typeof s!=='string'||!(/^(project\.json|manifest\.json|images\/[a-f0-9]{64}\.png)$/).test(s))fail('含不支持的文件路径');return s;}
  function pack(files){
    if(files.size>MAX_FILES)fail('文件过多');
    const parts=[],central=[];let offset=0,size=0;
    for(const [name,b]of files){
      const n=enc.encode(filename(name)),c=crc(b),h=new Uint8Array(30+n.length),v=new DataView(h.buffer);
      v.setUint32(0,0x04034b50,true);v.setUint16(4,20,true);v.setUint16(6,0x800,true);v.setUint16(12,33,true);v.setUint32(14,c,true);v.setUint32(18,b.length,true);v.setUint32(22,b.length,true);v.setUint16(26,n.length,true);h.set(n,30);
      const d=new Uint8Array(46+n.length),w=new DataView(d.buffer);w.setUint32(0,0x02014b50,true);w.setUint16(4,20,true);w.setUint16(6,20,true);w.setUint16(8,0x800,true);w.setUint16(14,33,true);w.setUint32(16,c,true);w.setUint32(20,b.length,true);w.setUint32(24,b.length,true);w.setUint16(28,n.length,true);w.setUint32(42,offset,true);d.set(n,46);
      parts.push(h,b);central.push(d);offset+=h.length+b.length;size+=d.length;
    }
    const end=new Uint8Array(22),v=new DataView(end.buffer);v.setUint32(0,0x06054b50,true);v.setUint16(8,files.size,true);v.setUint16(10,files.size,true);v.setUint32(12,size,true);v.setUint32(16,offset,true);
    if(offset+size+22>MAX)fail('文件超过40MB，请减少所选作品');
    const out=new Uint8Array(offset+size+22);let at=0;for(const b of [...parts,...central,end]){out.set(b,at);at+=b.length;}return out;
  }
  function unpack(b){
    if(!(b instanceof Uint8Array)||b.length<22||b.length>MAX)fail('容量或格式错误');
    const v=new DataView(b.buffer,b.byteOffset,b.byteLength),end=b.length-22;
    if(v.getUint32(end,true)!==0x06054b50||v.getUint16(end+4,true)||v.getUint16(end+6,true)||v.getUint16(end+20,true))fail('仅支持本应用导出的单卷ZIP');
    const count=v.getUint16(end+10,true),cd=v.getUint32(end+16,true),cdSize=v.getUint32(end+12,true);
    if(!count||count>MAX_FILES||count!==v.getUint16(end+8,true)||cd+cdSize!==end)fail('目录错误');
    const files=new Map();let at=cd,local=0,total=0;
    for(let i=0;i<count;i++){
      if(at+46>end||v.getUint32(at,true)!==0x02014b50)fail('目录已损坏');
      const flags=v.getUint16(at+8,true),method=v.getUint16(at+10,true),c=v.getUint32(at+16,true),size=v.getUint32(at+20,true),raw=v.getUint32(at+24,true),nl=v.getUint16(at+28,true),extra=v.getUint16(at+30,true),comment=v.getUint16(at+32,true),off=v.getUint32(at+42,true);
      if(flags!==0x800||method!==0||size!==raw)fail('仅支持本应用的无加密STORE格式，请从原应用重新导出');
      if(v.getUint16(at+34,true)||at+46+nl+extra+comment>end||off!==local||off+30>cd)fail('文件边界错误');
      const name=filename(dec.decode(b.subarray(at+46,at+46+nl)));
      if(files.has(name)||v.getUint32(off,true)!==0x04034b50||v.getUint16(off+6,true)!==flags||v.getUint16(off+8,true)!==method||v.getUint32(off+14,true)!==c||v.getUint32(off+18,true)!==size||v.getUint32(off+22,true)!==raw||v.getUint16(off+26,true)!==nl||v.getUint16(off+28,true)!==0)fail('重复文件或头部不一致');
      const start=off+30+nl,stop=start+size;
      if(stop>cd||dec.decode(b.subarray(off+30,start))!==name||(total+=raw)>MAX)fail('文件越界或展开超过40MB');
      const data=b.subarray(start,stop);if(crc(data)!==c)fail('文件CRC校验失败：'+name);
      files.set(name,data);local=stop;at+=46+nl+extra+comment;
    }
    if(at!==end||local!==cd)fail('目录与内容不一致');return files;
  }
  async function walk(v,fn){
    if(typeof v==='string')return fn(v);
    if(Array.isArray(v)){const out=[];for(const x of v)out.push(await walk(x,fn));return out;}
    if(v&&typeof v==='object'){const out=Object.create(null);for(const [k,x]of Object.entries(v)){if(['__proto__','constructor','prototype'].includes(k))fail('不支持的配置字段');out[k]=await walk(x,fn);}return out;}
    return v;
  }
  async function encode(project){
    const files=new Map(),cache=new Map();let size=0;
    const compact=await walk(project,async s=>{
      if(s.startsWith('diyzip:'))fail('工程含未解析素材');
      if(!s.startsWith('data:image/'))return s;
      if(cache.has(s))return cache.get(s);
      if(!/^data:image\/png;base64,[A-Za-z0-9+/]*={0,2}$/.test(s))fail('图片尚未转换成PNG');
      const b=bytes(s.slice(s.indexOf(',')+1)),id='images/'+await hash(b)+'.png',ref='diyzip:'+id;
      if(!files.has(id)){size+=b.length;if(size>MAX||files.size>=MAX_FILES-2)fail('素材容量或数量超限');files.set(id,b);}
      cache.set(s,ref);return ref;
    });
    const json=enc.encode(JSON.stringify(compact));files.set('project.json',json);
    const manifest={schema:'diy-test-zip/v1',projectSchema:project.schema,files:{}};
    for(const [name,b]of files)manifest.files[name]={bytes:b.length,sha256:await hash(b)};
    files.set('manifest.json',enc.encode(JSON.stringify(manifest)));
    return pack(files);
  }
  async function decode(raw){
    const files=unpack(raw);
    if(!files.has('manifest.json')||!files.has('project.json'))fail('缺少清单或工程');
    const manifest=JSON.parse(dec.decode(files.get('manifest.json')));
    if(manifest.schema!=='diy-test-zip/v1'||!manifest.files||Object.keys(manifest.files).length!==files.size-1)fail('清单格式不匹配');
    for(const [name,info]of Object.entries(manifest.files)){
      filename(name);const b=files.get(name);
      if(!b||name==='manifest.json'||info.bytes!==b.length||info.sha256!==await hash(b))fail('素材摘要不匹配：'+name);
    }
    const used=new Set(['project.json','manifest.json']),cache=new Map();let expanded=files.get('project.json').length;
    const project=await walk(JSON.parse(dec.decode(files.get('project.json'))),async s=>{
      if(s.startsWith('data:image/'))fail('ZIP内含非标准内嵌图片');
      if(!s.startsWith('diyzip:'))return s;
      const path=filename(s.slice(7));if(!path.startsWith('images/')||!files.has(path))fail('缺少引用图片');
      const b=files.get(path);if(b.length<8||[137,80,78,71,13,10,26,10].some((v,i)=>b[i]!==v))fail('图片格式错误');
      used.add(path);expanded+=4*Math.ceil(b.length/3)+22-s.length;if(expanded>MAX)fail('还原工程超过40MB，请减少作品后重新导出');
      if(!cache.has(path))cache.set(path,'data:image/png;base64,'+base64(b));return cache.get(path);
    });
    if(used.size!==files.size||manifest.projectSchema!==project.schema||project.diyTestExchange?.schema!=='diy-test-works/v1')fail('存在未引用文件或工程类型错误');
    if(enc.encode(JSON.stringify(project)).length>MAX)fail('还原工程超过40MB');
    return project;
  }
  function downloadZip(b,name){
    if(window.AndroidCardDesigner){
      if(typeof AndroidCardDesigner.downloadZip!=='function')fail('当前Android宿主不支持ZIP，请更新测试应用');
      AndroidCardDesigner.downloadZip(base64(b),name);return;
    }
    download(b,name,'application/zip');
  }
  window.WorkArchive={encode,decode,downloadZip};
})();
