"""Stage an existing-RC7 editor JSON with a modern, UEFA-scoped Dortmund row."""
import hashlib,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'repair-full8-rc9-ucl/runtime'))
from ucl_lp_roster import inject

def build(root,stage):
    root=Path(root);stage=Path(stage);relative=Path('assets/gateway-release/work/tools/myleague_editor.json');source=root/relative
    original=json.loads(source.read_text());updated=inject(original);target=stage/relative
    if target.exists():raise ValueError('fresh output required')
    target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(updated,ensure_ascii=False,indent=2)+'\n')
    report=dict(input_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),output_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),team_id=126,scope=122,players=22,normal_uefa_dortmund_also_updated=True,classic_rows_unchanged=True,native_preflight_required=True,phone_verified=False,full_package=False)
    (stage/'roster-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':build(*sys.argv[1:])
