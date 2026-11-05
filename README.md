# OpenDuck: Open Duck Mini v2 with a Microduck look

An Open Duck Mini v2 (ST3215-HS 12 V servos, 3S 18650, Radxa Zero 3W) with printed Microduck-style shells,
printed on a Bambu Lab A1 in white and black PLA.

| Folder | What is in it |
|---|---|
| `print/3mf/` | stock Open Duck Mini v2 plates, ready for Bambu Studio (A1) |
| `print/microduck_v3/` | current Microduck-look plates (`3mf/`), print list and fasteners (`README.md`) |
| `print/microduck_v2/`, `print/microduck_look/` | earlier versions (`microduck_look/3mf/6m_head_mechanism.3mf` is still used) |
| `print/profiles/` | flattened Bambu Studio profiles used by the CLI slicing scripts |
| `cad/microduck/` | OpenSCAD head/body/legs, `md_foot.py` (feet), `pla_sole.py` (PLA soles for rubber pads), STLs |
| `cad/microduck/checks/` | clearance, sweep, mass and height checks (trimesh + MuJoCo) |
| `tools/servo_setup.py` | servo ID / zero setup with 12 V checks (see `docs/servo-setup-guide.md`) |
| `docs/` | build plan, servo setup guide, shopping lists |
| `research/` | hardware, power, runtime and printing notes |

## Third-party code (not in this repo)

```bash
mkdir -p upstream && cd upstream
git clone https://github.com/apirrone/Open_Duck_Mini.git
git clone -b v2 https://github.com/apirrone/Open_Duck_Mini_Runtime.git
git clone --depth 1 -b support-feetech-sts3215 https://github.com/pollen-robotics/pypot.git
```

## Python environments

```bash
cd tools && uv venv -p 3.11 .venv && uv pip install --python .venv/bin/python pyserial
cd cad/microduck/checks && uv venv .venv && uv pip install --python .venv/bin/python trimesh manifold3d mujoco scipy rtree shapely networkx pillow matplotlib
```
Run heavy checks one at a time under `cad/microduck/checks/guard.sh` (memory guard).
