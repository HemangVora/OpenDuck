import numpy as np, trimesh, asm, math
D=math.degrees
asm.pose()
G=[(mn,b,t) for mn,b,t in asm.geoms(["foot_assembly","knee_and_ankle_assembly_2"])]
floor=min(t.bounds[0][2] for mn,b,t in G if b=="foot_assembly")
print("floor z (zero pose)",round(floor,2))
for mn,b,t in G: print(f"{b:28s} {mn:32s} {t.bounds.round(1).tolist()} vol {t.volume/1000 if t.is_watertight else float('nan'):.1f}cm3")
# ankle axis in print frame
j=asm.JN.index("left_ankle"); bid=asm.m.jnt_bodyid[j]
ax=asm.d.xmat[bid].reshape(3,3)@asm.m.jnt_axis[j]; p=asm.d.xpos[bid]*1000+asm.OFF+asm.d.xmat[bid].reshape(3,3)@asm.m.jnt_pos[j]*1000
print("left ankle axis point",p.round(1),"dir",ax.round(3))
# walking stance: foot inner gap and yaw
q={"left_hip_yaw":D(0.002),"left_hip_roll":D(0.053),"left_hip_pitch":D(-0.63),"left_knee":D(1.368),"left_ankle":D(-0.784),
   "right_hip_yaw":D(-0.003),"right_hip_roll":D(-0.065),"right_hip_pitch":D(0.635),"right_knee":D(1.379),"right_ankle":D(-0.796)}
asm.pose(q)
L=np.vstack([t.vertices for mn,b,t in asm.geoms(["foot_assembly"])]); R=np.vstack([t.vertices for mn,b,t in asm.geoms(["foot_assembly_2"])])
print("stance: left foot y",L[:,1].min().round(1),L[:,1].max().round(1)," right foot y",R[:,1].min().round(1),R[:,1].max().round(1),"x",L[:,0].min().round(1),L[:,0].max().round(1))
print("stance inner gap between feet (mm)", round(L[:,1].min()-R[:,1].max(),1))
