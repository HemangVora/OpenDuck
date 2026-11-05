S="../../stl/"; open=15;   // degrees
JP=[20,0,146];
W=[0.96,0.95,0.92]; K=[0.15,0.15,0.16];
color(W) import(str(S,"head_shell.stl"));
color(K) { import(str(S,"head_tray.stl")); import(str(S,"face_bill.stl")); }
color(W) { import(str(S,"eye_ring.stl")); import(str(S,"mouth_bill.stl")); }
translate(JP) rotate([0,open,0]) translate(-JP) { color(K) import(str(S,"head_jaw.stl")); color(W) import(str(S,"mouth_jaw.stl")); }
color([0.05,0.05,0.05]) { import(str(S,"v_camera.stl")); import(str(S,"v_tof.stl")); }
