"""Rebuild FULL8 RC29 (V32 Master League + RC26 for V19.1) from pinned release inputs and verify every file.

Inputs (cwd): V32.apk (extracted from the release rar), RC26.zip, rc29/RC29-DELTA.zip
Output (--artifact): payload/ (core) and payload-data/ (large gateway models), both with assets/... at the root.
Only files that differ from the V19.1 APK are included; no engine-read root asset (dt*.cpk, pc0010) is touched.
"""
import hashlib, json, zipfile, shutil, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STAGE = Path('payload'); OUT = Path('out')
BIG_BYTES = 50 << 20

def fsha(p, algo='sha256'):
    h = hashlib.new(algo)
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''): h.update(c)
    return h.hexdigest()

def main():
    inv = json.loads((HERE / 'payload-inventory.json').read_text())['files']
    src = json.loads((HERE / 'sources.json').read_text())
    apk = zipfile.ZipFile('V32.apk'); rc = zipfile.ZipFile('RC26.zip'); delta = zipfile.ZipFile(HERE / 'RC29-DELTA.zip')
    STAGE.mkdir(exist_ok=False)
    for row in inv:
        p = row['path']; dst = STAGE / p; dst.parent.mkdir(parents=True, exist_ok=True); kind = src[p]
        if kind == 'v32': data_src = (apk, p)
        elif kind == 'rc26': data_src = (rc, p)
        elif kind == 'delta':
            name = 'dt870_merged.cpk' if p.endswith(('dt870_mobile_and.cpk', 'dt870_ui74_mobile_and.cpk')) else p
            data_src = (delta, name)
        elif kind == 'generated': continue
        else: raise ValueError(kind)
        with data_src[0].open(data_src[1]) as fi, open(dst, 'wb') as fo: shutil.copyfileobj(fi, fo, 1 << 20)
    # app.imy = V32 app.imy + rc26_hook.pyc (V32 _protected_runtime unchanged)
    hooks = [(n, delta.read(n)) for n in ('rc26_hook.pyc', 'ml_isolation.pyc', 'ml_realism.pyc', 'ml_ratings.pyc', 'ml_awards.pyc', 'ml_cups.pyc', 'ml_dynamics.pyc')]
    with apk.open('assets/chaquopy/app.imy') as f: (OUT / 'v32-app.imy').write_bytes(f.read())
    app = STAGE / 'assets/chaquopy/app.imy'
    with zipfile.ZipFile(OUT / 'v32-app.imy') as zi, zipfile.ZipFile(app, 'w') as zo:
        infos = zi.infolist()
        for info in infos: zo.writestr(info, zi.read(info), compress_type=info.compress_type)
        for n, b in hooks:
            t = zipfile.ZipInfo(n, infos[-1].date_time); t.compress_type = zipfile.ZIP_DEFLATED; t.external_attr = infos[-1].external_attr
            zo.writestr(t, b)
    with zipfile.ZipFile(app) as z, zipfile.ZipFile(OUT / 'v32-app.imy') as v:
        assert z.testzip() is None and all(z.read(n) == v.read(n) for n in v.namelist()) and all(z.read(n) == b for n, b in hooks)
    (OUT / 'v32-app.imy').unlink()
    bj = json.loads(apk.read('assets/chaquopy/build.json')); bj['assets']['app.imy'] = fsha(app, 'sha1')
    (STAGE / 'assets/chaquopy/build.json').write_text(json.dumps(bj, indent=2))
    # verify every file
    expected = {r['path'] for r in inv}
    actual = {p.relative_to(STAGE).as_posix() for p in STAGE.rglob('*') if p.is_file()}
    assert actual == expected, (sorted(actual - expected)[:5], sorted(expected - actual)[:5])
    generated = {'assets/chaquopy/app.imy', 'assets/chaquopy/build.json'}
    for r in inv:
        p = STAGE / r['path']; assert p.stat().st_size == r['bytes'] and fsha(p) == r['sha256'], r['path']
    apk.close(); rc.close()
    if '--artifact' in sys.argv:
        # two artifact folders, each with assets/... at its root, ready to copy over the APK
        data = Path('payload-data')
        for r in sorted(x['path'] for x in inv if x['bytes'] > BIG_BYTES and not x['path'].startswith('assets/chaquopy/')):
            d = data / r; d.parent.mkdir(parents=True, exist_ok=True); shutil.move(str(STAGE / r), str(d))
        for m in ['README-VI.md', 'payload-inventory.json']: shutil.copy2(HERE / m, STAGE / m)
        shutil.copytree(HERE / 'source', STAGE / 'source/full8-rc29-v32-ml')
        print(json.dumps(dict(passed=True, files=len(inv), phone_verified=False)))
        return
    raise SystemExit('use --artifact')

if __name__ == '__main__':
    main()
