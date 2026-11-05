# Microduck v3: closer to the real Microduck, white + black only

Built on v2 (`../microduck_v2`). Source CAD: `../../cad/microduck/` (OpenSCAD head/body, `md_foot.py` for the feet).
v2 sources are frozen in `../../cad/microduck/_v2_backup/`. The skeleton, joint axes, servo mounts and every structural
ODM bracket are unchanged, so the MuJoCo model tree and the policy's observations and actions stay the same.

## What changed from v2 (and why: Microduck photo/model)

| Area | v2 | v3 |
|---|---|---|
| Face | white, part of the hood | **black face plate** (separate), recessed in the white hood |
| Eye | thin black bezel | **thick rounded white ring**, glued on, hides the two face screws |
| ToF | inside the eye ring | **pill slot beside the eye** (duck's right), board screwed to the face back |
| Mouth | one black jaw block | **fixed black upper bill + thin lower jaw**, white mouth linings shown when it opens |
| Jaw hub | round disc | **rounded-triangle side plate** with screw dimples |
| Feet | stock ODM tent feet | **rounded slipper feet** (stock foot + skin, every stock hole/interface kept) |
| Body, pillows, deck, panel | v2 | unchanged |

Colour map: Microduck purple = white, yellow = black, grey face = black, blue eye ring = white.

## Plates (Bambu A1, 0.4 nozzle)

| Plate | Colour | Parts | Time | Filament |
|---|---|---|---|---|
| 11a_head_shell_white | white | head_shell (hood) | 9.4 h | 222 g (75 g support) |
| 11b_body_shells_white | white | body_shell_left/right (same as v2) | 2.6 h | 116 g |
| 11c_thigh_pillows_white | white | thigh_pillow_left/right (same as v2) | 1.4 h | 59 g |
| 11bc_body_shells_pillows_white | white | 11b + 11c on one plate (alternative to printing them separately) | 4.0 h | 174 g |
| 11d_eye_mouth_white | white | eye_ring, mouth_jaw, mouth_bill | 0.5 h | 23 g |
| 11d14b_eye_mouth_soles_white | white | 11d + 14b on one plate (alternative to printing them separately) | 1.4 h | 49 g |
| 14b_sole_plates_white | white | foot_bottom_pla x2 (stock part, white = the sole band) | 0.9 h | 27 g |
| 12a_head_jaw_tray_black | black | head_jaw, head_tray | 3.7 h | 104 g |
| 12b_chassis_face_black | black | head_chassis (same as v2), face_bill | 4.2 h | 128 g |
| 12c_body_black | black | deck, panel, guard, clamps (same as v2) | 3.1 h | 73 g |
| 14a_feet_black | black | md_foot_top x2, md_foot_side x2 (replace stock plate 1 feet) | 5.2 h | 132 g |
| **Total** | | | **31 h** | **~880 g** (white ~445 g, black ~435 g) |

Not printed in v3: v2 `eye_bezel`, `tof_tab`; stock `1_feet_orange` foot_top/foot_side (replaced by 14a).
Still needed from the stock set: `8_tpu_soles` in **TPU**. Don't print the soles in PLA: the policy is trained
with rubber-like grip, and a PLA sole will slip.

No TPU? Print `15_pla_soles_rubber_<T>mm_black` (stock sole shape in PLA, bottom trimmed by the rubber thickness T
= 1.0 / 1.5 / 2.0 mm, printed upside down, no support, 0.8 h) and glue a rubber pad of that thickness on the flat face.
Sole + rubber = stock height, so the floor plane, the foot-switch reach and the foot checks are unchanged.
Source: `../../cad/microduck/pla_sole.py`.

Optional two-tone feet (like the Microduck's coloured sole): in Bambu Studio, add a filament change at **12 mm**
on plate 14a (layer slider, right click, "Add color change"), and load white for the first 12 mm.

## Fasteners (changes from v2)

- Hood: 4 more M3 x 5 inserts (bill bosses at x 60 / 92); 4 x M3 x 12 from below through the bill side walls.
  Fit the face_bill before the jaw (the jaw rails cover those screw heads).
- Face to chassis: 2 x M3 x 6 **button head** into the existing chassis face-boss inserts; the eye ring's back pockets cover them.
- Eye ring and both mouth linings: CA glue (the ring sits on the two screw heads).
- ToF (VL53L8CX carrier) on the face back: 2 x M2 x 4 self-tapping into the two bosses beside the window.
- Jaw: unchanged (SG90 horn on the right, M3 pivot on the left).
- Feet: all stock foot screws, unchanged. The skin has access windows for the horn screws and the two cheek bolts.

## Training-safety checks (run 2026-11-04, `../../cad/microduck/checks`)

- Kinematics: no joint, link or actuator change. Same MJCF tree, same 14 actuators, same 101-dim observation.
- Foot contact: the TPU sole is still the only floor contact. The skin reaches the floor only past the stock limits:
  roll 47.5 / 49.0 deg (stock 47.5 / 49.0), heel 65.5 deg (stock 65.5), toe 70.5 deg (stock 89; unreachable).
- Ankle range: the stock foot allows -65 to +47.5 deg, and the new foot keeps exactly that (the skin is carved from the shank sweep).
- Feet vs each other: walking stance gap 103.8 mm. Over 675 turning/roll/swing poses, one extreme pose
  (hip yaw -30 + roll +-15 + pitch -20) gets to 1.6 mm (stock 3.6). Within hip yaw +-15 the minimum is 3.0 mm (stock 3.4).
- Thigh pillows vs new feet: >= 10.4 mm over the full knee x ankle grid.
- Head: all parts single solids, no overlaps. Jaw sweeps 0..17.5 deg with no contact (front drops 25 mm at 15 deg).
  Neck movers >= 7 mm.
- Camera: 49 deg half-angle clear in every direction. Use a **standard IMX219** (62 x 49 deg). The IMX219-160 would see the ring and hood.
- ToF: >= 36 deg half-angle clear (needs 32.5 deg diagonal).
- Neck pitch: the body limits it. Clamp `neck_pitch` to **[-20, +25] deg** in the runtime and in the training command range.

### Mass: update the MJCF before training (planned step)

| | MJCF (trained on) | v2 estimate | v3 estimate |
|---|---|---|---|
| Everything above the head-pitch joint | 453 g | 603 g | 642 g |
| Head COM x (head-pitch axis at x 20) | 32 mm | 39 mm | 44 mm |
| Static torque on head/neck pitch | 0.055 N.m | 0.110 N.m | 0.153 N.m (8 % of ST3215-HS stall) |
| Each foot (printed foot_top + foot_side) | stock | 46 g | 60 g (+14 g) |

Torque margin is fine, but the head is about 190 g heavier than the model, and the feet are 14 g heavier each. Weigh the real printed
head and feet and put the numbers into the MJCF (`head_assembly`, `foot_assembly`, `foot_assembly_2`), along with the 3S pack
and servo changes already planned, before retraining. To trim weight, print 11a with 2 walls.
