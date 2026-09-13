"""Quadratic height-width charts with exact symmetry orbits.

The three-vector rank lemma proves invertibility under these constraints.
Default charts impose only Y-width, not full lattice width or the volume cut.
Optional volume lifting stays quadratic. Reconstruct any SAT output exactly.
"""
from fractions import Fraction as Q
from itertools import permutations
from pathlib import Path
import json
import time
import z3
from experiments.contact_contraction_trace_probe import build,certify
from experiments.nonunimodular_observer_guards import solve

ROOT=Path(__file__).resolve().parents[1]
HEIGHTS=(0,1,1,0)


def symmetries(P):
    edge_rows=[tuple(p[k]-P[0][k] for k in range(3)) for p in P[1:]]
    group=[]
    for p in permutations(range(4)):
        U=[solve(edge_rows,[P[p[j]][k]-P[p[0]][k] for j in range(1,4)]) for k in range(3)]
        if any(x.denominator!=1 for row in U for x in row):continue
        sign=1 if HEIGHTS[p[0]]==0 else -1
        if any(HEIGHTS[p[j]]!=HEIGHTS[p[0]]+sign*HEIGHTS[j] for j in range(4)):
            raise ValueError('unique width-one height not preserved up to sign')
        group.append({'permutation':p,'matrix':[[int(x) for x in r] for r in U],
                      'translation':P[p[0]],'height_sign':sign})
    remaining=set(permutations(range(4),2));orbits=[]
    while remaining:
        r,s=min(remaining)
        orbit={((g['permutation'][r],g['permutation'][s]) if g['height_sign']==1
                else (g['permutation'][s],g['permutation'][r])) for g in group}
        if not orbit<=remaining:raise ValueError('extrema orbit partition')
        remaining-=orbit;orbits.append(sorted(orbit))
    return group,orbits


def height_model(C,S,extrema,volume_cut=False,threshold=Q(17,5)):
    base,F,vectors=build(C,S,include_trace=False)
    replacements=[]
    for j in range(4):
        ids=[i for i in range(4) if i!=j]
        replacements.append((F[ids[2]][j],1-F[ids[0]][j]-F[ids[1]][j]))
    F=[[z3.simplify(z3.substitute(v,*replacements)) for v in row] for row in F]
    solver=z3.SolverFor('QF_NRA');solver.set(timeout=2000)
    solver.add(*[z3.simplify(z3.substitute(v,*replacements),som=True) for v in base.assertions()])
    low,high=extrema
    q=[z3.RealVal(0) if i==low else z3.RealVal(1) if i==high else z3.Real(f'q{i}') for i in range(4)]
    offset,gap=z3.Reals('height_offset height_gap')
    solver.add(*[v>=0 for v in q],*[v<=1 for v in q])
    solver.add(offset>=0,offset+gap<=1,gap>0,gap<z3.RealVal(str(1/threshold)))
    solver.add(*[sum(F[i][j]*q[i] for i in range(4))==offset+gap*HEIGHTS[j] for j in range(4)])
    if volume_cut:
        add_volume_cut(solver,F,gap,C,extrema)
    return solver,F,q,offset,gap,vectors


def add_volume_cut(solver,F,gap,C,extrema):
    """Exact volume cut via the complementary minor; no certificate input."""
    from experiments.contact_contraction_trace_probe import ell,BETA
    d=C['normalized_volume'];a=C['contact_points'][1][2]
    rows=[ell(v,d,a) for v in ((1,0,0),(3,0,1),(2,0,1))]
    masses=[sum(map(abs,r))/2 for r in rows]
    margin=2*BETA-max(masses)
    if margin<=0:raise ValueError('rank margin does not apply')
    r,s=[[z3.simplify(sum(F[i][j]*z3.RealVal(str(l[j])) for j in range(4)),som=True)
          for i in range(4)] for l in rows[:2]]
    i,j=[h for h in range(4) if h not in extrema]
    minor=z3.simplify(r[i]*s[j]-r[j]*s[i],som=True)
    k=z3.Real('height_minor')
    solver.add(z3.Or(k==minor,k==-minor),k>=z3.RealVal(str(BETA*margin/4)),
               k<=z3.RealVal(str(masses[0]*masses[1])),
               gap*k>z3.RealVal(str(BETA**3/6)),
               gap>z3.RealVal(str(BETA**3/(6*masses[0]*masses[1]))))
    return k,minor


def main():
    guards=json.loads((ROOT/'certificates/nonunimodular_observer_guards.json').read_text())
    scans=json.loads((ROOT/'results/two_vector_class_scan.json').read_text())
    output=[]
    for idx in (6,7):
        C=next(c for c in guards['classes'] if c['class_index']==idx)
        S=next(c for c in scans['classes'] if c['class_index']==idx)
        group,orbits=symmetries(C['contact_points']);cases=[]
        for orbit in orbits:
            extrema=orbit[0];solver,F,q,offset,gap,vectors=height_model(C,S,extrema)
            tag=f'{idx}_{extrema[0]}_{extrema[1]}'
            (ROOT/f'results/height_chart_{tag}.smt2').write_text(solver.to_smt2())
            start=time.monotonic();status=solver.check();elapsed=time.monotonic()-start
            row={'extrema':extrema,'orbit':orbit,'status':str(status),'elapsed_seconds':elapsed,'timeout_ms':2000}
            if status==z3.sat:
                model=solver.model()
                expressions=[v for r in F for v in r]+q+[offset,gap]
                if all(z3.is_rational_value(model.eval(v)) for v in expressions):
                    matrix=[[model.eval(v).as_fraction() for v in r] for r in F]
                    row['F']=[[str(v) for v in r] for r in matrix]
                    row['normalized_heights']=[str(model.eval(v).as_fraction()) for v in q]
                    row['offset']=str(model.eval(offset).as_fraction());row['gap']=str(model.eval(gap).as_fraction())
                    row['exact_body']=certify(matrix,C['contact_points'])
                else:row['algebraic_model']={str(v):str(model[v]) for v in model}
            elif status==z3.unknown:row['reason_unknown']=solver.reason_unknown()
            cases.append(row)
            print(json.dumps({'class_index':idx,'extrema':extrema,'status':str(status),'elapsed_seconds':elapsed}),flush=True)
        output.append({'class_index':idx,'determinant':C['normalized_volume'],'contact_points':C['contact_points'],
                       'gauge_vectors':vectors,'automorphisms':group,'extrema_orbits':orbits,'cases':cases})
        (ROOT/'results/contact_height_charts.json').write_text(json.dumps({
            'scope':'Complete Y-direction charts under the stated gauges and relative-interior contacts: the three-vector rank lemma guarantees invertibility and the guards guarantee hollowness. Not a complete lattice-width target; no volume cut is imposed in this archive.',
            'z3_version':z3.get_version_string(),'classes':output},indent=2)+'\n')


if __name__=='__main__':main()
