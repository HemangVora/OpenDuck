# Servo setup: all 14 ST3215-HS servos, from the Mac

Tool: `tools/servo_setup.py` (does what upstream `configure_motor.py` does, plus 12 V checks).
Do this **before** building any joint. Each servo gets an ID and is parked at its zero (2048) so you can fit the horn.

## 0. What you need on the table

- Waveshare **Bus Servo Adapter (A)**, jumper set to the **USB** position
- **USB-C data cable**, adapter to the Mac
- **12 V supply** into the adapter DC jack (5.5 x 2.1) or green terminal: 12 V 2 A+ wall adapter, or the 3S pack. Never above 12.6 V.
- The 14 servos + their 3-pin cables + their horns and horn screws
- Masking tape and a marker for labels

## 1. Rule: one servo on the bus at a time

New servos all ship as ID 1. If two are connected while setting IDs, both get the same ID.
Plug **only one** servo into the adapter for steps 3 to 5. All servos together only in step 7.

## 2. First connection (once)

1. Plug the adapter into the Mac with USB-C. Power the adapter with 12 V.
2. Open Terminal:
   ```bash
   cd ~/OpenDuck/tools
   .venv/bin/python servo_setup.py ports
   ```
   You should see something like `/dev/cu.usbmodem…` or `/dev/cu.wchusbserial…`.
   Nothing new? Different USB-C cable (data, not charge-only), check the jumper.

## 3. Check the first servo

Plug in servo #1 only.
```bash
.venv/bin/python servo_setup.py scan
```
Expect: `servos found: [(1, 'unassigned')]` and about `12.0 V`. (Scanning takes ~15 s.)
Then:
```bash
.venv/bin/python servo_setup.py info --id 1
```
Look at the `limits` line: the max must be at or above your supply (e.g. `… 14.0 V`). If the tool prints `!!`, stop.

## 4. Configure it

```bash
.venv/bin/python servo_setup.py setup right_hip_yaw
```
It must end with `DONE: id 10 = right_hip_yaw` and `holding at ~2048`. The servo is now stiff at zero.

## 5. Horn, label, unplug

1. While it holds zero, push the horn on so it lines up like the photo in
   `upstream/Open_Duck_Mini/docs/configure_motors.md`. Close is fine: small offsets are calibrated later on the built robot.
   Do not turn the output by hand while it holds (it fights you); if the horn needs a different spline position, lift it off and re-seat it.
2. Fit the horn screw.
3. Label the servo body: `10 R HIP YAW`.
4. Unplug it, plug in the next new servo, and repeat steps 4 and 5 with the next name.

## 6. The 14 names, in order

| # | command | ID | label |
|---|---|---|---|
| 1 | `setup right_hip_yaw` | 10 | R HIP YAW |
| 2 | `setup right_hip_roll` | 11 | R HIP ROLL |
| 3 | `setup right_hip_pitch` | 12 | R HIP PITCH |
| 4 | `setup right_knee` | 13 | R KNEE |
| 5 | `setup right_ankle` | 14 | R ANKLE |
| 6 | `setup left_hip_yaw` | 20 | L HIP YAW |
| 7 | `setup left_hip_roll` | 21 | L HIP ROLL |
| 8 | `setup left_hip_pitch` | 22 | L HIP PITCH |
| 9 | `setup left_knee` | 23 | L KNEE |
| 10 | `setup left_ankle` | 24 | L ANKLE |
| 11 | `setup neck_pitch` | 30 | NECK PITCH |
| 12 | `setup head_pitch` | 31 | HEAD PITCH |
| 13 | `setup head_yaw` | 32 | HEAD YAW |
| 14 | `setup head_roll` | 33 | HEAD ROLL |

The 2 spares: leave them at ID 1, unlabeled, in the box.

## 7. Final check: all together

Daisy-chain all 14 (servo to servo, or several into the adapter's ports), 12 V on, then:
```bash
.venv/bin/python servo_setup.py scan
```
It must list exactly the 14 IDs 10-14, 20-24, 30-33, all at ~12 V. A missing ID: that servo or its cable. An `id 1` in the list: a servo that was never configured.
Turn torque off on all before unplugging if you like: `servo_setup.py relax --id N`.

## Troubleshooting

| Message | Fix |
|---|---|
| `No USB serial port found` | data cable, jumper on USB, `servo_setup.py ports` |
| `No servo answers` | 12 V on? 3-pin plug fully in? try the other adapter port |
| `Found 2 servos …` | unplug all but one |
| `!! … ABOVE this servo's max-voltage limit` | stop: not a 12 V unit or wrong supply. Send the output. |
| `Readback mismatch` | run the same `setup` again |
| holding error bigger than ~10 steps | normal-ish without load; just re-run `center --id N` |
| need zero again later (horn refit) | `servo_setup.py center --id N` |
