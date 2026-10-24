"""Load only the V25 face/card payload into the 73 V16 local gateway."""
import importlib.util
import sys
from pathlib import Path

def install(root, module):
    tools = Path(root) / 'work/tools'
    existing = sys.modules.get('noodle_hair')
    if existing is None:
        spec = importlib.util.spec_from_file_location('noodle_hair', tools / 'noodle_hair.py')
        existing = importlib.util.module_from_spec(spec)
        sys.modules['noodle_hair'] = existing
        spec.loader.exec_module(existing)
    original = module._local_urls
    if not getattr(original, '_v25_73', False):
        def local_urls(value):
            # Preserve the 73 gateway's existing conversion and local port.
            return existing.advertise(original(value), 8085)
        local_urls._v25_73 = True
        module._local_urls = local_urls
    existing.start()
    try:
        import select_team_runtime
        select_team_runtime.start()
        import myleague_73
        myleague_73.install()
    except Exception as exc:
        import json
        (tools / 'myleague-73-status.json').write_text(json.dumps({'state':'ERROR','error':str(exc),'version':'v25-73-full1'},indent=2))
    return existing
