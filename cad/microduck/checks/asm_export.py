import trimesh, numpy as np, sys, json, os, asm
S="/Users/hemangvora/OpenDuck/cad/microduck/stl/"
OUT=sys.argv[1]; q=json.loads(sys.argv[2]) if len(sys.argv)>2 else {}
os.makedirs(OUT,exist_ok=True)
DROP={"head","head_bot_sheet","sg90","antenna","left_antenna_holder","right_antenna_holder","raspberrypizerow","board",
      "body_front","body_back","body_middle_bottom","body_middle_top","battery_pack_lid","power_switch","usb_c_charger","bms","cell","holder",
      "left_cache","right_cache"}
SERVO={"wj-wk00-0123middlecase_56","wj-wk00-0124bottomcase_45","wj-wk00-0122topcabinetcase_95","drive_palonier","passive_palonier"}
WHITE={"head_shell":"head_assembly","body_shell_left":"trunk_assembly","body_shell_right":"trunk_assembly",
       "thigh_pillow_left":"knee_and_ankle_assembly","thigh_pillow_right":"knee_and_ankle_assembly_3"}
BLACK={"head_tray":"head_assembly","head_jaw":"head_assembly","eye_bezel":"head_assembly","head_chassis":"head_assembly","tof_tab":"head_assembly",
       "body_deck":"trunk_assembly","body_panel":"trunk_assembly","switch_guard":"trunk_assembly","deck_clamp_rear":"trunk_assembly","deck_clamp_front":"trunk_assembly"}
VIT={"v_sg90_jaw":"head_assembly","v_radxa":"head_assembly","v_buck":"head_assembly","v_camera":"head_assembly","v_tof":"head_assembly",
     "v_pack":"trunk_assembly","v_bms":"trunk_assembly","v_adapter":"trunk_assembly","v_switch":"trunk_assembly","v_caps":"trunk_assembly"}
att={}
for grp in (WHITE,BLACK,VIT):
    for n,b in grp.items(): att[n]=asm.attach(trimesh.load(S+n+".stl",force='mesh'),b)
asm.pose(q)
g={"white":[], "black":[], "servo":[], "vit":[], "tpu":[]}
for mn,b,t in asm.geoms():
    if mn in DROP: continue
    if mn in SERVO: g["servo"].append(t)
    elif mn=="foot_bottom_tpu": g["tpu"].append(t)
    else: g["black"].append(t)
for n in WHITE: g["white"].append(att[n]())
for n in BLACK: g["black"].append(att[n]())
for n in VIT: g["vit"].append(att[n]())
allp=trimesh.util.concatenate(sum(g.values(),[])); zmin=allp.bounds[0][2]
for k,v in g.items():
    m=trimesh.util.concatenate(v); m.apply_translation([0,0,-zmin]); m.export(f"{OUT}/{k}.stl")
print("bounds after drop to floor", (allp.bounds-[0,0,zmin]).round(1).tolist())
