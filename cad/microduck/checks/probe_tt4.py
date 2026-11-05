import numpy as np, trimesh
p=trimesh.load("/Users/hemangvora/OpenDuck/upstream/Open_Duck_Mini/print/trunk_top.stl",force='mesh')
for y in [0,20,26]:
    row=[]
    for x in np.arange(-48,-39.9,0.5):
        loc,_,_=p.ray.intersects_location([[x,y,5]],[[0,0,-1]]); z=np.asarray(loc)[:,2]; z=z[z<-5]
        row.append(f"{x:.1f}:{z.max():.1f}" if len(z) else f"{x:.1f}:.")
    print("y",y," ".join(row))
for x in [-70,-44]:
    row=[]
    for y in np.arange(20,31,1.0):
        loc,_,_=p.ray.intersects_location([[x,y,5]],[[0,0,-1]]); z=np.asarray(loc)[:,2]; z=z[z<-5]
        row.append(f"{y:.0f}:{z.max():.1f}" if len(z) else f"{y:.0f}:.")
    print("x",x," ".join(row))
