import numpy as np, trimesh, asm
asm.pose(); tb={mn:t for mn,b,t in asm.geoms(["trunk_assembly"])}["trunk_bottom"]
V=tb.vertices
for z0,z1 in [(-20,-15),(-40,-20),(-60,-40),(-78,-60),(-89,-78)]:
    s=V[(V[:,2]>=z0)&(V[:,2]<z1)]
    if len(s): print(f"z[{z0},{z1}]: n {len(s)} x[{s[:,0].min():.1f},{s[:,0].max():.1f}] y[{s[:,1].min():.1f},{s[:,1].max():.1f}]  center(|y|<15) x[{s[np.abs(s[:,1])<15][:,0].min() if (np.abs(s[:,1])<15).any() else 0:.1f},{s[np.abs(s[:,1])<15][:,0].max() if (np.abs(s[:,1])<15).any() else 0:.1f}]")
