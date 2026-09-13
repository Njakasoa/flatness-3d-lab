"""Enforce all 18 primitive contact gauges of intrinsic mass at most6/5.

Continues the14-gauge archive with a genuinely stronger model. Previous
SAT body is removed from the stop marker because new cuts exclude it.
"""
import hashlib,json
import z3
from experiments import det5_joint_volume_gaps as driver
from experiments.det5_joint_enriched_roots import enriched_make,VECTORS
from experiments.contact_contraction_trace_probe import ell

NEW=[(1,1,0),(2,1,0),(3,1,1),(4,1,1)]
SOURCE=driver.ROOT/'results/det5_joint_enriched_cover.json'
ARCHIVE=driver.ROOT/'results/det5_joint_short_gauges.json'


def make(C,S,ye,ue,box):
    values=enriched_make(C,S,ye,ue,box);solver,F=values[:2]
    for v in NEW:
        l=ell(v,5,2);z=[sum(F[i][j]*z3.RealVal(str(l[j])) for j in range(4)) for i in range(4)]
        solver.add(z3.Or(*[sum(z[i] for i in range(4) if mask&(1<<i))>z3.RealVal('183/500') for mask in range(1,15)]))
    return values


def main():
    raw=SOURCE.read_bytes()
    if not ARCHIVE.exists():
        data=json.loads(raw);data.pop('retained_witness',None)
        data['volume_gap_seed']={'path':str(SOURCE.relative_to(driver.ROOT)),
                                'sha256':hashlib.sha256(raw).hexdigest(),'query_count':len(data['queries'])}
        data['extra_gauge_vectors']=sorted(VECTORS+NEW)
        data['intrinsic_gauge_cutoff']='6/5';data['total_gauge_count']=18
        ARCHIVE.write_text(json.dumps(data,indent=2)+'\n')
    driver.SOURCE=SOURCE;driver.ARCHIVE=ARCHIVE
    driver.PATH_PREFIX='det5_joint_short_gauges'
    driver.gap_make=make
    driver.main()


if __name__=='__main__':main()
