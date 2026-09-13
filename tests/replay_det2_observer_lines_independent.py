"""Independent stdlib replay of twelve-line guards, without generator imports."""
from copy import deepcopy
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
P=((0,0,0),(2,1,1),(0,1,0),(0,0,1))
# Derived independently by solving the six edge cross-product equations.
LINES=((( -1,0,0),(0,0,1)),((1,0,0),(0,0,1)),
       ((1,1,0),(-2,0,-1)),((-1,1,0),(-2,0,-1)),
       ((1,0,0),(0,1,0)),((-1,0,0),(0,1,0)),
       ((-1,0,1),(-2,-1,0)),((1,0,1),(-2,-1,0)),
       ((1,0,2),(0,-1,1)),((-1,0,0),(0,-1,1)),
       ((-1,0,-1),(2,1,1)),((-1,-1,0),(2,1,1)))


def need(ok,msg):
    if not ok:raise ValueError(msg)


def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def lam(z):
    x,y,z=map(F,z)
    return(1+x/2-y-z,x/2,y-x/2,z-x/2)
def mass(z):return sum(max(0,-x) for x in lam(z))
def point(s,v,t):return tuple(a+t*b for a,b in zip(s,v))


def verify(d):
    need(list(map(tuple,d['contact_points']))==list(P),'contacts')
    normals=set()
    for u in product(range(-2,3),repeat=3):
        if not any(u):continue
        vals=[dot(u,p) for p in P]
        if max(vals)-min(vals)==1:
            normals.add(u if next(x for x in u if x)>0 else tuple(-x for x in u))
    # Complete: b,c lie in [-1,1], and |2a+b+c|<=1 entails |a|<=1.
    need(normals=={(0,1,0),(0,0,1),(1,-1,-1)},'normals derivation')
    need(set(map(tuple,d['width_one_normals']))==normals,'normal certificate')
    need({z for z in product(range(3),range(2),range(2)) if min(lam(z))>=0}==set(P),'empty P')
    # mass<62 bounds X in [-123,125], Y,Z in [-61,62].
    # In each independent representative one coordinate of v has magnitude
    # >=1, and |s_i|<=2, forcing |t|<130; [-200,200] is therefore complete.
    guards=set()
    for s,v in LINES:
        pts={point(s,v,t) for t in range(-200,201) if mass(point(s,v,t))<62}
        need(len(pts)==123,'independent line count')
        guards.update(pts)
    need(len(guards)==1456,'independent union count')
    need(d['finite_guard_count']==1456,'guard count claim')
    need(len(d['lines'])==12,'line count claim')
    used=set()
    for line in d['lines']:
        s=tuple(line['base_point']);v=tuple(line['primitive_direction']);u=tuple(line['normal'])
        match=[i for i,(a,b) in enumerate(LINES) if cross(v,b)==(0,0,0) and cross(v,sub(s,a))==(0,0,0)]
        need(len(match)==1 and match[0] not in used,'line correspondence')
        used.add(match[0])
        ids=line['contact_indices']
        need(ids==[i for i,p in enumerate(P) if dot(u,p)==line['level']],'slab contacts')
        need(v==sub(P[ids[1]],P[ids[0]]),'edge direction')
        need(cross(v,sub(s,P[ids[0]]))==tuple(line['cross_sign']*x for x in u),'line cross product')
        included=[t for t in range(-200,201) if mass(point(s,v,t))<62]
        need(included==list(range(*[line['volume_below_21_parameter_interval'][0],line['volume_below_21_parameter_interval'][1]+1])),'strict volume interval')
        need(len(included)==line['point_count']==123,'line point count')
        box=d['coordinate_box']
        need(box==[[-124,126],[-62,63],[-62,63]],'enclosing box')
        enclosed=[t for t in range(-200,201) if all(a<=x<=b for x,(a,b) in zip(point(s,v,t),box))]
        need(enclosed==list(range(line['enclosing_box_parameter_interval'][0],line['enclosing_box_parameter_interval'][1]+1)),'box interval')
    rows=d['guards']
    need([tuple(r['point']) for r in rows]==sorted(guards),'complete guard list')
    nontrivial=[]
    for row in rows:
        z=tuple(row['point']);l=lam(z)
        need(F(row['negative_barycentric_mass'])==mass(z),'guard mass')
        # The closed row domain has vertices: designated weight 1, or
        # designated weight 1/2 and one other weight 1/2. Evaluate these
        # explicitly as weight vectors, independently of generator formulas.
        maxima=[];minima=[]
        for i in range(4):
            designated=i^1
            weights=[]
            pure=[F(0)]*4;pure[designated]=F(1);weights.append(pure)
            for j in range(4):
                if j not in (i,designated):
                    a=[F(0)]*4;a[designated]=a[j]=F(1,2);weights.append(a)
            vals=[dot(a,l) for a in weights]
            maxima.append(max(vals));minima.append(min(vals))
        blockers=[i for i,x in enumerate(maxima) if x<=0]
        need(row['tautological']==bool(blockers),'tautology classification')
        if blockers:
            need(row['blocking_row']==blockers[0],'blocking row')
        else:
            need(row['possible_blocking_rows']==[i for i,x in enumerate(minima) if x<=0],'possible rows')
            nontrivial.append(z)
    need(len(nontrivial)==d['pair_nontrivial_count']==484,'nontrivial count')
    need(d['pair_tautological_count']==972,'tautology count')
    need(list(map(tuple,d['pair_nontrivial_points']))==nontrivial,'nontrivial list')
    return {'lines':12,'guards':1456,'pair_nontrivial':484,'pair_tautological':972}


def main():
    d=json.loads((ROOT/'certificates/det2_observer_lines.json').read_text())
    report=verify(d)
    changes=[lambda x:x['guards'].pop(),
             lambda x:x['lines'][0]['base_point'].__setitem__(0,99),
             lambda x:x['lines'][0]['volume_below_21_parameter_interval'].__setitem__(0,-99),
             lambda x:x['guards'][0].__setitem__('negative_barycentric_mass','0'),
             lambda x:x['guards'][0].__setitem__('tautological',not x['guards'][0]['tautological']),
             lambda x:x['pair_nontrivial_points'].pop(),
             lambda x:x.__setitem__('pair_tautological_count',971),
             lambda x:x['width_one_normals'].pop()]
    for change in changes:
        altered=deepcopy(d);change(altered)
        try:verify(altered)
        except ValueError:continue
        raise RuntimeError('mutation accepted')
    report['mutations_rejected']=len(changes)
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
