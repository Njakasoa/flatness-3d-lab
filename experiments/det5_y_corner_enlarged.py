"""One new Y-only square extending beyond the twelve old certified rectangles."""
from fractions import Fraction as Q
from pathlib import Path
import sys,json,gzip,tempfile,argparse
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tests'))
from replay_height_cover_cvc5 import statement
from experiments.det5_y_corner_gauge_threshold import solve
from check_height_ethos import need,sha,real_reference,proof_body,checker,revision,ETHOS_REV,CVC5_REV

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--lower',default='2/3');a=ap.parse_args();lower=Q(a.lower);need(0<lower<1,'normalized lower endpoint');tag='two_thirds'if lower==Q(2,3)else f'{lower.numerator}_{lower.denominator}'
 out=ROOT/('results/det5_y_corner_enlarged.json'if lower==Q(2,3)else f'results/det5_y_corner_enlarged_{tag}.json')
 if out.exists():print('Recorded enlarged-square result exists; skipped');return
 C=next(c for c in json.loads((ROOT/'certificates/nonunimodular_observer_guards.json').read_text())['classes']if c['class_index']==5);S=next(c for c in json.loads((ROOT/'results/two_vector_class_scan.json').read_text())['classes']if c['class_index']==5)
 vectors=sorted(set(map(tuple,C['primitive_contact_edge_directions']))|{tuple(r['vector'])for r in S['eligible_vectors']})
 ext=[0,3];box=[[lower,Q(1)]]*2;text=statement(C,vectors,ext,box);p=ROOT/f'results/det5_y_enlarged_{tag}.smt2';p.write_text(text);r,proof=solve(text)
 r.update(scope='One enlarged Y-only square at the weak necessary global-target gauge. Partial height-domain obstruction only if independently certified; SAT is outer feasibility.',extrema=ext,box=[[str(x)for x in pair]for pair in box],beta='37/102',target='17/5',gauge_vectors=vectors,input_path=str(p.relative_to(ROOT)),input_sha256=sha(text.encode()))
 if proof:
  raw=proof.encode()if isinstance(proof,str)else proof;packed=gzip.compress(raw,mtime=0);p=ROOT/f'certificates/det5_y_enlarged_{tag}.cpc.gz';p.write_bytes(packed);ref,_,vs=real_reference(text);body,_=proof_body(raw,vs)
  ethos=Path('/tmp/flatness-ethos/build/src/ethos');es=Path('/tmp/flatness-ethos');cs=Path('/tmp/flatness-cvc5-signatures');need(revision(es)==ETHOS_REV and revision(cs)==CVC5_REV,'pinned checker')
  with tempfile.TemporaryDirectory(prefix='det5-Y-enlarged-')as tmp:
   pp=Path(tmp)/'proof.cpc';rr=Path(tmp)/'reference.smt2';pp.write_text(body);rr.write_text(ref);check=checker(ethos,cs,pp,rr);need(check['exit_code']==0 and check['stdout']=='correct'and not check['stderr'],'external proof')
  r.update(proof_path=str(p.relative_to(ROOT)),proof_sha256=sha(raw),compressed_proof_sha256=sha(packed),reference_sha256=sha(ref.encode()),ethos=check,ethos_revision=ETHOS_REV,cvc5_signature_revision=CVC5_REV)
 out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k]for k in('status','extrema','box','elapsed_seconds')}))
if __name__=='__main__':main()
