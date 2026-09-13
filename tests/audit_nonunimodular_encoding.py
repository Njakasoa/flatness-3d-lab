"""Read-only encoding audit; deliberately never calls Solver.check()."""
from fractions import Fraction as Q
from itertools import product
from math import gcd
from pathlib import Path
import json
import sys
import z3

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from experiments.nonunimodular_complete_smt import make
from replay_det13_contraction_independent import solve, need
from replay_weighted_trace_independent import determinant


def degree(e):
    if z3.is_rational_value(e):return 0
    if z3.is_const(e):return 1
    k=e.decl().kind();args=e.children()
    if k in (z3.Z3_OP_ADD,z3.Z3_OP_SUB):return max(map(degree,args))
    if k==z3.Z3_OP_MUL:return sum(map(degree,args))
    if k==z3.Z3_OP_UMINUS:return degree(args[0])
    if k==z3.Z3_OP_POWER:return degree(args[0])*args[1].as_long()
    if k==z3.Z3_OP_ITE:return max(degree(args[1]),degree(args[2]))
    raise ValueError('Unexpected arithmetic node: '+str(e))


def max_polynomial_degree(e):
    if e.sort().kind()==z3.Z3_REAL_SORT:
        return degree(e)
    return max([max_polynomial_degree(c) for c in e.children()]+[0])


def main():
    guards=json.loads((ROOT/'certificates/nonunimodular_observer_guards.json').read_text())
    scans=json.loads((ROOT/'results/two_vector_class_scan.json').read_text())
    archive=json.loads((ROOT/'results/nonunimodular_complete_smt.json').read_text())
    rows=[]
    for R in archive['results']:
        C=next(c for c in guards['classes'] if c['class_index']==R['class_index'])
        S=next(c for c in scans['classes'] if c['class_index']==R['class_index'])
        p0=C['contact_points'][0]
        matrix=[[p[k]-p0[k] for k in range(3)] for p in C['contact_points'][1:]]
        directions=set()
        for h in product(range(-3,4),repeat=3):
            if max(0,*h)-min(0,*h)>3:continue
            u=solve(matrix,h)
            if any(v.denominator!=1 for v in u):continue
            u=tuple(map(int,u))
            if not any(u) or gcd(*u)!=1:continue
            if next(v for v in u if v)<0:u=tuple(-v for v in u)
            directions.add(u)
        need(sorted(directions)==list(map(tuple,R['width_directions'])) and len(directions)==10,'independent complete covectors')
        solver,F,delta,dirs,_=make(C,S)
        path=ROOT/f"results/nonunimodular_complete_class_{R['class_index']}.smt2"
        archived=z3.parse_smt2_string(path.read_text())
        need(len(archived)==len(solver.assertions()),'archived assertion count')
        for old,new in zip(archived,solver.assertions()):
            need(z3.eq(z3.simplify(old,som=True),z3.simplify(new,som=True)),
                 'parsed archived target equals inspected encoding')
        need(degree(delta)==3,'cubic determinant')
        need(max(max_polynomial_degree(a) for a in solver.assertions())==3,'cubic assertions')
        variables={}
        def walk(e):
            if z3.is_const(e) and e.decl().kind()==z3.Z3_OP_UNINTERPRETED:variables[str(e)]=e
            for c in e.children():walk(c)
        for e in solver.assertions():walk(e)
        need(len(variables)==8,'eight real parameters')
        pin=[list(map(Q,row)) for row in R['controls']['F']]
        substitution=[]
        for j in range(4):
            ids=[i for i in range(4) if i!=j]
            substitution.extend([(variables[f'x{j}'],z3.RealVal(str(pin[ids[0]][j]))),
                                 (variables[f'y{j}'],z3.RealVal(str(pin[ids[1]][j])))])
        det_pin=z3.simplify(z3.substitute(delta,*substitution)).as_fraction()
        need(det_pin==determinant(pin),'independent pinned determinant')
        false_counts=[]
        for W in (Q(1),Q(17,5)):
            check,_,_,_,_=make(C,S,W)
            evaluations=[z3.simplify(z3.substitute(e,*substitution)) for e in check.assertions()]
            need(all(z3.is_true(v) or z3.is_false(v) for v in evaluations),'exact closed pin evaluation')
            false_counts.append(sum(z3.is_false(v) for v in evaluations))
        need(false_counts[0]==0 and false_counts[1]>0,'nontrivial pin controls without solver')
        need(R['status']=='unknown','reported bounded target outcome')
        rows.append({'class_index':R['class_index'],'variables':8,'maximum_degree':3,
                     'complete_width_directions':10,'guards':len(C['guards']),
                     'pin_false_constraint_counts':false_counts,'target_status':'unknown'})
    print(json.dumps({'status':'PASS','solver_queries_run':0,'models':rows,
                     'scope':'Encoding and exact arithmetic audit, not independent mathematical peer review or infeasibility proof.'},indent=2))


if __name__=='__main__':main()
