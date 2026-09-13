"""Independent full-matrix encoding and cvc5 proof-producing cover replay.

No experiment, Z3, or main geometry imports. Reconstruct barycentrics using
independent Fraction elimination. Exact cover arithmetic precedes all queries.
The cvc5 internal checker is used; this is not an external proof-kernel check.
"""
from fractions import Fraction as Q
from pathlib import Path
from itertools import permutations
from collections import Counter
import argparse,gzip,hashlib,json,time
import cvc5
from replay_det13_contraction_independent import solve,need

ROOT=Path(__file__).resolve().parents[1]


def rat(x):
    x=Q(x)
    if x<0:return '(- '+rat(-x)+')'
    return str(x.numerator) if x.denominator==1 else f'(/ {x.numerator} {x.denominator})'


def add(parts):
    parts=list(parts)
    return '0' if not parts else parts[0] if len(parts)==1 else '(+ '+' '.join(parts)+')'


def mul(a,b):return f'(* {a} {b})'


def statement(C,vectors,extrema,box,threshold=Q(17,5)):
    """Full 12-entry matrix, instead of the discovery encoding's 8 parameters."""
    P=C['contact_points'];A=[[Q(1)]*4]+[[Q(p[k]) for p in P] for k in range(3)]
    F=[['0' if i==j else f'F_{i}_{j}' for j in range(4)] for i in range(4)]
    free=[i for i in range(4) if i not in extrema]
    q=['0' if i==extrema[0] else '1' if i==extrema[1] else f'q_{i}' for i in range(4)]
    variables=[F[i][j] for i in range(4) for j in range(4) if i!=j]+[q[i] for i in free]+['offset','gap']
    variables += [f'product_{i}_{j}' for i in free for j in range(4) if i!=j]
    out=['(set-logic QF_LRA)']+[f'(declare-fun {v} () Real)' for v in variables]
    def require(e):out.append('(assert '+e+')')
    for i in range(4):
        for j in range(4):
            if i!=j:require(f'(> {F[i][j]} 0)')
    for j in range(4):require(f'(= {add(F[i][j] for i in range(4))} 1)')
    require('(>= offset 0)');require('(<= (+ offset gap) 1)');require('(> gap 0)');require(f'( < gap {rat(1/threshold)})')
    def coords(v,affine):
        l=solve(A,[Q(int(affine)),*map(Q,v)])
        return [add(mul(rat(l[j]),F[i][j]) for j in range(4) if l[j] and i!=j) for i in range(4)]
    for v in vectors:
        need(len(v)==3 and all(isinstance(x,int) for x in v) and any(v),'integer gauge vector')
        values=coords(v,False)
        require('(or '+' '.join(f'(> {add(values[i] for i in range(4) if mask&(1<<i))} (/ 37 102))' for mask in range(1,15))+')')
    for v in C['guards']:
        require('(or '+' '.join(f'(<= {x} 0)' for x in coords(v,True))+')')
    for i,(l,h) in zip(free,box):
        require(f'(>= {q[i]} {rat(l)})');require(f'(<= {q[i]} {rat(h)})')
        for j in range(4):
            if i==j:continue
            p=f'product_{i}_{j}';f=F[i][j]
            require(f'(>= {p} {mul(rat(l),f)})');require(f'(<= {p} {mul(rat(h),f)})')
            require(f'(>= {p} {add([q[i],mul(rat(h),f),rat(-h)])})')
            require(f'(<= {p} {add([q[i],mul(rat(l),f),rat(-l)])})')
    for j in range(4):
        terms=[]
        for i in range(4):
            if i==j or i==extrema[0]:continue
            terms.append(F[i][j] if i==extrema[1] else f'product_{i}_{j}')
        rhs='offset' if P[j][1]==0 else '(+ offset gap)'
        require(f'(= {add(terms)} {rhs})')
    return '\n'.join(out)+'\n'


def cover(data):
    need(len(data['charts'])==11,'eleven charts')
    allqueries={(r['class_index'],tuple(r['extrema']),r['node']):r for r in data['queries']}
    need(len(allqueries)==len(data['queries']),'unique queries')
    leaves=[];charts=[]
    for C in data['charts']:
        need(C['complete_cover'] and not C['pending_leaves'],'complete chart claim')
        idx=C['class_index'];ext=tuple(C['extrema']);seen=set();closed=set()
        def visit(tag,box):
            key=(idx,ext,tag);need(key in allqueries,'missing covering node');R=allqueries[key];seen.add(tag)
            need([[Q(x) for x in r] for r in R['box']]==[list(r) for r in box],'exact dyadic box')
            if R['status']=='unsat':closed.add(tag);leaves.append(R);return
            need(R['status'] in ('sat','unknown'),'split only recognized status')
            axis=max(range(2),key=lambda i:box[i][1]-box[i][0]);l,h=box[axis];mid=(l+h)/2
            for suffix,interval in (('0',(l,mid)),('1',(mid,h))):
                child=list(box);child[axis]=interval;visit(tag+suffix,tuple(child))
        visit('r',((Q(0),Q(1)),(Q(0),Q(1))))
        need(closed==set(C['closed_leaves']),'all terminal exclusions')
        need(len(seen)==C['queries'],'all chart queries accounted')
        area=sum((Q(allqueries[idx,ext,t]['box'][0][1])-Q(allqueries[idx,ext,t]['box'][0][0]))*
                 (Q(allqueries[idx,ext,t]['box'][1][1])-Q(allqueries[idx,ext,t]['box'][1][0])) for t in closed)
        need(area==1,'exact covered area')
        charts.append({'class_index':idx,'extrema':ext,'leaves':len(closed),'covered_area':'1'})
    need(len(leaves)==62,'leaf count')
    return leaves,charts


def run(text):
    solver=cvc5.Solver();solver.setOption('produce-proofs','true');solver.setOption('check-proofs','true')
    solver.setOption('check-proofs-complete','true');solver.setOption('tlimit-per','10000')
    parser=cvc5.InputParser(solver);parser.setStringInput(cvc5.InputLanguage.SMT_LIB_2_6,text,'independent-height-cover')
    sm=parser.getSymbolManager()
    while True:
        command=parser.nextCommand()
        if command.isNull():break
        command.invoke(solver,sm)
    start=time.monotonic();status=solver.checkSat();elapsed=time.monotonic()-start
    if not status.isUnsat():return {'status':str(status),'elapsed_seconds':elapsed},None
    proofs=solver.getProof();need(len(proofs)==1,'one full proof')
    todo=list(proofs);seen=set();rules=Counter()
    while todo:
        p=todo.pop()
        if p in seen:continue
        seen.add(p);rules[str(p.getRule())]+=1;todo.extend(p.getChildren())
    proof=solver.proofToString(proofs[0],cvc5.ProofFormat.CPC)
    return {'status':'unsat','elapsed_seconds':elapsed,'proof_nodes':len(seen),
            'proof_rules':dict(sorted(rules.items())),'internal_proof_check':True,
            'check_proofs_complete':True},proof


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--limit',type=int);args=parser.parse_args()
    data=json.loads((ROOT/'results/height_interval_relaxation.json').read_text());leaves,charts=cover(data)
    G=json.loads((ROOT/'certificates/nonunimodular_observer_guards.json').read_text())
    H=json.loads((ROOT/'results/contact_height_charts.json').read_text())
    rows=[];outdir=ROOT/'certificates/height_cover_cvc5';outdir.mkdir(exist_ok=True)
    for leaf in leaves[:args.limit]:
        idx=leaf['class_index'];ext=leaf['extrema'];tag=f'{idx}_{ext[0]}_{ext[1]}_{leaf["node"]}'
        C=next(c for c in G['classes'] if c['class_index']==idx)
        vectors=next(c for c in H['classes'] if c['class_index']==idx)['gauge_vectors']
        text=statement(C,vectors,ext,[[Q(x) for x in r] for r in leaf['box']])
        (outdir/(tag+'.smt2')).write_text(text)
        result,proof=run(text);result.update(class_index=idx,extrema=ext,node=leaf['node'],
            input_sha256=hashlib.sha256(text.encode()).hexdigest())
        if proof is not None:
            raw=proof if isinstance(proof,bytes) else proof.encode();packed=gzip.compress(raw,mtime=0)
            (outdir/(tag+'.cpc.gz')).write_bytes(packed)
            result.update(proof_sha256=hashlib.sha256(raw).hexdigest(),compressed_proof_sha256=hashlib.sha256(packed).hexdigest(),proof_bytes=len(raw))
        rows.append(result)
        report={'status':'PASS' if len(rows)==62 and all(r['status']=='unsat' for r in rows) else 'INCOMPLETE',
                'cvc5_version':cvc5.__version__,'independent_full_matrix_encoding':True,'charts':charts,'leaves':rows,
                'scope':'Exact cover and independent SMT-engine verification with cvc5 internal complete-proof checks. Exported CPC proofs have not been checked by an external proof kernel.'}
        (ROOT/'results/height_cover_cvc5_validation.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps({'leaf':tag,'status':result['status'],'elapsed_seconds':result['elapsed_seconds']}),flush=True)
        if result['status']!='unsat':raise SystemExit('Independent leaf did not verify; leave candidate unproved')


if __name__=='__main__':main()
