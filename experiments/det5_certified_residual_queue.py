"""Exact residual queue after subtracting certified closed Y rectangles.

Uses stdlib only. Keeps original four-dimensional boxes plus strict Boolean
complement clauses; never queries a solver or changes an older archive.
"""
from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
import gzip
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
JOINT = 'results/det5_joint_short_gauges.json'
PROOFS = 'results/det5_class5_y_cvc5_validation.json'
OVERLAY = 'results/det5_certified_y_overlay.json'
OUTPUT = 'results/det5_certified_residual_queue.json'


def need(condition, message):
    if not condition:
        raise ValueError(message)


def read(path):
    return json.loads((ROOT/path).read_text())


def sha(path):
    return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()


def rational_box(box):
    return [tuple(map(Q, interval)) for interval in box]


def measure(box):
    volume = Q(1)
    for lo, hi in box:
        volume *= max(Q(0), hi-lo)
    return volume


def intersect(a, b):
    c = [(max(lo, low), min(hi, high)) for (lo, hi), (low, high) in zip(a, b)]
    return None if any(lo>hi for lo, hi in c) else c


def inside(point, box):
    return all(lo<=x<=hi for x, (lo, hi) in zip(point, box))


def dyadic_box(tag, dimension):
    need(tag.startswith('r') and set(tag[1:])<={'0', '1'}, 'binary source tag')
    box = [(Q(0), Q(1)) for _ in range(dimension)]
    for digit in tag[1:]:
        axis = max(range(dimension), key=lambda i: box[i][1]-box[i][0])
        lo, hi = box[axis]
        mid = (lo+hi)/2
        box[axis] = (lo, mid) if digit=='0' else (mid, hi)
    return box


def strict_complement(rectangle, original, free_vertices):
    """Complement of a CLOSED rectangle, simplified only inside original box.

    A closed intersection has already been established. Literals impossible
    on original are removed. No strict endpoint is changed to a weak one.
    """
    literals = []
    for axis, ((low, high), (lo, hi)) in enumerate(zip(rectangle, original)):
        if lo<low:  # Otherwise q<low is impossible throughout original.
            literals.append({'free_coordinate':axis, 'vertex_index':free_vertices[axis],
                             'relation':'<', 'threshold':str(low)})
        if hi>high:  # Otherwise q>high is impossible throughout original.
            literals.append({'free_coordinate':axis, 'vertex_index':free_vertices[axis],
                             'relation':'>', 'threshold':str(high)})
    return literals


def outside_clause_holds(point, clause):
    need(all(a['relation'] in ('<','>') for a in clause['literals']), 'strict complement relations only')
    return any(point[a['free_coordinate']]<Q(a['threshold']) if a['relation']=='<' else
               point[a['free_coordinate']]>Q(a['threshold']) for a in clause['literals'])


def residual_contains(point, entry):
    """Evaluate all four original box bounds and the strict Y exclusions."""
    box = rational_box(entry['box'])
    return inside(point, box) and all(outside_clause_holds(point[:2], c) for c in entry['outside_Y_clauses'])


def partition_representatives(original, rectangles):
    """Represent every point/open-interval cell induced by all cut endpoints."""
    representatives = []
    for axis, (lo, hi) in enumerate(original):
        edges = {lo, hi}
        for rectangle in rectangles:
            edges.update(x for x in rectangle[axis] if lo<=x<=hi)
        edges = sorted(edges)
        points = sorted(set(edges)|{(a+b)/2 for a,b in zip(edges,edges[1:])})
        representatives.append(points)
    return list(product(*representatives))


def verify_subtraction(original, rectangles, clauses, removed):
    points = partition_representatives(original, rectangles)
    survivors = 0
    for point in points:
        expected = not any(inside(point, r) for r in rectangles)
        actual = False if removed else all(outside_clause_holds(point, c) for c in clauses)
        need(expected==actual, 'exact continuous subtraction on endpoint partition')
        survivors += int(actual)
    need((survivors==0)==removed, 'whole-box removal iff residual is empty')
    return len(points)


def load_bound_inputs():
    joint, proof, overlay = read(JOINT), read(PROOFS), read(OVERLAY)
    need(len(joint['queries'])==953, 'frozen 953-query joint source')
    need(proof['status']=='PASS' and proof['class_index']==5 and proof['target']=='17/5' and
         proof['beta']=='37/102', 'certified determinant-five Y exclusions')
    need(overlay['status']=='PASS' and overlay['source_joint_sha256']==sha(JOINT) and
         overlay['proof_receipt_sha256']==sha(PROOFS), 'existing exact-overlay source binding')
    need(proof['source_sha256']==sha(proof['source_path'])==overlay['source_Y_sha256'], 'original weak-Y snapshot binding')
    old = read(proof['source_path'])
    old_closed = {(tuple(c['extrema']), tag) for c in old['charts'] if c['class_index']==5 for tag in c['closed_leaves']}
    old_queries = {(tuple(r['extrema']), r['node']):r for r in old['queries'] if r['class_index']==5}
    need(len(old_closed)==12 and len(proof['leaves'])==12, 'twelve distinct certified old rectangles')
    seen, rectangles = set(), {}
    for r in proof['leaves']:
        key = (tuple(r['extrema']), r['node'])
        need(key in old_closed and key not in seen, 'certified leaf belongs uniquely to old closed set')
        seen.add(key)
        need(r['box']==old_queries[key]['box'] and rational_box(r['box'])==dyadic_box(r['node'],2), 'original exact Y rectangle')
        need(r['source_input_path']==old_queries[key]['path'] and sha(r['source_input_path'])==r['source_input_sha256'], 'original query input binding')
        need(sha(r['input_path'])==r['input_sha256'] and sha(r['proof_path'])==r['compressed_proof_sha256'], 'proof input and compressed payload binding')
        expanded = gzip.decompress((ROOT/r['proof_path']).read_bytes())
        need(hashlib.sha256(expanded).hexdigest()==r['proof_sha256'], 'expanded CPC payload binding')
        need(r['status']=='unsat' and r['internal_proof_check'] and r['check_proofs_complete'], 'recorded complete cvc5 proof')
        need(r['ethos']['exit_code']==0 and r['ethos']['stdout']=='correct' and not r['ethos']['stderr'], 'recorded successful external proof check')
        rectangles.setdefault(key[0], []).append(r)
    need(seen==old_closed, 'no certified region omitted or added')
    for rects in rectangles.values():
        for a,b in combinations(rects,2):
            overlap = intersect(rational_box(a['box']), rational_box(b['box']))
            need(overlap is None or measure(overlap)==0, 'certified rectangles have disjoint interiors')
    return joint, proof, overlay, rectangles


def main():
    joint, proof, overlay, rectangles = load_bound_inputs()
    previous = {(tuple(r['Y_extrema']),tuple(r['U_extrema']),r['node']):r for r in overlay['per_pending_box']}
    entries, removed, counts, validation_cache = [], [], Counter(), {}
    seen = set()
    for chart in joint['charts']:
        ext = tuple(chart['Y_extrema'])
        free_vertices = [i for i in range(4) if i not in ext]
        sources = rectangles.get(ext, [])
        all_rectangles = [rational_box(r['box']) for r in sources]
        for leaf in chart['pending_leaves']:
            key = (ext,tuple(chart['U_extrema']),leaf['node'])
            need(key not in seen and key in previous, 'one exact residual decision per original pending leaf')
            seen.add(key)
            box = rational_box(leaf['box'])
            need(box==dyadic_box(leaf['node'],4) and measure(box)>0, 'original closed four-box preserved')
            base = {'entry_id':f'{ext[0]}_{ext[1]}_{chart["U_extrema"][0]}_{chart["U_extrema"][1]}_{leaf["node"]}',
                    'Y_extrema':list(ext),'U_extrema':chart['U_extrema'],'node':leaf['node'],'box':leaf['box']}
            matches, clauses = [], []
            for r, rectangle in zip(sources, all_rectangles):
                overlap = intersect(box[:2], rectangle)
                if overlap is None:
                    continue
                matches.append((r, overlap))
                clauses.append({'certified_leaf':f'{ext[0]}_{ext[1]}:{r["node"]}',
                                'excluded_closed_Y_box':r['box'], 'proof_input_path':r['input_path'],
                                'literals':strict_complement(rectangle, box[:2], free_vertices)})
            covered = sum(measure(overlap) for r,overlap in matches)
            total = measure(box[:2])
            need(0<=covered<=total, 'exact covered area')
            wholly = covered==total
            kind = 'wholly_covered' if wholly else 'partially_covered_positive_area' if covered else 'boundary_only_intersection' if matches else 'no_intersection'
            need(kind==previous[key]['classification'] and covered/total==Q(previous[key]['covered_fraction']), 'independent overlay agreement')
            counts[kind] += 1
            cache_key = (ext,tuple(box[:2]))
            if cache_key not in validation_cache:
                validation_cache[cache_key] = verify_subtraction(box[:2], all_rectangles, clauses, wholly)
            if wholly:
                removed.append({**base,'reason':'Entire closed Y projection is covered by certified closed rectangles.',
                                'certified_leaves':[c['certified_leaf'] for c in clauses]})
                continue
            need(all(c['literals'] for c in clauses), 'no false complement clause in a retained entry')
            entries.append({**base,'domain_type':'closed_box_with_strict_Y_exclusions',
                            'free_Y_vertex_indices':free_vertices,'outside_Y_clauses':clauses,
                            'prior_overlap_classification':kind,'remaining_measure_fraction':str(1-covered/total)})
    need(len(seen)==259 and len(removed)==1 and len(entries)==258, 'exact whole-box removal count')
    need(counts==Counter({'wholly_covered':1,'partially_covered_positive_area':6,'boundary_only_intersection':105,'no_intersection':147}), 'expected four-way overlap counts')
    need(sum(e['remaining_measure_fraction']=='1/2' for e in entries)==6, 'six exactly half-covered boxes')
    # Independently verify the explicit semi-open form of all six half boxes.
    for entry in entries:
        if entry['remaining_measure_fraction']!='1/2':
            continue
        half_box = rational_box(entry['box'])
        need(entry['Y_extrema']==[0,1] and half_box[:2]==[(Q(1,4),Q(1,2))]*2, 'six half-box Y shapes')
        mids = [(lo+hi)/2 for lo,hi in half_box[2:]]
        rects = [rational_box(r['box']) for r in rectangles[tuple(entry['Y_extrema'])]]
        for x,y in partition_representatives(half_box[:2],rects):
            need(residual_contains([x,y,*mids],entry)==(x>Q(3,8) and y<Q(1,2)), 'exact semi-open half-box description')
    # Endpoint-sensitive controls use the same evaluator as the consumer API.
    sample = next(e for e in entries if e['prior_overlap_classification']=='partially_covered_positive_area')
    b = rational_box(sample['box'])
    u = [(lo+hi)/2 for lo,hi in b[2:]]
    need(not residual_contains([Q(3,8),Q(3,8),*u],sample), 'closed removed threshold 3/8 is excluded')
    need(residual_contains([Q(7,16),Q(3,8),*u],sample), 'point strictly beyond removed half survives')
    need(not residual_contains([Q(7,16),Q(1,2),*u],sample), 'certified Y boundary at 1/2 is excluded')
    need(not residual_contains([Q(9,16),Q(3,8),*u],sample), 'original box bound remains active')
    output = {'status':'READY','scope':'Exact residual of the frozen declared joint pending domain minus twelve independently certified closed Y cylinders. No claim that inherited joint UNSAT labels are certified or that the whole class is excluded.',
              'source_joint':{'path':JOINT,'sha256':sha(JOINT),'query_count':953,'pending_boxes':259},
              'certified_Y_proofs':{'path':PROOFS,'sha256':sha(PROOFS),'rectangles':12},
              'overlay':{'path':OVERLAY,'sha256':sha(OVERLAY)},
              'target':'17/5','class_index':5,
              'boolean_semantics':'An entry is the AND of every closed original box bound and every outside_Y_clause. Each outside_Y_clause is the OR of its strict (< or >) literals. The full residual queue is the union of entries, interpreted in their labeled Y/U chart.',
              'coordinate_semantics':'box[0:2] are free normalized Y heights in free_Y_vertex_indices order; box[2:4] are free normalized U heights in increasing index order outside U_extrema. Clause free_coordinate is 0 or1 in the Y pair; vertex_index permits direct substitution T[vertex_index][1] in the scaled frame.',
              'removed_whole_boxes':removed,'entry_count':len(entries),'entries':entries,
              'overlap_counts':dict(counts),'entries_with_strict_exclusions':sum(bool(e['outside_Y_clauses']) for e in entries),
              'unchanged_entries':sum(not e['outside_Y_clauses'] for e in entries),
              'outside_clause_count':sum(len(e['outside_Y_clauses']) for e in entries),
              'exact_validation':{'distinct_Y_projections':len(validation_cache),'endpoint_partition_representatives_checked':sum(validation_cache.values()),
                'method':'All rectangle predicates and strict complement literals are constant on the Cartesian cells formed by every interval endpoint. Every endpoint singleton and open interval has a representative. Exact membership agreement on all representative pairs proves equality on the entire continuous Y projection; U bounds are unchanged.',
                'endpoint_controls':4},'solver_queries_run':0,'proof_kernel_calls_run':0}
    destination = ROOT/OUTPUT
    if destination.exists():
        need(json.loads(destination.read_text())==output, 'existing residual queue differs; do not overwrite a changed state')
    else:
        destination.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:output[k] for k in ('status','entry_count','entries_with_strict_exclusions','unchanged_entries','outside_clause_count','exact_validation')},indent=2))


if __name__=='__main__':
    main()
