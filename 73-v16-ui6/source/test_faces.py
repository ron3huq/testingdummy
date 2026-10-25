from pathlib import Path
import json
P=Path('/workspace/ronaldo-work/73-ui6');s=Path('/workspace/testingdummy/efootxi-1.3.2/player-faces-v25/source/native_harness.py').read_text().replace("ep=Path('/workspace/ronaldo-work/apk/lib/arm64-v8a/libUE4.so')","ep=Path('/workspace/ronaldo-work/73-inspect/v16-meta/lib/arm64-v8a/libUE4.so')").replace("r/'libnoodle_hair.so'","r/'payload/work/tools/libnoodle_hair.so'");exec(s)
proof=[];with_texture=True
for src,dst,profile in[(106734785925546,89138556572074,'NX27'),(88044950524330,89136418985303,'NV17')]:
 for face_id in ['4522','4522ep00v0313','4522lg00v0000']:
  a=request(src,face_id);b=request(dst,face_id)
  wanted=lambda es:[e for e in es if e[0]in['mesh','path']]
  assert wanted(a)==wanted(b),(src,dst,face_id,wanted(a),wanted(b));assert any(e[0]=='mesh'and'SK_'+profile in e[1]for e in b)
 for pid in[dst-1,dst+1,dst+(1<<32),dst&0xffffffff]:
  if pid in[89136418985303,89138556572074]:continue
  b=request(pid,'4522');assert not any(e[0]=='mesh'and'SK_'+profile in e[1]for e in b),(pid,b)
 proof.append({'source':src,'destination':dst,'profile':profile,'three_face_variants_same_native_paths':True,'full64_collision_rejected':True})
(P/'face-copy-validation.json').write_text(json.dumps({'passed':True,'actual_compiled_arm64_hooks':True,'engine_callbacks_modeled':True,'copies':proof,'device_tested':False},indent=2));print('FACE_COPIES_PASS')
