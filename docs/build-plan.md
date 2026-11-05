# Open Duck Mini v2 — build plan (ST3215 12 V · 3S · Radxa Zero 3W · camera + ToF head)

Written 2026-10-28. Owner: Hemang (Vadodara). Research behind every section is in `../research/` (six reports, all claims cited there). Shopping list: `shopping-list.md`.

## 0. Decisions in one screen

| Topic | Decision | Why (details in research) |
|---|---|---|
| Base design | Open Duck Mini v2 (apirrone), unchanged except 3 parts | Only open biped with proven sim2real on Feetech bus servos; XL330 (Microduck) unobtainable in India |
| Servos | 16× Waveshare **ST3215-HS 20 kg·cm 12 V, 106 rpm** (14 + 2 spare), 100 % torque, never clamped | Switched 2026-10-29: Hubtronics' 30 kg stock fell to 11, too few for 16 of one model. Same case → prints unchanged (68 g vs 55 g per servo, +180 g total, re-check masses in MJCF). Torque ≈ stock 7.4 V servo (20 vs 19.5 kg·cm), speed 2× (≈11 rad/s), kt 8.3 kg·cm/A, stall 2.4 A, no-load 240 mA. Raise `max_motor_velocity` in the MJCF after BAM identification; reference gait stays as is. Re-identify + retrain |
| Power | **3S1P** Li-ion (12.6 V max), 15 A fuse, BMS, MOSFET soft switch, 2×1000 µF at servo board | Adapter and servo both rated to 12.6 V. 3S1P ≈ 20–30 min walking. 3S2P only if >40 min needed |
| Brain | **Radxa Zero 3W 2 GB** (Hubtronics, 11 in stock, ₹5,760) | Pi Zero 2W drop-in (same holes, header, 22-pin CSI), 4× the RAM/CPU for camera + policy. Only in-stock Pi-Zero-footprint board in India |
| Control | Our own Python runtime, **goal positions to servo P controller at 50 Hz**, kp 30 legs / 8 head, kd 0 | Mirrors the upstream runtime that actually walks. PWM/torque mode was tried upstream and deleted |
| Policy | Our fork of Open_Duck_Playground, same 101-dim obs / 14-dim action, **actuator re-identified with BAM at 12 V**, masses updated, train on a rented RTX 4090 | Upstream maintainer's advice for 12 V users: re-identify and retrain. ~$1–3 per 300 M-step run |
| Printing | Bambu A1, PLA 0.2 mm, 3 walls (4 on brackets), 15 % gyroid, tree supports; TPU 95A soles 40 % | ~35 h, ~1.0 kg PLA + 34 g TPU across 8 plates. head.stl is 200 mm wide → needed the A1, not the mini |
| CAD changes | (1) body_back + lid for 3 cells, (2) head face plate with camera window + ToF aperture, (3) screw-head slot on roll_motor_bottom (#17) | Stock bay fits only 2 cells; stock head has no camera opening |
| Sensors | BNO085 (I2C3, Blinka) with BNO055 as proven fallback; IMX219 (22-pin cable, Pi5-style); VL53L8CX on I2C3 | Policy only needs gyro + accel. Camera/ToF are phase 5 |

## 1. What we are building and how it differs from stock

Stock Open Duck Mini v2: 42 cm, 14× STS3215 7.4 V, 2S 18650 in `body_back`, Pi Zero 2W in the **head**, Waveshare Bus Servo Adapter (A) on a tray at the rear of `trunk_top`, BNO055 on top of `trunk_top` behind the neck, UBEC in the head, 2× SG90 antennas, 4 foot switches, 3× 6804ZZ bearings (two hip-yaw pivots in `trunk_bottom`, one head-roll pivot in the head).

Ours:
- 12 V servos and 3S pack. Everything else on the servo side is identical (protocol, registers, mounting).
- Radxa Zero 3W on the Pi standoffs in the head. 5 V buck (AP64500) also in the head where the UBEC was.
- 3-cell bay: `body_back` rails widened from ~40 mm to ~58 mm, lid enlarged to ~70 × 86 mm, BMS slot moved. Pack weight +48 g (cells ≈ 141 g total).
- Head face: IMX219 window (module 25 × 24 mm, lens Ø ~8 mm) and VL53L8CX aperture (no cover glass; 65° diagonal FoV) in `head.stl`. Camera and ToF cables stay inside the head because the Radxa is there.
- Through the neck: servo bus chain (as stock), 12 V to the head buck, IMU I2C from trunk to head, foot-switch wires. (The stock USB Pi→adapter cable becomes a 3-wire UART.)

## 2. Timeline

| Phase | Dates (2026) | Goal | Gate to pass |
|---|---|---|---|
| 0 Orders + software scaffolding | Oct 28 – Nov 1 | Everything ordered; repo, protocol library, sim pipeline running on the Mac | `pytest` green on packet codec; `mujoco_infer.py` runs an upstream ONNX |
| 1 Printer + servos arrive | Oct 30 – Nov 5 | A1 calibrated, test coupon printed, plates 1–3 done; servos configured on the bench | A servo fits `roll_motor_bottom`; inserts seat at Ø4.0; all 16 IDs set, max-voltage register checked |
| 2 CAD mods + electronics bench | Nov 5 – 12 | Plates 4–7 printed; `body_back`/lid and head face modelled and printed; pack built; Radxa talks to servos, IMU, camera | 14 servos sync-read at 50 Hz from the Radxa with <2 ms bus time; IMU 100 Hz; camera frames |
| 3 Assembly + calibration | Nov 12 – 19 | Robot assembled, offsets found, stands under kp ramp; BAM identification of a spare servo | Duck stands 5 min on its own; BAM fit error acceptable |
| 4 Train + walk | Nov 19 – 30 | Playground fork with our actuator + masses; 3–10 cloud runs; first steps | Walks forward on command for 30 s without a fall, 3 trials |
| 5 Vision + polish | December | ToF stop/turn, camera stream, person following (optional), telemetry, docs | Stops before a wall at 30 cm |

Diwali is around Nov 8–10: expect courier slowdowns Nov 6–12. Everything that must arrive goes out today or tomorrow.

## 3. Ordering (today)

Full list with links: `shopping-list.md`. Changes from the research, already appended there:

1. **Hubtronics cart today:** 16× ST3215-HS 20 kg (₹2,399, 18 in stock 2026-10-29), 1× Bus Servo Adapter (A) (₹449, 12 in stock), 4× KW-12 microswitch (₹15), **1× Radxa Zero 3W 2 GB with header (₹5,760, 11 in stock)**. Call before paying to confirm dispatch this week and that the Radxa units are real stock. Stock is moving fast (30 kg unit went 33 → 11 in one day).
2. **Cells:** Molicel P30B or P28A if you can find them in India; otherwise the Samsung 30Q (15 A continuous, 20 A pulse) is acceptable for 3S1P with more sag at peaks.
3. **Add:** 15 A ATM blade fuse + holder, 2 A fuse for the 5 V branch, 2× 1000 µF 25 V low-ESR caps, 470–1000 µF + 10 µF for the Radxa header, 16 AWG wire for the three short pack links, anti-spark MOSFET switch module (or a 20 A 12 VDC switch), 3S JST-XH balance pigtail + socket, second XT30 for the charge port, 18650 insulating rings, a 70 °C filament dryer (A1 cannot dry on its bed; TPU must stay <20 % RH), Radxa heatsink (mandatory, throttles in 2 min bare), optional INA226 current monitor.
4. **Drop:** rocker switch (no DC rating), M2 screws.

## 4. Printing plan (Bambu A1)

Settings: 0.20 mm Standard @BBL A1 profile, **3 walls** (4 on `roll_motor_*`, `leg_spacer`, `*_roll_to_pitch`), **15 % gyroid**, textured PEI at 65 °C, PLA 220 °C, tree supports on `head`, `foot_top`, `*_roll_to_pitch`, `trunk_top`, brim on the 143–153 mm tall shells. TPU: Generic TPU 95A profile, 230 °C, 45 °C bed, no glue, flow-dynamics calibration off, feed from the dry box straight into the extruder, print the two soles "by object". Re-download the STLs from the v2 branch (hole fix of Mar 2025, issue #7) before slicing.

| Plate | Colour | Parts | Time | Filament |
|---|---|---|---|---|
| 1 | orange | foot_top ×2, foot_side ×2, foot_bottom_pla ×2 | 3 h 41 | 93 g |
| 2 | white | knee_to_ankle sheets ×8, leg_spacer ×4, roll_motor_bottom ×2, roll_motor_top ×2, L/R roll_to_pitch, L/R cache | 8 h 42 (or split 4.7 h + 4 h) | 237 g |
| 3 | white | trunk_bottom, trunk_top, neck sheets ×2, battery_pack_lid (stock, for reference only) | 3 h 52 | 115 g |
| 4 | white | body_middle_bottom (lay on its 150 × 110 face), body_middle_top, **body_back (our 3S version)** | ~6 h | 216 g |
| 5 | white | body_front | 1 h 30 | 56 g |
| 6 | white | **head (our face-plate version, printed flat, ~5.5 h)**, head_pitch_to_yaw, head_yaw_to_roll, head_roll_mount, antenna holders ×2, eyes ×2, bulb ×2, flash parts, speaker parts | ~8 h | 246 g |
| 7 | white | head_bot_sheet (194 × 192 mm, own plate) | 1 h 26 | 54 g |
| 8 | TPU | foot_bottom_tpu ×2 | 1 h 22 | 34 g |

Total ≈ 35 h, 1.0 kg PLA, 34 g TPU; budget 40–55 h with reprints. **Revised 2026-11-02 after slicing every plate for real (`print/README.md`): ≈ 67 h and 1.53 kg PLA at Generic-PLA speeds, ≈ 50 h with Bambu PLA Basic; the stock head alone is 14.5 h / 300 g because its dome and eye features need tree supports. Ready 3MFs are in `print/3mf/`.** Order: test coupon (one `roll_motor_bottom` + a 20 mm cube with four Ø4.0 insert holes) → plates 1, 2, 3 (nothing we modify) → 5, 7 → 4 and 6 once the CAD mods exist. The orange beak is part of `head.stl`: use a filament change at the beak's first layer in Bambu Studio, or paint.

Heat-set inserts: holes are modelled Ø4.0 mm → ruthex-type M3 × 5.7 mm long, 4.6 mm OD. Iron at 220–230 °C with the M3 insert tip, push to 90 % then press flush with a flat plate. Budget 80–100 inserts. Loctite 243 on every metal-to-servo screw, never on screws into plastic.

## 5. CAD modifications (Onshape copy of the v2 document, or Fusion/FreeCAD on the STEP from the community mods)

1. **body_back 3S bay.** Stock pocket: rails ~40 mm apart, ~80 mm tall, ~21 mm deep, lid 51.4 × 86.4 × 7.5 mm on the inner face. New: rails 58–60 mm apart for a 3-slot holder (~78 × 60 × 22 mm) or a Ø40 × 65 mm spot-welded triangle pack; 64 mm of shell width is available at pocket depth, 100 mm at the lid plane. Move the BMS slot (46 × 60 × 3.4 mm) beside the pack, add a lid cut-out for the XT30 charge port and JST-XH balance/alarm socket. If the holder route is taken, replace its spring contacts with leaf contacts or solder leads directly (springs sag at 10+ A).
2. **Head face plate.** Add a 10 mm window for the IMX219 lens, a 4-screw boss pattern for the module (M2 holes, 21 mm pitch) behind it, and a 10 × 10 mm aperture for the VL53L8CX with the breakout on standoffs. Keep the eyes. Position both at the duck's eye line so the ToF looks slightly down (10–15°) for floor obstacles.
3. **roll_motor_bottom slot** for the screw head that rubs `roll_to_pitch` (issue #17), if not already in the current STL.
4. Export the modified bodies as STL for printing **and** keep the assembly so masses/CoM can be exported to the MJCF (section 9).

## 6. Servo preparation (bench, before assembly)

Hardware: FTDI adapter → Bus Servo Adapter (A) UART, bench supply 12 V ≥ 3 A (or the finished 3S pack). Set `latency_timer=1` on the FTDI (udev rule from the upstream runtime README).

Per servo, with our `tools/configure_motor.py`:
1. Ping at 1 Mbps on the factory ID 1.
2. Unlock EEPROM (reg 55 = 0). Write ID (reg 5): right leg 10–14, left leg 20–24, neck/head 30–33. Baud reg 6 = 0 (1 Mbps). Return delay reg 7 = 0. P/I/D regs 21/23/22 = 32/0/32 (upstream defaults; runtime overrides P). Acceleration reg 41 = 0, max accel reg 85 = 0. Max torque reg 16 = 1000 (100 %). Angle limits regs 9/11 = 0/4095. **Read reg 14 (max voltage) and make sure it is ≥ 126 (12.6 V); raise to 130 if the batch ships lower.** Relock reg 55 = 1.
3. Move to 2048, mount the horn aligned as in `docs/configure_motors.md`. Soft offsets are found later on the assembled robot (`tools/find_offsets.py`) and stored in `duck_config.json`.
4. Log stall current, no-load speed at 12.0 and 12.6 V for two units (expect ~45 rpm ≈ 4.7 rad/s, 2.7 A stall). These numbers feed section 9.

Keep servos 15 and 16 as spares; servo 16 becomes the BAM identification unit.

## 7. Electrical architecture

```
3S pack (3× 18650, 9.0–12.6 V)        ── B-, B1, B2, B+ ──► 3S 40 A BMS (same-port P+/P-)
   │ balance lead JST-XH 4-pin ──► lid socket (charger balance / LiPo alarm 3.5 V per cell)
   └► P+ ── 15 A ATM fuse ── MOSFET soft switch ── XT30 (main) ──┬► Bus Servo Adapter (A) screw terminal (+2×1000 µF 25 V)
                                                                 │      └► 14× ST3215 daisy chain (3 A/pin headers; split chain into 2–3 branches)
                                                                 ├► 2 A fuse ── AP64500 buck 5 V/5 A ──► Radxa header pins 2/4 (+470–1000 µF), camera, ToF, IMU, 2× SG90
                                                                 └► XT30 (charge port on lid, parallel to P+/P-)
Radxa Zero 3W: UART5 (pins 32/33, /dev/ttyS5, 1 Mbps, 3.3 V) ──► adapter UART header
               I2C3 (pins 3/5, 400 kHz via custom overlay) ──► BNO085 (trunk) + VL53L8CX (head) (+ INA226 optional)
               PWM8/PWM9 (pins 16/18) ──► SG90 antennas         GPIO 22/27 ──► foot switches (2 per foot, parallel)
               22-pin CSI ──► IMX219
```

Budget: 14 servos idle 2.8 A, walking estimate 6–10 A at 3S, stall-all 38 A (fuse and BMS handle). Radxa 3–4 W, camera 1.3 W, ToF 0.5 W → 5 V branch < 2 A. Wire: 16 AWG pack→fuse→switch→adapter (≤15 cm), 18 AWG servo rail, 20 AWG 5 V branch. Charging: iMax B6AC, **LiPo 3S program** (LiIo stops at 4.1 V/cell), 1.5 A for 30Q, 3 A for P30B, through the lid XT30 + balance socket. Alarm at 3.5 V/cell, software stop at 3.3 V/cell (read pack voltage from a servo's reg 62 or the INA226).

Checks on first power-up: thermal-camera or touch the adapter's P-FET after 5 min of walking (its ~10–12 A continuous rating is the weakest link); scope the 5 V rail under a servo stall; verify the BMS does not trip on the 2000 µF inrush with the soft switch (drop to 1000 µF if it does).

## 8. Assembly sequence (follow `docs/assembly_guide.md`, with our deltas)

1. Feet: TPU sole to `foot_bottom_pla` (2× M3×6), inserts in `foot_top`, press-fit KW-12 switches (trim the hinge lever or lengthen the ~6 × 15–20 × 7.5 mm slot), ankle servo.
2. Legs: knee/ankle sheets, `leg_spacer` inserts (4), servo cable routed through the right sheet as in the guide. Both legs.
3. Hips/trunk: two 6804ZZ in `trunk_bottom`, inserts, hip-yaw servos with `roll_motor_top`, join `trunk_bottom`/`trunk_top` (2× M3×10). Mount the adapter on its tray, IMU on the trunk block (natural orientation, chip up, X forward; record the mounting in config).
4. Body: `body_middle_bottom`, inserts, our `body_back` with the pack, BMS, fuse, switch; `body_middle_top`, `body_front`.
5. Neck + head: neck servos (30–33), third bearing in the head, Radxa on the standoffs with heatsink, buck, camera and ToF on our face plate, antenna SG90s, eyes. Route the harness through the neck sheets with 30 mm of slack per joint; test full neck travel before closing.
6. Power-up with torque off; run `tools/find_offsets.py`; stand with kp ramp 2 → 30 over 3 s.

## 9. Radxa bring-up

- OS: Radxa Debian 12 (kernel 6.1, Python 3.11). Enable overlays with `rsetup`: `rk3568-uart5-m1` (check it carries `radxa,zero3`; else use UART4 pins 16/18 and move antennas to PWM14/15), `rk3568-i2c3-m0`, PWM8/9, `radxa-zero3-rpi-camera-v2`. Custom 10-line overlay for I2C3 at 400 kHz. Do not use UART2 (boot console).
- Camera: GStreamer `v4l2src` path only (no libcamera); run `rkaiq_3A_server` or frames come out dark green; vendor driver gives 1080p30 (expect 20–30 fps). If the 6.1 image misbehaves, fall back to the Bullseye 5.10 image (confirmed working reports). Check the FPC connector orientation on the received board (some V1.12 units inverted).
- Python: `onnxruntime` 1.31 aarch64 wheel, `pyserial`, Adafruit Blinka (`radxazero3` board file: I2C/SPI/GPIO work, PWM does not → use `python-periphery` or sysfs for PWM), `adafruit-circuitpython-bno08x`, `smbus2`. Pin CPU governor to performance; run the control loop with `SCHED_FIFO` priority.
- Power the board from header pins 2/4 (official 5 V input), never from USB-C while the header is fed.

## 10. Software we will write (`~/OpenDuck`, Python 3.11)

```
duck/
  bus/feetech.py        # packet codec, PING/READ/WRITE/SYNC_READ 0x82/SYNC_WRITE 0x83, register map, EEPROM lock
  bus/serial_port.py    # pyserial, 1 Mbps, half-duplex timing, timeouts
  hw/servos.py          # 14-joint view: ids, offsets, rad<->ticks, kp set, torque on/off, sync read pos+vel, sync write goal
  hw/imu_bno08x.py      # gyro + accel at 100 Hz (I2C3), mounting rotation, bias
  hw/feet.py            # GPIO 22/27 switches
  hw/antennas.py        # PWM8/9
  hw/power.py           # pack voltage from servo reg 62 or INA226, low-battery policy
  control/observation.py# 101-dim obs exactly as upstream: gyro3, accel3, cmd7, dof_pos-init14, dof_vel*0.05 14, last 3 actions 42, motor_targets14, feet2, phase cos/sin 2
  control/policy.py     # onnxruntime CPU, input "obs" (1,101), output 14 tanh -> init_pos + 0.25*a
  control/loop.py       # 50 Hz, sync read -> obs -> policy -> head cmd mix -> optional low-pass -> sync write; timing stats
  control/safety.py     # torque-off on |pitch|>60° or |roll|>60°, bus timeout, temperature reg 63 > 65 °C, low battery, watchdog
  control/calibration.py# find offsets, standing pose, kp ramp
  teleop/gamepad.py     # Xbox/any gamepad over Bluetooth -> vx, vy, wz, head 4
  perception/camera.py  # GStreamer v4l2src -> frames (phase 5)
  perception/tof.py     # VL53L8CX 8x8 @ 15 Hz -> min range per column -> stop/turn command (phase 5)
tools/configure_motor.py, find_offsets.py, bench_servo.py (speed/stall logging), bus_benchmark.py
sim/ (fork of Open_Duck_Playground as a submodule) + sim/bam/ (identification scripts and our params)
tests/ (pytest: packet encode/decode against known-good bytes from the FTServo SDK, obs assembly, safety thresholds)
```

Order of work, so nothing waits on hardware: (0) packet codec + tests, obs assembly + tests, loop skeleton with a fake bus (Phase 0); (1) real bus on the bench with 1–16 servos, timing benchmark (Phase 1); (2) IMU, feet, antennas, power on the Radxa (Phase 2); (3) calibration and stand (Phase 3); (4) policy + teleop (Phase 4); (5) perception (Phase 5). Keep the observation layout identical to upstream so upstream ONNX files can be used as a smoke test of the plumbing (they will not walk well on 12 V servos, but they must not crash).

## 11. Actuator identification and training

1. **BAM identification (Phase 3, spare servo 16):** print the BAM pendulum rig, fit a known mass, run the BAM trajectories at 12.0 V and 12.6 V, fit model m1 (and m6 if time) as a new `feetech_sts3215_12V` actuator (subclass the existing STS3215 class; vin 12, firmware kp 32, error_gain 0.166, max_pwm 0.97, 3400 step/s rate limit). Compare with the Waveshare ST3025 12 V set (kt 1.62, R 3.73) as a sanity bound.
2. **Export to MuJoCo:** kp = 0.166·32·vin·0.97·kt/R, forcerange = vin·kt/R, damping = visc + kt²/R, armature, frictionloss. Stock 7.4 V values for reference: kp 17.1, forcerange ±3.23 N·m, damping 0.56, frictionloss 0.068, armature 0.027. Set `max_motor_velocity` to the measured no-load speed (~4.7 rad/s, not 5.24).
3. **MJCF masses:** update `body_back` mass/CoM (+48 g cells, new shell) and head (Radxa + camera + ToF + buck ≈ +40 g) in `open_duck_mini_v2_backlash.xml`, either by re-exporting from the Onshape copy with onshape-to-robot (`docs/prepare_robot.md`) or by editing the two `<inertial>` blocks. Keep the backlash joints.
4. **Domain randomization:** add vin ∈ [10.5, 12.6] V (BAM MujocoController supports it), keep friction 0.5–1, mass ×0.9–1.1, torso ±0.1 kg, CoM ±5 cm, kp ×0.9–1.1, pushes. Reference motion (Placo polynomials, ~0.40 s period) stays as is unless the measured servo speed is <4.5 rad/s, then regenerate with a longer `single_support_duration`.
5. **Train:** RunPod RTX 4090 (community ~$0.34–0.89/h) or L4, `jax[cuda12]`, driver ≥ 525, avoid RTX 50xx. `runner.py --task flat_terrain_backlash --num_timesteps 300000000`, expect 1–3 h → $1–3 per run; plan 3–10 runs (~$10–30). `export_onnx.py` → `mujoco_infer.py -o policy.onnx` → copy to the Radxa.
6. **Deploy:** stand → step in place → forward at 0.1 m/s → turn. Log 101-dim obs + actions + servo temp/current at 50 Hz to parquet for every trial; compare joint tracking against sim (upstream users measured knees reaching only 31–49 % of commanded range on 7.4 V units, so expect to tune kp/low-pass).

## 12. Vision (Phase 5)

Camera: GStreamer v4l2src → 640×480 @ 20–30 fps → optional person detection (YOLO-nano via onnxruntime, 2–5 fps on the Radxa) → bearing to target → `wz` command. ToF: VL53L8CX 8×8 at 15 Hz on I2C3 (ST ULD C driver with a thin Python binding, or the Pololu Arduino driver ported), take min distance per column, stop at <0.30 m, turn toward the freer side. Both run as separate processes publishing commands over ZMQ to the control loop, which treats them exactly like gamepad input. Expressions (eye LEDs, speaker) are optional extras from the upstream guide.

## 13. Risks and open questions

| Risk | Mitigation |
|---|---|
| Hubtronics stock not real / dispatch slips past Diwali | Call before paying; fallback Zbotic ST3215-HS (19 in stock on 10-27, ₹2,288, verify by hand since the site now blocks automated checks). Last resort: 11× 30 kg (legs + 1 spare) from Hubtronics plus 5× HS for head + spare, accepting two actuator models in sim |
| 12 V servo max-voltage register below 12.6 V | Read reg 14 on arrival, raise to 130 |
| 3S bay redesign takes longer than printing | Print all unmodified plates first; a temporary external pack on a strap lets Phase 3 start |
| Adapter P-FET / headers overheat at 10–12 A | Split the servo chain into 2–3 branches off the screw terminal; thermal check; quack-core style board later |
| BNO085 clock stretching on RK3566 I2C | Fallback BNO055 (proven upstream, Blinka) or BNO085 over SPI3 |
| Camera on the 6.1 kernel image | Fallback Bullseye 5.10 image; camera is not needed until Phase 5 |
| Slower servo breaks the upstream gait | Measured speed into `max_motor_velocity`; regenerate reference motion if < 4.5 rad/s |
| Unknown real walking current | INA226 on the pack line from day one |
| Radxa 2 GB vs 4 GB | 2 GB is plenty for policy + camera + ToF; swap-free, no desktop |

Open items to settle during Phase 1–2: exact neck cable routing (not documented upstream), KW-12 fit in the foot slot, UART5 overlay compatibility, whether the Robocraze BMS trips on capacitor inrush, true heat-set insert count.

## 14. References

- `../research/odm-hardware.md` — layout, battery bay, STL bounding boxes, bearings, community forks (feisuo Rockchip runtime with a 12 V ONNX, Jetson 3S2P build, Park Head camera face-plate mod)
- `../research/servo-st3215.md` — specs, register map, protocol timing, BAM model and Playground parameters
- `../research/radxa-zero-3w.md` — pinout, overlays, camera path, power, availability
- `../research/rl-and-runtime.md` — control loop, obs/action spec, MJCF actuator values, training cost
- `../research/printing-bambu-a1.md` — profiles, plate plan, inserts, TPU, humidity
- `../research/power-3s.md` — adapter schematic, currents, BMS, charging, wiring diagram
- Upstream: https://github.com/apirrone/Open_Duck_Mini (v2), Open_Duck_Playground, Open_Duck_Mini_Runtime (v2), https://github.com/Rhoban/bam
