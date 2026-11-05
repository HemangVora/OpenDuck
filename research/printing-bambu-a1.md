# Printing the Open Duck Mini v2 on a Bambu Lab A1 (Vadodara edition)

Research notes, 28 Oct 2026. Scope: Open Duck Mini v2 (`apirrone/Open_Duck_Mini`, branch `v2`, STLs in `print/`), printed on a Bambu Lab A1 (256 × 256 × 256 mm, 0.4 mm stainless nozzle, direct drive, no AMS), in Vadodara, Gujarat (hot, dry summer; humid monsoon).

Everything below is from primary sources (Bambu wiki, Bambu Studio's bundled profiles, the Open Duck repo, the STL geometry itself) unless marked "community". Where I ran Bambu Studio myself, the method is described so you can repeat it.

---

## 0. What the project itself specifies

Source: [docs/print_guide.md (v2)](https://github.com/apirrone/Open_Duck_Mini/blob/v2/docs/print_guide.md)

- "All the parts are printed in standard PLA with 15% infill, except for `foot_bottom_tpu.stl`, which is to be printed in TPU at 40% infill."
- 36 STL files, 54 printed pieces (quantities below). Open issue [#26](https://github.com/apirrone/Open_Duck_Mini/issues/26) says `bulb.stl` should be **x2**, not x1 (the print guide is wrong) -- I count it as 2 below, making 55 pieces.
- The BOM is a Google Sheet linked from the README; heat-set inserts are listed as "M3 inserts" from amazon.fr `B09ZPF48VK` (FENGYING, 50 pcs, brass, M3). Bearings and Feetech STS3215 servos mount into printed pockets.
- Assembly guide ([docs/assembly_guide.md](https://github.com/apirrone/Open_Duck_Mini/blob/v2/docs/assembly_guide.md)) tells you where inserts go: `trunk_bottom` (bearing seats + 4 inserts on the bottom for body parts), `foot_bottom_pla` (sandwiches the TPU sole), `foot_top`, `leg_spacer` (4 inserts total across both sides), `head` (all holes), `body_middle_bottom` / `body_middle_top` (battery pack and `body_front` mounts).

Part list with quantities (print guide + issue #26):

| PLA parts | qty | | qty |
|---|---|---|---|
| foot_top | 2 | head_pitch_to_yaw | 1 |
| foot_side | 2 | head_yaw_to_roll | 1 |
| foot_bottom_pla | 2 | head_roll_mount | 1 |
| knee_to_ankle_left_sheet | 4 | head | 1 |
| knee_to_ankle_right_sheet | 4 | head_bot_sheet | 1 |
| leg_spacer | 4 | left/right_antenna_holder | 1 + 1 |
| left/right_roll_to_pitch | 1 + 1 | left/right_cache | 1 + 1 |
| roll_motor_bottom | 2 | body_front / body_back | 1 + 1 |
| roll_motor_top | 2 | body_middle_bottom / _top | 1 + 1 |
| trunk_bottom / trunk_top | 1 + 1 | battery_pack_lid | 1 |
| neck_left/right_sheet | 1 + 1 | bulb | 2 (issue #26) |
| flash_light_module | 1 | flash_reflector_interface | 1 |
| left_eye / right_eye | 1 + 1 | speaker_interface / speaker_stand | 1 + 1 |
| **TPU** foot_bottom_tpu | 2 | | |

---

## 1. Heat-set inserts

### 1.1 The BOM insert and what the parts are designed for

- amazon.fr `B09ZPF48VK` resolves to "FENGYING 50 Pièces M3 insert fileté ... Écrous Moletés en Laiton" (brass, M3, 50 pcs). Amazon's page did not expose the dimensions to a non-browser fetch, so I could not confirm length/OD from the listing itself ([amazon.fr/dp/B09ZPF48VK](https://www.amazon.fr/dp/B09ZPF48VK)).
- The de-facto standard "3D-printing" M3 insert is the ruthex RX-M3x5.7 type: **M3 thread, 5.7 mm long, 4.6 mm knurl OD (D1), 3.9 mm lead-in (D2), 4.0 mm nominal hole (D3), 1.6 mm minimum wall** -- per the spec table on [3DJake's ruthex M3x5.7 page](https://www.3djake.com/ruthex/threaded-insert-m3-100-pieces) and [Grobotronics](https://grobotronics.com/ruthex-threaded-insert-m3-pack-of-70.html?sl=en) (OD 4.6, L 5.7). Accu's generic chart agrees: M3 heat-set, non-flanged, max OD 4.4-4.5 mm, **pilot hole 4.0 mm (-0/+0.1)**, ~4.8 mm deep for the short version ([Accu hole-size chart](https://accu-components.com/us/p/488-threaded-insert-hole-size-charts-for-3d-printing-pla-petg-resin)). RS Pro's equivalent: 4.6 mm OD, 5.7 mm long, 4 mm fixing hole ([RS 2040616](https://int.rsdelivers.com/product/rs-pro/rs-pro-brass-threaded-insert-46-mm-diameter-4-mm/2040616)).
- **I measured the STLs directly** (plane-sliced every part with a small numpy script, fitted circles to closed loops). The blind insert holes in `trunk_bottom`, `trunk_top`, `head`, `head_yaw_to_roll` and `foot_bottom_pla` are modelled at **Ø 4.0 mm**; M3 clearance through-holes are **Ø 3.2 mm**; screw-head counterbores are **Ø 6.5 mm**. (Measurement log: `scratchpad/agents/print/stl_measurements.txt`; holes on horizontal axes, e.g. in `leg_spacer`, are not captured by a Z-slice and were not measured.) So the parts are designed for the 4.0 mm-hole class of insert, which is exactly the ruthex/"3D printing" M3 x 5.7 x 4.6 OD type. Do not buy the 5.0-5.5 mm OD "M3 x 5 x 4" Voron-style or flanged inserts without widening holes.
- Printed holes come out slightly undersize on FDM (a 4.0 mm model hole often prints 3.8-3.9 mm). That is actually fine for heat-set inserts, which want 0.1-0.3 mm interference. If an insert will not start by hand it is correct; if it drops in cold, the hole is too big.

### 1.2 Installing them in PLA

- Temperature: [CNC Kitchen](https://cnckitchen.com/blog/tips-and-tricks-for-heat-set-inserts) recommends **~225 °C for PLA, i.e. 10-20 °C above the filament's print temperature**; ruthex's product pages say "10-15 °C above the hotend temperature of the filament" ([ruthex](https://www.ruthex.de/en/products/ruthex-m2-m3-m4-m5-gewindeeinsatze-sortimentskasten-lotspitzen-set-70-100-50-50-stuck-gewindebuchsen-aus-messing)). Other guides quote 200 °C ([PrintPal](https://printpal.io/resources/how-to-make-premium-3d-prints-with-heat-set-inserts)) up to 240-260 °C ([UW MEDesign lab](https://medesignlab.me.wisc.edu/?p=162)). Start at **220-230 °C** with a temperature-controlled iron (a TS101 / Pinecil / Hakko FX-888D class iron; a non-adjustable 40 W iron runs 350-400 °C and will overheat the PLA).
- Tip: a dedicated **heat-set tip** with a centering pin that fits the M3 bore (ruthex "Lötspitzen-Set", or any generic M3 insert tip, or a conical tip that enters the bore ~2 mm). It keeps the insert square. Do not use a chisel tip on the top face only.
- Technique (CNC Kitchen): push the insert ~90 % of the way with the iron, then press the last bit flush with a flat object (screwdriver shaft, steel ruler) and hold 3-5 s while it solidifies -- inserts creep back out otherwise. Go slowly; if it sinks instantly the iron is too hot. Test on a scrap print with a 4.0 mm hole first (Accu's advice; also print a 4.0/4.1/4.2/4.3/4.4 mm hole test coupon per CNC Kitchen if your first insert feels wrong).
- Keep the insert's knurl fully below the surface so the mating part sits flat (the duck has many face-to-face joints).
- Count: the assembly guide mentions inserts in at least 9 part types; the exact total is listed as "TODO" in the BOM. My STL survey found Ø4.0 mm blind holes: `trunk_top` 16, `head` 12, `trunk_bottom` 4-6, `head_yaw_to_roll` 4, `foot_bottom_pla` 2 x 2, plus unmeasured side-axis holes in `leg_spacer` (4), `foot_top`, `body_middle_*`. Budget **80-100 inserts**; a 50-pack is one bag short.

---

## 2. Bambu A1 PLA settings for strong functional robot parts

Primary source: the profiles bundled with Bambu Studio 02.07.01.62 (`/Applications/BambuStudio.app/Contents/Resources/profiles/BBL/`), which I resolved through their inheritance chain. These are what the slicer actually uses.

**"0.20mm Standard @BBL A1"** (A1 default): 0.20 mm layers, **2 walls**, **15 % grid**, 5 top / 3 bottom shells, outer wall 200 mm/s, inner wall 300, sparse infill 270, first layer 50, travel 700, accel 6000, seam aligned, classic wall generator, supports OFF (tree-auto when enabled, 30° threshold), brim auto/5 mm, elephant-foot comp 0.075, XY hole compensation 0.

**"0.20mm Strength @BBL A1"**: same but **6 walls, 25 % infill, outer wall 60 mm/s**. This is Bambu's own "strong parts" preset.

**Bambu PLA Basic @BBL A1** filament: 220 °C nozzle (190-240 allowed), **65 °C textured PEI plate**, 35 °C cool plate, max volumetric speed 21 mm³/s, fan 60-80 % (100 % on overhangs), slow-down when a layer is under 6 s (min 20 mm/s), density 1.26 g/cm³, Tg ~45 °C.

What the community actually prints the duck with:

- MakerWorld profile "Open Duck Mini V2 - Bipedal Robot" ([makerworld.com/en/models/2755651](https://www.makerworld.com/en/models/2755651)): **0.2 mm layer, 2 walls, 25 % infill, 6 plates, 52.8 h total** (search snippet; page is behind a bot wall so I could not read per-plate data or comments).
- Jaime Machuca's merged mod set in the repo ([print/mods/v2_Jaimes_Mods](https://github.com/apirrone/Open_Duck_Mini/tree/v2/print/mods/v2_Jaimes_Mods), [PR #25](https://github.com/apirrone/Open_Duck_Mini/pull/25)) ships `Bambu_X1C_Project_File.3mf`. I opened it: **0.16 mm layers, 4 walls, 15 % gyroid, 5/5 shells, tree(auto) supports ON, auto brim, PLA Basic / PLA Tough / PLA-CF**; its README recommends "3 perimeters for strength on structural covers, 15-20 % gyroid or cubic, supports only where unavoidable, skirt or minimal brim for tall narrow pieces". It also includes a `Print Orientation Reference.png` for its own parts.
- The original author's choice of 15 % infill is about mass (the robot carries its own weight on 9 g and STS3215 servos; the RL policy was trained with those inertias).

**Recommendation for the A1** (reasoned from the above):

| Setting | Value | Why |
|---|---|---|
| Process | start from **0.20mm Standard @BBL A1** | fastest profile that still gives good dimensional accuracy for servo pockets; 0.16 mm only buys nicer surfaces |
| Walls | **3** (4 on `left/right_roll_to_pitch`, `roll_motor_*`, `trunk_bottom`, `foot_top`) | walls, not infill, carry servo-bracket loads; 3 walls = 1.26 mm; Jaime used 4 |
| Infill | **15 % gyroid** (guide says 15 %; swap grid to gyroid) | gyroid is isotropic and does not cross itself, so it does not rattle the nozzle; grid is weak in one axis |
| Top/bottom | 5 / 4 | |
| Supports | tree(auto), 30°, ON only for parts with real overhangs: `head`, `foot_top`, `roll_to_pitch`, `trunk_top`, `head_yaw_to_roll` | tree supports leave servo pockets cleaner than normal supports |
| Brim | none for flat parts; **5 mm outer brim on tall thin pieces** (`left/right_cache` 153 mm tall, `body_front` 143 mm) | A1 bed is 65 °C textured PEI, PLA does not need brim otherwise |
| Speed | leave profile speeds; optionally cap outer wall to 120 mm/s on small brackets | the Standard profile already slows outer walls on overhangs; A1 vibration compensation handles 200 mm/s |
| Seam | aligned, "back" or painted away from bearing seats | |
| XY hole compensation | 0 (do not touch until you have measured) | parts are designed at 4.0 mm; the A1 is accurate enough; a 0.1 mm hole comp would loosen inserts |

**Small servo brackets / cooling.** Parts like `roll_motor_bottom` (32 × 31 × 31 mm) and `leg_spacer` have short layers; the Standard profile's "slow down for layer cooling" (min 6 s/layer, floor 20 mm/s) plus 60-80 % fan is enough for PLA. Printing two or more small parts on one plate is the easiest cooling fix (each layer takes longer). Avoid "by object" sequencing for PLA; "by layer" gives better cooling.

**What Bambu Studio estimates.** After slicing, the right-hand panel and the Preview show per-plate **estimated time, filament length (m), weight (g) and cost** (cost only if you enter a price/kg in the filament preset), plus a per-feature breakdown (walls, infill, support, travel). Bambu's own forum confirms cost is derived from weight × your price ([forum: Slicer shows cost](https://forum.bambulab.com/t/slicer-shows-cost/3375)). The same numbers are written into the gcode header (`; model printing time`, `; total estimated time`, `; total filament weight [g]`), which is how I pulled them in bulk below. Expect the real A1 to be within ~5 % of the estimate; the estimate excludes bed heat-up and the pre-print calibration (~3-6 min per plate).

---

## 3. TPU on the A1 (the two foot soles)

Primary sources: [Bambu wiki -- TPU Printing Guide](https://wiki.bambulab.com/en/knowledge-sharing/tpu-printing-guide) (edited 17 Sep 2026), [TPU 90A printing guide for A1 series](https://wiki.bambulab.com/en/filament-acc/filament/tpu-85a-90a-printing-guide-for-a-series), [Filament Drying Recommendations](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament), and the bundled Bambu Studio TPU profiles.

**Compatibility (official table).** A1 series: TPU 85A -- incompatible; **TPU 90A, TPU 95A HF, "TPU for AMS" -- compatible**. 0.4 mm nozzle is fine for all three; 0.2 mm is not. Bambu says printers "do not currently support TPU below 85A". The A1 has no AMS in your case, which is the right setup: the wiki states AMS / AMS lite / AMS 2 Pro are not compatible with TPU (only AMS HT, as a sealed box with a bypass outlet). "TPU for AMS" is a stiffer, 1.26 g/cm³ formulation (Bambu profile type `TPU-AMS`, 18 mm³/s) made so it can be pushed through an AMS; with an external spool on the A1 you do not need it, and regular TPU 95A HF gives you a softer sole. The author's design intent is a soft sole, so **use TPU 95A (HF if you buy Bambu; any 95A otherwise).**

**Profile values as shipped (Bambu Studio 2.07, A1 0.4):**

| | Bambu TPU 95A HF @BBL A1 | Generic TPU @BBL A1 | TPU for AMS @BBL A1 |
|---|---|---|---|
| Nozzle | 230 °C (200-250) | 240 °C | 230 °C |
| Textured PEI bed | **45 °C** | 45 °C | (base 35 °C) |
| Max volumetric speed | 12 mm³/s (≈ 150 mm/s at 0.2 × 0.42) | **3.2 mm³/s** (≈ 38 mm/s) | 18 mm³/s |
| Retraction | **0.8 mm** (A1 override; base 2 mm @ 10 mm/s) | 0.4 mm | 0.4 mm |
| Fan | 100 % | 100 % | 20-40 % |
| Slow-down layer time | 8 s, min 10 mm/s | 8 s | 10 s |
| Density | 1.22 | 1.24 | 1.26 |
| Flow dynamics cali | **turn OFF** (wiki) | OFF | OFF |

For a no-name 95A spool bought in India, start from **Generic TPU @BBL A1** (3.2 mm³/s is slow but almost never fails), or copy TPU 95A HF and cut max volumetric speed to 5-6 mm³/s.

**Procedure the wiki gives for the A1 (TPU 90A page, applies to 95A):**
1. Dry first (see §4): TPU 95A HF **70 °C / 8 h forced-air oven**, or 80-90 °C / 12 h on an enclosed printer's bed. The wiki explicitly says "P1P / A1 / A2L / A1 mini, as open-frame printers, cannot be used to dry filament."
2. Store at **< 20 % RH** with silica gel; print straight from a sealed dry box with a low-friction spool holder, box side-port open, **box raised so the filament exits above the extruder inlet** (they publish a spool-rack model). Spool width can grow from ~65.4 to ~69.4 mm after drying, so the 4 L Bambu box binds; use the 5.8 L one or any roomy box.
3. New or cold-pulled nozzle (TPU picks up residue). Flush with PLA at 250 °C 3-5 times if the nozzle has seen PLA-CF or glitter PLA.
4. Build plate: **textured PEI, no glue** (the wiki warns the textured plate gets *too* sticky with glue). Cool Plate SuperTack is not allowed. If you only have the smooth plate, glue is mandatory.
5. Load: remove one PTFE tube from the toolhead, feed straight from the box into the extruder inlet, preheat 250 °C, push by hand, use the screen's "down arrow" in short presses until it extrudes. Unload is manual on the A1 (heat to 250 °C, reverse the gear while pulling; the cutter is not used for TPU).
6. Disable flow-dynamics calibration for the print. Keep the default max volumetric speed; "avoid increasing the print speed". Do not print tall thin TPU objects (not an issue for an 8 mm sole).

**Common failures and the wiki's fixes.** Stringing/oozing -> print "by object" if several parts share a plate (the sole pair can be printed by object), drop nozzle temp 5 °C and max flow by 0.4 mm³/s, add 0.2 mm retraction, dry longer. Under-extrusion -> slower, check spool drag, check moisture, cold-pull. Extruder clog from filament buckling -> disassemble the extruder and clear it; keep the feed path short and straight. Stuck part -> isopropyl alcohol into a lifted edge, peel slowly. Forum A1 owners add: use a bearing spool holder; the printer may still "think" PLA is loaded on the external spool, so set the filament type on the screen; calibrate flow per roll (one user: flow 1.04, PA 0.45 at 240 °C) ([forum thread](https://forum.bambulab.com/t/bambu-95a-hf-tpu-on-the-a1/103100?page=2), [TPU 95A HF settings thread](https://forum.bambulab.com/t/recommended-tpu-95a-hf-print-settings/36470), [A1 TPU failed print](https://forum.bambulab.com/t/a1-tpu-failed-print-help/188347)).

**Will a 40 % infill sole print reliably?** Yes. `foot_bottom_tpu.stl` is a flat 101.9 × 40.7 × **8 mm** slab with two Ø3.4 mm through-holes and Ø6.5 mm counterbores -- the easiest TPU geometry there is (no overhangs, no tall sections, big flat base on a 45 °C textured plate). I sliced it with the TPU 95A HF A1 profile, 3 walls, 40 % gyroid, 0.20 mm: **41 min and 17.0 g per sole** (82 min / 34 g for the pair, printed one at a time). Use gyroid (bouncy, no crossings) rather than grid; 40 % gyroid at 8 mm thickness gives a firm but compliant sole. Print the two soles **by object** to avoid stringing across the gap, or on two separate 41-minute plates. The only realistic failure mode is wet filament (bubbles, holes, weak layers) or a spool that drags.

---

## 4. Filament in a humid climate (Vadodara)

Climate: IMD data via Wikipedia gives Vadodara afternoon RH of ~23 % (Apr), 32 % (May), 51 % (Jun), **74-75 % (Jul-Aug)**, annual mean 45 % ([weather-and-climate.com](https://weather-and-climate.com/average-monthly-Humidity-perc,vadodara-gujarat-in,India)). Morning RH in the monsoon is higher still. So: summer is harmless for PLA; June-September is the problem, especially for TPU, which is strongly hygroscopic.

**Official Bambu drying table** ([Filament Drying Recommendations](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament), edited 31 Jul 2026):

| Filament | Forced-air oven / filament dryer | Enclosed printer heatbed (X1/P1S/H2/P2S) | AMS 2 Pro / AMS HT |
|---|---|---|---|
| PLA Basic / Matte | **50 °C, 8 h** | 60-70 °C, 12 h, flip every 6 h, under a cover | 45 °C, 12 h |
| PLA Silk / CF | 55 °C, 8 h | 65-75 °C, 12 h | 45 °C, 12 h |
| TPU 95A HF, TPU for AMS | **70 °C, 8 h** | 80-90 °C, 12 h | AMS HT 75 °C 18 h (AMS 2 Pro "may not fully dry TPU") |
| TPU 85A / 90A | 70 °C, 8 h | 90 °C, 16 h | 75 °C, 18 h |

Notes from the same page: drying is "recommended" for PLA and **"required" for TPU**; static (non-rotating) drying is unsuitable for PLA and TPU because they soften and the layers stick together; keep a desiccant in the storage box; store TPU below 20 % RH; use spools that survive the temperature (some third-party spools deform).

**Can the A1's heated bed dry filament?** Bambu says **no**: "P1P / A1 / A2L / A1 mini, as open-frame printers, cannot be used to dry filament" (dry-filament page), repeated on the A-series TPU page ("Due to the A1/A1 mini being an open printer, it is not possible to dry the filament on a heatbed"). The reason is that without an enclosure the air over the bed never gets warm enough, and the bed tops out at 100 °C. People do it anyway with a cardboard box over the spool on the bed, but it is uncontrolled and the fan ducts/screen are not rated for it. For Vadodara buy a **real filament dryer** (Sunlu S2/S4, Eibos, Creality Space Pi, Polymaker PolyDryer, or Bambu's own if sold locally) that reaches 70 °C for TPU; the cheap 50-55 °C dryers are fine for PLA only. A kitchen oven at 50 °C is unreliable (thermostats swing ±15 °C); if you use one, put a thermometer inside ([forum report](https://forum.bambulab.com/t/tpu-95a-with-lots-of-strings/192105)).

**Storage practice for the monsoon**
- Keep spools in sealed boxes (any 5-6 L clip-lid food box or vacuum bag) with **100-200 g of silica gel per box** and a cheap hygrometer; target < 20 % RH for TPU, < 40 % for PLA. Recharge silica gel in the dryer or oven (Bambu's page has a section on this).
- Print TPU **from inside the dry box** (feed through a hole with a PTFE tube) -- the wiki's recommended setup for A-series TPU.
- PLA that has sat open for a week in July will string and have dull, weak layers; one 8 h dry at 50 °C fixes it. Wet PLA also absorbs enough water to cause popping and poor layer adhesion in the thin `*_sheet` parts.
- Ambient room temperature above ~35 °C is not a print problem for PLA on an open printer (Tg 45-60 °C), but keep the A1 out of direct sun and away from a wall AC blast (draughts cause layer lines on tall parts).

---

## 5. Open Duck Mini v2 community print resources

What exists (and what does not):

- **MakerWorld** "Open Duck Mini V2 - Bipedal Robot" ([makerworld.com/en/models/2755651](https://www.makerworld.com/en/models/2755651)): the one pre-arranged profile. Search metadata: **6 plates, 52.8 h, 0.2 mm, 2 walls, 25 % infill**, all parts in correct quantities, BOM reproduced, 1 rating (5.0), ~200 boosts. The page is Cloudflare-gated so I could not read comments, per-plate times or orientations -- open it in a browser and download the 3MF; it is the fastest way to get sane orientations. Which printer it was arranged for is not stated in the snippet; if it is an X1C/P1S plate set (256 mm bed) it fits the A1 unchanged.
- **GitHub `print/mods/`** ([v2 branch](https://github.com/apirrone/Open_Duck_Mini/tree/v2/print/mods)): `v2_Jaimes_Mods` (BD-X style covers, cable guides, trunk splits, RPi mount, an X1C 3MF with orientations and supports -- see §2) and `Justins_Park_Head_Mod` ([PR #23](https://github.com/apirrone/Open_Duck_Mini/pull/23), Park-style head, STEP + print files). [PR #15](https://github.com/apirrone/Open_Duck_Mini/pull/15) (an X1C 3MF of the stock parts) was *not* merged. [PR #44](https://github.com/apirrone/Open_Duck_Mini/pull/44) adds a display stand.
- **Tnkr guide** ([tnkr.ai/explore/docs/open-duck-mini/open-duck-mini-v2](https://tnkr.ai/explore/docs/open-duck-mini/open-duck-mini-v2)): 118 stars, 8 builds logged, 12 mods (companion remix, RPi mount remix, Halloween skins, eye mod, "grid holes" redesign, etc.). The site is JS-rendered; the mods page lists titles only. Tnkr also sells a kit.
- **Printables / Thingiverse**: nothing for the v2 stock parts (searched; only unrelated ducks).
- **Issues that are really print/fit issues:**
  - [#7](https://github.com/apirrone/Open_Duck_Mini/issues/7) (Mar 2025): the two holes on `left/right_roll_to_pitch` were **1.18 mm off-centre** from the servo holes; fixed in CAD and the STLs were regenerated the same week. If you have old STLs, re-download.
  - [#17](https://github.com/apirrone/Open_Duck_Mini/issues/17) (Apr 2025): a servo mounting screw head on `roll_motor_bottom` protrudes and rubs the `roll_to_pitch` part, blocking hip roll; the author's own duck "dug its own slot". Fix: a clearance slot (not confirmed in the STL) -- or use a low-profile M2.5/M3 screw there, or file a notch after printing.
  - [#26](https://github.com/apirrone/Open_Duck_Mini/issues/26): print **two** bulbs.
  - [#22](https://github.com/apirrone/Open_Duck_Mini/issues/22): STLs were once missing from the repo (now fixed).
- **Build logs**: "The Open Duck Mini Droid: 4 Days of Soldering, Assembling, and Electrical Exorcisms" ([YouTube tt-g_fi-eGU](https://www.youtube.com/watch?v=tt-g_fi-eGU)) -- a first-time builder; a commenter notes the leg "sheet" parts are much stronger printed flat than standing (layer lines across the thin section). Japanese build ([-DNNGdwmtdY](https://www.youtube.com/watch?v=-DNNGdwmtdY), ~80 000 JPY total with own printer), Apérobot talk ([uZwMqvsVOQE](https://www.youtube.com/watch?v=uZwMqvsVOQE)), Hackaday coverage ([hackaday.com, Apr 2025](https://hackaday.com/2025/04/05/disneys-bipedal-bdx-series-droid-gets-the-diy-treatment/)), Hackster "HRI with the Open Duck Mini" ([hackster.io](https://www.hackster.io/PaulTR/hri-with-the-open-duck-mini-caa398)). None of these publish print hours or failure lists; the only quantitative community number is MakerWorld's 52.8 h / 6 plates. Reddit is not reachable from this tool; the project's Discord (linked in the README) is where fit questions get answered.

**Orientation and support guidance (derived from geometry + Jaime's project + the YouTube comment):**
- All `*_sheet` parts (knee_to_ankle, neck, head_bot_sheet): **flat**, the 7-8 mm dimension vertical. No supports.
- `head.stl` (200 × 197 × 59 mm as exported): print **on its flat underside** (the way it is exported), 59 mm tall. It has a Ø4.0 insert ring and bearing/servo pockets on the underside; tree supports for the eye sockets / beak overhangs. This is the one part that uses most of the bed; place it alone or with a few small parts.
- `trunk_top` (125 × 101 × 41) and `trunk_bottom` (54 × 108 × 74): as exported (open side up), tree supports on.
- `left/right_roll_to_pitch` (47 × 86 × 31): as exported, flat; supports for the servo pocket roof.
- `foot_top` / `foot_side` (104 × 35 × 46 and 104 × 12 × 46): foot_top on its 104 × 35 face, supports under the toe; foot_side flat on its 104 × 46 face (12 mm tall), no supports.
- `left/right_cache` (90 × 40 × 153) and `body_front` (10 × 110 × 143): tall shells -- stand them as designed only if the open side faces up; otherwise lay `body_front` flat (10 mm thick plate). Use a brim.
- `foot_bottom_pla` (93 × 28 × 8) and the TPU sole: flat.

---

## 6. First-week A1 setup

Official pages: [Unboxing Guide for A1 Combo](https://wiki.bambulab.com/en/a1/manual/unboxing-a1-combo) (the solo A1 follows the same 18 steps minus the AMS lite), [A1 First Print with an External Spool](https://wiki.bambulab.com/en/a1/manual/first-print-with-external-spool), [How to enable LAN Mode](https://wiki.bambulab.com/en/knowledge-sharing/enable-lan-mode), [A1 Maintenance index](https://wiki.bambulab.com/en/a1/maintenance), [Hotend Replacement for A1 Series](https://wiki.bambulab.com/en/a1/maintenance/replace-hotend).

**Unboxing (18 steps, ~40 min).** Lift the frame by the Z brackets, not the X-axis; lift the base by the plastic housing, not the bed. Cut the zip tie under the bed; pass the base through the frame at 45°; remove toolhead zip ties/foam and any Z-axis stoppers (H2.0 key); slide the Y-rail cover off, fit **12 × ST3-23 screws** into the base, cover back on; tip the printer onto its back, clip the cable box in, plug the three colour-coded harnesses and the yellow-tag cable; stand it up, fit the plate, fold out the screen, fit the **purge wiper (1 × M3-12)**; fit the external spool holder on the cross-beam with the short PTFE tube into any toolhead inlet; put a box under the purge wiper (left side). Power on and follow the on-screen **initialization + calibration** (bed level, vibration compensation, motor noise cancellation -- takes ~10 min; you can skip Wi-Fi/Handy binding and do it later). Before the first print, slide the bed by hand through its full travel once (the wiki notes stiction after shipping can scar the plate). Accessory box contents: textured PEI plate, sample filament, unclogging pin, H2/H1.5 keys, cable organizer, scraper, **spare filament cutter**, grease + oil, 32 GB microSD (installed).

**Firmware.** Update from the screen (Settings -> Firmware) or Bambu Studio on day one; LAN-only "developer mode" for third-party tools arrived in A1 firmware 01.05.00.00. Re-run calibration after any firmware update that asks for it.

**Bambu Studio vs Bambu Handy.** Studio (desktop) is the slicer and the only way to arrange plates, paint supports/seams, and send multi-plate jobs; Handy (phone) is monitoring, camera, MakerWorld one-click prints and remote start via cloud. For the duck you live in Studio. Studio also runs the "Device" tab camera/controls on LAN.

**LAN-only mode.** On an A-series: Settings -> page 3 -> **LAN Only Mode** -> on (green); note the access code. In Studio: Device -> printer list -> the printer shows a lock icon -> enter the access code (or Device -> "No Printer" -> Bind with Access Code using IP + code if you are on a different subnet; IP must be re-entered each launch). Trade-offs stated by Bambu: no Handy app, no remote start from outside the LAN, no cloud print history. Everything needed for this build works in LAN mode.

**Nozzle / plate.**
- The A1 ships a 0.4 mm stainless hotend; the whole hotend is quick-swap (clip, no tools). After swapping to a different size/material you must set it under Settings -> Maintenance -> Nozzle. Keep **one spare 0.4 mm stainless hotend** (~₹1,000-1,500 class; clogs and blobs are easier to fix by swapping than by cleaning at 1 am) and consider a **0.6 mm** for faster TPU/structural prints later (wiki: 0.6/0.8 are "recommended" for TPU 90A; 0.4 is fine for 95A HF).
- **Textured PEI plate** (included) is the right plate for **both** PLA (65 °C) and TPU (45 °C, *no* glue). Bambu's guidance is to let the plate cool below ~35 °C before removing parts; the duck's large flat parts (`head_bot_sheet`, `head`) will pop off on their own as it cools. A second textured plate lets you queue the next plate while the first cools. Glue stick is only needed on the smooth/Cool plate or for PETG; a cheap PVP glue stick still earns its place for occasional release help on big TPU footprints and as a release layer for the first-layer-fused cases.
- Other spares worth having in India where shipping takes a week: a pack of PTFE tube + collets, 1-2 spare hotends, a second filament cutter (one is in the box), 1 kg of extra white PLA (the duck uses ~1 kg; see §7), silica gel, a hygrometer, a 0.4 mm nozzle needle (included), isopropyl alcohol for plate cleaning, and the cheap A1 "poop chute"/purge bucket model from MakerWorld.
- Maintenance pages exist for hotend cleaning, blob removal, Y-rail lubrication (the included oil), belt tension and extruder cleaning -- do the extruder clean before any TPU run.

---

## 7. Plate plan for the A1 with hours per plate

### 7.1 Method

I could not read MakerWorld's per-plate times, so I generated the estimate myself with the real slicer: Bambu Studio 02.07.01.62 CLI (`BambuStudio --load-settings machine;process --load-filaments fil --arrange 1 --allow-rotations --orient 1 --slice 0 ...`) with the bundled **Bambu Lab A1 0.4 nozzle** machine profile, **Bambu PLA Basic @BBL A1** and **Bambu TPU 95A HF @BBL A1** filaments, and two process variants:

- **A = official print guide**: 0.20mm Standard @BBL A1, 2 walls, 15 % grid, no supports.
- **B = recommended**: same, 3 walls, 15 % gyroid, tree(auto) supports.
- **TPU sole**: 3 walls, 40 % gyroid, no supports, TPU 95A HF profile (12 mm³/s cap).

Caveats: the CLI's auto-orient chose standing orientations for a few parts (e.g. it stood `head` on its side, 200 mm tall), so some per-part times are a few % off what a human-oriented plate gives; supports in B add material; estimates exclude ~4 min/plate of bed heating and calibration. Treat totals as ±10 %. Scripts and raw gcode headers: `scratchpad/agents/print/tools/batch_slice.py`, `out/parts_summary.csv`, `out/groups_summary.csv`.

### 7.2 Per-part estimates (one piece, variant A / variant B)

| Part | qty | time A | time B | g each (B) |
|---|---|---|---|---|
| head | 1 | 5 h 26 m | 5 h 26 m | 172 |
| left_cache / right_cache | 1+1 | 1 h 56 m | 1 h 55 m | 52 |
| trunk_top | 1 | 1 h 36 m | 1 h 55 m | 59 |
| head_bot_sheet | 1 | 1 h 21 m | 1 h 26 m | 54 |
| trunk_bottom | 1 | 1 h 06 m | 1 h 14 m | 33 |
| left/right_roll_to_pitch | 1+1 | 1 h 06 m | 1 h 07 m | 21 |
| foot_top | 2 | 1 h 01 m | 1 h 03 m | 24 |
| head_yaw_to_roll | 1 | 43 m | 45 m | 17 |
| foot_side | 2 | 39 m | 40 m | 14 |
| head_pitch_to_yaw | 1 | 32 m | 32 m | 11 |
| leg_spacer | 4 | 23 m | 23 m | 5 |
| head_roll_mount | 1 | 23 m | 23 m | 11 |
| roll_motor_top | 2 | 21 m | 21 m | 6 |
| roll_motor_bottom | 2 | 20 m | 20 m | 6 |
| foot_bottom_pla | 2 | 16 m | 18 m | 9 |
| left/right_antenna_holder | 1+1 | 15 m | 15 m | 4 |
| knee_to_ankle_left_sheet | 4 | 14 m | 15 m | 6 |
| knee_to_ankle_right_sheet | 4 | 14 m | 14 m | 6 |
| neck_left/right_sheet | 1+1 | 12 m | 12 m | 5 |
| foot_bottom_tpu (TPU) | 2 | -- | 41 m | 17 |
| body_middle_bottom | 1 | 2 h 20 m | 2 h 23 m | 81 |
| body_back | 1 | 2 h 04 m | 2 h 10 m | 67 |
| body_middle_top | 1 | 1 h 53 m | 1 h 54 m | 67 |
| body_front | 1 | 1 h 06 m | 1 h 30 m (supports) | 56 |
| speaker_stand | 1 | 33 m | 33 m | 7 |
| battery_pack_lid | 1 | 21 m | 24 m | 13 |
| flash_light_module | 1 | 20 m | 20 m | 7 |
| right_eye | 1 | 11 m | 11 m | 4 |
| flash_reflector_interface | 1 | 9 m | 8 m | 2 |
| speaker_interface | 1 | 7 m | 7 m | 2 |
| left_eye | 1 | 6 m | 5 m | 2 |
| bulb | 2 | 5 m | 5 m | 2 |

Variant B costs only ~3-10 % more time than the guide's settings while adding a third wall, so there is no reason to print at 2 walls.

### 7.3 Plates by colour / material (variant B, real auto-arranged runs)

Each group was fed to the CLI with the correct quantities (`--clone-objects`) and auto-arranged on the 256 × 256 bed; the slicer split a group onto a second plate only when it did not fit. Times are slicer estimates for the whole plate.

| Plate | Material / colour | Contents | Est. time | Filament | Tallest part |
|---|---|---|---|---|---|
| 1 | PLA, **orange** | foot_top ×2, foot_side ×2, foot_bottom_pla ×2 | **3 h 41 m** | 93 g | 68 mm |
| 2 | PLA, **white** (legs) | knee_to_ankle L/R sheets ×8, leg_spacer ×4, roll_motor_bottom ×2, roll_motor_top ×2, left/right_roll_to_pitch, left/right_cache | **8 h 42 m** (fits one plate; split into 2a brackets+sheets ≈ 4.7 h and 2b caches ≈ 4 h if you want a daytime-only plate) | 237 g | 153 mm |
| 3 | PLA, white (trunk) | trunk_bottom, trunk_top, neck L/R sheets, battery_pack_lid | **3 h 52 m** | 115 g | 74 mm |
| 4 | PLA, white (body) | body_middle_bottom, body_middle_top, body_back | **6 h 20 m** | 216 g | 150 mm (auto-orient stood body_middle_bottom on end; laid on its 150 × 110 face it is 86 mm tall and this plate drops to ≈ 6 h) |
| 5 | PLA, white (body) | body_front (did not fit on plate 4) | **1 h 30 m** | 56 g | 10 mm, flat |
| 6 | PLA, white (head) | head + head_pitch_to_yaw, head_yaw_to_roll, head_roll_mount, antenna holders ×2, eyes ×2, bulb ×2, flash_light_module, flash_reflector_interface, speaker_interface, speaker_stand | **8 h 22 m** | 246 g | 200 mm (auto-orient stood `head` on its side; printed on its flat base it is 59 mm tall and should be ~5.5 h for the head alone) |
| 7 | PLA, white (head) | head_bot_sheet (194 × 192 mm, needs a plate to itself) | **1 h 26 m** | 54 g | 3 mm |
| 8 | **TPU 95A**, black/grey | foot_bottom_tpu ×2 (print "by object") | **1 h 22 m** | 34 g | 8 mm |
| | | **Total** | **≈ 35 h 15 m** (33.9 h PLA + 1.4 h TPU) + ~30 min of per-plate heat-up/calibration | **≈ 1.02 kg PLA** (0.93 kg white + 0.09 kg orange) **+ 34 g TPU** | |

Sanity check against the only community figure: MakerWorld's profile reports **52.8 h over 6 plates** at 2 walls / 25 % infill. My 35 h at 3 walls / 15 % gyroid is plausible for an A1 at Bambu's default speeds (25 % infill and a slower printer profile explain most of the gap), but budget **40-55 h of printer time** for the first duck including reprints. Buy **2 × 1 kg white PLA, 1 × 1 kg orange PLA (you will use ~100 g), 1 × 500 g TPU 95A**.

Colour notes: the design has no separate beak part -- the beak is modelled into `head.stl` (see open question 4). The eyes (`left_eye`, `right_eye`), `bulb` and the flash parts are light-pipe/cosmetic pieces where you may want translucent/white; the "orange" plate above is just the feet.

### 7.4 Suggested sequence for week one

1. Day 1: unbox, calibrate, Bambu benchy, then **Plate: white legs** (small brackets + sheets; teaches you support removal and insert fitting on cheap parts; print one `leg_spacer` + one `roll_motor_bottom` first and test-fit an STS3215 and an insert).
2. Day 2: **feet (orange)** and the **TPU soles** (dry the TPU overnight on day 1).
3. Day 3-4: **trunk** and **body** plates (long prints; start in the morning).
4. Day 5: **head** plate (5.5 h for the head alone; print `head` by itself with the small head parts on a second plate).
5. Keep ~10 % spare time for reprints: the parts most likely to need a second attempt are `roll_to_pitch` (servo pocket fit; check issue #17 clearance), `head` (support scars in eye sockets), and the `*_cache` shells (tall, warp-prone without a brim).

---

## Open questions

1. **Exact BOM insert dimensions.** The amazon.fr listing's spec block was not readable without a browser; confirm it is the 4.6 mm OD / 5.7 mm long / 4.0 mm hole type. If it is the 5.0 mm OD "M3 x 5 x 4" Voron style, ream holes to 4.5 mm.
2. **MakerWorld profile internals.** Which printer the 6 plates were arranged for, per-plate hours, and whether the author hand-oriented parts. Needs a browser session with a MakerWorld login.
3. **Whether issue #17's clearance slot made it into the current STLs** -- check `roll_to_pitch` against your servo screw before gluing anything.
4. **Beak colour.** The beak is part of `head.stl`, so "orange beak" needs either a manual filament change at a layer height (Studio: right-click the layer slider -> "Add filament change"; the A1 pauses for a manual swap), painting, or a split-head mod. Which do you want?
5. **Insert count** is "TODO" in the BOM; my STL survey only sees vertical-axis holes. Count them while assembling and update this note.
6. **Local filament.** Bambu PLA Basic/TPU 95A HF are what the profiles assume; if you buy a local 95A TPU, run Studio's flow-rate and max-flow calibrations on it first.
