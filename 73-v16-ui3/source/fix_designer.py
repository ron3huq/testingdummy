from pathlib import Path
import re
p=Path('/workspace/ronaldo-work/73-ui3/apk-assets/assets/card-designer');f=p/'index.html';s=f.read_text()
s=s.replace("const tx=s=>String(s).replace(re,k=>words[k]);","const tx=s=>{s=String(s);return /[\\u3400-\\u9fff]/.test(s)?s.replace(re,k=>words[k]):s;};")
s=s.replace("editor.height=canvasHeight(player,scene);","if(editor.height!==canvasHeight(player,scene))editor.height=canvasHeight(player,scene);")
s=s.replace("$('detailPreview').height=canvasHeight(player,'detail');","if($('detailPreview').height!==canvasHeight(player,'detail'))$('detailPreview').height=canvasHeight(player,'detail');")
# Original synchronous renderer retained for export; UI repaint requests collapse into one frame.
s=s.replace('</html>', '''<script>
(()=>{const draw=render;let frame=0;window.__ui3Paints=0;render=function(){if(frame)return;frame=requestAnimationFrame(()=>{frame=0;if(document.hidden)return;window.__ui3Paints++;draw();});};document.addEventListener('visibilitychange',()=>{if(!document.hidden)render();});})();
</script>
</html>''').replace('UI2-E169','UI3-E169')
f.write_text(s)
f=p/'background-picker.js';s=f.read_text().replace('playing=true','playing=false')
# Videos already animate in composited DOM layers. Repainting three canvases and
# calibration overlays every video frame was unnecessary, even while editing.
a=s.index('  function animationFrame(');b=s.index('  function paint()',a);s=s[:a]+"  function tick(){} // Video elements animate independently; no full-editor repaint loop.\n"+s[b:]
s=s.replace("if(isVideo){if(playing&&!document.hidden)","if(isVideo){if(playing&&!document.hidden)")
f.write_text(s)
f=p/'card-suites.js';s=f.read_text().replace('id="videoToggle" aria-pressed="true">动态预览：开','id="videoToggle" aria-pressed="false">动态预览：关');s=s.replace("for(const id of ['suiteSeries','suiteSearch'])get(id).addEventListener(id==='suiteSeries'?'change':'input',()=>{page=0;list();});","let searchTimer=0;for(const id of ['suiteSeries','suiteSearch'])get(id).addEventListener(id==='suiteSeries'?'change':'input',()=>{clearTimeout(searchTimer);if(id==='suiteSeries'){page=0;list();}else searchTimer=setTimeout(()=>{page=0;list();},120);});")
f.write_text(s)
# Coalesce ResizeObserver/UI resize bursts and avoid identical layout writes.
f=p/'mobile-ui.js';s=f.read_text().replace('  function resizeCanvas(){if(!phone())return;requestAnimationFrame(()=>{','  let resizeFrame=0;function resizeCanvas(){if(!phone()||resizeFrame)return;resizeFrame=requestAnimationFrame(()=>{resizeFrame=0;');s=s.replace("wrap.style.width=Math.max(40,Math.min(box.clientWidth-16,(box.clientHeight-12)*r))+'px';","const width=Math.max(40,Math.min(box.clientWidth-16,(box.clientHeight-12)*r))+'px';if(wrap.style.width!==width)wrap.style.width=width;");f.write_text(s)
print('DESIGNER_PATCHED')
