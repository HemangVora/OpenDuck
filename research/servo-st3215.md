# Feetech STS3215 / Waveshare ST3215 research for Open Duck Mini v2 on 3S (12 V / 30 kg·cm unit)

Researched 2026-10-28. Every fact is tagged with its source; items marked **[inference]** are my own reasoning, not something a source states. Downloaded primary documents are in
`/private/tmp/claude-501/-Users-hemangvora/c8a30d1f-0498-4660-9327-b47c73ee9657/scratchpad/agents/servo/dl/`
(Feetech STS3215 datasheet, Seeed ST3215-C047 datasheet, Waveshare `ST3215 memory register map-EN.xls` V3.7, Waveshare Communication Protocol manual, Waveshare ST3215 user manual, Open Duck BOM CSV). Repos cloned next to it: `bam/`, `playground/`, `runtime/` (branch v2), `ftpy/` (FTServo_Python), `ftlinux/` (FTServo_Linux).

---

## 1. Specifications

### 1.1 Spec table

| Item | STS3215 7.4 V (ST3215-C001, "19 / 19.5 kg·cm") | STS3215 12 V 30 kg·cm (ST3215-C018; Seeed sells it as ST3215-C047; Waveshare "ST3215 12V" SKU 22414) | Waveshare ST3215-HS (SKU 25127) |
|---|---|---|---|
| Gear ratio | **1:345** [Feetech datasheet p.4 item 6-11][DS]; Seeed wiki lists C001 = 1:345 [SEEED-WIKI] | **1:345** (Seeed C047 datasheet: "1:345 metal gearbox" [C047]; Seeed wiki: C047 12 V 1:345 [SEEED-WIKI]). Not stated anywhere for "C018" by name, but C047 and C018 are the same 12 V/30 kg product sold by Seeed vs Feetech/Eckstein **[inference]** | not published; 106 rpm at 20 kg·cm implies a lower ratio **[inference]** |
| No-load speed @ rated V | 0.192 s/60° = **52 rpm @ 7.4 V**; 0.238 s/60° = 42 rpm @ 6 V [DS p.3]. Waveshare register-map header: 3400 step/s = 49.8 rpm @ 7.4 V [XLS] | 0.222 s/60° = **45 rpm @ 12 V** [WS-PROD][WS-WIKI][EVELTA] | 0.094 s/60° = **106 rpm @ 12 V** [WS-HS] |
| Stall torque | **19.5 kg·cm @ 7.4 V** (16.5 @ 6 V) [DS p.3]; Waveshare says 19.5 kg·cm @ 7.4 V [WS-PROD] | **30 kg·cm @ 12 V** [WS-PROD][EVELTA] ("peak stall torque") | **20 kg·cm @ 12 V** [WS-HS] |
| Rated (continuous) torque | 5 kg·cm @ 7.4 V (4 @ 6 V) [DS p.3] | 10 kg·cm @ 12 V [EVELTA] | not published |
| Stall current | 2.5 A @ 7.4 V (2 A @ 6 V) [DS p.3][WS-PROD] | 2.7 A @ 12 V [WS-PROD][WS-WIKI][EVELTA] | 2.4 A [WS-HS] |
| Running current, no load | 150 mA @ 7.4 V (130 @ 6 V) [DS p.3][XLS] | 200 mA [WS-PROD][WS-WIKI]; 180 mA @ 12 V [EVELTA] | 240 mA [WS-HS] |
| Idle current (stopped) | 6 mA [DS p.3] | not published | not published |
| Rated current | 650 mA @ 7.4 V (500 @ 6 V) [DS p.3] | not published | not published |
| Working voltage | 4–7.4 V [DS p.3][WS-PROD] | **6–12.6 V** [WS-PROD][WS-WIKI]; Evelta/Eckstein list "4–14 V" [EVELTA]; Seeed C047 "4–14 V" [C047] | 6–12.6 V [WS-HS] |
| kt (torque constant) | 8 kg·cm/A [DS p.3] = 0.785 N·m/A; Waveshare: 7.8 kg·cm/A [WS-PROD] | 11 kg·cm/A [WS-PROD] = 1.079 N·m/A | 8.3 kg·cm/A [WS-HS] |
| Motor terminal resistance | 2.5 Ω [DS p.3] | not published; V/I_stall = 12/2.7 = 4.44 Ω **[inference]** | — |
| Motor type | "Core motor" (cored/brushed) [DS p.4 6-14] | "Core Motor" [EVELTA] | — |
| Weight | 55 ± 1 g [DS p.4 6-8] | 55 ± 1 g [EVELTA] | 68 g [WS-HS] |
| Dimensions | 45.2 × 24.7 × 35 mm [DS p.4]; drawing 45.23 × 24.73 × 35 (36.5 incl. horn) [DS p.6] | 45.2 × 24.7 × 35 mm [EVELTA][C047]; Waveshare 45.22 × 35 × 24.72 [WS-WIKI] | drawing only [WS-HS] |
| Encoder | 12-bit magnetic, 360°/4096 = 0.088°/step, no mechanical limit, multi-turn ±7 turns not saved at power-off [DS p.4-5][WS-WIKI] | same [WS-PROD] | same [WS-HS] |
| Operating temperature | storage −30…80 °C, operating −20…60 °C [DS p.3] | −20…60 °C [EVELTA]; Seeed C047: −10…60 °C [C047] | not published |
| Firmware over-temp limit | register 13 default 70 °C → torque cut [XLS]; datasheet: overheat protection above 70 °C [DS p.5] | same register table | same |
| Output shaft | 25T, Ø5.9 mm spline, M3×6 screw; dual-axis (passive bearing on back) [DS p.4] | same [C047] | — |
| Backlash | ≤ 0.5° [DS p.4 6-12] | — | — |
| Life test | > 100 000 cycles (fwd 60° 0.25 s, stop 0.5 s, back 0.25 s, stop 0.5 s) at 1/5 stall torque [DS p.6] | — | — |
| Max position update rate | 1 ms [DS p.8] | — | — |

Sources: [DS] = Feetech STS3215 product specification A/0 (2020-04-10), machine-translated, https://core-electronics.com.au/attachments/uploads/sts3215-smart-servo-datasheet-translated.pdf ; [C047] = Seeed "Feetech ST3215-C047 12V 30Kg Servo" datasheet, https://store.comet.bg/download-file.php?id=31780 (also https://www.seeedstudio.com/STS3215-30KG-Serial-Servo-p-6340.html) ; [SEEED-WIKI] = https://wiki.seeedstudio.com/feetech_servo/ ; [WS-PROD] = https://www.waveshare.com/st3215-servo.htm ; [WS-WIKI] = https://www.waveshare.com/wiki/ST3215_Servo ; [WS-HS] = https://www.waveshare.com/product/modules/st3215-hs-servo-motor.htm ; [EVELTA] = https://evelta.com/sts3215-c018-12v-30kg-cm-dual-shaft-ttl-serial-servo-metal-gears-magnetic-encoder/ ; [XLS] = https://files.waveshare.com/upload/2/27/ST3215%20memory%20register%20map-EN.xls (V3.7, header "firmware 2.43").

Unit conversions: 1 kg·cm = 0.0980665 N·m → 19.5 kg·cm = 1.91 N·m, 30 kg·cm = 2.94 N·m, 20 kg·cm = 1.96 N·m, 10 kg·cm = 0.98 N·m, 5 kg·cm = 0.49 N·m. 52 rpm = 5.45 rad/s, 45 rpm = 4.71 rad/s, 106 rpm = 11.1 rad/s, 3400 step/s = 5.216 rad/s.

### 1.2 Is the 12 V unit the same gearbox with a different winding?

- Evidence: same 1:345 ratio [DS][C047][SEEED-WIKI], same 45.2×24.7×35 mm case and 55 g [DS][EVELTA], both "core motor" [DS][EVELTA], same 25T horn; Waveshare lists different kt (7.8 vs 11 kg·cm/A) and stall currents (2.5 vs 2.7 A) [WS-PROD].
- **[inference]** Identical mechanics + kt ratio 1.41 + implied winding resistance 2.96 Ω (7.4/2.5) vs 4.44 Ω (12/2.7) is exactly what a higher-turn-count winding of the same motor frame looks like. So yes: same gearbox, same magnet/frame, different winding. Nothing from Feetech states this explicitly.
- Consequence **[inference]**: at its rated voltage the 12 V unit has 1.54× the stall torque (30/19.5) but only 0.87× the no-load speed (45/52) of the 7.4 V unit. Continuous (thermal) rating is 2× (10 vs 5 kg·cm).

### 1.3 Does the 12 V unit run safely at 12.6 V (full 3S)?

- Waveshare rates the 12 V ST3215 and the ST3215-HS at **6–12.6 V** and says "12V is recommended" for the ESP32 driver board [WS-PROD][WS-WIKI][WS-HS]. Feetech/Seeed/Evelta list 4–14 V for C018/C047 [EVELTA][C047]. The Waveshare Bus Servo Adapter (A) input is 9–12.6 V [WS-ADAPTER]. So a freshly charged 3S pack at 12.6 V is inside every published range. At 12.6 V expect ≈ +5 % torque and speed (31.5 kg·cm, 47 rpm) **[inference, linear scaling]**.
- Firmware caveat: EEPROM register 14 "maximum input voltage" (unit 0.1 V) triggers the voltage-protection bit and unloads the servo when exceeded (unload-condition bit0 is enabled by default) [XLS]. On the 7.4 V unit it defaults to 80 (8.0 V). The 12 V units must ship with a higher default (not documented in any source I found; read it with the FD tool before trusting 12.6 V). **Open question.**
- The STS3215-HS and 12 V units both still have the 70 °C over-temperature cut-off [XLS].

---

## 2. Memory table (SMS/STS register map)

Authoritative source: Waveshare `ST3215 memory register map-EN.xls` V3.7 [XLS]. Cross-checked against Feetech FTServo SDK `SMS_STS.h` / `sms_sts.py` [FT-LINUX][FT-PY], pypot `sts3215_io.py` [PYPOT], rustypot `sts3215.rs` [RUSTYPOT-STS], and the AIFitLab STS memory table page [AIFIT]. All multi-byte values are **little-endian (low byte at the lower address)** for STS/SMS (magnetic-encoder series); the potentiometer SCS series is big-endian [PROTO p.2][XLS].

### 2.1 EEPROM (persist across power cycles; need lock = 0 to persist)

| Addr dec (hex) | Name | Bytes | Default | Range | Unit / meaning |
|---|---|---|---|---|---|
| 0–1 | Firmware major / minor version | 1+1 | 3 / 7 | RO | — |
| 3–4 (0x03) | Servo major / minor version ("model number") | 1+1 | 9 / 3 | RO | SDK `ping` reads 2 bytes at 3 as the model number; STS3215 reports **777** [RUSTYPOT-README] |
| 5 (0x05) | **ID** | 1 | 1 | 0–253 | 254 (0xFE) = broadcast, no reply except PING |
| 6 (0x06) | **Baud rate** | 1 | 0 | 0–7 | 0=1 000 000, 1=500 000, 2=250 000, 3=128 000, 4=115 200, 5=76 800, 6=57 600, 7=38 400 |
| 7 (0x07) | **Return delay** | 1 | **0** | 0–254 | ×2 µs; max 508 µs. Factory 0 confirmed on a real unit [ZENN] |
| 8 (0x08) | Response status level | 1 | 1 | 0–1 | 0 = reply only to READ and PING; 1 = reply to every instruction |
| 9–10 (0x09) | **Min angle limit** | 2 | 0 | −32766… | steps; set 0 for multi-turn mode |
| 11–12 (0x0B) | **Max angle limit** | 2 | 4095 | …32767 | steps; set 0 for multi-turn mode |
| 13 (0x0D) | Max temperature | 1 | 70 | 0–100 | °C |
| 14 (0x0E) | Max input voltage | 1 | 80 (7.4 V unit) | 0–254 | 0.1 V |
| 15 (0x0F) | Min input voltage | 1 | 40 | 0–254 | 0.1 V |
| 16–17 (0x10) | **Max torque** | 2 | 1000 | 0–1000 | 0.1 %; "1000 = 100 % of locked-rotor torque"; copied into addr 48 at power-up |
| 18 (0x12) | Phase | 1 | 12 | 0–254 | special bits (bit4 = multi-turn feedback); do not touch |
| 19 (0x13) | Unloading conditions | 1 | 44 | bitmask | bit0 voltage, bit1 sensor, bit2 temperature, bit3 current, bit4 angle, bit5 overload → 1 = unload (torque off) on that fault |
| 20 (0x14) | LED alarm conditions | 1 | 47 | bitmask | same bits → LED flashes |
| 21 (0x15) | **Position-loop P** | 1 | **32** | 0–254 | — |
| 22 (0x16) | **Position-loop D** | 1 | **32** | 0–254 | — |
| 23 (0x17) | **Position-loop I** | 1 | 0 | 0–254 | — |
| 24–25 (0x18) | Minimum starting force | 2 | 16 | 0–1000 | 0.1 % of stall torque |
| 26 (0x1A) | CW dead zone | 1 | 1 | 0–32 | steps |
| 27 (0x1B) | CCW dead zone | 1 | 1 | 0–32 | steps |
| 28–29 (0x1C) | **Protection current** | 2 | 500 | 0–511 | ×6.5 mA → default 3.25 A |
| 30 (0x1E) | Angle resolution | 1 | 1 | 1–3 | multiplier on 0.088°/step for multi-turn |
| 31–32 (0x1F) | **Position correction (offset)** | 2 | 0 | −2047…2047 | steps; bit11 = sign |
| 33 (0x21) | **Operating mode** | 1 | 0 | 0–3 | 0 = position servo; 1 = constant-speed (wheel) via addr 46, bit15 dir; 2 = PWM open-loop via addr 44, bit10 dir; 3 = step mode (addr 42 = step count; set 9 and 11 to 0) |
| 34 (0x22) | Protective torque | 1 | 20 | 0–100 | % of max torque output after overload protection trips |
| 35 (0x23) | Protection time | 1 | 200 | 0–254 | ×10 ms (load above overload torque for this long → protection) |
| 36 (0x24) | **Overload torque** | 1 | 80 | 0–100 | % of max torque threshold that starts the protection timer |
| 37 (0x25) | Speed-loop P (mode 1) | 1 | 10 | 0–100 | — |
| 38 (0x26) | Over-current protection time | 1 | 200 | 0–254 | ×10 ms |
| 39 (0x27) | Speed-loop I (mode 1) | 1 | 10 | 0–254 | 1/10 |

### 2.2 SRAM (volatile)

| Addr dec (hex) | Name | Bytes | Default | Range | Unit / meaning |
|---|---|---|---|---|---|
| 40 (0x28) | **Torque enable** | 1 | 0 | 0/1/128 | 0 off, 1 on, **128 = calibrate current position to 2048 (middle)** [XLS]; AIFitLab also lists 2 = damping mode [AIFIT] |
| 41 (0x29) | **Acceleration** | 1 | 0 | 0–254 | ×100 step/s² (= 8.79 °/s²); **0 = maximum** |
| 42–43 (0x2A) | **Goal position** | 2 | 0 | −30719…30719 | steps, bit15 = sign (sign-magnitude, SDK `scs_toscs(x,15)`) |
| 44–45 (0x2C) | Goal time / PWM | 2 | 0 | 0–1000 | in mode 2: duty 0.1 %, range 50–1000, bit10 dir. (SDK calls it "goal time"; pypot "goal time") |
| 46–47 (0x2E) | **Goal speed** | 2 | 0 | 0–3400 | step/s; 50 step/s = 0.732 rpm; **0 = max** |
| 48–49 (0x30) | **Torque limit** | 2 | 1000 (from addr 16) | 0–1000 | 0.1 %; "user can modify to control the output of the maximum torque" |
| 55 (0x37) | **Lock flag** | 1 | 0 (XLS) / 1 (AIFitLab) | 0–1 | **0 = unlocked: EEPROM writes persist; 1 = locked: EEPROM writes do not persist** |
| 56–57 (0x38) | **Present position** | 2 | RO | — | steps, bit15 sign |
| 58–59 (0x3A) | **Present speed** | 2 | RO | — | step/s, bit15 sign |
| 60–61 (0x3C) | **Present load** | 2 | RO | — | 0.1 % **PWM duty cycle** driving the motor, bit10 sign |
| 62 (0x3E) | **Present voltage** | 1 | RO | — | 0.1 V |
| 63 (0x3F) | **Present temperature** | 1 | RO | — | °C |
| 64 (0x40) | Async-write flag | 1 | RO | — | set when a REG WRITE is pending |
| 65 (0x41) | Servo status | 1 | RO | bitmask | bit0 voltage, bit1 sensor, bit2 temperature, bit3 current, bit4 angle, bit5 overload |
| 66 (0x42) | Moving flag | 1 | RO | — | 1 = moving |
| 69–70 (0x45) | **Present current** | 2 | RO | — | ×6.5 mA (max 3.25 A) |
| 80–86 | Factory block (rustypot names): 80 moving_velocity_threshold, 81 dts, 82 velocity_unit_factor, 83 hts, **84 maximum_velocity_limit**, **85 maximum_acceleration**, 86 acceleration_multiplier | 1 each | — | — | pypot maps `set_maximum_acceleration` → addr 85 ("not in memory table") [PYPOT]; rustypot: "hts is only meaningful from firmware 2.54" [RUSTYPOT-STS] |

Notes:
- Goal time at 44 is **not** a Dynamixel-style move duration on STS; Feetech's own `WritePosEx(id, pos, speed, acc)` writes 7 bytes starting at 41: `[acc, pos_L, pos_H, 0, 0, speed_L, speed_H]` (time bytes = 0) [FT-PY `sms_sts.py`].
- The protocol manual's WRITE example writes 6 bytes at 0x2A: position 2048, time 0, speed 1000 [PROTO p.6].
- Angle limits in XLS are plain unsigned steps; positions/speeds/offset are sign-magnitude ("Positions, speeds and the offset are sign-magnitude; the limits are plain steps." [RUSTYPOT-STS]).

### 2.3 Lock register procedure for EEPROM writes

- Protocol manual: "the memory table EPROM has a protection lock switch, which needs to be disabled (set to 0) before modifying the ID. Otherwise, the example ID will not be saved when power is off." [PROTO p.6]
- XLS: write 0 → "Disables the write lock, allowing values written to the EPROM address to be saved even after power loss"; write 1 → not saved [XLS].
- Feetech SDK: `unLockEprom(id)` = write 0 to addr 55; `LockEprom(id)` = write 1 [FT-PY][FT-LINUX].
- Sequence: write 0 @55 → write EEPROM registers (ID, baud, PID, limits, offset, mode, max torque…) → write 1 @55 (optional but what Open Duck's `configure_all_motors.py` does). Writing EEPROM wears flash; do it only in configuration scripts. The XLS says the power-on default of the lock flag is 0, AIFitLab says 1 — Open Duck scripts always write 0 first, which is the safe assumption.
- Middle-position calibration alternatives: write 128 to addr 40 (torque-enable register) → current position becomes 2048 [XLS]; SDK instruction `INST_OFSCAL = 0x0B` / `CalibrationOfs()` does the same [FT-PY `scservo_def.py`][FT-LINUX]; or write a signed step offset to addr 31.

---

## 3. Protocol

Primary source: Waveshare/Feetech "Communication Protocol User Manual" [PROTO] (https://files.waveshare.com/upload/2/27/Communication_Protocol_User_Manual-EN%28191218-0923%29.pdf), plus FTServo_Python `protocol_packet_handler.py` / `scservo_def.py` [FT-PY] (https://github.com/ftservo/FTServo_Python).

### 3.1 Physical layer
- Half-duplex asynchronous serial, **one signal wire** (TX and RX multiplexed), 3-pin 5264/2.54 mm connector: 1 GND, 2 VCC, 3 Signal [DS p.4][PROTO p.2]. 8 data bits, 1 stop, no parity, 10 bits/byte [PROTO p.2][DS p.4]. Signal high 2–5 V, low 0–0.45 V [DS p.8].
- Reference host circuit (datasheet p.8): SN74LVC1G126 (TX buffer, enabled by TXEN) + SN74LVC1G125 (RX buffer, disabled by TXEN) with a PNP transistor generating TXEN from TXD — i.e. the host must drive the line only while transmitting and tri-state it otherwise [DS p.8]. The Waveshare adapter boards do this for you.
- Baud: 38 400 – 1 000 000, **default 1 Mbps** [DS p.4][XLS].

### 3.2 Packet format
Instruction packet: `0xFF 0xFF | ID | LENGTH | INSTRUCTION | PARAM1..N | CHECKSUM`, LENGTH = N + 2, CHECKSUM = ~(ID + LENGTH + INSTRUCTION + ΣPARAM) & 0xFF [PROTO p.2-3].
Status packet: `0xFF 0xFF | ID | LENGTH | ERROR | PARAM1..N | CHECKSUM` [PROTO p.3]. ERROR bits (SDK names): 1 voltage, 2 angle/sensor, 4 overheat, 8 over-current ("OverEle"), 32 overload [FT-PY]. (The register-65 status byte uses the ordering bit0 voltage, bit1 sensor, bit2 temperature, bit3 current, bit4 angle, bit5 overload [XLS].)

### 3.3 Instructions

| Instruction | Code | Params | Notes |
|---|---|---|---|
| PING | 0x01 | 0 | returns status; broadcast ping must not be used with multiple servos |
| READ DATA | 0x02 | 2 (addr, len) | e.g. `FF FF 01 04 02 38 02 BE` reads 2 bytes @0x38 → reply `FF FF 01 04 00 18 05 DD` = 0x0518 = 1304 [PROTO p.5] |
| WRITE DATA | 0x03 | ≥1 (addr, data…) | e.g. set ID via broadcast `FF FF FE 04 03 05 01 F4` |
| REG WRITE | 0x04 | ≥2 | buffered until ACTION; sets async-write flag (addr 64) |
| ACTION | 0x05 | 0 | usually broadcast `FF FF FE 02 05 FA` |
| RESET | 0x06 (Waveshare manual) / 0x0A `INST_RESET` (Feetech SDK) | 0 | "reset the control table to factory value"; the two sources disagree on the code [PROTO p.4][FT-PY] |
| OFS CAL | 0x0B `INST_OFSCAL` (SDK only) | — | midpoint calibration [FT-PY] |
| SYNC READ | **0x82** | ≥3 (addr, len, ID1…IDn) | LENGTH = n + 4; servos reply one after another **in the ID order listed**; all must use the same addr/len [PROTO p.10-11] |
| SYNC WRITE | **0x83** | ≥2 | LENGTH = (L+1)·n + 4; params: addr, L, then (ID, L bytes) per servo; broadcast, no reply [PROTO p.9-10] |
| REBOOT | — | — | **No reboot instruction exists in the Feetech protocol** (Dynamixel's 0x08 is not listed in either source). Power-cycle instead. |

Example sync read of 8 bytes @0x38 from IDs 1,2: `FF FF FE 06 82 38 08 01 02 36`; replies `FF FF 01 0A 00 ...` then `FF FF 02 0A 00 ...` [PROTO p.11].

### 3.4 Timing for 14 servos at 1 Mbps (computed; 10 µs/byte)

| Transaction | Bytes on the wire | Time |
|---|---|---|
| SYNC READ request (8 + n) | 22 B | 0.22 ms |
| 14 replies, position only (2 B each → 8 B/reply) | 112 B | 1.12 ms |
| 14 replies, position + speed (4 B → 10 B) | 140 B | 1.40 ms |
| 14 replies, 56–63 pos/speed/load/volt/temp (8 B → 14 B) | 196 B | 1.96 ms |
| 14 replies, 56–70 incl. current (15 B → 21 B) | 294 B | 2.94 ms |
| SYNC WRITE goal position only (2 B/servo) | 36 B | 0.36 ms |
| SYNC WRITE Feetech `SyncWritePosEx` (7 B/servo: acc,pos,time,speed) | 106 B | 1.06 ms |

So one sync read of 14 positions ≈ **1.3 ms + 14 × (return delay + firmware turnaround)**, position+velocity in one 4-byte sync read ≈ 1.6 ms, and a full read+write cycle ≈ 2–3 ms of bus time — comfortably inside a 20 ms (50 Hz) period. Add to that:
- **Return delay (addr 7)**: ×2 µs, default 0; if someone set it to 254 it would add 0.5 ms per servo (7 ms per 14-servo sync read). Leave at 0 [XLS].
- **Response status level (addr 8)**: default 1 means every non-broadcast WRITE produces a 6-byte status packet you must read or flush. Sync writes are broadcast and produce no reply anyway [XLS][PROTO p.3].
- **USB-serial latency**: FTDI's latency timer defaults to 16 ms; Open Duck's README sets it to 1 ms with a udev rule (`SUBSYSTEM=="usb-serial", DRIVER=="ftdi_sio", ATTR{latency_timer}="1"`) [RUNTIME-README]. rustypot's benchmark comment: "USB turnaround (the FTDI latency timer, 16 ms unless lowered)" [RUSTYPOT-BENCH]. Full-speed USB bulk polling is 1 ms, so expect ≥1–2 ms per host round trip regardless of chip. The Feetech Python SDK uses a 50 ms packet timeout (`LATENCY_TIMER = 50`) [FT-PY `port_handler.py`].
- **Python overhead**: rustypot releases the GIL per transaction; lowering `sys.setswitchinterval` to 1 ms took a 6-motor chain from 126 Hz to 340 Hz under thread contention [RUSTYPOT-README].
- **Firmware**: max position update rate 1 ms [DS p.8]; the firmware rate-limits its internal target toward the goal at the goal-speed/max-velocity (3400 step/s ≈ 5.2 rad/s when goal speed = 0) and ramps with the acceleration register (0 = max) — BAM models this explicitly [BAM-FT-ACT].

Open Duck runtime currently does **two separate** list reads per 50 Hz tick (`read_present_position(ids)` then `read_present_velocity(ids)`) then one `write_goal_position(ids, values)` [RUNTIME-HWI]. Merging the reads into one 4-byte sync read at address 56 would save ~1.5 ms/tick **[inference]**.

### 3.5 Gotchas
- Single-wire half duplex: the host's own transmitted bytes may echo back on some adapters; SDKs search for the `FF FF ID` header to resync [FT-PY `rxPacket`].
- Never ping broadcast with several servos (collisions) [PROTO p.3].
- Duplicate IDs make pings fail entirely; configure one servo at a time [WS-MANUAL p.15].
- Sign-magnitude, not two's complement, for positions/speeds/offset; load uses bit10 for sign.
- Waveshare's ESP32 driver board firmware forwards the FD tool at 115 200 on UART0 ("Start Serial Forwarding") — the servo bus itself stays at 1 Mbps [WS-MANUAL p.17].
- Scanning IDs by pinging 0–253 is slow (Open Duck `configure_motor.py` does a 255-ID scan only if ID 1 is missing).

---

## 4. Configuration tools and hardware

### 4.1 Hardware
- **Open Duck BOM**: "Servo control board" = Waveshare **Bus Servo Adapter (A)** (https://www.waveshare.com/bus-servo-adapter-a.htm), 14 × "Feetech 7.4v STS 3215 … Be sure to buy the 7.4v ones, also called 19kg.cm", 2 × 18650 (Molicel P30B) with a 2S BMS, 5 V UBEC [BOM]. The adapter "integrates servo power supply and servo control circuit", input **9–12.6 V** via DC5521 jack or screw terminal, jumper A = UART (RX-RX, TX-TX to a Pi/MCU), jumper B = USB; the wiki does not name the USB chip [WS-ADAPTER][WS-ADAPTER-WIKI]. The runtime opens `/dev/ttyACM0` (USB CDC-ACM) [RUNTIME-HWI]; the README's FTDI udev rule would only matter with an FTDI dongle **[inference]**.
- Alternatives: Waveshare "Servo Driver with ESP32" (web UI at 192.168.4.1: Start Searching, Set New ID, **Set Middle Position** (ST series only), Set Servo/Motor Mode, Torque/Release, serial forwarding for the FD tool) [WS-MANUAL p.14-17]; Feetech FE-URT-1 USB-TTL board [SEEED-WIKI]; any USB-TTL + the datasheet's 74LVC1G126/125 direction circuit.
- Note the 9 V minimum of the Bus Servo Adapter (A): fine for 3S (9.0–12.6 V), marginal for 2S.

### 4.2 Software
- **Feetech FD** (Windows only): download from https://www.feetechrc.com/software.html ("FD" debugging software); open COM port at 1 000 000, "Search" to list motors, per-motor tabs for parameters and firmware "Upgrade" [LEROBOT-FW]. Seeed links FDServo to https://gitee.com/ftservo/fddebug [SEEED-WIKI].
- **Linux/macOS**: FT_SCServo_Debug_Qt (https://github.com/CarolinePascal/FT_SCServo_Debug_Qt, fork of Kotakku's tool; .deb for amd64/arm64, Qt5, needs the CH340 driver; no firmware upgrade) [LEROBOT-FW][FT-QT].
- **Feetech SDKs**: FTServo_Python (`scservo_sdk`, `sms_sts.py`) https://github.com/ftservo/FTServo_Python ; FTServo_Linux (`SMS_STS.h`) https://github.com/ftservo/FTServo_Linux ; Waveshare SCServo Arduino lib https://files.waveshare.com/upload/b/b7/scservo.zip.zip [WS-WIKI].
- **Open Duck Mini Runtime (v2)** scripts [RUNTIME]:
  - `scripts/configure_motor.py --id N [--port /dev/ttyACM0]`: finds the motor at default ID 1 (else scans 0–254), then `set_lock 0`, `set_mode 0`, `set_maximum_acceleration 0` (addr 85), `set_acceleration 0` (addr 41), `P=32, I=0, D=0` (addrs 21/23/22), `change_id`, then `set_goal_position 0`. Uses `pypot.feetech.FeetechSTS3215IO` from the `support-feetech-sts3215` branch of pollen-robotics/pypot (`setup.cfg`).
  - `scripts/configure_all_motors.py`: same settings for every ID, then `set_lock 1`, and interactively drives each to 0. **ID map**: left_hip_yaw 20, left_hip_roll 21, left_hip_pitch 22, left_knee 23, left_ankle 24, neck_pitch 30, head_pitch 31, head_yaw 32, head_roll 33, right_hip_yaw 10, right_hip_roll 11, right_hip_pitch 12, right_knee 13, right_ankle 14.
  - `scripts/find_soft_offsets.py`: software zero offsets, saved by hand into `~/duck_config.json` → `joints_offsets` (radians) and applied in `rustypot_position_hwi.py` (`pos + joints_offsets`). README: "This procedure won't be necessary in the future as we will be flashing the offsets directly in each motor's eeprom" (i.e. addr 31 or torque-enable=128) [RUNTIME-README].
  - `scripts/check_motors.py`, `check_voltage.py`, `turn_on.py`, `turn_off.py`.
  - Runtime control: `rustypot==0.1.0` (`rustypot.feetech(port, 1000000)`; `set_kps`, `set_kds`, `write_goal_position(ids, rad)`, `read_present_position(ids)`, `read_present_velocity(ids)`, `enable/disable_torque`) [RUNTIME-HWI]. Walk script: `control_freq = 50`, `pid = [30, 0, 0]` → kp 30 on legs, 8 on the four head joints, kd 0, `action_scale = 0.25`, `max_motor_velocity = 5.24` (clip commented out on the robot) [RUNTIME-WALK]. `turn_on()` first sets kp = 2 on all joints, moves to `init_pos`, then restores kp.
- pypot `FeetechSTS3215IO` register table matches §2 exactly (addresses 3…69 plus 77 vfk, 80 vmin, 83 vk, 84 maximum velocity, 85 maximum acceleration) and uses SYNC_READ (130) when more than one ID is requested [PYPOT].

---

## 5. Rhoban BAM actuator identification

Sources: BAM repo https://github.com/Rhoban/bam (docs in `docs/identification/*.rst`, code in `bam/`), ICRA 2025 paper "Extended Friction Models for the Physics Simulation of Servo Actuators" (arXiv 2410.08650) [BAM].

### 5.1 Procedure (what `bam/feetech/` actually does)
- **Test bench**: a pendulum arm bolted to the servo horn with a known mass at a known length; rigid mounting; must swing ±90° from vertical; record mass, arm mass, length [BAM-SETUP]. The XL-330 example uses 0.567 kg at 0.17 m on a 0.016 kg 3D-printed arm, and a full dataset of 240 six-second recordings over several mass/length combinations [BAM-ACQ]. **The specific masses/lengths used for the STS3215 dataset are not recorded in the repo (open question).**
- **Recording** (`bam/feetech/record.py`): opens `pypot.feetech.FeetechSTS3215IO("/dev/ttyACM0")`, mode 0, writes `P = kp`, `D = 0`, plays the trajectory for `trajectory.duration` (6 s), logging present position, present speed (deg→rad), present voltage (×0.1 V); load/temperature are not logged ("TMP"); then ramps back to 0 at 1 rad/s and disables torque. One JSON per run [BAM-FT-REC].
- **Sweep** (`bam/feetech/all_record.py`): `kps = [4, 8, 16, 32]` × `trajectories = ["brutal", "sin_sin", "lift_and_drop", "up_and_down", "sin_time_square"]` (note "brutal" is not in the current `bam/trajectory.py` registry, which has lift_and_drop, sin_time_square, up_and_down, sin_sin, half_sine, steps, nothing — so that entry would raise today). 20 runs × 6 s ≈ 2–3 min per mass/length configuration including return-to-zero [BAM-FT-ALL][BAM-TRAJ]. Trajectories: `sin_time_square` = sin(t²); `lift_and_drop` = cubic to −π/2 in 2 s then torque off (free fall separates viscous friction from back-EMF damping); `up_and_down` = cubic 0→π/2→0.8·π/2 (static/load friction); `sin_sin` = sin(t)·π/2 + sin(5t)·0.5·sin(2t) [BAM-ACQ].
- **Processing**: `python -m bam.process --dt 0.005` resamples to 5 ms [BAM-ACQ].
- **Fitting**: `python -m bam.fit --actuator sts3215 --model m6 --logdir data_processed --validation_kp 8` → CMA-ES (BIPOP) with 100 000 trials by default, minimising MAE of simulated vs measured position; hold out one kp as validation; fit m1…m6 and keep the best validation MAE [BAM-FIT]. Wall-clock is hours of CPU for m5/m6 (not stated precisely; the docs say "increase trials for complex models").
- **Actuator model** (`bam/feetech/actuator.py`, class `STS3215Actuator(VoltageControlledActuator)`): `vin = 7.4`, `kp = 32` (firmware units), `error_gain = 0.166` ("if multiplied by a position error and firmware KP, gives duty cycle… determined using an oscilloscope"), `max_pwm = 0.97`, `default_max_velocity = 3400·2π/4096 = 5.2155 rad/s`; the firmware's internal target is rate-limited to `max_velocity` (stateful `q_target_smooth`), duty = (q_smooth − q)·kp·error_gain·error_gain_ratio clamped to ±max_pwm, V = vin·duty; torque τ = kt·V/R − kt²·q̇/R; identified motor parameters: `kt` (init 0.7845 N·m/A = 8 kg·cm/A, range 0.05–2.5), `error_gain_ratio` (1.0, 0.1–10), `R` (2.0 Ω, 0.1–10), `armature` (1e-4, 1e-5–0.04 kg·m²), `q_offset`, `max_velocity` (0.1×–10× default), plus `command_delay` and the friction terms of the chosen model [BAM-FT-ACT][BAM-ACT].

### 5.2 Where the parameters live and what m6 contains
`bam/bam/params/feetech_sts3215_7_4V/m1.json … m6.json` (`"actuator": "sts3215"`). Models: m1 Coulomb, m2 Stribeck, m3 load-dependent, m4 Stribeck+load, m5 + directional, m6 + quadratic [BAM-MODEL].

m1 (Coulomb+viscous):
```
kt 1.1776  error_gain_ratio 1.0049  R 2.4787  armature 0.02608  q_offset -0.0506
max_velocity 5.2883  command_delay 0.00105  friction_base 0.0515  friction_viscous 0.0599
```
m6 (Stribeck, load-dependent, directional, quadratic):
```
kt 1.27532  error_gain_ratio 1.16170  R 2.75342  armature 0.021564  q_offset -0.06827
max_velocity 5.09575  command_delay 0.004981
friction_base 0.053313  friction_stribeck 4.26e-05  friction_viscous 0.028161
load_friction_motor 0.044912  load_friction_external 0.243555
load_friction_motor_stribeck 1.24e-04  load_friction_external_stribeck 0.142291
load_friction_motor_quad 0.007595  load_friction_external_quad 0.003404
dtheta_stribeck 0.37114  alpha 9.9309
```
(m2–m5 are in the same folder; kt 1.17–1.27 N·m/A, R 2.45–2.75 Ω, armature 0.0216–0.026, max_velocity 5.07–5.30 rad/s in all of them.) The fitted kt is ~1.5× the datasheet 0.785 N·m/A because kt and R are only identified through V/R and kt²/R with vin fixed — treat them as a pair, not as physical constants **[inference]**.

### 5.3 12 V parameters?
**None.** `bam/bam/params/` contains xl320, xl330, mx64, mx106, erob80_50, erob80_100, feetech_sts3215_7_4V and waveshare_st3025 only. The only 12 V Feetech-protocol servo BAM has is the **Waveshare ST3025** (a different, larger 12 V servo: `vin = 12`, `kp = 32`, `error_gain = 0.166` "inherited from STS3215", kt init 9 kgf·cm/A, R init 12 V/4.4 A, `max_pwm = 1.0` "not measured") — useful as a template for a 12 V STS3215 class, not as a parameter set [BAM-WS-ACT].

### 5.4 Do Open Duck Playground actuator settings come from BAM? Where?
Yes, via `bam.to_mujoco` (deprecated "approximation": kp = error_gain·kp_fw·vin·max_pwm·kt/R, forcerange = vin·kt/R, damping = friction_viscous + kt²/R, frictionloss = friction_base, armature = armature; only exact for m1) [BAM-TOMJ]. Open Duck's sim2real doc says "We used Rhoban's BAM … `bam.to_mujoco` exports the main parameters to MuJoCo units" and lists damping, kp, frictionloss, armature, forcerange [OD-S2R]. Recomputing from `m1.json` with vin 7.4, kp 32, error_gain 0.166, max_pwm 0.97 gives kp 18.1, forcerange 3.52 N·m, damping 0.619, frictionloss 0.0515 — i.e. the numbers below are an earlier m1 fit.

Files and values in `Open_Duck_Playground/playground/open_duck_mini_v2/` [OD-PG]:
- `xmls/joints_properties.xml` (fed to onshape-to-robot via `xmls/config.json` → `additional_xml`, `joint_properties.default.class = "sts3215"`):
  `<joint damping="0.60" frictionloss="0.052" armature="0.028"/>`, `<position kp="17.8" kv="0.0" forcerange="-3.35 3.35"/>`; class `backlash`: damping 0.01, frictionloss 0, armature 0.01, range ±0.008727 rad (±0.5°).
- `xmls/open_duck_mini_v2.xml` (**the file actually loaded** by `scene_flat_terrain.xml`): class `sts3215` = `damping="0.56" frictionloss="0.068" armature="0.027"`, `<position kp="13.37" kv="0.0" forcerange="-3.23 3.23"/>` (a `kp="17.12"` line is commented out). The generator's top-level default `<joint frictionloss="0.1" armature="0.005"/><position kp="50" dampratio="1"/>` is overridden by the class on every joint.
- `xmls/open_duck_mini_v2_backlash.xml` (loaded by `scene_flat_terrain_backlash.xml` / `scene_rough_terrain_backlash.xml`): same joint values, `kp="17.11"`, forcerange ±3.23; the older 0.60/0.052/0.028/17.8/3.35 set is commented out.
  → **kp differs between the no-backlash (13.37) and backlash (17.11) models; which one the released policy was trained with is an open question.**
- `joystick.py` `default_config()`: `ctrl_dt=0.02`, `sim_dt=0.002`, `action_scale=0.25`, `dof_vel_scale=0.05`, **`max_motor_velocity=5.24` rad/s** with `USE_MOTOR_SPEED_LIMITS = True` → motor targets are clipped to ±max_motor_velocity·dt per step (mirrors the firmware rate limiter BAM found, 3400 step/s = 5.2155 rad/s; BAM fits 5.07–5.29); action delay 0–3 steps; joint-position noise hip 0.03 / knee 0.05 / ankle 0.08 rad, joint-vel noise 2.5 rad/s; `torques` cost −1e-3 on `data.actuator_force`.
- `common/randomize.py`: kp × U(0.9, 1.1) (`actuator_gainprm[:,0]`, `biasprm[:,1]`), frictionloss × U(0.9, 1.1), armature × U(1.0, 1.05), floor friction U(0.5, 1.0), masses × U(0.9, 1.1), torso mass ± 0.1 kg, qpos0 jitter ± 0.03 rad.
- There is **no kd** anywhere (`kv="0.0"` in sim, `kds = 0` on the robot); "max torque" is only the MuJoCo `forcerange` (±3.23 N·m) which is the DC-model electrical stall vin·kt/R, not the mechanical 1.91 N·m datasheet stall (friction eats the difference) **[inference]**.
- On the robot the firmware kp is **30** (walk script) vs **32** in BAM/configure scripts.

---

## 6. Running the 12 V / 30 kg·cm unit with the 7.4 V actuator model

### 6.1 Expected torque / velocity ratios (12 V unit vs 7.4 V unit)
Evidence (datasheets, §1): stall torque 30 / 19.5 = **1.54×** (1.62× at 12.6 V); no-load speed 45 / 52 = **0.87×** (0.91× at 12.6 V); continuous torque 10 / 5 = 2×; stall current 2.7 vs 2.5 A.

Through the BAM DC model **[inference]**: using datasheet kt and R ≈ V/I_stall, forcerange_12V = 12 × 1.079 / 4.44 ≈ 2.9 N·m vs 7.4 × 0.765 / 2.96 ≈ 1.9 N·m (ratio 1.53, consistent with the spec ratio); electrical damping kt²/R = 0.262 vs 0.198 N·m·s/rad (BAM's fitted pair gives 0.56 for the 7.4 V unit, so expect a proportionally higher value for 12 V); MuJoCo-equivalent kp scales with vin·kt/R → ≈ 1.53× stiffer for the same firmware P = 32.

Velocity ceiling **[inference]**: the firmware's goal rate limit (3400 step/s ≈ 5.2 rad/s, `max_motor_velocity = 5.24` in the Playground) is a firmware constant, but the 12 V motor's no-load speed is only 4.7 rad/s at 12 V (4.95 at 12.6 V), below that limit, while the 7.4 V motor's 5.45 rad/s is above it. So with the 12 V unit the policy's 5.24 rad/s target-rate assumption is no longer backed by the hardware; lower `max_motor_velocity` to ≈ 4.7 (or re-identify `max_velocity`) when retraining.

### 6.2 Is "torque limit ≈ 65 %" a reasonable way to approximate the 19 kg·cm unit?
What the registers do (evidence): addr 16 "Maximum torque … 1000 corresponds to 100 % of the locked-rotor torque", copied to addr 48 "Torque limit" at power-up, "which can be modified by the user to control the output of the maximum torque"; addr 60 "Present load" is "the voltage duty cycle of the current control output driving motor" in 0.1 % [XLS]. The over-current path is separate (addr 28 protection current, 6.5 mA units).
**[inference]** Because the firmware's output is a PWM duty and "load" is reported as duty, the torque limit almost certainly clamps the duty cycle (effective motor voltage), not the current. If so, torque limit 650 on a 12 V bus = max 7.8 V (8.2 V at 12.6 V) on the 12 V winding → stall torque ≈ kt·V/R = 1.079 × 7.8 / 4.44 ≈ 1.9 N·m ≈ 19.4 kg·cm: the **stall torque matches** the 7.4 V unit (0.65 × 30 = 19.5 kg·cm). But speed scales with voltage too: no-load speed ≈ 45 × 7.8/12 ≈ 29 rpm ≈ 3.1 rad/s, i.e. **~0.56× the 7.4 V unit's 52 rpm** and well below the 5.2 rad/s rate limit the policy assumes. Also the P loop (duty = 0.166·kp·Δq) saturates at 65 % duty, so the proportional region is narrower.
Conclusion: a 65 % torque limit reproduces one number (stall torque) and breaks another (speed, by ~45 %). At 100 % you get 1.54× torque and 0.87× speed. No single scalar makes the 12 V winding behave like the 7.4 V one, because torque and speed both scale with voltage in a voltage-controlled servo. This is reasoning from the datasheets and the register definitions, not something any source tested.

### 6.3 What I would actually do **[inference]**
1. Keep the torque limit at 1000 (or ≥ 800 to retain a safety margin against the 2.7 A stall), keep the firmware P around 32 → 21 if you want the 7.4 V closed-loop stiffness (32 / 1.53), and verify the max-voltage register (addr 14) and protection current (addr 28) on the 12 V units with the FD tool.
2. Re-identify with BAM at 12 V: subclass `STS3215Actuator` like `ST3025Actuator` does (`vin = 12.0`, `kp = 32`, `error_gain = 0.166` inherited, `max_pwm` 0.97 unless re-measured; kt init 1.079 N·m/A, R init 4.44 Ω, armature init 0.02), record `all_record` at `--vin 12` (and 12.6 / 11.1 to span the 3S range), fit m1 for the MuJoCo export and m6 for `MujocoController`, then regenerate `joints_properties.xml` (kp, forcerange, damping, frictionloss, armature) and set `max_motor_velocity` from the fitted `max_velocity`. Expect kp ≈ 1.5× (≈ 20–26), forcerange ≈ 1.5× (≈ 4.9 N·m), lower max_velocity (≈ 4.7–5.0 rad/s), higher damping.
3. Battery sag matters more at 3S: BAM's `duty_cycle` is kept "for the battery drop model"; a 3S pack at 9.3 V would still give ≈ 1.2× the 7.4 V torque but only ≈ 0.67× the 12 V no-load speed.

---

## 7. Open questions
1. EEPROM defaults of the 12 V units (max-voltage register 14, phase, max torque) — read with FD before running at 12.6 V.
2. Whether the torque-limit register clamps duty (voltage) or current; verify with present-load (addr 60) vs present-current (addr 69) under stall.
3. Masses/arm lengths and vin used for BAM's `feetech_sts3215_7_4V` dataset (not in the repo).
4. Whether rustypot 0.1.0's `read_present_position(ids)` is a 0x82 sync read (current rustypot has `sync_read_*`; the 0.1.0 Python source is not tagged on GitHub).
5. Which kp (13.37 vs 17.11/17.8) the released `BEST_WALK_ONNX_2.onnx` was trained with.
6. USB-serial chip on the Bus Servo Adapter (A) (it enumerates as `/dev/ttyACM0`, so CDC-ACM, not FTDI).
7. ST3215-HS gear ratio; no BAM parameters exist for it either.

---

## Source index
- [DS] Feetech STS3215 product specification (translated): https://core-electronics.com.au/attachments/uploads/sts3215-smart-servo-datasheet-translated.pdf
- [C047] Seeed ST3215-C047 datasheet: https://store.comet.bg/download-file.php?id=31780 ; product: https://www.seeedstudio.com/STS3215-30KG-Serial-Servo-p-6340.html
- [SEEED-WIKI] https://wiki.seeedstudio.com/feetech_servo/
- [WS-PROD] https://www.waveshare.com/st3215-servo.htm
- [WS-WIKI] https://www.waveshare.com/wiki/ST3215_Servo
- [WS-HS] https://www.waveshare.com/product/modules/st3215-hs-servo-motor.htm
- [WS-ADAPTER] https://www.waveshare.com/bus-servo-adapter-a.htm ; [WS-ADAPTER-WIKI] https://www.waveshare.com/wiki/Bus_Servo_Adapter_(A)
- [WS-MANUAL] https://files.waveshare.com/upload/f/f4/ST3215_Servo_User_Manual.pdf
- [XLS] https://files.waveshare.com/upload/2/27/ST3215%20memory%20register%20map-EN.xls
- [PROTO] https://files.waveshare.com/upload/2/27/Communication_Protocol_User_Manual-EN%28191218-0923%29.pdf
- [EVELTA] https://evelta.com/sts3215-c018-12v-30kg-cm-dual-shaft-ttl-serial-servo-metal-gears-magnetic-encoder/
- [AIFIT] https://aifitlab-wiki.super.site/feetech-servo-motor-docs/feetech-sts-servo-memory-table-analysis
- [FT-PY] https://github.com/ftservo/FTServo_Python (scservo_sdk/sms_sts.py, scservo_def.py, protocol_packet_handler.py, group_sync_read.py, port_handler.py)
- [FT-LINUX] https://github.com/ftservo/FTServo_Linux (src/SMS_STS.h)
- [PYPOT] https://github.com/pollen-robotics/pypot/blob/support-feetech-sts3215/pypot/feetech/sts3215_io.py
- [RUSTYPOT-STS] https://github.com/pollen-robotics/rustypot/blob/develop/src/servo/feetech/sts3215.rs ; [RUSTYPOT-README] https://github.com/pollen-robotics/rustypot ; [RUSTYPOT-BENCH] https://github.com/pollen-robotics/rustypot/blob/develop/examples/fast_sync_read_bench.rs
- [ZENN] https://zenn.dev/usagi1975/articles/2026-05-18-000_sts3215-python (factory Return_Delay_Time = 0 observed)
- [LEROBOT-FW] https://huggingface.co/docs/lerobot/feetech ; [FT-QT] https://github.com/CarolinePascal/FT_SCServo_Debug_Qt ; Feetech software page https://www.feetechrc.com/software.html
- [BAM] https://github.com/Rhoban/bam ; [BAM-SETUP] docs/identification/setup.rst ; [BAM-ACQ] docs/identification/acquisition.rst ; [BAM-FIT] docs/identification/fitting.rst ; [BAM-ACT] bam/actuator.py ; [BAM-FT-ACT] bam/feetech/actuator.py ; [BAM-FT-REC] bam/feetech/record.py ; [BAM-FT-ALL] bam/feetech/all_record.py ; [BAM-TRAJ] bam/trajectory.py ; [BAM-MODEL] bam/model.py ; [BAM-TOMJ] bam/to_mujoco.py ; [BAM-WS-ACT] bam/waveshare/actuator.py ; params: bam/params/feetech_sts3215_7_4V/m1..m6.json
- [OD-PG] https://github.com/apirrone/Open_Duck_Playground (playground/open_duck_mini_v2/xmls/joints_properties.xml, open_duck_mini_v2.xml, open_duck_mini_v2_backlash.xml, config.json, joystick.py; playground/common/randomize.py)
- [RUNTIME] https://github.com/apirrone/Open_Duck_Mini_Runtime/tree/v2 ; [RUNTIME-HWI] mini_bdx_runtime/mini_bdx_runtime/rustypot_position_hwi.py ; [RUNTIME-WALK] scripts/v2_rl_walk_mujoco.py ; [RUNTIME-README] README.md ; scripts/configure_motor.py, configure_all_motors.py, find_soft_offsets.py ; setup.cfg (rustypot==0.1.0, pypot@support-feetech-sts3215)
- [OD-S2R] https://github.com/apirrone/Open_Duck_Mini/blob/v2/docs/sim2real.md ; [BOM] https://docs.google.com/spreadsheets/d/1gq4iWWHEJVgAA_eemkTEsshXqrYlFxXAPwO515KpCJc
