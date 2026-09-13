"""Filter the complete nonsimplicial contact candidates by their full minimum."""
import json
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from src.width_one_minimum import certify_minimum
from src.contact_obstruction import width_upper_from_minimum,below_candidate

def main():
    data=json.loads(Path('results/contact_extensions.json').read_text())
    rows=[]
    for c in data['classes']:
        cert=certify_minimum(c['vertices'],c['width_one_direction']);ell=F(cert['lambda1'])
        bound=width_upper_from_minimum(ell)
        rows.append({**c,'minimum_certificate':cert,
                     'width_upper':None if bound is None else bound.json(),
                     'survives_intermediate_threshold':ell>F(4,11),
                     'survives_candidate_threshold':bound is None or not below_candidate(bound)})
    result={'status':'exact_candidate_reduction_pending_independent_review',
            'classes_checked':len(rows),'counts_before':data['counts'],
            'counts_after_intermediate':dict(sorted(Counter(len(c['vertices']) for c in rows if c['survives_intermediate_threshold']).items())),
            'counts_after_candidate':dict(sorted(Counter(len(c['vertices']) for c in rows if c['survives_candidate_threshold']).items())),
            'classes':rows}
    Path('certificates/contact_hull_obstructions.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='classes'},indent=2))
    for i,c in enumerate(rows):print(i,len(c['vertices']),c['minimum_certificate']['lambda1'],c['survives_candidate_threshold'],flush=True)

if __name__=='__main__':main()
