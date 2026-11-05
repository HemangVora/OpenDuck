#!/usr/bin/env python3
"""Configure Feetech/Waveshare ST/STS bus servos (ST3215-HS 12 V) one at a time, Open Duck Mini v2 IDs.

Does what upstream Open_Duck_Mini_Runtime/scripts/configure_motor.py does (mode 0, acceleration 0,
max acceleration 0, P/I/D = 32/0/0, new ID, move to zero = 2048), plus 12 V safety checks:
refuses to run with more than one servo on the bus, and reads the supply voltage and the
voltage-limit registers before touching anything.

Usage (from OpenDuck/tools):
  .venv/bin/python servo_setup.py ports                 # list serial ports
  .venv/bin/python servo_setup.py scan                  # find servos on the bus
  .venv/bin/python servo_setup.py info  --id 1          # dump the key registers
  .venv/bin/python servo_setup.py setup left_knee       # configure the ONE servo on the bus as left_knee (ID 23)
  .venv/bin/python servo_setup.py setup 23              # same, by number
  .venv/bin/python servo_setup.py center --id 23        # move to 2048 again (for fitting the horn)
  .venv/bin/python servo_setup.py relax  --id 23        # torque off
Add --port /dev/cu.xxx if auto-detect picks the wrong port.
"""
import argparse, glob, sys, time
import serial

IDS = {
    "right_hip_yaw": 10, "right_hip_roll": 11, "right_hip_pitch": 12, "right_knee": 13, "right_ankle": 14,
    "left_hip_yaw": 20, "left_hip_roll": 21, "left_hip_pitch": 22, "left_knee": 23, "left_ankle": 24,
    "neck_pitch": 30, "head_pitch": 31, "head_yaw": 32, "head_roll": 33,
}
NAMES = {v: k for k, v in IDS.items()}

# STS register map (same addresses as pypot.feetech.sts3215_io)
R = dict(model=(3, 2), id=(5, 1), baud=(6, 1), min_angle=(9, 2), max_angle=(11, 2), max_temp=(13, 1),
         max_volt=(14, 1), min_volt=(15, 1), max_torque=(16, 2), P=(21, 1), D=(22, 1), I=(23, 1),
         offset=(31, 2), mode=(33, 1), torque_enable=(40, 1), acc=(41, 1), goal=(42, 2), lock=(55, 1),
         pos=(56, 2), speed=(58, 2), load=(60, 2), volt=(62, 1), temp=(63, 1), status=(65, 1),
         current=(69, 2), max_acc=(85, 1))
PING, READ, WRITE = 1, 2, 3
CENTER = 2048


class Bus:
    def __init__(self, port, baud=1_000_000):
        self.s = serial.Serial(port, baud, timeout=0.02)

    def _tx(self, sid, instr, params=b""):
        body = bytes([sid, len(params) + 2, instr]) + params
        self.s.reset_input_buffer()
        self.s.write(b"\xff\xff" + body + bytes([(~sum(body)) & 0xFF]))

    def _rx(self, sid):
        t0 = time.time(); buf = b""
        while time.time() - t0 < 0.05:
            buf += self.s.read(64)
            i = buf.find(b"\xff\xff")
            if i >= 0 and len(buf) >= i + 4:
                n = buf[i + 3]
                if len(buf) >= i + 4 + n:
                    pkt = buf[i + 2:i + 4 + n]          # id len err params chk
                    if (~sum(pkt[:-1])) & 0xFF != pkt[-1]:
                        raise IOError("bad checksum")
                    if pkt[0] != sid:
                        raise IOError(f"reply from id {pkt[0]}, expected {sid}")
                    return pkt[2], pkt[3:-1]
        return None

    def ping(self, sid):
        self._tx(sid, PING)
        try:
            return self._rx(sid) is not None
        except IOError:
            return True   # something answered (garbled): still counts as present

    def read(self, sid, reg):
        addr, n = R[reg]
        for _ in range(3):
            self._tx(sid, READ, bytes([addr, n]))
            r = self._rx(sid)
            if r:
                v = int.from_bytes(r[1][:n], "little")
                if reg in ("pos", "speed", "load", "current") and v & 0x8000:
                    v = -(v & 0x7FFF)
                return v
        raise IOError(f"no reply reading {reg} from id {sid}")

    def write(self, sid, reg, val):
        addr, n = R[reg]
        self._tx(sid, WRITE, bytes([addr]) + int(val).to_bytes(n, "little"))
        if sid != 0xFE:
            r = self._rx(sid)
            if r is None:
                raise IOError(f"no ack writing {reg} to id {sid}")
            if r[0]:
                print(f"  (status bits 0x{r[0]:02x} after writing {reg})")

    def scan(self, ids=range(0, 254)):
        return [i for i in ids if self.ping(i)]


def find_port():
    c = sorted(set(glob.glob("/dev/cu.usbmodem*") + glob.glob("/dev/cu.wchusbserial*") + glob.glob("/dev/cu.usbserial*")
                   + glob.glob("/dev/ttyACM*") + glob.glob("/dev/ttyUSB*")))
    if not c:
        sys.exit("No USB serial port found. Check the USB-C cable (must be a data cable) and the adapter jumper (USB / A).")
    if len(c) > 1:
        print(f"Several ports {c}; using {c[0]} (pass --port to choose)")
    return c[0]


def info(b, sid):
    v = {k: b.read(sid, k) for k in ("model", "id", "baud", "volt", "min_volt", "max_volt", "temp", "max_temp",
                                       "mode", "P", "I", "D", "acc", "max_acc", "max_torque", "min_angle", "max_angle",
                                       "offset", "lock", "torque_enable", "pos", "status")}
    print(f"id {sid} ({NAMES.get(sid, 'unassigned')}): model {v['model']}, firmware baud index {v['baud']}")
    print(f"  supply {v['volt']/10:.1f} V   limits {v['min_volt']/10:.1f}..{v['max_volt']/10:.1f} V   temp {v['temp']} C (max {v['max_temp']})")
    print(f"  mode {v['mode']}  P/I/D {v['P']}/{v['I']}/{v['D']}  acc {v['acc']}  max_acc {v['max_acc']}  max_torque {v['max_torque']}")
    print(f"  angle limits {v['min_angle']}..{v['max_angle']}  offset {v['offset']}  lock {v['lock']}  torque {v['torque_enable']}  position {v['pos']}  status 0x{v['status']:02x}")
    return v


def check_voltage(v):
    ok = True
    if v["volt"] > v["max_volt"]:
        print(f"!! Supply {v['volt']/10:.1f} V is ABOVE this servo's max-voltage limit {v['max_volt']/10:.1f} V: it will refuse torque.")
        print("   Wrong servo variant (7.4 V?) or wrong supply. Stop and check before continuing.")
        ok = False
    if v["volt"] < v["min_volt"]:
        print(f"!! Supply {v['volt']/10:.1f} V is BELOW the min-voltage limit {v['min_volt']/10:.1f} V. Check the supply.")
        ok = False
    if v["volt"] > 126:
        print(f"!! Supply {v['volt']/10:.1f} V is above 12.6 V. Use a 12 V supply or a 3S pack, nothing higher.")
        ok = False
    return ok


def setup(b, target):
    found = b.scan()
    if not found:
        sys.exit("No servo answers. Check 12 V power, the 3-pin cable, and the adapter jumper.")
    if len(found) > 1:
        sys.exit(f"Found {len(found)} servos {found}. Connect ONE servo at a time (new servos all share ID 1).")
    cur = found[0]
    print(f"Found one servo at id {cur}")
    v = info(b, cur)
    if not check_voltage(v):
        sys.exit("Not configuring. Fix the voltage problem first.")
    b.write(cur, "torque_enable", 0)
    b.write(cur, "lock", 0)                 # unlock EEPROM
    b.write(cur, "mode", 0)                 # position mode
    b.write(cur, "max_acc", 0)
    b.write(cur, "acc", 0)
    b.write(cur, "P", 32); b.write(cur, "I", 0); b.write(cur, "D", 0)   # upstream configure_motor.py values
    if cur != target:
        b.write(cur, "id", target)          # reply comes from the old id
        time.sleep(0.05)
    if not b.ping(target):
        sys.exit(f"Servo does not answer at the new id {target}. Run scan.")
    b.write(target, "lock", 1)              # relock EEPROM
    time.sleep(0.05)
    v2 = info(b, target)
    bad = [k for k, want in (("id", target), ("mode", 0), ("P", 32), ("I", 0), ("D", 0), ("acc", 0), ("max_acc", 0)) if v2[k] != want]
    if bad:
        sys.exit(f"Readback mismatch on {bad}. Run setup again.")
    center(b, target)
    print(f"\nDONE: id {target} = {NAMES.get(target, '?')}. Label it, then fit the horn (servo holds 2048).")


def center(b, sid):
    b.write(sid, "torque_enable", 1)
    b.write(sid, "goal", CENTER)
    time.sleep(1.0)
    p = b.read(sid, "pos")
    print(f"id {sid}: holding at {p} (target {CENTER}, error {p - CENTER} steps = {(p - CENTER) * 360 / 4096:.1f} deg)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["ports", "scan", "info", "setup", "center", "relax"])
    ap.add_argument("target", nargs="?", help="for setup: joint name or id")
    ap.add_argument("--id", type=int, default=None)
    ap.add_argument("--port", default=None)
    a = ap.parse_args()
    if a.cmd == "ports":
        print("\n".join(sorted(glob.glob("/dev/cu.*") + glob.glob("/dev/tty[AU]*")))); return
    b = Bus(a.port or find_port())
    if a.cmd == "scan":
        f = b.scan(); print(f"servos found: {[(i, NAMES.get(i, 'unassigned')) for i in f] or 'none'}")
        for i in f: print(f"  id {i}: {b.read(i, 'volt')/10:.1f} V, position {b.read(i, 'pos')}")
    elif a.cmd == "info":
        check_voltage(info(b, a.id if a.id is not None else 1))
    elif a.cmd == "setup":
        if not a.target: sys.exit(f"setup needs a joint name or id: {IDS}")
        t = IDS.get(a.target)
        t = t if t is not None else int(a.target)
        setup(b, t)
    elif a.cmd == "center":
        center(b, a.id)
    elif a.cmd == "relax":
        b.write(a.id, "torque_enable", 0); print(f"id {a.id}: torque off")


if __name__ == "__main__":
    main()
