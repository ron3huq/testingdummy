from pathlib import Path
import shutil
p=Path('/workspace/ronaldo-work/73-ui74');old=p.with_name('73-ui73')
for n in['smali','java','stubs-out']:shutil.copytree(old/n,p/n,dirs_exist_ok=True)
for n in['java-out','dex-helper','payload/work/tools']:(p/n).mkdir(parents=True,exist_ok=True)
shutil.copy2('/workspace/ronaldo-work/73-ui72/payload/work/tools/kits_runtime.py',p/'payload/work/tools/kits_runtime.py');f=p/'payload/work/tools/kits_runtime.py';s=f.read_text().replace('dt870_ui72_mobile_and.cpk','dt870_ui74_mobile_and.cpk').replace("version['version']+=61","version['version']+=63");f.write_text(s)
shutil.copy2(old/'payload/work/tools/mod_startup.py',p/'payload/work/tools/mod_startup.py');f=p/'payload/work/tools/mod_startup.py';f.write_text(f.read_text().replace('73-ui7.3','73-ui7.4').replace('>=8','>=64'))
for f in[p/'smali/org/efootballrevival/runtimeprobe/UiStringsData.smali',p/'java/org/efootballrevival/runtimeprobe/RuntimeDiagnostics.java']:
 s=f.read_text().replace('UI7.3','UI7.4')
 if f.suffix=='.java':s=s.replace('"mod-last-error.json",','"http-resource-status.json","mod-last-error.json",')
 f.write_text(s)
f=p/'smali/org/efootballrevival/runtimeprobe/EmbeddedGateway.smali';s=f.read_text();start=s.index('.method public serve(');at=s.index('    .line 127',start);s=s[:at]+'''    invoke-virtual {v2, v0}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z
    move-result v3
    if-eqz v3, :ui74_not_static
    iget-object v3, p0, Lorg/efootballrevival/runtimeprobe/EmbeddedGateway;->payload:Ljava/io/File;
    invoke-static {v3, p1}, Lorg/efootballrevival/runtimeprobe/LiveResourceServer;->serve(Ljava/io/File;Lfi/iki/elonen/NanoHTTPD$IHTTPSession;)Lfi/iki/elonen/NanoHTTPD$Response;
    move-result-object v3
    return-object v3
    :ui74_not_static

'''+s[at:];f.write_text(s)
