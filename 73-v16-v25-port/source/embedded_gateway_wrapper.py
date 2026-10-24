# Preserve the original 73 encrypted business module; add an explicit V25 bridge.
import _protected_runtime
_protected_runtime.exec_into(__name__, globals())
_v25_original_initialize = initialize

def initialize(root, installed_version=None):
    result = _v25_original_initialize(root, installed_version)
    try:
        import importlib.util
        import sys
        from pathlib import Path
        tools = Path(root) / 'work/tools'
        name = '_v25_bridge_73'
        bridge = sys.modules.get(name)
        if bridge is None:
            spec = importlib.util.spec_from_file_location(name, tools / 'bridge_73.py')
            bridge = importlib.util.module_from_spec(spec)
            sys.modules[name] = bridge
            spec.loader.exec_module(bridge)
        bridge.install(root, sys.modules[__name__])
    except Exception as exc:
        # A mod failure must not replace the working game's startup result.
        try:
            (Path(root) / 'work/tools/v25-73-bootstrap-error.txt').write_text(str(exc))
        except Exception:
            pass
    return result
