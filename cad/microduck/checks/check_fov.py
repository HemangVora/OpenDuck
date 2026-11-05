import numpy as np, trimesh
from common import *
JP=np.array([20,0,146.0])
def scene(open_deg):
    ms=[L(S+n+".stl") for n in ["face_bill","eye_ring","head_shell","mouth_bill"]]
    R=trimesh.transformations.rotation_matrix(np.radians(open_deg),[0,1,0],JP)
    for n in ["head_jaw","mouth_jaw"]:
        m=L(S+n+".stl"); m.apply_transform(R); ms.append(m)
    return trimesh.util.concatenate(ms)
def clear_angle(sc, origins, axis_dirs):
    """for each named direction (unit vector in the y/z plane), find the largest angle off +x that is unobstructed from every origin"""
    out={}
    for name,v in axis_dirs.items():
        best=0
        for ang in np.arange(1,89,1.0):
            d=np.array([np.cos(np.radians(ang)),*(np.sin(np.radians(ang))*np.asarray(v))])
            O=np.asarray(origins,float); D=np.tile(d,(len(O),1))
            hit=sc.ray.intersects_any(O+D*0.05,D)
            if hit.any(): break
            best=ang
        out[name]=best
    return out
dirs={"left(+y)":[1,0],"right(-y)":[-1,0],"up":[0,1],"down":[0,-1],"up-left":[0.707,0.707],"up-right":[-0.707,0.707],"down-left":[0.707,-0.707],"down-right":[-0.707,-0.707]}
cam=[[110.05,0,163.4]]+[[110.05,2.0*np.cos(t),163.4+2.0*np.sin(t)] for t in np.linspace(0,2*np.pi,8,endpoint=False)]
tof=[[106.6,-44+dy,168+dz] for dy in (-3.2,0,3.2) for dz in (-1.5,0,1.5)]
for od in (0,15):
    sc=scene(od)
    print(f"== jaw open {od} deg")
    print("  camera clear half-angles (deg):",clear_angle(sc,cam,dirs))
    print("  ToF    clear half-angles (deg):",clear_angle(sc,tof,dirs))
print("needs: IMX219 standard lens 31.1 H / 24.4 V / 37.5 diag half-angles; IMX219-160 ~80 diag; VL53L8CX 22.5 H/V, 32.5 diag")
