"""Bounded weaker-gauge probes for the certified upper Y corner.

At most three new threshold formulas; skip thresholds dominated by a proof.
Every UNSAT proof is checked externally, every SAT saves rational values.
"""
from pathlib import Path
from fractions import Fraction as Q
import sys,json,gzip,time,argparse,tempfile
import cvc5
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tests'))
from replay_height_cover_cvc5 import statement,rat
from check_height_ethos import need,sha,real_reference,proof_body,checker,revision,ETHOS_REV,CVC5_REV
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'results/det5_y_corner_gauge_threshold.json'

def solve(text):
 s=cvc5.Solver();s.setOption('produce-proofs','true');s.setOption('check-proofs','true');s.setOption('check-proofs-complete','true');s.setOption('produce-models','true');s.setOption('tlimit-per','10000')
 p=cvc5.InputParser(s);p.setStringInput(cvc5.InputLanguage.SMT_LIB_2_6,text,'new-Y-corner-threshold');sm=p.getSymbolManager()
 while True:
  c=p.nextCommand()
  if c.isNull():break
  c.invoke(s,sm)
 start=time.monotonic();st=s.checkSat();r={'status':str(st),'elapsed_seconds':time.monotonic()-start};proof=None
 if st.isUnsat():
  ps=s.getProof();need(len(ps)==1,'single proof');proof=s.proofToString(ps[0],cvc5.ProofFormat.CPC);r['internal_complete_proof_check']=True
 elif st.isSat():r['assignment']={str(t):str(s.getValue(t))for t in sm.getDeclaredTerms()}
 return r,proof

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--ethos',type=Path,required=True);ap.add_argument('--ethos-source',type=Path,required=True);ap.add_argument('--cvc5-source',type=Path,required=True);ap.add_argument('--betas',default='1/3,7/20,9/25');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args()
 out=a.output;betas=[Q(x)for x in a.betas.split(',')];need(all(0<x<1 for x in betas)and betas==sorted(set(betas)),'increasing distinct thresholds')
 if out.exists():print('Archived threshold probes exist; skipped');return
 need(revision(a.ethos_source)==ETHOS_REV and revision(a.cvc5_source)==CVC5_REV,'pinned sources')
 C=next(c for c in json.loads((ROOT/'certificates/nonunimodular_observer_guards.json').read_text())['classes']if c['class_index']==5);S=next(c for c in json.loads((ROOT/'results/two_vector_class_scan.json').read_text())['classes']if c['class_index']==5)
 vectors=sorted(set(map(tuple,C['primitive_contact_edge_directions']))|{tuple(r['vector'])for r in S['eligible_vectors']});base=statement(C,vectors,[0,3],[[Q(3,4),Q(1)]]*2)
 need(base.count('(/ 37 102)')==14*len(vectors),'only intended gauge atoms replaced')
 report={'scope':'Weaker uniform gauge thresholds on one Y-only corner. Conditional gauge/width bounds require the geometric proof; SAT is only an outer solution.','extrema':[0,3],'box':[['3/4','1']]*2,'gauge_vectors':vectors,'queries':[]}
 for beta in betas:
  text=base.replace('(/ 37 102)',rat(beta));tag=f'{beta.numerator}_{beta.denominator}';path=ROOT/f'results/det5_y_corner_beta_{tag}.smt2';path.write_text(text);r,proof=solve(text);r.update(beta=str(beta),input_path=str(path.relative_to(ROOT)),input_sha256=sha(text.encode()))
  if proof:
   raw=proof.encode()if isinstance(proof,str)else proof;packed=gzip.compress(raw,mtime=0);dest=ROOT/f'certificates/det5_y_corner_beta_{tag}.cpc.gz';dest.write_bytes(packed);ref,_,vs=real_reference(text);body,_=proof_body(raw,vs)
   with tempfile.TemporaryDirectory(prefix='det5-corner-beta-')as tmp:
    p=Path(tmp)/'proof.cpc';q=Path(tmp)/'reference.smt2';p.write_text(body);q.write_text(ref);e=checker(a.ethos,a.cvc5_source,p,q);need(e['exit_code']==0 and e['stdout']=='correct'and not e['stderr'],'external proof check')
   r.update(proof_path=str(dest.relative_to(ROOT)),proof_sha256=sha(raw),compressed_proof_sha256=sha(packed),reference_sha256=sha(ref.encode()),ethos=e,ethos_revision=ETHOS_REV,cvc5_signature_revision=CVC5_REV)
  report['queries'].append(r);out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:r[k]for k in('beta','status','elapsed_seconds')}),flush=True)
  if r['status']=='unsat':break

if __name__=='__main__':main()
