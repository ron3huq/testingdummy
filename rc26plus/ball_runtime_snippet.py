

# ---- RC26 PLUS: Ronaldo dip/knuckle ball trajectory, applied in memory (dt270 untouched) ----
_BALL_SIG=struct.pack('<5f',105.0,45.0,1.0,1.0,1.0)  # nonSpinMax,Min,Rate,TopDownDecRate,TopRiseDecRate (original)
# layout name -> (offset of signature, magnusRate, topSpinChangeSpeed) relative to struct start
_BALL_LAYOUTS={'engine':(0x244,0x208,0x2e0),'table':(0xac,0x98,0xf4)}
_BALL_NEW={'nonSpinMax':125.0,'nonSpinMin':38.0,'nonSpinRate':1.6,'nonSpinTopDownDecRate':5.0,'nonSpinTopRiseDecRate':0.75,
           'topSpinDownDecRate':15.0,'topSpinRiseDecRate':0.7}
_ball_status={'state':'not_started','patched':[],'scans':0,'repatches':0,'error':None}
def _ball_new_bytes():
    n=_BALL_NEW
    return (struct.pack('<5f',n['nonSpinMax'],n['nonSpinMin'],n['nonSpinRate'],n['nonSpinTopDownDecRate'],n['nonSpinTopRiseDecRate']),
            struct.pack('<2f',n['topSpinDownDecRate'],n['topSpinRiseDecRate']))
def _ball_regions():
    out=[]
    with open('/proc/self/maps') as f:
        for line in f:
            p=line.split(None,5)
            if len(p)<5 or p[1][:2]!='rw':continue
            name=p[5].strip() if len(p)>5 else ''
            if name.startswith('/dev/') or 'stack_and_tls' in name or 'dalvik' in name:continue
            a,b=(int(x,16) for x in p[0].split('-'))
            if b-a>(768<<20):continue
            out.append((a,b))
    return out
def _ball_check(fd,base,layout):
    sig,mag,top=_BALL_LAYOUTS[layout]
    try:
        m=os.pread(fd,4,base+mag);t=os.pread(fd,12,base+top)
    except OSError:return False
    if len(m)!=4 or len(t)!=12:return False
    mv=struct.unpack('<f',m)[0];tc,td,tr=struct.unpack('<3f',t)
    return abs(mv-0.035)<1e-5 and abs(tc-0.175)<1e-5 and (abs(td-10.0)<1e-4 or abs(td-_BALL_NEW['topSpinDownDecRate'])<1e-4) \
        and (abs(tr-1.0)<1e-5 or abs(tr-_BALL_NEW['topSpinRiseDecRate'])<1e-5)
def _ball_write(fd,addr,data):
    try:
        if os.pwrite(fd,data,addr)==len(data):return
    except OSError:pass
    C.memmove(addr,data,len(data))
def _ball_scan(fd):
    found=[];chunk=4<<20
    for a,b in _ball_regions():
        pos=a
        while pos<b:
            n=min(chunk+32,b-pos)
            try:buf=os.pread(fd,n,pos)
            except OSError:break
            i=buf.find(_BALL_SIG)
            while i>=0:
                hit=pos+i
                for layout,(sig,_m,_t) in _BALL_LAYOUTS.items():
                    if _ball_check(fd,hit-sig,layout):found.append((hit-sig,layout))
                i=buf.find(_BALL_SIG,i+4)
            if len(buf)<n:break
            pos+=chunk
    return sorted(set(found))
def _ball_apply(fd,base,layout):
    sig,_m,top=_BALL_LAYOUTS[layout];a,b=_ball_new_bytes()
    _ball_write(fd,base+sig,a);_ball_write(fd,base+top+4,b)
    return os.pread(fd,len(a),base+sig)==a and os.pread(fd,len(b),base+top+4)==b
def _ball_worker():
    a,b=_ball_new_bytes();known=[];delay=4
    try:
        fd=os.open('/proc/self/mem',os.O_RDWR)
    except OSError:
        fd=os.open('/proc/self/mem',os.O_RDONLY)
    _ball_status['state']='SCANNING'
    while True:
        try:
            alive=[]
            for base,layout in known:
                sig,_m,top=_BALL_LAYOUTS[layout]
                if not _ball_check(fd,base,layout):continue
                if os.pread(fd,len(a),base+sig)!=a or os.pread(fd,len(b),base+top+4)!=b:
                    if os.pread(fd,len(_BALL_SIG),base+sig)!=_BALL_SIG:continue
                    _ball_apply(fd,base,layout);_ball_status['repatches']+=1
                alive.append((base,layout))
            known=alive
            if not known or delay>=60:
                _ball_status['scans']+=1
                for hit in _ball_scan(fd):
                    if hit not in known and _ball_apply(fd,*hit):known.append(hit)
                delay=4 if not known else 0
            _ball_status['patched']=[{'address':hex(x),'layout':l} for x,l in known]
            _ball_status['state']='APPLIED' if known else 'SCANNING'
            _ball_status['error']=None
        except Exception as e:
            _ball_status['error']=repr(e)[:300]
        # once applied: cheap re-check every 2s, full rescan every ~60s for new copies (e.g. new match)
        if known:delay+=2;time.sleep(2)
        else:time.sleep(delay);delay=min(delay+2,20)
def _ball_start():
    if _ball_status['state']!='not_started':return
    _ball_status['state']='STARTING';_ball_status['values']=dict(_BALL_NEW)
    threading.Thread(target=_ball_worker,name='ball-trajectory',daemon=True).start()
