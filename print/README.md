# Printing the duck on the A1 — ready-made plates

Generated 2026-11-02 with Bambu Studio 02.07.01.62 (CLI) from the upstream v2 STLs in `../upstream/Open_Duck_Mini/print/`.
Open any file in `3mf/` in Bambu Studio, check the preview, send to the A1. Each 3MF already carries the printer, process and filament settings.

## Settings baked into the 3MFs

| Profile (in `profiles/`) | Used for | Walls | Infill | Supports | Other |
|---|---|---|---|---|---|
| `duck_pla_4walls` | brackets: feet, leg brackets, trunk, test plate | 4 | 15 % gyroid | tree(auto), 30° | 5 top / 4 bottom, auto brim |
| `duck_pla_3walls` | shells: caches, body, head parts | 3 | 15 % gyroid | tree(auto), 30° | same |
| `duck_tpu_sole` | the two TPU soles | 3 | 40 % gyroid | none | print **by object**, no brim |
| filament `fil_generic_pla_a1` | all PLA plates | 220 °C, 65 °C textured PEI, 12 mm³/s cap | | | |
| filament `fil_generic_tpu_a1` | soles | 240 °C, 45 °C bed, 3.2 mm³/s, flow-dynamics cali OFF | | | |

If your PLA is Bambu brand, switch the filament to "Bambu PLA Basic" in Studio; it prints ~25 % faster (21 mm³/s). For any other brand keep Generic PLA, it is the safe speed. The machine/filament/process JSONs in `profiles/` are fully flattened copies of the Bambu system presets because the CLI does not resolve preset inheritance (it otherwise slices for a 200 × 200 bed at 60 mm/s).

## Plates, in print order

| File | Parts | Est. time | Filament | Notes |
|---|---|---|---|---|
| `0_test_bracket.3mf` | roll_motor_bottom ×1, leg_spacer ×1 | 0 h 51 | 17 g | **Print this first.** Test-fit a servo in the pocket and an M3 insert in a hole before committing 60 h of filament |
| `1_feet_orange.3mf` | foot_top ×2, foot_side ×2, foot_bottom_pla ×2 | 5 h 09 | 128 g | orange if you have it; otherwise white |
| `2a_leg_brackets.3mf` | 2 plates: knee_to_ankle sheets ×8, leg_spacer ×4, roll_motor_bottom ×2, roll_motor_top ×2, left/right_roll_to_pitch | 5 h 09 + 3 h 38 | 194 g | sheets re-oriented flat (the upstream STLs are in robot frame, standing) |
| `2b_leg_caches.3mf` | left_cache, right_cache | 6 h 11 | 166 g | 153 mm tall shells; brim is on; start in the morning |
| `3_trunk.3mf` | trunk_bottom, trunk_top, neck sheets ×2, battery_pack_lid | 5 h 39 | 153 g | lid and neck sheets re-oriented flat |
| `4_body_stock.3mf` | 2 plates: body_back + body_middle_bottom; body_middle_top | 8 h 27 + 4 h 07 | 322 g | **stock 2-cell body_back.** Our 3S body_back is not modelled yet; print body_middle_* now, hold body_back until the 3S CAD exists (or print it anyway as a fit-check, 100 g) |
| `5_body_front.3mf` | body_front | 2 h 47 | 88 g | 143 mm tall, brim on |
| `6a_head_small.3mf` | 2 plates: head_pitch_to_yaw, head_yaw_to_roll, head_roll_mount, antenna holders, eyes, bulbs ×2, flash + speaker parts | 5 h 13 + 0 h 41 | 104 g | |
| `6b_head_stock.3mf` | head (stock, no camera opening) | **14 h 29** | **300 g** | The head is a hollow dome with eye and beak features that float without support, so ~100 g and 5 h of this is tree support. Hold until the camera face-plate version exists; print this only if you want the stock look now |
| `7_head_bot_sheet.3mf` | head_bot_sheet | 1 h 43 | 59 g | 194 × 192 mm flat plate, uses the whole bed |
| `8_tpu_soles.3mf` | foot_bottom_tpu ×2 (TPU) | 2 h 52 | 37 g | dry the TPU first (70 °C 8 h) or print from a freshly opened sealed bag; feed straight into the extruder, no glue on textured PEI |
| **Total** | 55 pieces | **≈ 67 h** | **≈ 1.53 kg PLA + 37 g TPU** | at Generic-PLA speeds; ~50 h with Bambu PLA Basic. Budget 2 × 1 kg white + a little orange |

The earlier 35 h estimate in `../research/printing-bambu-a1.md` assumed Bambu PLA speeds and a 5.5 h head; the head alone needs supports and is the big one.

## Before trusting a plate

Auto-arrange placed the parts; orientation is the STL's own except for the seven parts in `oriented/` (sheets, lid, head, head_bot_sheet), which were rotated flat and centred. In Studio, before printing each plate, look at the preview once for:
- shells standing on their open edge (`*_cache`, `body_front`, `body_back`): they must stand with the big flat edge on the plate and have the brim;
- `foot_top` (46 mm tall, supported): acceptable; if the support is messy, lay it on its flat top face instead;
- the servo pockets in `roll_motor_bottom` and `*_roll_to_pitch` must face up or sideways, never down onto supports;
- `head`: open side down, dome up, supports fill the cavity (expected).

## Day-1 printer checklist (short version of `../research/printing-bambu-a1.md` §6)

1. Unbox per the Bambu A1 guide; fit the 12 base screws and the purge wiper; slide the bed by hand through its full travel once.
2. Power on, run the on-screen calibration (bed level, vibration, motor noise, ~10 min). Update firmware. Wi-Fi or LAN-only mode, your choice; Studio works either way.
3. Load PLA on the external spool, print the bundled Benchy or a first-layer test once. Then `0_test_bracket.3mf`.
4. Push an M3 insert into the spacer with the iron at 200 °C; it should go in with gentle pressure and sit flush. If it falls in loose, the holes are oversized (XY compensation 0 is correct, check your filament flow); if it will not start, ream to 4.0 mm.
5. Drop a servo into the `roll_motor_bottom` pocket; it should seat without force. If tight, the usual cause is elephant foot on the first layer: enable 0.15 mm elephant-foot compensation and reprint the one part.

## Regenerating

`profiles/` holds the flattened presets; `oriented/` the re-oriented STLs; each `plates/<name>/` has the CLI `result.json` with per-object bounding boxes and feature-time breakdown. The CLI line used:

```
BambuStudio --load-settings "profiles/machine_a1_04.json;profiles/duck_pla_3walls.json" \
  --load-filaments profiles/fil_generic_pla_a1.json --clone-objects "1,1" \
  --arrange 1 --orient 0 --slice 0 --export-3mf out.3mf --outputdir out/ part1.stl part2.stl
```
