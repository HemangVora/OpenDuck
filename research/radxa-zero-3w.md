# Radxa Zero 3W as the Open Duck Mini v2 onboard computer

Research date: 2026-10-28. Target: ST3215 bus servos at 1 Mbps via Waveshare Bus Servo Adapter (A), BNO085 IMU on I2C at ~100 Hz, IMX219 camera, VL53L8CX 8x8 ToF, two SG90 PWM servos, a 50 Hz ONNX policy in Python, Pi Zero 2W footprint. Buyer is in Vadodara, India.

## TL;DR

- Electrically and mechanically the Zero 3W is a drop-in for a Pi Zero 2W: 65 x 30 mm, four Ø2.8 mm holes on a 57.85 x 22.9 mm grid (Pi Zero: 58 x 23 mm), same 40-pin header, same 22-pin 0.5 mm camera FPC. A Pi Zero (or Pi 5) 22-to-15-pin camera cable is the right cable for a stock IMX219 module.
- Every interface the robot needs is on the header and has an official rsetup overlay: UART3/4/5/9, I2C3/I2C4, SPI3, PWM8/9/12/13/14/15. A workable, conflict-free pin plan exists (below).
- The weak spots are software maturity, not hardware: camera needs the `rkaiq_3A_server` ISP daemon and is capped at 1080p30 by the vendor IMX219 driver (users see ~20-30 fps); PWM via mraa is broken on the 6.1 kernel (use python-periphery or sysfs instead); UART2 (pins 8/10) is the boot console and should be avoided; Blinka exists for the board but only for GPIO/I2C/SPI, not PWM.
- Power: 5 V only, 5 V/2 A adapter minimum, ~3 W idle / ~4 W all-core load measured (0.6-0.8 A). Heatsink is mandatory: 80 °C and throttling within 2 min at full load bare. Header pins 2/4 are an officially sanctioned 5 V input.
- Availability is the real problem. Arace: all 12 Zero 3W SKUs and all 4 Zero 3E SKUs sold out. ThinkRobotics: all 16 variants sold out. Hubtronics (India) has exactly one Zero 3W variant in stock today: 2 GB / no eMMC / with header, 11 units, ₹5,760 incl. GST. Everything else at Hubtronics incl. all Zero 3E variants is out of stock. Radxa's Sept 2026 product brief still promises supply until Sept 2030, but forum threads from Dec 2025-Apr 2026 report a worldwide shortage with no official explanation.
- Fallback: the Open Duck Mini v2 reference runtime is written for and "only tested on the Raspberry Pi Zero 2W" with a 50 Hz loop, onnxruntime CPU provider, rustypot Feetech at 1,000,000 baud over a USB serial adapter, and a BNO055 over Blinka I2C. So a Zero 2W is proven for the policy loop; the camera is the part that will be tight on 512 MB.

---

## 1. Camera

**Connector.** One 4-lane MIPI CSI-2 on a 22-pin, 0.5 mm pitch FPC connector (spec table and hardware-interface page). Pinout: D0-D3 differential pairs, CLK0, CAMERAB_PDN_L (pin 17), CIF_CLKOUT (pin 18), I2C2_SCL_M1/I2C2_SDA_M1 (pins 20/21), VCC_3V3 (pin 22).
- https://docs.radxa.com/en/zero/zero3
- https://docs.radxa.com/en/zero/zero3/hardware-design/hardware-interface
- Product brief §6.3: https://dl2.radxa.com/zero3/docs/hw/3w/radxa_zero_3w_product_brief.pdf

**Cable.** Same "mini" 22-pin 0.5 mm connector as the Pi Zero / Pi Zero 2 W and Pi 5. A Pi Zero camera cable (22-pin 0.5 mm at the board end, 15-pin 1.0 mm at the camera end) fits the Zero 3W and a standard IMX219 module (Pi Camera v2 / Radxa Camera 8M). The official Pi 5 camera cable is the same 22-to-15 arrangement, so it also works. Radxa staff on the forum recommended exactly "rpi zero fpc + rpi imx219 camera".
- https://forum.radxa.com/t/mpi-csi-camera-interface-radxa-zero-3w/19742
- Pi 5 cable is 22-pin to 15-pin: https://thepihut.com/collections/raspberry-pi/products/camera-adapter-cable-for-raspberry-pi-5
- Watch out: some boards from the V1.12 production run shipped with the FPC connector mounted inverted (contacts on the wrong side). Radxa staff (Raphael) called it "a manufacturing defect", not a revision. Workaround used by two forum users: flip the cable and the grey clamp. https://forum.radxa.com/t/zero-3w-camera-8m-doesn-t-work/22617
- The docs stress cable orientation: "pay attention to the direction of the interface of the camera cable!" https://docs.radxa.com/en/zero/zero3/accessories/camera

**Official IMX219 support.**
- Supported list: Raspberry Pi Camera V1.3 (OV5647), Raspberry Pi Camera V2 (IMX219), Radxa Camera 8M (IMX219). https://docs.radxa.com/en/zero/zero3/accessories/camera
- Overlay: `radxa-zero3-rpi-camera-v2.dtbo` (source: `radxa-zero3-rpi-camera-v2.dts`, "Enable Raspberry Pi Camera v2", sensor `sony,imx219` at I2C2 address 0x10, `data-lanes = <1 2>` i.e. 2-lane, 24 MHz xvclk, power-down GPIO3_C6). Enabled via `sudo rsetup` -> Overlays -> Manage overlays, then reboot; verify with `cat /boot/extlinux/extlinux.conf` for an `fdtoverlays /boot/dtbo/radxa-zero3-rpi-camera-v2.dtbo` line.
  - https://github.com/radxa/overlays/blob/main/arch/arm64/boot/dts/rockchip/overlays/radxa-zero3-rpi-camera-v2.dts
  - https://docs.radxa.com/en/zero/zero3/radxa-os/rsetup
- Pipeline that Radxa documents (V4L2 via GStreamer, no libcamera):
  `gst-launch-1.0 v4l2src device=/dev/video0 io-mode=4 ! videoconvert ! video/x-raw,format=NV12,width=1920,height=1080 ! jpegenc ! multifilesink location=test.jpg`
  Preview: `cheese`. OpenCV `cv2.VideoCapture(0, cv2.CAP_V4L2)` with NV12/YUYV works the same way (rkisp exposes /dev/video0 as the ISP main path). https://docs.radxa.com/en/zero/zero3/accessories/camera
- ISP daemon: dark/green images or 5-10 fps freezes mean the Rockchip AIQ 3A engine isn't running; Radxa staff: "run rkaiq_3A_server before run gst-launch". On Debian 12 the `camera_engine_rkaiq` package must be updated manually (deb linked on the download page). 
  - https://forum.radxa.com/t/zero-3w-raspberry-pi-camera-v2-doesnt-work/20132
  - https://docs.radxa.com/en/zero/zero3/download (RKISP tooling section)
- Achievable resolution/fps: the vendor kernel `media/i2c/imx219.c` defines a single mode, 1920x1080 @ 30 fps. Users measured ~21 fps at 720p (sensor still running 1080p, ISP scaling) and ~30 fps at 1280x720 with the performance governor; selecting 3280x2464 crashed the kernel. No 60 fps mode, no libcamera.
  - https://forum.radxa.com/t/imx219-resolution-on-3w/20788
- Kernel sensitivity: one user (Aug-Sep 2024, Bullseye b6) got the Radxa 8M/IMX219 working only on `5.10.160-26-rk356x`, not `-38`. The current official image is 6.1-based; the forum thread about the camera-v2 overlay had a fresh "same problem" post in Sept 2025. Treat camera bring-up as a day of work, not plug-and-play.
  - https://forum.radxa.com/t/zero-3w-camera-8m-doesn-t-work/22617
- Hardware encoder: H.264/H.265 up to 1080p60 on paper (brief), ~20 fps measured through `mpph264enc` by one user. https://forum.radxa.com/t/rk3566-h-264-encoding-performance-issue/28829

## 2. UART

**On the header (product brief §6.1.1 and hardware-interface page):**

| UART | Pins (RX / TX) | GPIO | Shares pins with | Overlay |
|---|---|---|---|---|
| UART2_M0 | 10 / 8 | GPIO0_D0 / D1 | boot console @1.5 Mbps, FIQ debugger | `rk3568-uart2-m0`, `rk3568-disable-fiq-debugger` |
| UART3_M0 | 3 / 5 | GPIO1_A0 / A1 | I2C3_M0 (+ onboard pull-ups) | `rk3568-uart3-m0` |
| UART4_M1 | 16 / 18 | GPIO3_B1 / B2 | PWM8_M0 / PWM9_M0 | `rk3568-uart4-m1` |
| UART5_M1 | 33 / 32 | GPIO3_C3 / C2 | I2S1 | `rk3568-uart5-m1` |
| UART9_M1 | 24 / 21 | GPIO4_C6 / C5 | SPI3_M1 CS0 / MISO, PWM13/12 | `rk3568-uart9-m1` |

- https://docs.radxa.com/en/zero/zero3/hardware-design/hardware-interface
- Overlay sources (all carry `compatible = ... "radxa,zero3"` and spell out the Zero 3 pin numbers in the description, e.g. UART4-M1 "On Radxa ZERO 3 this is RX pin 16 & TX pin 18"): https://github.com/radxa/overlays/tree/main/arch/arm64/boot/dts/rockchip/overlays (files `rk3568-uart3-m0.dts`, `rk3568-uart4-m1.dts`, `rk3568-uart5-m1.dts`, `rk3568-uart9-m1.dts`)
- Enable: `sudo rsetup` -> Overlays -> Manage overlays -> tick "Enable UARTx-Mx" -> reboot. https://docs.radxa.com/en/zero/zero3/radxa-os/rsetup
- Linux device names: `/dev/ttySn` with n = UART number (`/dev/ttyS3`, `/dev/ttyS4`, `/dev/ttyS5`, `/dev/ttyS9`); the mraa docs use `/dev/ttyS4`, a forum user wrote to `/dev/ttyS3` from a shell. https://docs.radxa.com/en/zero/zero3/app-development/mraa , https://forum.radxa.com/t/radxa-zero-3w-uart-tx-doesnt-work/27750
- Avoid UART2 (pins 8/10): it is the U-Boot/kernel console at 1500000n8 and the FIQ debugger; the docs say "not recommended for general use" and a user could not reclaim it on Armbian/DietPi/Bullseye. https://docs.radxa.com/en/zero/zero3/low-level-dev/serial , https://forum.radxa.com/t/uart-2-on-radxa-zero-3w/29765
- Known trap: UART2/UART3 "RX works, TX doesn't" reports (Jul 2025) on official, Armbian and DietPi images turned out to be minicom hardware flow control; Radxa staff: "You need close the Flow Ctrl option". Set `rtscts=False` in pyserial. https://forum.radxa.com/t/radxa-zero-3w-uart-tx-doesnt-work/27750

**Maximum baud / 1,000,000 bps.** The UARTs are Synopsys DesignWare APB UARTs (`compatible = "rockchip,rk3568-uart", "snps,dw-apb-uart"`, `clocks = <&cru SCLK_UARTn>` named `baudclk`). The Linux `8250_dw` driver re-programs `baudclk` to exactly `baud * 16` on every `set_termios` (`clk_round_rate`/`clk_set_rate(d->clk, newrate)`), and Rockchip's CRU derives SCLK_UART from the PLLs through fractional dividers, so 1,000,000 bps is produced with no divisor error. The board already runs its console at 1,500,000 bps out of the box, which is above the 1 Mbps needed. Open Duck Mini v2 itself talks Feetech at 1,000,000 baud (via USB adapter) so protocol speed is proven.
- https://github.com/torvalds/linux/blob/v6.1/arch/arm64/boot/dts/rockchip/rk356x.dtsi (uart3 node)
- https://github.com/torvalds/linux/blob/v6.1/drivers/tty/serial/8250/8250_dw.c (`dw8250_set_termios`)
- https://docs.radxa.com/en/zero/zero3/radxa-os/uart (1500000 default)
- Caveat: no forum post was found of someone running a Zero 3W header UART at exactly 1 Mbps with bus servos; the 921600-baud corruption thread is about the Amlogic Radxa Zero, not the 3W. Verify with a loopback and `python3 -m serial.tools.miniterm` before building.

**Levels.** All header GPIO is 3.3 V, absolute max 3.63 V. The Waveshare Bus Servo Adapter (A) does the TTL half-duplex merge on-board and takes 3.3 V TX/RX, so no level shifter. Do not back-feed servo battery voltage into the header. https://docs.radxa.com/en/zero/zero3/hardware-design/hardware-interface

## 3. PWM, I2C, SPI

**Hardware PWM on the header** (brief: "up to 6 x PWM"):

| PWM | Pin | Shares with | Overlay |
|---|---|---|---|
| PWM14_M0 | 7 | - | `rk3568-pwm14-m0` ("On Radxa ZERO 3 this is pin 7") |
| PWM8_M0 | 16 | UART4_RX_M1 | `rk3568-pwm8-m0` |
| PWM9_M0 | 18 | UART4_TX_M1 | `rk3568-pwm9-m0` |
| PWM15_IR_M1 | 19 | SPI3_MOSI_M1 | `rk3568-pwm15-m1` |
| PWM12_M1 | 21 | SPI3_MISO_M1, UART9_TX | `rk3568-pwm12-m1` |
| PWM14_M1 | 23 | SPI3_CLK_M1 | `rk3568-pwm14-m1` |
| PWM13_M1 | 24 | SPI3_CS0_M1, UART9_RX | `rk3568-pwm13-m1` |

- https://docs.radxa.com/en/zero/zero3/hardware-design/hardware-interface ; overlay files under https://github.com/radxa/overlays/tree/main/arch/arm64/boot/dts/rockchip/overlays
- Using it from Linux: after enabling the overlays each PWM controller appears as `/sys/class/pwm/pwmchipN` (a user saw pwmchip0-5 with seven PWM overlays on). Standard sysfs: `echo 0 > pwmchipN/export; echo 20000000 > pwm0/period; echo 1500000 > pwm0/duty_cycle; echo 1 > pwm0/enable` (SG90: 50 Hz, 1-2 ms). Chip numbers are assigned dynamically on the 6.1 kernel, so map them by `cat /sys/class/pwm/pwmchipN/device/of_node/name` or `/sys/kernel/debug/pwm` at boot and don't hard-code.
- mraa PWM is broken on 6.1: Radxa docs and staff both say "Due to changes in the pwmchip driver, the PWM function of the MRAA does not work properly on the 6.1 kernel." mraa GPIO/I2C/SPI/UART still work (`sudo apt install libmraa2 libmraa-dev python3-mraa mraa-tools`).
  - https://docs.radxa.com/en/zero/zero3/app-development/mraa
  - https://forum.radxa.com/t/solved-zero-3e-pwm-gpio-under-kernel-6-1-ubuntu/26423
- python-periphery (`PWM(chip, channel)`) is what the forum user got working on 6.1 instead of mraa; it is a thin wrapper over the same sysfs so it's the recommended Python route. gpiod (`python3-libgpiod`) is documented for GPIO; Rockchip naming GPIO3_C4 -> gpiochip3 line 20. https://docs.radxa.com/en/zero/zero3/app-development/gpiod
- Adafruit Blinka's generic rk3566 pin map only declares PWM0/PWM1 in `pwmOuts`, so `pwmio` on Blinka should be considered unsupported for header pins; Blinka's Zero 3 board file does label `PWM8 = D3_B1`, `PWM9 = D3_B2` but that's pin naming, not a working PWMOut.

**I2C** (brief: "up to 2 x I2C"):

| Bus | Pins (SDA / SCL) | Overlay | Notes |
|---|---|---|---|
| I2C3_M0 | 3 / 5 | `rk3568-i2c3-m0` ("On Radxa ZERO 3 this is SDA pin 3 and SCL pin 5") | onboard pull-ups present; excludes UART3 |
| I2C4_M0 | 27 / 28 | `rk3568-i2c4-m0` | onboard pull-ups present; a Zero 3W user enabled "I2C4-M0" in rsetup and saw `/dev/i2c-4` |
| I2C5_M0 | 31 / 29 | (not in overlay repo) | listed on hardware-interface page; no overlay found |

- https://docs.radxa.com/en/zero/zero3/hardware-design/hardware-interface ("Pin 3, Pin 5, Pin 27, and Pin 28 add extra pull-up resistors for I2C device power supply, so they work abnormally when used as GPIOs")
- https://github.com/radxa/overlays/blob/main/arch/arm64/boot/dts/rockchip/overlays/rk3568-i2c3-m0.dts
- https://forum.radxa.com/t/activating-pins-27-and-28-for-i2c-communication-on-radxa-zero-3w/28808
- Device names follow the bus number: `/dev/i2c-3`, `/dev/i2c-4`. Check `i2cdetect -l`; one Armbian user reported I2C3 "occupied by kernel default" so verify on the actual image.
- 400 kHz: neither the rk356x.dtsi `i2c3` node nor the Radxa overlay sets `clock-frequency`, so the rk3x-i2c driver defaults to 100 kHz. To run at 400 kHz write a 10-line overlay (`&i2c3 { status = "okay"; clock-frequency = <400000>; pinctrl-0 = <&i2c3m0_xfer>; };`), compile with `dtc`, and load via rsetup -> Overlays -> "Install 3rd party overlay". The rsetup page documents exactly this flow for a user LED overlay. https://docs.radxa.com/en/zero/zero3/radxa-os/rsetup
- BNO085 at 100 Hz needs clock stretching; the Rockchip rk3x I2C controller is a full master that honours SCL stretching (unlike the BCM2835 bug), but no Zero 3W + BNO08x report was found. Open question; test early.

**SPI** (brief: "1 x SPI bus"): SPI3_M1 on pins 19 (MOSI), 21 (MISO), 23 (CLK), 24 (CS0), 26 (CS1 per brief; hardware-interface page lists 26 as NC). Overlay files in the repo are `rk3568-spi3-m0-cs0-spidev.dts` (M0 is the ROCK 3 pinmux, not the Zero 3), so a Zero 3-specific `spi3-m1` spidev overlay may need to be written; the mraa docs' SPI example uses spidev0.0 on another board. Treat SPI as "possible with a custom overlay"; prefer I2C for the VL53L8CX unless you need the 8x8 @ 60 Hz mode that only SPI can sustain.
- https://docs.radxa.com/en/zero/zero3/hardware-design/hardware-interface

**Proposed conflict-free pin plan for the Duck:**
- Servo bus (Waveshare adapter): UART5_M1, pins 32 (TX) / 33 (RX) -> `/dev/ttyS5` (leaves UART4 pins free for PWM). Fallback: UART4_M1 pins 16/18 if the uart5-m1 overlay doesn't list zero3 in its compatible (not verified).
- BNO085 + VL53L8CX: I2C3_M0 pins 3/5 (`/dev/i2c-3`, pull-ups already on board) at 400 kHz via custom overlay; or split across I2C3 and I2C4 (pins 27/28) if the ToF's long transactions starve the IMU.
- SG90 x2: PWM8_M0 pin 16 and PWM9_M0 pin 18 (or PWM14_M0 pin 7 + one of them).
- Camera: CSI connector, overlay `radxa-zero3-rpi-camera-v2`.
- Spare: SPI3_M1 (19/21/23/24) for ToF over SPI later.

## 4. Power

- Input: 5 V only, through USB-C 1 (the USB 2.0 OTG port), or 5 V on header pins 2 and 4 (product brief §5.1 lists "5V Power from the GPIO PIN 2 & 4" as a supported input). Supplies above 5 V "may damage the device". https://dl2.radxa.com/zero3/docs/hw/3w/radxa_zero_3w_product_brief.pdf , https://docs.radxa.com/en/zero/zero3/faq
- Adapter rating: docs say 5 V/2 A minimum (brief rev 1.8 changed this from 1 A); the FAQ goes further and recommends "at least 15W" and the Radxa PD30W. https://docs.radxa.com/en/zero/zero3/getting-started/preparation
- Measured draw (Zero 3W review, 5 V/2.5 A supply): just under 3 W booted/idle with desktop, ~4 W with all four cores at 100 %. Armbian user: ~0.3 A idle, ~0.6 A full CPU with Wi-Fi on. Radxa wiki figure for the older Zero: 3.3 W max without USB peripherals. Budget 1.0 A continuous, 1.5 A peak for the board + IMX219 (~0.25 W) + Wi-Fi bursts, and give it its own 5 V/3 A buck off the servo battery.
  - https://magazinmehatronika.com/radxa-zero-3w-recenzija
  - https://forum.armbian.com/topic/24184-energy-consumption/
  - https://forum.radxa.com/t/energy-consumption/12404
- Thermals: brief rates 0-50 °C ambient and relies on DVFS throttling. Review: SoC hits 80 °C within ~2 minutes at full load with no heatsink and throttles; stays under 60 °C at light load. Forum: idle ~44 °C with a Waveshare Zero-HEATSINK, 72-85 °C under load before. Radxa sells a dedicated heatsink (5519A, ₹354 at Hubtronics, out of stock). A heatsink is required for a sustained 50 Hz loop plus camera.
  - https://forum.radxa.com/t/zero-3w-running-hot/19851
- Brownout: no Zero 3W-specific undervoltage/reboot thread found. One older Radxa Zero reset problem traced to a 500 mA USB-C charger module. A Zero 3W boot-hang on "mmc1: delay init for 600 ms to enable UHS mode" is SD-card related, not power. https://forum.radxa.com/t/radxa-burning-like-hell/19081
- USB 3.0 host port is limited to 500 mA (brief §6.2), relevant if you hang the servo adapter off USB instead of the header UART.

## 5. Mechanical

- Board 65 x 30 mm (spec table). https://docs.radxa.com/en/zero/zero3
- Mounting holes, extracted from Radxa's official 2D DXF (`radxa_zero_3w_v1110_top.dxf`, layer PIN_TOP): four Ø2.82 mm holes at (3.55, 3.6), (61.4, 3.6), (3.6, 26.45), (61.4, 26.5) mm -> 57.85 x 22.9 mm pattern, 3.6 mm from the edges. Raspberry Pi Zero 2 W: 65 x 30 mm, Ø2.75 mm holes on 58 x 23 mm, 3.5 mm inset. Within 0.15 mm, so any Pi Zero mount, standoff set or case plate fits. DXF: https://dl.radxa.com/zero3/docs/hw/3w/radxa_zero_3w_2d_dxf.zip (STP: https://dl.radxa.com/zero3/docs/hw/3w/radxa_zero_3w_3d_stp.zip)
- Header: standard 40-pin, same edge and orientation as the Pi Zero (sold with or without a soldered colour-coded female/male header depending on SKU). Camera FPC is at the short edge like the Pi Zero. Both USB-C ports and micro-HDMI are on the long edge opposite the header.
- Antenna: onboard PCB antenna by default; a U.FL (IPEX MHF1) connector for an external antenna, switched with the `radxa-zero3-external-antenna` overlay in rsetup. Metal chassis around the robot's head will attenuate Wi-Fi, so plan for the U.FL pigtail. https://docs.radxa.com/en/zero/zero3/accessories/zero3w-antenna
- Z-height differences vs Pi Zero 2W: two USB-C instead of two micro-USB, U.FL connector, and the heatsink. The Waveshare Zero-HEATSINK fits but "sits on the USB ports" and the bundled screws were too short (forum).

## 6. Software

- Official image: `radxa-zero3_bookworm_kde_b1` (Debian 12, Linux 6.1, released 2025-07-15, announced 2026-01-24 as the recommended image). Older: `radxa-zero3_debian_bullseye_xfce_b6` / `_cli_b6` and Ubuntu jammy b6 (5.10 kernel, Jan 2024). Third-party: Armbian 26.8.1 (Debian 13 / Ubuntu 26.04, vendor kernel 6.1.115 or mainline 6.18), DietPi Bookworm, OpenWrt 25.12.
  - https://docs.radxa.com/en/zero/zero3/download
  - https://github.com/radxa-build/radxa-zero3/releases
  - https://forum.radxa.com/t/release-announcement-debian-12-with-linux-6-1-for-the-rk3399-rk356x-series/30172
  - https://www.armbian.com/radxa-zero-3/
- There is no CLI-only Bookworm image from Radxa (the b1 is KDE; a user asked for CLI in the announcement thread). Use the Armbian Debian 13 minimal (vendor 6.1.115) or strip the KDE image. The rsetup/overlay tooling is Radxa-OS only; Armbian uses `armbian-config` with the same `rk3568-*` overlay names (user listed `pwm12-m1 pwm13-m1 pwm14-m0 ...`).
- Python: Debian 12 ships Python 3.11 (Debian 13: 3.13). Radxa documents venv use: https://docs.radxa.com/en/zero/zero3/app-development/venv-usage
- onnxruntime: PyPI 1.31.1 (2026-10-26) ships `cp311-manylinux_2_28_aarch64` wheels (also cp312/313/314); Bookworm's glibc 2.36 satisfies manylinux_2_28, so `pip install onnxruntime` just works. Open Duck pins `onnxruntime==1.18.1`, which also had aarch64 wheels. Radxa's own AI docs for the Zero 3 are RKNN (NPU) based; the RK3566's 0.8 TOPS NPU is irrelevant for a tiny MLP policy. https://pypi.org/project/onnxruntime/
- Adafruit Blinka: board file `src/adafruit_blinka/board/radxa/radxazero3.py` exists ("Radxa ZERO 3 pin definitions"). It maps `SDA = D1_A0` (pin 3), `SCL = D1_A1` (pin 5) -> I2C3; `SCLK/MOSI/MISO/CE0` -> SPI3_M1 pins 23/19/21/24; `TX/RX` -> UART2 pins 8/10 (the console; override with your own `serial.Serial`); `UART4_TX/RX = D3_B2/D3_B1`; `PWM8/PWM9` names only. The circuitpython.org board page lists the Zero 3W. So `adafruit-circuitpython-bno08x` (BNO085) will work over `busio.I2C()` after the I2C3 overlay is enabled; `adafruit_extended_bus.ExtendedI2C(4)` reaches I2C4. Blinka PWM is not usable on this board (see §3).
  - https://github.com/adafruit/Adafruit_Blinka/blob/main/src/adafruit_blinka/board/radxa/radxazero3.py
  - https://circuitpython.org/blinka/radxa_zero_3w/
- Alternatives without Blinka: `smbus2` (pure Python, works on any `/dev/i2c-N`) plus a pure-Python SH-2 (BNO08x) parser; VL53L8CX via `pip3 install circuitpython-vl53lxcx` (senseBox driver, covers L5CX and L8CX, Blinka-compatible, needs the sensor firmware .bin) or ST's STSW-IMG042 Linux C driver ("validated on Raspberry Pi 3") wrapped with ctypes.
  - https://circuitpython-vl53lxcx.readthedocs.io
  - https://www.st.com/en/embedded-software/stsw-img042.html
- Real-time: default governor on the Radxa kernel is `ondemand`, available `performance`/`schedutil`, OPPs 408 MHz-1.416 GHz (the 1.6/1.8 GHz OPP is disabled in the driver; overclocking requires a patched DTB). Frequency-switch latency 149 µs. Set `performance` and pin the control loop to one core with `taskset`/`isolcpus=3` in `/etc/kernel/cmdline` (Radxa boot-param docs). No PREEMPT_RT build is offered. A 50 Hz loop with a small MLP is tens of microseconds of compute; the jitter risk is the Python camera thread and Wi-Fi interrupts, not the CPU.
  - https://forum.radxa.com/t/zero-3w-running-hot/19851
  - https://forum.radxa.com/t/overclock-raxda-zero-3w/24483
  - https://docs.radxa.com/en/zero/zero3/os-config/bootparam
- Open Duck Mini v2 runtime facts (for porting): `v2_rl_walk_mujoco.py` defaults `control_freq=50`, `serial_port="/dev/ttyACM0"`; `OnnxInfer` uses `providers=["CPUExecutionProvider"]`; `rustypot.feetech(usb_port, 1000000)`; IMU is `adafruit_bno055.BNO055_I2C(busio.I2C(board.SCL, board.SDA))` sampled at control_freq/2; deps `onnxruntime==1.18.1 numpy==1.26.4 scipy adafruit-circuitpython-bno055 pygame adafruit_extended_bus pypot@support-feetech-sts3215`. README: "only tested on the Raspberry Pi Zero 2W", with Pi 5 notes (replace RPi.GPIO with lgpio). On the Zero 3W the only changes are `board.SCL/SDA` (already I2C3) and the serial port (`/dev/ttyS5` or `/dev/ttyACM0` if you keep the USB adapter).
  - https://github.com/apirrone/Open_Duck_Mini_Runtime

## 7. Availability for India (checked 2026-10-28)

| Seller | Zero 3W | Zero 3E | Notes |
|---|---|---|---|
| Arace (HK) https://arace.tech/products/radxa-zero-3w | all 12 SKUs SOLD OUT (list: 1 GB $20-32.9, 2 GB/16 GB $29.99-30.99, 4 GB $29.99-30.99, 4 GB/32 GB $44.99-50.99, 8 GB $50.99-65.99) | all 4 SKUs SOLD OUT ($32.9/39.99/30.99/50.99) | Ships DDU from Hong Kong in 3-7 business days; buyer pays Indian duties. https://arace.tech/policies/shipping-policy |
| Allnet.de https://shop-en.allnet.de/Products/Makerspace/Development-boards/Rock-Radxa/Radxa-Zero-3W | not in stock | - | allnetchina.cn blocks scripted access; could not verify |
| AliExpress | Radxa Computer (Shenzhen) store item 3256807428419499 showed $44.89 (4 GB/32 GB); third-party listings $94-159 are scalpers | 2 GB $20.97 / 4 GB $30.97 reported by CNX (dated) | https://www.aliexpress.us/item/3256807428419499.html ; verify live |
| Hubtronics (Bengaluru) | **2 GB / no eMMC / with header: IN STOCK, 11 units, ₹5,760 incl. GST** https://hubtronics.in/radxa-zero-3w-2gbram ; 4 GB ₹4,575 OOS; 4 GB/32 GB ₹6,099 OOS; 2 GB/16 GB ₹3,699 OOS; 1 GB ₹3,599/₹2,030 OOS | 1 GB ₹3,099 / 2 GB ₹2,575 / 4 GB ₹3,635 / 8 GB ₹6,090, all OOS | Heatsink 5519A ₹354 OOS |
| ThinkRobotics | all 16 variants SOLD OUT / pre-order (₹2,650-11,550) https://thinkrobotics.com/products/radxa-zero-3w | - | |
| Amazon.in, robu.in, Mouser.in, DigiKey.in | no Zero 3W listing found | - | Mouser/DigiKey do not stock Radxa SBCs |

- Shortage context: forum "Is Radxa Zero 3w (with eMMC) being phased out?" (Dec 2025-Feb 2026: eMMC variants vanished, a distributor said "don't expect any more", no Radxa reply); "Radxa restock or availability info" (Mar-Apr 2026: Zero 3E out of stock at Robodo, Evelta, Hubtronics, Arace, AllNet). Product brief rev 1.12 (2026-09-20) §8 still states availability "until a minimum date of September 2030".
  - https://forum.radxa.com/t/is-radxa-zero-3w-with-emmc-being-phased-out/29939
  - https://forum.radxa.com/t/radxa-restock-or-availability-info/30478
- Import cost for a ~$30 board shipped to Vadodara: a personal courier import is assessed under CTH 9804 at 10 % BCD + 10 % SWS on BCD + 18 % IGST (IGST on personal imports dropped from 28 % to 18 % on 22 Sep 2025; Budget 2026 cut BCD to 10 %), i.e. ~31 % of CIF, charged from the first rupee, plus the courier's clearance fee (DHL/FedEx typically ₹500-1,000). A commercial import under HS 8471 would be 0 % BCD + 18 % IGST but requires an IEC/GST invoice. Expect $30 + ~$15 shipping -> ~₹3,800 + ~₹1,200 duty + courier fee ≈ ₹5,500 landed and 1-3 weeks. That is the same as Hubtronics' in-stock price, so buy local.
  - https://www.refurb.me/import-costs/india , https://eximpe.com/hsncode-finder/84715000
- Zero 3E as a substitute: identical SoC/RAM/header/CSI, swaps Wi-Fi/BT and eMMC for Gigabit Ethernet + PoE (no wireless at all, so you'd add a USB Wi-Fi dongle on the single USB host port). Same overlays (`radxa,zero3` compatible). Also sold out everywhere checked. https://docs.radxa.com/en/zero/zero3

## 8. Fallbacks

**Raspberry Pi Zero 2 W** (₹1,549-1,709 at robu.in, in stock; 512 MB, 4x A53 @ 1 GHz).
- It is the reference platform: the Open Duck Mini v2 runtime image "is currently only tested on the Raspberry Pi Zero 2W", runs the 50 Hz ONNX loop with onnxruntime's CPU provider, Feetech at 1 Mbps and a BNO055 over Blinka. So policy + servo bus + IMU is proven. No published numbers on CPU headroom were found; the project's camera module (`camera.py`) exists in the runtime but the Open Duck Mini README lists camera/"expression" features as "still missing", so nobody has shown camera + policy on the Zero 2W. With 512 MB and a 1 GHz A53, a Picamera2/libcamera pipeline plus Python policy is feasible at low resolution (e.g. 640x480 @ 15-30 fps) but will need `isolcpus` and no desktop. The Pi Zero 2 W has libcamera/IMX219 fully supported, hardware PWM on GPIO12/13/18/19, I2C clock-stretching bug (BNO085 needs the software I2C or UART-RVC mode), and only one usable header UART (PL011 ttyAMA0 at 1 Mbps works; the mini-UART is unreliable).
  - https://github.com/apirrone/Open_Duck_Mini_Runtime
  - https://github.com/apirrone/Open_Duck_Mini
  - https://robu.in/?p=1124637
- Pi Zero 2 W uses the same 22-pin 0.5 mm camera connector as the Zero 3W, so the cable is shared.

**Raspberry Pi 5** (4 GB ≈ ₹5,500-6,200 in India per ThinkRobotics guide; 85 x 56 mm).
- 3.0 W idle headless, ~8.8 W all-core stress, up to ~16 W with USB/4K load; needs a 5 V/5 A PD supply or the USB ports are limited to 600 mA. Too big for the Duck head/torso cavity designed around 65 x 30 mm, and 3-4x the Zero 3W's power. Open Duck README already includes Pi 5 notes (lgpio instead of RPi.GPIO), and a Taiwan meetup listing shows a v2 built on a Pi 5, so software-wise it is the easiest fallback if the frame can be adapted.
  - https://raspberry.tips/en/faq/raspberry-pi-power-consumption-update-2026-all-models-compared
  - https://thinkrobotics.com/blogs/product-reviews-buying-guides/raspberry-pi-5-price-india-complete-cost-analysis-and-buying-guide

**Other Pi-Zero-footprint boards with 2-4 GB RAM:**
- Orange Pi Zero 2W (Allwinner H618, 1-4 GB, $13-24 on AliExpress, Indian resellers list it): no camera interface; the 24-pin FPC at the camera position is a "function" connector for the expansion board. Not usable for the IMX219. https://www.cnx-software.com/2023/09/09/orange-pi-zero-2w-raspberry-pi-zero-2w-alternative-4gb-ram/
- Banana Pi BPI-M4 Zero (H618, 2-4 GB): the 24-pin connector is now a "Misc" connector (USB 2.0, Fast Ethernet); no MIPI CSI. https://www.cnx-software.com/2023/12/12/banana-pi-bpi-m4-zero-allwinner-h618-sbc-raspberry-pi-zero-2-w/
- Luckfox Lyra Zero W (RK3506B, 3x A7 @ 1.2 GHz, 512 MB) - too little CPU/RAM and the camera input is on the Lyra Pico Zero variant. https://liliputing.com/luckfox-lyra-zero-boards-feature-npu-or-cortex-m-co-processor-options-sell-for-under-20/
- Radxa Zero 3E (see §7) is the only true Pi-Zero-footprint board with 2-4 GB and a working CSI port besides the 3W, and it is also sold out.
- Conclusion: there is no in-stock Indian alternative that gives Pi-Zero footprint + >=2 GB + MIPI CSI. The realistic choices are (a) the single in-stock Zero 3W 2 GB at Hubtronics, (b) Zero 2 W now and accept 512 MB, (c) Pi 5 / Pi 4 with a redesigned electronics bay.

## Open questions to settle on the bench

1. Does `rk3568-uart5-m1` list `radxa,zero3` in its compatible (so pins 32/33 can carry the servo bus and free pins 16/18 for PWM8/9)? If not, use UART4_M1 for servos and PWM14_M0 (pin 7) + PWM15_M1 (pin 19) for the SG90s.
2. BNO085 I2C clock stretching on the rk3x controller at 400 kHz - untested on this board.
3. Camera on the 6.1 Bookworm image: the only confirmed working reports are on 5.10; expect to run `rkaiq_3A_server` manually and possibly fall back to the Bullseye b6 image.
4. Check the FPC connector orientation on the specific unit received (V1.12 defect).
5. Confirm with Hubtronics that the 11 units are physically in stock before paying ₹5,760.
