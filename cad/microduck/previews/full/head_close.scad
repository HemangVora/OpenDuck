S="../../stl/";
color([0.96,0.95,0.92]) import(str(S,"head_shell.stl"));
color([0.16,0.16,0.17]) { import(str(S,"head_tray.stl")); import(str(S,"eye_bezel.stl")); }
color([0.30,0.30,0.32]) import(str(S,"head_jaw.stl"));
