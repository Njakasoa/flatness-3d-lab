"""Exact contact obstructions for both the ACMS cutoff and a lower threshold."""
import json
from fractions import Fraction as F
from pathlib import Path
from src.exact import Q
from src.contact_obstruction import simplex_difference_minimum,width_upper_from_minimum,below_candidate,congruence_minimum


def main():
    cases=json.loads(Path('results/empty_tetrahedra_through_21.json').read_text())['classes']
    rows=[]
    for i,c in enumerate(cases):
        cert=simplex_difference_minimum(c['vertices']);ell=F(cert['lambda1'])
        N=c['normalized_determinant'];h=c['hnf']
        assert h==[[N,0,0],[int(N>1),1,0],[h[2][0],0,1]]
        assert ell==congruence_minimum(N,h[2][0])
        assert ell*ell*N<=2
        upper=width_upper_from_minimum(ell)
        row={'index':i,'hnf':c['hnf'],'vertices':c['vertices'],'minimum_certificate':cert,
             'width_upper':None if upper is None else upper.json(),
             'width_upper_decimal_display':None if upper is None else float(upper),
             'survives_threshold_3A_over_2':ell>F(1,3),
             'survives_threshold_11A_over_7':ell>F(4,11),
             'survives_candidate_threshold':upper is None or not below_candidate(upper)}
        rows.append(row)
    surviving=[r for r in rows if r['survives_threshold_3A_over_2']]
    high=[r for r in rows if r['survives_candidate_threshold']]
    result={'status':'exact_computational_reduction_pending_novelty_review',
      'source':'ACMS Lemma5.1 and Minkowski2 + empty tetrahedron width1 + exact HNF enumeration',
      'threshold':Q(F(3,2),1,3).json(),
      'finite_reduction':'w>3A/2 implies lambda1(K-K)>1/3; for empty P subset K: N=6vol(P)<=12/(5 lambda1(P-P)^2)<108/5, hence N<=21.',
      'classes_checked':len(rows),'survivors_lower_threshold':len(surviving),
      'survivors_candidate_threshold':len(high),
      'intermediate_threshold':Q(F(11,7),F(22,21),3).json(),
      'survivors_intermediate_threshold':sum(r['survives_threshold_11A_over_7'] for r in rows),
      'sharper_determinant_bound':'The width-one section diamond has area 2N. Planar Minkowski gives N*lambda1(P-P)^2<=2. Thus w>3A/2 implies N<=17; w>11A/7 implies N<=15; w>=2+sqrt2 implies N<=14.',
      'surviving_lower_hnfs':[r['hnf'] for r in surviving],
      'surviving_candidate_hnfs':[r['hnf'] for r in high],
      'cases':rows}
    Path('certificates/contact_obstructions.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['cases','surviving_lower_hnfs','surviving_candidate_hnfs']},indent=2))
    for r in surviving:print('SURVIVES',r['hnf'],'ell',r['minimum_certificate']['lambda1'])
if __name__=='__main__':main()
