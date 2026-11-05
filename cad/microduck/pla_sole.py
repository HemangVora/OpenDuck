"""PLA stand-in for the stock TPU sole, for a glued-on rubber grip pad.
The bottom is trimmed by the rubber thickness T so that sole + rubber = stock height:
the floor plane, leg length, foot-switch reach and every v3 foot-clearance check stay the same.
Outputs (print-oriented: flat top face on the bed, trimmed face up):
  stl/pla_sole_T{T}.stl
Run: checks/.venv/bin/python pla_sole.py
"""
import numpy as np, trimesh, manifold3d as m3d, os
U = "/Users/hemangvora/OpenDuck/upstream/Open_Duck_Mini/print/foot_bottom_tpu.stl"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stl/")
FLOOR, TOP = -261.62, -253.62
t = trimesh.load(U, force="mesh")
M = m3d.Manifold(m3d.Mesh(vert_properties=np.asarray(t.vertices, np.float32), tri_verts=np.asarray(t.faces, np.uint32)))
for T in (1.0, 1.5, 2.0):
    cut = M ^ m3d.Manifold.cube([400, 400, TOP - FLOOR - T]).translate([-200, -100, FLOOR + T])
    mm = cut.to_mesh(); s = trimesh.Trimesh(np.asarray(mm.vert_properties)[:, :3], np.asarray(mm.tri_verts))
    sec, _ = t.section([0, 0, 1], [0, 0, FLOOR + T + 0.01]).to_2D()
    s.apply_transform(trimesh.transformations.rotation_matrix(np.pi, [1, 0, 0]))   # flip: top face down
    s.apply_translation(-s.bounds[0])
    s.export(OUT + f"pla_sole_T{T}.stl")
    print(f"T {T}: height {s.extents[2]:.2f} mm, trimmed face {sec.bounds[1][0]-sec.bounds[0][0]:.1f} x {sec.bounds[1][1]-sec.bounds[0][1]:.1f} mm, watertight {s.is_watertight}, pieces {len(s.split(only_watertight=False))}")
