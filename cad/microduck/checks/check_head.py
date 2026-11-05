import numpy as np, trimesh
from scipy.spatial import cKDTree
from common import *
PARTS=["head_shell","head_tray","head_jaw","eye_bezel","head_chassis","tof_tab"]
VIT=["v_sg90_jaw","v_radxa","v_buck","v_camera","v_tof"]
print("== parts (want manifold=True pieces=1)")
parts={n:solid_report(n,L(S+n+".stl")) for n in PARTS}
vit={n:L(S+n+".stl") for n in VIT}
static={"roll_mount":L("head_roll_mount.stl"),"roll_servo":L("roll_servo.stl")}
print("== overlaps > 0.5 mm3 (chassis/tof_tab touching roll_mount ears and radxa standoff contact are by design)")
allm={**parts,**vit,**static}; names=list(allm)
for i in range(len(names)):
    for j in range(i+1,len(names)):
        a,b=names[i],names[j]
        if a.startswith("v_") and b.startswith("v_"): continue
        if a in static and b in static: continue
        v=ivol(allm[a],allm[b])
        if v!=v or v>0.5: print(f"  {a} x {b}: {v:.1f}")
print("== clearance to moving neck parts (roll ±30, yaw ±160, pitch ±45)")
Pm=np.load("head_mover_pts.npy"); sel=Pm[np.random.default_rng(0).choice(len(Pm),400000,replace=False)].astype(float)
for n,t in {**parts,**vit}.items():
    kd=cKDTree(trimesh.sample.sample_surface(t,40000)[0]); dd,_=kd.query(sel)
    near=sel[dd<6]; ins=int(t.contains(near).sum()) if (len(near) and t.is_watertight) else 0
    print(f"  {n:14s} min {dd.min():5.2f} mm, mover points inside: {ins}")
