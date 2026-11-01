"""Allow distinct owned instances of the same person; retain ownership/serial checks."""
def install():
 import e186_cr_stats
 if getattr(e186_cr_stats.validate_cristiano,'_ui76',False):return
 def validate(data):
  # player_identity.validate_squad still verifies ownership and duplicate serials.
  seen=set()
  for row in data.get('player_list')or[]:
   key=row.get('gameplayer_id',row);identity=(int(key.get('id')or 0),int(key.get('serial')or 0))
   if not identity[0]:continue
   if identity in seen:raise ValueError('Same owned instance occupies multiple slots')
   seen.add(identity)
 validate._ui76=True;e186_cr_stats.validate_cristiano=validate
