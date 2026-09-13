"""Seek an exact witness on new midpoint fibers of the pending d5a2 cover.

A rational SAT matrix must be reconstructed; no rank claim is assumed.
Stop on the first nonsingular SAT matrix. This is Y-width, not global width.
"""
from fractions import Fraction as Q
from pathlib import Path
from itertools import product
from math import floor,ceil,gcd,prod
import json,time
import z3
from experiments.contact_height_charts import height_model
from experiments.contact_contraction_trace_probe import certify,ell

ROOT=Path(__file__).resolve().parents[1]


def inverse(A):
    n=len(A);M=[list(map(Q,row))+[Q(int(i==j)) for j in range(n)] for i,row in enumerate(A)]
    for j in range(n):
        pivot=next((i for i in range(j,n) if M[i][j]),None)
        if pivot is None:raise ValueError('singular matrix')
        M[j],M[pivot]=M[pivot],M[j];scale=M[j][j];M[j]=[x/scale for x in M[j]]
        for i in range(n):
            if i!=j:
                scale=M[i][j];M[i]=[x-scale*y for x,y in zip(M[i],M[j])]
    return [row[n:] for row in M]


def main():
    G=json.loads((ROOT/'certificates/nonunimodular_observer_guards.json').read_text())
    S=json.loads((ROOT/'results/two_vector_class_scan.json').read_text())
    D=json.loads((ROOT/'results/det5_height_interval.json').read_text())
    C=next(c for c in G['classes'] if c['class_index']==5);scan=next(c for c in S['classes'] if c['class_index']==5)
    chart=next(c for c in D['charts'] if c['class_index']==5 and c['extrema']==[1,0])
    ext=chart['extrema'];free=[i for i in range(4) if i not in ext]
    archive=ROOT/'results/det5_height_fiber_witness.json'
    records=json.loads(archive.read_text())['queries'] if archive.exists() else []
    if any(r.get('invertible') for r in records):
        print('Archived witness already exists; no repeated query');return
    for number,leaf in enumerate(chart['pending_leaves'][:16]):
        if number<len(records):continue
        mid=[sum(map(Q,pair))/2 for pair in leaf['box']]
        base,F,q,a,b,_=height_model(C,scan,ext)
        subs=[(q[i],z3.RealVal(str(value))) for i,value in zip(free,mid)]
        solver=z3.SolverFor('QF_LRA');solver.set(timeout=1000)
        solver.add(*[z3.simplify(z3.substitute(e,*subs),som=True) for e in base.assertions()])
        path=f'results/det5_fiber_{number}.smt2';(ROOT/path).write_text(solver.to_smt2())
        start=time.monotonic();status=solver.check();elapsed=time.monotonic()-start
        row={'class_index':5,'extrema':ext,'midpoint_heights':list(map(str,mid)),'source_node':leaf['node'],
             'path':path,'status':str(status),'elapsed_seconds':elapsed,'timeout_ms':1000}
        found=False
        if status==z3.sat:
            model=solver.model();matrix=[[model.eval(v,model_completion=True).as_fraction() for v in r] for r in F]
            row['F']=[[str(x) for x in r] for r in matrix];row['offset']=str(model.eval(a).as_fraction());row['gap']=str(model.eval(b).as_fraction())
            try:T=inverse(matrix)
            except (ValueError,ZeroDivisionError):row['invertible']=False
            else:
                row['invertible']=True;P=C['contact_points'];V=[[sum(Q(P[i][k])*T[i][j] for i in range(4)) for k in range(3)] for j in range(4)]
                boxcount=prod(max(0,floor(max(v[k] for v in V))-ceil(min(v[k] for v in V))+1) for k in range(3))
                row['integer_body_box_count']=boxcount
                if boxcount<=50000:
                    row['exact_body']=certify(matrix,P)
                    bounds=[floor(max(v[k] for v in V)-min(v[k] for v in V)) for k in range(3)]
                    if prod(2*x+1 for x in bounds)<=100000:
                        minimum=Q(1);best=[]
                        for z in product(*(range(-x,x+1) for x in bounds)):
                            if not any(z) or next(x for x in z if x)<0 or gcd(*z)!=1:continue
                            l=ell(z,5,2);gamma=sum(abs(sum(matrix[i][j]*l[j] for j in range(4))) for i in range(4))/2
                            if gamma<minimum:minimum=gamma;best=[z]
                            elif gamma==minimum:best.append(z)
                        row['full_difference_minimum']=str(minimum);row['minimizing_vectors']=best
                found=True
        elif status==z3.unknown:row['reason_unknown']=solver.reason_unknown()
        records.append(row)
        (ROOT/'results/det5_height_fiber_witness.json').write_text(json.dumps({
            'scope':'New exact midpoint fibers of a pending d5a2 outer cover. A SAT height witness need not have global width>17/5; any listed global minimum is checked over its full difference box.',
            'z3_version':z3.get_version_string(),'queries':records},indent=2)+'\n')
        print(json.dumps({k:row[k] for k in ('source_node','midpoint_heights','status','elapsed_seconds')}),flush=True)
        if found:break


if __name__=='__main__':main()
