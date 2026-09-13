"""Full rational replay of the d5a2 Y-width witness; no generator/core/solver."""
from fractions import Fraction as Q
from pathlib import Path
from itertools import product
from math import floor,ceil,gcd
from copy import deepcopy
import json
from replay_det13_contraction_independent import solve,need
from replay_weighted_trace_independent import inv,determinant,qvalue
from replay_two_vector_scan_independent import radical_sign

ROOT=Path(__file__).resolve().parents[1]


def replay(data,weak_failure=True):
    rows=[r for r in data['queries'] if r['status']=='sat'];need(len(rows)==1,'one archived exact witness')
    R=rows[0];F=[list(map(Q,row)) for row in R['F']]
    need(all(F[i][i]==0 for i in range(4)),'facet diagonal')
    need(all(F[i][j]>0 for i in range(4) for j in range(4) if i!=j),'relative facet interiors')
    need(all(sum(F[i][j] for i in range(4))==1 for j in range(4)),'column stochasticity')
    P=((0,0,0),(5,1,2),(0,1,0),(0,0,1));T=inv(F)
    V=[[sum(Q(P[i][k])*T[i][j] for i in range(4)) for k in range(3)] for j in range(4)]
    body=R['exact_body'];need([[qvalue(x) for x in r] for r in body['vertices']]==V,'vertex binding')
    A=[[Q(1)]*4]+[[Q(p[k]) for p in P] for k in range(3)]
    def coords(v,affine=False):
        l=solve(A,[Q(int(affine)),*map(Q,v)])
        return [sum(F[i][j]*l[j] for j in range(4)) for i in range(4)]
    bounds=[(ceil(min(v[k] for v in V)),floor(max(v[k] for v in V))) for k in range(3)]
    boundary=[];count=0
    for z in product(*(range(l,h+1) for l,h in bounds)):
        c=coords(z,True);count+=1;need(min(c)<=0,'no interior lattice point')
        if min(c)==0:boundary.append(list(z))
    need(body['hollow']['hollow'] and body['hollow']['boundary_points']==boundary,'full boundary list')
    D=[[V[i][k]-V[0][k] for k in range(3)] for i in range(1,4)];Di=inv(D)
    need(qvalue(body['volume'])==abs(determinant(D))/6,'exact volume')
    upper=min(max(v[k] for v in V)-min(v[k] for v in V) for k in range(3))
    limits=[floor(upper*sum(map(abs,row))) for row in Di];best=upper;minimizers=[]
    for u in product(*(range(-b,b+1) for b in limits)):
        if not any(u) or next(x for x in u if x)<0 or gcd(*u)!=1:continue
        vals=[sum(x*y for x,y in zip(u,v)) for v in V];w=max(vals)-min(vals)
        if w<best:best=w;minimizers=[list(u)]
        elif w==best:minimizers.append(list(u))
    need(qvalue(body['width']['width'])==best and body['width']['minimizing_directions_mod_sign']==minimizers,'complete width')
    Yspan=max(v[1] for v in V)-min(v[1] for v in V)
    need(Yspan==1/Q(R['gap']) and Yspan>Q(17,5)>best,'directional/global distinction')
    q=[(v[1]-min(w[1] for w in V))/Yspan for v in V]
    need(q.index(0)==R['extrema'][0] and q.index(1)==R['extrema'][1],'extrema binding')
    need([q[i] for i in range(4) if i not in R['extrema']]==list(map(Q,R['midpoint_heights'])),'exact fiber')
    need(Q(R['offset'])==-min(v[1] for v in V)/Yspan,'height offset')
    dbounds=[floor(max(v[k] for v in V)-min(v[k] for v in V)) for k in range(3)];minimum=Q(1);vectors=[]
    for z in product(*(range(-b,b+1) for b in dbounds)):
        if not any(z) or next(x for x in z if x)<0 or gcd(*z)!=1:continue
        g=sum(map(abs,coords(z)))/2
        if g<minimum:minimum=g;vectors=[list(z)]
        elif g==minimum:vectors.append(list(z))
    need(minimum==Q(R['full_difference_minimum']) and vectors==R['minimizing_vectors'],'full difference minimum')
    need(minimum>Q(37,102),'coarse gauge threshold')
    if weak_failure:
        need(minimum<Q(183,500),'valid stronger cut failed')
    else:
        need(minimum>Q(183,500),'strong rational cut passed')
        need(radical_sign(1-Q(17,5)*(1-minimum),Q(2,3))>0,
             'full minimum exceeds exact ACMS necessity at target17/5')
    return {'Y_width':str(Yspan),'lattice_width':str(best),'full_difference_minimum':str(minimum),
            'minimum_vectors':vectors,'lattice_points_checked':count,'boundary_points':len(boundary)}


def main():
    data=json.loads((ROOT/'results/det5_height_fiber_witness.json').read_text());result=replay(data)
    strong=json.loads((ROOT/'results/det5_strong_fiber.json').read_text())
    normalized={**strong,'midpoint_heights':strong['fixed_heights'],'exact_body':strong['body']}
    strong_result=replay({'queries':[normalized]},False)
    for mutation in ('matrix','width','minimum'):
        d=deepcopy(data);r=next(r for r in d['queries'] if r['status']=='sat')
        if mutation=='matrix':r['F'][0][1]='0'
        elif mutation=='width':r['exact_body']['width']['width']['a']='4'
        else:r['full_difference_minimum']='1/2'
        try:replay(d)
        except (ValueError,KeyError,ZeroDivisionError):continue
        raise ValueError('accepted '+mutation+' corruption')
    print(json.dumps({'status':'PASS','weak_witness':result,'strong_witness':strong_result,
                      'rejected_mutations':3,'solver_queries_run':0},indent=2))


if __name__=='__main__':main()
