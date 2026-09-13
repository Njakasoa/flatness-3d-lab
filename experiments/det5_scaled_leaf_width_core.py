"""Test weaker, interpretable width subsets on the newly UNSAT pending leaf.

Every query removes full-width assertions, preserving all other necessary
cuts. Independent cvc5 proof production is attempted once per new formula.
"""
from pathlib import Path
import sys,json,hashlib,gzip
import z3
from experiments.det5_scaled_pending_transfer import strengthened
from experiments.det5_scaled_width_frame import inputs,make,ROOT
sys.path.insert(0,str(ROOT/'tests'))
from check_det5_scaled_leaf_cvc5 import plain
from replay_height_cover_cvc5 import run
ARCHIVE=ROOT/'results/det5_scaled_leaf_width_core.json'

def main():
 if ARCHIVE.exists():print('Frozen width-subset attempts already exist; skipped');return
 data=json.loads((ROOT/'results/det5_scaled_pending_transfer.json').read_text());row=next(r for r in data['queries']if r['status']=='unsat');C,S=inputs();chart={'Y_extrema':row['Y_extrema'],'U_extrema':row['U_extrema']};leaf={'node':row['node'],'box':row['box']}
 solver,*_=strengthened(C,S,chart,leaf);base,*tail=make(C,S,chart['Y_extrema'],relax=True);dirs=tail[-1]
 widths={tuple(u):c for u,c in zip(dirs,list(base.assertions())[-15:])};known={c.sexpr()for c in widths.values()}
 fixed=[c for c in solver.assertions()if c.sexpr()not in known]
 out={'scope':'Weaker width-subset formulas on one pending box. Neither a complete class cover nor a claim that these direction sets suffice globally.','source_path':row['path'],'source_sha256':row['input_sha256'],'queries':[]}
 for name,keep in [('Z_only',[(0,0,1)]),('contact_width_two',[(0,0,1),(0,1,-1),(1,-2,-2)])]:
  # Y and U targets are already forced by b and the selected extrema/span.
  aa=[z3.simplify(c)for c in fixed+[widths[u]for u in keep]];aa=[c for c in aa if not z3.is_true(c)];vs=set()
  def visit(e):
   if z3.is_const(e)and e.decl().kind()==z3.Z3_OP_UNINTERPRETED:vs.add(str(e))
   for x in e.children():visit(x)
  for c in aa:visit(c)
  text='(set-logic QF_LRA)\n'+''.join(f'(declare-fun {v} () Real)\n'for v in sorted(vs))+''.join('(assert '+plain(c)+')\n'for c in aa)
  path=ROOT/f'results/det5_scaled_leaf_{name}.smt2';path.write_text(text);r,proof=run(text);r.update(name=name,additional_width_directions=keep,retained_Y_U_targets=True,path=str(path.relative_to(ROOT)),input_sha256=hashlib.sha256(text.encode()).hexdigest(),assertion_count=len(aa))
  if proof:
   raw=proof.encode()if isinstance(proof,str)else proof;p=ROOT/f'certificates/det5_scaled_leaf_{name}.cpc.gz';p.write_bytes(gzip.compress(raw,mtime=0));r['proof_path']=str(p.relative_to(ROOT));r['proof_sha256']=hashlib.sha256(raw).hexdigest()
  out['queries'].append(r);ARCHIVE.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:r[k]for k in('name','status','elapsed_seconds')}),flush=True)

if __name__=='__main__':main()
