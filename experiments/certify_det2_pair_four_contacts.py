"""Remove the fifth lattice contact by an exact facet perturbation.

The archived pair-column body's c1 parameter increases by 1/1000000.
This keeps the four assigned contacts and makes (-1,1,0) strictly outside.
Whole-body certification below is required, not inferred from continuity.
"""
import json
from fractions import Fraction
from pathlib import Path
from experiments.certify_det2_pair_column import ARCHIVED_PARAMETERS, exact_body

ROOT = Path(__file__).resolve().parents[1]


def main():
    parameters = list(map(Fraction, ARCHIVED_PARAMETERS))
    parameters[2] += Fraction(1,1000000)
    body = exact_body(parameters)
    expected = [[0,0,0],[0,0,1],[0,1,0],[2,1,1]]
    if body['boundary_points'] != expected or body['boundary_count'] != 4:
        raise ValueError('the exact perturbation must have precisely four lattice contacts')
    if body['row_pair_dominance_equalities']:
        raise ValueError('strict pair dominance is required')
    out = {'status':'exact_four_contact_pair_witness',
           'construction':{'source':'certificates/det2_pair_column.json',
                           'changed_parameter':'c1 (parameter index 2)',
                           'increment':'1/1000000',
                           'removed_contact':[-1,1,0],
                           'removed_contact_row0_slack':'-1/2000000'},
           'exact':body,
           'scope':'A maximal hollow tetrahedron with precisely four index-two lattice contacts in the strict pair branch, width >19/6. No class optimum, upper bound, or novelty claim.'}
    (ROOT/'certificates/det2_pair_four_contacts.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'width':body['width']['width'],
                      'boundary_points':body['boundary_points']}))


if __name__=='__main__':
    main()
