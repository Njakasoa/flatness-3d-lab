"""Second bounded joint-height continuation, preserving the 514-node archive."""
import hashlib,json
from experiments import det5_joint_height_interval as driver

SOURCE=driver.ROOT/'results/det5_joint_continuation.json'
ARCHIVE=driver.ROOT/'results/det5_joint_round2.json'


def main():
    raw=SOURCE.read_bytes();digest=hashlib.sha256(raw).hexdigest()
    if not ARCHIVE.exists():
        data=json.loads(raw)
        data['round2_seed']={'path':str(SOURCE.relative_to(driver.ROOT)),
                             'sha256':digest,'query_count':len(data['queries'])}
        ARCHIVE.write_text(json.dumps(data,indent=2)+'\n')
    else:
        if json.loads(ARCHIVE.read_text())['round2_seed']['sha256']!=digest:
            raise ValueError('Frozen round-one archive changed')
    driver.ARCHIVE=ARCHIVE
    try:driver.main()
    finally:
        if SOURCE.read_bytes()!=raw:raise ValueError('Prior archive changed')


if __name__=='__main__':main()
