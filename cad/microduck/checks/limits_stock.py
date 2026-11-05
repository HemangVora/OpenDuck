import numpy as np, trimesh, mujoco
from scipy.spatial import cKDTree
import asm
H=lambda P,M:(np.c_[P,np.ones(len(P))]@M.T)[:,:3]
for jn in ["neck_pitch","head_pitch","head_yaw","head_roll"]:
    j=asm.JN.index(jn); print(jn,"range deg",np.degrees(asm.m.jnt_range[j]).round(1))
asm.pose(); G=asm.geoms(["trunk_assembly"])
SB={"body_front","body_back","body_middle_top","body_middle_bottom"}
skd=cKDTree(np.vstack([trimesh.sample.sample_surface(t,40000)[0] for mn,b,t in G if mn in SB]))
from common import *
BODY=["body_shell_left","body_shell_right","body_deck","body_panel","switch_guard"]
mkd=cKDTree(np.vstack([trimesh.sample.sample_surface(L(S+n+".stl"),40000)[0] for n in BODY]))
Ti=np.linalg.inv(asm.body_T("head_assembly"))
shead=np.vstack([trimesh.sample.sample_surface(t,20000)[0] for mn,b,t in asm.geoms(["head_assembly"]) if mn=="head"]); sh_loc=H(shead,Ti)
NECKB=["neck_pitch_assembly","head_pitch_to_yaw","neck_yaw_assembly"]
NP=list(range(-20,66,10)); HPs=list(range(-45,46,15))
print("stock head+neck vs stock body | neck-only vs NEW body  (mm, HIT<1)")
print("neck\\head "+" ".join(f"{b:5d}" for b in HPs)+"  | neck-only new body")
for a in NP:
    row=[]
    for b in HPs:
        asm.pose({"neck_pitch":a,"head_pitch":b}); T=asm.body_T("head_assembly")
        neck=np.vstack([t.vertices[::3] for mn,bb,t in asm.geoms(NECKB)])
        d=skd.query(np.vstack([H(sh_loc,T),neck]))[0].min(); row.append(" HIT " if d<1 else f"{min(d,99):5.1f}")
    asm.pose({"neck_pitch":a}); neck=np.vstack([t.vertices[::3] for mn,bb,t in asm.geoms(NECKB)])
    dn,idx=mkd.query(neck); k=dn.argmin()
    print(f"{a:9d} "+" ".join(row)+f"  | {dn.min():5.1f} at {neck[k].round(0)}")
