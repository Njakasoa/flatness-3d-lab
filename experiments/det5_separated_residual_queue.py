"""Append exact separated-height necessities; no solver or archive edits."""
from copy import deepcopy
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'results/det5_enlarged_residual_queue.json'
THEOREM = 'proofs/DET5_COMPACT_SHAPE_CHART_REVIEW.md'
ORDER = 'proofs/DET5_Y_CORNER_ANALYTIC_PROBE.md'
OUTPUT = 'results/det5_separated_residual_queue.json'


def binding(path):
    return {'path': path, 'sha256': sha256((ROOT/path).read_bytes()).hexdigest()}


def cut():
    # Polynomial terms are [integer coefficient, exponent of q1, exponent of q2].
    return {
        'id': 'Y03_separated_heights', 'operator': 'OR',
        'variables': [{'name': 'q1', 'free_coordinate': 0, 'vertex_index': 1},
                      {'name': 'q2', 'free_coordinate': 1, 'vertex_index': 2}],
        'branches': [
            {'operator': 'AND', 'order': 'q1<q2', 'delta': '49/1500',
             'strict_positive_polynomials': [
                 [[-1,1,0],[1,0,1]],
                 [[-1500,1,0],[1451,0,1],[49,1,1]]]},
            {'operator': 'AND', 'order': 'q1>q2', 'delta': '249/1700',
             'strict_positive_polynomials': [
                 [[1,1,0],[-1,0,1]],
                 [[1451,1,0],[-1700,0,1],[249,1,1]]]}]}


def main():
    old = json.loads((ROOT/SOURCE).read_text())
    assert old['status']=='READY' and old['target']=='17/5'
    assert len(old['entries'])==old['entry_count']==258
    entries = deepcopy(old['entries'])
    amended = []
    for entry in entries:
        assert 'additional_necessary_constraints' not in entry
        if entry['Y_extrema']==[0,3]:
            assert entry['free_Y_vertex_indices']==[1,2]
            entry['additional_necessary_constraints'] = [cut()]
            amended.append(entry['entry_id'])
    assert len(amended)==70
    rectangle = [[Q(1,8),Q(63,500)],[Q(127,1000),Q(16,125)]]
    (xl,xh),(yl,yh) = rectangle
    maxgap, rhs = yh-xl, Q(49,1500)*yl*(1-xh)
    assert xh<yl and maxgap<rhs
    output = {
        'status': 'READY', 'target': '17/5', 'class_index': 5,
        'scope': 'Necessary residual-domain refinement for actual hollow strict facet-contact tetrahedra, global lattice width >17/5. No complete class exclusion or finite continuous coverage claimed.',
        'source_queue': binding(SOURCE),
        'analytic_sources': [binding(THEOREM),binding(ORDER)],
        'boolean_semantics': old['boolean_semantics']+' Additionally, AND every additional_necessary_constraint when present. Its OR branches each require every listed polynomial to be strictly positive. A term [c,i,j] means c*q1^i*q2^j. Missing additional constraints means true.',
        'coordinate_semantics': old['coordinate_semantics'],
        'inherited_measure_semantics': 'Every entry measure and overlap field is preserved verbatim from the preceding queue and describes that preceding domain only. No updated residual area or volume is asserted.',
        'entry_count': len(entries), 'entries': entries,
        'amended_entry_count': len(amended), 'amended_entry_ids': amended,
        'unchanged_entry_count': len(entries)-len(amended),
        'newly_removed_entries': [],
        'removal_scope': 'No emptiness classification of individual amended entries was attempted; all258 entries retained.',
        'new_excluded_closed_rectangle': {
            'Y_extrema': [0,3], 'box': [[str(a),str(b)] for a,b in rectangle],
            'area': str((xh-xl)*(yh-yl)),
            'order': 'q1<q2', 'maximum_gap': str(maxgap),
            'minimum_delta_product_bound': str(rhs),
            'strict_margin': str(rhs-maxgap),
            'proof': 'Throughout the closed rectangle, q1<q2, q2-q1<=maximum_gap<minimum_delta_product_bound<=49*q2*(1-q1)/1500. Both disjunction branches fail. The rectangle is disjoint from all eight previously excluded Y03 closed rectangles.'},
        'solver_queries_run': 0, 'proof_kernel_calls_run': 0}
    path = ROOT/OUTPUT
    if path.exists():
        assert json.loads(path.read_text())==output, 'Existing output differs; do not overwrite.'
    else:
        path.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k: output[k] for k in ('status','entry_count','amended_entry_count','unchanged_entry_count','new_excluded_closed_rectangle')},indent=2))


if __name__=='__main__':
    main()
