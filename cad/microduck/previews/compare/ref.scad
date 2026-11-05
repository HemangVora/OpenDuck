// reference Microduck at 1.7x, shown in the two print colours
color([0.96,0.95,0.92]) { import("ref_purple.stl"); import("ref_blue.stl"); }
color([0.16,0.16,0.17]) import("ref_yellow.stl");
color([0.05,0.05,0.06]) { import("ref_eye.stl"); import("ref_dark.stl"); }
color([0.55,0.55,0.57]) import("ref_grey.stl");
color([0.80,0.81,0.83]) translate([-160,-170,-0.5]) cube([320,340,0.5]);
