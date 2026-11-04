from pathlib import Path
import struct,cityhash
MASK=(1<<62)-1
def pid(s):return cityhash.CityHash64(s.lower().encode('utf-16-le'))
def objid(s):return (pid(s)&MASK)|(2<<62)
def rename(data,replacements,own_old=None,own_new=None,imports=None):
 b=bytearray(data);f=list(struct.unpack_from('<16I',b));ns,nsize,hs,hsize=f[6:10];at=ns;names=[];count=(hsize-8)//8;batch=bytearray();hashes=bytearray(b[hs:hs+hsize])
 for i in range(count):
  h=int.from_bytes(b[at:at+2],'big');at+=2;w=h>>15;n=h&32767;name=bytes(b[at:at+n*(2 if w else 1)]).decode('utf-16-le' if w else 'utf8');at+=n*(2 if w else 1)
  new=replacements.get(name,name);raw=new.encode('utf-16-le' if w else 'utf8');batch+=((len(new)|(w<<15))).to_bytes(2,'big')+raw;names.append((name,new))
  if new!=name:struct.pack_into('<Q',hashes,8+i*8,cityhash.CityHash64(new.lower().encode('utf-16-le' if w else 'utf8')))
 assert at==ns+nsize
 newhs=(ns+len(batch)+7)&~7;new=bytearray(b[:ns])+batch+b'\0'*(newhs-ns-len(batch))+hashes+b[hs+hsize:];shift=newhs-hs
 f[7]=len(batch);f[8]=newhs
 for j in [10,11,12,13]:f[j]+=shift
 struct.pack_into('<16I',new,0,*f)
 em=f[11];export_count=(f[12]-em)//72
 if own_old and own_new:
  oldbase=own_old.rsplit('/',1)[-1];newbase=own_new.rsplit('/',1)[-1]
  for i in range(export_count):
   field=em+72*i+56;v=struct.unpack_from('<Q',new,field)[0]
   if v==objid(own_old+'/'+oldbase):struct.pack_into('<Q',new,field,objid(own_new+'/'+newbase))
 for old,renamed in (imports or {}).items():
  oldval=objid(old+'/'+old.rsplit('/',1)[-1]);newval=objid(renamed+'/'+renamed.rsplit('/',1)[-1])
  for field in range(f[10],f[11],8):
   if struct.unpack_from('<Q',new,field)[0]==oldval:struct.pack_into('<Q',new,field,newval)
  gs=f[13];ge=gs+f[14];chunk=bytes(new[gs:ge]);chunk=chunk.replace(struct.pack('<Q',pid(old)),struct.pack('<Q',pid(renamed)));new[gs:ge]=chunk
 return bytes(new)
