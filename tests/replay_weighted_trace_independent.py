"""Independent exact weighted bounds and full trace-counterexample checks.

No generator, solver or geometry-core imports. Gaussian elimination and
radical comparisons come from earlier independent verifiers.
"""
from fractions import Fraction as Q
from itertools import permutations, product
from math import floor, ceil, gcd
from copy import deepcopy
from pathlib import Path
import json
from replay_det13_contraction_independent import solve, need
from replay_two_vector_scan_independent import radical_sign

ROOT=Path(__file__).resolve().parents[1]


def inv(A):
    cols=[solve(A,[int(i==j) for i in range(len(A))]) for j in range(len(A))]
    return list(map(list,zip(*cols)))


def determinant(A):
    n=len(A);result=Q(0)
    for p in permutations(range(n)):
        term=Q((-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n)))
        for i in range(n):term*=A[i][p[i]]
        result+=term
    return result


def qvalue(x):
    need(Q(x['b'])==0,'rational value required')
    return Q(x['a'])


def weighted(data):
    scan=json.loads((ROOT/'results/two_vector_class_scan.json').read_text())
    need(len(data['classes'])==10,'weighted class coverage')
    count=0;best_bounds={}
    for C,S in zip(data['classes'],scan['classes']):
        need(C['class_index']==S['class_index'],'weighted class index')
        expected={}
        for pair in S['all_eligible_pairs']:
            rows=[list(map(Q,r)) for r in pair['difference_barycentrics']]
            m1,m2=[min(map(abs,r)) for r in rows]
            a1,a2=[sum(map(abs,r))/2 for r in rows]
            for t in (Q(0),m2/(m1+m2),Q(1)):
                m=min(t*m1,(1-t)*m2);mass=t*a1+(1-t)*a2
                D=1+m-mass
                expected[(tuple(map(tuple,pair['vectors'])),(t,1-t))]=(m,mass,((1+m)/D,Q(2,3)/D))
        candidates=C['all_weight_candidates'];need(len(candidates)==len(expected),'three exact weight candidates per pair')
        seen=set();previous=None
        for r in candidates:
            key=tuple(map(tuple,r['vectors'])),tuple(map(Q,r['weights']))
            need(key in expected and key not in seen,'weight candidate coverage');seen.add(key)
            m,mass,bound=expected[key]
            need(Q(r['weighted_mass'])==mass and Q(r['mismatch_coefficient'])==m,'weighted loss constants')
            need(r['kind']==('intrinsic_endpoint' if not m else 'balanced'),'endpoint scope')
            need(r['bound']['d']==3 and (Q(r['bound']['a']),Q(r['bound']['b']))==bound,'weighted bound')
            if previous:need(radical_sign(bound[0]-previous[0],bound[1]-previous[1])>=0,'exact weighted order')
            previous=bound
        need(C['best']==(candidates[0] if candidates else None),'best recorded weights')
        if candidates:best_bounds[C['determinant']]=candidates[0]['bound']
        count+=len(candidates)
    need(best_bounds[8]=={'a':'13/7','b':'8/7','d':3},'determinant-eight weighted bound')
    return {'weight_candidates':count,'best_bounds':best_bounds}


def trace(data,strict):
    contacts=json.loads((ROOT/'certificates/nonunimodular_observer_guards.json').read_text())
    summaries=[]
    need(len(data['results'])==2,'two trace classes')
    for R in data['results']:
        need(R['status']=='sat','archived rational model required')
        C=next(c for c in contacts['classes'] if c['class_index']==R['class_index'])
        P=C['contact_points'];F=[list(map(Q,r)) for r in R['F']]
        need(all(F[i][i]==0 for i in range(4)),'facet contact diagonal')
        need(all(F[i][j]>0 for i in range(4) for j in range(4) if i!=j),'relative facet interiors')
        need(all(sum(F[i][j] for i in range(4))==1 for j in range(4)),'column normalization')
        det=determinant(F);need(det!=0,'bounded invertible chart')
        T=inv(F)
        V=[[sum(Q(P[i][k])*T[i][j] for i in range(4)) for k in range(3)] for j in range(4)]
        body=R['exact_body']
        need([[qvalue(x) for x in r] for r in body['vertices']]==V,'exact vertex reconstruction')
        need(Q(body['determinant'])==det,'determinant binding')
        matching=max(sum(F[p[j]][j] for j in range(4)) for p in permutations(range(4)))
        need(Q(body['maximum_permutation_trace'])==matching and Q(body['minimum_total_off_permutation_mass'])==4-matching,'all permutation traces')
        need(matching<Q(56,17) if strict else matching<=Q(56,17),'strict trace obstruction')
        affine=[[1]*4]+[[p[k] for p in P] for k in range(3)]
        def coords(v,point=False):
            l=solve(affine,[int(point),*v])
            return [sum(F[i][j]*l[j] for j in range(4)) for i in range(4)]
        beta=Q(R['beta']);need(beta==Q(37,102),'gauge threshold')
        for z in R['gauge_vectors']:need(sum(map(abs,coords(z)))/2>beta,'every recorded gauge')
        for z in C['guards']:need(min(coords(z,True))<=0,'every complete observer exclusion')
        bbox=[(ceil(min(v[k] for v in V)),floor(max(v[k] for v in V))) for k in range(3)]
        boundary=[];checked=0
        for z in product(*(range(a,b+1) for a,b in bbox)):
            c=coords(z,True);checked+=1
            need(min(c)<=0,'no integer interior point in full body box')
            if min(c)==0:boundary.append(list(z))
        need(body['hollow']['hollow'] and body['hollow']['interior_points']==[],'hollow result')
        need(body['hollow']['boundary_points']==boundary,'complete boundary list')
        # Independent complete lattice-width bound using a vertex frame.
        D=[[V[i][k]-V[0][k] for k in range(3)] for i in range(1,4)]
        Di=inv(D)
        upper=min(max(v[k] for v in V)-min(v[k] for v in V) for k in range(3))
        limits=[floor(upper*sum(map(abs,r))) for r in Di]
        best=upper;minimizers=[];direction_count=0
        for u in product(*(range(-b,b+1) for b in limits)):
            if not any(u) or next(x for x in u if x)<0 or gcd(*u)!=1:continue
            direction_count+=1
            values=[sum(x*y for x,y in zip(u,v)) for v in V];w=max(values)-min(values)
            if w<best:best=w;minimizers=[list(u)]
            elif w==best:minimizers.append(list(u))
        need(qvalue(body['width']['width'])==best,'complete width replay')
        need(body['width']['minimizing_directions_mod_sign']==minimizers,'all width minimizers')
        # An integer contact edge gives gamma<=1. Thus the whole K-K box
        # suffices for its first lattice minimum; no finite screen inference.
        dbounds=[floor(max(v[k] for v in V)-min(v[k] for v in V)) for k in range(3)]
        minimum=Q(1);vectors=[]
        for z in product(*(range(-b,b+1) for b in dbounds)):
            if not any(z) or next(x for x in z if x)<0 or gcd(*z)!=1:continue
            g=sum(map(abs,coords(z)))/2
            if g<minimum:minimum=g;vectors=[list(z)]
            elif g==minimum:vectors.append(list(z))
        need(minimum>beta,'global difference minimum exceeds the probe threshold')
        if strict and C['normalized_volume']==8:
            need(radical_sign(1-Q(17,5)*(1-minimum),Q(2,3))>0,
                 'determinant-eight example exceeds the sharper ACMS gauge threshold at 17/5')
        summaries.append({'class_index':R['class_index'],'width':str(best),
                          'integer_points_checked':checked,'width_directions_checked':direction_count,
                          'total_leakage':str(4-matching),'global_difference_minimum':str(minimum),
                          'minimum_vectors':vectors,'difference_box_bounds':dbounds})
    return summaries


def main():
    W=json.loads((ROOT/'certificates/weighted_two_vector_bounds.json').read_text())
    A=json.loads((ROOT/'results/contact_contraction_trace_probe.json').read_text())
    B=json.loads((ROOT/'results/contact_contraction_trace_probe_strict.json').read_text())
    result={'weighted':weighted(W),'nonstrict_trace_models':trace(A,False),'strict_trace_models':trace(B,True)}
    mutations=[('weight',lambda d:d['classes'][7]['all_weight_candidates'][0]['bound'].__setitem__('a','12/7')),
               ('trace',lambda d:d['results'][0]['F'][0].__setitem__(1,'1')),
               ('trace',lambda d:d['results'][0]['exact_body']['width']['width'].__setitem__('a','4')),
               ('trace',lambda d:d['results'][1]['exact_body'].__setitem__('minimum_total_off_permutation_mass','1/2'))]
    for kind,mutate in mutations:
        damaged=deepcopy(W if kind=='weight' else B);mutate(damaged)
        try:
            weighted(damaged) if kind=='weight' else trace(damaged,True)
        except (ValueError,KeyError,IndexError,TypeError):continue
        raise ValueError('corrupted artifact accepted')
    print(json.dumps({'status':'PASS',**result,'rejected_mutations':len(mutations)},indent=2))


if __name__=='__main__':main()
