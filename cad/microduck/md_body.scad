// =====================================================================
//  BODY  (rides on trunk_assembly: stock trunk_top / trunk_bottom)
//  body_shell(+1 / -1)  white  - left / right halves of the Microduck body
//  body_deck            black  - clamps to the trunk_top rear plate; 3S pack bay,
//                                servo-adapter shelf, shell and panel bosses
//  deck_clamp           black  - two bars under the rear plate (print 2)
//  body_panel           black  - rear port panel: switch, XT30, balance plug,
//                                battery hold-down finger
// =====================================================================

BX_F = 38.5;  BX_R = -102.5;  BY = 55;  BZ_B = -18;  BZ_T = 45;
R_FT = 30;    R_RT = 7;       R_BOT = 3;  R_PLAN = 8;  T_B = 2.5;
NECK_SLOT = [1, 26.5, 29];               // x from, |y| <=, z from (front top opening)
REAR_OPEN = [44, 38];                     // |y| <=, z <=  (open from the bottom edge)

// stock trunk_top features
PLATE = [-90.1, -40.2, 25.2];             // rear plate x0, x1, |y|; z -20.1 .. -9.1 (measured), 45 deg chamfer x -45..-41.5 up to z -5.5
BOSS_ADAPTER = [[-84.1, 14], [-84.1, -14], [-47, 14], [-47, -14]];
CLAMP_X = [-86, -50];  CLAMP_Y = 30;

// deck
DK_X0 = -100;  DK_X1 = -42.5;  DK_Y = 52;  DK_Z0 = -9.0;  DK_Z1 = -5.5;
PACK = [57.5, 67.4, 19.4];                // 3 x 18650 side by side + strips, x, y, z
RAIL_Y0 = 34.1; RAIL_Y1 = 36.5; RAIL_Z = 8;
SHELF = [-45, -12, 40, 21.3, 24.0];       // x0, x1, |y|, z0, z1  (on the trunk_top block top)
ADAPTER_HOLES = [[-41.5, 18.5], [-41.5, -18.5], [-13.5, 18.5], [-13.5, -18.5]];
SIDE_SCREWS = [[-88, -2], [-54, -2]];     // (x, z) on both sides
PANEL_SCREWS = [[40, -2], [-40, -2], [40, 33], [-40, 33]];   // (y, z)
SWITCH_C = [18, 29.5];  XT30_C = [-14, 31.5];  BAL_C = [-30, 31.5];
SEAM_TABS = [[-90, 37.5], [-5, 37.5]];    // (x, z) tabs joining the halves

// ---------------- outer form ----------------
module body_side2d(i = 0) hull() {
    translate([BX_F - R_FT, BZ_T - R_FT]) circle(r = R_FT - i);
    translate([BX_R + R_RT, BZ_T - R_RT]) circle(r = R_RT - i);
    translate([BX_F - R_BOT, BZ_B + R_BOT]) circle(r = max(R_BOT - i, 0.01));
    translate([BX_R + R_BOT, BZ_B + R_BOT]) circle(r = max(R_BOT - i, 0.01));
}
module body_form(i = 0) intersection() {
    translate([0, BY - i, 0]) rotate([90, 0, 0]) linear_extrude(2 * (BY - i)) body_side2d(i);
    translate([0, 0, -100]) linear_extrude(300) rrect(BX_R + i, BX_F - i, -BY + i, BY - i, R_PLAN - i);
}
module body_cavity() union() {
    body_form(T_B);
    translate([BX_R + T_B, -BY + T_B, BZ_B - 10]) cube([BX_F - BX_R - 2 * T_B, 2 * (BY - T_B), 10 + T_B + R_BOT]);   // open bottom (clears the stock trunk and hip yaw servos)
}

module seam_tab(s, x, z) {     // s=+1 left half tab y 0..3, s=-1 right half tab y -3..0
    difference() {
        hull() {
            translate([x - 4, s > 0 ? 0 : -3, z - 5]) cube([8, 3, 1]);
            translate([x - 5, s > 0 ? 0 : -3, BZ_T - T_B - 3]) cube([10, 3, 4]);
        }
        translate([x, 0, z]) rotate([90, 0, 0]) cylinder(d = M3_CLR, h = 20, center = true);
        if (s < 0) translate([x, -3 - EPS, z]) rotate([-90, 0, 0]) cylinder(d = M3_NUT, h = 2.6, $fn = 6);
    }
}

module body_shell(s) {     // s = +1 left (y>0), -1 right (y<0)
    difference() {
        union() {
            intersection() {
                difference() { body_form(); body_cavity(); }
                translate([BX_R - 5, s > 0 ? 0 : -BY - 5, BZ_B - 5]) cube([BX_F - BX_R + 10, BY + 5, 80]);
            }
            for (t = SEAM_TABS) seam_tab(s, t[0], t[1]);
            // front ribs that hug the trunk_top block sides (|y| 50.4)
            translate([22, s > 0 ? 50.6 : -BY + T_B - 0.1, -14]) cube([12, BY - T_B - 50.6 + 0.1, 32]);
        }
        // neck opening (front top) and rear port opening
        translate([NECK_SLOT[0], -NECK_SLOT[1], NECK_SLOT[2]]) cube([60, 2 * NECK_SLOT[1], 40]);
        translate([BX_R - 5, -REAR_OPEN[0], BZ_B - 5]) cube([5 + T_B + 1, 2 * REAR_OPEN[0], REAR_OPEN[1] - BZ_B + 5]);
        // side screws into the deck blocks (button head sits on the white surface)
        for (p = SIDE_SCREWS) translate([p[0], s * BY, p[1]]) rotate([90, 0, 0]) cylinder(d = M3_CLR, h = 10, center = true);
    }
}

// ---------------- black deck ----------------
module deck_plan_clip() translate([0, 0, -50]) linear_extrude(150) rrect(DK_X0, BX_F - T_B - 0.3, -BY + T_B + 0.3, BY - T_B - 0.3, R_PLAN - T_B + 0.5);
module body_deck() intersection() {
    deck_plan_clip();
    difference() {
        union() {
            translate([DK_X0, -DK_Y, DK_Z0]) cube([DK_X1 - DK_X0, 2 * DK_Y, DK_Z1 - DK_Z0]);
            for (s = [1, -1]) {
                // battery rails
                translate([DK_X0, s > 0 ? RAIL_Y0 : -RAIL_Y1, DK_Z1 - EPS]) cube([DK_X1 - 1.5 - DK_X0, RAIL_Y1 - RAIL_Y0, RAIL_Z - DK_Z1]);
                // shell screw blocks
                for (p = SIDE_SCREWS) translate([p[0] - 4, s > 0 ? 44 : -52.3, DK_Z0]) cube([8, 8.3, 6 - DK_Z0]);
                // rear panel columns
                translate([DK_X0, s > 0 ? 37 : -43, DK_Z0]) cube([7, 6, 37 - DK_Z0]);
                // adapter shelf posts
                translate([-47.5, s > 0 ? 37.5 : -43.5, DK_Z0]) cube([5, 6, SHELF[4] - DK_Z0]);
            }
            // adapter shelf over the trunk_top block, and its standoffs
            translate([SHELF[0] - 2.5, -SHELF[2] - 3.5, SHELF[3]]) cube([SHELF[1] - SHELF[0] + 2.5, 2 * SHELF[2] + 7, SHELF[4] - SHELF[3]]);
            for (p = ADAPTER_HOLES) translate([p[0], p[1], SHELF[4] - EPS]) cylinder(d = 5.5, h = 4);
            // ribs linking the rear columns across the top (keeps the deck square)
            for (s = [1, -1]) translate([DK_X0, s > 0 ? 37 : -43, 30]) cube([7, 6, 7]);
        }
        // stock adapter bosses poke up through the deck (deck is clamped instead)
        for (p = BOSS_ADAPTER) translate([p[0], p[1], DK_Z0 - 1]) cylinder(d = 7.5, h = 10);
        for (x = CLAMP_X, s = [1, -1]) translate([x, s * CLAMP_Y, DK_Z0 - 1]) cylinder(d = M3_CLR, h = 10);
        // relief for the plate-to-block 45 deg chamfer (trunk z = -9.0 + (x + 45)); 0.6 mm clear
        translate([-45.5, -30, -8.7]) rotate([0, -45, 0]) translate([0, 0, -10]) cube([20, 60, 10]);
        // inserts
        for (p = SIDE_SCREWS, s = [1, -1]) translate([p[0], s * 52.3, p[1]]) rotate([s > 0 ? -90 : 90, 0, 0]) insert_hole(7);
        for (p = PANEL_SCREWS) translate([DK_X0, p[0], p[1]]) rotate([0, 90, 0]) insert_hole(7);
        for (p = ADAPTER_HOLES) translate([p[0], p[1], SHELF[4] - 2]) cylinder(d = M2_TAP, h = 10);
        // shelf reliefs: stock servo screw heads and cable slots in the trunk_top block top
        for (y = [24.7, -24.7]) translate([-32.8, y, SHELF[3] - 1]) cylinder(d = 7.5, h = 10);
        for (s = [1, -1]) translate([-17.6, s > 0 ? 23.8 : -46.2, SHELF[3] - 1]) cube([7.5, 22.4, 10]);
        translate([-34, -12, SHELF[3] - 1]) cube([14, 24, 10]);        // wiring hole under the adapter
    }
}
module deck_clamp(x = -86) {
    difference() {
        translate([x - 2.5, -34, -24.5]) cube([5, 68, 4.1]);
        for (s = [1, -1]) translate([x, s * CLAMP_Y, -26]) {
            cylinder(d = M3_CLR, h = 10);
            cylinder(d = M3_NUT, h = 1.5 + 2.6, $fn = 6);
        }
    }
}

// ---------------- black rear panel ----------------
module body_panel() {
    difference() {
        union() {
            translate([BX_R, -REAR_OPEN[0] + 0.3, BZ_B + 2]) cube([T_B, 2 * (REAR_OPEN[0] - 0.3), REAR_OPEN[1] - 0.3 - BZ_B - 2]);
            translate([DK_X0 - EPS, -30, 22.6]) cube([40, 26, 2.4]);              // battery hold-down finger
            translate([DK_X0 - EPS, -30, 22.6]) cube([3, 26, 8]);                 // finger root
        }
        for (p = PANEL_SCREWS) translate([BX_R - 1, p[0], p[1]]) rotate([0, 90, 0]) {
            cylinder(d = M3_CLR, h = 10);
            cylinder(d = M3_HEAD, h = 1 + 1.2);
        }
        translate([BX_R - 1, SWITCH_C[0], SWITCH_C[1]]) rotate([0, 90, 0]) cylinder(d = 12.3, h = 10);
        translate([BX_R - 1, XT30_C[0] - 5.3, XT30_C[1] - 2.8]) cube([10, 10.6, 5.6]);
        translate([BX_R - 1, BAL_C[0] - 6.5, BAL_C[1] - 3.2]) cube([10, 13, 6.4]);
        for (z = [-8, -3, 2, 7]) translate([BX_R - 1, -22, z]) cube([10, 44, 2.2]);    // vents
    }
}

// ---------------- black switch guard ----------------
// The 12 V 20 A toggle's flip cover stands ~25 mm proud of the rear panel, and the rear
// face is what the duck lands on when it falls backwards. The guard clamps under the
// switch nut plus the top-right panel screw (use M3x12 there) and its U wall stands
// 30 mm out, open toward +y so the cover can still flip open.
GUARD_DEPTH = 30;  GUARD_T = 2.4;  GUARD_PLATE = 2;
GUARD_WIN = [34, 24];                     // inner window y, z (centred on the switch)
module switch_guard() {
    y0 = SWITCH_C[0] - GUARD_WIN[0] / 2;  y1 = SWITCH_C[0] + GUARD_WIN[0] / 2;
    z0 = SWITCH_C[1] - GUARD_WIN[1] / 2;  z1 = SWITCH_C[1] + GUARD_WIN[1] / 2;
    difference() {
        union() {
            // plate on the panel face
            translate([BX_R - GUARD_PLATE, 0, 0]) rotate([90, 0, 90])     // 2D (u, v) -> (y, z), extruded along +x
                linear_extrude(GUARD_PLATE) rrect(y0 - GUARD_T, PANEL_SCREWS[2][0] + 5, z0 - GUARD_T, z1 + GUARD_T, 3);
            // U wall: -y side, top and bottom
            translate([BX_R - GUARD_PLATE - GUARD_DEPTH, 0, 0]) difference() {
                translate([0, y0 - GUARD_T, z0 - GUARD_T]) cube([GUARD_DEPTH + EPS, y1 - y0 + GUARD_T, z1 - z0 + 2 * GUARD_T]);
                translate([-1, y0, z0]) cube([GUARD_DEPTH + 2, y1 - y0 + 1, z1 - z0]);
            }
        }
        translate([BX_R - 5, SWITCH_C[0], SWITCH_C[1]]) rotate([0, 90, 0]) cylinder(d = 12.3, h = 10);
        translate([BX_R - 5, PANEL_SCREWS[2][0], PANEL_SCREWS[2][1]]) rotate([0, 90, 0]) cylinder(d = M3_CLR, h = 10);
    }
}
