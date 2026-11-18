"""Tune ball flight constants (ball.o inside dt270 common/match/constant/constant_match.bin).

The engine fills its ball-physics struct only from this table (the C++ default is all zeros), so these values
drive every kicked ball.  Field offsets (inside ball.o) were mapped from libUE4's JSON reader for ball.json.

Usage: ball_tune.py dt270_in.cpk dt270_out.cpk [preset]
"""
import struct, sys, zlib, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import cpk

# offsets inside ball.o (scalars only)
FIELDS = {
    'magnusRate': 0x98,
    'nonSpinMax': 0xac, 'nonSpinMin': 0xb0, 'nonSpinRate': 0xb4,
    'nonSpinTopDownDecRate': 0xb8, 'nonSpinTopRiseDecRate': 0xbc,
    'topSpinChangeSpeed': 0xf4, 'topSpinDownDecRate': 0xf8, 'topSpinRiseDecRate': 0xfc,
}
ORIGINAL = {'magnusRate': 0.035, 'nonSpinMax': 105.0, 'nonSpinMin': 45.0, 'nonSpinRate': 1.0,
            'nonSpinTopDownDecRate': 1.0, 'nonSpinTopRiseDecRate': 1.0,
            'topSpinChangeSpeed': 0.175, 'topSpinDownDecRate': 10.0, 'topSpinRiseDecRate': 1.0}
PRESETS = {
    # Knuckle (non-spin) shots: wobble more, over a wider speed range, climb higher and then drop hard.
    # Dipping (top-spin) shots: climb a bit higher and dive harder.  Magnus (curl/pass bend) untouched.
    'ronaldo': {'nonSpinRate': 1.6, 'nonSpinMin': 38.0, 'nonSpinMax': 125.0,
                'nonSpinTopRiseDecRate': 0.75, 'nonSpinTopDownDecRate': 5.0,
                'topSpinRiseDecRate': 0.8, 'topSpinDownDecRate': 13.0},
    'original': {},
}
NAME = 'common/match/constant/constant_match.bin'

def patch_table(raw_bin, values):
    assert raw_bin[:8] == b'\xff QWESYS'
    cs, us = struct.unpack_from('<II', raw_bin, 8)
    u = bytearray(zlib.decompress(raw_bin[16:16 + cs])); assert len(u) == us
    n = struct.unpack_from('<I', u, 0)[0]
    entries = [struct.unpack_from('<III', u, 8 + 12 * i) for i in range(n)]
    names = {u[e[2]:u.index(b'\0', e[2])].decode(): e for e in entries}
    off, size, _ = names['ball.o']
    for k, v in ORIGINAL.items():
        cur = struct.unpack_from('<f', u, off + FIELDS[k])[0]
        assert abs(cur - v) < 1e-4, (k, cur, v)
    for k, v in values.items(): struct.pack_into('<f', u, off + FIELDS[k], float(v))
    c = zlib.compress(bytes(u), 9)
    return raw_bin[:8] + struct.pack('<II', len(c), len(u)) + c

def main(src, dst, preset='ronaldo'):
    d = bytearray(Path(src).read_bytes())
    hsize = struct.unpack('<Q', d[8:16])[0]
    hname, hcols, hrows = cpk.parse_schema(bytes(d[0x10:0x10 + hsize])); hdr = hrows[0]
    toc_off = hdr['TocOffset']; tsize = struct.unpack('<Q', d[toc_off + 8:toc_off + 16])[0]
    tname, tcols, toc = cpk.parse_schema(bytes(d[toc_off + 0x10:toc_off + 0x10 + tsize]))
    base = min(toc_off, hdr['ContentOffset'])
    row = next(r for r in toc if (r['DirName'] + '/' + r['FileName']) == NAME)
    start = base + row['FileOffset']; old = bytes(d[start:start + row['FileSize']])
    new = patch_table(old, PRESETS[preset])
    later = [base + r['FileOffset'] for r in toc if base + r['FileOffset'] > start]
    slot_end = min(later) if later else len(d)
    assert start + len(new) <= slot_end, 'patched table does not fit its slot'
    d[start:slot_end] = new + bytes(slot_end - start - len(new))
    # patch FileSize/ExtractSize of that row in place (UTF row data, big-endian), then re-mask
    t = bytearray(cpk.unmask(bytes(d[toc_off + 0x10:toc_off + 0x10 + tsize])))
    rows_off, = struct.unpack_from('>I', t, 8); rowlen, = struct.unpack_from('>H', t, 8 + 18)
    sizes = {0: 1, 1: 1, 2: 2, 3: 2, 4: 4, 5: 4, 6: 8, 7: 8, 8: 4, 0xA: 4, 0xB: 8}
    ri = toc.index(row); pos = 8 + rows_off + ri * rowlen
    for name, flags, const in tcols:
        if flags & 0xf0 != 0x50: continue
        n = sizes[flags & 0xf]
        if name in ('FileSize', 'ExtractSize'):
            assert n == 4 and struct.unpack_from('>I', t, pos)[0] == len(old); struct.pack_into('>I', t, pos, len(new))
        pos += n
    d[toc_off + 0x10:toc_off + 0x10 + tsize] = cpk.unmask(bytes(t))
    Path(dst).write_bytes(d)
    # read back
    h2, f2, d2 = cpk.read(dst)
    r2 = next(x for x in f2 if x['name'] == NAME); got = d2[r2['off']:r2['off'] + r2['size']]
    cs, us = struct.unpack_from('<II', got, 8); u = zlib.decompress(got[16:16 + cs])
    print(json.dumps(dict(preset=preset, values=PRESETS[preset], size=len(d)), indent=1))

if __name__ == '__main__':
    main(*sys.argv[1:])
