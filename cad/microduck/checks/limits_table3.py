import numpy as np, trimesh
from scipy.spatial import cKDTree
from common import *
import asm
BODY=["body_shell_left","body_shell_right","body_deck","body_panel","switch_guard"]
bkd=cKDTree(np.vstack([trimesh.sample.sample_surface(L(S+n+".stl"),40000)[0] for n in BODY]))
HEAD=["head_shell","head_tray","head_jaw","face_bill","eye_ring","head_chassis"]
asm.pose(); Ti=np.linalg.inv(asm.body_T("head_assembly"))
hp=np.vstack([trimesh.sample.sample_surface(L(S+n+".stl"),20000)[0] for n in HEAD])
H=lambda P,M:(np.c_[P,np.ones(len(P))]@M.T)[:,:3]
hp_loc=H(hp,Ti)
jaw=L(S+"head_jaw.stl"); JP=np.array([20,0,146.0]); jp=trimesh.sample.sample_surface(jaw,20000)[0]
best=None
for a in (15,-15):
    R=trimesh.transformations.rotation_matrix(np.radians(a),[0,1,0],JP); q=H(jp,R)
    if best is None or q[:,2].min()<best[:,2].min(): best=q
print("jaw open 15: lowest z %.1f (closed %.1f)"%(best[:,2].min(),jaw.bounds[0][2])); jo_loc=H(best,Ti)
NECKB=["neck_pitch_assembly","head_pitch_to_yaw","neck_yaw_assembly"]
NP=list(range(-20,66,10)); HPs=list(range(-45,46,15))
tab=np.zeros((len(NP),len(HPs))); tabj=np.zeros_like(tab)
for i,a in enumerate(NP):
    for j,b in enumerate(HPs):
        asm.pose({"neck_pitch":a,"head_pitch":b}); T=asm.body_T("head_assembly")
        neck=np.vstack([t.vertices[::3] for mn,bb,t in asm.geoms(NECKB)])
        d1=bkd.query(np.vstack([H(hp_loc,T),neck]))[0].min(); d2=bkd.query(H(jo_loc,T))[0].min()
        tab[i,j]=d1; tabj[i,j]=min(d1,d2)
def show(t,title):
    print(title); print("neck\\head "+" ".join(f"{b:5d}" for b in HPs))
    for i,a in enumerate(NP): print(f"{a:9d} "+" ".join((" HIT " if v<1.0 else f"{min(v,99):5.1f}") for v in t[i]))
show(tab,"== min clearance head+neck to body (mm), jaw closed; HIT = under 1 mm")
show(tabj,"== jaw open 15 deg")
