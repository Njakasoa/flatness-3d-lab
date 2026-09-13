"""Independent Fraction verification of gauge-truncated observer guards.

No imports from the generators, src, geometry core, or other replay scripts.
"""
from copy import deepcopy
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
P=((0,0,0),(2,1,1),(0,1,0),(0,0,1))
BETA=Q(37,102)
LINES=(((-1,0,0),(0,0,1)),((1,0,0),(0,0,1)),
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
def canonical(v):return v if next(x for x in v if x)>0 else tuple(-x for x in v)
def point(s,v,t):return tuple(x+t*y for x,y in zip(s,v))


def derive(s,v):
    ids=next((i,j) for i,j in combinations(range(4),2) if sub(P[j],P[i])==v)
    r=sub(s,P[ids[0]])
    others=[i for i in range(4) if i not in ids]
    w=sub(P[others[1]],P[others[0]])
    # Solve two independent coordinates for w=a*v+d*r, using Cramer's rule.
    i,j=next((i,j) for i,j in combinations(range(3),2) if v[i]*r[j]-v[j]*r[i])
    det=v[i]*r[j]-v[j]*r[i]
    a=Q(w[i]*r[j]-w[j]*r[i],det)
    d=Q(v[i]*w[j]-v[j]*w[i],det)
    if d<0:w=tuple(-x for x in w);a=-a;d=-d
    need(d==2 and a.denominator==1,'edge coordinates')
    need(tuple(a*x+d*y for x,y in zip(v,r))==w,'edge reconstruction')
    return ids,r,w,a,d


def retained(a,d,beta):
    # The small enumeration is complete for these explicit lines: |a|<=3,
    # d=2 and beta>=3/5 or beta=37/102 force |t|<10.
    return [t for t in range(-20,21)
            if beta*max(Q(1),abs(d*t-a)/(d+1),abs(d*(t-1)-a)/(d+1))<1]


def verify(data):
    need(Q(data['beta'])==BETA,'beta')
    need(data['volume_cutoff_required'] is False,'volume premise')
    expected_edges=sorted({canonical(sub(P[j],P[i])) for i,j in combinations(range(4),2)})
    need(list(map(tuple,data['edge_directions']))==expected_edges,'six edge coverage')
    expected_guards=set()
    for s,v in LINES:
        ids,r,w,a,d=derive(s,v)
        ts=retained(a,d,BETA)
        need(len(ts)==7,'independent per-line count')
        expected_guards.update(point(s,v,t) for t in ts)
    need(len(expected_guards)==64,'independent union count')
    need(len(data['lines'])==12,'twelve records')
    used=set();record_guards=set()
    for row in data['lines']:
        s=tuple(row['base_point']);v=tuple(row['primitive_direction'])
        matches=[i for i,(b,w) in enumerate(LINES) if cross(v,w)==(0,0,0) and cross(v,sub(s,b))==(0,0,0)]
        need(len(matches)==1 and matches[0] not in used,'line correspondence')
        used.add(matches[0])
        ids,r,w,a,d=derive(s,v)
        need(row['contact_indices']==list(ids),'line contacts')
        need(tuple(row['r'])==r and tuple(row['opposite_edge_oriented'])==w,'archived r/w')
        need(list(map(Q,row['opposite_edge_basis_coefficients']))==[a,d],'archived a/d')
        left=a/d+1-(d+1)/(d*BETA);right=a/d+(d+1)/(d*BETA)
        need(list(map(Q,row['open_parameter_interval']))==[left,right],'strict open endpoints')
        ts=retained(a,d,BETA)
        need(ts==[t for t in range(-20,21) if left<t<right],'rho versus interval')
        need(row['integer_parameter_interval']==[min(ts),max(ts)],'integer interval')
        pts=[point(s,v,t) for t in ts]
        need(list(map(tuple,row['points']))==pts,'line point list')
        record_guards.update(pts)
        # Verify both cancellations as vector equalities, not just formulas.
        for t in ts:
            for shift in (0,1):
                combination=tuple((d*(r[i]+(t-shift)*v[i])-w[i])/(d+1) for i in range(3))
                need(combination==tuple((d*(t-shift)-a)*x/(d+1) for x in v),'convex cancellation')
    need(record_guards==expected_guards,'union agreement')
    need(data['guard_count']==64,'guard count')
    need([tuple(r['point']) for r in data['guards']]==sorted(expected_guards),'complete guard list')
    non=[]
    for row in data['guards']:
        x,y,z=map(Q,row['point']);l=(1+x/2-y-z,x/2,y-x/2,z-x/2)
        mins=[];maxs=[]
        for i in range(4):
            weights=[]
            pure=[Q(0)]*4;pure[i^1]=1;weights.append(pure)
            for j in range(4):
                if j not in(i,i^1):
                    w=[Q(0)]*4;w[i^1]=w[j]=Q(1,2);weights.append(w)
            vals=[dot(w,l) for w in weights];mins.append(min(vals));maxs.append(max(vals))
        blocking=[i for i,x in enumerate(maxs) if x<=0]
        need(row['tautological']==bool(blocking),'pair classification')
        if blocking:need(row['blocking_row']==blocking[0],'blocking row')
        else:
            need(row['possible_blocking_rows']==[i for i,x in enumerate(mins) if x<=0],'possible blockers')
            non.append(tuple(row['point']))
    need(len(non)==20==data['pair_nontrivial_count'],'nontrivial count')
    need(list(map(tuple,data['pair_nontrivial_points']))==non,'twenty clauses')
    need(data['pair_tautological_count']==44,'tautology count')
    need(Q(3)/BETA-1==Q(269,37)<8,'general interval bound')
    need(data['general_d_greater_than_one_maximum_guards']==96,'general guard bound')
    return {'guards':64,'pair_nontrivial':20,'pair_tautological':44,'edge_directions':6}


def main():
    # A separate exact boundary case makes strict versus weak observable:
    # beta=3/5,a=1,d=2 yields interval (-1,3), excluding both integer ends.
    need(retained(Q(1),Q(2),Q(3,5))==[0,1,2],'strict endpoint regression')
    data=json.loads((ROOT/'certificates/det2_observer_gauge_guards.json').read_text())
    report=verify(data)
    mutations=[
        lambda d:d['lines'][0]['open_parameter_interval'].__setitem__(0,'-3'),
        lambda d:d['lines'][0]['integer_parameter_interval'].__setitem__(0,-3),
        lambda d:d['lines'][0]['opposite_edge_oriented'].__setitem__(0,-2),
        lambda d:d['lines'][0]['opposite_edge_basis_coefficients'].__setitem__(1,'-2'),
        lambda d:d['lines'][0]['r'].__setitem__(0,2),
        lambda d:d['edge_directions'].pop(),
        lambda d:d['guards'].pop(),
        lambda d:d['pair_nontrivial_points'].pop(),
        lambda d:d['lines'][0]['points'].pop(),
        lambda d:d['guards'][0].__setitem__('tautological',not d['guards'][0]['tautological']),
    ]
    for change in mutations:
        altered=deepcopy(data);change(altered)
        try:verify(altered)
        except ValueError:continue
        raise RuntimeError('mutation accepted')
    report['mutations_rejected']=len(mutations)
    report['strict_integer_endpoint_regression']='passed'
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
