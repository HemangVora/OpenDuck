// =====================================================================
//  THIGH PILLOWS  (white)  - replace the stock left_cache / right_cache
//  Bolt to the thigh's outer sheet (y = 113.0) with the stock cache screws,
//  into the leg_spacer inserts. Print flat face down, dome up, no supports.
// =====================================================================
PIL_Y0 = 113.0;                    // outer face of left_knee_to_ankle_left_sheet
PIL_T = 15;                        // pillow thickness
PIL_RE = 7;                        // edge roll radius
PIL_CROWN = 2.5;                   // extra dome in the middle
PIL_FLANGE = 2.1;                  // same screw seat as the stock cache (seat at y 115.1)
// outline: top edge z -42 (x -42..30), bottom edge z -121 (x -34..4)
PIL_C = [[18, -54, 12], [-30, -54, 12], [-6, -111, 10], [-24, -111, 10]];   // (x, z, r)
CACHE_HOLES = [[-8.1, -85.4], [-24.1, -85.4]];                                 // (x, z)

module pil2d(i = 0) hull() for (c = PIL_C) translate([c[0], c[1]]) circle(r = max(c[2] - i, 0.6));
// map 2D (u, v) + extrude w  ->  world (x = u, y = w, z = v)
module xz_extrude(h) multmatrix([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]]) linear_extrude(h) children();

module thigh_pillow_left() {
    N = 9;
    difference() {
        hull() {
            translate([0, PIL_Y0, 0]) xz_extrude(PIL_T - PIL_RE) pil2d(0);
            for (k = [1 : N]) {
                a = 90 * k / N;
                translate([0, PIL_Y0 + PIL_T - PIL_RE + PIL_RE * sin(a) - 0.01, 0]) xz_extrude(0.01) pil2d(PIL_RE * (1 - cos(a)));
            }
            // soft crown: a smaller, taller centre so the pillow reads as puffy
            translate([0, PIL_Y0 + PIL_T + PIL_CROWN - 0.01, 0]) xz_extrude(0.01) pil2d(PIL_RE + 9);
        }
        for (h = CACHE_HOLES) translate([h[0], 0, h[1]]) {
            translate([0, PIL_Y0 - 1, 0]) rotate([-90, 0, 0]) cylinder(d = M3_CLR, h = PIL_T + 10);
            translate([0, PIL_Y0 + PIL_FLANGE, 0]) rotate([-90, 0, 0]) cylinder(d = M3_HEAD + 0.5, h = PIL_T + 10);
        }
    }
}
module thigh_pillow_right() mirror([0, 1, 0]) thigh_pillow_left();
