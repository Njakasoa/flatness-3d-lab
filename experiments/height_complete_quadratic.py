"""Complete quadratic lattice-width lift of the normalized height charts.

Construction only: main archives the eleven genuinely new volume-cut charts
without querying any solver. The 21-variable model is an alternative to the
8-variable cubic encoding, not a mathematical class exclusion.
"""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import json
import z3
from experiments.contact_height_charts import height_model,symmetries
from experiments.nonunimodular_complete_smt import width_directions

ROOT=Path(__file__).resolve().parents[1]


def make(C,S,extrema,threshold=Q(17,5)):
    solver,F,q,a,b,vectors=height_model(C,S,extrema,volume_cut=True,threshold=threshold)
    X=z3.Reals('vertex_X0 vertex_X1 vertex_X2 vertex_X3')
    Z=z3.Reals('vertex_Z0 vertex_Z1 vertex_Z2 vertex_Z3')
    P=C['contact_points']
    for coord,axis in ((X,0),(Z,2)):
        solver.add(*[sum(F[i][j]*coord[i] for i in range(4))==P[j][axis] for j in range(4)])
    directions=width_directions(C['normalized_volume'],P[1][2])
    for ux,uy,uz in directions:
        differences=[ux*b*(X[i]-X[j])+uy*(q[i]-q[j])+uz*b*(Z[i]-Z[j])
                     for i,j in combinations(range(4),2)]
        solver.add(z3.Or(*[sign*v>z3.RealVal(str(threshold))*b for v in differences for sign in (-1,1)]))
    return solver,F,q,a,b,X,Z,directions


def main():
    guards=json.loads((ROOT/'certificates/nonunimodular_observer_guards.json').read_text())
    scans=json.loads((ROOT/'results/two_vector_class_scan.json').read_text())
    rows=[]
    for idx in (6,7):
        C=next(c for c in guards['classes'] if c['class_index']==idx)
        S=next(c for c in scans['classes'] if c['class_index']==idx)
        _,orbits=symmetries(C['contact_points'])
        for orbit in orbits:
            ext=orbit[0];solver,*_=make(C,S,ext)
            path=f'results/height_complete_{idx}_{ext[0]}_{ext[1]}.smt2'
            (ROOT/path).write_text(solver.to_smt2())
            rows.append({'class_index':idx,'extrema':ext,'path':path,'status':'not_run'})
    (ROOT/'results/height_complete_quadratic.json').write_text(json.dumps({
        'scope':'Complete lattice-width targets at 17/5 with necessary gauge and volume cuts. Twenty-one real variables, degree two. Constraints archived without querying a solver.',
        'solver_queries_run':0,'cases':rows},indent=2)+'\n')
    print('Archived eleven complete quadratic targets; zero solver queries')


if __name__=='__main__':main()
