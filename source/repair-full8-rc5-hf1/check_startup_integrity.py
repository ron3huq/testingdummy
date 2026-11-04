"""Exercise actual pre-login asset validators; never load ARM64 hooks on host.
This complements the outer installer manifest check, which missed RC5's nested pin.
"""
from pathlib import Path
import sys,json,hashlib,ast

def verify(root):
 root=Path(root);g=root/'assets/gateway-release';t=g/'work/tools';sys.path.insert(0,str(t))
 import noodle_hair,private_bundles,mod_integrity
 noodle_hair.HERE=t;private_bundles.HERE=t
 mod_integrity._cache.clear();private_bundles.verified.cache_clear()
 meta=noodle_hair.bundle() # Same validator that blocked the phone's LOGIN.
 private=private_bundles.verified()
 # Check the module-specific native SHA constants without importing workers.
 native_pins=0
 for source in t.glob('*.py'):
  tree=ast.parse(source.read_text());pins={}
  for node in tree.body:
   if isinstance(node,ast.Assign)and isinstance(node.value,ast.Constant):
    for target in node.targets:
     if isinstance(target,ast.Name):pins[target.id]=node.value.value
  pin=pins.get('HOOK_SHA')
  if not isinstance(pin,str)or len(pin)!=64:continue
  # Known library ownership; never map another record type by assumption.
  owned={'noodle_hair.py':'libnoodle_hair.so','single_player_runtime.py':'libsingle_player.so','single_player_live_runtime.py':'libsingle_player_live.so','cached_lookup_runtime.py':'libcached_lookup.so','tactics_bridge_runtime.py':'libtactics_bridge.so'}
  lib=owned.get(source.name)
  if lib:assert hashlib.sha256((t/lib).read_bytes()).hexdigest()==pin,source.name;native_pins+=1
 runtime=json.loads((g/'ui6-runtime-manifest.json').read_text())
 for row in runtime['files']:
  p=g/row['path'];assert p.stat().st_size==row['bytes']and hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'],row['path']
 # Confirm the guard still requires ready native modules, without invoking it.
 guard=(t/'mod_startup.py').read_text();assert 'if guarded:require_ready()'in guard and 'noodle_hair.wait_ready(15)'in guard
 return dict(passed=True,actual_noodle_bundle_prelogin_validator=True,actual_private_bundle_validator=True,nested_appearance_pins=len(meta['appearance_files']),private_asset_files=len(private['files']),module_native_pins=native_pins,runtime_assets=len(runtime['files']),login_readiness_guard_preserved=True,phone_verified=False)
if __name__=='__main__':print(json.dumps(verify(sys.argv[1]),indent=2))
