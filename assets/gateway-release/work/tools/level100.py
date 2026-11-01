"""Raise the editable progression ceiling for every card type; do not train or grant points on load."""
def install():
 import player_editor
 development=player_editor.development
 development.LEVEL_LIMIT_MAX=100
 development.CARD_LEVEL_CAPS.clear()
 return True
