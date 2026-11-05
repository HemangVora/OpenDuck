# Open Duck Mini v2 — hardware research for the India build (ST3215 12 V / 3S / Radxa Zero 3W / IMX219 + VL53L8CX)

Researched 2026-10-28 against the `v2` branch of https://github.com/apirrone/Open_Duck_Mini (repo default branch is `v2`; 4,547 stars, 577 forks per the GitHub API). All part dimensions marked "measured" come from parsing the repo's binary STLs with a stdlib-only Python script (bounding boxes, plane slices and orthographic depth renders); the STLs are exported in one shared assembly frame (robot +X = forward, +Z = up), so coordinates below are assembly-frame millimetres. Scratch files (STLs, downloaded guide photos, renders, scripts) are under `/private/tmp/claude-501/-Users-hemangvora/c8a30d1f-0498-4660-9327-b47c73ee9657/scratchpad/agents/odm-hardware/`.

Primary sources used throughout:

- README: https://github.com/apirrone/Open_Duck_Mini/blob/v2/README.md
- Print guide: https://github.com/apirrone/Open_Duck_Mini/blob/v2/docs/print_guide.md
- Assembly guide: https://github.com/apirrone/Open_Duck_Mini/blob/v2/docs/assembly_guide.md
- Wiring diagram: https://github.com/apirrone/Open_Duck_Mini/blob/v2/docs/open_duck_mini_v2_wiring_diagram.png
- BOM (Google Sheet, exported as CSV): https://docs.google.com/spreadsheets/d/1gq4iWWHEJVgAA_eemkTEsshXqrYlFxXAPwO515KpCJc/edit?usp=sharing
- Runtime: https://github.com/apirrone/Open_Duck_Mini_Runtime (branch `v2`)
- Onshape CAD link (from README): https://cad.onshape.com/documents/64074dfcfa379b37d8a47762/w/3650ab4221e215a4f65eb7fe/e/0505c262d882183a25049d05

---

## 1. Mechanical layout — where everything lives

### Summary table

| Component | Location | Evidence |
|---|---|---|
| Raspberry Pi Zero 2W | **Head**, on 4 standoffs on the head floor, front-left area; no pocket, open floor | Assembly guide "Head" section: "insert the bearing, mount the ear motors and the raspberry pi zero 2w"; interior photo https://github.com/user-attachments/assets/91284081-a563-4c02-bb3d-194b3afbc25c ; `head.stl` render (4 bosses at 58 × 23 mm pitch) |
| 5 V regulator (HENGE UBEC, BOM "5V regulator") | **Head** (wiring diagram draws the UBEC inside the "Head" box, fed by the 7.4 V pack line, 5 V out to the Pi) | https://github.com/apirrone/Open_Duck_Mini/blob/v2/docs/open_duck_mini_v2_wiring_diagram.png ; BOM row "5V regulator" https://www.alibaba.com/product-detail/HENGE-4A-6A-8A-12A-UBEC_1601260325461.html |
| Servo driver board (Waveshare Bus Servo Adapter (A), 42 × 33 mm) | **Trunk**, on a lowered tray at the rear of `trunk_top` (assembly X ≈ −90…−45, four bosses at ≈37 × 28 mm pitch), behind the neck, inside `body_middle` | Guide says "Mount the servo driver board — TODO take a photo"; the green board is visible behind the neck in CAD photos https://github.com/user-attachments/assets/f96fe44f-a7bc-423e-a925-4aef3e7bf568 and https://github.com/user-attachments/assets/03f3bdae-06c3-4c37-b68f-14587edd6123 ; `trunk_top.stl` render; the Jetson fork's layout doc also records "Servo-driver board … the board's original trunk_top tray pocket" at trunk-frame (−63.5, 16.5, 60.4) mm https://github.com/XiaohuiChen-personal/Open_Duck_Mini_Jetson/blob/v2/docs/jetson-mod/component_layout_v2.md |
| IMU (Adafruit BNO055) | **Trunk**, screwed (4 screws) onto the top face of the raised block of `trunk_top`, directly behind the neck-pitch servo | Guide "Mount the IMU" photos https://github.com/user-attachments/assets/8772996d-5906-48fa-8cbe-6b6823982375 and https://github.com/user-attachments/assets/172f44c7-c7c6-47f8-894a-14024abd24f4 ; note in guide: mounting it upside-down is fine, set `imu_upside_down` in `duck_config.json` |
| Battery pack (2 × 18650 holder + 2S BMS + USB-C charger board + power switch + barrel jack) | **`body_back`** (rear body shell). Cells vertical in a rail pocket; BMS in a slot to the left of the pocket; USB-C charger board in a pocket above; switch and jack through the shell | Guide "Battery pack" renders https://github.com/user-attachments/assets/371db809-7cb3-47e1-b277-7fc2bdf21025 and https://github.com/user-attachments/assets/3acfa4e6-ecf7-41f6-a965-35a3040f52fb ; `body_back.stl` render/slices |
| Bearings (3 × 6804ZZ) | 2 in `trunk_bottom` (hip-yaw axes), 1 in the head (head-roll rear pivot) | see §7 |
| Antenna 9 g servos, eye LEDs, projector, speaker (MAX98357A), mic, camera | Head | Guide pin-map table; wiring diagram |

### Head (Pi/Radxa pocket) — measured from `head.stl` and `head_bot_sheet.stl`

- `head.stl` bounding box 199.8 × 197.3 × 59.4 mm (assembly X −79.8…120, Y ±98.7, Z 109.7…169.1). The head is a 5-sided shell closed underneath by `head_bot_sheet.stl` (193.8 × 191.6 × 3 mm).
- Interior floor is open, trapezoidal: ≈198 mm long (X) and ≈190 mm wide at the front/wide end (+X) narrowing to ≈105 mm at the rear. Interior height ≈ 46 mm (bot-sheet top at Z ≈ 112.7 to roof at ≈ 158).
- Pi mount: four bosses at **57.4 × 23 mm** pitch (measured on the render, i.e. the Pi Zero 58 × 23 pattern), at X ≈ +26…+84, Y ≈ +37…+60 (front, left of centre). Four larger bosses at ≈30 × 54 mm pitch at X ≈ 65…95, Y ±27 carry `head_roll_mount` (the roll servo). A speaker grille is at the front-right, a standing bearing holder at X ≈ −27 (rear), and small camera/LED holes on the front face (visible in https://github.com/user-attachments/assets/ef4cd513-6b8d-41fa-9cc3-149fc8333d3e and https://github.com/user-attachments/assets/679a9cd2-89ca-41e8-9d03-f93fc040068b).
- **Radxa Zero 3W fit**: Radxa's 2D DXF (https://dl.radxa.com/zero3/docs/hw/3w/radxa_zero_3w_2d_dxf.zip, `radxa_zero_3w_v1110_top.dxf`) has four Ø2.82 mm holes at (3.55, 3.60), (3.60, 26.45), (61.40, 3.60), (61.40, 26.50) → **57.85 × 22.9 mm pitch, identical to the Pi Zero**, board 65 × 30 mm (https://docs.radxa.com/en/zero/zero3). It drops onto the stock standoffs. Differences that matter for the head: both USB-C ports and the micro-HDMI are on one long edge (the Pi Zero's micro-USB are on the other long edge), and the CSI is "1x4 lane MIPI CSI (22-Pin, 0.5mm pitch)" at a different position (https://www.cnx-software.com/2023/12/08/radxa-zero-3w-sbc-rockchip-rk3566-8gb-ram-wifi6-raspberry-pi-zero-2-w-form-factor/ : "some of the connectors are different"). The Pi's 50 cm micro-USB→USB-C data cable to the servo adapter becomes USB-C→USB-C.

### Cable routing through the neck (what the sources say)

The neck is `neck_pitch` (ID 30, in the trunk) and `head_pitch` (ID 31) stacked, enclosed by `neck_left_sheet` / `neck_right_sheet` (30.7 × ~7 × 58 mm plates); then `head_pitch_to_yaw` → `head_yaw` (ID 32) → `head_yaw_to_roll` → `head_roll` (ID 33) in `head_roll_mount` (motor IDs: https://github.com/apirrone/Open_Duck_Mini/blob/v2/docs/configure_motors.md). Per the wiring diagram, five harnesses cross the neck:

1. Servo TTL bus daisy chain (trunk adapter → neck_pitch → head_pitch → head_yaw → head_roll; each servo has two 5264-3P ports).
2. 7.4 V pack pair (pack → UBEC in the head).
3. USB data (Pi micro-USB → adapter USB-C in the trunk; BOM "50cm micro usb to usb c cable").
4. BNO055 I²C (4 wires, trunk → Pi).
5. Foot-switch wires (feet → legs → trunk → Pi GPIO 22/27).

The guide only shows the technique: cables pass between the sheet plates like the shin ("plug the motor cable in the foot's motor, and make it go through the right_sheet", https://github.com/user-attachments/assets/a1432505-6b6c-4765-aea6-0a7a0b8b220b), and the BOM includes a braided "Cable sheath". There is no drawing of a dedicated neck channel; `head_bot_sheet` has a cut-out around the head mechanism through which the bundle enters the head. Treat the exact routing as undocumented (open question below).

Pi Zero header map (guide): eye LEDs GPIO 23/24, projector GPIO 25, antennas PWM GPIO 12/13, foot switches GPIO 22 (left) / 27 (right) with pull-ups, BNO055 on I²C GPIO 2/3, MAX98357A on I²S GPIO 18/19/21. (The feet-wiring photo in the guide says "Right foot gpio 26" but the table and `feet_contacts.py` use 27 — trust 27.)

---

## 2. Battery pack and the 3S question

### Stock parts (BOM)

- Cells: 2 × Molicel INR18650-P30B 3000 mAh / 30 A (https://www.nkon.nl/fr/molicel-inr18650-p30b-3000mah-30a.html); "Get the beefiest 18650 cells you can find".
- Holder: CABLEPELADO flat 2 × 18650 holder, 7.4 V, 200 mm leads, Amazon.fr B08YDTSML8 (https://www.amazon.fr/CABLEPELADO-Support-pour-piles-MR18650/dp/B08YDTSML8). The Amazon page gives no dimensions (page title: "Porte-piles plat | Support de batterie 18650 | Comprend un câble de 200 mm | Tension totale : 7,4 V"). From the CAD pocket it must be ≈40 × 77 × ≤21 mm (two cells side by side).
- 2S BMS (shorturl link in BOM), USB-C charger board (Amazon B0BWTK7SVN), small power switch (B0CH3JCQM5), 2.1 mm barrel jacks ×2, XT30 pair.

### Measured geometry (`body_back.stl`, `battery_pack_lid.stl`)

- `body_back` bbox 40 × 110 × 125 mm (X −135…−95, Y ±55, Z −82…43). The shell is a chevron in plan: deepest at the centre (X = −135 at Y = 0), sloping to X = −95 at Y = ±55.
- Battery pocket: two vertical rails with inner faces **≈40 mm apart** (Y ≈ −21…+20), rail outer faces ≈49 mm apart, rails ≈85 mm tall (Z ≈ −71…+11, clear ≈ 77–80 mm), pocket floor at X ≈ −115 so the pocket is **≈21 mm deep** to the lid plane at X = −95. Cells sit vertical. The Jetson fork's CAD check even found the stock 2-cell pack fouls `battery_pack_lid` by 385 mm³ and `body_back` by 514 mm³ ("PRE-EXISTING in the upstream 2-cell model") — it is a tight fit as shipped (https://github.com/XiaohuiChen-personal/Open_Duck_Mini_Jetson/blob/v2/docs/jetson-mod/battery_bay_before.txt).
- BMS: a narrow vertical slot immediately left of the pocket (Y ≈ −30…−25); USB-C charger: a pocket above the cells near the top edge; a round hole in the left wall (barrel jack) and a slot in the top for the switch (renders of https://github.com/user-attachments/assets/371db809-7cb3-47e1-b277-7fc2bdf21025).
- `battery_pack_lid.stl`: **51.4 × 86.4 × 7.5 mm**, 4 corner holes, notched 4 mm at both ends for the leads, with a raised 25 × 50 mm pad that presses on the cells. It sits at X −102.5…−95, i.e. on the **inner** face of `body_back`: the lid screws to M3 inserts in the rail ends and closes the pocket from the trunk side; you remove `body_back` (screws into inserts in `body_middle_bottom`/`body_middle_top`, guide "Body" section) to get at the cells.
- Clearance behind the rails: at the pocket-floor depth (X = −115) the shell's inner walls are ≈ ±32 mm (≈64 mm clear); at the lid plane the shell is ≈100 mm clear. The region above the pocket (Z +11…+35) holds the charger board.

### Verdict for a 3S pack

- A 3 × 18650 side-by-side holder (~58 × 77 × 21 mm) **does not fit the stock pocket** (40 mm between rails, 51 mm lid). A new lid alone is not enough.
- It **can fit inside the existing `body_back` envelope** if the two rails are moved out to ≈60 mm clear (there is ≈64 mm of shell at the pocket floor and 100 mm at the lid plane) — but the BMS slot on the left must move (e.g. above/below the pack with the charger), and a wider lid (~70 × 86 mm) is needed. That is a moderate `body_back` + `battery_pack_lid` redesign, not a full re-layout. Expect to raise the rails slightly if your holder is >21 mm thick (some 3-cell holders are 22–23 mm).
- Precedent: the Jetson fork fitted **six cells (3S2P) by deepening the rear hump rather than widening it** — a `holder_6cell` tray 62.8 × 42.2 × 22 mm (3 × 2 array, 20.6 mm pitch, Ø18.6 bores) centred at trunk-frame (−156.5, 0, +32.5) mm, with "0.00 mm³ of interference"; they list "battery_pack_lid redesign" as still open (https://github.com/XiaohuiChen-personal/Open_Duck_Mini_Jetson/blob/v2/docs/jetson-mod/component_layout_v2.md).
- Electrical consequences: 2S BMS → 3S BMS (≥15–20 A continuous; 14 servos × 2.7 A locked-rotor = 38 A worst case), 2S USB-C charger → 3S charger, confirm the HENGE UBEC input range covers 12.6 V (its listing says 4A–12A; input range not captured), and note the Waveshare Bus Servo Adapter (A) is specified "9~12.6V voltage input (the input voltage and the servo voltage must be matched)" (https://www.waveshare.com/bus-servo-adapter-a.htm) — a full 3S pack at 12.6 V is exactly at the adapter's and the ST3215's 12.6 V ceiling.

---

## 3. Foot switches

- BOM: "Feet contact switches (SS-10)", AliExpress item 1005006164610609, qty 4 (two per foot). The listing could not be fetched (AliExpress timed out / blocked). Do **not** assume the Omron SS-10: Omron's SS-10 body is 19.8 × 6.4 × 10.2 mm (https://www.tme.eu/html/EN/microswitch-snap-action-ss-omron-electronic-components/ramka_12679_EN_pelny.html) and would not fit the slot below; the CAD model shows a ≈13 × 6 × 6 mm 3-pin snap switch, i.e. the KW10/KW11/"SS-10"-style miniature switch commonly sold under that name.
- Mounting (guide "Assemble the feet": "You can add the foot switches like this too … You press fit them so that the switch is activated when the foot touches the ground", renders https://github.com/user-attachments/assets/71b9ad91-864e-423f-97a3-911d65182ab9 and https://github.com/user-attachments/assets/59e15c7c-3515-4408-bfe9-80e30c4cd007). Measured in `foot_top.stl`: two through-slots in the floor of `foot_top`, each **≈6 mm wide × ≈15–20 mm long × 7.5 mm deep** (assembly X ≈ −35…−29 and +17…+23, Y ≈ 84…99), with small nubs at mid-depth that give the press fit. The switch goes in body-first from inside the foot, solder pins up, plunger down toward the sole. `foot_bottom_pla` (93 × 27.7 × 8 mm) and `foot_bottom_tpu` (101.9 × 40.7 × 8 mm) make up the sole beneath; the two Ø4 holes in `foot_bottom_pla` are the M3 insert positions for the two M3×6 screws joining PLA and TPU, not switch holes.
- Wiring (guide photo https://github.com/user-attachments/assets/d3376494-4690-4484-8352-132e6284731a): per foot the two switches are paralleled, C → GND, NO → GPIO (22 left, 27 right); the runtime reads them with pull-ups (`feet_contacts.py`).
- **KW-12 hinge-lever comparison** (your 12.8 × 5.8 × 6.5 mm body): the body matches the slot (5.8 < 6 mm width, 12.8 mm < slot length), so it press-fits the same way. The hinge lever (≈13–14 mm, hinged at one end) extends beyond the body and sits 2–3 mm proud of the plunger, so it needs either the lever removed/trimmed (use it as a plunger switch) or a lengthened slot plus more sole travel; a lever also lowers actuation force, which is welcome. Confirm with a sample: the stock actuation path (how much the sole moves relative to `foot_top` before the plunger trips) is not documented.

---

## 4. Print set — STL list, quantities, measured bounding boxes

Print guide: "All the parts are printed in standard PLA with 15% infill, except for `foot_bottom_tpu.stl`, which is to be printed in TPU at 40% infill." The guide gives **no** support, orientation or layer-height guidance ("Layer height, wall count, supports, orientation and temperatures are not fully specified" — Tnkr-derived guide at https://microduckrobot.org/diy/open-duck-mini/ says the same). Jaime's mod README is the only orientation note in the repo and it covers his cover parts only (PETG/PLA-CF, 0.2 mm, 15–20 % gyroid, 3 walls, "Supports: Only where unavoidable", https://github.com/apirrone/Open_Duck_Mini/blob/v2/print/mods/v2_Jaimes_Mods/README.md).

All 36 stock STLs are binary. Bounding boxes measured (X × Y × Z, assembly frame, mm; mesh volume in cm³):

| STL | Qty | X | Y | Z | Vol cm³ | Note |
|---|---|---|---|---|---|---|
| foot_top | 2 | 103.5 | 34.9 | 46.0 | 39.7 | |
| foot_side | 2 | 103.5 | 12.0 | 46.0 | 21.4 | |
| foot_bottom_pla | 2 | 93.0 | 27.7 | 8.0 | 15.9 | |
| foot_bottom_tpu | 2 | 101.9 | 40.7 | 8.0 | 23.6 | **TPU, 40 %** |
| knee_to_ankle_left_sheet | 4 | 30.7 | 8.4 | 70.6 | 8.3 | |
| knee_to_ankle_right_sheet | 4 | 30.7 | 7.2 | 70.6 | 6.5 | |
| leg_spacer | 4 | 28.1 | 36.9 | 10.0 | 7.1 | |
| left_roll_to_pitch | 1 | 46.9 | 86.1 | 30.7 | 29.6 | mirrored pair |
| right_roll_to_pitch | 1 | 46.9 | 86.1 | 30.7 | 29.6 | |
| roll_motor_bottom | 2 | 32.0 | 30.7 | 31.4 | 8.5 | |
| roll_motor_top | 2 | 38.0 | 28.7 | 20.0 | 9.2 | |
| trunk_bottom | 1 | 54.4 | 108.0 | 73.7 | 82.6 | bearing seats |
| trunk_top | 1 | 125.5 | 100.7 | 41.0 | 144.7 | servo board tray, IMU block |
| neck_left_sheet | 1 | 30.7 | 7.1 | 58.0 | 8.1 | |
| neck_right_sheet | 1 | 30.7 | 5.8 | 58.0 | 6.2 | |
| head_pitch_to_yaw | 1 | 32.0 | 44.9 | 72.0 | 13.5 | |
| head_yaw_to_roll | 1 | 88.0 | 80.0 | 42.2 | 29.4 | |
| head_roll_mount | 1 | 40.0 | 64.7 | 15.1 | 13.4 | |
| **head** | 1 | **199.8** | **197.3** | 59.4 | 229.4 | **> 180 mm in X and Y** |
| **head_bot_sheet** | 1 | **193.8** | **191.6** | 3.0 | 65.9 | **> 180 mm in X and Y** |
| left_antenna_holder | 1 | 26.9 | 20.0 | 41.7 | 2.9 | |
| right_antenna_holder | 1 | 26.9 | 20.0 | 41.7 | 2.9 | |
| left_cache | 1 | 90.0 | 40.0 | 152.6 | 64.6 | thigh cover |
| right_cache | 1 | 90.0 | 40.0 | 152.6 | 64.6 | |
| body_front | 1 | 10.0 | 110.0 | 143.0 | 142.6 | |
| body_middle_bottom | 1 | 150.0 | 110.0 | 86.2 | 147.5 | |
| body_middle_top | 1 | 150.0 | 110.0 | 56.8 | 76.3 | |
| body_back | 1 | 40.0 | 110.0 | 125.0 | 105.5 | battery hump |
| battery_pack_lid | 1 | 7.5 | 51.4 | 86.4 | 23.6 | |
| bulb | 1 | 2.0 | 35.0 | 35.0 | 1.7 | expression pkg |
| flash_light_module | 1 | 28.0 | 31.5 | 41.0 | 12.5 | expression pkg |
| flash_reflector_interface | 1 | 12.7 | 23.0 | 23.0 | 2.2 | expression pkg |
| left_eye | 1 | 4.3 | 35.0 | 35.0 | 1.4 | expression pkg |
| right_eye | 1 | 8.4 | 40.0 | 40.0 | 4.6 | expression pkg |
| speaker_interface | 1 | 38.6 | 20.8 | 36.9 | 1.8 | expression pkg |
| speaker_stand | 1 | 51.4 | 46.0 | 47.4 | 7.0 | expression pkg |

Totals: 50 PLA prints + 2 TPU prints. Quantities are from the print guide (https://github.com/apirrone/Open_Duck_Mini/blob/v2/docs/print_guide.md).

**Parts over 180 mm:** only `head.stl` (199.8 × 197.3) and `head_bot_sheet.stl` (193.8 × 191.6). Both are near-square, so they cannot be rotated onto a 180 × 180 bed (A1 mini / Ender-3 class need ≥200 × 200 with margins, i.e. 220 × 220 or 256 × 256 beds are comfortable). Workaround already in the repo: Justin's Park Head mod ships an A1-mini cut ("Open_Duck_Mini_ParkHead A1_MINI_VERSION" STEP and `print cut for A1/*.3mf`) — a different (BD-X-style) head, not the stock one (https://github.com/apirrone/Open_Duck_Mini/tree/v2/print/mods/Justins_Park_Head_Mod). Next largest parts: `left/right_cache` 152.6 mm tall, `body_middle_*` 150 mm, `body_front` 143 mm.

**Filament estimate.** Summing mesh volume × quantity gives ≈1.59 L of PLA geometry (≈1,970 g if solid) plus 47 cm³ of TPU. Because most parts are 3 mm shells (2 perimeters + top/bottom are nearly solid, only a thin core is 15 % infill), a realistic print-mass factor is ~0.45–0.6 → **≈0.9–1.2 kg PLA and ≈40–55 g TPU** (plus supports/brims). The BOM's own figure is "Maybe 500g of filament" — treat that as optimistic; budget two 1 kg spools.

---

## 5. Onshape / editable CAD

- Link (README and assembly guide): https://cad.onshape.com/documents/64074dfcfa379b37d8a47762/w/3650ab4221e215a4f65eb7fe/e/0505c262d882183a25049d05
- Anonymous access is **not** possible: the REST call `GET /api/v6/documents/64074dfcfa379b37d8a47762` returns HTTP 403 and the document URL redirects a logged-out headless browser to the Onshape sign-in page. So the document is shared as an Onshape "Public" document that requires any (free) Onshape account to open; public documents can be duplicated ("Make a copy") into your own workspace for edits but not edited in place. I could not confirm the document name or copy permission without logging in — verify after sign-in.
- Alternative editable sources already in the repo: the full-robot STEP inside Jaime's mods (`print/mods/v2_Jaimes_Mods/Mini BDX V2 Jaimes Mods.step`, 64 MB) and Justin's head STEP (`print/mods/Justins_Park_Head_Mod/Open_Duck_Mini_ParkHead.step`, 7 MB). The Tnkr project page (https://tnkr.ai/open-duck-mini/open-duck-mini-v2) offers "Clone Project" and a Files tab (needs a Tnkr account; its documentation tab errored in a headless browser, and it also sells a $600 kit).
- For the lid: the stock lid is a simple 51.4 × 86.4 × 7.5 plate — easy to re-model from scratch to 70 × 86 with the same 4-hole pattern once you decide the new rail spacing. For the face plate, the head front is part of the single `head.stl` shell; editing it needs the Onshape copy or the STEP.

---

## 6. Community forks and builds relevant to 12 V / 3S / other SBCs / cameras

Searched: GitHub forks of both repos (API, sorted by stars; 577 + ~100 forks scanned for post-fork pushes), GitHub repo search, web search, Tnkr mods page, Printables/MakerWorld.

| Project | What it does | Relevance |
|---|---|---|
| **feisuo/Open_Duck_Mini_Runtime_Rockchip** https://github.com/feisuo/Open_Duck_Mini_Runtime_Rockchip | Runtime ported to a Rockchip SBC (Rockchip Debian, user `linaro`): `python-periphery` sysfs GPIO (pins 119/124/125/133/138), PWM chips 2/3 for antennas, BNO055 on I²C bus 3 via `adafruit-extended-bus`, servo bus on hardware UART `/dev/ttyS8` through `rustypot` (no USB adapter), ALSA speaker; 34 commits ahead of upstream; **commit "add 12v model" adds `scripts/ONNX_12V_test.onnx`** (a policy for 12 V servos) and a `9B.onnx`. Board model is not named anywhere (README-RK.md is in Chinese). | Closest precedent for both Radxa (RK3566/RK3588-class) and 12 V servos. |
| **XiaohuiChen-personal/Open_Duck_Mini_Jetson** https://github.com/XiaohuiChen-personal/Open_Duck_Mini_Jetson | Jetson Orin Nano in the trunk, **14 × Feetech STS3250 (12 V) servos, 6 × 18650 3S2P + 3S BMS, IMX219 CSI camera planned**, Isaac Lab policies; body_front/body_back/body_middle_bottom/trunk_bottom modified, battery hump deepened for a 62.8 × 42.2 × 22 mm 6-cell tray; lid redesign open; hardware build "Planned" (not walking yet). Bench finding on their FE-URT-2 adapter: **servo V+ rail is tied to USB VBUS** ("11.1 V will land on USB VBUS → split harness"; https://github.com/XiaohuiChen-personal/Open_Duck_Mini_Jetson/blob/v2/docs/jetson-mod/bench_test_servo.md) — measure your Waveshare adapter before putting 12 V on a bus that shares USB with the Radxa. | Direct 3S + 12 V + camera precedent, with CAD numbers. |
| **venkateswarann/duck-brain** https://github.com/venkateswarann/duck-brain | Pi 4 companion + Pi Zero 2W in the head with a head camera, 2 × GC9A01 eye displays, face tracking; reads battery voltage from the servos. | Camera-in-head precedent (Pi camera). |
| **rimim/Open_Duck_Mini_Runtime** (merged upstream) | Raspberry Pi 5 support (`lgpio` instead of RPi.GPIO) — upstream README now says "In Raspberry Pi 5…". | Shows the runtime's GPIO layer is the thing to port. |
| **maxmakesstuff/Open_Duck_Mini_Runtime** | Pre-built Pi Zero 2W image 0.2.3 (upstream README). | Pi-only. |
| **jmachuca77 (Jaime's mods)** in-repo | BD-X style covers, cable guides, full STEP; warns covers shift CoM. | STEP source. |
| **Codezombie23 (Justin's Park Head)** in-repo | BD-X style head, A1-mini split version, "FacePlateCurve.3mf" vs "FacePlateCurve NoCam.3mf" (a camera-variant face plate). | Camera-ready face plate design exists in this mod. |
| seanmayer/open-duck-mini-build https://github.com/seanmayer/open-duck-mini-build | 2026 build log: "A compact replacement 2S battery holder … fits the reprinted rear panel"; stock 7.4 V. | Confirms people already reprint `body_back` for other holders. |
| ToolKnox/hawkridge-open-duck-mini-v2-bipedal-robot https://github.com/ToolKnox/hawkridge-open-duck-mini-v2-bipedal-robot | Apache-2.0 mirror + condensed guide ("Press-fit two foot switches per foot"). | Guide only. |
| Tnkr mods page https://tnkr.ai/open-duck-mini/open-duck-mini-v2/mods | 12 mods: skins, "Open Duck Mini V2'ye Raspberry Pi" remix, eye mods, Halloween, rocket launcher, etc. | Nothing on 12 V / 3S / Radxa. |
| Printables / MakerWorld | No "Open Duck Mini" listing found via search engines (direct site search is Cloudflare-gated for headless browsers). | — |

No published build using a Radxa, a 3S1P pack, or Waveshare ST3215 12 V in the stock body was found. The Waveshare ST3215 (12 V) and ST3215-7.4V share the body (retailer listings give 45.2 × 24.7 × 35 mm, 55 g for both Feetech variants; https://eckstein-shop.de/Motors?mf=1602), 12 V spec: 6–12.6 V, 30 kg·cm @ 12 V, 2.7 A locked rotor vs 19.5 kg·cm / 2.5 A for the 7.4 V part (https://www.waveshare.com/st3215-servo.htm). The runtime's `check_voltage.py` reads pack voltage from the servos over the bus (https://github.com/apirrone/Open_Duck_Mini_Runtime/blob/v2/scripts/check_voltage.py); `camera.py` uses `picamzero` (Pi-specific) and `example_config.json` has `expression_features.camera` (https://github.com/apirrone/Open_Duck_Mini_Runtime/blob/v2/example_config.json).

---

## 7. Bearings

- BOM: "Bearing", qty 3, Amazon.fr B0CXXSVFTV = "Kozelo 2 Pièces Roulement à Billes **6804Zz [20X32X7mm]**" (https://www.amazon.fr/dp/B0CXXSVFTV) — sold in packs of 2, so buy 2 packs (or 3 loose). Confirmed 6804ZZ, 20 × 32 × 7.
- Where they go:
  1. and 2. **`trunk_bottom`**: guide "Place the bearings in `trunk_bottom` like so" (https://github.com/user-attachments/assets/9ed8591a-7c96-4410-8d7e-9b7d88c6bd1f). Measured: two Ø32 mm seats in the bottom plate at Y = ±37 mm (Z ≈ −89…−82) — these carry the left/right hip-yaw axes (the hip-yaw servo horn drives `roll_motor_top` from above, the bearing supports the yaw pivot below, assembly photos https://github.com/user-attachments/assets/768f1664-030c-4432-9071-c52d79d3ef6b and https://github.com/user-attachments/assets/dba458ae-e9cb-4e16-a82e-cbe74d2350fa).
  3. **Head**: guide "Then insert the bearing, mount the ear motors and the raspberry pi zero 2w"; measured a Ø32 seat in a standing holder at X ≈ −27 (rear-centre of the head floor, ring centre Z ≈ 130) — the rear pivot of the head-roll axis, opposite the `head_roll` servo in `head_roll_mount` at the front. Visible in the real interior photo (white ring holder beside the Pi).

---

## Open questions I could not resolve

1. **Exact neck cable channel** — no drawing; only the "pass it through the sheet" technique and the `head_bot_sheet` cut-out. Needs the Onshape model or a built robot.
2. **Stock foot-switch part** — AliExpress listing 1005006164610609 unreachable; slot size (≈6 × 15–20 × 7.5 mm) measured from CAD says it is a KW10/KW11-class mini switch, not Omron SS-10. Also unclear how much the sole travels before the plunger trips.
3. **CABLEPELADO holder dimensions** — Amazon page has none; inferred ≈40 × 77 × ≤21 mm from the pocket.
4. **UBEC input range** — Alibaba listing (HENGE 4A–12A UBEC) could not be fetched; confirm it accepts 12.6 V.
5. **Onshape copy permission / document name** — login required; 403 anonymously.
6. **Which Rockchip board feisuo used** and what hardware the `ONNX_12V_test.onnx` policy was trained for (servo model, voltage, mass).
7. **Waveshare Bus Servo Adapter (A) servo-V+ ↔ USB VBUS coupling** — only measured by the Jetson fork on a Feetech FE-URT-2; check the Waveshare board with a meter before running 12 V with the Radxa on the same USB.
8. **Print orientation/supports** — not specified anywhere official; Tnkr documentation tab would not load.
9. **Radxa Zero 3W GPIO/PWM/I²S availability** for the antennas (PWM), MAX98357A (I²S) and LEDs was not checked here (see `radxa-zero-3w.md` in this folder).
