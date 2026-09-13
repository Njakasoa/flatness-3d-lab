"""Exact overlay of 12 certified Y rectangles on 259 frozen joint pending boxes.

No solver or proof-kernel calls. Uses the previously reviewed full-matrix
statement generator to bind geometric data to existing proof inputs.
"""
from collections import Counter
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import gzip
import hashlib
import json
from replay_height_cover_cvc5 import statement
from check_height_ethos import real_reference, ETHOS_REV, CVC5_REV

ROOT=Path(__file__).resolve().parents[1]


def need(c,message):
    if not c:raise ValueError(message)


def read(p):return json.loads((ROOT/p).read_text())
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def boxq(box):return [tuple(map(Q,interval)) for interval in box]
def boxstr(box):return [[str(x) for x in pair] for pair in box]
def measure(box):
    out=Q(1)
    for lo,hi in box:out*=max(Q(0),hi-lo)
    return out


def tagged_box(node,dimension):
    need(node.startswith('r') and set(node[1:])<={'0','1'},'binary leaf tag')
    box=[(Q(0),Q(1)) for _ in range(dimension)]
    for digit in node[1:]:
        axis=max(range(dimension),key=lambda k:box[k][1]-box[k][0])
        lo,hi=box[axis];mid=(lo+hi)/2
        box[axis]=(lo,mid) if digit=='0' else (mid,hi)
    return box


def intersection(a,b):
    out=[(max(l,L),min(h,H)) for (l,h),(L,H) in zip(a,b)]
    return None if any(lo>hi for lo,hi in out) else out


def overlay(projected,rectangles):
    pieces=[]
    for r in rectangles:
        overlap=intersection(projected,boxq(r['box']))
        if overlap is not None:
            pieces.append({'certified_Y_leaf':r['node'],'intersection':boxstr(overlap),'intersection_area':str(measure(overlap))})
    area=measure(projected)
    need(area>0,'nondegenerate pending Y projection')
    covered=sum(Q(p['intersection_area']) for p in pieces)
    need(0<=covered<=area,'disjoint certified rectangle area bound')
    if covered==area:classification='wholly_covered'
    elif covered>0:classification='partially_covered_positive_area'
    elif pieces:classification='boundary_only_intersection'
    else:classification='no_intersection'
    return {'classification':classification,'covered_Y_area':str(covered),'Y_area':str(area),
            'covered_fraction':str(covered/area),'intersections':pieces}


def main():
    old_path='results/det5_height_interval.json';joint_path='results/det5_joint_short_gauges.json'
    proof_path='results/det5_class5_y_cvc5_validation.json'
    old,joint,proof=read(old_path),read(joint_path),read(proof_path)
    need(proof['status']=='PASS' and proof['source_path']==old_path and proof['source_sha256']==sha(old_path),'certified source snapshot binding')
    need(proof['class_index']==5 and proof['target']=='17/5' and proof['beta']=='37/102','geometric target classification')
    need(proof['ethos_revision']==ETHOS_REV and proof['cvc5_signature_revision']==CVC5_REV,'pinned checker/signature receipt')
    C=next(c for c in read('certificates/nonunimodular_observer_guards.json')['classes'] if c['class_index']==5)
    S=next(c for c in read('results/two_vector_class_scan.json')['classes'] if c['class_index']==5)
    need(C['contact_points']==[[0,0,0],[5,1,2],[0,1,0],[0,0,1]],'exact d5a2 contact ordering')
    vectors=sorted(set(map(tuple,C['primitive_contact_edge_directions']))|{tuple(v['vector']) for v in S['eligible_vectors']})
    need(len(vectors)==10 and vectors==list(map(tuple,proof['gauge_vectors'])),'complete certified ten-gauge input data')
    oldrows={(r['class_index'],tuple(r['extrema']),r['node']):r for r in old['queries']}
    declared={(tuple(c['extrema']),node) for c in old['charts'] if c['class_index']==5 for node in c['closed_leaves']}
    need(len(declared)==12 and len(proof['leaves'])==12,'all twelve old weak Y exclusions certified')
    certificates={};by_y={}
    for r in proof['leaves']:
        key=(tuple(r['extrema']),r['node'])
        need(key in declared and key not in certificates,'one certificate per original closed leaf')
        original=oldrows[5,key[0],key[1]]
        need(original['status']=='unsat' and original['box']==r['box'] and original['path']==r['source_input_path'],'original leaf binding')
        need(boxq(r['box'])==tagged_box(r['node'],2),'exact original Y dyadic rectangle')
        need(sha(r['source_input_path'])==r['source_input_sha256'] and sha(r['input_path'])==r['input_sha256'],'original and proof-input hashes')
        encoded=statement(C,vectors,r['extrema'],boxq(r['box']))
        need(encoded==(ROOT/r['input_path']).read_text(),'proof input exactly reconstructs geometric rectangle')
        reference,_,_=real_reference(encoded)
        need(hashlib.sha256(reference.encode()).hexdigest()==r['reference_sha256'],'external reference normalization binding')
        packed=(ROOT/r['proof_path']).read_bytes()
        need(hashlib.sha256(packed).hexdigest()==r['compressed_proof_sha256'] and hashlib.sha256(gzip.decompress(packed)).hexdigest()==r['proof_sha256'],'compressed and expanded proof binding')
        need(r['status']=='unsat' and r['internal_proof_check'] and r['check_proofs_complete'],'complete cvc5 refutation record')
        need(not any('TRUST' in p or 'SORRY' in p for p in r['proof_rules']),'no recorded admitted proof rule')
        need(r['ethos']['exit_code']==0 and r['ethos']['stdout']=='correct' and not r['ethos']['stderr'],'recorded external proof check')
        certificates[key]=r;by_y.setdefault(key[0],[]).append(r)
    need(set(certificates)==declared,'no old exclusion omitted or added')
    need(any(r.get('negative_control')=='unreferenced assumption rejected' for r in proof['leaves']),'reference negative control recorded')
    for rects in by_y.values():
        for a,b in combinations(rects,2):
            cut=intersection(boxq(a['box']),boxq(b['box']))
            need(cut is None or measure(cut)==0,'certified Y rectangles have disjoint interiors')
    need(len(joint['queries'])==953,'frozen joint campaign query count')
    totals=Counter();charts=[];leaves=[];seen=set()
    for chart in joint['charts']:
        ext=tuple(chart['Y_extrema']);rects=by_y.get(ext,[]);counts=Counter()
        for leaf in chart['pending_leaves']:
            key=(ext,tuple(chart['U_extrema']),leaf['node'])
            need(key not in seen,'unique joint pending box');seen.add(key)
            box=boxq(leaf['box'])
            need(len(box)==4 and box==tagged_box(leaf['node'],4),'exact joint normalized four-box')
            row=overlay(box[:2],rects);counts[row['classification']]+=1;totals[row['classification']]+=1
            leaves.append({'Y_extrema':list(ext),'U_extrema':chart['U_extrema'],**leaf,**row,
                           'covered_four_volume':str(measure(box)*Q(row['covered_fraction']))})
        counts={k:counts[k] for k in ['wholly_covered','partially_covered_positive_area','boundary_only_intersection','no_intersection']}
        charts.append({'Y_extrema':list(ext),'U_extrema':chart['U_extrema'],'pending_boxes':len(chart['pending_leaves']),
                       'certified_Y_rectangles':len(rects),**counts,
                       'partially_covered_including_boundary':counts['partially_covered_positive_area']+counts['boundary_only_intersection']})
    need(len(leaves)==259,'all 259 original pending boxes accounted')
    # Controls distinguish a union cover from single-rectangle containment,
    # and genuine endpoint overlap from positive-area coverage.
    square=[(Q(0),Q(1)),(Q(0),Q(1))]
    two=[{'node':'left','box':[['0','1/2'],['0','1']]},{'node':'right','box':[['1/2','1'],['0','1']]}]
    need(overlay(square,two)['classification']=='wholly_covered','union of two halves covers square')
    touching=[{'node':'touch','box':[['1','2'],['0','1']]}]
    need(overlay(square,touching)['classification']=='boundary_only_intersection','closed endpoint contact distinguished')
    partial=[{'node':'quarter','box':[['0','1/2'],['0','1/2']]}]
    need(overlay(square,partial)['covered_fraction']=='1/4','partial area exact')
    need(overlay(square,[])['classification']=='no_intersection','empty old chart')
    totals={k:totals[k] for k in ['wholly_covered','partially_covered_positive_area','boundary_only_intersection','no_intersection']}
    result={'status':'PASS','scope':'Exact geometric overlay of externally certified old Y rectangles onto frozen joint pending boxes. No solver/kernel rerun; remaining joint UNSAT labels are not certified by this overlay.',
            'source_Y_sha256':sha(old_path),'source_joint_sha256':sha(joint_path),'proof_receipt_sha256':sha(proof_path),
            'certified_Y_rectangles':12,'original_pending_boxes':259,'totals':totals,
            'three_way_geometric_counts':{'wholly_covered':totals['wholly_covered'],
                'partially_covered':totals['partially_covered_positive_area']+totals['boundary_only_intersection'],
                'uncovered':totals['no_intersection']},
            'positive_area_counts':{'wholly_covered':totals['wholly_covered'],
                'partially_covered':totals['partially_covered_positive_area'],
                'no_positive_area_coverage':totals['boundary_only_intersection']+totals['no_intersection']},
            'remaining_original_boxes_after_whole_box_removal':259-totals['wholly_covered'],
            'certified_Y_areas':{','.join(map(str,k)):str(sum(measure(boxq(r['box'])) for r in rs)) for k,rs in by_y.items()},
            'coverage_method':'Intersect Y projections with all certified rectangles. Their interiors are disjoint; sum exact rational areas. Full area implies full containment since the rectangle union is closed. Boundary-only intersections are recorded separately.',
            'per_chart':charts,'per_pending_box':leaves,'solver_queries_run':0,'proof_kernel_calls_run':0,'geometric_controls':4}
    (ROOT/'results/det5_certified_y_overlay.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','totals','remaining_original_boxes_after_whole_box_removal','certified_Y_areas']},indent=2))


if __name__=='__main__':main()
