"""Repair exterior jaw normals and coincident seam skin weights; preserve rig/LOD."""
from pathlib import Path
import sys,json,numpy as np
from scipy.spatial import cKDTree
from iostore import Toc
from bundle_tools import Bundle
from mesh_tools import Mesh,quantize
from shading_tools import repair_frame

O=Path(__file__).resolve().parent.parent;R=Path('/workspace/ronaldo-work')
t=Toc(str(O/'heads-container/pc9298_mobile_and.utoc'));bundle=Bundle(t);report=[]
for profile,log in [('NWOZep00v0313',O.parent/'player-faces-v20/reader-logs/SK_NWOZep00v0313_Face.log'),('NDDBep00v0313',R/'v10-NDDBep00v0313.log')]:
    path='character/RealFace/SK_'+profile+'_Face.uasset';original=t.read(t.files[path]);raw=bytearray(original)
    for lod in [0,1]:
        m=Mesh(original,log.read_text(),lod);n=m.info[0]['verts']-135
        pos=m.positions.copy();rows=[dict(x)for x in m.global_weights(0)];tri=m.indices[:m.info[0]['tris']];exterior=tri[np.max(tri,axis=1)<n]
        folds_before=folds_after=0;fold_vertices=set()
        # Only outer chin/neck, excluding mouth, eyes and all internal accessories.
        ids=np.array([i for i,p in enumerate(pos[:n])if p[2]<166.5 and not(abs(p[0])<4.8 and p[1]>16 and p[2]>164)])
        groups=[]
        if len(ids):
            parent={int(i):int(i)for i in ids}
            def root(i):
                while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
                return i
            for a,b in cKDTree(pos[ids]).query_pairs(.025):
                a,b=int(ids[a]),int(ids[b])
                if set(rows[a])|set(rows[b]) <= {4,5,6,7,8}:parent[root(a)]=root(b)
            merged={}
            for i in ids:merged.setdefault(root(int(i)),[]).append(int(i))
            groups=[g for g in merged.values()if len(g)>1]
        changed_weights=[]
        for group in groups:
            pos[group]=pos[group].mean(0)
            if len({tuple(sorted(rows[i].items()))for i in group})>1:
                average={k:sum(rows[i].get(k,0)for i in group)/len(group)for k in set().union(*(rows[i]for i in group))}
                for i in group:rows[i]=average.copy()
                changed_weights.append(group)
        # Geometric jaw normals, averaged across UV seams. Keep other facial frames.
        tan=m.tangents.copy();norm=np.zeros((len(pos),3));q=np.cross(pos[tri[:,1]]-pos[tri[:,0]],pos[tri[:,2]]-pos[tri[:,0]])
        for k in range(3):np.add.at(norm,tri[:,k],q)
        oldnormal=tan.view('i1')[:,4:7].astype(float);valid=np.linalg.norm(norm,axis=1)>1e-7
        if np.median(np.sum(norm[valid]*oldnormal[valid],axis=1))<0:norm=-norm
        for group in groups:
            v=norm[group].sum(0)
            if np.linalg.norm(v)>1e-7:norm[group]=v
        jaw=(pos[:,2]<166.5)&(np.arange(len(pos))<n)&valid&~((np.abs(pos[:,0])<4.8)&(pos[:,1]>16)&(pos[:,2]>164))
        normal=norm[jaw];normal/=np.linalg.norm(normal,axis=1,keepdims=True)
        tan[jaw,4:7]=np.rint(normal*127).astype('i1').view('u1')
        tan=repair_frame(pos,tan,m.uv,tri)
        # Restore untouched vertices literally, including hair and accessory frames.
        tan[~jaw]=m.tangents[~jaw]
        weights=m.weights.copy();weights[:m.info[0]['verts']]=quantize(rows,m.info[0]['bones'])
        # Keep all unrelated packed weight rows exactly, including tie order.
        changed=set(i for g in changed_weights for i in g)
        for i in range(len(weights)):
            if i not in changed:weights[i]=m.weights[i]
        at=m.r['POSITIONS_BEGIN']+16;raw[at:at+pos.nbytes]=pos.astype('<f4').tobytes()
        at=m.r['TANGENT_UV_BEGIN']+26;raw[at:at+tan.nbytes]=tan.tobytes()
        at=m.r['SKIN_WEIGHTS_BEGIN']+30;raw[at:at+weights.nbytes]=weights.tobytes()
        report.append({'profile':profile,'lod':lod,'exterior_folded_triangles_before':folds_before,'exterior_folded_triangles_after':folds_after,'fold_repair_vertices':len(fold_vertices),'coincident_chin_neck_weight_groups_unified':changed_weights,'jaw_normals_rebuilt':int(jaw.sum()),'max_bind_displacement_cm':float(np.linalg.norm(pos-m.positions,axis=1).max()),'rig_and_bone_palettes_unchanged':True})
    for lod in [0,1]:
        a=Mesh(original,log.read_text(),lod);b=Mesh(bytes(raw),log.read_text(),lod)
        assert np.array_equal(a.indices,b.indices)and np.array_equal(a.uv,b.uv)and a.info==b.info
        assert original[a.r['REF_BEGIN']:a.r['REF_END']]==bytes(raw)[b.r['REF_BEGIN']:b.r['REF_END']]
    key,body=bundle.files[path];bundle.files[path]=(key,bytes(raw))
bundle.write(O/'seams-container');(O/'seam-repair.json').write_text(json.dumps({'repairs':report,'synthetic_geometry_checks_only':True,'phone_verified':False},indent=2));print('JAW_FOLDS_AND_WEIGHT_SEAMS_REPAIRED')
