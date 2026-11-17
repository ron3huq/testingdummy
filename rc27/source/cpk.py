"""Minimal CRI CPK reader (UTF tables, TOC) for comparing game data packs."""
import struct, sys, hashlib

def unmask(b):
    out = bytearray(len(b)); m = 0x655f
    for i, c in enumerate(b):
        out[i] = c ^ (m & 0xff); m = (m * 0x4115) & 0xffffffff
    return bytes(out)

def read_utf(data):
    if data[:4] != b'@UTF': data = unmask(data)
    assert data[:4] == b'@UTF', data[:8]
    size = struct.unpack('>I', data[4:8])[0]
    t = data[8:8 + size]
    rows_off, str_off, data_off, name_off = struct.unpack('>IIII', t[0:16])
    ncols, rowlen, nrows = struct.unpack('>HHI', t[16:24])
    strs = t[str_off:data_off]; blob = t[data_off:]
    def gstr(o):
        e = strs.index(b'\0', o); return strs[o:e].decode('utf-8', 'replace')
    cols = []; p = 24
    fmts = {0: ('>B', 1), 1: ('>b', 1), 2: ('>H', 2), 3: ('>h', 2), 4: ('>I', 4), 5: ('>i', 4), 6: ('>Q', 8), 7: ('>q', 8), 8: ('>f', 4), 0xA: ('S', 4), 0xB: ('D', 8)}
    for _ in range(ncols):
        flags = t[p]; p += 1
        name = gstr(struct.unpack('>I', t[p:p + 4])[0]); p += 4
        storage = flags & 0xf0; typ = flags & 0x0f; const = None
        if storage == 0x30:
            const, n = readval(t, p, typ, fmts, gstr, blob); p += n
        cols.append((name, storage, typ, const))
    rows = []
    for r in range(nrows):
        q = rows_off + r * rowlen; row = {}
        for name, storage, typ, const in cols:
            if storage == 0x50:
                row[name], n = readval(t, q, typ, fmts, gstr, blob); q += n
            elif storage == 0x30: row[name] = const
            else: row[name] = None
        rows.append(row)
    return rows

def readval(t, p, typ, fmts, gstr, blob):
    f, n = fmts[typ]
    if f == 'S': return gstr(struct.unpack('>I', t[p:p + 4])[0]), 4
    if f == 'D':
        o, l = struct.unpack('>II', t[p:p + 8]); return blob[o:o + l], 8
    return struct.unpack(f, t[p:p + n])[0], n

def read(path):
    d = open(path, 'rb').read()
    assert d[:4] == b'CPK '
    hdr = read_utf(d[0x10:0x10 + struct.unpack('<Q', d[8:16])[0]])[0]
    toc_off = hdr['TocOffset']; content_off = hdr.get('ContentOffset') or toc_off
    tsize = struct.unpack('<Q', d[toc_off + 8:toc_off + 16])[0]
    toc = read_utf(d[toc_off + 0x10:toc_off + 0x10 + tsize])
    base = min(toc_off, content_off)
    files = []
    for r in toc:
        off = r['FileOffset'] + base
        name = (r['DirName'] + '/' if r.get('DirName') else '') + r['FileName']
        raw = d[off:off + r['FileSize']]
        files.append(dict(name=name, size=r['FileSize'], extract=r['ExtractSize'], id=r.get('ID'), off=off, sha=hashlib.sha256(raw).hexdigest()))
    return hdr, files, d

if __name__ == '__main__':
    hdr, files, _ = read(sys.argv[1])
    print({k: v for k, v in hdr.items() if not isinstance(v, bytes)})
    for f in files[:int(sys.argv[2]) if len(sys.argv) > 2 else 20]: print(f)
    print('files', len(files))

# ---------------- writer ----------------
def parse_schema(data):
    """Return (table_name, cols, rows) preserving column schema."""
    if data[:4] != b'@UTF': data = unmask(data)
    size = struct.unpack('>I', data[4:8])[0]; t = data[8:8 + size]
    rows_off, str_off, data_off, name_off = struct.unpack('>IIII', t[0:16])
    ncols, rowlen, nrows = struct.unpack('>HHI', t[16:24])
    strs = t[str_off:data_off]
    def gstr(o): e = strs.index(b'\0', o); return strs[o:e].decode()
    fmts = {0: ('>B', 1), 1: ('>b', 1), 2: ('>H', 2), 3: ('>h', 2), 4: ('>I', 4), 5: ('>i', 4), 6: ('>Q', 8), 7: ('>q', 8), 8: ('>f', 4), 0xA: ('S', 4), 0xB: ('D', 8)}
    cols = []; p = 24
    for _ in range(ncols):
        flags = t[p]; name = gstr(struct.unpack('>I', t[p + 1:p + 5])[0]); p += 5; const = None
        if flags & 0xf0 == 0x30:
            const, n = readval(t, p, flags & 0xf, fmts, gstr, t[data_off:]); p += n
        cols.append((name, flags, const))
    return gstr(name_off), cols, read_utf(data)

def write_utf(table_name, cols, rows, pad_to=None):
    fmts = {0: '>B', 1: '>b', 2: '>H', 3: '>h', 4: '>I', 5: '>i', 6: '>Q', 7: '>q', 8: '>f'}
    sizes = {0: 1, 1: 1, 2: 2, 3: 2, 4: 4, 5: 4, 6: 8, 7: 8, 8: 4, 0xA: 4, 0xB: 8}
    pool = bytearray(); index = {}; dpool = bytearray()
    def s(x):
        if x not in index: index[x] = len(pool); pool.extend(x.encode() + b'\0')
        return index[x]
    s(table_name)
    for name, flags, const in cols: s(name)
    def enc(typ, v):
        if typ == 0xA: return struct.pack('>I', s(v))
        if typ == 0xB:
            v = v or b''; o = len(dpool); dpool.extend(v); return struct.pack('>II', o if v else 0, len(v))
        return struct.pack(fmts[typ], v)
    coldesc = bytearray()
    for name, flags, const in cols:
        coldesc += bytes([flags]) + struct.pack('>I', index[name])
        if flags & 0xf0 == 0x30: coldesc += enc(flags & 0xf, const)
    rowdata = bytearray(); rowlen = 0
    for name, flags, const in cols:
        if flags & 0xf0 == 0x50: rowlen += sizes[flags & 0xf]
    for r in rows:
        for name, flags, const in cols:
            if flags & 0xf0 == 0x50: rowdata += enc(flags & 0xf, r[name])
    rows_off = 24 + len(coldesc); str_off = rows_off + len(rowdata); data_off = str_off + len(pool)
    t = struct.pack('>IIII', rows_off, str_off, data_off, 0) + struct.pack('>HHI', len(cols), rowlen, len(rows)) + coldesc + rowdata + pool + dpool
    return b'@UTF' + struct.pack('>I', len(t)) + t

def build(src_path, new_files, out_path):
    """Rebuild CPK: keep src files/order, append new_files [(dir, name, bytes)] with new IDs."""
    d = open(src_path, 'rb').read()
    hsize = struct.unpack('<Q', d[8:16])[0]
    hname, hcols, hrows = parse_schema(d[0x10:0x10 + hsize]); hdr = hrows[0]
    toc_off = hdr['TocOffset']; tsize = struct.unpack('<Q', d[toc_off + 8:toc_off + 16])[0]
    tname, tcols, toc = parse_schema(d[toc_off + 0x10:toc_off + 0x10 + tsize])
    base = min(toc_off, hdr['ContentOffset']); align = hdr['Align']
    blobs = [d[r['FileOffset'] + base:r['FileOffset'] + base + r['FileSize']] for r in toc]
    rows = [dict(r) for r in toc]; nid = max(r['ID'] for r in toc) + 1
    for dirn, name, data in new_files:
        rows.append(dict(DirName=dirn, FileName=name, FileSize=len(data), ExtractSize=len(data), FileOffset=0, ID=nid, UserString='<NULL>')); blobs.append(data); nid += 1
    def al(x): return (x + align - 1) // align * align
    # iterate: toc size depends only on strings/rows, not offset values
    toc_bytes = write_utf(tname, tcols, rows)
    content_off = al(toc_off + 0x10 + len(toc_bytes))
    # file layout in original offset order
    order = sorted(range(len(rows)), key=lambda i: (toc[i]['FileOffset'] if i < len(toc) else 1 << 62, i))
    pos = content_off; layout = {}
    for i in order:
        layout[i] = pos; pos = al(pos + len(blobs[i])) if i != order[-1] else pos + len(blobs[i])
    end = pos
    for i in range(len(rows)): rows[i]['FileOffset'] = layout[i] - toc_off
    toc_bytes = write_utf(tname, tcols, rows)
    content_size = al(end) - content_off if end % align else end - content_off
    hdr2 = dict(hdr); hdr2['ContentOffset'] = content_off; hdr2['ContentSize'] = content_size; hdr2['TocSize'] = len(toc_bytes) + 0x10
    hdr2['Files'] = len(rows)
    if new_files: hdr2['Sorted'] = 0
    hdr2['EnabledPackedSize'] = hdr['EnabledPackedSize'] + sum(len(b) for b in blobs[len(toc):])
    hdr2['EnabledDataSize'] = hdr['EnabledDataSize'] + sum(len(b) for b in blobs[len(toc):])
    hdr_bytes = write_utf(hname, hcols, [hdr2])
    out = bytearray(al(end) if end % align else end)
    out[0:16] = d[0:4] + d[4:8] + struct.pack('<Q', len(hdr_bytes))
    out[0x10:0x10 + len(hdr_bytes)] = unmask(hdr_bytes)
    gap = 0x10 + len(hdr_bytes)
    out[gap:toc_off] = d[gap:toc_off]  # preserve original filler between header and TOC
    out[toc_off:toc_off + 16] = d[toc_off:toc_off + 8] + struct.pack('<Q', len(toc_bytes))
    out[toc_off + 0x10:toc_off + 0x10 + len(toc_bytes)] = unmask(toc_bytes)
    for i in range(len(rows)): out[layout[i]:layout[i] + len(blobs[i])] = blobs[i]
    open(out_path, 'wb').write(bytes(out))
    return dict(files=len(rows), size=len(out), content_off=content_off)
