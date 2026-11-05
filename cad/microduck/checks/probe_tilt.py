import numpy as np, trimesh
from common import *
U="/Users/hemangvora/OpenDuck/upstream/Open_Duck_Mini/print/"
NEW=trimesh.util.concatenate([L(S+"md_foot_top.stl"),L(S+"md_foot_side.stl")]); tpu=L(U+"foot_bottom_tpu.stl")
V=tpu.vertices; b=V[V[:,2]<tpu.bounds[0][2]+0.3]; print("TPU bottom face y range",b[:,1].min().round(2),b[:,1].max().round(2),"x range",b[:,0].min().round(2),b[:,0].max().round(2))
for a,sign in [(33.0,-1),(34.5,1)]:
    R=trimesh.transformations.rotation_matrix(sign*np.radians(a),[1,0,0]); W=(np.c_[NEW.vertices,np.ones(len(NEW.vertices))]@R.T)[:,:3]
    i=W[:,2].argmin(); print(f"tilt {a}: lowest new vertex (unrotated) {NEW.vertices[i].round(2)}")
