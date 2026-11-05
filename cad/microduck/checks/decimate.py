import trimesh, sys
for f in sys.argv[1:]:
    m=trimesh.load(f,force='mesh'); n=len(m.faces)
    if n>150000:
        m=m.simplify_quadric_decimation(percent=1-120000/n); m.export(f)
    print(f.split('/')[-1], n, "->", len(m.faces))
