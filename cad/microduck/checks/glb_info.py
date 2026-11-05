import trimesh, numpy as np
sc=trimesh.load("/Users/hemangvora/Downloads/microduck/source/Microduck_WRS.glb")
print(type(sc), len(sc.geometry))
for name,node in list(sc.graph.to_flattened().items())[:0]: pass
rows=[]
for node in sc.graph.nodes_geometry:
    T,g=sc.graph[node]; m=sc.geometry[g]
    col=None
    try:
        mat=m.visual.material; col=getattr(mat,'baseColorFactor',None)
        if col is None: col=getattr(mat,'diffuse',None)
    except Exception: pass
    b=trimesh.transform_points(m.bounds,T)
    rows.append((node,g,len(m.faces),None if col is None else np.round(np.asarray(col)[:3],2).tolist(),np.round(b.min(0),3).tolist(),np.round(b.max(0),3).tolist()))
for r in rows: print(r)
print("scene bounds",sc.bounds.round(3).tolist())
