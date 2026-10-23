import json,numpy as np
from pathlib import Path
class Gltf:
 def __init__(self,path):
  p=Path(path);self.d=json.loads(p.read_text());self.b=(p.parent/self.d['buffers'][0]['uri']).read_bytes()
 def get(self,i):
  a=self.d['accessors'][i];v=self.d['bufferViews'][a['bufferView']];w={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}[a['type']];dt={5121:'u1',5123:'<u2',5125:'<u4',5126:'<f4'}[a['componentType']];off=v.get('byteOffset',0)+a.get('byteOffset',0);return np.ndarray((a['count'],w),dt,buffer=self.b,offset=off,strides=(v.get('byteStride',np.dtype(dt).itemsize*w),np.dtype(dt).itemsize)).copy()
