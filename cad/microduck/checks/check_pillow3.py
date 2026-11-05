import numpy as np, trimesh, itertools
from scipy.spatial import cKDTree
from common import *
import asm
SIDES={"left":dict(th="knee_and_ankle_assembly",mov=["knee_and_ankle_assembly_2","foot_assembly"],hip=["trunk_assembly","hip_roll_assembly","left_roll_to_pitch_assembly"],cache="left_cache"),
       "right":dict(th="knee_and_ankle_assembly_3",mov=["knee_and_ankle_assembly_4","foot_assembly_2"],hip=["trunk_assembly","hip_roll_assembly_2","right_roll_to_pitch_assembly"],cache="right_cache")}
BODY=["body_shell_left","body_shell_right","body_deck","body_panel","deck_clamp_rear","deck_clamp_front","switch_guard"]
STOCKBODY={"body_front","body_back","body_middle_bottom","body_middle_top","battery_pack_lid","power_switch","usb_c_charger","bms","cell","holder","board"}
bodypts=np.vstack([trimesh.sample.sample_surface(L(S+n+".stl"),15000)[0] for n in BODY])
MDF=[L(S+"md_foot_top.stl"),L(S+"md_foot_side.stl")]
def pts(meshes,n=800): return np.vstack([np.vstack([t.vertices,trimesh.sample.sample_surface(t,n)[0]]) for t in meshes]) if meshes else np.zeros((0,3))
def to_frame(P,Tcur,T0): M=T0@np.linalg.inv(Tcur); return (np.c_[P,np.ones(len(P))]@M.T)[:,:3]
for side,c in SIDES.items():
    print(f"== {side}"); pil=solid_report(f"thigh_pillow_{side}",L(S+f"thigh_pillow_{side}.stl"))
    asm.pose(); T0=asm.body_T(c["th"])
    cache=[t for mn,b,t in asm.geoms([c["th"]]) if mn==c["cache"]][0]
    pk=cKDTree(trimesh.sample.sample_surface(pil,40000)[0]); ck=cKDTree(trimesh.sample.sample_surface(cache,40000)[0])
    lo,hi=pil.bounds[0]-10,pil.bounds[1]+10
    def near(P): return P[np.all((P>lo)&(P<hi),1)]
    j=side; bad=[]; worst=99; skipped=0; n=0
    for knee,ank in itertools.product(range(-90,91,30),range(-65,48,15)):
        asm.pose({f"{j}_knee":knee,f"{j}_ankle":ank})
        movs=[t for mn,b,t in asm.geoms(c["mov"]) if mn not in ("foot_top","foot_side")]
        fb="foot_assembly" if side=="left" else "foot_assembly_2"; dy=0 if side=="left" else -181.2
        asm.pose(); Tf0=asm.body_T(fb); asm.pose({f"{j}_knee":knee,f"{j}_ankle":ank}); Tf=asm.body_T(fb)
        for f in MDF:
            g=f.copy(); g.apply_translation([0,dy,0]); g.apply_transform(Tf@np.linalg.inv(Tf0)); movs.append(g)
        P=near(to_frame(pts(movs),asm.body_T(c["th"]),T0))
        if not len(P): n+=1; continue
        if ck.query(P)[0].min()<0.5: skipped+=1; continue
        n+=1; d=pk.query(P)[0].min(); worst=min(worst,d)
        if d<1.0: bad.append((knee,ank,round(d,2)))
    print(f"  knee x ankle: {n} poses free with stock cache, {len(bad)} within 1 mm of pillow, min clearance {worst:.2f} mm; stock-blocked {skipped}", bad[:8])
    bad=[]; worst=99; skipped=0; n=0
    pr=range(-70,31,20) if side=="left" else range(-30,71,20)
    for yaw,roll,pitch in itertools.product([-30,0,30],[-25,0,25],pr):
        asm.pose({f"{j}_hip_yaw":yaw,f"{j}_hip_roll":roll,f"{j}_hip_pitch":pitch}); Tc=asm.body_T(c["th"])
        G=asm.geoms(c["hip"]); other=[t for mn,b,t in G if mn not in STOCKBODY]; stockb=[t for mn,b,t in G if mn in STOCKBODY-{"board"}]
        P=near(to_frame(pts(other),Tc,T0)); Ps=near(to_frame(pts(stockb),Tc,T0)); Pb=near(to_frame(bodypts,Tc,T0))
        if (len(P) and ck.query(P)[0].min()<0.5) or (len(Ps) and ck.query(Ps)[0].min()<0.5): skipped+=1; continue
        n+=1; Q=np.vstack([P,Pb]) if len(Pb) else P
        if not len(Q): continue
        d=pk.query(Q)[0].min(); worst=min(worst,d)
        if d<1.0: bad.append((yaw,roll,pitch,round(d,2)))
    print(f"  hip sweep: {n} poses free with stock cache, {len(bad)} within 1 mm of pillow, min clearance {worst:.2f} mm; stock-blocked {skipped}", bad[:8])
