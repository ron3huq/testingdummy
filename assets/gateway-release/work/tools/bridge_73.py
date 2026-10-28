"""Load only the V25 face/card payload into the 73 V16 local gateway."""
import importlib.util
import sys
from pathlib import Path

def install(root, module):
    tools = Path(root) / 'work/tools'
    import mod_startup
    mod_startup.install()
    import level100
    level100.install()
    import multi_cards
    multi_cards.install()
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
            return __import__('photo_editor').advertise(__import__('private_bundles').advertise(kits_runtime.advertise(manager_runtime.advertise(extras_runtime.advertise(existing.advertise(original(value),8085),8085),8085),8085),8085),8085)
        local_urls._v25_73 = True
        module._local_urls = local_urls
    import editor_names,editor_fast,card_rules
    editor_names.install()
    card_rules.install()
    import appearance_choices
    appearance_choices.migrate(root,module._logic.conn)
    card_rules.install_native_config(root)
    import body_dimensions
    body_dimensions.install(root,module)
    import player_model
    player_model.install(module)
    import player_tuning
    player_tuning.install(module)
    appearance_choices.install(module)
    import appearance_gear
    appearance_gear.install(module)
    import profile_editor
    profile_editor.install(module)
    import photo_editor
    photo_editor.install(module)
    import stat_editor
    stat_editor.install(module)
    import motion_editor
    motion_editor.install(module)
    import transfer_editor
    transfer_editor.install(module)
    editor_fast.install(module)
    existing.start()
    try:
        import select_team_runtime
        select_team_runtime.start()
        import myleague_73
        myleague_73.install()
        transfer_editor.post_install()
        if not myleague_73._installed:raise RuntimeError("My League adapter did not install")
        mod_startup._python_ready=True
    except Exception as exc:
        import json
        try:(tools / 'myleague-73-status.json').write_text(json.dumps({'state':'ERROR','error':str(exc),'version':'73-ui7-full'},indent=2))
        except OSError:pass
        raise RuntimeError('UI7 Python adapter initialization failed')from exc
    return existing
