import trimesh, os
O="/Users/hemangvora/OpenDuck/print/microduck_v3/oriented/"; L=O+"layout/"; os.makedirs(L,exist_ok=True)
def place(plate, items):
    for i,(n,x,y) in enumerate(items):
        m=trimesh.load(O+n+".stl",force='mesh'); m.apply_translation(-m.bounds[0]+[x,y,0]); fn=f"{L}{plate}__{i}_{n}.stl"; m.export(fn)
        print(plate,n,m.bounds[:,:2].round(1).tolist())
place("11a",[("head_shell",5,5)])
place("11d",[("eye_ring",5,5),("mouth_jaw",62,5),("mouth_bill",108,5)])
place("12a",[("head_jaw",5,5),("head_tray",132,5)])
place("12b",[("head_chassis",5,5),("face_bill",172,5)])
place("14a",[("md_foot_top",5,5),("md_foot_top",5,52),("md_foot_side",5,99),("md_foot_side",5,124)])
place("14b",[("foot_bottom_pla",5,5),("foot_bottom_pla",5,40)])
