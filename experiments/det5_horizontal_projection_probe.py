"""Bounded exact rational base probe after analytic cuts; no solver calls.

This finite list is not a continuous cover. The existing probe archive is
retained without repeating its computations. Each projected branch records
an exact rational witness or a directly checkable strict-Farkas certificate.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from experiments.det5_horizontal_projection import project

OUTPUT = ROOT / 'results/det5_horizontal_projection_base_probe.json'


def main():
    if OUTPUT.exists():
        print('Retained existing finite probe; no repeated computation.')
        return
    rows = []
    found = []
    for order in ('lt', 'gt'):
        for p, q, C, E in product(
            map(Q, ['0', '1/4', '1/2', '3/4']),
            map(Q, ['0', '1/4', '1/2', '3/4']),
            map(Q, ['1/16', '1/8', '1/4', '3/8']),
            map(Q, ['1/2', '5/8', '3/4', '7/8']),
        ):
            A = C + p*E
            B = q*C + E
            S = C + E
            L = 1 - p*q
            k = 3 if order == 'lt' else 2
            if S >= 1 or L*E <= (5-k)*Q(183, 500)*q:
                continue
            if order == 'lt' and not (B > Q(183, 200) or B-A > Q(83, 200)):
                continue
            if order == 'gt' and not A-B < Q(17, 100):
                continue
            result = project((p, q, C, E), order)
            rows.append(result)
            if result['status'] == 'infeasible':
                found.append({'order': order, 'base': result['base']})
                print('new base obstruction', found[-1], flush=True)
            if len(found) >= 4 or len(rows) >= 60:
                break
        if len(found) >= 4 or len(rows) >= 60:
            break
    OUTPUT.write_text(json.dumps({
        'scope': 'Finite rational base probe after analytic cuts; no continuous coverage. All projected branches have exact witnesses or certificates.',
        'solver_queries_run': 0,
        'controls': rows,
        'new_infeasible_after_cuts': found,
    }, indent=2) + '\n')
    print('completed', len(rows), 'bases', len(found), 'additional point obstructions', flush=True)


if __name__ == '__main__':
    main()
