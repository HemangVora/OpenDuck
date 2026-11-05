# Zbotic cart (verified 2026-10-30 via Zbotic's product API)

Zbotic has 11 of the list's parts in stock. The servos are ₹111 cheaper each than Hubtronics (₹2,288 vs ₹2,399), saving ₹1,776 on 16. Product IDs are WooCommerce IDs; stock max is Zbotic's own cart limit.

| # | Part | Qty | Price | Stock max | Product ID | Page |
|---|---|---|---|---|---|---|
| 1 | Waveshare ST3215-HS 20 kg·cm 106 rpm bus servo | 16 | ₹2,288.02 | 19 | 513478 | https://zbotic.in/product/waveshare-20kg-cm-bus-servo-motor-106prm-high-speed-large-torque-with-360-degrees-high-precision-magnetic-encoder/ |
| 2 | Waveshare Serial Bus Servo Driver Board (= Bus Servo Adapter A) | 1 | ₹418.90 | – | 540912 | https://zbotic.in/product/waveshare-serial-bus-servo-driver-integrates-servo-power-supply-control/ |
| 3 | XY-3606 buck 9–36 V → 5 V 5 A (Radxa supply; replaces the Robocraze AP64500) | 1 | ₹132.16 | – | 17852 | https://zbotic.in/product/12v-24v-to-5v-5a-power-module-dc-dc-xy-3606-power-converter/ |
| 4 | FT232RL USB-TTL, 3.3/5 V jumper (servo setup from the Mac) | 1 | ₹94.40 | – | 3172 | https://zbotic.in/product/ft232rl-usb-to-ttl-5v-3-3v-download-cable-to-serial-adapter-module-for-arduino/ |
| 5 | TowerPro SG90 (antennas) | 2 | ₹86.14 | – | 4520 | https://zbotic.in/product/towerpro-sg90-180-degree-rotation-servo-motor/ |
| 6 | 16 AWG extrasoft silicone wire, 1 m (pack links) | 2 | ₹55.46 | 8 | 465175 | https://zbotic.in/product/16awg-extrasoft-silicone-wire/ |
| 7 | 18 AWG extrasoft silicone wire, 1 m, red (servo rail) | 3 | ₹30.14 | – | 464892 | https://zbotic.in/product/18awg-extrasoft-silicone-wire-color-red/ |
| 8 | Kapton tape 10 mm × 100 ft | 1 | ₹74.34 | – | 454642 | https://zbotic.in/product/10mm-100ft-high-temperature-heat-resistant-polyimide-koptan-tape-hot/ |
| 9 | Heat-shrink assortment, 140 pcs | 1 | ₹186.44 | – | 586627 | https://zbotic.in/product/140-pieces-heat-shrink-tubes-insulated-wire-cable-sleeving-wrap/ |
| 10 | 5–36 V high-power MOSFET trigger module (optional soft power switch) | 1 | ₹33.28 | – | 6876 | https://zbotic.in/product/5-36v-switch-drive-high-power-mosfet-trigger-module/ |
| 11 | 3× 18650 holder, bench tests only | 1 | ₹33.16 | – | 448578 | https://zbotic.in/product/black-plastic-storage-box-case-holder-for-battery-3-x-18650-cell-box-without-cover/ |

Cart total ≈ ₹38,000 (servos ₹36,608 + ₹1,400 small parts).

## How to add everything to the cart in your open tab

Zbotic's pages sit behind a Cloudflare check that blocks automated browsers, so the add has to happen from your own tab. Two ways:

**A. One paste (fastest).** In the Zbotic tab press ⌥⌘J (Chrome DevTools console), paste this, press Enter, then open https://zbotic.in/cart/ :

```js
(async()=>{const items=[[513478,16],[540912,1],[17852,1],[3172,1],[4520,2],[465175,2],[464892,3],[454642,1],[586627,1],[6876,1],[448578,1]];
for(const [id,q] of items){const r=await fetch('/?wc-ajax=add_to_cart',{method:'POST',credentials:'include',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:`product_id=${id}&quantity=${q}`});const j=await r.json().catch(()=>({}));console.log(id,q,j.error?'FAILED':'ok');}
console.log('done, open /cart/');})();
```

**B. Click the links** (each one adds the item and lands on the cart):

- https://zbotic.in/cart/?add-to-cart=513478&quantity=16
- https://zbotic.in/cart/?add-to-cart=540912&quantity=1
- https://zbotic.in/cart/?add-to-cart=17852&quantity=1
- https://zbotic.in/cart/?add-to-cart=3172&quantity=1
- https://zbotic.in/cart/?add-to-cart=4520&quantity=2
- https://zbotic.in/cart/?add-to-cart=465175&quantity=2
- https://zbotic.in/cart/?add-to-cart=464892&quantity=3
- https://zbotic.in/cart/?add-to-cart=454642&quantity=1
- https://zbotic.in/cart/?add-to-cart=586627&quantity=1
- https://zbotic.in/cart/?add-to-cart=6876&quantity=1
- https://zbotic.in/cart/?add-to-cart=448578&quantity=1

## Checked and NOT available at Zbotic (keep the other sources)

Radxa Zero 3W (Hubtronics only) · BNO085/BNO055 (Robocraze) · 3S 40 A BMS (only 3S 10 A boards; Robocraze/Amazon/local) · iMax B6AC (copy out of stock, only the ₹6,684 SkyRC original; Robocraze ₹2,280) · 18650 cells · 6804ZZ bearings · KW-12/KW10 microswitches (out of stock; Hubtronics) · 1000/470 µF capacitors · M3 heat-set inserts · M3 screws · microSD 64 GB · blade fuse holder · JST-XH kit · XT30 pairs (only the female half) · LiPo alarm (only the no-alarm tester) · INA226.

If you buy the servos here, the Hubtronics cart shrinks to: Radxa Zero 3W 2 GB, heatsink, 4× KW-12. The driver board can come from either.
