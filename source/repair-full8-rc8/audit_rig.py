import struct

def names(b):
 f=struct.unpack_from('<16I',b);at=f[6];out=[]
 for i in range((f[9]-8)//8):
  h=int.from_bytes(b[at:at+2],'big');at+=2;wide=h>>15;n=h&32767;out.append(b[at:at+n*(2 if wide else 1)].decode('utf16le'if wide else'utf8'));at+=n*(2 if wide else 1)
 return out

