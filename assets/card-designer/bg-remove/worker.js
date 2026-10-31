'use strict';
let session=null;
async function ready(){
 if(session)return session;
 self.postMessage({phase:'Loading offline background model…'});
 importScripts('ort.min.js');
 ort.env.wasm.numThreads=1;
 ort.env.wasm.wasmPaths=new URL('./',self.location.href).href;
 session=await ort.InferenceSession.create(new URL('u2netp.onnx',self.location.href).href,{executionProviders:['wasm'],graphOptimizationLevel:'all'});
 return session;
}
self.onmessage=async({data})=>{
 try{
  const s=await ready(),rgba=new Uint8ClampedArray(data.rgba),size=320*320,input=new Float32Array(size*3);
  let max=1;for(let i=0;i<rgba.length;i+=4)max=Math.max(max,rgba[i],rgba[i+1],rgba[i+2]);
  const mean=[.485,.456,.406],std=[.229,.224,.225];
  for(let i=0;i<size;i++)for(let c=0;c<3;c++)input[c*size+i]=(rgba[i*4+c]/max-mean[c])/std[c];
  self.postMessage({phase:'Removing background offline…'});
  const result=await s.run({[s.inputNames[0]]:new ort.Tensor('float32',input,[1,3,320,320])}),prediction=result[s.outputNames[0]].data;
  let lo=Infinity,hi=-Infinity;for(let i=0;i<size;i++){lo=Math.min(lo,prediction[i]);hi=Math.max(hi,prediction[i]);}
  if(!Number.isFinite(lo+hi)||hi-lo<1e-6)throw Error('Could not separate the subject. Keep the original or try another photo.');
  const mask=new Uint8ClampedArray(size);let kept=0;
  for(let i=0;i<size;i++){let alpha=Math.max(0,Math.min(1,((prediction[i]-lo)/(hi-lo)-.04)/.92));mask[i]=Math.round(alpha*255);if(alpha>.5)kept++;}
  if(kept<size*.002||kept>size*.998)throw Error('No clear foreground found. The original photo was kept.');
  for(const value of Object.values(result))if(value.dispose)value.dispose();
  self.postMessage({mask:mask.buffer},[mask.buffer]);
 }catch(e){self.postMessage({error:String(e.message||e)});}
};
