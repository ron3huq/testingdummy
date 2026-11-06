"""Stage launcher + new single DEX operation from an exact RC7 input.
Never overwrite the existing payload/inventory or advertise unfinished UCL.
"""
from pathlib import Path
import sys,hashlib,subprocess,json,shutil
RC7_DEX='687f574b70c37888c274bd8d9b1cf193dc3eff33d4556eb8db34d8b124a53c51'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def build(root,stage):
    root=Path(root).resolve();stage=Path(stage).resolve();source=Path(__file__).resolve().parent
    if stage.exists():raise ValueError('Use a fresh stage directory')
    assert sha(root/'classes5.dex')==RC7_DEX,'Expected untouched RC7 DEX'
    stage.mkdir(parents=True);smali=stage/'smali';jar=root/'.ci-full8-rc5/apktool.jar';tool=root/'source/repair-full8-rc4/DexTool.java'
    def run(*args):subprocess.run([str(v)for v in args],check=True,stdout=subprocess.DEVNULL)
    run('java','-cp',jar,tool,'d',root/'classes5.dex',smali)
    before={p.relative_to(smali).as_posix():sha(p)for p in smali.rglob('*.smali')}
    target=smali/'org/efootballrevival/runtimeprobe/LauncherWeb.smali';body=target.read_text();anchor='    sput-object v0, Lorg/efootballrevival/runtimeprobe/LauncherWeb;->EDITOR_OPS:Ljava/util/Map;';assert body.count(anchor)==1 and '"ui73_ucl"'not in body
    addition='''

    const-string v1, "ucl"

    const-string v2, "ui73_ucl"

    invoke-interface {v0, v1, v2}, Ljava/util/Map;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;'''
    target.write_text(body.replace(anchor,anchor+addition));outdex=stage/'classes5-ucl-entry.dex';run('java','-cp',jar,tool,'a',smali,outdex)
    verify=stage/'verify-smali';run('java','-cp',jar,tool,'d',outdex,verify)
    after={p.relative_to(verify).as_posix():sha(p)for p in verify.rglob('*.smali')};assert before.keys()==after.keys();changed=[p for p in before if before[p]!=after[p]];assert changed==['org/efootballrevival/runtimeprobe/LauncherWeb.smali'],changed
    launcher=stage/'assets/launcher';launcher.mkdir(parents=True)
    for name in ['index.html','launcher.js','launcher.css','editor.css','private.css','earth.css']:
        shutil.copyfile(root/'assets/launcher'/name,launcher/name)
    html=(launcher/'index.html').read_text();assert 'id="private-ucl"'not in html
    html=html.replace('<link rel="stylesheet" href="earth.css">','<link rel="stylesheet" href="earth.css">\n<link rel="stylesheet" href="ucl.css">')
    anchor='<button class="quick" id="private-single-player"';assert html.count(anchor)==1
    html=html.replace(anchor,'<button class="quick" id="private-ucl" data-go="home" type="button"><b>UEFA Champions League</b><small>36 đội · 8 lượt · Play-off</small></button>\n'+anchor)
    html=html.replace('<script src="launcher.js"></script>','<script src="launcher.js"></script>\n<script src="ucl.js"></script>');(launcher/'index.html').write_text(html)
    for p in(source/'launcher').iterdir():shutil.copyfile(p,launcher/p.name)
    tools=stage/'assets/gateway-release/work/tools';tools.mkdir(parents=True)
    runtime=root/'source/repair-full8-rc9-ucl/runtime'
    for p in runtime.glob('*.py'):shutil.copyfile(p,tools/p.name)
    for p in runtime.glob('ucl_lp_*.json'):shutil.copyfile(p,tools/p.name)
    bootstrap=root/'assets/gateway-release/work/tools/bridge_73.py';text=bootstrap.read_text();needle='        mod_startup._python_ready=True';assert text.count(needle)==1;text=text.replace(needle,'        import ucl_lp_install\n        ucl_lp_install.install(module)\n'+needle);(tools/'bridge_73.py').write_text(text)
    report=dict(staged_only=True,finished_full=False,baseline_dex_sha256=RC7_DEX,entry_dex_sha256=sha(outdex),classes_verified=len(before),changed_classes=changed,normal_single_player_transfer_classes_exact=True,original_payload_not_modified=True,aggregate_provider_installed=False,phone_verified=False)
    (stage/'entry-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
if __name__=='__main__':build(*sys.argv[1:])
