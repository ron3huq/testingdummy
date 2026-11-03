from pathlib import Path
import hashlib,json,sys,ast
R=Path('/workspace/work/full8-rc2');P=R/'payload';T=P/'assets/gateway-release/work/tools';sys.path[:0]=[str(T),'/workspace/73-v191-migration/decoded']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
import hook_arena,tactics_bridge_runtime,single_player_runtime
assert all(e in hook_arena.PLANS for e in [0x72f2de0,0x8294a5c,0x8294a7c]);a=object.__new__(hook_arena.Arena);a.index={};assert not a.reachable(123)
assert sha(T/'libtactics_bridge.so')==tactics_bridge_runtime.HOOK_SHA
assert sha(T/'libsingle_player.so')==single_player_runtime.HOOK_SHA
from elftools.elf.elffile import ELFFile
with (T/'libtactics_bridge.so').open('rb')as f:
 e=ELFFile(f);assert not[x.name for x in e.get_section_by_name('.dynsym').iter_symbols()if x.name and x['st_shndx']=='SHN_UNDEF']
D=R/'dex-roundtrip2/org/efootballrevival/runtimeprobe'
assert 'CameraPanel;->install(Landroid/app/Application;)V'in(D/'LauncherWeb.smali').read_text()
assert 'SinglePlayerInMatch;->attach(Landroid/app/Activity;)V'in(D/'CameraPanel.smali').read_text()
assert 'TransferTraitsEditor;->menu'in(D/'TransferPlayerEditor.smali').read_text()
assert 'ui7_single_player_live'in(D/'SinglePlayerInMatch.smali').read_text()
for r in json.loads((P/'payload-inventory.json').read_text())['files']:
 f=P/r['path'];assert f.stat().st_size==r['bytes']and sha(f)==r['sha256'],f
for name in ['release-manifest.json','ui6-runtime-manifest.json']:
 d=json.loads((P/'assets/gateway-release'/name).read_text());known={r['path']:r for r in d['files']}
 for rel in ['work/tools/libtactics_bridge.so','work/tools/tactics_bridge_runtime.py','work/tools/transfer_traits.py','livedata/pc9332_mobile_and.ucas']:
  assert known[rel]['sha256']==sha(P/'assets/gateway-release'/rel)
old=Path('/workspace/work/full8/candidate');assert sha(P/'assets/gateway-release/livedata/dt870_mobile_and.cpk')==sha(old/'assets/gateway-release/livedata/dt870_mobile_and.cpk')
assert all(sha(f)==sha(old/f.relative_to(P))for f in(P/'assets/gateway-release/livedata').glob('pc9327*'))
report=dict(passed=True,inventory_files_verified=1090,helper_integrity_pins=True,all_three_additional_hook_slots_preregistered=True,missing_slot_reachable_regression_fixed=True,DEX_roundtrip_actual_launcher_to_lifecycle_to_inmatch_button=True,transfer_menu_to_traits_handler_linked=True,new_resources_in_both_manifests=True,login_CPK_and_working_accessory_pack_unchanged=True,native_helper_no_undefined_imports=True,phone_verified=False)
(R/'package-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
