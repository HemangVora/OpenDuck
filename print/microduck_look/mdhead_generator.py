"""Microduck-look head for Open Duck Mini v2 skeleton. Robot frame, mm. +x forward, z up.
Outputs new STLs only (existing upstream files untouched)."""
import numpy as np, trimesh, os, sys, json
from scipy.interpolate import PchipInterpolator
OUT=sys.argv[1] if len(sys.argv)>1 else "out"; os.makedirs(OUT,exist_ok=True)
# ---------------- parameters ----------------
X_BACK, X_FRONT = -60.0, 146.0      # loft extent (front gets cut by the leaning plane)
Z0 = 109.7                          # bottom of tray = ODM head_bot_sheet bottom
H  = 84.0                           # outer height at the front crown
W  = 75.0                           # outer half width at the front
T  = 2.5                            # wall
Z_SPLIT = 123.7                     # tray / top-shell split
FLOOR = 3.0
LEAN = 6.0                          # front edge leans forward by this over H
FACE_X = 128.0                      # back face of the face plate (plate FACE_X-3 .. FACE_X)
CAM = (0.0, 156.0, 16.0)            # y, z, dia of camera hole
TOF = (22.0, 156.0, 10.0)           # y, z, square window
ROLL_BOSS = [(65,27.4),(65,-27.4),(95,27.4),(95,-27.4)]; ROLL_BOSS_Z=158.4
NECK_OPEN = (20.0, 0.0, 100.0, 8.0) # centre x,y, size, corner r  (identical to ODM sheet)
L = X_FRONT - X_BACK
# ---------------- reference-derived profile functions (normalised u = (x-X_BACK)/L) --------------
# plan half-width fraction of W (from Microduck top shell z=114/125 sections)
_u = np.array([0.0,0.01,0.095,0.18,0.265,0.35,0.53,0.70,0.86,0.95,1.0])
_w = np.array([0.0,0.30,0.687,0.794,0.845,0.84,0.886,0.919,0.95,0.998,1.0])
wfun = PchipInterpolator(_u,_w)
def w_out(u): return W*np.clip(wfun(np.clip(u,0,1)),0,1)
# centreline top height fraction of H (side profile): vertical back to 0.36, round to 0.87 at u=0.28, slope to 1.0
def h_frac(u):
    u=np.asarray(u,float); z=np.empty_like(u)
    a=u<0.28; z[a]=0.36+(0.87-0.36)*np.sqrt(np.clip(1-((0.28-u[a])/0.28)**2,0,1))
    z[~a]=0.87+0.13*(u[~a]-0.28)/0.72
    return z
def h_out(u): return Z0+H*h_frac(u)
# cross-section: vertical to z1 = zb + 0.40*(h-zb), then y = w*(1-k t)*(1-t^n)^(1/n)
K,N = 0.30, 5.0
def section(w,h,zb,m=40):
    """closed outline (y,z), vertical from zb to Z_SPLIT then slanted superellipse to the crown"""
    z1 = Z_SPLIT if h>Z_SPLIT+2 else zb+0.4*(h-zb)
    t = np.linspace(0,1,m)
    yy = w*(1-K*t)*np.power(np.clip(1-t**N,0,1),1/N)
    zz = z1 + t*(h-z1)
    right = np.c_[np.r_[w, yy], np.r_[zb, zz]]        # from (w,zb) up to (0,h)
    left  = right[::-1].copy(); left[:,0]*=-1          # from (0,h) down to (-w,zb)
    pts = np.vstack([right, left[1:]])                 # top point shared
    return pts                                         # not repeating the first point
def loft(wf, hf, zb, x0, x1, n=160, m=40):
    xs=np.linspace(x0,x1,n); us=(xs-X_BACK)/L
    rings=[]; 
    for x,u in zip(xs,us):
        w=max(wf(u),0.01); h=hf(u); 
        s=section(w,h,zb,m); rings.append(np.c_[np.full(len(s),x),s])
    rings=np.array(rings)             # n x P x 3
    P=rings.shape[1]; V=rings.reshape(-1,3); F=[]
    for i in range(n-1):
        for j in range(P):
            a=i*P+j; b=i*P+(j+1)%P; c=(i+1)*P+(j+1)%P; d=(i+1)*P+j
            F.append([a,b,c]); F.append([a,c,d])
    # caps: back (fan) and front (fan)
    cb=len(V); V=np.vstack([V, rings[0].mean(0)]); 
    for j in range(P): F.append([cb,(j+1)%P,j])
    cf=len(V); V=np.vstack([V, rings[-1].mean(0)]); base=(n-1)*P
    for j in range(P): F.append([cf,base+j,base+(j+1)%P])
    mesh=trimesh.Trimesh(V,np.array(F),process=True)
    mesh.merge_vertices(); mesh.update_faces(mesh.nondegenerate_faces()); mesh.remove_unreferenced_vertices()
    trimesh.repair.fix_normals(mesh)
    if mesh.volume<0: mesh.invert()
    return mesh
def offset_loft(t, zb, x0=None, x1=None):
    return loft(lambda u: w_out(u)-t, lambda u: h_out(u)-t, zb, (X_BACK+t) if x0 is None else x0, X_FRONT+10 if x1 is None else x1)
def box(x0,x1,y0,y1,z0,z1):
    b=trimesh.creation.box(extents=[x1-x0,y1-y0,z1-z0]); b.apply_translation([(x0+x1)/2,(y0+y1)/2,(z0+z1)/2]); return b
def cyl(r,z0,z1,x,y,axis='z',sections=48):
    c=trimesh.creation.cylinder(radius=r,height=z1-z0,sections=sections)
    if axis=='x': c.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[0,1,0]))
    c.apply_translation([x,y,(z0+z1)/2] if axis=='z' else [(z0+z1)/2,y,x]); return c
def rrect_prism(cx,cy,sx,sy,r,z0,z1):
    from shapely.geometry import box as sbox
    poly=sbox(cx-sx/2+r,cy-sy/2+r,cx+sx/2-r,cy+sy/2-r).buffer(r,join_style=1,resolution=16)
    m=trimesh.creation.extrude_polygon(poly,z1-z0); m.apply_translation([0,0,z0]); return m
def U(a,b): return a.union(b,engine='manifold')
def D(a,b): return a.difference(b,engine='manifold')
def I(a,b): return a.intersection(b,engine='manifold')
# ---------------- solids ----------------
outer = loft(w_out,h_out,Z0,X_BACK,X_FRONT)
inner = offset_loft(T, Z0-5)
# leaning front plane: keep x <= 134 + LEAN*(z-Z0)/H   -> normal pointing to +x side removed
_n=np.array([H,0,-LEAN]); _n=_n/np.linalg.norm(_n)
_cutbox=trimesh.creation.box(extents=[1000,1000,1000])
_ang=np.arctan2(LEAN,H)
_cutbox.apply_transform(trimesh.transformations.rotation_matrix(_ang,[0,1,0]))
_cutbox.apply_translation(np.array([134,0,Z0])+_n*500)
def lean_cut(m):
    return m.difference(_cutbox,engine='manifold')
outer=lean_cut(outer); inner=lean_cut(inner)
shell_full = D(outer, inner)
BIG=500
top_shell = I(shell_full, box(-BIG,BIG,-BIG,BIG,Z_SPLIT,BIG))
tray      = I(shell_full, box(-BIG,BIG,-BIG,BIG,Z0,Z_SPLIT))
# tray floor: inner solid between Z0 and Z0+FLOOR
floor = I(lean_cut(offset_loft(T-0.01, Z0-1)), box(-BIG,BIG,-BIG,BIG,Z0,Z0+FLOOR))
tray = U(tray, floor)
# registration lip on tray: between inner(T+0.25) and inner(T+1.65), z split..split+3
lipA = I(D(lean_cut(offset_loft(T-0.6,Z0-5)), lean_cut(offset_loft(T+1.65,Z0-5))), box(-BIG,BIG,-BIG,BIG,Z_SPLIT-2.5,Z_SPLIT))      # ledge overlapping the tray wall
lipB = I(D(lean_cut(offset_loft(T+0.25,Z0-5)), lean_cut(offset_loft(T+1.65,Z0-5))), box(-BIG,BIG,-BIG,BIG,Z_SPLIT-0.01,Z_SPLIT+3))  # lip inside the top shell
lip = U(lipA, lipB)
tray = U(tray, lip)
# neck opening + rim screw holes in floor
cx,cy,sz,rr = NECK_OPEN
tray = D(tray, rrect_prism(cx,cy,sz,sz,rr,Z0-1,Z0+FLOOR+1))
# rim bosses (top shell -> floor screws, M3 insert in boss, 3.2 clearance in floor)
def w_in_at(x): return w_out((x-X_BACK)/L)-T
rim_xy=[]
for x in [-30.0, 20.0, 70.0, 118.0]:
    y=w_in_at(x)-3.5; rim_xy += [(x,y),(x,-y)]
rim_xy += [(-50.0,0.0)]   # one at the back centre
for (x,y) in rim_xy:
    web = box(x-4,x+4, min(y,0)-(0 if y<=0 else 0), max(y,0), Z0+FLOOR, Z_SPLIT+10) if abs(y)>1 else box(x-80,x+4,-4,4,Z0+FLOOR,Z_SPLIT+10)
    if abs(y)>1: web = box(x-4,x+4, min(y, 80*np.sign(y)), max(y, 80*np.sign(y)), Z0+FLOOR, Z_SPLIT+10)   # web out to the side wall
    top_shell = U(top_shell, I(U(cyl(4.0, Z0+FLOOR, Z_SPLIT+10, x, y), web), lean_cut(offset_loft(0.3, Z0-5))))
    top_shell = D(top_shell, cyl(2.0, Z0+FLOOR-1, Z0+FLOOR+8, x, y))      # 4.0 mm insert hole, 8 deep
    tray = D(tray, cyl(1.6, Z0-1, Z0+FLOOR+1, x, y))                         # 3.2 through
    tray = D(tray, cyl(3.1, Z0-1, Z0+1.5, x, y))                             # counterbore for M3 head
    tray = D(tray, cyl(4.3, Z0+FLOOR-0.01, Z_SPLIT+4, x, y))                 # clear the boss through tray wall zone
# roll-mount cage: 2 mm walls x 60..100, y +-33.4, from ceiling down to ROLL_BOSS_Z, with 4 corner bosses
cage_out = box(58-2,102+2,-34.4-2,34.4+2,ROLL_BOSS_Z,BIG); cage_in=box(58,102,-34.4,34.4,ROLL_BOSS_Z-1,BIG)
cage = D(cage_out,cage_in)
for (x,y) in ROLL_BOSS: cage = U(cage, cyl(6.0, ROLL_BOSS_Z, BIG, x, y, sections=32))
cage = I(cage, lean_cut(offset_loft(T-0.3, Z0-5)))     # trim to inside of the shell (slightly overlapping the wall)
top_shell = U(top_shell, cage)
for (x,y) in ROLL_BOSS: top_shell = D(top_shell, cyl(2.0, ROLL_BOSS_Z-1, ROLL_BOSS_Z+8, x, y))
# face plate bosses: 2 from ceiling, 2 from tray floor, at x=FACE_X-3-4 .. FACE_X-3 (behind plate)
u_face=(FACE_X-X_BACK)/L; wi=w_out(u_face)-T; hi=h_out(u_face)-T
fb_top=[( 38.0, 176.0),(-38.0, 176.0)]; fb_bot=[( wi-14, Z0+FLOOR+12),(-(wi-14), Z0+FLOOR+12)]
bx0, bx1 = FACE_X-3-8, FACE_X-3
for (y,z) in fb_top:
    top_shell = U(top_shell, box(bx0,bx1,y-5,y+5,z-5,BIG))      # column up to ceiling
    top_shell = D(top_shell, cyl(2.0, bx0-1, bx1+1, z, y, axis='x'))
for (y,z) in fb_bot:
    tray = U(tray, box(bx0,bx1,y-5,y+5,Z0+FLOOR-0.01,z+5))
    tray = D(tray, cyl(2.0, bx0-1, bx1+1, z, y, axis='x'))
top_shell = I(top_shell, lean_cut(outer))   # keep everything inside the outer skin
tray      = I(tray, lean_cut(outer))
# ---------------- face plate ----------------
from shapely.geometry import Polygon
_ref = lean_cut(offset_loft(T+2.2, Z0-5))
_s = _ref.section(plane_origin=[FACE_X-3,0,0],plane_normal=[1,0,0])
_Q = max([np.array(d) for d in _s.discrete], key=len)
poly = Polygon([(q[1],q[2]) for q in _Q]).buffer(-0.3)
poly = poly.intersection(Polygon([(-200,Z0+FLOOR+0.5),(200,Z0+FLOOR+0.5),(200,400),(-200,400)]))
fp=trimesh.creation.extrude_polygon(poly, 3.0)       # extruded along local z -> map local (x,y,z)->(y,z,x)
fp.apply_transform(np.array([[0,0,1,FACE_X-3],[1,0,0,0],[0,1,0,0],[0,0,0,1]],float))
fp = D(fp, cyl(CAM[2]/2, FACE_X-5, FACE_X+2, CAM[1], CAM[0], axis='x'))
fp = D(fp, box(FACE_X-5,FACE_X+2, TOF[0]-TOF[2]/2, TOF[0]+TOF[2]/2, TOF[1]-TOF[2]/2, TOF[1]+TOF[2]/2))
for (y,z) in fb_top+fb_bot: fp = D(fp, cyl(1.7, FACE_X-5, FACE_X+2, z, y, axis='x'))
# ---------------- bezel ring ----------------
ring = D(cyl(21.0, FACE_X, FACE_X+6, CAM[1], CAM[0], axis='x', sections=96), cyl(9.0, FACE_X-1, FACE_X+7, CAM[1], CAM[0], axis='x', sections=96))
ring = D(ring, D(cyl(21.0, FACE_X+4, FACE_X+7, CAM[1], CAM[0], axis='x', sections=96), cyl(16.0, FACE_X+3, FACE_X+8, CAM[1], CAM[0], axis='x', sections=96)))
parts={"md_head_top":top_shell,"md_head_tray":tray,"md_face_plate":fp,"md_cam_ring":ring}
rep={}
for n,m in parts.items():
    m.update_faces(m.unique_faces())
    import manifold3d as m3d
    _man=m3d.Manifold(m3d.Mesh(vert_properties=np.asarray(m.vertices,dtype=np.float32), tri_verts=np.asarray(m.faces,dtype=np.uint32)))
    assert _man.status()==m3d.Error.NoError, (n,_man.status())
    try: _man=_man.simplify(0.02)
    except Exception: pass
    _mm=_man.to_mesh(); m=trimesh.Trimesh(np.asarray(_mm.vert_properties)[:,:3],np.asarray(_mm.tri_verts),process=False)
    _comps=[c for c in m.split(only_watertight=False) if abs(c.volume)>1.0]
    if len(_comps)!=1: print("!! ",n,"has",len(_comps),"solid pieces:",[(round(c.volume),c.bounds.mean(0).round(0).tolist()) for c in sorted(_comps,key=lambda c:-c.volume)[1:]])
    m=_comps[0] if len(_comps)==1 else trimesh.util.concatenate(_comps)
    rep[n]=dict(watertight=bool(m.is_watertight), volume_cm3=round(float(m.volume)/1000,1), mass_g_pla=round(float(m.volume)/1000*1.24,0),
               bounds=np.round(m.bounds,1).tolist(), faces=len(m.faces))
    m.export(os.path.join(OUT,n+".stl"))
print(json.dumps(rep,indent=1))
json.dump(dict(rim_xy=rim_xy, roll_boss=ROLL_BOSS, face_bosses=dict(top=fb_top,bot=fb_bot), params=dict(X_BACK=X_BACK,X_FRONT=X_FRONT,Z0=Z0,H=H,W=W,T=T,Z_SPLIT=Z_SPLIT,FACE_X=FACE_X,CAM=CAM,TOF=TOF)), open(os.path.join(OUT,"md_head_params.json"),"w"), indent=1)
