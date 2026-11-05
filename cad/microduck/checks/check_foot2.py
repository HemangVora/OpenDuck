import numpy as np, trimesh, itertools, math
from scipy.spatial import cKDTree
from common import *
import asm
U="/Users/hemangvora/OpenDuck/upstream/Open_Duck_Mini/print/"
NEW=trimesh.util.concatenate([L(S+"md_foot_top.stl"),L(S+"md_foot_side.stl")]); OLD=trimesh.util.concatenate([L(U+"foot_top.stl"),L(U+"foot_side.stl")])
tpu=L(U+"foot_bottom_tpu.stl")
def first_contact(parts, axis, sign):
    for a in np.arange(0.5,90,0.5):
        R=trimesh.transformations.rotation_matrix(sign*np.radians(a),axis)
        zt=(np.c_[tpu.vertices,np.ones(len(tpu.vertices))]@R.T)[:,2].min(); zp=(np.c_[parts.vertices,np.ones(len(parts.vertices))]@R.T)[:,2].min()
        if zp<=zt: return a
    return None
print("== tilt before anything other than the TPU sole reaches the floor (stock foot vs new foot)")
for name,axis,sign in [("roll onto the +y edge",[1,0,0],-1),("roll onto the -y edge",[1,0,0],1),("toe down",[0,1,0],1),("heel down",[0,1,0],-1)]:
    print(f"   {name:22s}: stock {first_contact(OLD,axis,sign)} deg, new {first_contact(NEW,axis,sign)} deg")
D=math.degrees
base={"left_hip_yaw":D(0.002),"left_hip_roll":D(0.053),"left_hip_pitch":D(-0.63),"left_knee":D(1.368),"left_ankle":D(-0.784),
      "right_hip_yaw":D(-0.003),"right_hip_roll":D(-0.065),"right_hip_pitch":D(0.635),"right_knee":D(1.379),"right_ankle":D(-0.796)}
def pair(src):
    l=asm.attach(src,"foot_assembly"); r0=src.copy(); r0.apply_translation([0,-181.2,0]); r=asm.attach(r0,"foot_assembly_2"); return l,r
nl,nr=pair(NEW); ol,orr=pair(OLD)
rows=[]
for yl,yr,rl,rr,dp in itertools.product([-30,-15,0,15,30],[-30,-15,0,15,30],[-15,0,15],[-15,0,15],[-20,0,20]):
    q=dict(base); q["left_hip_yaw"]+=yl; q["right_hip_yaw"]+=yr; q["left_hip_roll"]+=rl; q["right_hip_roll"]+=rr; q["left_hip_pitch"]+=dp; q["right_hip_pitch"]-=dp
    asm.pose(q)
    dn=cKDTree(trimesh.sample.sample_surface(nr(),3000)[0]).query(trimesh.sample.sample_surface(nl(),3000)[0])[0].min()
    do=cKDTree(trimesh.sample.sample_surface(orr(),3000)[0]).query(trimesh.sample.sample_surface(ol(),3000)[0])[0].min()
    rows.append((yl,yr,rl,rr,dp,do,dn))
R=np.array(rows); lost=R[(R[:,5]>=2)&(R[:,6]<2)]
print(f"== feet over {len(R)} turning/roll/swing poses: stock clash(<2mm) {int((R[:,5]<2).sum())}, new clash {int((R[:,6]<2).sum())}, new-only clashes {len(lost)}")
for r in lost[:12]: print("   yaw L/R %+d/%+d roll L/R %+d/%+d dpitch %+d : stock %.1f new %.1f"%tuple(r))
inner=R[(np.abs(R[:,0])<=15)&(np.abs(R[:,1])<=15)]; print("   with hip yaw within +-15: min gap stock %.1f new %.1f mm"%(inner[:,5].min(),inner[:,6].min()))
