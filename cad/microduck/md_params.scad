// =====================================================================
//  Microduck-look skin for the Open Duck Mini v2 skeleton
//  Shared parameters and helpers.
//  Frame: Open Duck print/robot frame, mm. +x forward, +y left, +z up.
//  Every part is modelled where it sits on the robot (zero pose).
// =====================================================================

$fn = 72;
EPS = 0.01;

// ---------- fasteners ----------
INSERT_D   = 4.0;   // hole for M3 x 5 brass heat-set insert (Amazon B0DZ8B7FW1)
INSERT_L   = 6.0;   // hole depth for that insert
M3_CLR     = 3.4;   // M3 clearance
M3_HEAD    = 6.5;   // M3 socket-head counterbore
M3_NUT     = 6.4;   // M3 nut across corners (+clearance)
M2_TAP     = 1.8;   // M2 self-tapping pilot (SG90 tab screws, servo adapter)
M25_TAP    = 2.2;   // M2.5 self-tapping pilot (Radxa)
M2_CLR     = 2.4;

// ---------- colours (for previews only) ----------
C_WHITE = [0.95, 0.94, 0.90];
C_BLACK = [0.13, 0.13, 0.14];

// ---------- helpers ----------
function lerp(a, b, t) = a + (b - a) * t;

// Section with vertical sides from zb to zc and a superellipse cap from zc to zt.
// Points are (y, z). n = 2 gives an ellipse, larger n gives a squarer top.
function se_pts(w, zb, zc, zt, n, N = 56) =
    concat(
        [[ w, zb]],
        [for (i = [0:N]) let(t = i * 180 / N, c = cos(t), s = sin(t))
            [w * sign(c) * pow(abs(c), 2 / n), zc + (zt - zc) * pow(abs(s), 2 / n)]],
        [[-w, zb]]
    );

// st = [x, half_width, z_bottom, z_curve_start, z_top, exponent]
module station(st, inset = 0, ext = 0) {
    translate([st[0], 0, 0]) rotate([90, 0, 90])
        linear_extrude(height = EPS, center = true)
            offset(delta = -inset)
                polygon(se_pts(st[1], st[2] - ext, st[3], st[4], st[5]));
}

// piecewise loft through convex stations (hull of neighbours)
module loft(sts, inset = 0, ext = 0) {
    for (i = [0:len(sts) - 2])
        hull() { station(sts[i], inset, ext); station(sts[i + 1], inset, ext); }
}

// station parameters interpolated at any x inside the list
function st_at(sts, x) =
    let(i = max([for (k = [0:len(sts) - 2]) if (sts[k][0] <= x) k]),
        a = sts[i], b = sts[i + 1], t = (x - a[0]) / (b[0] - a[0]))
    [x, lerp(a[1], b[1], t), lerp(a[2], b[2], t), lerp(a[3], b[3], t),
        lerp(a[4], b[4], t), lerp(a[5], b[5], t)];

// heat-set insert pocket: opening at origin, going along -z by default
module insert_hole(depth = INSERT_L, d = INSERT_D) {
    translate([0, 0, -depth]) cylinder(d = d, h = depth + EPS);
    translate([0, 0, -0.6]) cylinder(d1 = d, d2 = d + 0.8, h = 0.6 + EPS);   // lead-in chamfer
}

// M3 clearance with counterbore, axis +z, counterbore at the top
module m3_cb(len_total, cb_depth) {
    translate([0, 0, -EPS]) cylinder(d = M3_CLR, h = len_total + 2 * EPS);
    translate([0, 0, len_total - cb_depth]) cylinder(d = M3_HEAD, h = cb_depth + 1);
}

module rrect(x0, x1, y0, y1, r) {
    translate([x0 + r, y0 + r]) offset(r = r) square([x1 - x0 - 2 * r, y1 - y0 - 2 * r]);
}
