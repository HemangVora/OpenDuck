"""Open Duck v2 assembly helper: poses meshes per body in the print frame (mm)."""
import mujoco, numpy as np, trimesh, os
R="/Users/hemangvora/OpenDuck/upstream/Open_Duck_Mini/mini_bdx/robots/open_duck_mini_v2"
OFF=np.array([19.0,0.0,-465.0])
m=mujoco.MjModel.from_xml_path(os.path.join(R,"robot.xml")); d=mujoco.MjData(m)
JN=[mujoco.mj_id2name(m,mujoco.mjtObj.mjOBJ_JOINT,j) for j in range(m.njnt)]
BN=[mujoco.mj_id2name(m,mujoco.mjtObj.mjOBJ_BODY,b) for b in range(m.nbody)]
def pose(q=None):
    d.qpos[:]=m.qpos0
    if q:
        for k,v in q.items():
            j=JN.index(k); d.qpos[m.jnt_qposadr[j]]=np.radians(v)
    mujoco.mj_forward(m,d)
def body_T(name):
    b=BN.index(name); T=np.eye(4); T[:3,:3]=d.xmat[b].reshape(3,3); T[:3,3]=d.xpos[b]*1000.0+OFF; return T
def geoms(filter_body=None):
    out=[]
    for g in range(m.ngeom):
        if m.geom_type[g]!=mujoco.mjtGeom.mjGEOM_MESH: continue
        b=BN[m.geom_bodyid[g]]
        if filter_body and b not in filter_body: continue
        mid=m.geom_dataid[g]; mn=mujoco.mj_id2name(m,mujoco.mjtObj.mjOBJ_MESH,mid)
        va=m.mesh_vertadr[mid]; vn=m.mesh_vertnum[mid]; fa=m.mesh_faceadr[mid]; fn=m.mesh_facenum[mid]
        V=m.mesh_vert[va:va+vn]; F=m.mesh_face[fa:fa+fn]
        W=(V@d.geom_xmat[g].reshape(3,3).T+d.geom_xpos[g])*1000.0+OFF
        out.append((mn,b,trimesh.Trimesh(W,F,process=False)))
    return out
_T0={}
def attach(mesh, body):
    """mesh given in the zero-pose print frame; returns function giving its pose in the current pose"""
    pose(); T0=body_T(body); L=np.linalg.inv(T0)
    loc=mesh.copy(); loc.apply_transform(L)
    def cur():
        mm=loc.copy(); mm.apply_transform(body_T(body)); return mm
    return cur
