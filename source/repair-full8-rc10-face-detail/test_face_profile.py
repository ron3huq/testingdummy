from pathlib import Path
import os,sys,json
sys.path.insert(0,str(Path(__file__).parent.parent/'repair-full8-rc9-ucl'))
import importlib.util
helper=Path(__file__).parent.parent/'repair-full8-rc9-ucl/test_face_profile.py';spec=importlib.util.spec_from_file_location('rc9_arm64_profile_control',helper);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);Runner=module.Runner
# Loaded as a script under another module name to avoid shadowing this file.
if __name__=='__main__':
 stage=Path(os.environ.get('FACE_TEST_BUILD',str(Path(__file__).parents[2]/'.ci-face-detail')));old=Runner(stage/'rc7-noodle.so');new=Runner(stage/'face-noodle.so');ids=[106654775417922,106782819217056,88035555413452,105756321970183,123,89138556572073,89138556572075]
 for palette in range(1,7):
  assert new.call(0x101028,palette)==1;assert new.profile(89138556572074)=='R9B'+str(palette)
  for pid in ids:assert old.profile(pid)==new.profile(pid)
 for v in [0,7,255]:assert new.call(0x101028,v)==0
 print(json.dumps(dict(passed=True,actual_arm64_executed=True,palettes=6,unrelated_card_controls=len(ids),phone_verified=False)))
