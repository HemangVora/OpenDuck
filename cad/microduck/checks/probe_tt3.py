import numpy as np, trimesh, asm
U="/Users/hemangvora/OpenDuck/upstream/Open_Duck_Mini/print/"
asm.pose(); G={mn:t for mn,b,t in asm.geoms(["trunk_assembly"])}
for n in ["trunk_top","body_middle_bottom","body_back"]:
    p=trimesh.load(U+n+".stl",force='mesh'); m=G[n]
    print(f"{n:20s} print-STL bounds {p.bounds.round(2).tolist()}\n{'':20s} mujoco bounds    {m.bounds.round(2).tolist()}")
p=trimesh.load(U+"trunk_top.stl",force='mesh')
for x,y in [(-70,0),(-44,0),(-60,20)]:
    loc,_,_=p.ray.intersects_location([[x,y,0]],[[0,0,-1]]); print("print STL plate top at",(x,y), np.sort(np.asarray(loc)[:,2].round(2))[::-1][:3])
