import sys
sys.path.insert(0,'/home/user/work/scripts')
from smali_merge import merge_norm
base,ours,theirs,dest=sys.argv[1:5]
t,c=merge_norm(*(open(p).read() for p in (base,ours,theirs)))
open(dest,'w').write(t);print(dest.split('/')[-1],'conflicts:',c)
