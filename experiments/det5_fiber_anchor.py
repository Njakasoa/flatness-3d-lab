"""One rational-height LRA anchor for the new fiber compiler; archived once."""
from pathlib import Path
import hashlib,json,sys
import z3
from experiments.det5_quadratic_height_chart import problem
from experiments.det5_horizontal_fiber_oracle import statement

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tests'))
from experiments.det5_y_corner_gauge_threshold import solve


def main():
    out=ROOT/'results/det5_fiber_anchor.json'
    if out.exists():
        print('Anchor archive exists; unchanged query skipped');return
    values,F,q,a,b,constraints,vectors,boxes=problem('lt','183/500',[(1,-1,1)])
    fixed=[(values[0],z3.RealVal(0)),(values[1],z3.RealVal('1/8'))]
    rows=[z3.simplify(z3.substitute(row,*fixed)) for row in constraints]
    text=statement(rows);path=ROOT/'results/det5_fiber_anchor.smt2';path.write_text(text)
    result,proof=solve(text)
    result.update(scope='One exact fixed-height anchor with strong eleven gauges; no full-width conclusion.',
                  fixed_heights=['0','1/8'],order='lt',beta='183/500',target='17/5',
                  input_path=str(path.relative_to(ROOT)),input_sha256=hashlib.sha256(text.encode()).hexdigest(),
                  gauge_vectors=vectors,excluded_rectangles=boxes,solver_queries_run=1)
    if proof:
        # Preserve the proof for independent checking; status alone closes no family.
        import gzip
        raw=proof.encode() if isinstance(proof,str) else proof
        p=ROOT/'certificates/det5_fiber_anchor.cpc.gz';p.write_bytes(gzip.compress(raw,mtime=0))
        result.update(proof_path=str(p.relative_to(ROOT)),proof_sha256=hashlib.sha256(raw).hexdigest())
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','elapsed_seconds')},indent=2))


if __name__=='__main__':main()
