"""Shared static and perspective product envelopes on certified residual domains.

No archived target is rerun: each model adds directional coupling and exact
complements of certified closed Y rectangles. SAT is outer feasibility only.
"""
from fractions import Fraction as Q
from pathlib import Path
from itertools import combinations
import argparse, hashlib, json, time
import z3
from experiments.det5_scaled_pending_transfer import strengthened,U
from experiments.det5_scaled_width_frame import inputs,rat,R,TARGET,GAP_MIN,GAP_MAX,ROOT,inspect
from experiments.nonunimodular_complete_smt import width_directions
OUT=ROOT/'results/det5_coupled_scaled_frame.json'


def intervals(ext,box):
    out=[None]*4;out[ext[0]]=(Q(0),Q(0));out[ext[1]]=(Q(1),Q(1))
    for i,iv in zip([i for i in range(4)if i not in ext],box):out[i]=tuple(map(Q,iv))
    return out


def bounds(C,chart,leaf,i,u):
    """Bounds on u.T_i, including Y and U interval correlations."""
    L=chart['Y_extrema'][0];q=intervals(chart['Y_extrema'],leaf['box'][:2]);rs=intervals(chart['U_extrema'],leaf['box'][2:])
    ph=[sum(u[k]*p[k]for k in range(3))for p in C['contact_points']];cap=R*(max(ph)-min(ph))
    lo,hi=-cap*GAP_MAX,cap*GAP_MAX
    if i==L:return Q(0),Q(0),cap
    if tuple(u)==(0,1,0):return q[i][0],q[i][1],cap
    dlo,dhi=rs[i][0]-rs[L][1],rs[i][1]-rs[L][0]
    vals=[d*x for d in(dlo,dhi)for x in(TARGET*GAP_MIN,2*R*GAP_MAX)]
    ulo,uhi=min(vals),max(vals)
    if tuple(u)==U:lo,hi=max(lo,ulo),min(hi,uhi)
    if tuple(u)==(1,-2,-2):lo,hi=max(lo,ulo-q[i][1]),min(hi,uhi-q[i][0])
    if lo>hi:raise ValueError('inconsistent valid interval')
    return lo,hi,cap


def make(C,S,chart,leaf):
    s,F,T,b,products=strengthened(C,S,chart,leaf);L,H=chart['Y_extrema']
    before=len(s.assertions())
    # Every old certified rectangle is closed; its complement is strict.
    cert=json.loads((ROOT/'results/det5_class5_y_cvc5_validation.json').read_text())
    qfree=[i for i in range(4)if i not in chart['Y_extrema']]
    excluded=[]
    for r in cert['leaves']:
        if r['extrema']!=chart['Y_extrema']:continue
        clause=z3.Or(*[atom for i,(lo,hi)in zip(qfree,r['box'])for atom in(T[i][1]<rat(Q(lo)),T[i][1]>rat(Q(hi)))])
        s.add(clause);excluded.append(r['node'])
    # Eight independent tau=bF; the third off-diagonal entry enforces sum_i tau=b.
    tau={}
    for j in range(4):
        ids=[i for i in range(4)if i!=j];tau[j,j]=rat(0)
        tau[ids[0],j]=z3.Real(f'tau{ids[0]}_{j}');tau[ids[1],j]=z3.Real(f'tau{ids[1]}_{j}')
        tau[ids[2],j]=b-tau[ids[0],j]-tau[ids[1],j]
        for i in ids:
            f=F[i][j];t=tau[i,j]
            s.add(t>=rat(GAP_MIN)*f,t<=rat(GAP_MAX)*f,
                  t>=b+rat(GAP_MAX)*f-rat(GAP_MAX),t<=b+rat(GAP_MIN)*f-rat(GAP_MIN))
    def w(i,j,k):
        if i==j or i==L:return rat(0)
        if k==1 and i==H:return F[i][j]
        return z3.Real(f'w{i}_{j}_{k}')
    interval_records=[]
    for i in range(4):
        for u in width_directions(5,2):
            lo,hi,cap=bounds(C,chart,leaf,i,u)
            g=sum(u[k]*T[i][k]for k in range(3));s.add(g>=rat(lo),g<=rat(hi))
            interval_records.append({'vertex':i,'direction':list(u),'bounds':[str(lo),str(hi)],'homogeneous_cap':str(cap)})
            for j in range(4):
                if i==j:continue
                f=F[i][j];z=sum(u[k]*w(i,j,k)for k in range(3));t=tau[i,j]
                # f in [0,1], static interval [lo,hi].
                s.add(z>=rat(lo)*f,z>=g+rat(hi)*f-rat(hi),z<=g+rat(lo)*f-rat(lo),z<=rat(hi)*f)
                # -cap*b<=g<=cap*b, sharing the same tau and vector W.
                s.add(z>=-rat(cap)*t,z>=g+rat(cap)*t-rat(cap)*b,
                      z<=g-rat(cap)*t+rat(cap)*b,z<=rat(cap)*t)
    return s,F,T,b,products,{'base_assertions':before,'new_assertions':len(s.assertions())-before,'excluded_Y_leaves':excluded,'intervals':interval_records}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--max-new',type=int,default=9);ap.add_argument('--timeout-ms',type=int,default=5000);a=ap.parse_args()
    if min(a.max_new,a.timeout_ms)<=0:raise ValueError('positive limits required')
    source=ROOT/'results/det5_scaled_pending_transfer.json';raw=source.read_bytes();prior=json.loads(raw)
    data=json.loads(OUT.read_text())if OUT.exists()else{'scope':'New coupled static/perspective outer formulas on certified residual domains. No complete chart, contact-class or global exclusion.','source_sha256':hashlib.sha256(raw).hexdigest(),'certified_Y_receipt_sha256':hashlib.sha256((ROOT/'results/det5_class5_y_cvc5_validation.json').read_bytes()).hexdigest(),'queries':[]}
    if data['source_sha256']!=hashlib.sha256(raw).hexdigest():raise ValueError('changed source')
    done={(tuple(r['Y_extrema']),tuple(r['U_extrema']),r['node'])for r in data['queries']}
    # Interleave charts; start with known outer SAT leaves to measure model strength.
    todo=sorted([r for r in prior['queries']if r['status']!='unsat'],key=lambda r:(r['status']!='sat',r['node']))
    C,S=inputs();count=0
    for leaf in todo:
        key=(tuple(leaf['Y_extrema']),tuple(leaf['U_extrema']),leaf['node'])
        if key in done:continue
        if count>=a.max_new:break
        s,F,T,b,products,meta=make(C,S,leaf,leaf);s.set(timeout=a.timeout_ms)
        ye,ue=leaf['Y_extrema'],leaf['U_extrema'];path=ROOT/f'results/det5_coupled_{ye[0]}_{ye[1]}_{ue[0]}_{ue[1]}_{leaf["node"]}.smt2'
        if path.exists():raise ValueError('unrecorded existing input; inspect before running')
        path.write_text(s.to_smt2());start=time.monotonic();status=s.check()
        row={k:leaf[k]for k in('Y_extrema','U_extrema','node','box')};row.update(meta,previous_status=leaf['status'],path=str(path.relative_to(ROOT)),input_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),timeout_ms=a.timeout_ms,status=str(status),elapsed_seconds=time.monotonic()-start)
        if status==z3.unknown:row['reason_unknown']=s.reason_unknown()
        if status==z3.sat:
            m=s.model();row['assignment']={str(v):str(m[v])for v in m};row['all_assertions_true']=all(z3.is_true(m.eval(c,model_completion=True))for c in s.assertions())
            fm=[[m.eval(x).as_fraction()for x in rr]for rr in F];row['actual_F']=inspect(fm,C)
            row['maximum_product_residual']=str(max(abs(m.eval(w).as_fraction()-m.eval(F[i][j]).as_fraction()*m.eval(T[i][k]).as_fraction())for i,j,k,w in products))
        data['queries'].append(row);OUT.write_text(json.dumps(data,indent=2)+'\n');count+=1
        print(json.dumps({k:row[k]for k in('Y_extrema','U_extrema','node','previous_status','status','elapsed_seconds')}),flush=True)
        if row.get('actual_F',{}).get('all_15_above_target'):return

if __name__=='__main__':main()
