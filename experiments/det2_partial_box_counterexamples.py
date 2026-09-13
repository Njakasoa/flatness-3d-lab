"""Exact counterexamples to sufficiency of the 216-point hollow screen.

These are nonhollow bodies, not flatness counterexamples. Parameters were
obtained by rounding recorded runs 7 and 14 to six decimal places, retaining
the small positive first-column entries, and solving two active contact
linear equations exactly. No solver or floating search is rerun here.
"""
import itertools
import json
from fractions import Fraction as R
from pathlib import Path
from src.exact import Q, inverse
from src.geometry import Polytope, certify_width, certify_hollow

ROOT = Path(__file__).resolve().parents[1]
SIGMA = (1, 0, 3, 2)
PARAMETERS = [
    ['4999999/5000000','1/10000000','227447/250000','1063/25000',
     '2425571/15000000','135101/250000','52429/100000','46173/125000'],
    ['4999999/5000000','1/10000000','14327/15625','56427/1000000',
     '238823/500000','46491/125000','2577131/15000000','109/200'],
]


def require(value, message):
    if not value:
        raise ValueError(message)


def barycentric(z):
    x,y,z = map(R,z)
    return (1+x/2-y-z,x/2,y-x/2,z-x/2)


def certificate(parameters, hidden):
    values = list(map(R, parameters))
    F = [[R(0) for _ in range(4)] for _ in range(4)]
    for j in range(4):
        others = [i for i in range(4) if i not in (j,SIGMA[j])]
        F[SIGMA[j]][j] = values[2*j]
        F[others[0]][j] = values[2*j+1]
        F[others[1]][j] = 1-values[2*j]-values[2*j+1]
    require(all(F[i][j]>0 for i in range(4) for j in range(4) if i!=j),'offdiagonal')
    surplus=[F[i][SIGMA[i]]-sum(F[i][j] for j in range(4) if j not in(i,SIGMA[i])) for i in range(4)]
    require(all(x>=0 for x in surplus) and any(x>0 for x in surplus),'pair dominance')
    require(all(sum(F[i][j] for i in range(4))==1 for j in range(4)),'columns')
    T=inverse([[Q(x) for x in row] for row in F])
    K=Polytope([(2*T[1][j],T[1][j]+T[2][j],T[1][j]+T[3][j]) for j in range(4)])
    def slacks(point):
        lam=barycentric(point)
        return [sum(F[i][j]*lam[j] for j in range(4)) for i in range(4)]
    small_interior=[list(z) for z in itertools.product(range(-2,4),repeat=3) if all(x>0 for x in slacks(z))]
    require(not small_interior,'small-box screen fails')
    hidden_slacks=slacks(hidden)
    require(all(x>0 for x in hidden_slacks),'hidden point not strictly interior')
    hollow=certify_hollow(K);width=certify_width(K)
    require(hollow['interior_points']==[tuple(hidden)],'whole-box interior list changed')
    require(Q.from_json(width['width'])>Q(R(7,2)), 'width must exceed 7/2')
    gamma_x=sum(F[i][SIGMA[i]] for i in range(4))/2-1
    require(gamma_x<R(37,102),'new ACMS cut must reject this candidate')
    # Uniform L-infinity perturbation of eight column parameters: each
    # row slack changes by at most twice their radius times ||lambda||_1.
    robust_radius=min(hidden_slacks)/(4*sum(map(abs,barycentric(hidden))))
    return {'parameters':parameters,'F':[[str(x) for x in row] for row in F],
            'vertices':K.json(),'pair_surplus':list(map(str,surplus)),
            'small_box':[-2,3],'small_points_checked':216,'small_interior_points':[],
            'hidden_point':hidden,'hidden_positive_slacks':list(map(str,hidden_slacks)),
            'hidden_point_parameter_robustness_radius':str(robust_radius),
            'hollow':hollow,'width':width,'gamma_eX':str(gamma_x),
            'rejected_by_ACMS_target_17_over_5_cut':True}


def main():
    rows=[certificate(p,z) for p,z in zip(PARAMETERS,[[-3,1,-1],[-3,-1,1]])]
    out={'status':'exact_nonhollow_partial_screen_counterexamples',
         'scope':'The 216-point screen is insufficient even for pair tetrahedra of width >7/2. Both violate the newer necessary ACMS gauge cut; neither is a flatness counterexample or a solution of the column target model.',
         'cases':rows}
    (ROOT/'certificates/det2_partial_box_counterexamples.json').write_text(json.dumps(out,indent=2)+'\n')
    print('PASS: two exact widths >7/2, zero small-box interiors, one hidden interior each, both ACMS-rejected')


if __name__=='__main__':
    main()
