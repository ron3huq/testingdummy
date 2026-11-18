import zlib,struct,sys,itertools
sys.path.insert(0,'/home/user/testingdummy/rc26plus'); import ball_tune as bt
d=open('v19/assets/dt270_mobile_all.cpk','rb').read()
st=2048+24576; raw=d[st:st+2582]; cs,us=struct.unpack_from('<II',raw,8)
u=bytearray(zlib.decompress(raw[16:16+cs]))
n=struct.unpack_from('<I',u,0)[0]
ents=[struct.unpack_from('<III',u,8+12*i) for i in range(n)]
names={bytes(u[e[2]:u.index(b'\0',e[2])]).decode():e for e in ents}
off=names['ball.o'][0]
P=dict(bt.PRESETS['ronaldo'],nonSpinRate=1.625,topSpinRiseDecRate=0.8125)
for k,v in P.items(): struct.pack_into('<f',u,off+bt.FIELDS[k],float(v))
u=bytes(u); hits={}
for lvl,ml,strat,wb in itertools.product(range(1,10),range(1,10),range(5),range(9,16)):
    c=zlib.compressobj(lvl,8,wb,ml,strat); x=c.compress(u)+c.flush()
    hits.setdefault(len(x),(lvl,ml,strat,wb))
print(cs, min(hits), hits[min(hits)])
import zopfli.zlib as zz
for it in (15,100,500):
    z=zz.compress(u,numiterations=it); print('zopfli',it,len(z)); 
    assert zlib.decompress(z)==u
def raw(b): return zz.compress(b,numiterations=15)[2:-4]
def build(k, empties=0):
    pre=b''.join(b'\x00\x00\x00\xff\xff' for _ in range(empties))
    if k: pre+=b'\x00'+struct.pack('<HH',k,k^0xffff)+u[:k]
    return b'\x78\xda'+pre+raw(u[k:])+struct.pack('>I',zlib.adler32(u))
best=None
for k in range(0,200):
    x=build(k)
    if len(x)<=cs and (cs-len(x))%5==0:
        x=build(k,(cs-len(x))//5); assert len(x)==cs and zlib.decompress(x)==u; best=(k,x); break
print('found', best[0], len(best[1]))
newtab=d[st:st+8]+struct.pack('<II',cs,us)+best[1]
assert len(newtab)==2582
out=bytearray(d); out[st:st+2582]=newtab; open('dt270_eq.cpk','wb').write(out)
print(sum(1 for a,b in zip(out,d) if a!=b))
