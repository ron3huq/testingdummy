"""Validate that prior host motion evidence belongs to this exact cooked mesh."""
from pathlib import Path
import sys,json,hashlib
root=Path(sys.argv[1]);sys.path.insert(0,str(root/'source/repair-full8-rc4'))
from iostore import Toc
report=json.loads((Path(__file__).parent/'host-motion-report.json').read_text());toc=Toc(str(root/'assets/gateway-release/livedata/pc9385_mobile_and.utoc'));raw=toc.read(toc.files[report['asset_path']]);assert hashlib.sha256(raw).hexdigest()==report['asset_sha256'];assert report['phone_verified']is False
(root/'validation/full8-rc10-host-motion.json').write_text(json.dumps(report,indent=2));print('Host motion evidence matches actual cooked mesh; NOT an Android test.')
