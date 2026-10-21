"""Prepared classic-only stat policy. Not installed while roster data is incomplete."""
import copy
from pathlib import Path

def balance(parameters,role=None):
 import native_overall
 p=list(parameters)
 if len(p)!=147:raise ValueError('canonical147 required')
 p[72]=0
 # Keep each player's style; lower all athletic/technical attributes evenly,
 # preserving height, weak foot and position proficiency. Neutral OVR cap.
 fields=[i for i in range(14,41) if i not in (33,37)]
 for attempt in range(90):
  values=[native_overall.rating(p,pos) for pos in range(13)]
  if max(values)<=89:return p,values
  for i in fields:p[i]=max(40,p[i]-1)
 raise ValueError('unable to satisfy neutral OVR89')

def remove_learned_marseille(slots):return [74 if s==3 else s for s in slots]
