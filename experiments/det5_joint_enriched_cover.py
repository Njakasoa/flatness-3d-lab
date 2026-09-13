"""Pending-box refinement with the witnessed four-vector gauge orbit."""
import hashlib,json
from experiments import det5_joint_volume_gaps as driver
from experiments.det5_joint_enriched_roots import enriched_make,VECTORS

ARCHIVE=driver.ROOT/'results/det5_joint_enriched_cover.json'


def main():
    raw=driver.SOURCE.read_bytes()
    if not ARCHIVE.exists():
        data=json.loads(raw)
        data['volume_gap_seed']={'path':str(driver.SOURCE.relative_to(driver.ROOT)),
                                'sha256':hashlib.sha256(raw).hexdigest(),'query_count':len(data['queries'])}
        data['linear_volume_gap_cuts']={'Y':str(driver.Y_GAP),'U':str(driver.U_GAP),
                                       'proof':'proofs/DET5_VOLUME_GAP_BOUNDS.md'}
        data['extra_gauge_vectors']=VECTORS
        data['gauge_orbit_proof']='proofs/DET5_RETAINED_TWO_DIRECTION_WITNESS.md'
        ARCHIVE.write_text(json.dumps(data,indent=2)+'\n')
    driver.ARCHIVE=ARCHIVE
    driver.PATH_PREFIX='det5_joint_enriched_gap'
    driver.gap_make=enriched_make
    driver.main()


if __name__=='__main__':main()
