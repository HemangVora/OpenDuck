import numpy as np, asm
asm.pose()
for mn,b,t in asm.geoms(["trunk_assembly","hip_roll_assembly","hip_roll_assembly_2"]):
    lo,hi=t.bounds
    if hi[2] < -15 or lo[2] < -18:
        print(f"{b:22s} {mn:34s} x[{lo[0]:6.1f},{hi[0]:6.1f}] y[{lo[1]:6.1f},{hi[1]:6.1f}] z[{lo[2]:6.1f},{hi[2]:6.1f}]")
