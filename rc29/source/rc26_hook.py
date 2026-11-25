"""RC26 bridge for the V32 runtime: wraps _protected_runtime.exec_into (no change to the runtime file itself).
RC29: ml_isolation keeps the V32 Master League on the original V32 functions and data (My League stays RC26)."""
import _protected_runtime as _pr
if not getattr(_pr, '_rc27_hooked', False):
    _original_exec_into = _pr.exec_into
    def _wrap_initialize(namespace):
        original = namespace['initialize']
        def initialize(root, installed_version=None):
            result = original(root, installed_version)
            import bridge_73, sys
            iso = None
            try:
                import ml_isolation as iso
                iso.snapshot()
            except Exception:
                iso = None
            bridge_73.install(root, sys.modules[namespace['__name__']])
            if iso is not None:
                try:
                    iso.install()
                except Exception:
                    pass
            try:
                import ml_realism
                ml_realism.install()
            except Exception:
                pass
            try:
                import ml_awards
                ml_awards.install()
            except Exception:
                pass
            try:
                import ml_skills
                ml_skills.install()
            except Exception:
                pass
            try:
                import ml_transfer
                ml_transfer.install()
            except Exception:
                pass
            try:
                import ml_guard
                ml_guard.install()
            except Exception:
                pass
            return result
        namespace['initialize'] = initialize
    def exec_into(name, namespace):
        _original_exec_into(name, namespace)
        if name == 'legends_v10':
            import v191_original_card, v191_live
            v191_live.pin_rebased_kits(namespace)
            namespace['_start_legend_portrait_binding'] = v191_original_card.bind(namespace['_start_legend_portrait_binding'])
        if name == 'new_cards_pack_data':
            import v191_original_card
            namespace['DOCUMENT'] = v191_original_card.extend_catalogue(namespace['DOCUMENT'])
        if name == 'embedded_gateway':
            _wrap_initialize(namespace)
    _pr.exec_into = exec_into
    _pr._rc27_hooked = True
