"""Restore the pinned v16 source container that is used as a read-only baseline."""
from pathlib import Path
import hashlib,zipfile
root=Path(__file__).resolve().parent.parent;src=root.parent/'player-faces-v16/Faces-v16-13-cards.zip';assert hashlib.sha256(src.read_bytes()).hexdigest()=='1bc1baaa90b4ac618c46c07651d5fb174c7cd8e1bd38ebd320e0437719ae2732'
dest=root.parent/'player-faces-v16/container';dest.mkdir(exist_ok=True)
with zipfile.ZipFile(src) as z:
 for ext in ['pak','utoc','ucas']:(dest/('pc9298_mobile_and.'+ext)).write_bytes(z.read('livedata/pc9298_mobile_and.'+ext))
print('PINNED_V16_SOURCE_CONTAINER_RESTORED')
