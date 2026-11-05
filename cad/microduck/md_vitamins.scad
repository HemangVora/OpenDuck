// Envelopes of the bought electronics, placed where the parts expect them (for fit checks and renders)
SG90_STL = "/Users/hemangvora/OpenDuck/upstream/Open_Duck_Mini/mini_bdx/robots/open_duck_mini_v2/sg90.stl";
module v_sg90_jaw() multmatrix([[1,0,0,JAW_P[0]-5.7],[0,0,-1,-SG_BASE],[0,1,0,JAW_P[1]],[0,0,0,1]]) import(SG90_STL);
module v_radxa() {                         // Radxa Zero 3W 65 x 30 board on 6 mm standoffs + 16 mm component/wire budget
    translate([RADXA_X0, RADXA_Y0, CH_Z1 + 6]) { cube([65, 30, 1.6]); translate([2, 2, 1.6]) cube([61, 26, 16]); translate([0, 0, -2]) cube([65, 30, 2]); }
}
module v_buck() translate([-30, -13.5, CH_Z1 + 1]) cube([46, 27, 12]);            // XY-3606 (HW-688), generous envelope
module v_camera() translate([103.8, -12.5, EYE_C[1] - 14.5]) { cube([1.0, 25, 24]); translate([1.0, 12.5 - 4.25, 14.5 - 4.25]) cube([5.2, 8.5, 8.5]); }  // Pi cam v2 / IMX219 board + lens module
module v_tof() translate([103.8, TOF_C[0] - 6.5, TOF_C[1] - 6.5]) { cube([1.0, 13, 13]); translate([1.0, 6.5 - 3.2, 6.5 - 1.5]) cube([1.75, 6.4, 3.0]); }
module head_vitamins() { v_sg90_jaw(); v_radxa(); v_buck(); v_camera(); v_tof(); }

// ---------------- body electronics ----------------
module v_pack()    translate([DK_X0, -PACK[1] / 2, DK_Z1]) cube(PACK);                       // 3S1P Samsung 30Q pack
module v_bms()     translate([DK_X0 + 5, -31, DK_Z1 + PACK[2] + 0.5]) cube([48, 62, 7]);      // 3S 40 A BMS, 5-FET board
module v_adapter() translate([-44, -21, SHELF[4] + 4]) { cube([33, 42, 1.6]); translate([1, 1, 1.6]) cube([31, 40, 10]); }   // Bus Servo Adapter (A)
module v_switch()  {   // AUTO MT 12 V 20 A toggle, 12 mm hole; body 28 x 16 behind the panel, cover outside
    translate([DK_X0, SWITCH_C[0] - 14, SWITCH_C[1] - 8]) cube([45, 28, 16]);
    translate([BX_R - 25, SWITCH_C[0] - 14, SWITCH_C[1] - 8]) cube([25, 28, 16]);
}
module v_xt30()    translate([DK_X0, XT30_C[0] - 5.1, XT30_C[1] - 2.6]) cube([16, 10.2, 5.2]);
module v_balance() translate([DK_X0, BAL_C[0] - 6.2, BAL_C[1] - 2.9]) cube([8, 12.4, 5.8]);
module v_caps()    for (y = [26, 33]) translate([-40, y, SHELF[4] + 5.3]) rotate([0, 90, 0]) cylinder(d = 10.2, h = 21);  // 2 x 1000 uF 25 V lying on the shelf
module body_vitamins() { v_pack(); v_bms(); v_adapter(); v_switch(); v_xt30(); v_balance(); v_caps(); }
