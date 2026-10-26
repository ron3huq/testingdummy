"""Native IoStore writer for immutable per-colour texture generations."""

import struct,hashlib,zlib

from pathlib import Path

ENTRY=16

def wstr(s):
    b = s.encode("latin1") + b"\0"
    return struct.pack("<i", len(b)) + b

def build_store(entries):
    n = len(entries)
    head = bytearray(); tail = bytearray(); tail_base = ENTRY * n
    for i, (fixed, imports) in enumerate(entries):
        e = bytearray(fixed)
        field = ENTRY * i + 8
        if imports:
            pos = tail_base + len(tail); tail += struct.pack("<%dQ" % len(imports), *imports)
            e += struct.pack("<II", len(imports), pos - field)
        else:
            e += struct.pack("<II", 0, 0)
        head += e
    return bytes(head + tail)

def dir_index(mount, paths_to_index):
    """FIoDirectoryIndexResource with the given relative paths -> toc entry index."""
    strings, sidx = [], {}
    def S(x):
        if x not in sidx:
            sidx[x] = len(strings); strings.append(x)
        return sidx[x]
    dirs = [[0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF]]  # root
    files = []
    children = {0: {}}
    for path, idx in sorted(paths_to_index.items()):
        parts = path.split("/")
        d = 0
        for part in parts[:-1]:
            ch = children[d]
            if part not in ch:
                nd = len(dirs); dirs.append([S(part), 0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF]); children[nd] = {}
                # prepend as first child
                dirs[nd][2] = dirs[d][1]; dirs[d][1] = nd; ch[part] = nd
            d = ch[part]
        fi = len(files); files.append([S(parts[-1]), dirs[d][3], idx]); dirs[d][3] = fi
    out = bytearray(wstr(mount))
    out += struct.pack("<I", len(dirs)) + b"".join(struct.pack("<IIII", *x) for x in dirs)
    out += struct.pack("<I", len(files)) + b"".join(struct.pack("<III", *x) for x in files)
    out += struct.pack("<I", len(strings)) + b"".join(wstr(x) for x in strings)
    return bytes(out)


def write(folder,stem,header,pak,files):
 folder=Path(folder);folder.mkdir(parents=True,exist_ok=True);cid=int.from_bytes(hashlib.sha256(b'ui79-rgb-container').digest()[:8],'little');pids=[];entries=[];chunks=[];paths={};block=65536
 for path,idb,data,entry in files:
  paths[path]=len(chunks);chunks.append((idb,data,hashlib.sha1(data).digest()+b'\0'*12+b'\1'));pids.append(int.from_bytes(idb[:8],'little'));entries.append(entry)
 assert len(pids)==len(set(pids));st=build_store(entries);hb=struct.pack('<QI',cid,len(pids))+struct.pack('<i',0)+struct.pack('<iQ',8,0xC1640000)+struct.pack('<i',len(pids))+struct.pack('<%dQ'%len(pids),*pids)+struct.pack('<i',len(st))+st+struct.pack('<ii',0,0);chunks.append((struct.pack('<Q',cid)+b'\0\0\0\x0a',hb,hashlib.sha1(hb).digest()+b'\0'*13));ids=[];ols=[];blocks=[];voff=0
 with(folder/(stem+'.ucas')).open('wb')as out:
  for idb,body,meta in chunks:
   ids.append(idb);ols.append((voff,len(body)))
   for at in range(0,len(body),block):
    raw=body[at:at+block];compressed=zlib.compress(raw,6);method=int(len(compressed)<len(raw));payload=compressed if method else raw;blocks.append((out.tell(),len(payload),len(raw),method));out.write(payload)
   voff+=(len(body)+block-1)//block*block
 di=dir_index('../../../PesMobile/Content/Assets/',paths);h=bytearray(header);struct.pack_into('<9I',h,20,len(h),len(ids),len(blocks),12,1,32,block,len(di),0);struct.pack_into('<Q',h,56,cid);h[64:80]=b'\0'*16;h[80]=9
 toc=bytes(h)+b''.join(ids)+b''.join(a.to_bytes(5,'big')+b.to_bytes(5,'big')for a,b in ols)+b''.join(a.to_bytes(5,'little')+b.to_bytes(3,'little')+c.to_bytes(3,'little')+bytes([m])for a,b,c,m in blocks)+b'Zlib'.ljust(32,b'\0')+di+b''.join(row[2]for row in chunks)
 (folder/(stem+'.utoc')).write_bytes(toc);(folder/(stem+'.pak')).write_bytes(pak)
 return {ext:{'size':(folder/(stem+'.'+ext)).stat().st_size,'sha256':hashlib.sha256((folder/(stem+'.'+ext)).read_bytes()).hexdigest()}for ext in ['pak','utoc','ucas']}
