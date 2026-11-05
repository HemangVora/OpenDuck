import trimesh, numpy as np, manifold3d as m3d
S="/Users/hemangvora/OpenDuck/cad/microduck/stl/"
def L(p): return trimesh.load(p,force='mesh')
def MAN(t): return m3d.Manifold(m3d.Mesh(vert_properties=np.asarray(t.vertices,dtype=np.float32), tri_verts=np.asarray(t.faces,dtype=np.uint32)))
def ok(M): return M.status()==m3d.Error.NoError
def clean(t):
    M=MAN(t); mm=M.to_mesh(); return trimesh.Trimesh(np.asarray(mm.vert_properties)[:,:3], np.asarray(mm.tri_verts)), M
def ivol(a,b):
    A,B=MAN(a),MAN(b)
    return (A^B).volume() if ok(A) and ok(B) else float('nan')
def solid_report(n,t):
    c,M=clean(t); pieces=len([p for p in c.split(only_watertight=False) if abs(p.volume)>1])
    print(f"  {n:18s} manifold={ok(M)} pieces={pieces} vol={c.volume/1000:6.1f} cm3 bounds={c.bounds.round(1).tolist()}")
    return c
