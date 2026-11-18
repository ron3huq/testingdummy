"""Make card 88044950524330 use exactly the face of 88042803047215 (profile NR17) in libnoodle_hair.so.

Every native decision keyed on 88044950524330 (A) is changed to behave like 88042803047215 (B):
  * A-only special cases (NV17 family) are neutralised (constant A -> A+1, a card id that is never used);
  * B-only cases also accept A, through small trampolines in the existing RC8 stub page (0x1010d0..0x1011fc, udf filler);
  * cases already grouping A and B are left alone.
"""
import struct, sys, hashlib
from pathlib import Path
src, dst = sys.argv[1:3]
b = bytearray(Path(src).read_bytes())
EXPECT = 'deb6cfcbc718e8d8da3f40abc921ff03e434453edff8d00940b058682d5db29a'
assert hashlib.sha256(b).hexdigest() == EXPECT, 'unexpected libnoodle_hair.so'
A = 88044950524330; B = 88042803047215
# segments: (vaddr, offset, size)
SEGS = [(0x0, 0x0, 0x32bc), (0x132bc, 0x32bc, 0xc4b0), (0x100000, 0x40000, 0x12d4)]
def off(va):
    for v, o, n in SEGS:
        if v <= va < v + n: return o + va - v
    raise ValueError(hex(va))
def rd(va): return struct.unpack_from('<I', b, off(va))[0]
def wr(va, w): struct.pack_into('<I', b, off(va), w)
def B_(at, to): return 0x14000000 | (((to - at) >> 2) & 0x3ffffff)
def BC(at, to, cond): return 0x54000000 | ((((to - at) >> 2) & 0x7ffff) << 5) | cond
EQ, NE = 0, 1
def movz(rd_, imm, hw): return 0xD2800000 | (hw << 21) | (imm << 5) | rd_
def movk(rd_, imm, hw): return 0xF2800000 | (hw << 21) | (imm << 5) | rd_
def cmp(rn, rm): return 0xEB000000 | (rm << 16) | (rn << 5) | 31
def load(rd_, v): return [movz(rd_, v & 0xffff, 0), movk(rd_, (v >> 16) & 0xffff, 1), movk(rd_, (v >> 32) & 0xffff, 2)]

# 1) neutralise A-only special cases: movz Xn,#0x11aa -> #0x11ab at these addresses
for at in (0x14f84, 0x15b50, 0x1610c, 0x1b208, 0x1cec0):
    w = rd(at); assert (w & 0xFFE00000) == 0xD2800000 and ((w >> 5) & 0xffff) == 0x11aa, hex(at)
    assert rd(at + 4) == movk(w & 31, 0x9000, 1) and rd(at + 8) == movk(w & 31, 0x5013, 2), hex(at)
    wr(at, (w & ~(0xffff << 5)) | (0x11ab << 5))

# 2) trampolines
T = 0x1010d0; END = 0x1011fc
for va in range(T, END, 4): assert rd(va) == 0, hex(va)  # udf #0 filler
code = []
def emit(words, at):
    for i, w in enumerate(words): wr(at + 4 * i, w)
    return at + 4 * len(words)
pc = T
# profile_for leaf: 0x1a82c cmp x0,x8(A) ; 0x1a830 b.ne default -> A must return NR17 (0x1ab84)
assert rd(0x1a830) == BC(0x1a830, 0x1abb4, NE)
t1 = pc
pc = emit([BC(pc, 0x1ab84, EQ), B_(pc + 4, 0x1abb4)], pc)
wr(0x1a830, B_(0x1a830, t1))
# 0x19864 cmp x24,x8(B) ; 0x19868 b.eq 0x19a44 ; fallthrough 0x1986c
assert rd(0x19864) == cmp(24, 8) and rd(0x19868) == BC(0x19868, 0x19a44, EQ)
t2 = pc
seq = [BC(pc, 0x19a44, EQ)] + load(8, A) + [cmp(24, 8)]
seq.append(BC(pc + 4 * len(seq), 0x19a44, EQ)); seq.append(B_(pc + 4 * len(seq), 0x1986c))
pc = emit(seq, pc)
wr(0x19868, B_(0x19868, t2))
# 0x1d2e4 cmp x27,x8(B) ; 0x1d2e8 b.ne 0x1d974 ; match falls to 0x1d2ec
assert rd(0x1d2e4) == cmp(27, 8) and rd(0x1d2e8) == BC(0x1d2e8, 0x1d974, NE)
t3 = pc
seq = [BC(pc, 0x1d2ec, EQ)] + load(8, A) + [cmp(27, 8)]
seq.append(BC(pc + 4 * len(seq), 0x1d2ec, EQ)); seq.append(B_(pc + 4 * len(seq), 0x1d974))
pc = emit(seq, pc)
wr(0x1d2e8, B_(0x1d2e8, t3))
assert pc <= END
Path(dst).write_bytes(b)
print('patched', hex(T), '..', hex(pc), hashlib.sha256(b).hexdigest())
