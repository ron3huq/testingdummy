from pathlib import Path
import importlib.util, json

r = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('hair_hints_test', r/'noodle_hair.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
results = []
for page in [4096, 16384]:
    target = 0x7103883248
    # A large hole starts too far away but ends immediately before libUE4.
    rows = [(target-0x30000000, target-0x20000000, 'r--p', 0, 'before'),
            (target-0x03800000, target+0x07000000, 'r-xp', 0, 'libUE4.so')]
    old = [((a[1]+page-1)&~(page-1)) for a,b in zip(rows,rows[1:])
           if ((a[1]+page-1)&~(page-1))+page <= b[0]
           and abs(((a[1]+page-1)&~(page-1))-target)<(1<<27)-page]
    hints = m.trampoline_hints(rows, target, page)
    assert old == [] and hints
    for hint in hints:
        assert hint%page == 0 and rows[0][1] <= hint and hint+page <= rows[1][0]
        m.branch(target, hint)
    assert not m.trampoline_hints([(target-4096,target+4096,'r-xp',0,'only')],target,page)
    # No MAP_FIXED: never overwrite any existing memory mapping.
    results.append({'page_size':page,'old_hints':old,'new_hints':[hex(x)for x in hints]})
assert 'allocated = libc.mmap(hint,page,3,0x22,-1,0)' in (r/'noodle_hair.py').read_text()
(r.parent/'trampoline-validation.json').write_text(json.dumps({'status':'WHOLE_GAP_INTERSECTION_PASS','cases':results,'phone_allocation_verified':False},indent=2))
print('WHOLE_GAP_INTERSECTION_PASS')
