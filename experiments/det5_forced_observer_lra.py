"""Two newly justified forced-observer patterns, without height products.

A SAT assignment belongs only to this necessary matrix relaxation. An UNSAT
label needs independent input audit and external proof replay before use.
"""
from pathlib import Path
import gzip,hashlib,json
import z3
from experiments.det5_horizontal_fiber_oracle import coordinates,rational,statement,VECTORS
from experiments.det5_y_corner_gauge_threshold import solve
ROOT=Path(__file__).resolve().parents[1]


def problem(order):
    if order not in ('lt','gt'):raise ValueError('order')
    F=[[z3.RealVal(0) if i==j else z3.Real(f'F_{i}_{j}')for j in range(4)]for i in range(4)]
    rows=[F[i][j]>0 for i in range(4) for j in range(4) if i!=j]
    rows += [sum(F[i][j]for i in range(4))==1 for j in range(4)]
    for v in VECTORS:
        co=coordinates(v);im=[sum(F[i][j]*rational(co[j])for j in range(4))for i in range(4)]
        rows.append(z3.Or(*[sum(im[i]for i in range(4)if mask&(1<<i))>rational('183/500') for mask in range(1,15)]))
    C=next(c for c in json.loads((ROOT/'certificates/nonunimodular_observer_guards.json').read_text())['classes']if c['class_index']==5)
    for point in C['guards']:
        co=coordinates(point,True)
        rows.append(z3.Or(*[sum(F[i][j]*rational(co[j])for j in range(4))<=0 for i in range(4)]))
    # Physical g2=(2,1,1) must be outside facet1 (lt) or facet2 (gt).
    first=1 if order=='lt' else 2
    co=coordinates((2,1,1),True)
    rows.append(sum(F[first][j]*rational(co[j])for j in range(4))<=0)
    # Both original orders force g3=(3,1,1) outside facet0.
    co=coordinates((3,1,1),True)
    rows.append(sum(F[0][j]*rational(co[j])for j in range(4))<=0)
    return F,rows


def main():
    for order in ('lt','gt'):
        stem=f'det5_forced_observer_lra_{order}';out=ROOT/'results'/f'{stem}.json'
        if out.exists():print(stem+': existing archive retained');continue
        F,rows=problem(order);text=statement(rows);p=ROOT/'results'/f'{stem}.smt2';p.write_text(text)
        result,proof=solve(text)
        result.update(order=order,target='17/5',beta='183/500',gauge_vectors=VECTORS,
                      forced_observers=[{'point':[2,1,1],'facet':1 if order=='lt' else 2},{'point':[3,1,1],'facet':0}],
                      scope='Necessary linear contact-matrix relaxation with newly proved forced observers; omits actual-height reconstruction, widths and volume. SAT is not an actual high-width body.',
                      input_path=str(p.relative_to(ROOT)),input_sha256=hashlib.sha256(text.encode()).hexdigest(),solver_queries_run=1)
        if proof:
            raw=proof.encode()if isinstance(proof,str)else proof;p=ROOT/'certificates'/f'{stem}.cpc.gz';p.write_bytes(gzip.compress(raw,mtime=0));result.update(proof_path=str(p.relative_to(ROOT)),proof_sha256=hashlib.sha256(raw).hexdigest())
        out.write_text(json.dumps(result,indent=2)+'\n');print(order,result['status'],result['elapsed_seconds'],flush=True)


if __name__=='__main__':main()
