"""One bounded strengthened continuous-height rectangle; immutable archive."""
from pathlib import Path
from fractions import Fraction as Q
import json,hashlib,gzip,sys
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root));sys.path.insert(0,str(root/'tests'))
from replay_height_cover_cvc5 import statement
from experiments.det5_y_corner_gauge_threshold import solve

def main():
    out=root/'results/det5_strong_anchor_rectangle.json'
    if out.exists():raise SystemExit('Recorded rectangle exists; unchanged query skipped')
    C=next(c for c in json.loads((root/'certificates/nonunimodular_observer_guards.json').read_text())['classes']if c['class_index']==5)
    vectors=[(0,0,1),(0,1,-1),(0,1,0),(1,0,0),(1,0,1),(2,0,1),(3,0,1),(5,0,2),(5,1,1),(5,1,2),(1,-1,1)]
    box=[[Q(0),Q(1,256)],[Q(31,256),Q(33,256)]]
    text=statement(C,vectors,[0,3],box).replace('(/ 37 102)','(/ 183 500)')
    text+='(assert (> gap (/ 2042829 50000000)))\n'
    p=root/'results/det5_strong_anchor_rectangle.smt2';p.write_text(text)
    r,proof=solve(text)
    r.update(scope='One continuous height rectangle with strengthened eleven gauges and a true-global-target volume gap necessity. Status alone is not a certificate.',extrema=[0,3],box=[[str(v)for v in row]for row in box],beta='183/500',target='17/5',gap_lower='2042829/50000000',gauge_vectors=vectors,input_path=str(p.relative_to(root)),input_sha256=hashlib.sha256(text.encode()).hexdigest(),solver_queries_run=1)
    if proof:
     raw=proof.encode()if isinstance(proof,str)else proof;p=root/'certificates/det5_strong_anchor_rectangle.cpc.gz';p.write_bytes(gzip.compress(raw,mtime=0));r.update(proof_path=str(p.relative_to(root)),proof_sha256=hashlib.sha256(raw).hexdigest())
    out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k]for k in('status','elapsed_seconds')},indent=2))

if __name__=="__main__":main()
