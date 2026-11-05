import numpy as np, trimesh
from common import *
import asm
asm.pose(); G={mn:t for mn,b,t in asm.geoms(["trunk_assembly"])}
tt=G["trunk_top"]; print("trunk_top bounds",tt.bounds.round(1).tolist())
for n,other in [("body_deck",tt),("switch_guard",L(S+"v_switch.stl"))]:
    I=(MAN(other)^MAN(L(S+n+".stl"))).to_mesh()
    im=trimesh.Trimesh(np.asarray(I.vert_properties)[:,:3],np.asarray(I.tri_verts))
    print("==",n,"intersection total",round(im.volume,1))
    for c in sorted(im.split(only_watertight=False),key=lambda c:-abs(c.volume))[:12]:
        print("   vol %7.1f  bounds %s"%(abs(c.volume), c.bounds.round(1).tolist()))
