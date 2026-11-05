import numpy as np, trimesh
import asm
from common import *
asm.pose(); tt={mn:t for mn,b,t in asm.geoms(["trunk_assembly"])}["trunk_top"]
deck=L(S+"body_deck.stl")
xs=np.arange(-88,-43,4); ys=np.arange(-26,27,4)
print("first hit z going down from z=0 (trunk_top) ; '.' = none")
print("      y:"+"".join(f"{y:6d}" for y in ys))
for x in xs:
    O=np.array([[x,y,0.0] for y in ys]); D=np.tile([0,0,-1.0],(len(O),1))
    loc,ri,_=tt.ray.intersects_location(O,D)
    row=[]
    for k in range(len(ys)):
        z=loc[ri==k][:,2]; row.append(f"{z.max():6.1f}" if len(z) else "     .")
    print(f"x{x:5d}  "+"".join(row))
print("deck underside first hit going up from z=-30:")
for x in xs[::3]:
    O=np.array([[x,y,-30.0] for y in ys]); D=np.tile([0,0,1.0],(len(O),1))
    loc,ri,_=deck.ray.intersects_location(O,D)
    print(f"x{x:5d}  "+"".join((f"{loc[ri==k][:,2].min():6.1f}" if (ri==k).any() else "     .") for k in range(len(ys))))
