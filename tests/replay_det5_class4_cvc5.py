"""Independent full-matrix cvc5 refutations for the five class-4 root boxes.

Reuses only the independent Fraction/SMT encoder, not discovery experiments.
This certifies the five formulas; geometric necessity is audited separately.
"""
from fractions import Fraction as Q
from pathlib import Path
import gzip, hashlib, json
import cvc5
from replay_height_cover_cvc5 import statement, run, need

ROOT = Path(__file__).resolve().parents[1]


def main():
    data = json.loads((ROOT/'results/det5_height_interval.json').read_text())
    C = next(c for c in json.loads((ROOT/'certificates/nonunimodular_observer_guards.json').read_text())['classes'] if c['class_index']==4)
    S = next(c for c in json.loads((ROOT/'results/two_vector_class_scan.json').read_text())['classes'] if c['class_index']==4)
    need(C['contact_points']==[[0,0,0],[5,1,1],[0,1,0],[0,0,1]], 'correct contact class')
    vectors = sorted(set(map(tuple,C['primitive_contact_edge_directions'])) | {tuple(v['vector']) for v in S['eligible_vectors']})
    expected = {(0,1),(0,2),(0,3),(1,0),(1,3)}
    charts = [c for c in data['charts'] if c['class_index']==4]
    leaves = [q for q in data['queries'] if q['class_index']==4]
    need(len(charts)==len(leaves)==5 and {tuple(c['extrema']) for c in charts}==expected, 'five expected charts')
    need({tuple(q['extrema']) for q in leaves}==expected, 'five unique root queries')
    for c in charts:
        need(c['complete_cover'] and not c['pending_leaves'] and c['closed_leaves']==['r'] and c['queries']==1, 'root closes whole square')
    outdir=ROOT/'certificates/det5_class4_cvc5';outdir.mkdir(exist_ok=True)
    rows=[]
    report={'status':'INCOMPLETE','class_index':4,'contact_points':C['contact_points'],
            'cvc5_version':cvc5.__version__,'independent_full_matrix_encoding':True,
            'gauge_vectors':vectors,'guard_count':len(C['guards']), 'leaves':rows,
            'scope':'Five exact full-square outer-relaxation refutations for class 4 only. The full 12-entry matrix encoding is independent of the discovery experiments. Geometry and height-orbit coverage require their separate audit; class 5 is not included.'}
    output=ROOT/'results/det5_class4_cvc5_validation.json'
    for leaf in leaves:
        need(leaf['node']=='r' and leaf['status']=='unsat' and [[Q(x) for x in r] for r in leaf['box']]==[[Q(0),Q(1)]]*2, 'full unit square root')
        ext=leaf['extrema'];tag=f'4_{ext[0]}_{ext[1]}_r'
        text=statement(C,vectors,ext,[[Q(0),Q(1)]]*2)
        (outdir/(tag+'.smt2')).write_text(text)
        result,proof=run(text)
        result.update(class_index=4,extrema=ext,node='r',box=leaf['box'],covered_area='1',input_sha256=hashlib.sha256(text.encode()).hexdigest())
        if proof is not None:
            need(not any('TRUST' in rule or 'SORRY' in rule for rule in result['proof_rules']), 'no trusted proof rules')
            raw=proof if isinstance(proof,bytes) else proof.encode();packed=gzip.compress(raw,mtime=0)
            (outdir/(tag+'.cpc.gz')).write_bytes(packed)
            result.update(proof_sha256=hashlib.sha256(raw).hexdigest(),compressed_proof_sha256=hashlib.sha256(packed).hexdigest(),proof_bytes=len(raw))
        rows.append(result)
        output.write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps({'leaf':tag,'status':result['status'],'seconds':result['elapsed_seconds']}),flush=True)
        need(result['status']=='unsat', 'independent root did not refute')
    report['status']='PASS';output.write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':main()
