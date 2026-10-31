"""Reuse read-only editor responses until the local database changes.
No body/motion projection, no per-player SQL, and no background preload.
"""
import functools,sqlite3

def install(module):
 original=module.manage
 if getattr(original,'_ui2_fast',False):return False
 cache={};last_conn=None
 def stamp():
  conn=module._logic.conn
  return conn,conn.total_changes,conn.execute('PRAGMA data_version').fetchone()[0],conn.in_transaction
 @functools.wraps(original)
 def manage(action,path=''):
  nonlocal last_conn
  if action not in ('editor_list','editor_catalog'):
   # Save restore, edits and game commands retain the original implementation.
   cache.clear()
   return original(action,path)
  try:mark=stamp()
  except (AttributeError,sqlite3.ProgrammingError):
   # Let the original gateway reopen/recover a restored or closed save first.
   cache.clear();value=original(action,path)
   try:
    post=stamp();last_conn=post[0];cache[(action,path)]=(post,value)
   except (AttributeError,sqlite3.ProgrammingError):pass
   return value
  if mark[0]is not last_conn:cache.clear();last_conn=mark[0]
  key=(action,path);item=cache.get(key)
  if item is not None and item[0]==mark:return item[1]
  value=original(action,path)
  cache[key]=(stamp(),value)
  if len(cache)>4:
   for k in list(cache):
    if k!=key:cache.pop(k,None)
  return value
 manage._ui2_fast=True;module.manage=manage
 return True
