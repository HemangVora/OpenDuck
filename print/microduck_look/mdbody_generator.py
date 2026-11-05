"""Microduck-look body shells for the Open Duck Mini v2 trunk. Robot frame, mm, +x forward, z up.
Replaces body_middle_top, body_middle_bottom, body_front, body_back, battery_pack_lid. New files only."""
import numpy as np, trimesh, os, sys, json, manifold3d as m3d
OUT=sys.argv[1] if len(sys.argv)>1 else "body_out"; os.makedirs(OUT,exist_ok=True)
# ---- envelope (identical to upstream): y +-55, z -100..43, middle x -95..55, front plate x 55..65, back x -135..-95
W2, ZB, ZT = 55.0, -100.0, 43.0
RT, RB = 19.0, 12.0            # fillet radii top / bottom long edges (inside the upstream chamfers)
T = 3.2                        # skin
ZSPLIT = -13.8
XF0, XF1 = 55.0, 65.0          # front plate
XB0, XB1 = -135.0, -95.0       # back part (flange -100..-95)
XM0, XM1 = -95.0, 55.0         # middle shells
HOLES8 = [(45,17.4),(-45,17.4),(45,-22.3),(-45,-22.3),(45,-62),(-45,-62),(29.4,33),(-29.4,33)]   # (y,z) front/back screw pattern
NECK = (-5.0, 0.0, 100.0, 50.0)         # neck opening on top: cx, cy, sx, sy
TRUNK_HOLES = [(10,10),(10,-10),(-10,10),(-10,-10)]
PAD_TOP = -89.0                         # floor top under trunk_bottom
SHELF_TOP = -82.0                       # rear floor shelf (upstream back flange sits at z -82)
BAY = dict(y=31.0, z0=-82.0, z1=22.0, x0=-122.5, x1=-103.0)   # 62 wide channel for a 58x65x19 3S1P pack + BMS
LID = dict(w=66.0, h=96.0, cz=-30.0, t=3.0, holes=[(27,-74),(-27,-74),(27,14),(-27,14)])
BIG=600
# ---- profile: rounded rectangle offset inward by d, as a closed (y,z) polygon with fixed point count
def profile(d, n=14):
    w=W2-d; zb=ZB+d; zt=ZT-d; rt=max(RT-d,0.3); rb=max(RB-d,0.3)
    pts=[]
    def arc(cy,cz,r,a0,a1):
        for a in np.linspace(a0,a1,n,endpoint=False): pts.append((cy+r*np.cos(a),cz+r*np.sin(a)))
    arc( w-rt, zt-rt, rt, 0, np.pi/2)          # top-right
    arc(-w+rt, zt-rt, rt, np.pi/2, np.pi)      # top-left
    arc(-w+rb, zb+rb, rb, np.pi, 1.5*np.pi)    # bottom-left
    arc( w-rb, zb+rb, rb, 1.5*np.pi, 2*np.pi)  # bottom-right
    return np.array(pts)
def loft(dfun, x0, x1, n=40):
    xs=np.linspace(x0,x1,n); rings=np.array([np.c_[np.full(len(profile(0)),x), profile(dfun(x))] for x in xs])
    P=rings.shape[1]; V=rings.reshape(-1,3); F=[]
    for i in range(n-1):
        for j in range(P):
            a=i*P+j; b=i*P+(j+1)%P; c=(i+1)*P+(j+1)%P; dd=(i+1)*P+j
            F+=[[a,b,c],[a,c,dd]]
    cb=len(V); V=np.vstack([V,rings[0].mean(0)]); F+=[[cb,(j+1)%P,j] for j in range(P)]
    cf=len(V); V=np.vstack([V,rings[-1].mean(0)]); base=(n-1)*P; F+=[[cf,base+j,base+(j+1)%P] for j in range(P)]
    m=trimesh.Trimesh(V,np.array(F),process=True); trimesh.repair.fix_normals(m)
    if m.volume<0: m.invert()
    return m
def prism(d, x0, x1): return loft(lambda x: d, x0, x1, n=2)
def box(x0,x1,y0,y1,z0,z1):
    b=trimesh.creation.box(extents=[x1-x0,y1-y0,z1-z0]); b.apply_translation([(x0+x1)/2,(y0+y1)/2,(z0+z1)/2]); return b
def cyl(r,a0,a1,p,q,axis='z',sections=40):
    c=trimesh.creation.cylinder(radius=r,height=a1-a0,sections=sections)
    if axis=='x': c.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[0,1,0])); c.apply_translation([(a0+a1)/2,p,q])
    elif axis=='y': c.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[1,0,0])); c.apply_translation([p,(a0+a1)/2,q])
    else: c.apply_translation([p,q,(a0+a1)/2])
    return c
def rrect_x(cx,cy,sx,sy,r,z0,z1):   # rounded rect in xy extruded along z
    from shapely.geometry import box as sbox
    poly=sbox(cx-sx/2+r,cy-sy/2+r,cx+sx/2-r,cy+sy/2-r).buffer(r,join_style=1,resolution=12)
    m=trimesh.creation.extrude_polygon(poly,z1-z0); m.apply_translation([0,0,z0]); return m
def rrect_yz(cy,cz,sy,sz,r,x0,x1):  # rounded rect in yz extruded along x
    from shapely.geometry import box as sbox
    poly=sbox(cy-sy/2+r,cz-sz/2+r,cy+sy/2-r,cz+sz/2-r).buffer(r,join_style=1,resolution=12)
    m=trimesh.creation.extrude_polygon(poly,x1-x0)
    m.apply_transform(np.array([[0,0,1,x0],[1,0,0,0],[0,1,0,0],[0,0,0,1]],float)); return m
U=lambda a,b: a.union(b,engine='manifold'); D=lambda a,b: a.difference(b,engine='manifold'); I=lambda a,b: a.intersection(b,engine='manifold')
def finish(n,m):
    m.update_faces(m.unique_faces())
    man=m3d.Manifold(m3d.Mesh(vert_properties=np.asarray(m.vertices,dtype=np.float32), tri_verts=np.asarray(m.faces,dtype=np.uint32)))
    assert man.status()==m3d.Error.NoError,(n,man.status())
    try: man=man.simplify(0.02)
    except Exception: pass
    mm=man.to_mesh(); m=trimesh.Trimesh(np.asarray(mm.vert_properties)[:,:3],np.asarray(mm.tri_verts),process=False)
    comps=[c for c in m.split(only_watertight=False) if abs(c.volume)>1.0]
    if len(comps)!=1: print("!! ",n,"has",len(comps),"solid pieces:",[(round(c.volume),c.bounds.mean(0).round(0).tolist()) for c in sorted(comps,key=lambda c:-c.volume)[1:]])
    m=max(comps,key=lambda c:c.volume) if len(comps)==1 else trimesh.util.concatenate(comps)
    m.export(os.path.join(OUT,n+".stl"))
    return dict(watertight=bool(m.is_watertight),volume_cm3=round(m.volume/1000,1),mass_g_solid=round(m.volume/1000*1.24),bounds=np.round(m.bounds,1).tolist(),faces=len(m.faces),pieces=len(comps))
rep={}
# ================= middle shells =================
skin = D(prism(0, XM0-1, XM1+1), prism(T, XM0-2, XM1+2))          # hollow tube, open both ends
mid_top = I(skin, box(XM0,XM1,-BIG,BIG,ZSPLIT,BIG))
mid_bot = I(skin, box(XM0,XM1,-BIG,BIG,-BIG,ZSPLIT))
# neck opening
cx,cy,sx,sy=NECK; mid_top = D(mid_top, rrect_x(cx,cy,sx,sy,3.0, ZT-10, ZT+5))
# hip openings: no side wall between x -35..35 for |y| > 43 (upstream has none there)
for s in (1,-1): mid_bot = D(mid_bot, box(-35,35, 43*s, 70*s, ZB-1, ZSPLIT+1) if s>0 else box(-35,35,-70,-43,ZB-1,ZSPLIT+1))
# floor: thin skin already there; add trunk pad (top at -89) and rear shelf (top at -82)
mid_bot = U(mid_bot, I(box(-45,XM1,-45,45,ZB,PAD_TOP), prism(T-0.5, XM0-2, XM1+2)))
mid_bot = U(mid_bot, I(box(XM0,-40,-BIG,BIG,SHELF_TOP-T,SHELF_TOP), prism(T-0.5, XM0-2, XM1+2)))
for s in (1,-1): mid_bot = U(mid_bot, I(box(XM0,-40, (W2-T-6)*s, (W2-T+0.5)*s, ZB, SHELF_TOP) if s>0 else box(XM0,-40,-(W2-T+0.5),-(W2-T-6),ZB,SHELF_TOP), prism(T-0.5,XM0-2,XM1+2)))  # shelf side ribs
for (y,z) in TRUNK_HOLES:
    mid_bot = D(mid_bot, cyl(1.6, ZB-1, PAD_TOP+1, y, z) if False else cyl(1.6, ZB-1, PAD_TOP+1, y, z))
    mid_bot = D(mid_bot, cyl(3.25, ZB-1, ZB+4.0, y, z))   # 6.5 counterbore from below, 4 deep (screw head), like upstream z -99..-96
# 8 bosses: cylinders along x at both ends, 9 long, dia 9, 4.0 hole
for (y,z) in HOLES8:
    part = mid_top if z>ZSPLIT else mid_bot
    for (x0,x1) in [(XM1-9,XM1),(XM0,XM0+9)]:
        boss = cyl(4.5,x0,x1,y,z,axis='x')
        if abs(y)>40: web = box(x0,x1, min(y,W2*np.sign(y)), max(y,W2*np.sign(y)), z-4.5, z+4.5)   # web out to the side wall
        else:         web = box(x0,x1, y-4.5, y+4.5, z, ZT)                                           # web up to the top
        part = U(part, I(U(boss,web), prism(0.3,XM0-2,XM1+2)))
        part = D(part, cyl(2.0,x0-1,x1+1,y,z,axis='x'))
    if z>ZSPLIT: mid_top=part
    else: mid_bot=part
rep["md_body_top"]=finish("md_body_top",mid_top); rep["md_body_bottom"]=finish("md_body_bottom",mid_bot)
# ================= front plate (10 thick, rounded edge toward the front face) =================
R_EDGE=6.0
def d_front(x): return 0.0 if x<=XF1-R_EDGE else R_EDGE-np.sqrt(max(R_EDGE**2-(x-(XF1-R_EDGE))**2,0))
front = loft(d_front, XF0, XF1, n=24)
for (y,z) in HOLES8:
    front = D(front, cyl(1.75, XF0-1, XF1+1, y, z, axis='x'))
    front = D(front, cyl(3.25, XF1-5, XF1+1, y, z, axis='x'))     # counterbore 6.5 x 5 deep from the front face
rep["md_body_front"]=finish("md_body_front",front)
# ================= back: flange x -100..-95 (frame), hollow rounded block x -135..-100, rear lid =================
RR=15.0
def d_back(x): return 0.0 if x>=XB0+RR else RR-np.sqrt(max(RR**2-(x-(XB0+RR))**2,0))
back_outer = loft(d_back, XB0, XB1, n=40)
back_inner = loft(lambda x: d_back(x)+T, XB0-0.0, XB1+1, n=40)      # same rounding, offset by T; open toward the flange
REAR_T = 6.5
back_inner = I(back_inner, box(XB0+REAR_T, BIG, -BIG,BIG,-BIG,BIG))    # rear wall 6.5 thick (lid recess 3 + 3.5 left)
back = D(back_outer, back_inner)
# flange: frame ring x -100..-95 is already part of the skin; make the flange solid ring 5 thick around the opening P(T)
back = U(back, D(prism(0,-100,-95), prism(T+0.0,-101,-94)))             # (skin already T; nothing extra) kept for clarity
# flange lower limit: upstream flange spans z -82..43 (sits on the floor shelf): cut skin below -82 for x > -100-RR? keep rear block full height; cut flange region only
back = D(back, box(-100.5,-94, -BIG,BIG, -BIG, SHELF_TOP))
# flange ears around the 8 screw holes (upstream flange has ears reaching in to y +-45), then holes + counterbores from inside
for (y,z) in HOLES8:
    ear = cyl(5.0, -100, -95, y, z, axis='x')
    if abs(y)>40: web = box(-100,-95, min(y,W2*np.sign(y)), max(y,W2*np.sign(y)), z-5, z+5)
    else:         web = box(-100,-95, y-5, y+5, z, ZT)
    back = U(back, I(U(ear,web), prism(0,-101,-94)))
for (y,z) in HOLES8:
    back = D(back, cyl(1.75, -101, -94, y, z, axis='x'))
    back = D(back, cyl(3.0, -103, -97, y, z, axis='x'))
# bay channel ribs (hold a 62 wide pack), shelf at bay z0
b=BAY
shelf = I(box(XB0, -100, -BIG, BIG, b['z0']-3, b['z0']), loft(lambda x: d_back(x)+T-0.5, XB0, XB1+1, n=40))   # full-width shelf, overlaps walls
back = U(back, shelf)
for sg in (1,-1):
    rib = box(XB0+REAR_T-0.5, -100, min(b['y']*sg,(b['y']+2.4)*sg), max(b['y']*sg,(b['y']+2.4)*sg), b['z0']-1, b['z1'])
    back = U(back, I(rib, back_outer))
# rear lid opening + recess + bosses
L=LID
back = D(back, rrect_yz(0, L['cz'], L['w'], L['h'], 6, XB0-1, XB0+T+1))                        # through opening
back = D(back, rrect_yz(0, L['cz'], L['w']+2*8, L['h']+2*8, 8, XB0-1, XB0+L['t']))             # recess for the lid (flush)
for (y,z) in L['holes']:
    back = U(back, I(cyl(4.0, XB0+REAR_T-0.5, XB0+REAR_T+6, y, z, axis='x'), back_outer))
    back = D(back, cyl(2.0, XB0-1, XB0+REAR_T+7, y, z, axis='x'))
rep["md_body_back"]=finish("md_body_back",back)
lid = rrect_yz(0, L['cz'], L['w']+2*8-0.6, L['h']+2*8-0.6, 7.7, XB0, XB0+L['t'])
for (y,z) in L['holes']: lid = D(lid, cyl(1.7, XB0-1, XB0+L['t']+1, y, z, axis='x'))
lid = D(lid, box(XB0-1, XB0+L['t']+1, -8, 8, L['cz']+L['h']/2-2, L['cz']+L['h']/2+6))   # finger notch
rep["md_battery_lid"]=finish("md_battery_lid",lid)
print(json.dumps(rep,indent=1))
json.dump(dict(HOLES8=HOLES8,NECK=NECK,TRUNK_HOLES=TRUNK_HOLES,BAY=BAY,LID=LID,T=T,RT=RT,RB=RB),open(os.path.join(OUT,"md_body_params.json"),"w"),indent=1)
