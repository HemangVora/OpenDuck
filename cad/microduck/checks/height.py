import numpy as np, trimesh, asm, math
from common import *
S2=S
att={n:asm.attach(L(S2+n+".stl"),b) for n,b in {"head_shell":"head_assembly","head_jaw":"head_assembly","body_shell_left":"trunk_assembly","body_shell_right":"trunk_assembly","switch_guard":"trunk_assembly","thigh_pillow_left":"knee_and_ankle_assembly","thigh_pillow_right":"knee_and_ankle_assembly_3"}.items()}
DROP={"head","head_bot_sheet","sg90","antenna","left_antenna_holder","right_antenna_holder","raspberrypizerow","board","body_front","body_back","body_middle_bottom","body_middle_top","battery_pack_lid","power_switch","usb_c_charger","bms","cell","holder","left_cache","right_cache"}
D=math.degrees
poses={"straight legs (zero pose)":{},
 "walking stance (policy default)":{"left_hip_yaw":D(0.002),"left_hip_roll":D(0.053),"left_hip_pitch":D(-0.63),"left_knee":D(1.368),"left_ankle":D(-0.784),
   "right_hip_yaw":D(-0.003),"right_hip_roll":D(-0.065),"right_hip_pitch":D(0.635),"right_knee":D(1.379),"right_ankle":D(-0.796)},
 "render crouch":{"left_hip_pitch":-30,"left_knee":60,"left_ankle":-30,"right_hip_pitch":30,"right_knee":60,"right_ankle":-30}}
for name,q in poses.items():
    asm.pose(q); V=[t.vertices for mn,b,t in asm.geoms() if mn not in DROP]+[f().vertices for f in att.values()]
    V=np.vstack(V); lo,hi=V.min(0),V.max(0); e=hi-lo
    zh=[f().vertices[:,2].max() for k,f in att.items() if k=="head_shell"][0]; print(f"{name:34s} floor-to-body-top {max(f().vertices[:,2].max() for k,f in att.items() if k.startswith('body_shell'))-lo[2]:4.0f} height {e[2]:5.0f} mm  depth {e[0]:4.0f}  width {e[1]:4.0f}")
