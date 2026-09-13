"""Independently bind the reduced five-width box formula to the full transfer.

No discovery imports and no solver/checker calls. The external-checker receipt
is byte-bound as existing evidence; this script does not rerun its kernel.
"""
from copy import deepcopy
from itertools import combinations
from pathlib import Path
import gzip
import hashlib
import json
import z3
from audit_det5_scaled_pending_transfer_independent import formula, bind_leaf
from audit_det5_scaled_frame_independent import canonical, forms, compare, need, rat, TARGET

ROOT=Path(__file__).resolve().parents[1]
KEEP=((0,0,1),(0,1,-1),(1,-2,-2))
BOX=[['3/4','1'],['3/4','1'],['1/2','1'],['1/2','1']]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rejected(action,label):
    try:
        action()
    except (ValueError,AssertionError):
        return
    raise ValueError('accepted mutation '+label)


def main():
    transfer_path=ROOT/'results/det5_scaled_pending_transfer.json'
    transfer=json.loads(transfer_path.read_text())
    transfer_receipt=json.loads((ROOT/'results/det5_scaled_pending_transfer_validation.json').read_text())
    need(transfer_receipt['status']=='PASS' and transfer_receipt['archive_sha256']==sha(transfer_path),'existing full-transfer audit binding')
    source=json.loads((ROOT/transfer['source']['path']).read_text())
    archive_path=ROOT/'results/det5_scaled_leaf_width_core.json'
    archive=json.loads(archive_path.read_text())
    rows=[r for r in transfer['queries'] if r['path']==archive['source_path']]
    need(len(rows)==1,'unique full-transfer source')
    row=rows[0]
    need(row['Y_extrema']==[0,3] and row['U_extrema']==[0,3] and row['box']==BOX,'specified continuous four-box')
    bind_leaf(row,source)
    source_smt=ROOT/row['path']
    need(sha(source_smt)==archive['source_sha256']==row['input_sha256'],'full-transfer formula hash')
    C=next(c for c in json.loads((ROOT/'certificates/nonunimodular_observer_guards.json').read_text())['classes'] if c['class_index']==5)
    S=next(c for c in json.loads((ROOT/'results/two_vector_class_scan.json').read_text())['classes'] if c['class_index']==5)
    full,F,T,b,lifted,dirs,cuts=formula(C,S,row)
    source_assertions=list(z3.parse_smt2_file(str(source_smt)))
    compare(full,source_assertions)
    # Rebuild the fifteen directional LOWER-width formulas explicitly.
    width_forms={}
    for u in dirs:
        width_forms[tuple(u)]=z3.Or(*[sign*sum(rat(u[k])*(T[i][k]-T[j][k]) for k in range(3))>rat(TARGET)*b
                                     for i,j in combinations(range(4),2) for sign in (-1,1)])
    known={canonical(z3.simplify(e)) for e in width_forms.values()}
    need(len(known)==15,'fifteen distinct complete-width clauses')
    fixed=[e for e in full if canonical(z3.simplify(e)) not in known]
    expected=fixed+[width_forms[u] for u in KEEP]
    record=next(r for r in archive['queries'] if r['name']=='contact_width_two')
    need(record['additional_width_directions']==[list(u) for u in KEEP] and record['retained_Y_U_targets'],'archived width selection')
    core_path=ROOT/record['path']
    need(sha(core_path)==record['input_sha256'],'reduced input binding')
    core=list(z3.parse_smt2_file(str(core_path)))
    need(len(core)==record['assertion_count']==589,'589 archived assertions')
    compare(expected,core)
    need(forms(core)<=forms(source_assertions),'exact normalized formula subset of full transfer')
    removed=forms(source_assertions)-forms(core)
    expected_removed=known-{canonical(z3.simplify(width_forms[u])) for u in KEEP}
    need(removed==expected_removed and len(removed)==12,'only twelve lower-width clauses removed')
    # Confirm preservation of the constraints forcing the other two widths.
    D=sum(rat((1,-1,-2)[k])*(T[3][k]-T[0][k]) for k in range(3))
    core_forms=forms(core)
    need(canonical(z3.simplify(b<rat(1/TARGET))) in core_forms,'Y width forced by normalized span and reciprocal gap')
    need(canonical(z3.simplify(D>rat(TARGET)*b)) in core_forms,'U width forced by actual selected span')
    five={*KEEP,(0,1,0),(1,-1,-2)}
    contact_small={tuple(u) for u in dirs if max(sum(u[k]*p[k] for k in range(3)) for p in C['contact_points'])-
                   min(sum(u[k]*p[k] for k in range(3)) for p in C['contact_points'])<=2}
    need(five==contact_small and len(five)==5,'precisely five contact-width-at-most-two directions')
    # Bind existing proof evidence without rerunning either cvc5 or Ethos.
    need(record['status']=='unsat' and record['internal_proof_check'] and record['check_proofs_complete'],'complete cvc5 proof record')
    need(not any('TRUST' in k or 'SORRY' in k for k in record['proof_rules']),'no recorded admitted proof rule')
    proof_path=ROOT/record['proof_path']
    proof=gzip.decompress(proof_path.read_bytes())
    proof_hash=hashlib.sha256(proof).hexdigest()
    need(proof_hash==record['proof_sha256'],'CPC payload binding')
    ethos_path=ROOT/'results/det5_scaled_width_core_ethos_validation.json'
    ethos=json.loads(ethos_path.read_text())
    need(ethos['status']=='PASS' and ethos['archive_sha256']==sha(archive_path),'external receipt and archive binding')
    need(ethos['input_sha256']==sha(core_path) and ethos['proof_sha256']==proof_hash and
         ethos['compressed_proof_sha256']==sha(proof_path),'external input/proof binding')
    need(ethos['external_check']['exit_code']==0 and ethos['external_check']['stdout']=='correct' and
         not ethos['external_check']['stderr'],'recorded successful external check')
    need(ethos['unreferenced_assumption_rejected'] and ethos['missing_refutation_rejected'],'external negative controls recorded')
    bad=deepcopy(row);bad['box'][0]=['0','1']
    rejected(lambda:bind_leaf(bad,source),'changed continuous box')
    first_width=canonical(z3.simplify(width_forms[KEEP[0]]))
    dropped=[e for e in core if canonical(z3.simplify(e))!=first_width]
    rejected(lambda:compare(expected,dropped),'omitted Z-width clause')
    first_volume=canonical(z3.simplify(cuts['barycentric_volume'][0]))
    need(first_volume in core_forms and first_volume is not True,'nontrivial retained volume atom')
    dropped=[e for e in core if canonical(z3.simplify(e))!=first_volume]
    rejected(lambda:compare(expected,dropped),'omitted non-width volume cut')
    result={'status':'PASS','scope':'Standalone continuous-box exclusion encoding with five lower-width directions and globally necessary gauge/volume cuts; not a class exclusion or a theorem from five widths alone.',
            'Y_extrema':row['Y_extrema'],'U_extrema':row['U_extrema'],'box':BOX,
            'source_input_sha256':sha(source_smt),'reduced_input_sha256':sha(core_path),
            'assertion_count':len(core),'removed_lower_width_clauses':12,
            'five_lower_width_directions':sorted(five),'retained_all_other_assertions':True,
            'cvc5_proof_nodes':record['proof_nodes'],'proof_sha256':proof_hash,'proof_bytes':len(proof),
            'ethos_receipt_sha256':sha(ethos_path),'recorded_external_check':'PASS',
            'solver_queries_run':0,'proof_kernel_calls_run':0,'rejected_mutations':3,
            'cover_scope':'This one box does not depend on inherited UNSAT labels. A complete class cover would still require all other boxes and their proof chains.'}
    (ROOT/'results/det5_five_direction_box_encoding_validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
