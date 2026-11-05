# Microduck v2 shells (OpenSCAD) on the Open Duck Mini v2 skeleton

Source: `../../cad/microduck/` (md_params / md_head / md_body / md_leg / md_vitamins.scad, `parts/*.scad`, `stl/` in robot frame).
Nothing upstream or in `../microduck_look` was changed. Skeleton, joints, ST3215-HS servos and the MuJoCo model stay stock ODM v2.

## Plates (Bambu A1, 0.4 nozzle, 256 mm bed, sliced with the flattened profiles in `../profiles`)

| Plate | Colour | Parts | Time | Filament |
|---|---|---|---|---|
| 11a_head_shell_white | white | head_shell (integral face) | 9.7 h | 244 g (75 g support) |
| 11b_body_shells_white | white | body_shell_left, body_shell_right | 2.6 h | 116 g |
| 11c_thigh_pillows_white | white | thigh_pillow_left, thigh_pillow_right | 1.4 h | 59 g |
| 12a_head_tray_jaw_black | black | head_tray, head_jaw | 3.9 h | 121 g |
| 12b_head_chassis_black | black | head_chassis, tof_tab, eye_bezel | 2.3 h | 70 g |
| 12c_body_black | black | body_deck, body_panel, switch_guard, deck_clamp_rear, deck_clamp_front | 3.1 h | 73 g |
| **Total** | | | **23 h** | **~683 g** (white 419 g, black 264 g) |

Load `3mf/*.3mf` in Bambu Studio. Re-slice with `./slice.sh [white|black|all]` (layouts in `oriented/layout/`).
White uses Bambu PLA Lite 3 walls; black uses Generic PLA 4 walls.

## Fasteners

- Heat-set inserts: M3 x 5 (hole 4.0 x 6 deep) in the head rim bosses, roll-mount ears, tray posts, deck side blocks and rear panel columns.
- Head rim: 7 x M3 x 20 from below through the tray columns into the shell boss inserts.
- Head chassis to roll-mount ears: 4 x M3 x 20 from the top.
- Radxa Zero 3W: 4 x M2.5 x 6 brass standoffs (4 mm thread) into the chassis.
- ToF tab: 2 x M2.5 x 6 into the chassis plate.
- Jaw: right side on the SG90 single-arm horn plus the horn screw (access hole Ø5.5); left side pivots on an M3 pin/screw. SG90 tabs: 2 x M2 self-tapping.
- Body: 4 x M3 button head through the white shells into the deck side inserts; 4 x M3 into the rear panel inserts (the top-right one is M3 x 12 because it also holds the switch guard); 4 x M3 deck clamp bolts with nuts trapped in the two clamp bars under the trunk plate.
- Servo adapter board on the shelf: 4 x M2 self-tapping.
- Thigh pillows: the stock cache screws into the leg_spacer inserts.
- Lengths not given above (jaw pivot, clamp bolts, body side screws): measure at assembly.

## Verification (checks in `../../cad/microduck/checks`, rerun with `./guard.sh .venv/bin/python check_*.py`)

Run 2026-11-04, one process at a time under a 4 GB memory guard:

- Every printed part is one manifold solid. No overlaps between parts or with the electronics. Two exceptions, both by design: the switch cover sits on the switch guard face, and the BMS box touches the deck (3 mm³).
- Head vs moving neck (roll ±30, yaw ±160, pitch ±45): ≥ 7.0 mm (tray), ≥ 7.7 mm (chassis), shell 20.9 mm.
- Body: zero overlap with the fixed trunk hardware. The deck now seats on the measured plate top (z −9.1), with a relief for the 45° plate chamfer.
- Legs: 258 hip/knee poses that the stock body allows, none closer than 2.07 mm to the new body. Neck −20..+20 sweep: 2.05 mm.
- Thigh pillows: knee x ankle ≥ 10.4 mm; hip sweep ≥ 2.9 mm. No pose that the stock cache allows is blocked.

### Head/neck soft limits (new body vs stock)

The neck plates clip the body top when neck pitch goes above about +30° (stock allows up to +60° with head pitch ≤ 0).
The big head also hits at neck +20 / head +15 (stock cleared it by 2.6 mm). Other head-pitch hits are the same as on the stock duck.
Walking is unaffected: the default pose has all head joints at 0, and the upstream runtime forces the gamepad neck-pitch command to 0.
Clamp neck_pitch to [−20°, +30°] in the runtime (and in the training command range if retraining).
