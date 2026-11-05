import numpy as np, trimesh, manifold3d as m3d, asm
from common import MAN
U="/Users/hemangvora/OpenDuck/upstream/Open_Duck_Mini/print/"
stock=MAN(trimesh.load(U+"foot_top.stl",force='mesh'))+MAN(trimesh.load(U+"foot_side.stl",force='mesh'))+MAN(trimesh.load(U+"foot_bottom_pla.stl",force='mesh'))
asm.pose(); Tf0=asm.body_T("foot_assembly")
for a in [0,-30,30,-60,60]:
    asm.pose({"left_ankle":a}); M=Tf0@np.linalg.inv(asm.body_T("foot_assembly")); out=[]
    for mn,b,t in asm.geoms(["knee_and_ankle_assembly_2"]):
        t=t.copy(); t.apply_transform(M); Mt=MAN(t)
        out.append(f"{mn}:{(Mt^stock).volume():.1f}" if Mt.status()==m3d.Error.NoError else f"{mn}:nonmanifold")
    print(a, out)
