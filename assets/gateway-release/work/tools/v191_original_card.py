"""Import only the exact upstream Ronaldo2017 card; never grant or rewrite other cards."""
import copy
CARD=89136418985332
def install(module):
 import v191_card_source as source,new_cards_pack_data,legends_v10,diy_runtime
 source._DOCUMENT['cards']=[r for r in source._DOCUMENT['cards']if int(r['payload']['gameplayer_id']['id'])==CARD]
 source._ROUTES=[r for r in source._ROUTES if r['cardId']==CARD]
 source._DOCUMENT['config']={'draw_card_ids':[CARD],'draw_card_labels':['Cristiano Ronaldo']}
 source._DOCUMENT['config']={'draw_card_ids':[CARD],'draw_card_labels':['Cristiano Ronaldo']}
 source._DOCUMENT['config']={'draw_card_ids':[CARD],'draw_card_labels':['Cristiano Ronaldo']}
 source._DOCUMENT['config']={'draw_card_ids':[CARD],'draw_card_labels':['Cristiano Ronaldo']}
 source._DOCUMENT['config']={'draw_card_ids':[CARD],'draw_card_labels':['Cristiano Ronaldo']}
 source._DOCUMENT['config']={'draw_card_ids':[CARD],'draw_card_labels':['Cristiano Ronaldo']}
 source._DOCUMENT['config']={'draw_card_ids':[CARD],'draw_card_labels':['Cristiano Ronaldo']}
 source._DOCUMENT['config']={'draw_card_ids':[CARD],'draw_card_labels':['Cristiano Ronaldo']}
 source._DOCUMENT['config']={'draw_card_ids':[CARD],'draw_card_labels':['Cristiano Ronaldo']}
 source._DOCUMENT['config']={'draw_card_ids':[CARD],'draw_card_labels':['Cristiano Ronaldo']}
 source.MARKER='private_v191_original_ronaldo2017_v1'
 original=new_cards_pack_data.document if hasattr(new_cards_pack_data,'document')else None
 if original is not None:
  def document():return source.extend_document(original())
  new_cards_pack_data.document=document
 result=source.install_once(module._logic.conn)
 return result

def bind(original):
 import diy_runtime
 route={'cardId':CARD,'suiteDonorId':89133724764840,'portraitKey':'9500031','modelNativeId':56334}
 import full2_cards
 return full2_cards.bind(diy_runtime.prepare_binding(original,[route])[0])

def extend_catalogue(document):
 if any(int(r['payload']['gameplayer_id']['id'])==CARD for r in document['cards']):return document
 import v191_card_source as source
 source._DOCUMENT['cards']=[r for r in source._DOCUMENT['cards']if int(r['payload']['gameplayer_id']['id'])==CARD]
 source._DOCUMENT['config']={'draw_card_ids':[CARD],'draw_card_labels':['Cristiano Ronaldo']}
 return source.extend_document(document)
