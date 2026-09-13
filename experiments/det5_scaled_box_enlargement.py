"""Bounded larger-box tests around the certified five-width obstruction.

Each new rectangle strictly contains the proved [3/4,1]^2 x [1/2,1]^2
box. Uses five direction tests and unchanged necessary gauge/volume cuts.
"""
from fractions import Fraction as Q
from pathlib import Path
import argparse,gzip,hashlib,json,sys,tempfile
import z3
from experiments.det5_scaled_pending_transfer import strengthened
from experiments.det5_scaled_width_frame import inputs,make,ROOT
sys.path.insert(0,str(ROOT/'tests'))
from check_det5_scaled_leaf_cvc5 import plain,reference
from replay_height_cover_cvc5 import run
from check_height_ethos import need,sha,proof_body,checker,revision,ETHOS_REV,CVC5_REV
ARCHIVE=ROOT/'results/det5_scaled_box_enlargement.json'

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--ethos',type=Path,required=True);ap.add_argument('--ethos-source',type=Path,required=True);ap.add_argument('--cvc5-source',type=Path,required=True);args=ap.parse_args()
 if ARCHIVE.exists():print('Frozen enlargement attempts already exist; skipped');return
 need(revision(args.ethos_source)==ETHOS_REV and revision(args.cvc5_source)==CVC5_REV,'pinned sources')
 C,S=inputs();chart={'Y_extrema':[0,3],'U_extrema':[0,3]};base,*tail=make(C,S,[0,3],relax=True);directions=tail[-1];widths={tuple(u):c for u,c in zip(directions,list(base.assertions())[-15:])};old={c.sexpr()for c in widths.values()};keep=[(0,0,1),(0,1,-1),(1,-2,-2)]
 data={'scope':'Independent enlarged continuous-box tests with five widths and global-target gauge/volume necessities. No class exclusion.','queries':[]}
 for tag,yl,ul in [('half_half',Q(1,2),Q(1,2)),('three_quarters_zero',Q(3,4),Q(0)),('zero_half',Q(0),Q(1,2))]:
  box=[[str(yl),'1']]*2+[[str(ul),'1']]*2;s,*_=strengthened(C,S,chart,{'box':box})
  aa=[z3.simplify(c)for c in list(s.assertions())if c.sexpr()not in old]+[z3.simplify(widths[u])for u in keep];aa=[c for c in aa if not z3.is_true(c)];vs=set()
  def visit(e):
   if z3.is_const(e)and e.decl().kind()==z3.Z3_OP_UNINTERPRETED:vs.add(str(e))
   for x in e.children():visit(x)
  for c in aa:visit(c)
  text='(set-logic QF_LRA)\n'+''.join(f'(declare-fun {v} () Real)\n'for v in sorted(vs))+''.join('(assert '+plain(c)+')\n'for c in aa)
  path=ROOT/f'results/det5_scaled_enlarged_{tag}.smt2';path.write_text(text);r,pr=run(text);r.update(tag=tag,**chart,box=box,path=str(path.relative_to(ROOT)),input_sha256=sha(text.encode()),additional_width_directions=keep,retained_Y_U_targets=True)
  if pr:
   raw=pr.encode()if isinstance(pr,str)else pr;packed=gzip.compress(raw,mtime=0);p=ROOT/f'certificates/det5_scaled_enlarged_{tag}.cpc.gz';p.write_bytes(packed);r.update(proof_path=str(p.relative_to(ROOT)),proof_sha256=sha(raw),compressed_proof_sha256=sha(packed))
   ref,variables=reference(text);body,counts=proof_body(raw,variables)
   with tempfile.TemporaryDirectory(prefix='det5-enlarged-')as tmp:
    p=Path(tmp)/'proof.cpc';q=Path(tmp)/'reference.smt2';p.write_text(body);q.write_text(ref);e=checker(args.ethos,args.cvc5_source,p,q)
    need(e['exit_code']==0 and e['stdout']=='correct'and not e['stderr'],'external proof check');r['ethos']=e;r['reference_sha256']=sha(ref.encode());r['ethos_revision']=ETHOS_REV;r['cvc5_signature_revision']=CVC5_REV
  data['queries'].append(r);ARCHIVE.write_text(json.dumps(data,indent=2)+'\n');print(json.dumps({k:r[k]for k in('tag','status','elapsed_seconds')}),flush=True)

if __name__=='__main__':main()
