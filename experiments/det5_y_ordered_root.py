"""Two exact-height-order branches in the whole remaining Y[0,3] chart.

A new analytic contact identity forbids q1=q2 and fixes the Z gauge signs.
These are necessary cuts for actual bodies, not consequences assumed for
arbitrary old McCormick assignments. Old checked Y regions are subtracted.
"""
from pathlib import Path
from fractions import Fraction as Q
import sys,json,gzip,tempfile,argparse
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tests'))
from replay_height_cover_cvc5 import statement
from experiments.det5_y_corner_gauge_threshold import solve
from check_height_ethos import need,sha,sexps,emit,real_reference,proof_body,checker,revision,ETHOS_REV,CVC5_REV
OUT=ROOT/'results/det5_y_ordered_root.json'

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--offset-order',action='store_true');ap.add_argument('--difference-products',action='store_true');a=ap.parse_args();need(not a.difference_products or a.offset_order,'difference-products requires offset-order');suffix='_difference'if a.difference_products else'_offset'if a.offset_order else'';out=ROOT/f'results/det5_y_ordered_root{suffix}.json'
 if out.exists():print('Ordered-root archive exists; unchanged queries skipped');return
 C=next(c for c in json.loads((ROOT/'certificates/nonunimodular_observer_guards.json').read_text())['classes']if c['class_index']==5);S=next(c for c in json.loads((ROOT/'results/two_vector_class_scan.json').read_text())['classes']if c['class_index']==5)
 vectors=sorted(set(map(tuple,C['primitive_contact_edge_directions']))|{tuple(r['vector'])for r in S['eligible_vectors']})
 # Omitting Z from the generic disjunctions replaces it with its exact linear
 # formula after the selected strict ordering. All other gauges remain.
 other=[v for v in vectors if v!=(0,0,1)]
 base=statement(C,other,[0,3],[[Q(0),Q(1)]]*2)
 oldp=ROOT/'results/det5_class5_y_cvc5_validation.json';newp=ROOT/'results/det5_y_corner_enlarged_3_5.json';old=json.loads(oldp.read_text());new=json.loads(newp.read_text());need(old['status']=='PASS'and new['ethos']['stdout']=='correct','certified region receipts')
 rectangles=[r['box']for r in old['leaves']if r['extrema']==[0,3]]+[new['box']]
 def rat(q):
  q=Q(q);return str(q.numerator)if q.denominator==1 else f'(/ {q.numerator} {q.denominator})'
 for box in rectangles:
  base+='(assert (or '+' '.join(atom for i,(lo,hi)in zip((1,2),box)for atom in(f'(< q_{i} {rat(lo)})',f'(> q_{i} {rat(hi)})'))+'))\n'
 result={'scope':'Two exhaustive actual-height order branches in Y[0,3], using the analytic fixed Z signs and exact complements of certified Y regions. SAT is only outer feasibility; status alone cannot close a chart.','extrema':[0,3],'box':[['0','1']]*2,'beta':'37/102','target':'17/5','old_Y_proof_receipt_sha256':sha(oldp.read_bytes()),'enlarged_proof_receipt_sha256':sha(newp.read_bytes()),'excluded_Y_rectangles':rectangles,'offset_order':a.offset_order,'difference_products':a.difference_products,'queries':[]}
 for order in ['lt','gt']:
  op='<'if order=='lt'else'>';positive=(2,1)if order=='lt'else(1,2);pos,neg=positive
  cuts=f'(assert ({op} q_1 q_2))\n(assert (> F_{pos}_3 F_{pos}_0))\n(assert (< F_{neg}_3 F_{neg}_0))\n(assert (> (+ F_0_3 F_{pos}_3 (- F_{pos}_0)) (/ 37 102)))\n'
  if a.offset_order:
   cuts+=f'(assert (< q_{neg} offset))\n(assert (< offset q_{pos}))\n'
  if a.difference_products:
   for i,(lo,hi)in ((pos,(0,1)),(neg,(-1,0))):
    z=f'(- F_{i}_3 F_{i}_0)';r=f'(- product_{i}_3 product_{i}_0)';q=f'q_{i}'
    cuts+=f'(assert (>= {r} (* {lo} {q})))\n(assert (>= {r} (+ (* {hi} {q}) {z} (- {hi}))))\n(assert (<= {r} (+ (* {lo} {q}) {z} (- {lo}))))\n(assert (<= {r} (* {hi} {q})))\n'
  text=base+cuts;p=ROOT/f'results/det5_y_ordered_root{suffix}_{order}.smt2';p.write_text(text);r,proof=solve(text);r.update(order=order,input_path=str(p.relative_to(ROOT)),input_sha256=sha(text.encode()))
  if proof:
   raw=proof.encode()if isinstance(proof,str)else proof;packed=gzip.compress(raw,mtime=0);p=ROOT/f'certificates/det5_y_ordered_root{suffix}_{order}.cpc.gz';p.write_bytes(packed);ref,_,vs=real_reference(text);body,_=proof_body(raw,vs);ethos=Path('/tmp/flatness-ethos/build/src/ethos');es=Path('/tmp/flatness-ethos');cs=Path('/tmp/flatness-cvc5-signatures');need(revision(es)==ETHOS_REV and revision(cs)==CVC5_REV,'pinned checker')
   with tempfile.TemporaryDirectory(prefix='det5-order-')as tmp:
    pp=Path(tmp)/'proof.cpc';rr=Path(tmp)/'reference.smt2';pp.write_text(body);rr.write_text(ref);e=checker(ethos,cs,pp,rr);need(e['exit_code']==0 and e['stdout']=='correct'and not e['stderr'],'external refutation')
   r.update(proof_path=str(p.relative_to(ROOT)),proof_sha256=sha(raw),compressed_proof_sha256=sha(packed),reference_sha256=sha(ref.encode()),ethos=e,ethos_revision=ETHOS_REV,cvc5_signature_revision=CVC5_REV)
  result['queries'].append(r);out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:r[k]for k in('order','status','elapsed_seconds')}),flush=True)

if __name__=='__main__':main()
