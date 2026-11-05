# Open Duck Mini v2 on 3S Li-ion with ST3215 12 V servos: power-system research

Date: 2026-10-28. Scope: 14x Feetech/Waveshare ST3215 (12 V, 30 kg.cm) + 2x SG90 on a 3S1P pack of Samsung INR18650-30Q, Waveshare Bus Servo Adapter (A), 7Semi AP64500 5 V/5 A buck feeding a Radxa Zero 3W + IMX219 + VL53L8CX + BNO085. Parts already picked: Robocraze 3S 40 A balance BMS, iMax B6AC, XT30, 18 AWG silicone wire, LiPo alarm. Stock design: 2S 18650 + UBEC + Pi Zero 2W.

Everything marked **[est.]** is my calculation, not a measurement. Everything marked **[no source found]** was searched for and not found.

---

## 1. Waveshare Bus Servo Adapter (A)

**It is the same board as the "Serial Bus Servo Driver Board".** The product page title at https://www.waveshare.com/bus-servo-adapter-a.htm reads "Serial Bus Servo Driver Board, Integrates Servo Power Supply And Control Circuit, Applicable for ST/SC Series Serial Bus Servos | Bus Servo Adapter (A)" (Waveshare SKU 25514, $4.99, 16 g). The wiki URL `Serial_Bus_Servo_Driver_Board` returns 404; the live wiki is https://www.waveshare.com/wiki/Bus_Servo_Adapter_(A).

Published specs (wiki, same URL):
- "Input voltage: 9~12.6V (should match servo voltage)" — so **yes, 12.6 V (full 3S) is in spec and passes straight to the servos** (the board "integrates the servo power supply", i.e. the servo rail is the input rail, see schematic below).
- "Power supply interface: 5.5*2.1mm DC"; the usage section adds "you can input it via the DC5521 power header and green power screw terminal" (both are present and wired in parallel).
- Communication: UART header (jumper on **A**) or USB-C (jumper on **B**). "the connection must be RX-RX, TX-TX" for the UART header.
- "Simultaneous control of up to 253 ST/SC series serial bus servos (require sufficient power)". **No maximum current is published anywhere.**
- 42 x 33 mm, 2.5 mm mounting holes (37 x 28 mm pattern per product page).

What the schematic shows (https://files.waveshare.com/wiki/Bus-Servo-Adapter-(A)/Bus%20Servo%20Adapter%20(A)-Sch.pdf, text-extracted locally):
- DC005 5.5x2.1 jack and KF350-2P screw terminal on the same net `DC_IN0`.
- **SMAJ15CA** bidirectional TVS across the input (15 V standoff, clamps at ~24 V) — surge/transient protection only.
- **AO4407 P-channel MOSFET (M1)** with a BZT52C6V8S zener and 2 k gate resistor in the classic high-side **reverse-polarity protection** arrangement. The AO4407 is rated -30 V, **-12 A continuous**, RDS(on) < 14 mOhm at VGS = -10 V (AOS datasheet: https://www.aosmd.com/pdfs/datasheet/AO4407.pdf). This single SO-8 FET is the whole servo-rail pass element: at 12 A it dissipates ~2 W on a small 2-layer board, so **treat ~10-12 A as the board's practical continuous limit** [est.].
- A small buck (4.7 uH SWPA6020S4R7MT inductor, 0.8 V FB) makes 5 V, then an **AMS1117-3.3** makes 3.3 V for the **CH343P** USB-UART. The UART header runs at **3.3 V logic (net `3V3_OP`)**; the ST3215 bus accepts 2-5 V high level (Feetech datasheet, section 7 "Signal high level voltage 2V-5V"), so the Radxa's 3.3 V UART is a direct match.
- **No undervoltage lockout / low-voltage cut-off, no fuse, no current limit** on the servo rail. The servo headers are 5264-type 3-pin; HeyPCB's quack-core project (which copies this exact half-duplex driver: 74LVC1G126 + 74LVC1G125 + MMBT3906) notes they are "rated 3 A per pin (spec 3.4), which a leg chain can exceed while walking, as on the Waveshare adapter the duck uses today" (https://github.com/HeyPCB/quack-core).

Alternatives:
| Board | Input | Interface | Size | Notes |
|---|---|---|---|---|
| Bus Servo Adapter (A) = Serial Bus Servo Driver Board | 9-12.6 V | UART (3.3 V) or USB-C | 42x33 mm | Reverse-polarity FET, TVS; no LVC; ~12 A FET limit. Cheapest, smallest. |
| Servo Driver with ESP32 (https://www.waveshare.com/wiki/Servo_Driver_with_ESP32) | "DC 6-12V (the input voltage and the servo voltage must be matched)"; wiki says 6-12.6 V, 12 V recommended for ST3020 | ESP32 (WiFi/BT/ESP-NOW), USB-C download, UART, OLED | 65x30 mm, 2.75 mm holes 23x58 mm | Auto-scans IDs 0-20 at boot. Adds an MCU you do not need if the Radxa drives the bus; bigger. No protections listed. |
| HeyPCB quack-core (open KiCad, 2S only) | 2S XT30 | Pi Zero 2W carrier | fits duck | 20 A fuse, INA226 current sense, 2x AON6411 soft switch, 2x470 uF bulk; **2S design, servos rated 7.4 V** — a template for what a 3S board should contain, not a drop-in. |

Verdict: keep the Adapter (A). Feed it through the **green screw terminal with 16-18 AWG** (not the barrel jack: 5.5x2.1 jacks are typically rated 2-5 A), and add your own fuse and switch upstream (section 7).

---

## 2. Current draw and runtime

### Datasheet numbers
ST3215 12 V (Waveshare wiki https://www.waveshare.com/wiki/ST3215_Servo): "Input Voltage: 6-12.6V", "No load Current: 200 mA", "Locked-rotor Current: 2.7 A", "up to 30kg.cm@12V", "0.222sec/60° (45RPM) @12V", 1 Mbps half-duplex TTL, 45.22 x 35 x 24.72 mm.

Feetech STS3215 7.4 V datasheet (translated, https://core-electronics.com.au/attachments/uploads/sts3215-smart-servo-datasheet-translated.pdf) gives the shape of the curve, which scales to the 12 V unit: idle (stopped) 6 mA, no-load 150 mA, **rated 650 mA at 5 kg.cm**, stall 2.5 A at 19.5 kg.cm, Kt = 8 kg.cm/A, motor winding 2.5 Ohm, 55 g. Firmware protections: over-current (default trips when running current > 2 A for a set time), over-voltage window (default 4-7.4 V on that variant; 12 V units are configured for 12.6 V), over-temperature at 70 °C.

Per robot (14 servos) [est.]:
- All idle, torque on, holding: 14 x 0.2 A = **2.8 A** (worst case; servos stopped with no load are much less).
- All stalled simultaneously: 14 x 2.7 A = **37.8 A** (unrealistic as a steady state, but a 100-300 ms peak when the robot catches itself is plausible at 20-30 A).

### Community numbers
- **No measured walking current or runtime for Open Duck Mini v2 was found** [no source found]. Searches of GitHub (apirrone/Open_Duck_Mini v2 docs, ToolKnox mirror), orobot, tnkr.ai and openelab turned up nothing numeric. The official assembly guide (https://github.com/apirrone/Open_Duck_Mini/blob/v2/docs/assembly_guide.md) only says "make sure your cells are charged to the same voltage before placing them in the holder".
- The ToolKnox build guide (https://github.com/ToolKnox/hawkridge-open-duck-mini-v2-bipedal-robot) documents the stock power path: "Build the 2S pack: two 18650 cells in the holder, BMS, XT30 lead, power switch and USB-C charger board", "Power the servo bus straight from the pack", "Feed the Raspberry Pi through the 5 V UBEC". It recommends Molicel INR18650-P30B cells.
- The best engineering estimate is HeyPCB quack-core (https://github.com/HeyPCB/quack-core), a replacement power board designed from the duck's URDF and a simulated walking policy: design point "**15 A continuous, 30 A peaks; simulated walking 13.5-14.4 A**" at 2S, "about 5-7 A each" per leg, and "The duck's 8 A / 10 A BMS is the first limit". It also specifies 2x 470 uF bulk on the servo rail.

### 3S translation [est.]
Walking power from the quack-core figure: 13.5-14.4 A x ~7.4 V = **100-107 W**. Same mechanical work at 10.8 V nominal = **9.2-9.9 A** average at the pack. Add Radxa + camera + sensors (~7.5 W / 0.88 eff) = +0.8 A. So:

| Scenario | Pack current (3S) | Runtime 3S1P 3000 mAh | Runtime 3S2P |
|---|---|---|---|
| Standing, torque on | ~2-3 A | 60-90 min | 2-3 h |
| Light walking (0.35 A/servo avg) | ~5.7 A | ~32 min | ~63 min |
| Moderate walking (0.5 A/servo) | ~7.8 A | ~23 min | ~46 min |
| Simulated-policy walking (quack-core, scaled) | ~10-11 A | **~18 min** | ~36 min |
| Peak (catching a fall, several servos near stall) | 20-30 A for <1 s | — | — |

(32.4 Wh pack; runtime = 3 Ah / I x 60, no derating for the 3.3 V/cell alarm cutoff, which removes ~10 %.)

Note the simulated figure is probably pessimistic (the policy runs the motors ~70 % above the catalog torque in sim, per the fport/open-duck-mac sim-to-real notes), so expect **20-30 min of walking on 3S1P**, ~1 h mixed use.

### Is 3S1P adequate? Cell choice
- Samsung 30Q: 3000 mAh, **15 A continuous**, "no problems with 20A pulses" (lygte review https://lygte-info.dk/review/batteries2012/Samsung%20INR18650-30Q%203000mAh%20(Pink)%20UK.html), IR < 18 mOhm (1 kHz) / < 30 mOhm DC, standard charge 1.5 A, rapid 4 A, 2.5 V cutoff (datasheet copy: https://e2e.ti.com/cfs-file/__key/communityserver-discussions-components-files/196/samsung_5F00_30q_5F00_data_5F00_sheet.pdf). A 10 A average is 0.67 C with 20-30 A peaks — **at the edge** of what a 30Q tolerates; three cells in series each see the full current, and three 30 mOhm cells plus BMS plus wiring is ~0.15 Ohm: a 25 A peak drops **~3.5 V** at the pack, which is enough to brown out servos (they read 12.6 -> 9 V) and trip a low-voltage alarm set at the pack.
- Molicel INR18650-P30B: 3000 mAh typ / 2900 min, **30 A continuous** (80 °C cutoff), 3 A standard / 9 A max charge, DC impedance ~17 mOhm, 47 g max (datasheet copy https://fsaeonline.com/content/INR-18650-P30B-80111.pdf). This is also the cell the ToolKnox Open Duck guide recommends. **Same capacity as the 30Q with double the current rating and roughly half the DC resistance — the better cell for 3S1P.**
- Molicel P28A: 2800 mAh, 35 A, 20 mOhm, standard charge 2.8 A, "not that different from the P26A" (lygte: https://lygte-info.dk/review/batteries2012/Molicel%20INR18650-P28A%202800mAh%20(Gray)%20UK.html). P26A: 2600 mAh, 35 A, 20 mOhm, 46 g.
- Recommendation: **3S1P is adequate for 15-30 min walking sessions if you use P30B (first choice) or P28A; with 30Q keep peaks in check (soft-start, bulk capacitance) and accept the sag.** Go 3S2P (6 cells, +140 g, ~2x volume) only if you need > 40 min continuous walking; the duck's battery bay was sized for two cells, so 3S1P is already a squeeze (section 6).

---

## 3. BMS: Robocraze "3 Series 40A 11.1V 12.6V 18650 Lithium Battery Protection Board with Balance"

Spec table from the product page (https://robocraze.com/products/3-series-40a-11-1v-12-6v-18650-lithium-battery-protection-board-with-balance):
- "Overcharge detection voltage (V) 4.25 ± 0.025"
- "Over-discharge detection voltage (V) 2.50 ± 0.08"
- "Over current Protection (A) 40"; "Working current (A) 20"; "continuous discharge of 40A ... Maximum continuous charge current: 20A"
- "balanced current of 100mA" (passive bleed, typically starts at ~4.2 V/cell)
- "Compact size (46 x 60 x 3.4 mm)", 9 g, -40 to +85 °C, "auto recovery function"
- Note on the page: "When using a brush motor, connect a non-polar capacitor (withstand voltage >25V, capacity 10uF-100uF) across the motor's positive and negative terminals". It is marketed for drills ("start current below 80A").

Generic behaviour of this family (same-port 3S boards; manual for the 25 A sibling: https://shillehtek.com/blogs/shillehtek-product-manuals/3s-12v-18650-lithium-battery-protection-board-11-1v-12-6v-balanced-25a-manual; pin description: https://www.tinytronics.nl/en/power/bms-and-chargers/bms/li-ionli-po-protection-circuit-(bms)-3s):
- **Charge and discharge share the same port (P+ / P-).** "Connect the charger to P+/P-, not to the battery pads directly."
- Pads: **B- = cell 1 negative (pack negative); B1 = cell1+ / cell2- junction; B2 = cell2+ / cell3- junction; B+ = cell 3 positive (pack positive); P+ / P- = load and charger.** On most 3S boards B+ and P+ are the same copper; the protection MOSFETs sit in the negative leg between B- and P-.
- **Connection order matters:** "Wire in the order B-, B1, B2, B+ — never connect a higher tap before the ones beneath it ... Connecting B+ first puts the full pack voltage across the protection IC inputs and can destroy it instantly." Check "B- to B1 = 3.7V, B- to B2 = 7.4V, B- to B+ = 11.1V" before connecting the load.
- Recovery: after an over-discharge or over-current trip the output stays off until the load is removed and/or a charger is applied: "Connect a 12.6V charger for a few seconds — that energizes the protection IC and enables the discharge MOSFET."

Is 40 A right for a 5-15 A load? The 40 A over-current trip only protects against gross faults (a hard short through 18 AWG wire will exceed 40 A, so it still trips). The MOSFETs of a 40 A board have lower RDS(on) than a 10-15 A board, which is good for voltage sag. **Yes, keep it — but it does not protect the wiring or the Waveshare board at 15-25 A, so add a 15 A fuse (section 7).** The 2.50 V/cell over-discharge setting is a last-ditch cut-off, not a usable low-battery signal.

Low-voltage alarm threshold: the 30Q/P30B datasheets allow 2.5 V, but under a 10 A load the terminal voltage sags ~0.2-0.3 V/cell below open-circuit, and the Waveshare board + servos need >= 9 V to behave. **Set the alarm to 3.5 V/cell (10.5 V pack) as "land the robot now" and treat 3.3 V/cell (9.9 V) as the hard stop**; that leaves ~10-15 % in the cells and keeps the BMS from ever tripping in use. Plug the alarm's 4-pin JST-XH lead into the same balance connector used for charging (section 4).

---

## 4. Charging

### iMax B6AC via XT30 + JST-XH balance lead
From the manual (https://www.pololu.com/file/0J525/iMAXB6ACmanual.pdf): "Max. charge power 50W", "Charge current range: 0.1~5.0A", "Discharge current range: 0.1~1.0A", "li-ion/Polymer cell count: 1~6 series", balance sockets are "JST-XH ports". "The main battery leads must be connected along with the balance lead connector as shown before charging." Chemistry presets: **"LiIo ... Max. charge voltage: 4.1V/cell"; "LiPo ... Max. charge voltage: 4.2V/cell"; LiFe 3.6 V.** So for 30Q/P30B (4.20 V cells) use the **LiPo program at 3S for full 4.2 V**, or the LiIo program for a gentler 4.1 V/cell (about -10 % capacity, longer cycle life). Charge current: **1.5 A** for 30Q ("Standard charge: 1.5 A CC/CV to 4.20 V, 150 mA cutoff, ~180 min"; rapid 4 A allowed) or **3 A** for P30B (standard). 50 W / 12.6 V = 4 A max from the B6AC anyway.

Balance connector pinout (3S JST-XH 4-pin, standard RC convention, e.g. https://www.progressiverc.com/products/3s-jst-xh-charge-balance-cable): **pin 1 = pack negative (black) -> BMS B-; pin 2 = cell 1 positive -> B1; pin 3 = cell 2 positive -> B2; pin 4 = pack positive (red) -> B+.** The lead goes to the cell taps (B-, B1, B2, B+), never to P-.

Through the BMS or bypass? Two valid options:
1. **Through the BMS (recommended, simplest):** XT30 main lead on P+/P-, balance lead on B-/B1/B2/B+. Caveat: inside the B6AC the balance-port pin 1 and the output negative are the same ground, so **during charging the BMS discharge FET is bridged** by the balance lead (quack-core makes the same observation: "Its B- pin is the cell side of the pack's BMS: tying it to the board's ground would bypass the BMS's discharge FETs"). This is harmless while charging (the B6AC does per-cell monitoring and cuts off at 4.2 V), and once the charger is unplugged the BMS is back in the circuit. Do not leave the balance lead plugged into anything that ties pin 1 to P- while the robot runs.
2. Bypass (RC-style): main lead on B+/B- directly. Only worth it if the BMS's 20 A "working current" or FET losses bother you; it does not for a 1.5-3 A charge.

### Alternative: 12.6 V 2 A CC/CV wall charger through the BMS
A 3S Li-ion CC/CV adapter (e.g. "Battery Charger 3S Li-Ion 12.6V 2A, 5.5 x 2.5 mm plug" https://robu.in/product/battery-charger-3s-li-ion-12-6v-2a-with-5-5-x-2-5mm-dc-plug ; Tinytronics: "first charges the pack with a constant current (CC) and then switches to a constant voltage (CV)") plugs into P+/P-; the BMS stops each cell at 4.25 V and bleeds 100 mA to balance. **Caveats:** the 4.25 V overcharge trip is above the cells' 4.20 V rating, so balancing depends on the adapter holding 12.60 V accurately — verify with a meter; 100 mA passive balance is slow (fine for cells that start matched). It is the hands-off option; the B6AC is the accurate one.

### Charge-port scheme that fits under the battery lid
```
   lid cut-outs:   [XT30 female]  [JST-XH 4P female]      (both recessed 3-4 mm, keyed)
                       |               |
   pack: cells --B-/B1/B2/B+--> BMS --P+/P--> XT30 pigtail (main, to switch/fuse/servo board)
                 |                    |
                 +-- JST-XH 4P tail   +-- 2nd XT30 (charge port) in parallel with P+/P-
```
- The main XT30 to the robot and the charge XT30 are the same net (P+/P-), so **charging works with the main switch off**, and with the switch on the robot would run from the charger (do not).
- The JST-XH balance connector doubles as the **LiPo alarm socket** when not charging.
- If you prefer the wall charger, replace the charge XT30 with a 5.5x2.1 DC jack (rated >= 2.5 A) on P+/P-.
- Mark polarity on the lid; keyed connectors only; no bare pads.

---

## 5. Buck converter: 7Semi AP64500 module

Module (hubtronics https://hubtronics.in/dc-dc-power-converter-modules/ap64500-5v-5a-dc-dc-buck-converter ; evelta https://evelta.com/7semi-dc-dc-buck-converter-7v-40v-input-to-5v-5a-output-ap64500/): "Input Voltage Range: 7V to 40V DC", "Output Voltage: 5V (Fixed)", "Output Current Up to: 5A continuous", "Efficiency: Up to 90%", "Switching Frequency: 500kHz", "25mm x 22mm", 2 g, ₹822. **No ripple figure, no derating curve, no connector spec published** — pads/screw terminals, check the board.

Chip (Diodes AP64500 datasheet https://www.diodes.com/assets/Datasheets/AP64500.pdf, text-extracted): 3.8-40 V in, 5 A, 45 mOhm / 20 mOhm FETs, fsw 500 kHz with RT = 200 k, **HS peak current limit 6.8-9.2 A (cycle-by-cycle, then hiccup after 512 cycles)**, UVLO 3.5 V rising / 400 mV hysteresis, thermal shutdown 160 °C, 4 ms soft-start, FSS +/-6 % jitter for EMI, theta-JA 45 °C/W (SO-8EP), "Up to 85% Efficiency at 5mA Light Load" (PFM). The 12 V efficiency curve (Figure 4) is only a graph; for 12 V -> 5 V at 1-3 A the curve sits in the high 80s to ~90 % [est. from curve shape]. At 5 V / 2 A that is ~1.2 W of loss in a 25x22 mm module — fine without a heatsink.

Can it power a Radxa Zero 3W? Radxa product brief (https://dl2.radxa.com/zero3/docs/hw/3w/radxa_zero_3w_product_brief.pdf): "The Radxa ZERO 3W support DC +5V voltage: Power adapter with 5V/2A on the USB-C 1 port; 5V Power from the GPIO PIN 2 & 4". Forum (https://forum.radxa.com/t/power-the-zero-via-gpio-pins/13465): pins 2 and 4 "are tied directly to the +5V pins on the USB power port", and "there's no overvoltage protection on the board". Measured draw with a display + USB receiver: "0.9-1.2 amps" (https://forum.radxa.com/t/radxa-zero-3w-plan-questions-for-direct-battery-connection-pmic-rk817-features/27171). **No documented brownout threshold for the Zero 3W was found** [no source found]; the 4.75 V figure is the USB spec floor, and the RK817 PMIC's internal bucks need headroom, so hold the rail at 5.0-5.1 V at the header. Budget: Radxa ~1.2 A + IMX219 ~0.25 A + VL53L8CX ~0.1 A + BNO085 ~0.05 A + 2x SG90 ~0.3 A peak = **~1.5-2 A**, well inside 5 A; at the pack that is ~0.8 A.

**Feed via GPIO pins 2/4, not USB-C**: the header avoids the USB-C cable's resistance (a 1 m USB cable can drop 0.3 V at 2 A), lets you use 20 AWG, and leaves USB-C 1 free for OTG/serial. Put the buck within 10 cm of the Radxa, 20 AWG, and **470-1000 uF low-ESR electrolytic + 10 uF ceramic at the header**. The 5 V rail must be separate from the servo rail (it is — the Waveshare board's own 5 V only feeds its CH343P).

Bulk capacitor on the servo bus: yes. The pack-BMS-fuse-switch-wire path is ~0.15 Ohm [est.] and 14 servos stepping together produce 10-20 A current steps that drop the rail 1.5-3 V for milliseconds. quack-core uses "2 x 470 uF / 16 V" bulk plus 10 uF per port. For 12.6 V use **2x 1000 uF 25 V low-ESR electrolytic across the Waveshare screw terminal** (the same place the Robocraze page's own note about a 10-100 uF motor cap points). Inrush: 2000 uF charging from 0 to 12.6 V through the BMS when you flip the switch is a ~100 A spike for ~1 ms; a 40 A BMS has a short-circuit trip (typically 50-100 us) that may or may not fire — quack-core flags the same risk ("Check the BMS's short-circuit trip against that inrush"). A high-side MOSFET soft switch (section 7) or a 10 Ohm/2 W pre-charge resistor across the switch avoids it.

---

## 6. Mechanical

Holders (3x18650 in a row):
- Hubtronics "18650 3S spring holder" (https://hubtronics.in/18650-3s-spring-holder, ₹35 ex GST): page gives no dimensions or weight, only "Comes with colored soldered wires", "double mounting hole in the center ... 3mm screws", spring contacts.
- Generic 3-slot wired holders: 78.24 x 59.46 x 21.41 mm, 30 g (Little Bird https://littlebirdelectronics.com.au/products/3-x-18650-battery-holder-with-dc2-1-power-jack); 77.5 x 60 x 21.5 mm (Videotronics); 77 x 60 x 20 mm, 25 g (iFuturetech https://ifuturetech.org/product/3x-18650-battery-holder/); 78 x 60 x 22 mm (Tayda). The "58 x 77 x 21" figure in common listings is within tolerance of these — plan on **78 x 60 x 22 mm, 25-30 g**. Note the stock duck bay holds a 2-slot holder (~78 x 40 x 22); the 3-slot is 20 mm wider — check `body_middle_bottom`.
- Spring holders are a known weak point at 10+ A: thin spring steel contacts and 22-24 AWG pigtails add 20-50 mOhm per cell and can lose contact under impact (a falling biped). If you keep a holder, **solder/crimp 18 AWG onto the contacts and bridge each spring to its plate with a short wire**, or use a holder with leaf (not coil) contacts.

Compact alternative: 3 cells in a triangle, spot-welded with 0.15 x 8 mm nickel strip: envelope ~Ø40 x 65 mm (cells 18.6 x 65.2 mm max), weight 3 x 47 g = **~141 g of cells** (P30B 47 g max; 30Q ~48 g; vs 2 cells ~95 g in the stock design) + ~10 g BMS/strip/wrap. Requirements: a spot welder (never solder directly to cell cans), **insulating rings on every positive end**, fish paper or Kapton between cells and under the BMS, 1.5 mm fish paper where nickel crosses an edge, 72 mm PVC heat-shrink wrap, balance and main leads strain-relieved to the wrap (not the strip) with hot glue or a 3D-printed end cap, and fuse-holder outside the wrap. Mark cell polarity and date on the wrap.

---

## 7. Wiring

Wire gauge (Powerstream table https://www.powerstream.com/Wire_Size.htm, "chassis wiring" column, short runs in free air): 16 AWG 22 A (13.2 mOhm/m), **18 AWG 16 A** (20.9 mOhm/m), 20 AWG 11 A, 22 AWG 7 A. A 0.3 m 18 AWG loop drops 0.13 V at 10 A [est.] — acceptable. So **18 AWG silicone is OK for pack -> fuse -> switch -> servo board at the 8-12 A average, marginal for sustained 15 A**; use 16 AWG for the three ~10 cm pack links if you can route it, 18 AWG everywhere else on the servo rail, 20 AWG for the buck and Radxa, 24-26 AWG for balance taps.

Connectors: XT30 is rated **15 A** (Amass; e.g. https://pro.maplin.co.uk/products/prewared-male-xt30u-connector-15a-10cm-amass) — fine for the average, tight for 20-30 A peaks; genuine Amass only. XT60 (30 A) if you want headroom and have the space.

Switch: a KCD1-type rocker is "10A 125VAC / 6A 250VAC" with no DC rating (LCSC guide: "always derate AC ratings significantly before using a switch on DC circuits", https://www.lcsc.com/blog/kcd1-switches-rocker-switches-guide/). A 10 A AC rocker on a 12 V motor load with 2000 uF of bulk capacitance will weld or pit. Options: (a) a **DC-rated 20 A rocker** (e.g. KCD4 size, 20 A 12 VDC marked) — bulky; (b) **high-side P-MOSFET soft switch**: a small slide switch drives the gate of a 30 V P-FET (quack-core uses 2x AON6411 back-to-back, which also gives reverse-pack protection, with the slide switch carrying "about 80 uA"), a 100 k gate pull-up and 10-47 nF gate cap for soft start that also solves the capacitor inrush; off-the-shelf "anti-spark XT30/XT60 switch" modules do the same. Choose (b).

Fuse: **15 A mini (ATM) blade fuse** in an in-line holder, as close to the pack P+ as possible, 16-18 AWG leads. It protects the wire, the XT30 and the Waveshare AO4407 (12 A) from a stuck/shorted servo chain; the BMS's 40 A trip does not. A polyfuse is wrong here: resettable PTCs rated for 10-15 A hold are large, have 10-30 mOhm, and trip slowly and at ~2x hold. Add a **2 A mini blade or 2 A fast glass fuse** on the buck input branch.

Servo-chain fan-out: do not daisy-chain all 14 servos from one 5264 port (3 A/pin). Use at least 3 ports (left leg, right leg, neck/head) as the stock design does, and inject power at the far end of each leg chain with 20 AWG if a chain exceeds 4 servos.

### One-page wiring diagram
```
                     +---------------------------- BALANCE / ALARM ------------------------------+
                     |  JST-XH 4P (lid):  1=B-  2=B1  3=B2  4=B+                                  |
                     |  <- LiPo alarm when idle; <- iMax B6AC balance port when charging          |
                     |                                                                             |
  [Cell1]--[Cell2]--[Cell3]   (3S1P, P30B or 30Q, spot-welded or holder with reinforced contacts)
   B-   B1        B2   B+
   |    |         |    |
   v    v         v    v
  +-------------------------+
  | 3S 40A balance BMS      |   over-charge 4.25 V, over-discharge 2.50 V, OCP 40 A, bal. 100 mA
  |  B-  B1  B2  B+   P+ P- |   (wire taps in order B-, B1, B2, B+; load/charger on P+/P-)
  +-------------------------+
                    P+  P-
                    |    |
        +-----------+    +---------------------------------------------------+
        |                                                                    |
   [15 A ATM fuse]                                                           |
        |                                                                    |
        +---------- XT30 (lid) CHARGE PORT  <- B6AC main lead (LiPo 3S, 1.5-3 A)
        |                                        or 12.6 V 2 A CC/CV adapter
        |                                                                    |
   XT30 (main) ======= 16/18 AWG =======                                     |
        |                                                                    |
  [P-FET soft switch]  (slide switch -> gate; 100k pull-up, gate cap = soft start)
        |                                                                    |
        +-----> 2x 1000 uF 25 V low-ESR  (at the servo board screw terminal) |
        |                                                                    |
        +-----> Waveshare Bus Servo Adapter (A), green screw terminal (9-12.6 V in)
        |         jumper A (UART); wiki: connect RX-RX, TX-TX to the Radxa UART (3.3 V logic)
        |         servo ports: J-left leg (6 ST3215) / J-right leg (6) / J-neck+head (2)
        |         + 18-20 AWG power injection at the knee of each leg chain
        |
        +--[2 A fuse]--> 7Semi AP64500 buck  (12.6->5.0 V, 5 A max; keep <=2 A)
                            |  20 AWG, <10 cm
                            +--> 470-1000 uF + 10 uF  at Radxa header
                            +--> Radxa Zero 3W pins 2/4 (+5 V) & 6/9 (GND)   [USB-C 1 left free]
                            +--> 2x SG90 (5 V, PWM from Radxa)
                            +--> IMX219 (CSI), VL53L8CX + BNO085 (3.3 V from Radxa header, I2C)

  GND: single star at the BMS P- -> switch module GND tab -> servo board GND -> buck GND. Radxa GND
  via the buck only (plus the UART GND wire to the servo board, which is the same net).
```

---

## 8. Recommended parts delta (vs the list in the brief)

Change:
1. **Cells:** prefer Molicel INR18650-P30B (3000 mAh, 30 A, ~17 mOhm) over Samsung 30Q (15 A). Second choice P28A. Keep 30Q only if already bought; then budget for more sag at peaks.
2. **Wire:** 16 AWG for the pack -> fuse -> switch -> servo board links (≤15 cm), 18 AWG elsewhere on the servo rail, 20 AWG for the 5 V branch.
3. **Switch:** replace the rocker with a high-side P-MOSFET soft switch (anti-spark XT30/XT60 switch module, or AON6411/AO4407-class P-FET + slide switch + RC gate), or a switch explicitly rated >= 20 A at 12 VDC.
4. **LiPo alarm:** set to 3.5 V/cell (adjustable 1S-8S buzzer type); it shares the JST-XH balance socket.

Add:
5. **15 A ATM blade fuse + holder** at pack P+; **2 A fuse** on the buck branch.
6. **2x 1000 uF 25 V low-ESR electrolytics** at the servo board input; **470-1000 uF + 10 uF** at the Radxa header.
7. **JST-XH 4-pin balance lead/socket** (3S) and a **second XT30 (charge port)** on the lid; XT30 female-female parallel pigtail.
8. **Battery build consumables:** 18650 positive insulating rings, fish paper/Kapton, 0.15 x 8 mm nickel strip (if spot-welding), 72 mm PVC heat-shrink, or a holder with leaf contacts and re-wired 18 AWG leads.
9. Optional: **INA226/INA219 current monitor** on the pack line read by the Radxa (I2C) so you get real walking-current data and a software low-battery cutoff — the single biggest open question below.
10. Optional: a 10 Ohm 2 W pre-charge resistor across the switch if you do not use the MOSFET soft switch.

Keep as is: Waveshare Bus Servo Adapter (A) (feed via screw terminal), Robocraze 3S 40 A BMS, iMax B6AC (LiPo 3S program, 1.5 A for 30Q / 3 A for P30B), 7Semi AP64500 (feed Radxa via pins 2/4).

---

## 9. Open questions
- **Real walking current** of 14 ST3215 at 12 V on this robot: nothing measured exists publicly; the 100-107 W simulated figure is the only anchor. Measure with an INA226 or a clamp meter before trusting the runtime numbers.
- Whether the Waveshare AO4407 pass FET and 5264 headers survive sustained 10-12 A with 20-30 A peaks at 12.6 V (quack-core's reason for a custom board). Thermal-camera the board on the first walks.
- The 12 V ST3215's firmware over-voltage ceiling (12.6 V is in the Waveshare spec; confirm the register default is >= 12.6 V on your batch, ideally 13 V).
- Whether the Robocraze BMS's short-circuit detector trips on the 2000 uF inrush (test with the soft switch; if it still trips, lower to 1000 uF).
- Exact pads/terminals and output ripple of the 7Semi AP64500 module (not published); scope the 5 V rail under servo load before trusting the Radxa on it.
- Fit of a 78 x 60 x 22 mm 3-slot holder (or a Ø40 x 65 mm triangle pack) in `body_middle_bottom`; the stock bay is for 2 cells.

## Sources
- Waveshare Bus Servo Adapter (A): https://www.waveshare.com/bus-servo-adapter-a.htm ; https://www.waveshare.com/wiki/Bus_Servo_Adapter_(A) ; schematic https://files.waveshare.com/wiki/Bus-Servo-Adapter-(A)/Bus%20Servo%20Adapter%20(A)-Sch.pdf
- Waveshare Servo Driver with ESP32: https://www.waveshare.com/wiki/Servo_Driver_with_ESP32
- AO4407 datasheet: https://www.aosmd.com/pdfs/datasheet/AO4407.pdf
- ST3215 12 V: https://www.waveshare.com/wiki/ST3215_Servo ; STS3215 7.4 V datasheet (translated): https://core-electronics.com.au/attachments/uploads/sts3215-smart-servo-datasheet-translated.pdf
- Open Duck Mini v2: https://github.com/apirrone/Open_Duck_Mini/blob/v2/docs/assembly_guide.md ; https://github.com/ToolKnox/hawkridge-open-duck-mini-v2-bipedal-robot ; sim-to-real torque notes https://github.com/fport/open-duck-mac
- HeyPCB quack-core (power-path design numbers): https://github.com/HeyPCB/quack-core
- Samsung 30Q: datasheet copy https://e2e.ti.com/cfs-file/__key/communityserver-discussions-components-files/196/samsung_5F00_30q_5F00_data_5F00_sheet.pdf ; review https://lygte-info.dk/review/batteries2012/Samsung%20INR18650-30Q%203000mAh%20(Pink)%20UK.html
- Molicel P30B: https://fsaeonline.com/content/INR-18650-P30B-80111.pdf ; P28A review https://lygte-info.dk/review/batteries2012/Molicel%20INR18650-P28A%202800mAh%20(Gray)%20UK.html ; P26A https://www.18650batterystore.com/products/molicel-p26a
- Robocraze 3S 40 A BMS: https://robocraze.com/products/3-series-40a-11-1v-12-6v-18650-lithium-battery-protection-board-with-balance
- 3S BMS wiring/behaviour: https://shillehtek.com/blogs/shillehtek-product-manuals/3s-12v-18650-lithium-battery-protection-board-11-1v-12-6v-balanced-25a-manual ; https://www.tinytronics.nl/en/power/bms-and-chargers/bms/li-ionli-po-protection-circuit-(bms)-3s
- iMax B6AC manual: https://www.pololu.com/file/0J525/iMAXB6ACmanual.pdf ; 3S JST-XH lead https://www.progressiverc.com/products/3s-jst-xh-charge-balance-cable
- 12.6 V 2 A charger: https://robu.in/product/battery-charger-3s-li-ion-12-6v-2a-with-5-5-x-2-5mm-dc-plug ; https://www.tinytronics.nl/shop/en/power/bms-and-chargers/li-ion-and-li-po/without-protection-circuit/li-ion-charger-with-dc-jack-3s-12.6v-2a
- AP64500: module https://hubtronics.in/dc-dc-power-converter-modules/ap64500-5v-5a-dc-dc-buck-converter ; https://evelta.com/7semi-dc-dc-buck-converter-7v-40v-input-to-5v-5a-output-ap64500/ ; datasheet https://www.diodes.com/assets/Datasheets/AP64500.pdf
- Radxa Zero 3W: product brief https://dl2.radxa.com/zero3/docs/hw/3w/radxa_zero_3w_product_brief.pdf ; GPIO power thread https://forum.radxa.com/t/power-the-zero-via-gpio-pins/13465 ; battery/PMIC thread https://forum.radxa.com/t/radxa-zero-3w-plan-questions-for-direct-battery-connection-pmic-rk817-features/27171
- 3x18650 holders: https://hubtronics.in/18650-3s-spring-holder ; https://littlebirdelectronics.com.au/products/3-x-18650-battery-holder-with-dc2-1-power-jack ; https://ifuturetech.org/product/3x-18650-battery-holder/
- Wire gauge: https://www.powerstream.com/Wire_Size.htm ; XT30 15 A: https://pro.maplin.co.uk/products/prewired-male-xt30u-connector-15a-10cm-amass ; KCD1 DC derating: https://www.lcsc.com/blog/kcd1-switches-rocker-switches-guide/
