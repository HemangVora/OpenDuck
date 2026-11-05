# Open Duck Mini v2 — buy locally in Vadodara

Companion to `shopping-list.md`. Everything here is generic enough that a local shop will have it, usually cheaper and same-day. Carry this list on your phone; the **Ask for** column is what to say at the counter, the **Check** column is how to avoid the wrong part. Online fallbacks are in `shopping-list.md`.

Rough local total: **₹3,500–5,500** (versus ≈ ₹7,500 online for the same items). More importantly it removes ~15 courier parcels from the Diwali week.

## 1. Electronics component shop (component market, not a mobile-accessory stall)

| Item | Qty | Ask for | Check | Est. |
|---|---|---|---|---|
| Silicone wire 16 AWG | 1 m red + 1 m black | "16 AWG silicone wire, 1.3 sq mm, red and black" | Soft silicone jacket, fine-strand copper. Not the stiff PVC "hookup" wire. For pack links, BMS to switch, switch to servo adapter | ₹80–120 |
| Silicone wire 18 AWG | 2 m red + 2 m black | "18 AWG silicone, 0.8 sq mm" | Same. Servo power rail and fuse wiring | ₹80–120 |
| Hookup wire 22–24 AWG | 2 m each of 4 colours | "22 AWG multi-strand hookup wire" | For IMU, foot switches, 5 V to the Radxa header | ₹60 |
| JST-XH 2.54 mm connectors | 10× 2-pin, 5× 4-pin housings + crimp pins, and one **4-pin (3S) balance socket** | "JST-XH 2.54 mm housing with pins, 2-pin and 4-pin" | 2.54 mm pitch, white, with a latch. The shop may call them "relimate 2.54 mm", which is the same thing. Need one 4-pin for the balance lead to the charger | ₹100 |
| XT30 connector pairs | 3 pairs | "XT30 male-female pair" | Yellow, 2-pin, ~30 A. If they only have XT60 that also works but is bulkier; if neither, buy online | ₹40 ea |
| Blade fuse holder + 15 A fuse | 1 holder, 2 fuses | "Inline ATM/mini blade fuse holder with 16 AWG wire, 15 A fuses" | Blade type, wire ≥ 16 AWG. Auto parts shop (section 3) has these too | ₹80 |
| Toggle or rocker switch, DC rated | 1 | "Toggle switch 20 A 12 V DC" | Must say a **DC amp rating**, 15 A minimum. Most small rockers are rated 6 A 250 VAC only and will arc at 10 A DC. An automotive toggle is the safe pick | ₹60–120 |
| Electrolytic capacitors | 2× 1000 µF 25 V, 1× 470 µF 16 V | "1000 µF 25 V low ESR electrolytic" | Voltage rating ≥ 25 V for the 12.6 V rail. 105 °C type if offered | ₹40 |
| Ceramic / MLCC capacitors | 2× 10 µF, 2× 0.1 µF | "10 µF 25 V ceramic" | For the 5 V rail at the Radxa | ₹20 |
| Heat-shrink tube assortment | 1 box | "Heat shrink sleeve assorted, 2 mm to 10 mm" | Includes 8–10 mm for XT30 and 2–3 mm for JST pins | ₹100 |
| Solder wire 0.8 mm + flux | 1 roll, 1 tub | "60/40 or 63/37 solder 0.8 mm, rosin flux paste" | Leaded 60/40 is fine and easier on a 60 W iron | ₹150 |
| Soldering iron 60 W adjustable | 1 | "60 W temperature-controlled soldering iron, conical and chisel tips" | Temperature knob, 200–450 °C. A spare conical tip is the one that will press the heat-set inserts | ₹500–700 |
| Soldering stand, sponge, brass tip cleaner | 1 | – | – | ₹150 |
| Desoldering wick | 1 | "Solder wick 2 mm" | – | ₹50 |
| Nylon cable ties 100 mm, 2.5 mm | 1 pack | "Cable ties 100 mm" | For routing servo cables in the legs | ₹40 |
| Kapton tape 10–20 mm | 1 roll | "Polyimide / Kapton tape, high temp" | Amber, thin. Many shops stock it for phone repair | ₹100–150 |
| Double-sided foam tape | 1 | "3M double-sided foam tape 10 mm" | For the BNO085 and the buck module | ₹60 |
| USB to TTL adapter | 1 | "CP2102 or FTDI USB to TTL 3.3 V" | **Must have a 3.3 V logic jumper or be 3.3 V**. Used only to configure servos from the Mac before the Radxa is ready. CP2102 is fine if it's genuine | ₹120–200 |
| 5 V 5 A buck converter (fallback only) | 1 | "XL4015 5 A buck module" | Only if the Robocraze AP64500 is delayed. Set it to 5.10 V with a multimeter before connecting the Radxa | ₹120 |
| Multimeter | 1 if you don't own one | "Digital multimeter with DC current 10 A" | Needed to set the buck, check pack voltage and polarity before first power-on | ₹400–800 |
| USB-C to USB-C and micro-USB cables | 1 each | – | For flashing and the servo adapter's USB-C port | ₹150 |

## 2. Battery / inverter / mobile-repair shop

| Item | Qty | Ask for | Check | Est. |
|---|---|---|---|---|
| 18650 cells | 3 (buy 4 for a matched set) | "Samsung 30Q, Samsung 25R, LG HG2, Molicel P26A/P28A, or Sony VTC6" | **Only these branded high-drain cells.** Walk away from cells marked 4000–9900 mAh, "UltraFire" or any unbranded wrap: they are 800–1500 mAh and cannot deliver 10 A. Ask for flat-top, unprotected. Check all have the same printed batch code. Measure each at the counter: 3.5–3.8 V and within 0.05 V of each other | ₹350–500 ea |
| 3S 18650 BMS 40 A, same-port, with balance | 1 | "3S 12.6 V 40 A BMS with balancing" | Four solder pads: B-, B1, B2, B+ (plus P- out). "With balance" matters; the ₹60 ones without it will drift. 40 A rating | ₹120–200 |
| Nickel strip | 30 cm | "0.15 × 8 mm nickel strip" | Only if you want to spot weld; our plan solders 16 AWG to the cell ends with a hot iron and flux, so this is optional | ₹50 |
| Fish paper / insulating rings | 20 rings + 1 sheet | "18650 insulation rings" | Mobile-repair shops that rebuild power banks stock these | ₹50 |
| 18650 3-cell holder (test only) | 1 | "3× 18650 holder with wires" | For bench tests only; spring holders cannot carry walking current. Not for the robot | ₹60 |

Charger note: the **iMax B6AC** stays an online or RC-hobby-shop item. If Vadodara has an RC/drone hobby shop, they will have it or a SkyRC equivalent for ₹2,000–2,800; make sure it has a 3S balance port and a LiPo/LiIon program.

## 3. Auto parts / two-wheeler accessories shop

| Item | Qty | Ask for | Check | Est. |
|---|---|---|---|---|
| Blade fuse holder + 15 A fuses | 1 + 2 | "Mini blade fuse holder with wire, 15 A fuse" | Same as above, usually better quality here | ₹80 |
| 20 A DC toggle switch | 1 | "Headlight toggle switch, 20 A" | Chunky metal toggle. DC rated by default | ₹80–150 |
| Insulation tape, good brand | 1 | – | – | ₹30 |

## 4. Bearing dealer (industrial area / GIDC shops)

| Item | Qty | Ask for | Check | Est. |
|---|---|---|---|---|
| 6804ZZ bearing 20 × 32 × 7 mm | 3 (buy 4) | "6804 ZZ, 20 bore, 32 OD, 7 wide, metal shielded" | Say the numbers; "6804-2Z" and "61804-ZZ" are the same part. Any brand is fine for the duck's loads; NBC/SKF/HCH all work. Spin it: must be smooth with no grit | ₹60–150 ea |

## 5. Hardware / fastener shop

| Item | Qty | Ask for | Check | Est. |
|---|---|---|---|---|
| M3 socket-head (allen) screws, stainless or black | 40× M3×6, 40× M3×8, 30× M3×10, 20× M3×12, 10× M3×16, 10× M3×20 | "M3 allen socket head cap screw, full thread" | Socket head, **not** pan/Phillips. Buy counts generously; the kit online is 600 pcs for ₹629, so stop if local is more than ~₹2.5 per screw | ₹300–500 |
| M3 nuts + M3 nyloc nuts | 30 + 20 | "M3 hex nut, M3 nyloc" | – | ₹60 |
| M3 washers | 30 | – | – | ₹30 |
| M2.5 screws + nuts | 10 | "M2.5 × 6 and × 10" | Radxa/Pi mounting standoffs (Ø2.8 holes) | ₹40 |
| M2.5 × 6 mm nylon or brass standoffs | 4 (+4 nuts) | "M2.5 standoff 6 mm" | Lifts the Radxa off the head floor | ₹40 |
| Hex key set 1.5–6 mm | 1 | "Allen key set, long arm, metric" | Needs 2.0 and 2.5 mm (M2.5, M3) and 1.5 mm for the servo screws. Ball-end tips help inside the legs | ₹150–250 |
| Loctite 243 (blue, medium) | 1 small tube | "Loctite 243" or "Loctite 242" | Blue only. Red 271 is permanent and will stop you ever disassembling. Also an anaerobic generic "medium strength" is fine | ₹200–350 |
| Small flat and Phillips screwdrivers, tweezers | 1 set | – | – | ₹150 |
| Flush cutter / nipper | 1 | "Flush cut nipper, 5 inch" | Flush face on one side | ₹150–250 |
| Needle files or a deburring blade | 1 | "Needle file set" | Cleans print edges and the switch slots in the feet | ₹100–200 |
| Super glue (cyanoacrylate) + a 50 mm roll of sandpaper 240 grit | 1 | – | TPU soles do not glue, but small PLA repairs do | ₹80 |
| Digital vernier calliper 150 mm | 1 if you don't own one | – | Check the first print's dimensions and the insert hole size (Ø4.0) | ₹300–600 |

## Things that must stay online (do not waste a trip)

- Servos, Bus Servo Adapter (A), KW-12 switches, Radxa and heatsink → Hubtronics.
- BNO085 IMU, AP64500 buck, iMax B6AC, LiPo alarm → Robocraze (or RC shop for the charger).
- **M3 × 5 mm brass heat-set inserts (Ø4.0 hole)**: local shops stock press-fit knurled inserts for plastic injection parts but almost never the short 3D-print style; order B0DZ8B7FW1 online now.
- microSD 64 GB **A2** (SanDisk Extreme / Samsung Pro Plus): mobile shops have A1 cards, which boot slowly and wear fast. Only buy locally if the card says A2 on the front and the shop is a brand outlet (fakes are common).
- Filament dryer, camera, ToF, INA226.

## Before paying, at the counter

1. Cells: measure voltage; all within 0.05 V; printed batch code matches.
2. Switch and fuse holder: a **DC** current rating printed on them.
3. Bearings: 20 × 32 × 7, spin smooth.
4. USB-TTL: 3.3 V logic; servos ignore 5 V TTL only sometimes, and the adapter's RX pin is 3.3 V.
5. Screws: socket head, M3, full thread.
6. Wire: strip 1 cm; fine silicone-jacketed strands, copper-coloured (not silver aluminium).

## Mumbai version (added 2026-11-02, for the ETHGlobal week at 400076 Powai)

Two markets cover everything above except the heat-set inserts, the balance charger, the LiPo alarm and the servos.

**Lamington Road, Grant Road East 400007** (electronics market, ~22 km / 45–60 min from Powai). Wire, JST-XH ("relimate 2.54"), XT30, heat-shrink, Kapton, foam tape, cable ties, capacitors, BMS, switch, fuse holder, USB-TTL, multimeter, calliper, tweezers, wick, flux, 18650 cells.
- Visha World, 17, 1st floor, Ganesh Bhavan, opp. Lamington Road Police Station, 357 Lamington Rd, +91 98335 99908, vishaworld.com (Soldron distributor; online catalogue shows 3S 25 A BMS ₹150, hookup wire packets, generic 18650 only).
- Aavkar Electronics, Lamington Road (batteries incl. 18650 wholesale/retail since 1991; WhatsApp for brands and stock before going; insist on Samsung 30Q / LG / Molicel wraps).
- Prism Electronics, Shop 2, Panditalaya Bldg, Chunam Lane, Lamington Rd. New Silikon Electronic (general components).

**Nagdevi Street / Masjid Bunder 400003** (bearing and fastener market, ~3 km from Lamington Rd). 6804ZZ bearings, M3 socket-head screws, nyloc nuts, M2.5 screws and standoffs, hex keys, Loctite 243.
- The Bearing Store, Nagdevi, WhatsApp +91 98676 48784, Mon–Sat 11:00–18:45 (bearingstore.in; message "6804ZZ ×4" first).
- Ball Bearing & Machinery Corp, 172/174 Nagdevi St, 2nd floor. Vaibhav Bearing Centre, Nagdevi.
- Allen-bolt dealers along Nagdevi St and Lohar Chawl for the M3/M2.5 hardware.

**Checked and not useful:** Evelta (Jui Nagar, Navi Mumbai) lists ST3215-C018 12 V and C001 7.4 V but both are "notify when back in stock"; RC Mumbai (rcmumbai.com) is online-only, iMax B6/B6AC sold out there. No component shop near Powai; the Vikhroli/Ghatkopar listings are electrical/appliance stores.
