"""Certify the twelve old class5 Y-only closed rectangles independently.

No discovery node is rerun. This first independent full-matrix cvc5 proof
campaign upgrades archived Z3 labels and externally checks every CPC proof.
It is a partial Y-domain collection, not a class exclusion.
"""
from pathlib import Path
from fractions import Fraction as Q
import argparse,gzip,json,tempfile
from replay_height_cover_cvc5 import statement,run
from check_height_ethos import need,sha,real_reference,proof_body,checker,revision,ETHOS_REV,CVC5_REV
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results/det5_class5_y_cvc5_validation.json'

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--ethos',type=Path,required=True);ap.add_argument('--ethos-source',type=Path,required=True);ap.add_argument('--cvc5-source',type=Path,required=True);a=ap.parse_args()
 need(revision(a.ethos_source)==ETHOS_REV and revision(a.cvc5_source)==CVC5_REV,'pinned sources')
 source=ROOT/'results/det5_height_interval.json';data=json.loads(source.read_text());C=next(c for c in json.loads((ROOT/'certificates/nonunimodular_observer_guards.json').read_text())['classes']if c['class_index']==5);S=next(c for c in json.loads((ROOT/'results/two_vector_class_scan.json').read_text())['classes']if c['class_index']==5)
 vectors=sorted(set(map(tuple,C['primitive_contact_edge_directions']))|{tuple(r['vector'])for r in S['eligible_vectors']})
 leaves=[]
 for chart in data['charts']:
  if chart['class_index']!=5:continue
  for tag in chart['closed_leaves']:
   row=next(r for r in data['queries']if r['class_index']==5 and r['extrema']==chart['extrema']and r['node']==tag);need(row['status']=='unsat','old closed label');leaves.append(row)
 need(len(leaves)==12,'twelve archived rectangles')
 report=json.loads(OUT.read_text())if OUT.exists()else{'status':'INCOMPLETE','scope':'First independent proof certification of12oldY-only rectangles. Partial domain only; no full class exclusion.','source_path':str(source.relative_to(ROOT)),'source_sha256':sha(source.read_bytes()),'class_index':5,'target':'17/5','beta':'37/102','gauge_vectors':vectors,'ethos_revision':ETHOS_REV,'cvc5_signature_revision':CVC5_REV,'leaves':[]}
 need(report['source_sha256']==sha(source.read_bytes()),'immutable source');done={(tuple(r['extrema']),r['node'])for r in report['leaves']};outdir=ROOT/'certificates/det5_class5_y';outdir.mkdir(exist_ok=True)
 for leaf in leaves:
  ext=leaf['extrema'];tag=leaf['node']
  if(tuple(ext),tag)in done:continue
  text=statement(C,vectors,ext,[[Q(x)for x in pair]for pair in leaf['box']]);base=outdir/f'{ext[0]}_{ext[1]}_{tag}';base.with_suffix('.smt2').write_text(text)
  r,proof=run(text);r.update(extrema=ext,node=tag,box=leaf['box'],source_input_path=leaf['path'],source_input_sha256=sha((ROOT/leaf['path']).read_bytes()),input_path=str(base.with_suffix('.smt2').relative_to(ROOT)),input_sha256=sha(text.encode()))
  if proof:
   raw=proof.encode()if isinstance(proof,str)else proof;packed=gzip.compress(raw,mtime=0);p=base.with_suffix('.cpc.gz');p.write_bytes(packed);r.update(proof_path=str(p.relative_to(ROOT)),proof_sha256=sha(raw),compressed_proof_sha256=sha(packed))
   need(not any('TRUST'in k or'SORRY'in k for k in r['proof_rules']),'no admitted rule')
   ref,_,vs=real_reference(text);body,_=proof_body(raw,vs)
   with tempfile.TemporaryDirectory(prefix='det5-old-y-')as tmp:
    p=Path(tmp)/'proof.cpc';q=Path(tmp)/'reference.smt2';p.write_text(body);q.write_text(ref);e=checker(a.ethos,a.cvc5_source,p,q);r['ethos']=e
    need(e['exit_code']==0 and e['stdout']=='correct'and not e['stderr'],'external check');r['reference_sha256']=sha(ref.encode())
    if not any('negative_control'in rr for rr in report['leaves']):
     p.write_text(body+'\n(assume @fresh_unrelated false)\n');bad=checker(a.ethos,a.cvc5_source,p,q);need(bad['exit_code']!=0 and'assumption'in(bad['stdout']+bad['stderr']).lower(),'fresh assumption rejected');r['negative_control']='unreferenced assumption rejected'
  report['leaves'].append(r);OUT.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'Y':ext,'node':tag,'cvc5':r['status'],'ethos':r.get('ethos',{}).get('stdout')}),flush=True)
 report['status']='PASS'if len(report['leaves'])==12 and all(r.get('ethos',{}).get('stdout')=='correct'for r in report['leaves'])else'INCOMPLETE';OUT.write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
