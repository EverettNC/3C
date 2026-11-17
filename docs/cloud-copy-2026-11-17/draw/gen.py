import math
def spiral(cx, cy, r0, r1, turns, end_deg, n=400, flip=True):
    # Archimedean spiral, ends (outer end) pointing at end_deg
    pts=[]
    total=turns*2*math.pi
    end=math.radians(end_deg)
    for i in range(n+1):
        t=i/n
        a=end - total*(1-t)
        r=r0+(r1-r0)*t
        pts.append((cx+r*math.cos(a), cy-r*math.sin(a)))
    return pts
def d(pts): return "M"+" L".join(f"{x:.1f},{y:.1f}" for x,y in pts)
import json,sys
w=spiral(390,240,6,78,2.6,180)
c=spiral(470,300,8,170,3.0,180)
json.dump({"whole":d(w),"whole_end":w[-1],"conch":d(c),"conch_pts":c},open("sp.json","w"))
print(w[-1], c[-1])
