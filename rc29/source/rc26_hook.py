"""RC26/RC27 bridge for the V30 runtime: wraps _protected_runtime.exec_into (no change to the runtime file itself)."""
import _protected_runtime as _pr
if not getattr(_pr, '_rc27_hooked', False):
    _original_exec_into = _pr.exec_into
    def _wrap_initialize(namespace):
        original = namespace['initialize']
        def initialize(root, installed_version=None):
            result = original(root, installed_version)
            import bridge_73, sys
            bridge_73.install(root, sys.modules[namespace['__name__']])
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
