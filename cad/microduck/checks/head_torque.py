import numpy as np, trimesh, asm
from common import *
g=9.81
def joint_pt(name):
    j=asm.JN.index(name); b=asm.m.jnt_bodyid[j]; R=asm.d.xmat[b].reshape(3,3)
    return asm.d.xpos[b]*1000+asm.OFF+R@asm.m.jnt_pos[j]*1000, R@asm.m.jnt_axis[j]
asm.pose()
hp,_=joint_pt("head_pitch"); npt,_=joint_pt("neck_pitch")
# baseline the policy is trained on: MJCF head_assembly inertial (+ yaw/roll links above head pitch)
def body_com(name):
    b=asm.BN.index(name); return asm.d.xipos[b]*1000+asm.OFF, asm.m.body_mass[b]*1000
above_hp=["head_assembly","neck_yaw_assembly","left_antenna_holder","right_antenna_holder"]
mj=[body_com(n) for n in above_hp]; Mmj=sum(m for c,m in mj); Cmj=sum(c*m for c,m in mj)/Mmj
# our head: printed parts (slicer model grams split by volume inside each plate) + electronics + kept stock links
def parts_mass(plate_g, names):
    ms=[L(S+n+".stl") for n in names]; V=sum(m.volume for m in ms); return [(m, plate_g*m.volume/V) for m in ms]
v2=parts_mass(168.6,["v2/head_shell"]) if False else None
B="/Users/hemangvora/OpenDuck/cad/microduck/_v2_backup/stl/"
def LB(n): return trimesh.load(B+n+".stl",force='mesh')
def pm(plate_g, ms):
    V=sum(m.volume for m in ms); return [(m.center_mass, plate_g*m.volume/V) for m in ms]
P2=pm(168.6,[LB("head_shell")])+pm(119.9,[LB("head_tray"),LB("head_jaw")])+pm(69.0,[LB("head_chassis"),LB("eye_bezel"),LB("tof_tab")])
P3=pm(146.2,[L(S+"head_shell.stl")])+pm(22.8,[L(S+n+".stl") for n in ["eye_ring","mouth_jaw","mouth_bill"]])+pm(102.8,[L(S+n+".stl") for n in ["head_jaw","head_tray"]])+pm(124.5,[L(S+n+".stl") for n in ["head_chassis","face_bill"]])
rs=L("roll_servo.stl"); rm=L("head_roll_mount.stl")
ELEC=[(rs.bounds.mean(0),68.0),(rm.bounds.mean(0),20.0),(np.array([64,0,177.0]),12.0),(np.array([-30,0,178.0]),14.0),(np.array([106,0,163.4]),4.0),(np.array([104,-44,168.0]),2.0),(np.array([14,-40,146.0]),9.0),(np.array([0,0,150.0]),25.0)]
yaw=body_com("neck_yaw_assembly")   # yaw servo + link stay stock
def total(P): L_=P+ELEC+[yaw]; M=sum(m for c,m in L_); C=sum(np.asarray(c)*m for c,m in L_)/M; return M,C
for name,(M,C) in [("MJCF stock (trained on)",(Mmj,Cmj)),("v2 build (est.)",total(P2)),("v3 build (est.)",total(P3))]:
    t_hp=M/1000*g*abs(C[0]-hp[0])/1000; t_np=M/1000*g*abs(C[0]-npt[0])/1000
    print(f"{name:26s} mass above head-pitch {M:6.0f} g  COM x {C[0]:6.1f} z {C[2]:6.1f} | static torque head-pitch {t_hp:.3f} N.m, neck-pitch {t_np:.3f} N.m")
print(f"head pitch axis at x {hp[0]:.1f} z {hp[2]:.1f}; neck pitch axis at x {npt[0]:.1f} z {npt[2]:.1f}; ST3215-HS stall ~1.96 N.m (20 kg.cm)")
