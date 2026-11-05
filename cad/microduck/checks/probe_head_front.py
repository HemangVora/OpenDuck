import numpy as np, trimesh, asm
from common import *
rs=L("roll_servo.stl"); rm=L("head_roll_mount.stl")
for n,t in [("roll_servo",rs),("roll_mount",rm)]:
    print(n,"bounds",t.bounds.round(1).tolist())
    V=t.vertices
    for x0 in [60,70,80,90,100]:
        s=V[V[:,0]>=x0]; print(f"   x>={x0}: z[{s[:,2].min():.1f},{s[:,2].max():.1f}] |y|<={np.abs(s[:,1]).max():.1f}" if len(s) else f"   x>={x0}: none")
Pm=np.load("head_mover_pts.npy"); s=Pm[Pm[:,0]>55]; print("movers x>55: n",len(s), "x max",Pm[:,0].max().round(1))
asm.pose(); A={mn:t for mn,b,t in asm.geoms(["foot_assembly"])}; B={mn:t for mn,b,t in asm.geoms(["foot_assembly_2"])}
TL=asm.body_T("foot_assembly"); TR=asm.body_T("foot_assembly_2"); M=TR@np.linalg.inv(TL)
print("right foot = M * left foot; M rot:\n",M[:3,:3].round(3)," trans",M[:3,3].round(1))
for n in ["foot_top","foot_side"]: print(n,"right bounds",B[n].bounds.round(1).tolist())
