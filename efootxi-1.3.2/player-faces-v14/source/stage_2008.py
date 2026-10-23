from pathlib import Path
import shutil
out=Path(__file__).resolve().parent.parent
shutil.copytree(out/'container',out/'2008-container',dirs_exist_ok=True)
shutil.copyfile(out/'build-report.json',out/'2008-build-report.json')
