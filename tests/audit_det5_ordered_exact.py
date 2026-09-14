"""Independent reconstruction of the two exact-product ordered formulations."""
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
import hashlib,json
import z3
from audit_det5_scaled_frame_independent import canonical
ROOT=Path(__file__).resolve().parents[1]
def need(c,m):
 if not c:raise ValueError(m)
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def forms(a):return Counter(canonical(z3.simplify(e))for e in a)
def main():
 p='results/det5_y_ordered_exact.json';d=json.loads((ROOT/p).read_text());need(sha(d['source_archive_path'])==d['source_archive_sha256'],'frozen parent archive')
 prior=json.loads((ROOT/d['source_archive_path']).read_text());byorder={r['order']:r for r in prior['queries']};rows=[]
 need({r['order']for r in d['queries']}=={'lt','gt'}and len(d['queries'])==2,'both strict orders')
 for r in d['queries']:
  old=byorder[r['order']];need(r['source_path']==old['input_path']and r['source_sha256']==old['input_sha256']==sha(r['source_path']),'parent input binding')
  source=list(z3.parse_smt2_file(str(ROOT/r['source_path'])));equations=[]
  for i in(1,2):
   for j in range(4):
    if i!=j:equations.append(z3.Real(f'product_{i}_{j}')-z3.Real(f'F_{i}_{j}')*z3.Real(f'q_{i}')==0)
  need(sha(r['input_path'])==r['input_sha256'],'new input hash');actual=list(z3.parse_smt2_file(str(ROOT/r['input_path'])))
  expected=source+equations;need(forms(actual)==forms(expected),'same necessary formula plus six exact products')
  need(forms(actual)!=forms(expected[:-1]),'missing exact product rejected')
  rows.append({'order':r['order'],'status':r['status'],'assertions':len(actual),'exact_products':6,'input_sha256':r['input_sha256']})
 out={'status':'PASS','scope':'Exact polynomial input and inherited-source audit only; nonlinear UNKNOWN remains unresolved. Completeness of two orders follows from the independently proved strict contact-ordering lemma.','source_archive_sha256':sha(p),'queries':rows,'missing_product_control':True,'solver_queries_run':0,'proof_kernel_calls_run':0}
 (ROOT/'results/det5_ordered_exact_encoding_validation.json').write_text(json.dumps(out,indent=2)+'\n');print('ORDERED_EXACT_INPUTS=PASS')
if __name__=='__main__':main()
