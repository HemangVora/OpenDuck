"""Cached sweep clouds + static head hardware, written next to this file."""
import numpy as np, trimesh, asm
asm.pose(); Th0=asm.body_T("head_assembly")
pts=[]
for r in np.linspace(-30,30,7):
  for yw in np.linspace(-160,160,17):
    for hp in [-45,0,45]:
      asm.pose({"head_roll":r,"head_yaw":yw,"head_pitch":hp}); Li=Th0@np.linalg.inv(asm.body_T("head_assembly"))
      for mn,b,t in asm.geoms(["neck_yaw_assembly","head_pitch_to_yaw","neck_pitch_assembly"]):
        V=t.vertices[::7]; pts.append((np.c_[V,np.ones(len(V))]@Li.T)[:,:3])
P=np.vstack(pts); P=P[P[:,2]>95]; np.save("head_mover_pts.npy",P.astype(np.float32)); print("head movers",len(P))
asm.pose(); T0=asm.body_T("trunk_assembly"); pts=[]
for a in np.arange(-20,21,2.5):
    asm.pose({"neck_pitch":a}); Li=T0@np.linalg.inv(asm.body_T("trunk_assembly"))
    for mn,b,t in asm.geoms(["neck_pitch_assembly"]): pts.append((np.c_[t.vertices,np.ones(len(t.vertices))]@Li.T)[:,:3])
np.save("neck_sheets_np20.npy",np.vstack(pts).astype(np.float32)); print("neck sheets",sum(len(p) for p in pts))
asm.pose(); G=[(mn,t) for mn,b,t in asm.geoms(["head_assembly"])]
[t for mn,t in G if mn=="head_roll_mount"][0].export("head_roll_mount.stl")
trimesh.util.concatenate([t for mn,t in G if mn.startswith("wj-")]).export("roll_servo.stl")
print("static head parts exported")
