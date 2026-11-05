import numpy as np, trimesh
U="/Users/hemangvora/OpenDuck/upstream/Open_Duck_Mini/print/"
ft=trimesh.load(U+"foot_top.stl",force='mesh'); fs=trimesh.load(U+"foot_side.stl",force='mesh'); pl=trimesh.load(U+"foot_bottom_pla.stl",force='mesh'); tp=trimesh.load(U+"foot_bottom_tpu.stl",force='mesh')
for n,m in [("foot_top",ft),("foot_side",fs),("pla",pl),("tpu",tp)]: print(n,m.bounds.round(2).tolist(),"watertight",m.is_watertight)
both=trimesh.util.concatenate([ft,fs])
def hits(o,d):
    loc,_,_=both.ray.intersects_location([o],[d]); return sorted(np.asarray(loc).reshape(-1,3)[:, np.argmax(np.abs(d))].round(2).tolist())
for x in [-40,-16,10,35]:
    for z in [-248,-240,-230,-220]:
        print(f"x {x:4d} z {z}: y-crossings", hits([x,0,z],[0,1,0]))
for x in [-50,-30,-16,0,20,40]:
    print(f"x {x:4d} y 94: z-crossings", hits([x,94,-300],[0,0,1]), " y 73:",hits([x,73,-300],[0,0,1])," y 111:",hits([x,111,-300],[0,0,1]))
