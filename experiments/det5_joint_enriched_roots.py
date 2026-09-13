"""Strengthen the nine open joint charts by a witnessed missing gauge orbit.

The 27 already closed charts are not queried. New full-square targets add
four necessary global gauges, so differ from all previous root formulas.
"""
from fractions import Fraction as Q
from itertools import product
from math import floor,gcd,prod
from pathlib import Path
import hashlib,json,time
import z3
from experiments.det5_joint_volume_gaps import gap_make,inspect_matrix
from experiments.det5_height_fiber_witness import inverse
from experiments.contact_contraction_trace_probe import ell

ROOT=Path(__file__).resolve().parents[1]
ARCHIVE=ROOT/'results/det5_joint_enriched_roots.json'
VECTORS=[(1,-1,1),(2,1,1),(3,1,0),(6,1,2)]
BETA=Q(183,500)


def enriched_make(C,S,ye,ue,box):
    values=gap_make(C,S,ye,ue,box);solver,F=values[:2]
    for v in VECTORS:
        l=ell(v,5,2)
        z=[sum(F[i][j]*z3.RealVal(str(l[j])) for j in range(4)) for i in range(4)]
        solver.add(z3.Or(*[sum(z[i] for i in range(4) if mask&(1<<i))>z3.RealVal(str(BETA)) for mask in range(1,15)]))
    return values


def missing_gauge(matrix,P):
    try:T=inverse(matrix)
    except ValueError:return {'invertible':False}
    V=[[sum(Q(P[i][k])*T[i][j] for i in range(4)) for k in range(3)] for j in range(4)]
    bounds=[floor(BETA*(max(v[k] for v in V)-min(v[k] for v in V))) for k in range(3)]
    count=prod(2*b+1 for b in bounds)
    if count>100000:return {'invertible':True,'box_bounds':bounds,'box_count':count,'status':'search_cap'}
    bad=[]
    for v in product(*(range(-b,b+1) for b in bounds)):
        if not any(v) or gcd(*v)!=1 or next(x for x in v if x)<0:continue
        l=ell(v,5,2);g=sum(abs(sum(matrix[i][j]*l[j] for j in range(4))) for i in range(4))/2
        if g<=BETA:bad.append({'vector':v,'gauge':str(g)})
    bad.sort(key=lambda v:Q(v['gauge']))
    return {'invertible':True,'box_bounds':bounds,'box_count':count,'status':'complete_threshold_check','violations':bad}


def main():
    source=ROOT/'results/det5_joint_round2.json';raw=source.read_bytes();seed=json.loads(raw)
    C=next(c for c in json.loads((ROOT/'certificates/nonunimodular_observer_guards.json').read_text())['classes'] if c['class_index']==5)
    S=next(c for c in json.loads((ROOT/'results/two_vector_class_scan.json').read_text())['classes'] if c['class_index']==5)
    data=json.loads(ARCHIVE.read_text()) if ARCHIVE.exists() else {
        'scope':'Four new global-gauge cuts on whole root boxes of nine previously open joint charts. Prior closed charts not re-queried; root SAT is a relaxation only.',
        'source_sha256':hashlib.sha256(raw).hexdigest(),'source_path':str(source.relative_to(ROOT)),
        'extra_gauge_vectors':VECTORS,'beta':str(BETA),'queries':[]}
    if data['source_sha256']!=hashlib.sha256(raw).hexdigest():raise ValueError('source changed')
    for chart in seed['charts']:
        if chart['complete_cover']:continue
        ye,ue=chart['Y_extrema'],chart['U_extrema']
        if any(r['Y_extrema']==ye and r['U_extrema']==ue for r in data['queries']):continue
        box=[[Q(0),Q(1)] for _ in range(4)]
        solver,F,*_=enriched_make(C,S,ye,ue,box)
        path=f'results/det5_joint_enriched_{ye[0]}_{ye[1]}_{ue[0]}_{ue[1]}_root.smt2'
        smt=solver.to_smt2().encode();(ROOT/path).write_bytes(smt)
        start=time.monotonic();status=solver.check()
        row={'Y_extrema':ye,'U_extrema':ue,'box':[['0','1'] for _ in range(4)],'path':path,
             'input_sha256':hashlib.sha256(smt).hexdigest(),'status':str(status),
             'elapsed_seconds':time.monotonic()-start,'timeout_ms':1000}
        if status==z3.unknown:row['reason_unknown']=solver.reason_unknown()
        data['queries'].append(row)
        if status==z3.sat:
            m=solver.model();matrix=[[m.eval(v,model_completion=True).as_fraction() for v in r] for r in F]
            row['F']=[[str(x) for x in r] for r in matrix]
            ARCHIVE.write_text(json.dumps(data,indent=2)+'\n')
            row['actual_matrix']=inspect_matrix(matrix,C['contact_points'])
            row['missing_global_gauges']=missing_gauge(matrix,C['contact_points'])
        ARCHIVE.write_text(json.dumps(data,indent=2)+'\n')
        print(json.dumps({k:row[k] for k in ('Y_extrema','U_extrema','status','elapsed_seconds')}),flush=True)
    if source.read_bytes()!=raw:raise ValueError('source modified')


if __name__=='__main__':main()
