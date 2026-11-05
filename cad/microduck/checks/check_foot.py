import numpy as np, trimesh, itertools, math
from scipy.spatial import cKDTree
from common import *
import asm
U="/Users/hemangvora/OpenDuck/upstream/Open_Duck_Mini/print/"
new=[L(S+"md_foot_top.stl"),L(S+"md_foot_side.stl")]; old=[L(U+"foot_top.stl"),L(U+"foot_side.stl")]
tpu=L(U+"foot_bottom_tpu.stl"); pla=L(U+"foot_bottom_pla.stl")
NEW=trimesh.util.concatenate(new); OLD=trimesh.util.concatenate(old)
print("== parts"); [solid_report(n,t) for n,t in zip(["md_foot_top","md_foot_side"],new)]
print("== new parts vs sole plates overlap (mm3):", round(ivol(new[0],pla)+ivol(new[1],pla),2), round(ivol(new[0],tpu)+ivol(new[1],tpu),2))
# 1) floor contact: tilt the whole foot about each sole edge until the skin would reach the floor before the TPU
floor=tpu.bounds[0][2]; print("== contact: TPU bottom z %.2f, lowest new-part point z %.2f (%.1f mm above floor)"%(floor,NEW.bounds[0][2],NEW.bounds[0][2]-floor))
Vn=NEW.vertices; Vt=tpu.vertices
for name,axis,pt in [("roll outward (+y edge)",[1,0,0],[0,Vt[:,1].max(),floor]),("roll inward (-y edge)",[-1,0,0],[0,Vt[:,1].min(),floor]),
                     ("pitch toe down",[0,-1,0],[Vt[:,0].max(),0,floor]),("pitch heel down",[0,1,0],[Vt[:,0].min(),0,floor])]:
    ang=None
    for a in np.arange(0.5,90,0.5):
        R=trimesh.transformations.rotation_matrix(np.radians(a),axis,pt)
        zt=(np.c_[Vt,np.ones(len(Vt))]@R.T)[:,2].min(); zn=(np.c_[Vn,np.ones(len(Vn))]@R.T)[:,2].min()
        if zn<=zt+0.01: ang=a; break
    print(f"   {name:24s}: skin would touch the floor only past {ang} deg of tilt")
# 2) ankle range: shank parts vs stock and new foot at every angle
asm.pose(); Tf0=asm.body_T("foot_assembly"); worse=[]
for a in np.arange(-90,90.1,2.5):
    asm.pose({"left_ankle":a}); M=Tf0@np.linalg.inv(asm.body_T("foot_assembly"))
    so=sn=0.0
    for mn,b,t in asm.geoms(["knee_and_ankle_assembly_2"]):
        if "palonier" in mn: continue
        t=t.copy(); t.apply_transform(M); Mt=MAN(t)
        if not ok(Mt): continue
        so+=sum((Mt^MAN(o)).volume() for o in old); sn+=sum((Mt^MAN(o)).volume() for o in new)
    if sn>so+0.5: worse.append((a,round(so,1),round(sn,1)))
print("== ankle: angles where the new foot collides more than the stock foot:", worse if worse else "none")
# 3) the two feet: walking stance, turning (hip yaw), hip roll, single support swings
D=math.degrees
base={"left_hip_yaw":D(0.002),"left_hip_roll":D(0.053),"left_hip_pitch":D(-0.63),"left_knee":D(1.368),"left_ankle":D(-0.784),
      "right_hip_yaw":D(-0.003),"right_hip_roll":D(-0.065),"right_hip_pitch":D(0.635),"right_knee":D(1.379),"right_ankle":D(-0.796)}
fL=asm.attach(NEW,"foot_assembly"); fR_src=NEW.copy(); fR_src.apply_translation([0,-181.2,0]); fR=asm.attach(fR_src,"foot_assembly_2")
fLo=asm.attach(OLD,"foot_assembly"); fRo_src=OLD.copy(); fRo_src.apply_translation([0,-181.2,0]); fRo=asm.attach(fRo_src,"foot_assembly_2")
worst=(99,None); worst_o=(99,None)
for yl,yr,rl,rr,dp in itertools.product([-30,0,30],[-30,0,30],[-15,0,15],[-15,0,15],[-20,0,20]):
    q=dict(base); q["left_hip_yaw"]+=yl; q["right_hip_yaw"]+=yr; q["left_hip_roll"]+=rl; q["right_hip_roll"]+=rr; q["left_hip_pitch"]+=dp; q["right_hip_pitch"]-=dp
    asm.pose(q)
    a=trimesh.sample.sample_surface(fL(),4000)[0]; d=cKDTree(trimesh.sample.sample_surface(fR(),4000)[0]).query(a)[0].min()
    ao=trimesh.sample.sample_surface(fLo(),4000)[0]; do=cKDTree(trimesh.sample.sample_surface(fRo(),4000)[0]).query(ao)[0].min()
    if d<worst[0]: worst=(d,(yl,yr,rl,rr,dp))
    if do<worst_o[0]: worst_o=(do,(yl,yr,rl,rr,dp))
asm.pose(base); a=trimesh.sample.sample_surface(fL(),6000)[0]; d0=cKDTree(trimesh.sample.sample_surface(fR(),6000)[0]).query(a)[0].min()
print(f"== feet: default stance gap {d0:.1f} mm; worst over 243 turning/roll/swing poses: new {worst[0]:.1f} mm at {worst[1]}, stock {worst_o[0]:.1f} mm at {worst_o[1]}")
# 4) thigh/knee vs foot over knee x ankle (stock-relative)
thigh=[t for mn,b,t in asm.geoms(["knee_and_ankle_assembly"])]
bad=[]
for kn,an in itertools.product(range(-90,91,15),range(-65,48,7)):
    asm.pose({"left_knee":kn,"left_ankle":an}); P=np.vstack([trimesh.sample.sample_surface(t,800)[0] for mn,b,t in asm.geoms(["knee_and_ankle_assembly"])])
    dn=cKDTree(trimesh.sample.sample_surface(fL(),5000)[0]).query(P)[0].min(); do=cKDTree(trimesh.sample.sample_surface(fLo(),5000)[0]).query(P)[0].min()
    if dn<1.0 and do>=1.0: bad.append((kn,an,round(dn,2),round(do,2)))
print("== thigh vs foot: poses blocked by the new foot but free on the stock foot:", bad if bad else "none")
