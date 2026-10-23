from pathlib import Path
import hashlib,zipfile
out=Path(__file__).resolve().parent.parent;src=out.parent/'player-faces-v16/Faces-v16-13-cards.zip'
assert hashlib.sha256(src.read_bytes()).hexdigest()=='1bc1baaa90b4ac618c46c07651d5fb174c7cd8e1bd38ebd320e0437719ae2732'
(out/'container').mkdir(exist_ok=True)
with zipfile.ZipFile(src) as z:
 for ext in ['pak','utoc','ucas']:(out/'container'/('pc9298_mobile_and.'+ext)).write_bytes(z.read('livedata/pc9298_mobile_and.'+ext))
print('PINNED_V16_ASSETS_RESTORED_BYTE_IDENTICAL')
