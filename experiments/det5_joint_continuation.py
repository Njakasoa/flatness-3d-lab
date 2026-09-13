"""Continue pending joint boxes while preserving the published seed archive.

The inherited driver visits pending children only. Existing node paths are
retained; all new tags are absent from the seed and are never re-queried.
"""
import hashlib
import json
from experiments import det5_joint_height_interval as driver

SOURCE = driver.ARCHIVE
ARCHIVE = driver.ROOT / 'results/det5_joint_continuation.json'


def main():
    raw = SOURCE.read_bytes()
    if not ARCHIVE.exists():
        data = json.loads(raw)
        data['continuation_seed'] = {
            'path':str(SOURCE.relative_to(driver.ROOT)),
            'sha256':hashlib.sha256(raw).hexdigest(),
            'query_count':len(data['queries'])}
        ARCHIVE.write_text(json.dumps(data,indent=2)+'\n')
    else:
        data = json.loads(ARCHIVE.read_text())
        if data['continuation_seed']['sha256'] != hashlib.sha256(raw).hexdigest():
            raise ValueError('Published seed changed')
    driver.ARCHIVE = ARCHIVE
    try:
        driver.main()
    finally:
        if SOURCE.read_bytes() != raw:
            raise ValueError('Published seed archive was modified')


if __name__ == '__main__':
    main()
