import trimesh, numpy as np, os
O="/Users/hemangvora/OpenDuck/cad/microduck/previews/compare/"; os.makedirs(O,exist_ok=True)
sc=trimesh.load("/Users/hemangvora/Downloads/microduck/source/Microduck_WRS.glb")
M=np.array([[1,0,0,0],[0,0,-1,0],[0,1,0,0],[0,0,0,1.0]]); S=np.diag([1700,1700,1700,1.0])
T=np.eye(4); T[:3,3]=[20-1.7*41,0,109.7-1.7*205.4]
G={"purple":[],"yellow":[],"blue":[],"eye":[],"dark":[],"grey":[]}
def grp(n):
    if n.startswith("Cable"): return None
    if any(k in n for k in ["head_shell","body_right_shell","body_left_shell","thigh_right_shell","thigh_left_shell","sole__","mouth_"]): return "purple"
    if n in ("head",) or n.startswith("jaw") or "_foot__" in n: return "yellow"
    if n=="eye_shell": return "blue"
    if n=="eye": return "eye"
    if "palonier" in n or n.endswith("_1") and "Hardware" in n: return "grey"
    return "dark"
for node in sc.graph.nodes_geometry:
    Tn,g=sc.graph[node]; k=grp(node)
    if k is None: continue
    m=sc.geometry[g].copy(); m.apply_transform(T@S@M@Tn); G[k].append(m)
zmin=min(min(m.bounds[0][2] for m in v) for v in G.values() if v)
for k,v in G.items():
    if v: m=trimesh.util.concatenate(v); m.apply_translation([0,0,-zmin]); m.export(O+f"ref_{k}.stl")
allv=np.vstack([m.vertices for v in G.values() for m in v]); print("ref bounds (mm, floored)", (allv.min(0)-[0,0,zmin]).round(0), (allv.max(0)-[0,0,zmin]).round(0))
