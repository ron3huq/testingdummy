"""Rebuild FULL8 RC27 (V30 + RC26 merge for V19.1) from pinned release inputs and verify every file.

Inputs (cwd): V30.apk (extracted from the release rar), RC26.zip, rc27/RC27-DELTA.zip
Output: payload/ and out/FULL8-RC27-V30-MERGE-part{1,2}.zip
"""
import hashlib, json, zipfile, shutil, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STAGE = Path('payload'); OUT = Path('out')
BIG = {'assets/pc0010_mobile_and.ucas', 'assets/dt500_mobile_all.cpk', 'assets/card-art/pack.bin',
       'assets/gateway-release/livedata/pc3700_mobile_and.ucas',
       'assets/gateway-release/custom-resources/legends-v10/pc3700_mobile_and.ucas'}
STORE = ('.ucas', '.cpk', '.bin', '.imy', '.png', '.jpg', '.webp', '.mp4', '.webm', '.onnx', '.wasm', '.gz', '.zlib')

def fsha(p, algo='sha256'):
    h = hashlib.new(algo)
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''): h.update(c)
    return h.hexdigest()

def main():
    inv = json.loads((HERE / 'payload-inventory.json').read_text())['files']
    src = json.loads((HERE / 'sources.json').read_text())
    apk = zipfile.ZipFile('V30.apk'); rc = zipfile.ZipFile('RC26.zip'); delta = zipfile.ZipFile(HERE / 'RC27-DELTA.zip')
    STAGE.mkdir(exist_ok=False)
    for row in inv:
        p = row['path']; dst = STAGE / p; dst.parent.mkdir(parents=True, exist_ok=True); kind = src[p]
        if kind == 'v30': data_src = (apk, p)
        elif kind == 'rc26': data_src = (rc, p)
        elif kind == 'delta':
            name = 'dt870_merged.cpk' if p.endswith(('dt870_mobile_and.cpk', 'dt870_ui74_mobile_and.cpk')) else p
            data_src = (delta, name)
        elif kind == 'generated': continue
        else: raise ValueError(kind)
        with data_src[0].open(data_src[1]) as fi, open(dst, 'wb') as fo: shutil.copyfileobj(fi, fo, 1 << 20)
    # app.imy = V30 app.imy + rc26_hook.pyc (V30 _protected_runtime unchanged)
    hook = delta.read('rc26_hook.pyc')
    with apk.open('assets/chaquopy/app.imy') as f: (OUT / 'v30-app.imy').write_bytes(f.read())
    app = STAGE / 'assets/chaquopy/app.imy'
    with zipfile.ZipFile(OUT / 'v30-app.imy') as zi, zipfile.ZipFile(app, 'w') as zo:
        infos = zi.infolist()
        for info in infos: zo.writestr(info, zi.read(info), compress_type=info.compress_type)
        t = zipfile.ZipInfo('rc26_hook.pyc', infos[-1].date_time); t.compress_type = zipfile.ZIP_DEFLATED; t.external_attr = infos[-1].external_attr
        zo.writestr(t, hook)
    with zipfile.ZipFile(app) as z, zipfile.ZipFile(OUT / 'v30-app.imy') as v:
        assert z.testzip() is None and all(z.read(n) == v.read(n) for n in v.namelist()) and z.read('rc26_hook.pyc') == hook
    (OUT / 'v30-app.imy').unlink()
    bj = json.loads(apk.read('assets/chaquopy/build.json')); bj['assets']['app.imy'] = fsha(app, 'sha1')
    (STAGE / 'assets/chaquopy/build.json').write_text(json.dumps(bj, indent=2))
    # verify every file
    expected = {r['path'] for r in inv}
    actual = {p.relative_to(STAGE).as_posix() for p in STAGE.rglob('*') if p.is_file()}
    assert actual == expected, (sorted(actual - expected)[:5], sorted(expected - actual)[:5])
    generated = {'assets/chaquopy/app.imy', 'assets/chaquopy/build.json'}
    for r in inv:
        if r['path'] in generated: continue
        p = STAGE / r['path']; assert p.stat().st_size == r['bytes'] and fsha(p) == r['sha256'], r['path']
    apk.close(); rc.close()
    if '--artifact' in sys.argv:
        # two artifact folders, each with assets/... at its root, ready to copy over the APK
        data = Path('payload-data')
        for r in sorted(BIG):
            if not (STAGE / r).exists(): continue
            d = data / r; d.parent.mkdir(parents=True, exist_ok=True); shutil.move(str(STAGE / r), str(d))
        for m in ['README-VI.md', 'payload-inventory.json']: shutil.copy2(HERE / m, STAGE / m)
        shutil.copytree(HERE / 'source', STAGE / 'source/full8-rc27-v30-merge')
        print(json.dumps(dict(passed=True, files=len(inv), phone_verified=False)))
        return
    # package
    for part, sel in [(1, lambda r: r not in BIG), (2, lambda r: r in BIG)]:
        out = OUT / f'FULL8-RC27-V30-MERGE-part{part}.zip'
        with zipfile.ZipFile(out, 'w', allowZip64=True) as z:
            for r in sorted(expected):
                if not sel(r): continue
                z.write(STAGE / r, r, compress_type=zipfile.ZIP_STORED if r.endswith(STORE) else zipfile.ZIP_DEFLATED)
            if part == 1:
                for m in ['README-VI.md', 'payload-inventory.json']: z.write(HERE / m, m)
                for m in sorted((HERE / 'source').iterdir()): z.write(m, 'source/full8-rc27-v30-merge/' + m.name)
        with zipfile.ZipFile(out) as z: assert z.testzip() is None
        print(out, out.stat().st_size, fsha(out))
    print(json.dumps(dict(passed=True, files=len(inv), phone_verified=False)))

if __name__ == '__main__':
    main()
