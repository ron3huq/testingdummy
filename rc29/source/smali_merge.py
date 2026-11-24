"""Method-level 3-way merge of smali files: base, ours (rc26), theirs (v30)."""
import re, sys

def split(text):
    """Return (header_lines_list, ordered list of (key, block)) where key is member signature."""
    lines = text.splitlines(keepends=True)
    items = []; cur = None; buf = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith('.method '):
            sig = ln.strip().split()[-1]
            j = i
            while not lines[j].startswith('.end method'): j += 1
            items.append(('M:' + sig, ''.join(lines[i:j + 1]), ln))
            i = j + 1; continue
        if ln.startswith('.field '):
            name = ln.split(' = ')[0].strip().split()[-1]
            blk = [ln]; k = i + 1
            # field annotations
            if k < len(lines) and lines[k].startswith('    .annotation'):
                while not lines[k].startswith('.end field'): blk.append(lines[k]); k += 1
                blk.append(lines[k]); k += 1
            items.append(('F:' + name, ''.join(blk), ln)); i = k; continue
        items.append(('T:%d' % i, ln, ln)); i += 1
    return items

def keyed(items):
    return {k: b for k, b, _ in items if not k.startswith('T:')}

def merge(base, ours, theirs):
    B, O, T = keyed(split(base)), keyed(split(ours)), keyed(split(theirs))
    conflicts = []
    out = {}
    for k in set(B) | set(O) | set(T):
        b, o, t = B.get(k), O.get(k), T.get(k)
        if o == t: out[k] = o
        elif o == b: out[k] = t
        elif t == b: out[k] = o
        else: out[k] = ('CONFLICT', o, t); conflicts.append(k)
    # emit using theirs ordering, then ours-only members
    res = []; emitted = set()
    titems = split(theirs)
    for k, b, _ in titems:
        if k.startswith('T:'): res.append(b); continue
        v = out.get(k)
        emitted.add(k)
        if v is None: continue
        res.append(v if isinstance(v, str) else '#CONFLICT ' + k + '\n')
    extra = [k for k, _, _ in split(ours) if not k.startswith('T:') and k not in emitted and out.get(k)]
    for k in extra:
        v = out[k]
        res.append('\n' + (v if isinstance(v, str) else '#CONFLICT ' + k + '\n'))
    return ''.join(res), conflicts, out

if __name__ == '__main__':
    base, ours, theirs, dest = sys.argv[1:5]
    text, conflicts, out = merge(*(open(p).read() for p in (base, ours, theirs)))
    open(dest, 'w').write(text)
    print(dest.split('/')[-1], 'conflicts:', conflicts)

LABEL = re.compile(r':((?:cond|goto|try_start|try_end|catch|catchall|catchall|pswitch|sswitch|array|pswitch_data|sswitch_data)_[0-9a-f]+)\b')
def normalize(block):
    if block is None: return None
    lines = [l for l in block.splitlines(keepends=True) if not l.startswith('    .line ')]
    text = ''.join(lines)
    mapping = {}
    def sub(m):
        n = m.group(1)
        if n not in mapping:
            kind = n.rsplit('_', 1)[0]
            mapping[n] = '%s_n%d' % (kind, len(mapping))
        return ':' + mapping[n]
    return LABEL.sub(sub, text)

def merge_norm(base, ours, theirs):
    import subprocess, tempfile, os
    B, O, T = [{k: normalize(v) for k, v in keyed(split(x)).items()} for x in (base, ours, theirs)]
    out = {}; conflicts = []
    for k in set(B) | set(O) | set(T):
        b, o, t = B.get(k), O.get(k), T.get(k)
        if o == t: out[k] = o
        elif o == b: out[k] = t
        elif t == b: out[k] = o
        elif None in (b, o, t): out[k] = ('CONFLICT', o, t); conflicts.append(k)
        else:
            with tempfile.TemporaryDirectory() as d:
                for n, v in (('b', b), ('o', o), ('t', t)): open(os.path.join(d, n), 'w').write(v)
                r = subprocess.run(['git', 'merge-file', '-p', os.path.join(d, 'o'), os.path.join(d, 'b'), os.path.join(d, 't')], capture_output=True, text=True)
                out[k] = r.stdout
                if r.returncode: conflicts.append(k)
    res = []; emitted = set()
    for k, b, _ in split(theirs):
        if k.startswith('T:'): res.append(b); continue
        emitted.add(k); v = out.get(k)
        if v: res.append(v if isinstance(v, str) else '#CONFLICT ' + k + '\n')
    for k, _, _ in split(ours):
        if not k.startswith('T:') and k not in emitted and out.get(k):
            v = out[k]; res.append('\n' + (v if isinstance(v, str) else '#CONFLICT ' + k + '\n'))
    return ''.join(res), conflicts
