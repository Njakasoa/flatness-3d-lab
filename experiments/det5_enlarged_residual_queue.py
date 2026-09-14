"""Exact incremental subtraction of one certified closed Y square; stdlib only.

No solver calls. The frozen predecessor is read but never modified. Endpoint
cells handle both overlapping certified rectangles and strict residual bounds.
"""
from collections import Counter
from copy import deepcopy
from fractions import Fraction as Q
from itertools import product
import argparse
import gzip
import hashlib
import json

from experiments.det5_certified_residual_queue import (
    ROOT, JOINT, PROOFS, OUTPUT as PREVIOUS, need, read, sha, rational_box,
    inside, measure, partition_representatives, strict_complement,
    outside_clause_holds, load_bound_inputs,
)

RECEIPT = 'results/det5_y_corner_enlarged_3_5.json'
OUTPUT = 'results/det5_enlarged_residual_queue.json'


def open_cells(original, rectangles):
    axes = []
    for axis, (lo, hi) in enumerate(original):
        endpoints = sorted({lo, hi} | {x for r in rectangles for x in r[axis] if lo <= x <= hi})
        axes.append([(a, b) for a, b in zip(endpoints, endpoints[1:]) if a < b])
    for cell in product(*axes):
        yield tuple((a+b)/2 for a, b in cell), measure(cell)


def outside_old(point, clauses):
    return all(outside_clause_holds(point, clause) for clause in clauses)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--receipt', default=RECEIPT)
    parser.add_argument('--output', default=OUTPUT)
    args = parser.parse_args()
    joint, old_proof, overlay, certified = load_bound_inputs()
    old, receipt = read(PREVIOUS), read(args.receipt)
    need(old['status']=='READY' and old['entry_count']==len(old['entries'])==258, 'frozen predecessor queue')
    need(old['source_joint']['sha256']==sha(JOINT) and old['certified_Y_proofs']['sha256']==sha(PROOFS), 'predecessor source bindings')
    need(receipt['status']=='unsat' and receipt['internal_complete_proof_check'], 'new complete refutation recorded')
    need(receipt['ethos']['exit_code']==0 and receipt['ethos']['stdout']=='correct' and not receipt['ethos']['stderr'], 'new external proof check recorded')
    need(receipt['target']=='17/5' and receipt['beta']=='37/102' and receipt['extrema']==[0,3], 'new theorem target and labeled chart')
    need(receipt['gauge_vectors']==old_proof['gauge_vectors'], 'same ten necessary target gauges')
    need(sha(receipt['input_path'])==receipt['input_sha256'], 'new input hash')
    need(sha(receipt['proof_path'])==receipt['compressed_proof_sha256'], 'new compressed proof hash')
    need(hashlib.sha256(gzip.decompress((ROOT/receipt['proof_path']).read_bytes())).hexdigest()==receipt['proof_sha256'], 'new expanded proof hash')
    square = rational_box(receipt['box'])
    need(len(square)==2 and square[0]==square[1] and 0<square[0][0]<square[0][1]==1, 'closed upper square')
    pending = {(tuple(c['Y_extrema']),tuple(c['U_extrema']),l['node']): l['box'] for c in joint['charts'] for l in c['pending_leaves']}
    need(len(pending)==259, 'frozen joint pending count')
    entries, removed, decisions = [], [], []
    counts = Counter({k:0 for k in ('wholly_removed','partial_positive_area','boundary_only','no_new_intersection')})
    charts = {}
    representatives_checked = 0
    total_old_volume = total_new_volume = total_removed_volume = Q(0)
    seen = set()
    for entry in old['entries']:
        key = (tuple(entry['Y_extrema']),tuple(entry['U_extrema']),entry['node'])
        need(key not in seen and key in pending and pending[key]==entry['box'], 'original source box preserved exactly')
        seen.add(key)
        box = rational_box(entry['box'])
        old_rects = [rational_box(r['box']) for r in certified.get(key[0],[])]
        applies = entry['Y_extrema']==receipt['extrema']
        cuts = old_rects + ([square] if applies else [])
        points = partition_representatives(box[:2],cuts)
        old_hits, new_hits, survivors = [], [], []
        for p in points:
            previous = outside_old(p,entry['outside_Y_clauses'])
            need(previous==(not any(inside(p,r) for r in old_rects)), 'predecessor clauses exactly subtract old union')
            if previous:
                old_hits.append(p)
                (new_hits if applies and inside(p,square) else survivors).append(p)
        representatives_checked += len(points)
        need(old_hits, 'predecessor entry is nonempty')
        prior_area = removed_area = Q(0)
        for p, area in open_cells(box[:2],cuts):
            if outside_old(p,entry['outside_Y_clauses']):
                prior_area += area
                if applies and inside(p,square):
                    removed_area += area
        need(prior_area/measure(box[:2])==Q(entry['remaining_measure_fraction']), 'predecessor exact area')
        wholly = not survivors
        kind = ('wholly_removed' if wholly else 'partial_positive_area' if removed_area else
                'boundary_only' if new_hits else 'no_new_intersection')
        need(not wholly or removed_area==prior_area, 'removed entry has no residual volume')
        counts[kind] += 1
        chart = f'Y{key[0][0]}{key[0][1]}_U{key[1][0]}{key[1][1]}'
        charts.setdefault(chart,Counter())[kind] += 1
        updated = deepcopy(entry)
        if new_hits and not wholly:
            literals = strict_complement(square,box[:2],entry['free_Y_vertex_indices'])
            need(literals, 'retained entry has satisfiable complement')
            updated['outside_Y_clauses'].append({
                'certified_leaf':'0_3:enlarged_'+str(square[0][0]).replace('/','_'),
                'excluded_closed_Y_box':receipt['box'], 'proof_input_path':receipt['input_path'],
                'proof_receipt_path':args.receipt, 'literals':literals})
        for p in points:
            expected = outside_old(p,entry['outside_Y_clauses']) and not (applies and inside(p,square))
            actual = False if wholly else outside_old(p,updated['outside_Y_clauses'])
            need(expected==actual, 'exact incremental subtraction including all boundary cells')
        remaining_area = prior_area-removed_area
        info = {'entry_id':entry['entry_id'],'Y_extrema':entry['Y_extrema'],'U_extrema':entry['U_extrema'],
                'node':entry['node'],'classification':kind,'previous_Y_area':str(prior_area),
                'newly_excluded_Y_area':str(removed_area),'remaining_Y_area':str(remaining_area),
                'newly_excluded_fraction_of_previous':str(removed_area/prior_area)}
        decisions.append(info)
        if wholly:
            removed.append({**deepcopy(entry),'new_removal':info})
        else:
            updated['previous_remaining_measure_fraction'] = entry['remaining_measure_fraction']
            updated['remaining_measure_fraction'] = str(remaining_area/measure(box[:2]))
            updated['enlargement_overlap_classification'] = kind
            entries.append(updated)
        u_area = measure(box[2:])
        total_old_volume += prior_area*u_area
        total_new_volume += remaining_area*u_area
        total_removed_volume += removed_area*u_area
    need(total_old_volume==total_new_volume+total_removed_volume, 'exact labeled four-volume balance')
    need(len(entries)+len(removed)==258, 'complete predecessor partition')
    # Union area is evaluated once per elementary open cell, never by summing
    # pairwise overlap areas of rectangles that now overlap in their interiors.
    target_old = [rational_box(r['box']) for r in certified[(0,3)]]
    old_area = enlarged_area = new_area = Q(0)
    new_cells = []
    for p, area in open_cells([(Q(0),Q(1))]*2,target_old+[square]):
        in_old = any(inside(p,r) for r in target_old)
        in_new = inside(p,square)
        old_area += area*in_old
        enlarged_area += area*(in_old or in_new)
        new_area += area*(in_new and not in_old)
        if in_new and not in_old:
            new_cells.append({'midpoint':list(map(str,p)),'area':str(area)})
    need(old_area==Q(7,16) and enlarged_area==old_area+new_area, 'exact union area balance')
    output = {
        'status':'READY','scope':'Exact residual-domain update in the labeled determinant-five Y/U charts for the global target width >17/5. No whole-class exclusion, symmetry transport, or validation of inherited joint UNSAT labels is claimed.',
        'source_queue':{'path':PREVIOUS,'sha256':sha(PREVIOUS),'entry_count':258},
        'source_joint':old['source_joint'],'old_certified_Y_proofs':old['certified_Y_proofs'],
        'new_certified_Y_proof':{'path':args.receipt,'sha256':sha(args.receipt),'extrema':receipt['extrema'],
          'box':receipt['box'],'input_path':receipt['input_path'],'input_sha256':receipt['input_sha256'],
          'proof_path':receipt['proof_path'],'compressed_proof_sha256':receipt['compressed_proof_sha256']},
        'target':'17/5','class_index':5,
        'boolean_semantics':old['boolean_semantics'],'coordinate_semantics':old['coordinate_semantics'],
        'overlap_counts':dict(counts),'per_chart_counts':{k:dict(v) for k,v in charts.items()},
        'entry_count':len(entries),'entries':entries,'newly_removed_entries':removed,'per_previous_entry':decisions,
        'Y03_unit_chart_area':{'old_certified_union':str(old_area),'new_square':str(measure(square)),
            'new_square_outside_old_union':str(new_area),'updated_certified_union':str(enlarged_area),
            'new_positive_area_cells':new_cells},
        'labeled_pending_four_volume':{'previous':str(total_old_volume),'newly_excluded':str(total_removed_volume),'remaining':str(total_new_volume),
            'scope':'Sum of box measures across labeled charts; not invariant geometric volume and not a coverage percentage of the class.'},
        'exact_validation':{'endpoint_partition_representatives_checked':representatives_checked,
            'method':'Partition at every old/new rectangle endpoint; evaluate each singleton and open-interval midpoint. All predicates are constant on every Cartesian cell. Areas sum disjoint open cells. U bounds stay unchanged.',
            'old_half_entries_preserved':sum(e['previous_remaining_measure_fraction']=='1/2' and e['remaining_measure_fraction']=='1/2' for e in entries)},
        'solver_queries_run':0,'proof_kernel_calls_run':0}
    need(output['exact_validation']['old_half_entries_preserved']==6,'all six old half boxes preserved')
    destination = ROOT/args.output
    need(destination.resolve() not in {(ROOT/PREVIOUS).resolve(),(ROOT/JOINT).resolve(),(ROOT/PROOFS).resolve()}, 'never overwrite old archives')
    if destination.exists():
        need(json.loads(destination.read_text())==output, 'existing enlarged queue differs; no overwrite')
    else:
        destination.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:output[k] for k in ('status','entry_count','overlap_counts','per_chart_counts','Y03_unit_chart_area','exact_validation')},indent=2))


if __name__=='__main__':
    main()
