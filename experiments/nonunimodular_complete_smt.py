"""Bounded complete cubic targets for determinant-seven/eight contact classes.

Target 17/5 only. Ten primitive covectors suffice because P is contained
in K and every omitted direction has integer width on P at least four.
All six contact-edge gauges are imposed for the exact observer guard list.
"""
from fractions import Fraction as Q
from itertools import product
from math import gcd
from pathlib import Path
import json
import time
import z3
from experiments.det2_adjugate_smt import determinant4, signed_adjugate

ROOT=Path(__file__).resolve().parents[1]
TARGET=Q(17,5)
BETA=Q(37,102)


def rat(x):return z3.RealVal(str(x))


def ell(v,d,a,affine=False):
    x,y,z=map(Q,v)
    return ((1 if affine else 0)+a*x/d-y-z,x/d,y-x/d,z-a*x/d)


def width_directions(d,a):
    directions=set()
    for h,y,z in product(range(-3,4),repeat=3):
        if max(0,h,y,z)-min(0,h,y,z)>3 or (h-y-a*z)%d:
            continue
        u=((h-y-a*z)//d,y,z)
        if not any(u) or gcd(*u)!=1:
            continue
        if next(x for x in u if x)<0:u=tuple(-x for x in u)
        directions.add(u)
    return sorted(directions)


def make(C,scan,threshold=TARGET):
    d=C['normalized_volume'];a=C['contact_points'][1][2]
    x=z3.Reals('x0 x1 x2 x3');y=z3.Reals('y0 y1 y2 y3')
    F=[[rat(0) for j in range(4)] for i in range(4)]
    for j in range(4):
        ids=[i for i in range(4) if i!=j]
        for i,value in zip(ids,(x[j],y[j],1-x[j]-y[j])):F[i][j]=value
    solver=z3.SolverFor('QF_NRA');solver.set(timeout=10000)
    solver.add(*[F[i][j]>0 for i in range(4) for j in range(4) if i!=j])
    delta=z3.simplify(determinant4(F),som=True)
    S=[[z3.simplify(v,som=True) for v in row] for row in signed_adjugate(F)]
    abs_delta=z3.If(delta>0,delta,-delta)
    # vol(K)=d/(6|det F|), vol(K)<1/beta^3 is a necessary ACMS cut.
    solver.add(abs_delta>rat(Q(d,6)*BETA**3))
    vectors=sorted(set(map(tuple,C['primitive_contact_edge_directions'])) |
                   {tuple(r['vector']) for r in scan['eligible_vectors']})
    for v in vectors:
        l=ell(v,d,a)
        values=[sum(F[i][j]*rat(l[j]) for j in range(4)) for i in range(4)]
        solver.add(z3.Or(*[sum(values[i] for i in range(4) if mask&(1<<i))>rat(BETA) for mask in range(1,15)]))
    for v in C['guards']:
        l=ell(v,d,a,True)
        solver.add(z3.Or(*[sum(F[i][j]*rat(l[j]) for j in range(4))<=0 for i in range(4)]))
    directions=width_directions(d,a)
    for u in directions:
        values=[sum(p[k]*u[k] for k in range(3)) for p in C['contact_points']]
        differences=[z3.simplify(sum(values[i]*(S[i][j]-S[i][k]) for i in range(4)),som=True)
                     for j in range(4) for k in range(j+1,4)]
        solver.add(z3.Or(*[sign*N>rat(threshold)*abs_delta for N in differences for sign in (-1,1)]))
    return solver,F,delta,directions,vectors


def controls(C,scan):
    sigma=(1,0,3,2)
    pin=[[Q(0) if i==j else Q(499,500) if i==sigma[j] else Q(1,1000) for j in range(4)] for i in range(4)]
    outcomes=[]
    for W in (Q(1),TARGET):
        solver,F,_,_,_=make(C,scan,W)
        solver.add(*[F[i][j]==rat(pin[i][j]) for i in range(4) for j in range(4)])
        status=solver.check();outcomes.append(str(status))
    if outcomes!=['sat','unsat']:raise ValueError('nontrivial exact controls failed: '+repr(outcomes))
    return {'F':[[str(x) for x in r] for r in pin],
            'width_one_control':outcomes[0],'target_width_control':outcomes[1],
            'scope':'Lower-threshold pin is a control only; all completeness claims concern target 17/5.'}


def main():
    guards=json.loads((ROOT/'certificates/nonunimodular_observer_guards.json').read_text())
    scans=json.loads((ROOT/'results/two_vector_class_scan.json').read_text())
    output=[]
    for idx in (6,7):
        C=next(c for c in guards['classes'] if c['class_index']==idx)
        scan=next(c for c in scans['classes'] if c['class_index']==idx)
        pins=controls(C,scan)
        solver,F,delta,directions,vectors=make(C,scan)
        (ROOT/f'results/nonunimodular_complete_class_{idx}.smt2').write_text(solver.to_smt2())
        start=time.monotonic();status=solver.check();elapsed=time.monotonic()-start
        row={'class_index':idx,'determinant':C['normalized_volume'],'target':str(TARGET),
             'beta':str(BETA),'real_variable_count':8,'width_directions':directions,
             'width_direction_count':len(directions),'gauge_vectors':vectors,
             'guard_count':len(C['guards']),'controls':pins,
             'status':str(status),'elapsed_seconds':elapsed,'timeout_ms':10000}
        if status==z3.unknown:row['reason_unknown']=solver.reason_unknown()
        if status==z3.sat:
            row['model']={str(v):str(solver.model()[v]) for v in solver.model()}
            row['warning']='Requires separate exact whole-body reconstruction and independent validation.'
        output.append(row)
        print(json.dumps({k:row[k] for k in ('class_index','status','elapsed_seconds','width_direction_count')}),flush=True)
    (ROOT/'results/nonunimodular_complete_smt.json').write_text(json.dumps({
        'scope':'Complete hollow tetrahedron targets in the specified relative-interior facet-contact charts at width 17/5, with necessary rational ACMS cuts. UNKNOWN is not infeasibility; any SAT requires independent reconstruction.',
        'z3_version':z3.get_version_string(),'results':output},indent=2)+'\n')


if __name__=='__main__':main()
