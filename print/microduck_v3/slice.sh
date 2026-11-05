#!/bin/bash
# Re-slice the Microduck v3 plates with the Bambu Studio CLI (see README.md).
V=/Users/hemangvora/OpenDuck/print/microduck_v3; PR=/Users/hemangvora/OpenDuck/print/profiles; O=$V/oriented
P=/Applications/BambuStudio.app/Contents/Resources/profiles/BBL; B="/Applications/BambuStudio.app/Contents/MacOS/BambuStudio"; M="$PR/machine_a1_04.json"   # flattened: the system preset alone gives a 200 x 200 bed
run(){ name=$1; proc=$2; fil=$3; arr=$4; shift 4; d=$V/plates/$name; rm -rf "$d"; mkdir -p "$d"
  ( cd "$d" && "$B" --load-settings "$M;$PR/$proc.json" --load-filaments "$PR/$fil.json" --arrange $arr --orient 0 --slice 0 --export-3mf "$name.3mf" --outputdir "$d" "$@" >log 2>&1 )
  python3 -c "
import json
d=json.load(open('$d/result.json')); print('$name', d.get('error_string'), 'code', d.get('return_code'))
for sp in d.get('sliced_plates',[]): print('   plate',sp['id'],'h',round(sp['main_predication']/3600,2),'g',round(sp['filaments'][0]['total_used_g'],1),'support min',round(sp['feature_type_times'].get('Support',0)/60),[o['name'] for o in sp.get('objects',[])])"
  [ -f "$d/$name.3mf" ] && cp "$d/$name.3mf" $V/3mf/; }
W="duck_pla_3walls fil_bambu_pla_lite_a1"; K="duck_pla_4walls fil_generic_pla_a1"
Y=$O/layout
G=${1:-all}
lay(){ ls $Y/$1__*.stl; }
if [ "$G" = all ] || [ "$G" = white ]; then
  run 11a_head_shell_white $W 0 $(lay 11a)
  run 11d_eye_mouth_white $W 0 $(lay 11d)
  run 14b_sole_plates_white $W 0 $(lay 14b)
fi
if [ "$G" = all ] || [ "$G" = black ]; then
  run 12a_head_jaw_tray_black $K 0 $(lay 12a)
  run 12b_chassis_face_black $K 0 $(lay 12b)
  run 14a_feet_black $K 0 $(lay 14a)
fi
