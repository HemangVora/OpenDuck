import numpy as np, trimesh, itertools
from scipy.spatial import cKDTree
from common import *
FIX=["head_shell","head_tray","face_bill","eye_ring","mouth_bill","head_chassis"]
MOV=["head_jaw","mouth_jaw"]
VIT=["v_sg90_jaw","v_radxa","v_buck","v_camera","v_tof"]
print("== parts (want manifold=True pieces=1)")
P={n:solid_report(n,L(S+n+".stl")) for n in FIX+MOV}
V={n:L(S+n+".stl") for n in VIT}; ST={"roll_mount":L("head_roll_mount.stl"),"roll_servo":L("roll_servo.stl")}
allm={**P,**V,**ST}
print("== overlaps > 0.5 mm3 (closed jaw)")
for a,b in itertools.combinations(allm,2):
    if (a in V or a in ST) and (b in V or b in ST): continue
    if {a,b}=={"head_jaw","v_sg90_jaw"}: continue          # horn sits in the jaw pocket by design
    v=ivol(allm[a],allm[b])
    if v!=v or v>0.5: print(f"  {a} x {b}: {v:.1f}")
print("== jaw sweep 0..17.5 deg (front drops): overlap mm3 with fixed parts, min gap")
JP=np.array([20,0,146.0]); fixed={k:v for k,v in allm.items() if k not in MOV and k!="v_sg90_jaw"}
fk={k:cKDTree(trimesh.sample.sample_surface(v,30000)[0]) for k,v in fixed.items()}
for a in [0,2.5,5,7.5,10,12.5,15,17.5]:
    R=trimesh.transformations.rotation_matrix(np.radians(a),[0,1,0],JP)
    worst=[]; gmin=99
    for m in MOV:
        j=P[m].copy(); j.apply_transform(R); pts=trimesh.sample.sample_surface(j,30000)[0]
        for k,t in fixed.items():
            v=ivol(j,t)
            if v!=v or v>0.5: worst.append(f"{m}x{k}:{v:.1f}")
            gmin=min(gmin,fk[k].query(pts)[0].min())
    print(f"  {a:5.1f} deg: lowest z {min(P['head_jaw'].copy().apply_transform(R).bounds[0][2],999):6.1f} min gap {gmin:5.2f} mm overlaps: {worst if worst else 'none'}")
print("== clearance to moving neck parts (roll +-30, yaw +-160, pitch +-45)")
Pm=np.load("head_mover_pts.npy"); sel=Pm[np.random.default_rng(0).choice(len(Pm),300000,replace=False)].astype(float)
for n in ["face_bill","head_jaw","head_shell","head_tray"]:
    kd=cKDTree(trimesh.sample.sample_surface(P[n],40000)[0]); print(f"  {n:12s} min {kd.query(sel)[0].min():5.2f} mm")
