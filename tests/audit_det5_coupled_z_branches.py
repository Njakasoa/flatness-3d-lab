"""Independent exact branch-input and exhaustive-extrema cover audit.

Imports no discovery code and makes no solver query. UNKNOWN stays unresolved.
"""
from collections import Counter
from itertools import permutations
from pathlib import Path
from fractions import Fraction as Q
import hashlib,json
import z3
from audit_det5_scaled_frame_independent import canonical
ROOT=Path(__file__).resolve().parents[1]
def need(c,m):
 if not c:raise ValueError(m)
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def normalize(aa):return Counter(canonical(z3.simplify(a))for a in aa)
def main():
 path='results/det5_coupled_z_extrema.json';d=json.loads((ROOT/path).read_text());need(sha(d['source_path'])==d['source_sha256'],'parent input binding')
 parent=json.loads((ROOT/'results/det5_coupled_scaled_frame.json').read_text());need(sha('results/det5_coupled_scaled_frame.json')==d['source_archive_sha256'],'parent archive frozen')
 matches=[r for r in parent['queries']if r['path']==d['source_path']];need(len(matches)==1,'unique parent')
 original=matches[0]
 for key in ['Y_extrema','U_extrema','box','node']:need(original[key]==d[key],'parent '+key)
 base=list(z3.parse_smt2_file(str(ROOT/d['source_path'])));L=d['Y_extrema'][0]
 heights=[z3.RealVal(0)if i==L else z3.Real(f't{i}_2')for i in range(4)];b=z3.Real('scaled_b');seen=set();rows=[]
 for r in d['queries']:
  low,high=r['Z_extrema'];need((low,high)in set(permutations(range(4),2))and(low,high)not in seen,'distinct valid extrema pair');seen.add((low,high))
  added=[v-heights[low]>=0 for v in heights]+[heights[high]-v>=0 for v in heights]+[heights[high]-heights[low]>z3.RealVal('17/5')*b]
  # Simplify both additions in their original ordering form; common base is exact AST.
  expected=base+[v>=heights[low]for v in heights]+[v<=heights[high]for v in heights]+[heights[high]-heights[low]>z3.RealVal('17/5')*b]
  need(sha(r['path'])==r['input_sha256'],'branch bytes');actual=list(z3.parse_smt2_file(str(ROOT/r['path'])))
  need(normalize(actual)==normalize(expected),'same full parent plus nine exact Z assertions')
  rows.append({'Z_extrema':r['Z_extrema'],'status':r['status'],'assertions':len(actual),'input_sha256':r['input_sha256']})
 need(seen==set(permutations(range(4),2)),'all twelve ordered pairs')
 # A full-dimensional body has strictly positive Z span. Its minimum and
 # maximum are attained at distinct indices; non-strict ordering includes ties.
 # This proves union coverage without a numerical enumeration of height values.
 sample=expected.copy();sample[-1]=heights[high]-heights[low]>=z3.RealVal('17/5')*b
 need(normalize(sample)!=normalize(expected),'strict width endpoint mutation rejected')
 report={'status':'PASS','scope':'All twelve Z branches reproduce their inherited coupled input plus exact extrema restrictions. Continuous cover follows from attained positive Z span; no UNKNOWN/UNSAT status is certified by this audit.','source_archive_sha256':sha(path),'queries':rows,'exact_ordered_pairs':12,'strict_endpoint_control':True,'solver_queries_run':0,'proof_kernel_calls_run':0}
 (ROOT/'results/det5_coupled_z_encoding_validation.json').write_text(json.dumps(report,indent=2)+'\n');print('COUPLED_Z_BRANCH_INPUTS=PASS')
if __name__=='__main__':main()
