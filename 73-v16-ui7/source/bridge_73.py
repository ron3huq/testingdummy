"""Load only the V25 face/card payload into the 73 V16 local gateway."""
import importlib.util
import sys
from pathlib import Path

def install(root, module):
    tools = Path(root) / 'work/tools'
    import mod_startup
    mod_startup.install()
    existing = sys.modules.get('noodle_hair')
    if existing is None:
        spec = importlib.util.spec_from_file_location('noodle_hair', tools / 'noodle_hair.py')
        existing = importlib.util.module_from_spec(spec)
        sys.modules['noodle_hair'] = existing
        spec.loader.exec_module(existing)
    import extras_runtime,manager_runtime,kits_runtime
    original = module._local_urls
    if not getattr(original, '_v25_73', False):
        def local_urls(value):
            # Preserve the 73 gateway's existing conversion and local port.
            return kits_runtime.advertise(manager_runtime.advertise(extras_runtime.advertise(existing.advertise(original(value),8085),8085),8085),8085)
        local_urls._v25_73 = True
        module._local_urls = local_urls
    import editor_names,editor_fast,card_rules
    editor_names.install()
    card_rules.install()
    card_rules.install_native_config(root)
    import body_dimensions
    body_dimensions.install(root,module)
    editor_fast.install(module)
    existing.start()
    try:
        import select_team_runtime
        select_team_runtime.start()
        import myleague_73
        myleague_73.install()
        if not myleague_73._installed:raise RuntimeError("My League adapter did not install")
        mod_startup._python_ready=True
    except Exception as exc:
        import json
        try:(tools / 'myleague-73-status.json').write_text(json.dumps({'state':'ERROR','error':str(exc),'version':'73-ui7-full'},indent=2))
        except OSError:pass
        raise RuntimeError('UI7 Python adapter initialization failed')from exc
    return existing
