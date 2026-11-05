import numpy as np, trimesh
import asm
asm.pose(); tt={mn:t for mn,b,t in asm.geoms(["trunk_assembly"])}["trunk_top"]
for z in [-9.5,-8,-7]:
    s=tt.section([0,0,z],[0,0,1])
    if s is None: print(z,"none"); continue
    V=s.vertices; V=V[(V[:,0]<-40)&(np.abs(V[:,1])<30)]
    if len(V):
        # cluster in xy
        from scipy.cluster.hierarchy import fcluster, linkage
        lab=fcluster(linkage(V[:,:2],'single'),3,'distance')
        for k in np.unique(lab):
            q=V[lab==k][:,:2]; print(f"   cluster x[{q[:,0].min():.1f},{q[:,0].max():.1f}] y[{q[:,1].min():.1f},{q[:,1].max():.1f}] n{len(q)}")
z=tt.vertices[:,2]; sel=tt.vertices[(tt.vertices[:,0]<-40)&(np.abs(tt.vertices[:,1])<30)]
print("max z of trunk_top in rear zone", sel[:,2].max().round(2), "; distinct top z levels", np.unique(sel[:,2].round(1))[-8:])
