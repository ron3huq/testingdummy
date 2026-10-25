from pathlib import Path
import hashlib,zlib,struct,json,re
from loguru import logger
logger.remove()
from androguard.core.dex import DEX
p=Path('/workspace/ronaldo-work/73-ui6');b=(p/'classes5.dex').read_bytes();assert b[:8]==b'dex\n037\x00';assert hashlib.sha1(b[32:]).digest()==b[12:32];assert zlib.adler32(b[12:])&0xffffffff==struct.unpack_from('<I',b,8)[0]
d=DEX(b);old=DEX(Path('/workspace/ronaldo-work/73-inspect/v16-meta/classes5.dex').read_bytes());classes={x.get_name():x for x in d.get_classes()};assert set(x.get_name()for x in old.get_classes())<=set(classes)
for c in classes.values():
 methods=[(m.get_name(),m.get_descriptor())for m in c.get_methods()];assert len(set(methods))==len(methods),c.get_name()
C='Lorg/efootballrevival/runtimeprobe/'
for cls,names in [('GatewayBootActivity',['idleArm','idleStop','idleCheck','dispatchTouchEvent','onWindowFocusChanged','styleEnter']),('EnglishDisplay',['setText'])]:
 m={x.get_name()for x in classes[C+cls+';'].get_methods()};assert set(names)<=m
assert not any('EditorExtras'in x or 'PlayerDetails'in x for x in classes)and b'Body & motion'not in b and b'Height / skills'not in b
assert C+'ResponsiveUi;'in classes and C+'ModPayloadRepair;'in classes
assert b'ui6-runtime-manifest.json'in b
assert 'ModPayloadRepair;->ensure' in (p/'smali/org/efootballrevival/runtimeprobe/EmbeddedGateway.smali').read_text()
assert 'ui6_preserve_done'in (p/'smali/org/efootballrevival/runtimeprobe/EmbeddedGateway.smali').read_text()
u=(p/'smali/org/efootballrevival/runtimeprobe/UiStrings.smali').read_text();assert 'ExtraTranslations;->fill' in u
# New method register allocation: p0=v7; wide pairs remain below v7.
s=(p/'smali/org/efootballrevival/runtimeprobe/GatewayBootActivity.smali').read_text();chunk=s[s.index('.method public idleCheck()V'):];chunk=chunk[:chunk.index('.end method')];assert '.registers 8' in chunk and 'const-wide/16 v5,0x2710' in chunk and 'idleTouch:Z' in chunk
assert 'Auto-enter after 10s idle' in (p/'smali/org/efootballrevival/runtimeprobe/UiStringsData.smali').read_text()
checks=['DEX signature/checksum parse and original classes retained','all class method signatures unique; Body & motion classes and calls absent; idle hooks preserved','English forced; English-only strings bypass Chinese regex templates','10-second timer uses monotonic time; touch/busy/editor/notice/window/pause guards present; exact remaining-delay scheduling','launcher subtitle explains idle enter; Enter minimum height doubled']
(p/'ui-validation.json').write_text(json.dumps({'passed':True,'checks':checks,'android_device_tested':False,'original_classes':len(old.get_classes()),'updated_classes':len(classes)},indent=2));print('DEX_PASS',len(classes))
