import numpy as np, trimesh, itertools
from scipy.spatial import cKDTree
from common import *
import asm
PARTS=["body_shell_left","body_shell_right","body_deck","body_panel","deck_clamp_rear","deck_clamp_front","switch_guard"]
VIT=["v_pack","v_bms","v_adapter","v_switch","v_xt30","v_balance","v_caps"]
print("== parts"); parts={n:solid_report(n,L(S+n+".stl")) for n in PARTS}
vit={n:clean(L(S+n+".stl"))[0] for n in VIT}; allm={**parts,**vit}
print("== part/part and part/vitamin overlaps > 0.5 mm3")
for a,b in itertools.combinations(allm,2):
    if a.startswith("v_") and b.startswith("v_"): continue
    v=ivol(allm[a],allm[b])
    if v!=v or v>0.5: print(f"  {a} x {b}: {v:.1f}")
STOCK={"board","body_front","body_back","body_middle_bottom","body_middle_top","battery_pack_lid","power_switch","usb_c_charger","bms","cell","holder"}
asm.pose(); G=asm.geoms(["trunk_assembly"])
print("== fixed trunk hardware vs new parts (overlap mm3)")
for mn,b,t in G:
    if mn in STOCK: continue
    for n,p in allm.items():
        v=ivol(t,p)
        if v==v and v>0.5: print(f"  {mn} x {n}: {v:.1f}")
        elif v!=v:
            d=cKDTree(trimesh.sample.sample_surface(p,20000)[0]).query(trimesh.sample.sample_surface(t,5000)[0])[0].min()
            if d<1.0: print(f"  {mn} x {n}: non-manifold hw, min dist {d:.2f}")
mine=trimesh.util.concatenate(list(parts.values()))
stock=trimesh.util.concatenate([t for mn,b,t in G if mn in STOCK-{"board"}])
mkd=cKDTree(trimesh.sample.sample_surface(mine,120000)[0]); skd=cKDTree(trimesh.sample.sample_surface(stock,120000)[0])
lo=mine.bounds[0]-8; hi=mine.bounds[1]+8
LEG={"left":["hip_roll_assembly","left_roll_to_pitch_assembly","knee_and_ankle_assembly","knee_and_ankle_assembly_2","foot_assembly"],
     "right":["hip_roll_assembly_2","right_roll_to_pitch_assembly","knee_and_ankle_assembly_3","knee_and_ankle_assembly_4","foot_assembly_2"]}
bad=[]; minfree=99; nposes=0
for side in ("left","right"):
  for yaw,roll,pitch,knee in itertools.product([-30,-15,0,15,30],[-25,0,25],[-70,-35,0,30],[-90,0,90]):
    sg=1 if side=="left" else -1
    asm.pose({f"{side}_hip_yaw":yaw,f"{side}_hip_roll":roll,f"{side}_hip_pitch":pitch*sg,f"{side}_knee":knee})
    P=[]
    for mn,b,t in asm.geoms(LEG[side]):
        if not np.any(np.all((t.vertices>lo)&(t.vertices<hi),1)): continue
        p=np.vstack([t.vertices,trimesh.sample.sample_surface(t,1200)[0]]); P.append(p[np.all((p>lo)&(p<hi),1)])
    P=np.vstack(P) if P else np.zeros((0,3))
    if not len(P): continue
    ds=skd.query(P)[0].min()
    if ds<1.0: continue                  # stock ODM body is in the way too: not a reachable pose
    nposes+=1; dm=mkd.query(P)[0].min(); minfree=min(minfree,dm)
    if dm<1.0: bad.append((side,yaw,roll,pitch,knee,round(dm,2)))
print(f"== leg sweep: {nposes} poses free on the stock body; {len(bad)} of them come within 1 mm of the new body; min clearance {minfree:.2f} mm")
for b in bad[:20]: print("  ",b)
nk=np.load("neck_sheets_np20.npy").astype(float); nk=nk[np.all((nk>lo)&(nk<hi),1)]
print(f"== neck pitch -20..20 sweep vs new body: min clearance {mkd.query(nk)[0].min():.2f} mm" if len(nk) else "== neck sweep: nothing near body")
