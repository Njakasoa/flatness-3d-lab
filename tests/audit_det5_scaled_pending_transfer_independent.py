"""Independent formulas, inherited-leaf binding and rational SAT transfer audit.

Reuses the independent base-frame auditor; imports no discovery code and runs
no solver. Recorded UNSAT labels are deliberately not certified by this audit.
"""
from collections import Counter
from copy import deepcopy
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import z3
from audit_det5_scaled_frame_independent import reconstruct, compare, rat, inverse, need, R, TARGET, canonical

ROOT = Path(__file__).resolve().parents[1]
U = (1,-1,-2)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bind_leaf(row, source):
    charts = [c for c in source['charts'] if c['Y_extrema']==row['Y_extrema'] and c['U_extrema']==row['U_extrema']]
    need(len(charts)==1, 'unique inherited Y/U chart')
    leaves = [p for p in charts[0]['pending_leaves'] if p['node']==row['node']]
    need(len(leaves)==1 and leaves[0]['box']==row['box'], 'exact inherited pending leaf')
    need(len(row['box'])==4 and all(Q(0)<=Q(l)<=Q(h)<=Q(1) for l,h in row['box']), 'normalized four-box domain')


def formula(C,S,row):
    base_row = {'Y_extrema':row['Y_extrema'], 'kind':'relaxation'}
    base,F,T,b,lifted,dirs,envelopes = reconstruct(C,S,base_row)
    e = list(base)
    cuts = {'Y_box':[], 'U_box':[], 'volume_span':[], 'barycentric_volume':[]}
    box = [[Q(x) for x in pair] for pair in row['box']]
    L,H = row['Y_extrema']
    # Every shared product is either an existing lifted scalar, zero, or F_ij.
    W = {(i,j,k):(z3.Real(f'w{i}_{j}_{k}') if (i,j,k) in lifted else z3.simplify(F[i][j]*T[i][k]))
         for i,j,k in product(range(4),range(4),range(3))}
    for i,(lo,hi) in zip([i for i in range(4) if i not in (L,H)],box[:2]):
        t = T[i][1]
        cuts['Y_box'].extend((t>=rat(lo),t<=rat(hi)))
        for j in range(4):
            if j==i:
                continue
            need((i,j,1) in lifted, 'free-height product already shared')
            f,w = F[i][j],W[i,j,1]
            cuts['Y_box'].extend((w-rat(lo)*f>=0,rat(hi)*f-w>=0,
                                  w-t-rat(hi)*f+rat(hi)>=0,t+rat(lo)*f-rat(lo)-w>=0))
    A,B = row['U_extrema']
    heights = [sum(rat(U[k])*T[i][k] for k in range(3)) for i in range(4)]
    span = heights[B]-heights[A]
    cuts['U_box'].append(span>rat(TARGET)*b)
    for h in heights:
        cuts['U_box'].extend((h>=heights[A],h<=heights[B]))
    for i,(lo,hi) in zip([i for i in range(4) if i not in (A,B)],box[2:]):
        cuts['U_box'].extend((heights[i]-heights[A]>=rat(lo)*span,
                              heights[i]-heights[A]<=rat(hi)*span))
    for u in dirs:
        hP = [sum(u[k]*p[k] for k in range(3)) for p in C['contact_points']]
        cap = rat(R*(max(hP)-min(hP)))*b
        for i,j in combinations(range(4),2):
            difference = sum(rat(u[k])*(T[i][k]-T[j][k]) for k in range(3))
            cuts['volume_span'].extend((difference<cap,-difference<cap))
    # Derive affine contact coordinates by Gaussian inversion, not hardcoded ell.
    P = C['contact_points']
    Bary = inverse([[1]*4]+[[p[k] for p in P] for k in range(3)])
    center = [sum(W[i,0,k] for i in range(4)) for k in range(3)]
    for i in range(4):
        homogeneous = [b]+[T[i][k]-center[k] for k in range(3)]
        bary = [sum(rat(a)*x for a,x in zip(r,homogeneous)) for r in Bary]
        for mask in range(1,16):
            cuts['barycentric_volume'].append(sum(bary[j] for j in range(4) if mask&(1<<j))<rat(R)*b)
    for group in cuts.values():
        e.extend(group)
    return e,F,T,b,lifted,dirs,cuts


def check_assignment(row, assertions, F, T, b, dirs, C):
    values = {name:Q(v) for name,v in row['assignment'].items()}
    substitutions = [(z3.Real(name),rat(value)) for name,value in values.items()]
    for assertion in assertions:
        need(z3.is_true(z3.simplify(z3.substitute(assertion,*substitutions))), 'saved rational SAT assignment satisfies every assertion')
    fm = [[z3.simplify(z3.substitute(x,*substitutions)).as_fraction() for x in r] for r in F]
    need(fm==[list(map(Q,r)) for r in row['F']], 'saved F binding')
    tm = [[z3.simplify(z3.substitute(x,*substitutions)).as_fraction() for x in r] for r in T]
    bm = z3.simplify(z3.substitute(b,*substitutions)).as_fraction()
    residual = max(abs(values[f'w{i}_{j}_{k}']-fm[i][j]*tm[i][k])
                   for i,j,k in product(range(4),range(4),range(3)) if f'w{i}_{j}_{k}' in values)
    try:
        fi = inverse(fm)
    except (StopIteration,ZeroDivisionError):
        need(not row['actual_F']['invertible'], 'singular actual F binding')
        body = {'invertible':False}
    else:
        need(row['actual_F']['invertible'], 'nonsingular actual F binding')
        V = [[sum(Q(C['contact_points'][i][k])*fi[i][j] for i in range(4)) for k in range(3)] for j in range(4)]
        widths = {tuple(u):max(sum(u[k]*v[k] for k in range(3)) for v in V)-min(sum(u[k]*v[k] for k in range(3)) for v in V) for u in dirs}
        minimum = min(widths.values())
        need(minimum==Q(row['actual_F']['minimum_of_complete_15']), 'independent actual-F direction minimum')
        need(widths[tuple(row['actual_F']['minimizing_list_direction'])]==minimum, 'actual-F minimizing direction')
        need(row['actual_F']['all_15_above_target']==(minimum>TARGET), 'actual-F width target flag')
        body = {'invertible':True, 'minimum_of_complete_15':str(minimum), 'all_15_above_target':minimum>TARGET}
    return {'node':row['node'], 'Y_extrema':row['Y_extrema'], 'U_extrema':row['U_extrema'],
            'saved_rational_variables':len(values), 'maximum_product_residual':str(residual), 'actual_F':body}


def rejected(action, message):
    try:
        action()
    except (ValueError,AssertionError):
        return
    raise ValueError('accepted mutation: '+message)


def main():
    path = ROOT/'results/det5_scaled_pending_transfer.json'
    archive = json.loads(path.read_text())
    source_path = ROOT/archive['source']['path']
    need(sha(source_path)==archive['source']['sha256'], 'frozen source hash')
    source = json.loads(source_path.read_text())
    need(len(source['queries'])==archive['source']['query_count']==953, 'source query count')
    C = next(c for c in json.loads((ROOT/'certificates/nonunimodular_observer_guards.json').read_text())['classes'] if c['class_index']==5)
    S = next(c for c in json.loads((ROOT/'results/two_vector_class_scan.json').read_text())['classes'] if c['class_index']==5)
    keys, receipts, sat = set(),[],[]
    for row in archive['queries']:
        bind_leaf(row,source)
        key = (tuple(row['Y_extrema']),tuple(row['U_extrema']),row['node'])
        need(key not in keys, 'no duplicate transferred query')
        keys.add(key)
        smt = ROOT/row['path']
        need(sha(smt)==row['input_sha256'], 'archived input hash')
        actual = list(z3.parse_smt2_file(str(smt)))
        expected,F,T,b,lifted,dirs,cuts = formula(C,S,row)
        compare(expected,actual)
        need(row['status'] in ('sat','unsat','unknown'), 'recognized status label')
        receipts.append({'path':row['path'],'input_sha256':row['input_sha256'],'status':row['status'],
                         'assertions':len(actual),'additional_groups':{k:len(v) for k,v in cuts.items()}})
        if row['status']=='sat':
            sat.append(check_assignment(row,actual,F,T,b,dirs,C))
    first = archive['queries'][0]
    bad = deepcopy(first)
    bad['box'][0] = ['0','0']
    rejected(lambda:bind_leaf(bad,source), 'inherited box altered')
    actual = list(z3.parse_smt2_file(str(ROOT/first['path'])))
    expected,F,T,b,lifted,dirs,cuts = formula(C,S,first)
    for group in ('Y_box','U_box','volume_span','barycentric_volume'):
        altered = list(expected)
        # An explicit false atom ensures any canonicalized valid duplicates
        # cannot hide this corrupted group entry.
        target = cuts[group][0]
        altered.append(z3.Not(target))
        rejected(lambda:compare(altered,actual), 'reversed '+group+' atom')
    row = next(r for r in archive['queries'] if r['status']=='sat')
    bad = deepcopy(row)
    bad['assignment']['scaled_b'] = '4'
    actual = list(z3.parse_smt2_file(str(ROOT/row['path'])))
    expected,F,T,b,lifted,dirs,cuts = formula(C,S,row)
    rejected(lambda:check_assignment(bad,actual,F,T,b,dirs,C), 'changed rational SAT gap')
    result = {'status':'PASS', 'scope':'Independent encoding and inherited pending-leaf binding; exact saved SAT assignments. No UNSAT proof-kernel check or full class exclusion.',
              'archive_sha256':sha(path),'source_sha256':sha(source_path),'solver_queries':0,
              'query_count':len(receipts),'recorded_status_counts':dict(Counter(r['status'] for r in receipts)),
              'rejected_mutations':6,'inputs':receipts,'saved_rational_SAT_checks':sat}
    (ROOT/'results/det5_scaled_pending_transfer_validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','query_count','recorded_status_counts','rejected_mutations','solver_queries')},indent=2))


if __name__=='__main__':
    main()
