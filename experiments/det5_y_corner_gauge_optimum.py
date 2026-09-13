"""One bounded optimization of the closed Y-corner outer relaxation.

The closed relaxation is weaker than the actual strict contact model. Reported
optimum is guidance until a separate strict-threshold refutation is checked.
"""
from pathlib import Path
import json,sys,time
import z3
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tests'))
from check_height_ethos import sha
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'results/det5_y_corner_gauge_optimum.json'

def close(e):
 if z3.is_gt(e):return close(e.arg(0))>=close(e.arg(1))
 if z3.is_lt(e):return close(e.arg(0))<=close(e.arg(1))
 if e.num_args()==0:return e
 return e.decl()(*[close(c)for c in e.children()])

def main():
 if OUT.exists():print('Closed optimization archive exists; skipped');return
 p=ROOT/'certificates/det5_class5_y/0_3_r1111.smt2';text=p.read_text();needle='(/ 37 102)';count=text.count(needle)
 if count!=140:raise ValueError('ten gauges with14atoms')
 text=text.replace('(set-logic QF_LRA)','(set-logic QF_LRA)\n(declare-fun gauge_level () Real)').replace(needle,'gauge_level')
 aa=[close(c)for c in z3.parse_smt2_string(text)];g=z3.Real('gauge_level');aa.extend((g>=0,g<=1));s=z3.Optimize();s.set(timeout=15000);s.add(*aa);obj=s.maximize(g)
 path=ROOT/'results/det5_y_corner_closed_optimum.smt2';path.write_text(s.sexpr());start=time.monotonic();st=s.check()
 r={'scope':'One bounded closed-outer-relaxation optimization; rational SAT point checked, no proof of an upper bound independently certified here.','source_path':str(p.relative_to(ROOT)),'source_sha256':sha(p.read_bytes()),'input_path':str(path.relative_to(ROOT)),'input_sha256':sha(path.read_bytes()),'status':str(st),'elapsed_seconds':time.monotonic()-start,'timeout_ms':15000,'z3_version':z3.get_version_string()}
 if st==z3.unknown:r['reason_unknown']=s.reason_unknown()
 if st==z3.sat:
  m=s.model();r['upper']=str(obj.upper());r['lower']=str(obj.lower());r['assignment']={str(v):str(m[v])for v in m};r['gauge_level']=str(m.eval(g));r['all_assertions_true']=all(z3.is_true(z3.simplify(m.eval(c)))for c in aa)
 OUT.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items()if k!='assignment'}))

if __name__=='__main__':main()
