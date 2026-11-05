# Hubtronics cart (built 2026-10-30)

Store: https://hubtronics.in (Pune, OpenCart, shows exact stock). Cart page: https://hubtronics.in/index.php?route=checkout/cart
Prices are GST-inclusive. Shipping is added at checkout (3–5 days to Vadodara).

**Final cart 2026-10-30: ₹46,503.00** (₹39,409.32 + 18 % IGST ₹7,093.68). 15 lines, 2.40 kg. Hemang removed the 60 W iron, solder wire and microSD (already owned); the KCD4 rocker, fuse holder and glass fuses (buying switch and fuse at a local shop); and the IMX219 camera + adapter cable (vision is Phase 5, a camera will be chosen then). **Air shipment: nothing in the cart contains a battery, and the two lines whose names mention batteries (18650 holder, XT60 "for LiPo battery") were removed on 2026-10-30 so courier screening has nothing to flag.**

**Hubtronics' cart silently drops lines beyond 24 distinct products** (seen three times: 25→24, 27→24, 25→24). Keep it at 24 lines or fewer; consolidate instead of adding.

## What is in the cart

| # | Item | Product ID | Qty | Unit | Line | Stock seen | Note |
|---|---|---|---|---|---|---|---|
| 1 | ST3215-HS 20 kg·cm 12 V bus servo, 106 rpm | 3722 | 16 | ₹2,399.00 | ₹38,384.00 | 18 | 14 + 2 spare, all one model |
| 2 | Serial Bus Servo Driver Board (Bus Servo Adapter A) | 4122 | 1 | ₹449.00 | ₹449.00 | 12 | |
| 3 | KW-12 lever microswitch (foot contacts) | 7153 | 4 | ₹15.00 | ₹60.00 | 100 | |
| 4 | Radxa Zero 3W 2 GB with header, RS107-D2E0H1W15 | 4360 | 1 | ₹5,760.00 | ₹5,760.00 | 9 | 4 GB and eMMC variants all out of stock |
| 6 | XY-3606 12/24 V → 5 V 5 A buck (HW-688) | 6506 | 1 | ₹129.00 | ₹129.00 | 446 | AP64500 out of stock; XY-3606 was already the Amazon alternative |
| 8 | TowerPro SG90 (antennas) | 507 | 2 | ₹89.00 | ₹178.00 | 383 | |
| 9 | 1000 µF 25 V 105 °C electrolytic (Hyncdz) | 4119 | 4 | ₹7.00 | ₹28.00 | 124 | servo-bus inrush, 2 used + 2 spare |
| 10 | 470 µF 25 V 105 °C electrolytic (Hyncdz) | 3658 | 3 | ₹5.00 | ₹15.00 | 439 | 5 V rail |
| 11 | 0.1 µF ceramic disc, pack of 25 | 7040 | 1 | ₹35.00 | ₹35.00 | 91 | through-hole decoupling |
| 12 | Multitec 06 micro shear cutter | 4113 | 1 | ₹103.00 | ₹103.00 | 80 | flush cutter |
| 13 | Heat-shrink 2 mm black, 1 m (Woer) | 531 opt 291=442 | 2 | ₹5.90 | ₹11.80 | 139 | |
| 14 | Heat-shrink 4 mm black, 1 m | 531 opt 291=443 | 2 | ₹11.80 | ₹23.60 | | |
| 16 | JST-XH 4-pin female to bare wire, 28 cm | 2151 | 2 | ₹11.80 | ₹23.60 | 140 | = 3S balance lead (B−, B1, B2, B+) |
| 17 | **7Semi BNO055 Qwiic IMU** (substitute) | 7871 | 1 | ₹1,274.00 | ₹1,274.00 | 9 | BNO085 out of stock here (both boards). BNO055 is the IMU in the official Open Duck Mini v2 BOM, so the upstream runtime supports it as-is. Remove if you will wait for the Robocraze BNO085 (₹2,089, after 3 Nov) |
| 25 | Aluminium heat-sink set for Pi 3B (3 pcs, adhesive) | 8465 | 1 | ₹29.00 | ₹29.00 | 41 | Radxa 5519A heatsink out of stock; stick the 14 mm one on the RK3566 |

Removed for air shipping: 18650 3S spring holder (pid 2310, ₹35.40) and XT60 pairs (pid 5510). Removed to stay under the 24-line cap: 6 mm heat-shrink (pid 531 opt 444). Only one substitute remains: the BNO055 (upstream's stock IMU). Switch, fuse and 16 AWG wire come from a Vadodara shop (see `local-shopping-list.md`).

## Not available at Hubtronics (buy elsewhere)

Out of stock on 2026-10-30 although listed: Radxa heatsink 5519A, BNO085 (both 7Semi boards), AP64500 5 V 5 A buck, all branded 18650 cells (Molicel P28A/P30B/M35A, Samsung 30Q/25R, LG F1L), inline blade fuse holder, FT232RL and every CH340/CP2102 USB-TTL module, the 60 W iron kit with tips and the 80 W irons, 3S 10 A BMS, 4S 40 A BMS, M3 kit, IMX219 for Pi 5 (22-pin), Pi Camera V2, 8 Ω speaker.

Never stocked: 3S 40 A BMS, iMax B6AC / any balance charger, XT30, silicone wire, JST-XH crimp kit, heat-set inserts, M3 socket screw kit, 6804ZZ bearings, Loctite, hex keys, LiPo voltage alarm, Kapton, 18650 insulating rings, INA226 module (only the bare IC; INA219 module ₹89 is limited to 3.2 A), VL53L8CX, MOSFET trigger switch, deburring tool.

So the remaining orders are: Amazon (FTDI B072NDZL9K, 18650 Samsung 30Q B0HL8CRN1P, XT30, inserts, M3 kit, bearings, Loctite, iron, hex keys, Kapton, rings, INA226), Robocraze (iMax B6AC, 3S 40 A BMS, LiPo alarm, BNO085 if wanted), local shops per `local-shopping-list.md` (wire, cells, BMS, fuse, switch, bearings, screws). DigiKey for the VL53L8CX when vision starts.

## Re-adding the cart in your own browser

The cart above lives in the gstack browser window. To rebuild it in your own Chrome, open any hubtronics.in page, press F12 → Console, paste:

```js
(async()=>{const items=[[3722,16],[4122,1],[7153,4],[4360,1],[6506,1],[507,2],[4119,4],[3658,3],[7040,1],[4113,1],[531,2,{'option[291]':'442'}],[531,2,{'option[291]':'443'}],[2151,2],[7871,1],[8465,1]];
for(const [pid,qty,opt] of items){const fd=new URLSearchParams({product_id:pid,quantity:qty,...(opt||{})});const r=await fetch('/index.php?route=checkout/cart/add',{method:'POST',body:fd,headers:{'X-Requested-With':'XMLHttpRequest'}});console.log(pid,qty,(await r.json()).success?'ok':'FAIL')}
location.href='/index.php?route=checkout/cart'})()
```

Delete any `[pid,qty]` pair you do not want before pasting, and never exceed 24 pairs (see the cap above). Check the cart page once before paying: Hubtronics' own banner says quantities cannot be changed after ordering.

Pitfall for future lookups: on a product page the first `input[name=product_id]` is often a related product in the "frequently bought together" block; the real id is in the page scripts as `product_id=NNNN` (slug `60w-soldering-iron` → 3195, not the 4656 that the first input shows).

## Stock snapshot 2026-10-30 (for the record)

ST3215-HS 18 (unchanged since 10-27) · ST3215 30 kg 9 (was 33 → 11 → 9) · Radxa Zero 3W 2 GB 9 (was 11) · Bus Servo Adapter 12 (was 15) · KW-12 100 · SanDisk Extreme 64 GB 8 · BNO055 Qwiic 9 · IMX219-160 1.
