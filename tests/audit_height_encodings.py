"""Read-only height encoding audit: no Solver.check calls."""
from fractions import Fraction as Q
from itertools import permutations,product
from pathlib import Path
import json,sys
import z3
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from experiments.contact_height_charts import height_model
from experiments.height_complete_quadratic import make
from replay_det13_contraction_independent import need,solve
from replay_weighted_trace_independent import inv,determinant
from audit_nonunimodular_encoding import max_polynomial_degree


def stats(solver):
    variables={}
    def walk(e):
        if z3.is_const(e) and e.decl().kind()==z3.Z3_OP_UNINTERPRETED:variables[str(e)]=e
        for child in e.children():walk(child)
    for e in solver.assertions():walk(e)
    return len(variables),max(max_polynomial_degree(e) for e in solver.assertions())


def equivalent_archive(solver,path):
    def canonical(e):
        if not e.children():return e.sexpr()
        args=[canonical(c) for c in e.children()]
        if e.decl().kind() in (z3.Z3_OP_OR,z3.Z3_OP_AND,z3.Z3_OP_ADD,z3.Z3_OP_MUL,z3.Z3_OP_EQ):
            args.sort(key=repr)
        return (str(e.decl()),tuple(args))
    old=z3.parse_smt2_file(str(path));new=solver.assertions()
    need(len(old)==len(new),'archive count')
    for a,b in zip(old,new):
        need(canonical(z3.simplify(a,som=True))==canonical(z3.simplify(b,som=True)),
             'archive expression equality modulo commutative operand order')


def main():
    archive=json.loads((ROOT/'results/contact_height_charts.json').read_text())
    guards=json.loads((ROOT/'certificates/nonunimodular_observer_guards.json').read_text())
    scans=json.loads((ROOT/'results/two_vector_class_scan.json').read_text())
    controls=json.loads((ROOT/'results/nonunimodular_complete_smt.json').read_text())
    fullarchive=json.loads((ROOT/'results/height_complete_quadratic.json').read_text())
    need(fullarchive['solver_queries_run']==0 and len(fullarchive['cases'])==11,'full encodings not run')
    reports=[]
    for D in archive['classes']:
        idx=D['class_index'];C=next(c for c in guards['classes'] if c['class_index']==idx)
        S=next(c for c in scans['classes'] if c['class_index']==idx);P=C['contact_points']
        need({(1,0,0),(3,0,1),(2,0,1)}<=set(map(tuple,D['gauge_vectors'])),'rank gauge coverage')
        # Independent affine lattice symmetry reconstruction from inverse frame.
        E=[[Q(P[j][k]-P[0][k]) for k in range(3)] for j in range(1,4)]
        sym={}
        for p in permutations(range(4)):
            U=[solve(E,[Q(P[p[j]][k]-P[p[0]][k]) for j in range(1,4)]) for k in range(3)]
            if any(x.denominator!=1 for row in U for x in row):continue
            need(abs(determinant(U))==1,'lattice automorphism determinant')
            sign=1-2*P[p[0]][1]
            need(U[1]==[0,sign,0],'Y direction reflected or preserved')
            sym[p]=([[int(x) for x in row] for row in U],P[p[0]],sign)
        need(len(sym)==(2 if idx==6 else 4),'full group size')
        need(set(sym)=={tuple(g['permutation']) for g in D['automorphisms']},'full group list')
        gauges=set(map(tuple,D['gauge_vectors']))
        for g in D['automorphisms']:
            U,t,sign=sym[tuple(g['permutation'])]
            need((g['matrix'],g['translation'],g['height_sign'])==(U,t,sign),'affine symmetry binding')
            for v in gauges:
                w=tuple(sum(U[i][j]*v[j] for j in range(3)) for i in range(3))
                need(w in gauges or tuple(-x for x in w) in gauges,'gauge symmetry closure')
        seen=set()
        for orbit in D['extrema_orbits']:
            L,H=orbit[0]
            expected={(p[L],p[H]) if sign==1 else (p[H],p[L]) for p,(_,_,sign) in sym.items()}
            need(expected==set(map(tuple,orbit)) and not seen&expected,'exact orbit');seen|=expected
        need(seen==set(permutations(range(4),2)),'all twelve ordered extrema covered')
        for case in D['cases']:
            ext=case['extrema'];tag=f'{idx}_{ext[0]}_{ext[1]}'
            old,*_=height_model(C,S,ext)
            need(stats(old)==(12,2),'twelve quadratic height variables')
            equivalent_archive(old,ROOT/f'results/height_chart_{tag}.smt2')
            need(case['status']=='unknown','old recorded result')
            volume,*_=height_model(C,S,ext,volume_cut=True)
            need(stats(volume)==(13,2),'thirteen quadratic volume variables')
            full,*_=make(C,S,ext)
            need(stats(full)==(21,2),'twenty-one quadratic full variables')
            equivalent_archive(full,ROOT/f'results/height_complete_{tag}.smt2')
        # Exact inverse of the existing nontrivial near-permutation pin.
        pin=next(c for c in controls['results'] if c['class_index']==idx)['controls']['F']
        F0=[list(map(Q,r)) for r in pin];T=inv(F0)
        V=[[sum(Q(P[i][k])*T[i][j] for i in range(4)) for k in range(3)] for j in range(4)]
        y=[v[1] for v in V];span=max(y)-min(y);qn=[(x-min(y))/span for x in y]
        ext=(qn.index(0),qn.index(1));a0=-min(y)/span;b0=1/span
        # Input difference coordinates solved in an independent affine frame.
        A=[[Q(1)]*4]+[[Q(p[k]) for p in P] for k in range(3)]
        r,s=[[sum(F0[i][j]*l[j] for j in range(4)) for i in range(4)]
             for l in (solve(A,[0,1,0,0]),solve(A,[0,3,0,1]))]
        i,j=[h for h in range(4) if h not in ext];k0=abs(r[i]*s[j]-r[j]*s[i])
        counts=[]
        for W in (Q(1),Q(17,5)):
            solver,F,q,a,b,X,Z,dirs=make(C,S,ext,W)
            subs=[]
            for i in range(4):
                for j in range(4):
                    if z3.is_const(F[i][j]) and not z3.is_rational_value(F[i][j]):subs.append((F[i][j],z3.RealVal(str(F0[i][j]))))
                if not z3.is_rational_value(q[i]):subs.append((q[i],z3.RealVal(str(qn[i]))))
                subs.extend(((X[i],z3.RealVal(str(V[i][0]))),(Z[i],z3.RealVal(str(V[i][2])))))
            subs.extend(((a,z3.RealVal(str(a0))),(b,z3.RealVal(str(b0))),(z3.Real('height_minor'),z3.RealVal(str(k0)))))
            values=[z3.simplify(z3.substitute(e,*subs)) for e in solver.assertions()]
            need(all(z3.is_true(e) or z3.is_false(e) for e in values),'exact closed pin evaluation')
            counts.append(sum(z3.is_false(e) for e in values))
        need(counts[0]==0 and counts[1]>0,'nontrivial positive/negative controls')
        reports.append({'class_index':idx,'height_orbits':len(D['cases']),'automorphisms':len(sym),
                        'height_variables':12,'with_volume_variables':13,'full_width_variables':21,
                        'maximum_degree':2,'pin_false_constraint_counts':counts})
    print(json.dumps({'status':'PASS','solver_queries_run':0,'classes':reports,
                      'scope':'Exact encoding, symmetry and pinned arithmetic audit. No infeasibility proof.'},indent=2))


if __name__=='__main__':main()
