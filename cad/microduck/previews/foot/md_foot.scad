S="../../stl/"; U="/Users/hemangvora/OpenDuck/upstream/Open_Duck_Mini/print/";
color([0.15,0.15,0.16]) { import(str(S,"md_foot_top.stl")); import(str(S,"md_foot_side.stl")); }
color([0.96,0.95,0.92]) import(str(U,"foot_bottom_pla.stl"));
color([0.35,0.35,0.36]) import(str(U,"foot_bottom_tpu.stl"));
