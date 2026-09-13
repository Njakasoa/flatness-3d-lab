"""Exact optimal weights for the specified two-vector mismatch estimate.

The bound is fractional linear on either side of the balancing weight;
only the two intrinsic endpoints and that weight need evaluation.
This is not optimality among arbitrary multiple-vector arguments.
"""
from fractions import Fraction as F
from pathlib import Path
import json
from src.exact import Q

ROOT=Path(__file__).resolve().parents[1]
A=Q(1,F(2,3),3)


def build():
    source=json.loads((ROOT/'results/two_vector_class_scan.json').read_text())
    records=[]
    for C in source['classes']:
        candidates=[]
        for pair in C['all_eligible_pairs']:
            rows=[list(map(F,r)) for r in pair['difference_barycentrics']]
            minima=[min(map(abs,r)) for r in rows]
            masses=list(map(F,pair['positive_masses']))
            weights=[minima[1]/sum(minima),minima[0]/sum(minima)]
            m=weights[0]*minima[0]
            if m!=weights[1]*minima[1]:raise ValueError('balanced loss coefficients')
            S=sum(w*a for w,a in zip(weights,masses))
            B=(m+A)/(m-S+1)
            options=[('balanced',(str(weights[0]),str(weights[1])),B)]
            for i in range(2):
                options.append(('intrinsic_endpoint',tuple('1' if k==i else '0' for k in range(2)),A/(1-masses[i])))
            for kind,w,bound in options:
                candidates.append((bound,{'vectors':pair['vectors'],'kind':kind,
                    'weights':w,'bound':bound.json(),
                    'weighted_mass':str(sum(F(x)*a for x,a in zip(w,masses))),
                    'mismatch_coefficient':str(min(F(x)*a for x,a in zip(w,minima)))}))
        candidates.sort(key=lambda r:r[0])
        records.append({'class_index':C['class_index'],'determinant':C['normalized_determinant'],
                        'pair_count':C['distinct_code_pair_count'],
                        'best':candidates[0][1] if candidates else None,
                        'all_weight_candidates':[r for _,r in candidates]})
    return {'status':'exact_weight_optimization_for_two_vector_loss_bound',
            'scope':'Only the minimum-coefficient two-vector mismatch estimate, on the previously certified vector domain. Intrinsic endpoints are already known containment bounds. No new class is excluded.',
            'classes':records}


def main():
    data=build()
    (ROOT/'certificates/weighted_two_vector_bounds.json').write_text(json.dumps(data,indent=2)+'\n')
    for C in data['classes']:
        if C['best']:print(json.dumps({'determinant':C['determinant'],'best':C['best']}))


if __name__=='__main__':main()
