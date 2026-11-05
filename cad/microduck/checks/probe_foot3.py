import numpy as np, trimesh
from scipy.cluster.hierarchy import fcluster, linkage
U="/Users/hemangvora/OpenDuck/upstream/Open_Duck_Mini/print/"
ft=trimesh.load(U+"foot_top.stl",force='mesh'); fs=trimesh.load(U+"foot_side.stl",force='mesh')
both=trimesh.util.concatenate([ft,fs])
for side,y0,d,face in [("inner/foot_side",40,1,67.15),("outer/foot_top",140,-1,114.05)]:
    pts=[]
    for x in np.arange(-56,48.5,0.5):
        O=np.array([[x,y0,z] for z in np.arange(-254,-207,0.5)]); D=np.tile([0,d,0],(len(O),1))
        loc,ri,_=both.ray.intersects_location(O,D,multiple_hits=False)
        first=np.full(len(O),np.nan)
        if len(ri): loc=np.asarray(loc).reshape(-1,3); first[ri]=loc[:,1]
        # inside the cheek silhouette (first hit exists) but the first hit is deeper than the face by > 0.6 mm -> hole/recess
        for k,z in enumerate(O[:,2]):
            if not np.isnan(first[k]) and abs(first[k]-face)>0.6: pts.append((x,z,first[k]))
    P=np.array(pts)
    lab=fcluster(linkage(P[:,:2],'single'),1.0,'distance')
    print("==",side)
    for k in np.unique(lab):
        q=P[lab==k]
        if len(q)<4: continue
        print(f"  feature x[{q[:,0].min():6.1f},{q[:,0].max():6.1f}] z[{q[:,1].min():7.1f},{q[:,1].max():7.1f}] depth to y {np.round(np.median(q[:,2]),1)} n{len(q)}")
