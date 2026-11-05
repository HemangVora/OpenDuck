"""Microduck-look feet for the Open Duck Mini v2 (v3).

md_foot_top  = stock foot_top  + outer half of a rounded slipper skin
md_foot_side = stock foot_side + inner half of the skin
The stock parts are kept whole (every hole, horn seat and bolt interface is untouched).
The skin only lives where nothing moves and nothing needs access:
  - outside the tent interior between the cheeks (y 72.15..109.05) except at the toe/heel caps,
  - clear of the PLA plate and its pocket, the deck slots, the horn screws and the two cheek bolts,
  - clear of the shank's swept volume over every ankle angle the stock foot allows (+1.5 mm).
Contact stays stock: the skin bottom is 11.2 mm above the TPU sole bottom.
Both feet use the same two parts (ODM feet are translated copies, not mirrored).
Frame: robot/print frame, left foot at zero pose, mm.

Run: checks/.venv/bin/python md_foot.py   (from cad/microduck)
"""
import numpy as np, trimesh, manifold3d as m3d, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "checks"))
import asm

U = "/Users/hemangvora/OpenDuck/upstream/Open_Duck_Mini/print/"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stl/")

# ---------------- parameters ----------------
X0, X1 = -60.0, 52.0          # skin plan length (stock -55.65..47.81)
Y0, Y1 = 62.65, 118.55        # skin plan width: stock 67.15..114.05 + 4.5 mm each side (each side is the inner side on one foot)
R_TOE, R_HEEL = 20.0, 16.0    # plan corner radii
Z_BOT, Z_TOP = -250.0, -228.0 # skin bottom (floor is -261.62) and top (ankle axis -222.4)
R_TOP = 5.0                   # rounded top edge
CHAMF = 3.0                   # bottom outer chamfer
CHEEK_IN = (72.15, 109.05)    # cheek inner faces
DECK_BOT = -245.2             # deck underside / plate pocket top
TOE_FILL_X, HEEL_FILL_X = 34.0, -46.0   # caps between the cheeks only beyond these x
AXIS = (-16.1, -222.4)        # ankle axis (x, z), along y
HORN_WIN_R = 12.5             # window around the horn screws (screws at r 7, heads 6)
BOLTS = [(-43.25, -241.5), (29.5, -241.5)]   # cheek-joining bolt heads on the inner face (y 67.15)
BOLT_WIN_D = 7.5
SPLIT_Y = 79.15               # foot_side | foot_top joint plane
SWEEP_CLR = 1.5
# underside bevels: planes through the TPU contact-face edges, so the skin never reaches the floor before
# the stock foot would (stock: roll 47.5 deg, toe 89, heel 65.5; TPU contact face x -45.92..41.97, y 80.63..99.58)
FLOOR = -261.62
TPU_FACE = (-45.92, 41.97, 80.63, 99.58)
BEVEL_ROLL, BEVEL_TOE, BEVEL_HEEL = 49.0, 61.0, 56.0

def MAN(t): return m3d.Manifold(m3d.Mesh(vert_properties=np.asarray(t.vertices, np.float32), tri_verts=np.asarray(t.faces, np.uint32)))
def TM(M):
    mm = M.to_mesh(); t = trimesh.Trimesh(np.asarray(mm.vert_properties)[:, :3], np.asarray(mm.tri_verts))
    parts = [c for c in t.split(only_watertight=False) if abs(c.volume) > 1.0]      # drop zero-volume slivers from the cuts
    return trimesh.util.concatenate(parts) if len(parts) > 1 else parts[0]
def box(x0, x1, y0, y1, z0, z1): return m3d.Manifold.cube([x1 - x0, y1 - y0, z1 - z0]).translate([x0, y0, z0])

def plan(inset):
    """rounded plan rectangle with different toe/heel radii, inset by `inset`"""
    pts = []
    def arc(cx, cy, r, a0, a1):
        for a in np.linspace(a0, a1, 24): pts.append((cx + r * np.cos(a), cy + r * np.sin(a)))
    rt, rh = max(R_TOE - inset, 0.5), max(R_HEEL - inset, 0.5)
    x0, x1, y0, y1 = X0 + inset, X1 - inset, Y0 + inset, Y1 - inset
    arc(x1 - rt, y0 + rt, rt, -np.pi / 2, 0); arc(x1 - rt, y1 - rt, rt, 0, np.pi / 2)
    arc(x0 + rh, y1 - rh, rh, np.pi / 2, np.pi); arc(x0 + rh, y0 + rh, rh, np.pi, 1.5 * np.pi)
    return m3d.CrossSection([pts])

def slipper():
    """plan-rounded block with a filleted top edge and a chamfered bottom edge (stacked slices)"""
    parts = []
    n = 20
    for i in range(n):                                     # top fillet
        a0, a1 = np.pi / 2 * i / n, np.pi / 2 * (i + 1) / n
        z0 = Z_TOP - R_TOP + R_TOP * np.sin(a0); z1 = Z_TOP - R_TOP + R_TOP * np.sin(a1)
        ins = R_TOP - R_TOP * np.cos(a1)
        parts.append(m3d.Manifold.extrude(plan(ins), z1 - z0).translate([0, 0, z0]))
    mid0 = Z_BOT + CHAMF
    parts.append(m3d.Manifold.extrude(plan(0), Z_TOP - R_TOP - mid0).translate([0, 0, mid0]))
    for i in range(4):                                     # bottom chamfer
        z0 = Z_BOT + CHAMF * i / 4; z1 = Z_BOT + CHAMF * (i + 1) / 4
        parts.append(m3d.Manifold.extrude(plan(CHAMF * (1 - (i + 0.5) / 4)), z1 - z0).translate([0, 0, z0]))
    return m3d.Manifold.batch_boolean(parts, m3d.OpType.Add)

def shank_keepout(stock):
    """union of the shank part hulls (inflated) over every ankle angle the stock foot allows"""
    asm.pose(); Tf0 = asm.body_T("foot_assembly")
    allowed, hulls = [], []
    for a in np.arange(-90, 90.1, 2.5):
        asm.pose({"left_ankle": a}); M = Tf0 @ np.linalg.inv(asm.body_T("foot_assembly"))
        meshes, names = [], []
        for mn, b, t in asm.geoms(["knee_and_ankle_assembly_2"]):
            t = t.copy(); t.apply_transform(M); meshes.append(t); names.append(mn)
        # stock-allowed? real meshes vs stock foot (manifold where possible)
        hit = 0.0
        for (mn, t) in zip(names, meshes):
            if "palonier" in mn: continue          # horns seat in the cheeks by design (same overlap at every angle)
            Mt = MAN(t)
            if Mt.status() == m3d.Error.NoError: hit += (Mt ^ stock).volume()
        if hit > 1.0: continue
        allowed.append(a)
        for t in meshes:
            V = t.convex_hull.vertices
            dirs = np.array([[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]] + [[sx,sy,sz] for sx in (-1,1) for sy in (-1,1) for sz in (-1,1)], float)
            dirs /= np.linalg.norm(dirs, axis=1, keepdims=True)
            P = (V[:, None, :] + SWEEP_CLR * dirs[None]).reshape(-1, 3)
            hulls.append(m3d.Manifold.hull_points(P.astype(np.float32)))
    print(f"stock-allowed ankle angles: {min(allowed)} .. {max(allowed)} deg ({len(allowed)} samples)")
    return m3d.Manifold.batch_boolean(hulls, m3d.OpType.Add), allowed

def main():
    ft = trimesh.load(U + "foot_top.stl", force="mesh"); fs = trimesh.load(U + "foot_side.stl", force="mesh")
    pl = trimesh.load(U + "foot_bottom_pla.stl", force="mesh")
    FT, FS, PL = MAN(ft), MAN(fs), MAN(pl)
    stock = FT + FS + PL
    skin = slipper()
    big = 400
    # tent interior between the cheeks (servo space, deck slots) except the toe/heel caps above the deck
    interior = box(HEEL_FILL_X, TOE_FILL_X, CHEEK_IN[0], CHEEK_IN[1], DECK_BOT, 0)
    pocket = box(-54.2, 40.7, 75.6, 104.4, -270, DECK_BOT + 0.05)                # PLA plate + pocket
    horn = m3d.Manifold.cylinder(big, HORN_WIN_R, HORN_WIN_R, 96).rotate([-90, 0, 0]).translate([AXIS[0], -big / 2, AXIS[1]])
    bolts = [m3d.Manifold.cylinder(114.05 - 40, BOLT_WIN_D / 2, BOLT_WIN_D / 2, 48).rotate([-90, 0, 0]).translate([x, 40, z]) for x, z in BOLTS]   # through to the outer cheek face: keeps the screw path in foot_top open
    keep, allowed = shank_keepout(stock)
    big2 = 600
    below = m3d.Manifold.cube([big2, big2, big2]).translate([-big2 / 2, -big2 / 2, -big2])   # z < 0
    bevels = [below.rotate([BEVEL_ROLL, 0, 0]).translate([0, TPU_FACE[3], FLOOR]),          # rises toward +y
              below.rotate([-BEVEL_ROLL, 0, 0]).translate([0, TPU_FACE[2], FLOOR]),         # rises toward -y
              below.rotate([0, -BEVEL_TOE, 0]).translate([TPU_FACE[1], 0, FLOOR]),          # rises toward +x
              below.rotate([0, BEVEL_HEEL, 0]).translate([TPU_FACE[0], 0, FLOOR])]          # rises toward -x
    for b in bevels: skin = skin - b
    skin = skin - interior - pocket - horn - keep - PL
    for b in bolts: skin = skin - b
    side_half = skin ^ box(-big, big, -big, SPLIT_Y, -big, big)
    top_half = skin - box(-big, big, -big, SPLIT_Y, -big, big)
    new_top, new_side = FT + top_half, FS + side_half
    os.makedirs(OUT, exist_ok=True)
    for n, M in [("md_foot_top", new_top), ("md_foot_side", new_side), ("md_foot_skin_only", skin)]:
        t = TM(M); t.export(OUT + n + ".stl")
        pc = sorted([abs(c.volume) for c in t.split(only_watertight=False)], reverse=True)
        print(f"{n:18s} vol {t.volume/1000:6.1f} cm3 bounds {t.bounds.round(1).tolist()} pieces {len(pc)} {[round(v,1) for v in pc[:6]]}")
    print(f"stock foot_top {ft.volume/1000:.1f} cm3, foot_side {fs.volume/1000:.1f} cm3")

if __name__ == "__main__":
    main()
