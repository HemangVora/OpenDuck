import trimesh, numpy as np, sys, json, os, asm
S="/Users/hemangvora/OpenDuck/cad/microduck/stl/"
OUT=sys.argv[1]; q=json.loads(sys.argv[2]) if len(sys.argv)>2 else {}; JAW=float(sys.argv[3]) if len(sys.argv)>3 else 0
os.makedirs(OUT,exist_ok=True)
DROP={"head","head_bot_sheet","sg90","antenna","left_antenna_holder","right_antenna_holder","raspberrypizerow","board",
      "body_front","body_back","body_middle_bottom","body_middle_top","battery_pack_lid","power_switch","usb_c_charger","bms","cell","holder",
      "left_cache","right_cache","foot_top","foot_side"}
SERVO={"wj-wk00-0123middlecase_56","wj-wk00-0124bottomcase_45","wj-wk00-0122topcabinetcase_95","drive_palonier","passive_palonier"}
H="head_assembly"; T="trunk_assembly"
WHITE={"head_shell":H,"eye_ring":H,"mouth_bill":H,"body_shell_left":T,"body_shell_right":T,
       "thigh_pillow_left":"knee_and_ankle_assembly","thigh_pillow_right":"knee_and_ankle_assembly_3"}
BLACK={"head_tray":H,"face_bill":H,"head_chassis":H,"body_deck":T,"body_panel":T,"switch_guard":T,"deck_clamp_rear":T,"deck_clamp_front":T}
JAWP={"head_jaw":"black","mouth_jaw":"white"}
JP=np.array([20,0,146.0]); Rj=trimesh.transformations.rotation_matrix(np.radians(JAW),[0,1,0],JP)
att=[]
for grp,col in ((WHITE,"white"),(BLACK,"black")):
    for n,b in grp.items(): att.append((col,asm.attach(trimesh.load(S+n+".stl",force='mesh'),b)))
for n,col in JAWP.items():
    m=trimesh.load(S+n+".stl",force='mesh'); m.apply_transform(Rj); att.append((col,asm.attach(m,H)))
for n in ["md_foot_top","md_foot_side"]:
    m=trimesh.load(S+n+".stl",force='mesh'); att.append(("black",asm.attach(m,"foot_assembly")))
    r=m.copy(); r.apply_translation([0,-181.2,0]); att.append(("black",asm.attach(r,"foot_assembly_2")))
asm.pose(q)
g={"white":[],"black":[],"servo":[],"tpu":[]}
for mn,b,t in asm.geoms():
    if mn in DROP: continue
    if mn in SERVO: g["servo"].append(t)
    elif mn=="foot_bottom_tpu": g["tpu"].append(t)
    elif mn=="foot_bottom_pla": g["white"].append(t)          # white sole band
    else: g["black"].append(t)
for col,f in att: g[col].append(f())
allp=trimesh.util.concatenate(sum(g.values(),[])); zmin=allp.bounds[0][2]
for k,v in g.items():
    m=trimesh.util.concatenate(v); m.apply_translation([0,0,-zmin])
    if len(m.faces)>150000: m=m.simplify_quadric_decimation(percent=1-120000/len(m.faces))
    m.export(f"{OUT}/{k}.stl")
print("bounds", (allp.bounds-[0,0,zmin]).round(1).tolist())
