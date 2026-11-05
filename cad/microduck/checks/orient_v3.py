import trimesh, numpy as np, os
from common import *
S="/Users/hemangvora/OpenDuck/cad/microduck/stl/"; U="/Users/hemangvora/OpenDuck/upstream/Open_Duck_Mini/print/"
O="/Users/hemangvora/OpenDuck/print/microduck_v3/oriented/"
R=trimesh.transformations.rotation_matrix; X,Y=[1,0,0],[0,1,0]; pi=np.pi
V2="/Users/hemangvora/OpenDuck/print/microduck_v2/oriented/"
ORI={"head_shell":None,"face_bill":None,"head_jaw":None,"head_tray":None,"eye_ring":R(-pi/2,Y),"mouth_jaw":None,"mouth_bill":None,
     "md_foot_top":None,"md_foot_side":None}
for n,T in ORI.items():
    t,_=clean(L(S+n+".stl"))
    if T is not None: t.apply_transform(T)
    t.apply_translation(-t.bounds[0]); e=t.extents; t.apply_translation([-e[0]/2,-e[1]/2,0])
    fn=t.face_normals; c=t.triangles_center
    bed=t.area_faces[(fn[:,2]<-0.999)&(c[:,2]<0.05)].sum(); oh=t.area_faces[(fn[:,2]<-0.85)&(c[:,2]>0.3)].sum()
    t.export(O+n+".stl"); print(f"{n:14s} size {e.round(1).tolist()} bed {bed/100:6.1f} cm2 overhang {oh/100:6.1f} cm2")
# unchanged parts reused from v2 (already oriented), stock sole plate in white
for n in ["head_chassis","body_shell_left","body_shell_right","thigh_pillow_left","thigh_pillow_right","body_deck","body_panel","switch_guard","deck_clamp_rear","deck_clamp_front"]:
    trimesh.load(V2+n+".stl",force='mesh').export(O+n+".stl")
t=L(U+"foot_bottom_pla.stl"); t.apply_translation(-t.bounds[0]); e=t.extents; t.apply_translation([-e[0]/2,-e[1]/2,0]); t.export(O+"foot_bottom_pla.stl")
print("ok")
