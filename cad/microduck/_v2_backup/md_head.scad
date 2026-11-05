// =====================================================================
//  HEAD  (rides on head_assembly: stock head_roll_mount + roll servo)
//  head_shell  white  - Microduck loaf cap with the recessed face built in
//  head_tray   black  - floor band, rear and sides (the stripe under the cap)
//  head_jaw    black  - lower beak, pivots on an SG90 (right) and an M3 pin (left)
//  eye_bezel   black  - eye ring around the camera lens and ToF window
//  head_chassis black - hidden plate on the roll mount: Radxa, buck, camera,
//                        ToF, SG90 and pivot brackets
// =====================================================================

Z_BAND   = 136;     // white cap above, black band + jaw below (Microduck band top at 1.7x = 136.9)
Z_BOT    = 109.7;   // head bottom = stock head_bot_sheet bottom
Z_FLOOR  = 112.7;   // tray floor top
T_H      = 2.6;     // cap wall
FACE_X0  = 105.3;   // face wall back
FACE_X1  = 107.8;   // face wall front
EYE_C    = [0, 163.4];          // lens centre (y, z)
EYE_OD   = 50;  EYE_HOLE = 32.5;
FACE_SCREWS = [[19, 163.4], [-19, 163.4]];
TOF_C    = [0, 180.5];          // ToF window centre (y, z), inside the eye ring
JAW_P    = [20, 146];           // jaw pivot (x, z), axis along y
JAW_OPEN = 15;                  // max opening, degrees (front drops)
SG_BASE  = 37;                  // SG90 base plane |y|, shaft points outward
HUB_Y0   = 63;  HUB_Y1 = 71;  HUB_R = 16;
CHIN_X0  = 74;  CHIN_X1 = 121;
CH_Z0    = 167.1; CH_Z1 = 172.1;            // chassis plate on top of head_roll_mount
ROLL_HOLES = [[65, 27.4], [65, -27.4], [95, 27.4], [95, -27.4]];
ROLL_EAR_Z = 158.8;                        // top of the roll-mount ears that carry the M3 inserts
TOF_FOOT_HOLES = [[101.5, 12.5], [101.5, -12.5]];   // M2.5 screws holding the separate ToF tab
RADXA_X0 = 32; RADXA_Y0 = -15;             // Radxa Zero 3W 65 x 30, holes 58 x 23
RADXA_HOLES = [[35.5, 11.5], [35.5, -11.5], [93.5, 11.5], [93.5, -11.5]];
CAM_HOLES = [[10.5, 163.4], [-10.5, 163.4], [10.5, 150.9], [-10.5, 150.9]];   // Pi camera v2 / IMX219 pattern
// rim screws (shell boss <- tray column), with web direction to the nearest wall
RIM = [[-75, 0, -1, 0], [-62, 34, 0, 1], [-62, -34, 0, -1], [-38, 54, 0, 1],
       [-38, -54, 0, -1], [-12, 60, 0, 1], [-12, -60, 0, -1]];
RIM_SCREW_L = 20;                          // M3 x 20 from below; counterbore depth follows
RIM_SEAT_Z = Z_BAND + 5.5 - RIM_SCREW_L;    // screw head seat (5.5 mm into the cap insert)
POSTS = [[-45, 30], [-45, -30]];           // tray posts up to the chassis plate
NECK_OPEN = [-30, 70, -50, 50, 8];          // same 100 x 100 opening as head_bot_sheet

// Microduck head profile at 1.7x, sampled and refit (x, half width, z bottom, z curve start, z top, n)
H = [
 [-82.8,  6.0, 115.0, 116.0, 126.0, 2.0],
 [-82.0, 14.0, 112.0, 113.0, 131.0, 2.2],
 [-80.0, 23.0, 110.5, 112.0, 140.5, 2.3],
 [-78.0, 31.0, 109.7, 112.0, 149.5, 2.3],
 [-75.0, 37.5, 109.7, 113.0, 157.0, 2.35],
 [-72.0, 42.0, 109.7, 114.0, 163.4, 2.4],
 [-68.0, 46.0, 109.7, 115.0, 168.4, 2.4],
 [-64.0, 49.3, 109.7, 116.0, 172.6, 2.4],
 [-60.0, 52.0, 109.7, 117.0, 176.2, 2.45],
 [-55.0, 55.0, 109.7, 118.0, 179.3, 2.45],
 [-50.0, 57.5, 109.7, 119.0, 182.6, 2.5],
 [-45.0, 59.5, 109.7, 119.5, 185.5, 2.5],
 [-40.0, 61.3, 109.7, 120.0, 187.8, 2.5],
 [-35.0, 63.0, 109.7, 120.5, 189.6, 2.55],
 [-27.0, 64.8, 109.7, 121.0, 192.0, 2.6],
 [-20.0, 66.2, 109.7, 121.5, 194.2, 2.6],
 [-10.0, 68.3, 109.7, 122.0, 196.2, 2.65],
 [  0.0, 70.3, 109.7, 122.0, 197.8, 2.7],
 [ 10.0, 72.0, 109.7, 122.0, 199.3, 2.7],
 [ 20.0, 73.3, 109.7, 122.0, 200.7, 2.75],
 [ 30.0, 74.0, 109.7, 122.0, 201.5, 2.8],
 [ 45.0, 74.7, 109.7, 122.0, 202.4, 2.8],
 [ 60.0, 75.0, 109.7, 122.0, 203.3, 2.8],
 [ 80.0, 75.0, 109.7, 122.0, 204.2, 2.8],
 [100.0, 74.6, 109.7, 122.0, 204.9, 2.8],
 [115.0, 74.3, 109.7, 122.0, 205.5, 2.8],
 [129.0, 74.0, 109.7, 122.0, 205.6, 2.8]
];
H_IN = concat([st_at(H, H[0][0] + T_H)],
              [for (s = H) if (s[0] > H[0][0] + T_H) s],
              [[140, 74.0, 109.7, 122.0, 205.6, 2.8]]);

module head_outer() loft(H);
module head_inner(extra = 0) loft(H_IN, inset = T_H + extra, ext = 25);
module zslab(z0, z1) translate([-200, -200, z0]) cube([400, 400, z1 - z0]);
module xslab(x0, x1) translate([x0, -200, -400]) cube([x1 - x0, 400, 800]);

// extrude a 2D (x, z) shape along y between |y| = y0 .. y1 on one side
module side_extrude(s, y0, y1) {
    if (s > 0) translate([0, y1, 0]) rotate([90, 0, 0]) linear_extrude(height = y1 - y0) children();
    else mirror([0, 1, 0]) translate([0, y1, 0]) rotate([90, 0, 0]) linear_extrude(height = y1 - y0) children();
}

// ---------------- jaw outline in the side view ----------------
module jaw_upper2d(clr = 0) offset(r = clr) union() {
    translate(JAW_P) circle(r = HUB_R);
    hull() { translate(JAW_P) circle(r = 9); translate([8, Z_BOT + 2]) square([26, Z_BAND - 0.5 - Z_BOT - 2]); }
}
module jaw_side2d(clr = 0) union() {
    jaw_upper2d(clr);
    offset(r = clr) translate([3, Z_BOT - 1]) square([CHIN_X1 - 3, Z_BAND - 0.5 - (Z_BOT - 1)]);
}
module jaw_keepout2d()
    union() for (a = [0 : -2.5 : -(JAW_OPEN + 2.5)])
        translate(JAW_P) rotate(a) translate(-JAW_P) jaw_side2d(0.8);
module jaw_keepout3d() for (s = [1, -1]) side_extrude(s, 58, 90) jaw_keepout2d();

// ---------------- white cap ----------------
module rim_boss(p, r = 4.5, h = 11) {
    hull() {
        translate([p[0], p[1], Z_BAND]) cylinder(r = r, h = h);
        translate([p[0] + p[2] * 9, p[1] + p[3] * 9, Z_BAND]) cylinder(r = r, h = h);
    }
}
module face_wall() intersection() { head_outer(); xslab(FACE_X0, FACE_X1); zslab(Z_BAND, 260); }

module head_shell() {
    difference() {
        union() {
            intersection() { difference() { head_outer(); head_inner(); } zslab(Z_BAND, 260); }
            face_wall();
            intersection() { head_outer(); union() for (p = RIM) rim_boss(p); }
        }
        jaw_keepout3d();
        // eye, face screws and ToF window
        translate([FACE_X0 - 1, EYE_C[0], EYE_C[1]]) rotate([0, 90, 0]) cylinder(d = EYE_HOLE, h = 10);
        for (p = FACE_SCREWS) translate([FACE_X0 - 1, p[0], p[1]]) rotate([0, 90, 0]) cylinder(d = M3_CLR, h = 10);
        translate([FACE_X0 - 1, TOF_C[0] - 4, TOF_C[1] - 2.5]) cube([10, 8, 5]);
        // inserts in the rim bosses, opening downward
        for (p = RIM) translate([p[0], p[1], Z_BAND]) rotate([180, 0, 0]) insert_hole(8);
    }
}

// ---------------- black floor band ----------------
module tray_lip() intersection() {
    difference() { head_inner(0.3); head_inner(2.3); }
    zslab(Z_BAND - EPS, Z_BAND + 3);
    xslab(-100, 3);
}
module head_tray() {
    difference() {
        union() {
            difference() {
                intersection() { head_outer(); xslab(-100, 3); zslab(Z_BOT - 1, Z_BAND); }
                intersection() { head_inner(); zslab(Z_FLOOR, 300); }
            }
            difference() { tray_lip(); for (p = RIM) rim_boss(p, r = 5.3, h = 4); }
            // rim columns, each webbed to the nearest wall (no free-standing pillars)
            intersection() { head_outer(); union() for (p = RIM) hull() {
                translate([p[0], p[1], Z_BOT]) cylinder(r = 4.5, h = Z_BAND - 0.2 - Z_BOT);
                translate([p[0] + p[2] * 9, p[1] + p[3] * 9, Z_BOT]) cylinder(r = 4.5, h = Z_BAND - 0.2 - Z_BOT);
            } }
            for (p = POSTS) translate([p[0], p[1], Z_BOT]) {
                cylinder(d = 10, h = CH_Z0 - 0.2 - Z_BOT);
                cylinder(d1 = 18, d2 = 10, h = Z_FLOOR - Z_BOT + 5);
            }
        }
        translate([0, 0, Z_BOT - 2]) linear_extrude(Z_FLOOR - Z_BOT + 4)
            rrect(NECK_OPEN[0], NECK_OPEN[1], NECK_OPEN[2], NECK_OPEN[3], NECK_OPEN[4]);
        jaw_keepout3d();
        for (p = RIM) translate([p[0], p[1], Z_BOT]) {
            translate([0, 0, -1]) cylinder(d = M3_CLR, h = 30);
            translate([0, 0, -1]) cylinder(d = M3_HEAD, h = 1 + RIM_SEAT_Z - Z_BOT);
        }
        for (p = POSTS) translate([p[0], p[1], CH_Z0 - 0.2]) insert_hole(8);
    }
}

// ---------------- black jaw ----------------
module jaw_low_zone() intersection() { head_outer(); xslab(3, CHIN_X1); zslab(Z_BOT - 1, Z_BAND - 0.5); }
module head_jaw() {
    difference() {
        union() {
            difference() {
                jaw_low_zone();
                intersection() {
                    loft(H_IN, inset = 5, ext = 25);
                    union() {
                        translate([-10, -200, Z_BOT - 10]) cube([CHIN_X0 + 10, 400, 60]);       // no floor behind the chin
                        translate([CHIN_X0, -200, Z_FLOOR]) cube([CHIN_X1 - 4 - CHIN_X0, 400, 60]); // chin floor 3 mm, front wall 4 mm
                    }
                }
            }
            for (s = [1, -1]) side_extrude(s, HUB_Y0, HUB_Y1) jaw_upper2d();
        }
        // left (+y): pivot screw, counterbore outside
        translate([JAW_P[0], 0, JAW_P[1]]) rotate([-90, 0, 0]) {
            cylinder(d = 3.6, h = 100);
            translate([0, 0, HUB_Y1 - 2.6]) cylinder(d = M3_HEAD, h = 10);
        }
        // right (-y): SG90 single-arm horn pocket + access hole for the shaft screw
        translate([JAW_P[0], -HUB_Y0 + EPS, JAW_P[1]]) rotate([90, 0, 0]) {
            cylinder(d = 7.8, h = 6.2);
            translate([0, 0, 4.0]) rotate([0, 0, 45]) translate([0, -3.3, 0]) cube([20, 6.6, 2.2]);
            cylinder(d = 5.5, h = 20);
        }
    }
}

// ---------------- black eye bezel ----------------
module eye_bezel() {
    translate([FACE_X1, EYE_C[0], EYE_C[1]]) rotate([0, 90, 0]) difference() {
        union() {
            hull() {
                cylinder(d = EYE_OD, h = 6);
                translate([0, 0, 6]) cylinder(d = EYE_OD - 6, h = 3);
            }
            translate([0, 0, -(FACE_X1 - FACE_X0) + 0.1]) cylinder(d = EYE_HOLE - 0.25, h = FACE_X1 - FACE_X0);
        }
        translate([0, 0, -5]) cylinder(d = 18, h = 20);
        translate([0, 0, -5]) cylinder(d = 26, h = 5 + 4);                           // camera lens pocket
        for (p = FACE_SCREWS) translate([-(p[1] - EYE_C[1]), p[0] - EYE_C[0], -EPS]) cylinder(d = 7.2, h = 3.6); // screw heads
        translate([-(TOF_C[1] - EYE_C[1]) - 2.5, TOF_C[0] - EYE_C[0] - 4, -5]) cube([5, 8, 20]);   // ToF window
    }
}

// ---------------- black chassis ----------------
module chassis_plate2d() union() {
    rrect(-52, 103, -46, 46, 6);
    rrect(8, 36, -(SG_BASE + 20.4), SG_BASE + 20.4, 4);
}
module bracket(s) {      // s = -1 right (SG90), +1 left (pivot)
    yb0 = SG_BASE + 17.9;  yb1 = yb0 + 2.5;
    difference() {
        union() {
            side_extrude(s, yb0, yb1) polygon([[-4, 136], [33, 136], [33, CH_Z0 + 0.5], [8, CH_Z0 + 0.5], [-4, 160]]);
            side_extrude(s, SG_BASE + 6, yb0 + 0.1) polygon([[29, 152], [33, 152], [33, CH_Z0 + 0.5], [29, CH_Z0 + 0.5]]);   // gusset
            if (s > 0) translate([JAW_P[0], 0, JAW_P[1]]) rotate([-90, 0, 0]) translate([0, 0, yb1 - 0.5]) cylinder(d = 11, h = HUB_Y0 - 0.5 - yb1 + 0.5);
        }
        if (s < 0) {
            sx = JAW_P[0] - 5.7;          // SG90 body centre x (shaft is 5.7 mm off centre)
            side_extrude(s, yb0 - 1, yb1 + 1) translate([sx - 11.9, JAW_P[1] - 6.9]) square([23.8, 13.8]);
            for (dx = [-13.9, 13.9]) translate([sx + dx, -yb0 + 1, JAW_P[1]]) rotate([90, 0, 0]) cylinder(d = M2_TAP, h = 6);
        } else {
            translate([JAW_P[0], HUB_Y0 - 0.5 + EPS, JAW_P[1]]) rotate([90, 0, 0]) insert_hole(7);
        }
    }
}
module head_chassis() {
    difference() {
        union() {
            intersection() {
                translate([0, 0, CH_Z0]) linear_extrude(CH_Z1 - CH_Z0) chassis_plate2d();
                head_inner(1.5);
            }
            // pegs that drop onto the roll-mount ears (like the stock head's bosses); plate top stays flat
            for (p = ROLL_HOLES) translate([p[0], p[1], ROLL_EAR_Z]) cylinder(d = 9, h = CH_Z0 - ROLL_EAR_Z + 0.1);   // pegs bear on the ears, plate floats 0.2 over the cup
            translate([100.3, -21, 141]) cube([2.5, 42, CH_Z0 - 141 + 0.5]);                   // camera plate (clear of roll mount x<=100)
            for (p = CAM_HOLES) translate([102.7, p[0], p[1]]) rotate([0, 90, 0]) cylinder(d = 4.2, h = 1.1);   // camera standoffs
            for (p = FACE_SCREWS) translate([102.7, p[0], p[1]]) rotate([0, 90, 0]) cylinder(d = 8, h = FACE_X0 - 0.2 - 102.7);
            bracket(-1); bracket(1);
        }
        for (p = ROLL_HOLES) translate([p[0], p[1], ROLL_EAR_Z - 1]) cylinder(d = M3_CLR, h = 30);          // M3x20 from the top into the ear inserts
        for (p = RADXA_HOLES) translate([p[0], p[1], CH_Z0 + 1]) cylinder(d = M25_TAP, h = 20);         // M2.5 x 6 brass standoffs, 4 mm thread
        for (p = TOF_FOOT_HOLES) translate([p[0], p[1], CH_Z0 + 1]) cylinder(d = M25_TAP, h = 20);
        for (p = CAM_HOLES) translate([99, p[0], p[1]]) rotate([0, 90, 0]) cylinder(d = M2_TAP, h = 10);
        for (p = FACE_SCREWS) translate([FACE_X0 - 0.2, p[0], p[1]]) rotate([0, 90, 0]) rotate([180, 0, 0]) insert_hole(5);
        for (p = POSTS) translate([p[0], p[1], CH_Z0 - 1]) {
            cylinder(d = M3_CLR, h = 20);
            translate([0, 0, CH_Z1 - CH_Z0 + 1 - 2.5]) cylinder(d = M3_HEAD, h = 5);
        }
        translate([0, 0, CH_Z0 - 1]) linear_extrude(10) rrect(20, 54, -11, 11, 3);       // cable pass-through
        for (x = [-22, 6], y = [-18.5, 16.5]) translate([x, y, CH_Z0 - 1]) cube([3, 2, 10]); // buck zip-tie slots
    }
}

// separate ToF tab (black): L bracket screwed to the chassis plate top with 2 x M2.5 x 6
module tof_tab() {
    difference() {
        union() {
            translate([97.8, -16, CH_Z1]) cube([5, 32, 2.5]);                       // foot
            translate([100.3, -9, CH_Z1]) cube([2.5, 18, 189 - CH_Z1]);             // upright
            for (dz = [-5.2, 5.2]) translate([102.7, 0, TOF_C[1] + dz]) rotate([0, 90, 0]) cylinder(d = 3.6, h = 1.1);
        }
        for (dz = [-5.2, 5.2]) translate([99, 0, TOF_C[1] + dz]) rotate([0, 90, 0]) cylinder(d = M2_TAP, h = 10);
        for (p = TOF_FOOT_HOLES) translate([p[0], p[1], CH_Z1 - 1]) cylinder(d = 2.8, h = 10);
    }
}
